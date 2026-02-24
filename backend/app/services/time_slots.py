from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


VALID_PERIODS: tuple[str, str] = ("صباحي", "مسائي")

_ARABIC_DIGIT_MAP = {
    "٠": "0",
    "١": "1",
    "٢": "2",
    "٣": "3",
    "٤": "4",
    "٥": "5",
    "٦": "6",
    "٧": "7",
    "٨": "8",
    "٩": "9",
    "۰": "0",
    "۱": "1",
    "۲": "2",
    "۳": "3",
    "۴": "4",
    "۵": "5",
    "۶": "6",
    "۷": "7",
    "۸": "8",
    "۹": "9",
}

SLOT_TIME_RANGES: Dict[str, Sequence[Tuple[str, str]]] = {
    "صباحي": (
        ("08:00", "08:50"),
        ("09:00", "09:50"),
        ("10:00", "10:50"),
        ("11:00", "11:40"),
        ("12:30", "13:20"),
        ("13:21", "14:10"),
        ("14:15", "15:05"),
        ("15:06", "15:56"),
    ),
    "مسائي": (
        ("16:00", "16:50"),
        ("16:51", "17:41"),
        ("17:50", "18:40"),
        ("18:41", "19:31"),
        ("19:40", "20:30"),
        ("20:31", "21:21"),
        ("21:30", "22:20"),
        ("22:21", "23:11"),
    ),
}


@dataclass(frozen=True)
class TimeRange:
    start_hhmm: Optional[int]
    end_hhmm: Optional[int]
    start_min: Optional[int]
    end_min: Optional[int]


@dataclass(frozen=True)
class SlotResolution:
    period: str
    slot_indices: List[int]
    time_range: TimeRange


def normalize_digit_chars(value: Optional[str]) -> str:
    return str(value or "").translate(str.maketrans(_ARABIC_DIGIT_MAP))


def hhmm_to_minutes(hhmm: Optional[int]) -> Optional[int]:
    if not isinstance(hhmm, int):
        return None
    hours = hhmm // 100
    minutes = hhmm % 100
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return None
    return (hours * 60) + minutes


def parse_token_to_hhmm(token: Optional[str]) -> Optional[int]:
    normalized = normalize_digit_chars(token).strip()
    if not normalized:
        return None

    clock_match = re.match(r"^(\d{1,2})[:.](\d{2})$", normalized)
    if clock_match:
        hours = int(clock_match.group(1))
        minutes = int(clock_match.group(2))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return (hours * 100) + minutes
        return None

    digits = re.sub(r"[^0-9]", "", normalized)
    if len(digits) == 3:
        digits = f"0{digits}"
    if len(digits) < 4:
        return None
    candidate = int(digits[:4])
    return candidate if hhmm_to_minutes(candidate) is not None else None


def extract_hhmm_tokens(text_value: Optional[str]) -> List[int]:
    normalized = normalize_digit_chars(text_value)
    matches = re.findall(r"\d{1,2}[:.]\d{2}|\d{3,4}", normalized)
    out: List[int] = []
    for token in matches:
        hhmm = parse_token_to_hhmm(token)
        if isinstance(hhmm, int):
            out.append(hhmm)
    return out


def resolve_time_range(time_value: Optional[str], time_hhmm: Optional[int] = None) -> TimeRange:
    tokens = extract_hhmm_tokens(time_value)

    first: Optional[int] = tokens[0] if tokens else None
    if first is None and isinstance(time_hhmm, int):
        first = time_hhmm
    second: Optional[int] = tokens[1] if len(tokens) > 1 else None

    start_hhmm = first
    end_hhmm = second
    start_min = hhmm_to_minutes(start_hhmm)
    end_min = hhmm_to_minutes(end_hhmm)

    # Normalize reversed ranges (e.g. "1130 - 0900") to start<=end.
    if start_min is not None and end_min is not None and end_min < start_min:
        start_hhmm, end_hhmm = end_hhmm, start_hhmm
        start_min, end_min = end_min, start_min

    return TimeRange(
        start_hhmm=start_hhmm if isinstance(start_hhmm, int) else None,
        end_hhmm=end_hhmm if isinstance(end_hhmm, int) else None,
        start_min=start_min,
        end_min=end_min,
    )


def _clock_label_to_hhmm(label: str) -> int:
    hhmm = parse_token_to_hhmm(label)
    if hhmm is None:
        raise ValueError(f"Invalid slot label: {label}")
    return hhmm


