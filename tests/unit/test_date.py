# -*- coding: utf-8 -*-
__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"

__author__ = "CX Catalog Team"
__email__ = "cxcatalog-notifications@cisco.com"
__copyright__ = """
Copyright 2022, Cisco Systems, Inc.
All Rights Reserved.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""  # noqa
__status__ = "Production"


from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from fastapi_mongodb_utils.date import (
    datetime_to_iso8601_with_z_suffix,
    day_of_week_to_int,
    days_of_week_to_int,
    days_since,
    is_today_not_in_days_of_week,
    normalize_str_datetime,
    now,
    now_str,
    str_to_datetime,
)


class TestDateUtils:
    """Test date utils."""

    def test_datetime_to_iso8601_with_z_suffix_tz_aware(self):
        """Test datetime_to_iso8601_with_z_suffix with tz aware datetime."""
        dt = datetime(2022, 1, 1, tzinfo=timezone.utc)
        result = datetime_to_iso8601_with_z_suffix(dt)
        assert result == "2022-01-01T00:00:00Z"

    def test_datetime_to_iso8601_with_z_suffix_tz_naive(self):
        """Test datetime_to_iso8601_with_z_suffix with tz naive datetime."""
        dt = datetime(2022, 1, 1)
        result = datetime_to_iso8601_with_z_suffix(dt)
        assert result == "2022-01-01T00:00:00Z"

    @pytest.mark.parametrize(
        "value, expected_value, expected_excinfo_value",
        [
            pytest.param(
                "October 22, 2022",
                datetime(2022, 10, 22, tzinfo=timezone.utc),
                None,
                id="datetime_str",
            ),
            pytest.param(
                "invalid",
                None,
                "Unknown string format: invalid",
                id="invalid-date",
            ),
        ],
    )
    def test_str_to_datetime_invalid(
        self, value, expected_value, expected_excinfo_value
    ):
        """Test str_to_datetime with invalid datetime string."""
        if expected_excinfo_value:
            with pytest.raises(ValueError) as excinfo:
                str_to_datetime(value)
            assert str(excinfo.value) == expected_excinfo_value
        else:
            assert str_to_datetime(value) == expected_value

    @pytest.mark.parametrize(
        "kwargs",
        [
            pytest.param({}, id="no-kwargs"),
            pytest.param({"days": -1}, id="now-minus-1-day"),
        ],
    )
    def test_now(self, kwargs):
        """Test now function."""
        current_timestamp = now()
        modified_timestamp = now(**kwargs)
        delta = modified_timestamp - current_timestamp
        assert isinstance(modified_timestamp, datetime), "Expected datetime object"
        assert modified_timestamp.tzinfo == timezone.utc, "Expected timezone UTC"
        for key, value in kwargs.items():
            assert (
                getattr(delta, key) == value
            ), f"Expected {key} to be {value}, got {getattr(delta, key)}"

    def test_now_str(self):
        """Test now_str function."""
        current_timestamp = now_str()
        assert isinstance(current_timestamp, str)

    def test_day_of_week_to_int_valid_string(self):
        """Test day_of_week_to_int with a valid string."""
        result = day_of_week_to_int("Monday")
        assert result == 0

    def test_day_of_week_to_int_valid_integer(self):
        """Test day_of_week_to_int with a valid integer."""
        result = day_of_week_to_int(2)
        assert result == 2

    def test_day_of_week_to_int_invalid_string(self):
        """Test day_of_week_to_int with an invalid string."""
        with pytest.raises(ValueError) as excinfo:
            day_of_week_to_int("Invalid")
        assert str(excinfo.value) == "Invalid day of the week: Invalid"

    def test_days_of_week_to_int(self):
        """Test days_of_week_to_int function."""
        days_of_week = ["Monday", "Tuesday", "Wednesday"]
        result = days_of_week_to_int(days_of_week)
        assert result == {0, 1, 2}

    @pytest.mark.parametrize(
        "timestamp, expected_value",
        [
            pytest.param("2024-09-05T00:00:00Z", 0, id="0-days-str"),
            pytest.param(
                datetime(2024, 9, 5, tzinfo=timezone.utc), 0, id="0-days-datetime"
            ),
            pytest.param(datetime(2024, 8, 30, tzinfo=timezone.utc), 6, id="6-days"),
        ],
    )
    @patch("fastapi_mongodb_utils.date.now")
    def test_days_since_str(self, mocked_now, timestamp, expected_value):
        """Test days_since function."""
        mocked_now.return_value = datetime(2024, 9, 5, tzinfo=timezone.utc)
        assert days_since(timestamp) == expected_value

    @pytest.mark.parametrize(
        "today, days_of_week, expected_value",
        [
            pytest.param(
                datetime(2024, 9, 5, tzinfo=timezone.utc),
                {"Monday"},
                True,
                id="datetime-not-in-monday-set",
            ),
            pytest.param(
                datetime(2024, 9, 5, tzinfo=timezone.utc),
                ["Monday"],
                True,
                id="datetime-not-in-monday-array",
            ),
            pytest.param(
                datetime(2024, 9, 5, tzinfo=timezone.utc),
                ("Monday",),
                True,
                id="datetime-not-in-monday-tuple",
            ),
            pytest.param(
                datetime(2024, 9, 2, tzinfo=timezone.utc),
                {"Monday"},
                False,
                id="datetime-in-monday-set",
            ),
            pytest.param(
                datetime(2024, 9, 2, tzinfo=timezone.utc),
                ["Monday"],
                False,
                id="datetime-in-monday-array",
            ),
            pytest.param(
                datetime(2024, 9, 2, tzinfo=timezone.utc),
                ("Monday",),
                False,
                id="datetime-in-monday-tuple",
            ),
        ],
    )
    @patch("fastapi_mongodb_utils.date.now")
    def test_is_today_not_in_days_of_week(
        self, mocked_now, today, days_of_week, expected_value
    ):
        """Test is_today_not_in_days_of_week function."""
        mocked_now.return_value = today
        assert is_today_not_in_days_of_week(days_of_week) == expected_value

    @pytest.mark.parametrize(
        "value, expected_value",
        [
            pytest.param("2024-01-02", "2024-01-02T00:00:00Z", id="date-to-iso8601"),
            pytest.param(
                "2024-01-02T00:00:00+00:00",
                "2024-01-02T00:00:00Z",
                id="date-to-iso8601",
            ),
        ],
    )
    def test_normalize_str_datetime(self, value, expected_value):
        """Test normalize_str_datetime function."""
        assert normalize_str_datetime(value) == expected_value
