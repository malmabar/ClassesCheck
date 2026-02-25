from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = PROJECT_ROOT / "backend" / "app" / "ui"


def test_index_html_uses_local_assets_only() -> None:
    html = (UI_ROOT / "index.html").read_text(encoding="utf-8")

    assert "/ui/scripts/lucide.local.js" in html
    assert "/ui/scripts/dashboard.js" in html

    forbidden_hosts = [
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "unpkg.com",
        "jsdelivr.net",
        "cdnjs.cloudflare.com",
    ]
    for host in forbidden_hosts:
        assert host not in html


def test_local_font_and_icon_assets_are_present() -> None:
    tokens = (UI_ROOT / "styles" / "tokens.css").read_text(encoding="utf-8")

    assert "/ui/assets/fonts/SFArabic.ttf" in tokens
    assert (UI_ROOT / "assets" / "fonts" / "SFArabic.ttf").exists()
    assert (UI_ROOT / "scripts" / "lucide.local.js").exists()