def _build_schedule() -> Dict[str, Sequence[dict]]:
    out: Dict[str, Sequence[dict]] = {}
    for period, ranges in SLOT_TIME_RANGES.items():
        rows = []
        for idx, (start_label, end_label) in enumerate(ranges, start=1):
            start_hhmm = _clock_label_to_hhmm(start_label)
            end_hhmm = _clock_label_to_hhmm(end_label)
            rows.append(
                {
                    "slot": idx,
                    "start_hhmm": start_hhmm,
                    "end_hhmm": end_hhmm,
                    "start_min": hhmm_to_minutes(start_hhmm),
                    "end_min": hhmm_to_minutes(end_hhmm),
                }
            )
        out[period] = tuple(rows)
    return out


_SCHEDULE_BY_PERIOD = _build_schedule()


def get_schedule_for_period(period: Optional[str]) -> Sequence[dict]:
    if period == "مسائي":
        return _SCHEDULE_BY_PERIOD["مسائي"]
    return _SCHEDULE_BY_PERIOD["صباحي"]


def find_slot_by_time(period: str, hhmm: int) -> Optional[int]:
    schedule = get_schedule_for_period(period)
    for slot in schedule:
        if slot["start_hhmm"] == hhmm:
            return slot["slot"]
    minutes = hhmm_to_minutes(hhmm)
    if minutes is None:
        return None
    for slot in schedule:
        if minutes >= slot["start_min"] and minutes < slot["end_min"]:
            return slot["slot"]
    return None


def collect_overlapping_slots(period: str, time_range: TimeRange) -> List[int]:
    if time_range.start_min is None:
        return []

    effective_end = (
        time_range.end_min
        if time_range.end_min is not None and time_range.end_min > time_range.start_min
        else time_range.start_min + 1
    )

    slots: List[int] = []
    for slot in get_schedule_for_period(period):
        overlaps = time_range.start_min < slot["end_min"] and effective_end > slot["start_min"]
        if overlaps:
            slots.append(slot["slot"])
    return sorted(set(slots))


def infer_period_from_time_range(time_range: TimeRange) -> Optional[str]:
    morning_slots = collect_overlapping_slots("صباحي", time_range)
    evening_slots = collect_overlapping_slots("مسائي", time_range)
    if len(morning_slots) != len(evening_slots):
        return "صباحي" if len(morning_slots) > len(evening_slots) else "مسائي"

    hhmm_ref = time_range.start_hhmm if isinstance(time_range.start_hhmm, int) else time_range.end_hhmm
    if isinstance(hhmm_ref, int):
        return "مسائي" if hhmm_ref >= 1600 else "صباحي"
    return None


def _period_from_section_type(section_type: Optional[str]) -> Optional[str]:
    text = normalize_digit_chars(section_type).strip()
    if "صباح" in text:
        return "صباحي"
    if "مسائ" in text:
        return "مسائي"
    return None


def _ordered_unique(values: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def resolve_period_and_slots(
    *,
    time_value: Optional[str],
    time_hhmm: Optional[int],
    section_type: Optional[str],
    period_hint: Optional[str],
) -> SlotResolution:
    time_range = resolve_time_range(time_value, time_hhmm)
    inferred_period = infer_period_from_time_range(time_range)
    section_period = _period_from_section_type(section_type)
    valid_hint = period_hint if period_hint in VALID_PERIODS else None

    candidates = _ordered_unique(
        value
        for value in (inferred_period, section_period, valid_hint, "صباحي", "مسائي")
        if value in VALID_PERIODS
    )

    best_period = candidates[0] if candidates else "صباحي"
    best_slots: List[int] = []
    for period in candidates:
        slots = collect_overlapping_slots(period, time_range)
        if len(slots) > len(best_slots):
            best_slots = slots
            best_period = period

    if not best_slots and isinstance(time_range.start_hhmm, int):
        for period in candidates:
            slot = find_slot_by_time(period, time_range.start_hhmm)
            if slot is not None:
                best_period = period
                best_slots = [slot]
                break

    if not best_slots and isinstance(time_hhmm, int):
        for period in candidates:
            slot = find_slot_by_time(period, time_hhmm)
            if slot is not None:
                best_period = period
                best_slots = [slot]
                break

    return SlotResolution(
        period=best_period,
        slot_indices=sorted(set(best_slots)),
        time_range=time_range,
    )

