from __future__ import annotations

import hashlib
import html
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import PROJECT_ROOT
from app.models.issues import MCIssue
from app.models.publish import (
    MCPublishCRNsCopy,
    MCPublishDistribution,
    MCPublishHallsCopy,
    MCPublishTrainersSC,
)
from app.models.run import MCRun, MCRunLog, MCRunOutputArtifact
from app.services.publish_service import publish_run_outputs
from app.services.schema_guard import ensure_publish_schema


EXPORTS_ROOT = PROJECT_ROOT / "artifacts" / "exports"
PDF_PREVIEW_LIMIT = 40

RULE_LABELS_AR = {
    "TRAINER_TIME_CONFLICT": "تعارض وقت المدرب",
    "ROOM_TIME_CONFLICT": "تعارض وقت القاعة",
    "ROOM_CAPACITY_EXCEEDED": "تجاوز سعة القاعة",
}


def _sanitize_file_token(value: str, fallback: str = "na") -> str:
    text = re.sub(r"\s+", "_", str(value or "").strip())
    text = re.sub(r"[^A-Za-z0-9_.-]+", "", text)
    return text or fallback


def _period_token(period: str) -> str:
    if period == "صباحي":
        return "morning"
    if period == "مسائي":
        return "evening"
    return "period"


def _relative_storage_path(file_path: Path) -> str:
    try:
        return str(file_path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(file_path)


def _ensure_published(db: Session, run: MCRun, triggered_by: str) -> None:
    published_halls = db.scalar(
        select(func.count())
        .select_from(MCPublishHallsCopy)
        .where(MCPublishHallsCopy.run_id == run.id)
    ) or 0
    if published_halls > 0:
        return
    publish_run_outputs(db=db, run_id=run.id, triggered_by=triggered_by)


def _register_artifact(
    db: Session,
    run_id: str,
    artifact_type: str,
    content_type: str,
    file_path: Path,
) -> MCRunOutputArtifact:
    payload = file_path.read_bytes()
    checksum = hashlib.sha256(payload).hexdigest()
    artifact = MCRunOutputArtifact(
        run_id=run_id,
        artifact_type=artifact_type,
        file_name=file_path.name,
        content_type=content_type,
        file_size=len(payload),
        checksum=checksum,
        storage_path=_relative_storage_path(file_path),
    )
    db.add(artifact)
    db.flush()
    return artifact


def _column_ref(index: int) -> str:
    letters = []
    current = index
    while current > 0:
        current, remainder = divmod(current - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def _xml_cell(cell_ref: str, value: object) -> str:
    if value is None:
        return f'<c r="{cell_ref}"/>'
    if isinstance(value, bool):
        return f'<c r="{cell_ref}" t="b"><v>{1 if value else 0}</v></c>'
    if isinstance(value, (int, float)):
        return f'<c r="{cell_ref}"><v>{value}</v></c>'
    raw_text = str(value)
    text = html.escape(raw_text)
    space_attr = ' xml:space="preserve"' if raw_text != raw_text.strip() else ""
    return f'<c r="{cell_ref}" t="inlineStr"><is><t{space_attr}>{text}</t></is></c>'


def _sheet_xml(rows: Sequence[Sequence[object]]) -> bytes:
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>',
    ]
    for row_idx, row in enumerate(rows, start=1):
        parts.append(f'<row r="{row_idx}">')
        for col_idx, value in enumerate(row, start=1):
            parts.append(_xml_cell(f"{_column_ref(col_idx)}{row_idx}", value))
        parts.append("</row>")
    parts.append("</sheetData></worksheet>")
    return "".join(parts).encode("utf-8")


def _build_xlsx(sheet_specs: Sequence[tuple[str, Sequence[Sequence[object]]]]) -> bytes:
    unique_names: list[str] = []
    used: set[str] = set()
    for idx, (name, _) in enumerate(sheet_specs, start=1):
        base = re.sub(r"[\[\]:*?/\\]", "_", str(name or f"Sheet{idx}")).strip()[:31] or f"Sheet{idx}"
        candidate = base
        suffix = 1
        while candidate in used:
            suffix += 1
            candidate = f"{base[: max(0, 31 - len(str(suffix)) - 1)]}_{suffix}"
        used.add(candidate)
        unique_names.append(candidate)

    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx in range(1, len(sheet_specs) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    workbook_parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>',
    ]
    for idx, name in enumerate(unique_names, start=1):
        workbook_parts.append(
            f'<sheet name="{html.escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>'
        )
    workbook_parts.append("</sheets></workbook>")

    workbook_rels = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
    ]
    for idx in range(1, len(sheet_specs) + 1):
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{idx}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheet_specs) + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    workbook_rels.append("</Relationships>")

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill></fills>'
        "<borders count=\"1\"><border><left/><right/><top/><bottom/><diagonal/></border></borders>"
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )

    out = io.BytesIO()
    with zipfile.ZipFile(out, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", "".join(workbook_parts))
        zf.writestr("xl/_rels/workbook.xml.rels", "".join(workbook_rels))
        zf.writestr("xl/styles.xml", styles_xml)
        for idx, (_, rows) in enumerate(sheet_specs, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", _sheet_xml(rows))
    return out.getvalue()


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_simple_pdf(lines: Iterable[str]) -> bytes:
    text_lines = [str(line) for line in lines]
    content_parts = ["BT", "/F1 12 Tf", "50 560 Td"]
    for index, line in enumerate(text_lines):
        if index > 0:
            content_parts.append("0 -16 Td")
        encoded = line.encode("latin-1", "replace").decode("latin-1")
        content_parts.append(f"({_pdf_escape(encoded)}) Tj")
    content_parts.append("ET")
    stream = "\n".join(content_parts).encode("latin-1")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 842 595] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        b"5 0 obj\n<< /Length "
        + str(len(stream)).encode("ascii")
        + b" >>\nstream\n"
        + stream
        + b"\nendstream\nendobj\n",
    ]

    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(pdf.tell())
        pdf.write(obj)
    xref_start = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.write(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF"
        ).encode("ascii")
    )
    return pdf.getvalue()


