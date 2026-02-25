from __future__ import annotations

from app.tools.responsive_gate import _eval_rules


def _base_metrics() -> dict:
    return {
        "doc": {"clientWidth": 1366, "scrollWidth": 1366},
        "layoutOverflow": {"maxRightOverflow": 0, "minLeft": -200},
        "selectedRect": {"width": 920, "top": 120},
        "controlsRect": {"width": 380, "top": 120},
        "controlsVisible": True,
        "screensRect": {"width": 900},
        "heatWrapRect": {"width": 860, "height": 300},
        "heatTableRect": {"width": 900},
        "bentoClass": "bento-grid",
    }


def test_eval_rules_passes_for_desktop_happy_path() -> None:
    metrics = _base_metrics()
    hidden = {
        "doc": {"clientWidth": 1366, "scrollWidth": 1366},
        "selectedRect": {"width": 1220},
        "controlsVisible": False,
        "bentoClass": "bento-grid controls-hidden",
    }
    failures = _eval_rules(metrics, viewport_width=1366, hidden_metrics=hidden)
    assert failures == []


def test_eval_rules_fails_on_large_horizontal_overflow() -> None:
    metrics = _base_metrics()
    metrics["layoutOverflow"]["maxRightOverflow"] = 84
    failures = _eval_rules(metrics, viewport_width=1366, hidden_metrics=None)
    assert any(item.startswith("page_horizontal_overflow_right=") for item in failures)


def test_eval_rules_fails_when_heatmap_too_narrow() -> None:
    metrics = _base_metrics()
    metrics["heatWrapRect"]["width"] = 300
    metrics["screensRect"]["width"] = 900
    failures = _eval_rules(metrics, viewport_width=1366, hidden_metrics=None)
    assert "heatmap_wrap_too_small_vs_screens_card" in failures
