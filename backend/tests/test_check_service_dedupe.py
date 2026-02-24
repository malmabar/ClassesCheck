from __future__ import annotations

from types import SimpleNamespace

from app.services.check_service import _collect_code_conflicts


def _code(code_id: int):
    return SimpleNamespace(id=code_id)


def test_collect_code_conflicts_collapses_repeated_slot_overlaps() -> None:
    c1 = _code(1)
    c2 = _code(2)
    grouped_by_slot = {
        ("T100", 1, 1): [c1, c2],
        ("T100", 1, 2): [c1, c2],
        ("T100", 1, 3): [c1, c2],
    }

    result = _collect_code_conflicts(grouped_by_slot)

    assert result == {
        ("T100", 1, 1): {"peer_ids": [2], "slot_indices": [1, 2, 3]},
        ("T100", 1, 2): {"peer_ids": [1], "slot_indices": [1, 2, 3]},
    }


def test_collect_code_conflicts_merges_peers_and_slots_per_code() -> None:
    c1 = _code(11)
    c2 = _code(22)
    c3 = _code(33)
    grouped_by_slot = {
        ("R-A", 2, 4): [c1, c2, c3],
        ("R-A", 2, 5): [c1, c2],
    }

    result = _collect_code_conflicts(grouped_by_slot)

    assert result == {
        ("R-A", 2, 11): {"peer_ids": [22, 33], "slot_indices": [4, 5]},
        ("R-A", 2, 22): {"peer_ids": [11, 33], "slot_indices": [4, 5]},
        ("R-A", 2, 33): {"peer_ids": [11, 22], "slot_indices": [4]},
    }