def _format_value(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _rule_label(rule_code: str) -> str:
    code = str(rule_code or "").strip()
    return RULE_LABELS_AR.get(code, code or "-")


def _table_html(title: str, headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    table_rows = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(_format_value(cell))}</td>" for cell in row)
        table_rows.append(f"<tr>{cells}</tr>")
    if not table_rows:
        table_rows.append(f'<tr><td colspan="{len(headers)}">لا توجد بيانات</td></tr>')

    head_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body_html = "".join(table_rows)
    return (
        f'<section class="table-card">'
        f"<h3>{html.escape(title)}</h3>"
        f"<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table>"
        f"</section>"
    )


def _build_operational_pdf_html(report: dict) -> str:
    run = report["run"]
    totals = report["totals"]
    issues_by_rule = report["issues_by_rule"]
    day_distribution = report["day_distribution"]
    halls_preview = report["halls_preview"]
    crns_preview = report["crns_preview"]
    trainers_preview = report["trainers_preview"]
    issues_preview = report["issues_preview"]

    issue_rows = [[_rule_label(rule_code), total] for rule_code, total in issues_by_rule]
    day_rows = [
        [day_name, day_order, occupied_total, total_cells, f"{avg_ratio:.2f}%"]
        for day_name, day_order, occupied_total, total_cells, avg_ratio in day_distribution
    ]
    halls_rows = [
        [row.room_code, row.building_code, row.day_name, row.slot_index, row.occupancy_count, row.crn_count]
        for row in halls_preview
    ]
    crns_rows = [
        [row.crn, row.course_code, row.room_code, row.trainer_name, row.day_name, row.slot_index]
        for row in crns_preview
    ]
    trainers_rows = [
        [row.trainer_name, row.trainer_job_id, row.day_name, row.slot_index, row.load_count, row.crn_count]
        for row in trainers_preview
    ]
    issue_preview_rows = [
        [row.rule_code, row.severity, row.message]
        for row in issues_preview
    ]

    cards = [
        ("رقم التشغيل", run.id),
        ("الفصل", run.semester),
        ("الفترة", run.period),
        ("الحالة", run.status),
        ("إجمالي الملاحظات", totals["issues_total"]),
        ("صفوف القاعات", totals["halls_rows"]),
        ("صفوف الشعب", totals["crns_rows"]),
        ("صفوف المدربين", totals["trainers_rows"]),
        ("صفوف التوزيع", totals["distribution_rows"]),
        ("وقت التقرير (UTC)", report["generated_at_utc"]),
    ]
    cards_html = "".join(
        (
            '<article class="stat">'
            f"<span>{html.escape(label)}</span>"
            f"<strong>{html.escape(_format_value(value))}</strong>"
            "</article>"
        )
        for label, value in cards
    )

    sections = [
        _table_html("تفصيل الملاحظات حسب القاعدة", ["القاعدة", "العدد"], issue_rows),
        _table_html(
            "ملخص التوزيع اليومي",
            ["اليوم", "ترتيب اليوم", "إجمالي الخلايا المشغولة", "إجمالي الخلايا", "متوسط الإشغال"],
            day_rows,
        ),
        _table_html(
            f"القاعات (أول {PDF_PREVIEW_LIMIT} صف)",
            ["القاعة", "المبنى", "اليوم", "الفترة", "عدد الإشغال", "عدد الشعب"],
            halls_rows,
        ),
        _table_html(
            f"الشعب (أول {PDF_PREVIEW_LIMIT} صف)",
            ["CRN", "المقرر", "القاعة", "المدرب", "اليوم", "الفترة"],
            crns_rows,
        ),
        _table_html(
            f"المدربين (أول {PDF_PREVIEW_LIMIT} صف)",
            ["اسم المدرب", "رقم المدرب", "اليوم", "الفترة", "الحمل", "عدد الشعب"],
            trainers_rows,
        ),
        _table_html(
            f"أمثلة الملاحظات (أول {PDF_PREVIEW_LIMIT} صف)",
            ["القاعدة", "الشدة", "الرسالة"],
            issue_preview_rows,
        ),
    ]

    sections_html = "".join(sections)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <title>تقرير تشغيل Morning Classes Check</title>
  <style>
    @page {{
      size: A4;
      margin: 14mm 10mm;
    }}
    body {{
      font-family: "IBM Plex Sans Arabic", "Noto Sans Arabic", "Segoe UI", Tahoma, Arial, sans-serif;
      color: #1f2937;
      margin: 0;
      background: #f8fafc;
      font-size: 11px;
      line-height: 1.45;
    }}
    .header {{
      border: 1px solid #d1d5db;
      border-radius: 10px;
      background: #ffffff;
      padding: 10px 12px;
      margin-bottom: 10px;
    }}
    .header h1 {{
      margin: 0 0 4px;
      font-size: 20px;
      color: #065f46;
    }}
    .header p {{
      margin: 0;
      color: #4b5563;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-bottom: 10px;
    }}
    .stat {{
      border: 1px solid #d1d5db;
      border-radius: 8px;
      background: #fff;
      padding: 6px 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}
    .stat span {{
      color: #475569;
      font-size: 10px;
    }}
    .stat strong {{
      color: #0f172a;
      font-size: 12px;
      word-break: break-all;
    }}
    .table-card {{
      border: 1px solid #d1d5db;
      border-radius: 10px;
      background: #fff;
      margin-bottom: 10px;
      overflow: hidden;
    }}
    .table-card h3 {{
      margin: 0;
      padding: 8px 10px;
      background: #ecfeff;
      color: #0f172a;
      border-bottom: 1px solid #d1d5db;
      font-size: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      border: 1px solid #e5e7eb;
      padding: 4px 6px;
      text-align: right;
      vertical-align: top;
    }}
    th {{
      background: #f1f5f9;
      color: #111827;
      font-weight: 700;
    }}
    td {{
      color: #1f2937;
      word-break: break-word;
    }}
  </style>
</head>
<body>
  <section class="header">
    <h1>تقرير التشغيل التشغيلي</h1>
    <p>Morning Classes Check - تقرير عربي تفصيلي للمخرجات المنشورة</p>
  </section>
  <section class="stats">{cards_html}</section>
  {sections_html}
</body>
</html>
"""


def _build_pdf_with_playwright(html_document: str) -> bytes:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()
        page.set_content(html_document, wait_until="load")
        payload = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "12mm", "right": "8mm", "bottom": "12mm", "left": "8mm"},
            prefer_css_page_size=True,
        )
        browser.close()
        return payload


def _build_sheet_rows(db: Session, run_id: str) -> list[tuple[str, list[list[object]]]]:
    halls_rows = db.execute(
        select(MCPublishHallsCopy)
        .where(MCPublishHallsCopy.run_id == run_id)
        .order_by(
            MCPublishHallsCopy.room_code.asc(),
            MCPublishHallsCopy.day_order.asc(),
            MCPublishHallsCopy.slot_index.asc(),
        )
    ).scalars().all()
    crns_rows = db.execute(
        select(MCPublishCRNsCopy)
        .where(MCPublishCRNsCopy.run_id == run_id)
        .order_by(
            MCPublishCRNsCopy.crn.asc(),
            MCPublishCRNsCopy.day_order.asc(),
            MCPublishCRNsCopy.slot_index.asc(),
        )
    ).scalars().all()
    trainers_rows = db.execute(
        select(MCPublishTrainersSC)
        .where(MCPublishTrainersSC.run_id == run_id)
        .order_by(
            MCPublishTrainersSC.trainer_job_id.asc(),
            MCPublishTrainersSC.day_order.asc(),
            MCPublishTrainersSC.slot_index.asc(),
        )
    ).scalars().all()
    distribution_rows = db.execute(
        select(MCPublishDistribution)
        .where(MCPublishDistribution.run_id == run_id)
        .order_by(
            MCPublishDistribution.day_order.asc(),
            MCPublishDistribution.slot_index.asc(),
        )
    ).scalars().all()

    issues_total = db.scalar(
        select(func.count()).select_from(MCIssue).where(MCIssue.run_id == run_id)
    ) or 0
    issues_by_rule = dict(
        db.execute(
            select(MCIssue.rule_code, func.count())
            .where(MCIssue.run_id == run_id)
            .group_by(MCIssue.rule_code)
        ).all()
    )

    summary = [
        ["run_id", run_id],
        ["generated_at_utc", datetime.now(timezone.utc).isoformat()],
        ["issues_total", issues_total],
        ["trainer_time_conflict", int(issues_by_rule.get("TRAINER_TIME_CONFLICT", 0))],
        ["room_time_conflict", int(issues_by_rule.get("ROOM_TIME_CONFLICT", 0))],
        ["room_capacity_exceeded", int(issues_by_rule.get("ROOM_CAPACITY_EXCEEDED", 0))],
        ["halls_rows", len(halls_rows)],
        ["crns_rows", len(crns_rows)],
        ["trainers_rows", len(trainers_rows)],
        ["distribution_rows", len(distribution_rows)],
    ]

    halls = [
        [
            "room_code",
            "building_code",
            "day_name",
            "day_order",
            "slot_index",
            "occupancy_count",
            "crn_count",
            "crn_list",
        ]
    ]
    halls.extend(
        [
            row.room_code,
            row.building_code,
            row.day_name,
            row.day_order,
            row.slot_index,
            row.occupancy_count,
            row.crn_count,
            row.crn_list,
        ]
        for row in halls_rows
    )

    crns = [
        [
            "crn",
            "course_code",
            "course_name",
            "room_code",
            "trainer_job_id",
            "trainer_name",
            "day_name",
            "day_order",
            "slot_index",
            "occupancy_count",
        ]
    ]
    crns.extend(
        [
            row.crn,
            row.course_code,
            row.course_name,
            row.room_code,
            row.trainer_job_id,
            row.trainer_name,
            row.day_name,
            row.day_order,
            row.slot_index,
            row.occupancy_count,
        ]
        for row in crns_rows
    )

    trainers = [
        [
            "trainer_job_id",
            "trainer_name",
            "day_name",
            "day_order",
            "slot_index",
            "load_count",
            "crn_count",
            "crn_list",
        ]
    ]
    trainers.extend(
        [
            row.trainer_job_id,
            row.trainer_name,
            row.day_name,
            row.day_order,
            row.slot_index,
            row.load_count,
            row.crn_count,
            row.crn_list,
        ]
        for row in trainers_rows
    )

    distribution = [
        ["day_name", "day_order", "slot_index", "occupied_cells", "total_cells", "occupancy_ratio"]
    ]
    distribution.extend(
        [
            row.day_name,
            row.day_order,
            row.slot_index,
            row.occupied_cells,
            row.total_cells,
            row.occupancy_ratio,
        ]
        for row in distribution_rows
    )

    return [
        ("Summary", summary),
        ("Halls_Copy", halls),
        ("CRNs_Copy", crns),
        ("TrainersSC", trainers),
        ("Distribution", distribution),
    ]


def _collect_pdf_report_data(db: Session, run: MCRun) -> dict:
    run_id = run.id
    halls_rows = db.scalar(
        select(func.count()).select_from(MCPublishHallsCopy).where(MCPublishHallsCopy.run_id == run_id)
    ) or 0
    crns_rows = db.scalar(
        select(func.count()).select_from(MCPublishCRNsCopy).where(MCPublishCRNsCopy.run_id == run_id)
    ) or 0
    trainers_rows = db.scalar(
        select(func.count()).select_from(MCPublishTrainersSC).where(MCPublishTrainersSC.run_id == run_id)
    ) or 0
    distribution_rows = db.scalar(
        select(func.count()).select_from(MCPublishDistribution).where(MCPublishDistribution.run_id == run_id)
    ) or 0
    issues_total = db.scalar(select(func.count()).select_from(MCIssue).where(MCIssue.run_id == run_id)) or 0

    issues_by_rule = db.execute(
        select(MCIssue.rule_code, func.count())
        .where(MCIssue.run_id == run_id)
        .group_by(MCIssue.rule_code)
        .order_by(func.count().desc(), MCIssue.rule_code.asc())
    ).all()

    day_distribution = db.execute(
        select(
            MCPublishDistribution.day_name,
            MCPublishDistribution.day_order,
            func.sum(MCPublishDistribution.occupied_cells),
            func.max(MCPublishDistribution.total_cells),
            func.avg(MCPublishDistribution.occupancy_ratio),
        )
        .where(MCPublishDistribution.run_id == run_id)
        .group_by(MCPublishDistribution.day_name, MCPublishDistribution.day_order)
        .order_by(MCPublishDistribution.day_order.asc())
    ).all()

    halls_preview = db.execute(
        select(MCPublishHallsCopy)
        .where(MCPublishHallsCopy.run_id == run_id)
        .order_by(
            MCPublishHallsCopy.occupancy_count.desc(),
            MCPublishHallsCopy.crn_count.desc(),
            MCPublishHallsCopy.room_code.asc(),
        )
        .limit(PDF_PREVIEW_LIMIT)
    ).scalars().all()
    crns_preview = db.execute(
        select(MCPublishCRNsCopy)
        .where(MCPublishCRNsCopy.run_id == run_id)
        .order_by(
            MCPublishCRNsCopy.day_order.asc(),
            MCPublishCRNsCopy.slot_index.asc(),
            MCPublishCRNsCopy.crn.asc(),
        )
        .limit(PDF_PREVIEW_LIMIT)
    ).scalars().all()
    trainers_preview = db.execute(
        select(MCPublishTrainersSC)
        .where(MCPublishTrainersSC.run_id == run_id)
        .order_by(
            MCPublishTrainersSC.load_count.desc(),
            MCPublishTrainersSC.crn_count.desc(),
            MCPublishTrainersSC.trainer_job_id.asc(),
        )
        .limit(PDF_PREVIEW_LIMIT)
    ).scalars().all()
    issues_preview = db.execute(
        select(MCIssue)
        .where(MCIssue.run_id == run_id)
        .order_by(MCIssue.id.asc())
        .limit(PDF_PREVIEW_LIMIT)
    ).scalars().all()

    return {
        "run": run,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "issues_total": int(issues_total),
            "halls_rows": int(halls_rows),
            "crns_rows": int(crns_rows),
            "trainers_rows": int(trainers_rows),
            "distribution_rows": int(distribution_rows),
        },
        "issues_by_rule": issues_by_rule,
        "day_distribution": day_distribution,
        "halls_preview": halls_preview,
        "crns_preview": crns_preview,
        "trainers_preview": trainers_preview,
        "issues_preview": issues_preview,
    }


def export_run_xlsx(db: Session, run_id: str, triggered_by: str = "api-user") -> dict:
    ensure_publish_schema(db)

    run = db.get(MCRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    _ensure_published(db, run, triggered_by=triggered_by)
    sheets = _build_sheet_rows(db, run_id)
    payload = _build_xlsx(sheets)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semester_token = _sanitize_file_token(run.semester, fallback="semester")
    period_token = _period_token(run.period)
    file_name = f"mc_{semester_token}_{period_token}_{timestamp}.xlsx"

    output_dir = EXPORTS_ROOT / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / file_name
    file_path.write_bytes(payload)

    artifact = _register_artifact(
        db=db,
        run_id=run_id,
        artifact_type="EXPORT_XLSX",
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file_path=file_path,
    )
    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="EXPORT_XLSX",
            message="XLSX export generated successfully.",
            details_json='{"artifact_type":"EXPORT_XLSX"}',
        )
    )
    db.commit()

    return {
        "run_id": run_id,
        "artifact_id": artifact.id,
        "file_name": artifact.file_name,
        "content_type": artifact.content_type,
        "file_size": artifact.file_size,
        "checksum": artifact.checksum,
        "storage_path": artifact.storage_path,
        "absolute_path": str(file_path),
    }


def export_run_pdf(db: Session, run_id: str, triggered_by: str = "api-user") -> dict:
    ensure_publish_schema(db)

    run = db.get(MCRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    _ensure_published(db, run, triggered_by=triggered_by)
    report_data = _collect_pdf_report_data(db=db, run=run)
    html_document = _build_operational_pdf_html(report_data)

    build_mode = "playwright"
    fallback_error = None
    try:
        payload = _build_pdf_with_playwright(html_document)
    except Exception as exc:  # noqa: BLE001
        build_mode = "fallback_simple_pdf"
        fallback_error = f"{exc.__class__.__name__}: {exc}"
        totals = report_data["totals"]
        fallback_lines = [
            "Morning Classes Check - Operational Run Report",
            f"Run ID: {run.id}",
            f"Semester: {run.semester}",
            f"Period: {run.period}",
            f"Status: {run.status}",
            f"Issues Total: {totals['issues_total']}",
            f"Halls Rows: {totals['halls_rows']}",
            f"CRNs Rows: {totals['crns_rows']}",
            f"Trainers Rows: {totals['trainers_rows']}",
            f"Distribution Rows: {totals['distribution_rows']}",
            f"Generated UTC: {report_data['generated_at_utc']}",
            "Render Mode: fallback_simple_pdf",
        ]
        payload = _build_simple_pdf(fallback_lines)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    semester_token = _sanitize_file_token(run.semester, fallback="semester")
    period_token = _period_token(run.period)
    file_name = f"mc_{semester_token}_{period_token}_{timestamp}.pdf"

    output_dir = EXPORTS_ROOT / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / file_name
    file_path.write_bytes(payload)

    artifact = _register_artifact(
        db=db,
        run_id=run_id,
        artifact_type="EXPORT_PDF",
        content_type="application/pdf",
        file_path=file_path,
    )
    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="EXPORT_PDF",
            message="PDF export generated successfully.",
            details_json=json.dumps(
                {
                    "artifact_type": "EXPORT_PDF",
                    "mode": build_mode,
                    "fallback_error": fallback_error,
                },
                ensure_ascii=False,
            ),
        )
    )
    db.commit()

    return {
        "run_id": run_id,
        "artifact_id": artifact.id,
        "file_name": artifact.file_name,
        "content_type": artifact.content_type,
        "file_size": artifact.file_size,
        "checksum": artifact.checksum,
        "storage_path": artifact.storage_path,
        "absolute_path": str(file_path),
    }
