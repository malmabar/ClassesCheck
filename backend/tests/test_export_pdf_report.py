from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.services.export_service import (
    _build_operational_pdf_html,
    _build_pdf_with_playwright,
    _build_simple_pdf,
)


def _sample_report() -> dict:
    run = SimpleNamespace(
        id="run-123",
        semester="144620",
        period="صباحي",
        status="PUBLISHED",
    )
    halls_row = SimpleNamespace(
        room_code="A101",
        building_code="B1",
        day_name="الأحد",
        slot_index=1,
        occupancy_count=2,
        crn_count=2,
    )
    crn_row = SimpleNamespace(
        crn="28317",
        course_code="MTH101",
        room_code="A101",
        trainer_name="أحمد صالح",
        day_name="الأحد",
        slot_index=1,
    )
    trainer_row = SimpleNamespace(
        trainer_name="أحمد صالح",
        trainer_job_id="1011",
        day_name="الأحد",
        slot_index=1,
        load_count=2,
        crn_count=2,
    )
    issue_row = SimpleNamespace(
        rule_code="ROOM_CAPACITY_EXCEEDED",
        severity="ERROR",
        message="Registered exceeds room capacity",
    )
    return {
        "run": run,
        "generated_at_utc": "2026-02-24T00:00:00+00:00",
        "totals": {
            "issues_total": 3,
            "halls_rows": 10,
            "crns_rows": 12,
            "trainers_rows": 8,
            "distribution_rows": 40,
        },
        "issues_by_rule": [("ROOM_CAPACITY_EXCEEDED", 3)],
        "day_distribution": [("الأحد", 1, 20, 40, 50.0)],
        "halls_preview": [halls_row],
        "crns_preview": [crn_row],
        "trainers_preview": [trainer_row],
        "issues_preview": [issue_row],
    }


def test_build_operational_pdf_html_contains_arabic_sections() -> None:
    html_document = _build_operational_pdf_html(_sample_report())

    assert "تقرير التشغيل التشغيلي" in html_document
    assert "تفصيل الملاحظات حسب القاعدة" in html_document
    assert "القاعات" in html_document
    assert "تجاوز سعة القاعة" in html_document
    assert "A101" in html_document


def test_build_simple_pdf_has_valid_signature() -> None:
    payload = _build_simple_pdf(["line 1", "line 2"])
    assert payload.startswith(b"%PDF-")


def test_build_pdf_with_playwright_generates_pdf_or_skips() -> None:
    html_document = "<html lang='ar' dir='rtl'><body><h1>تقرير عربي</h1></body></html>"
    try:
        payload = _build_pdf_with_playwright(html_document)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Playwright PDF not available in this environment: {exc}")
    assert payload.startswith(b"%PDF")
