from __future__ import annotations

from types import SimpleNamespace

from app.services.check_service import _collect_pair_conflicts


def _code(code_id: int):
    return SimpleNamespace(id=code_id)


def test_collect_pair_conflicts_collapses_repeated_slot_overlaps() -> None:
    c1 = _code(1)
    c2 = _code(2)
    grouped_by_slot = {
        ("T100", 1, 1): [c1, c2],
        ("T100", 1, 2): [c1, c2],
        ("T100", 1, 3): [c1, c2],
    }

    result = _collect_pair_conflicts(grouped_by_slot)

    assert result == {("T100", 1, 1, 2): [1, 2, 3]}


def test_collect_pair_conflicts_builds_unique_pairs_for_group_size_three() -> None:
    c1 = _code(11)
    c2 = _code(22)
    c3 = _code(33)
    grouped_by_slot = {
        ("R-A", 2, 4): [c1, c2, c3],
        ("R-A", 2, 5): [c1, c2],
    }

    result = _collect_pair_conflicts(grouped_by_slot)

    assert result == {
        ("R-A", 2, 11, 22): [4, 5],
        ("R-A", 2, 11, 33): [4],
        ("R-A", 2, 22, 33): [4],
    }
