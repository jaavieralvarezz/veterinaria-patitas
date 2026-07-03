from datetime import date, time

import pytest

from patitas.validation import is_open_day, is_open_time, validate_appointment


def test_clinic_opens_monday_to_saturday():
    assert is_open_day(date(2026, 7, 4))
    assert not is_open_day(date(2026, 7, 5))


def test_clinic_accepts_hours_between_9_and_21_included():
    assert is_open_time(time(9, 0))
    assert is_open_time(time(21, 0))
    assert not is_open_time(time(8, 59))
    assert not is_open_time(time(21, 1))


def test_validate_appointment_requires_reason():
    with pytest.raises(ValueError, match="motivo"):
        validate_appointment(date(2026, 7, 4), time(10, 0), "")


def test_validate_appointment_rejects_sunday():
    with pytest.raises(ValueError, match="domingos"):
        validate_appointment(date(2026, 7, 5), time(10, 0), "Revision")

