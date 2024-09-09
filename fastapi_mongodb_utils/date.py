# -*- coding: utf-8 -*-
__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"

from datetime import datetime, timedelta, timezone
from typing import Collection

from dateutil.parser import ParserError, parse


def datetime_to_iso8601_with_z_suffix(value: datetime) -> str:
    """
    Convert datetime to ISO 8601 with Z suffix.

    Args:
        value (datetime): datetime object to be converted.

    Returns:
        str: ISO 8601 formatted datetime with Z suffix.
    """
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    formatted_datetime: str = value.isoformat()
    if formatted_datetime.endswith("+00:00"):
        formatted_datetime = formatted_datetime[:-6] + "Z"
    return formatted_datetime


def day_of_week_to_int(day_of_week: str | int) -> int:
    """Convert day of week to int."""
    if isinstance(day_of_week, int) and day_of_week in range(7):
        return day_of_week

    try:
        return int(day_of_week)
    except ValueError:
        pass

    try:
        datetime_of_the_week = parse(day_of_week)  # type: ignore
        return datetime_of_the_week.weekday()
    except ParserError:
        pass

    raise ValueError(f"Invalid day of the week: {day_of_week}")


def days_of_week_to_int(days_of_week: Collection[str | int]) -> set[int]:
    """Convert days of week to int."""
    return {day_of_week_to_int(day_of_week) for day_of_week in days_of_week}


def days_since(timestamp: str | datetime) -> int:
    """Get the number of days since a timestamp."""
    if isinstance(timestamp, str):
        timestamp = str_to_datetime(timestamp)
    return (now() - timestamp).days


def is_today_not_in_days_of_week(days_of_week: Collection[str | int]) -> bool:
    """Check if today is not in the days of week."""
    return now().weekday() not in days_of_week_to_int(days_of_week)


def normalize_str_datetime(value: str) -> str:
    """Convert string to normalized datetime in str."""
    return datetime_to_iso8601_with_z_suffix(str_to_datetime(value))


def now(tz: timezone = timezone.utc, **kwargs) -> datetime:
    """
    Get current datetime with timezone.

    Args:
        tz (timezone): timezone.
        **kwargs (dict): Arbitrary keyword arguments that will be passed to timedelta.

    Returns:
        datetime: current datetime object with timezone and offset.
    """
    now_datetime = datetime.now(tz)
    if kwargs:
        now_datetime += timedelta(**kwargs)
    return now_datetime


def now_str(**kwargs) -> str:
    """Get current datetime as string."""
    return datetime_to_iso8601_with_z_suffix(now(**kwargs))


def str_to_datetime(value: str) -> datetime:
    """Convert string to datetime."""
    parsed_datetime = parse(value)
    if parsed_datetime.tzinfo is None:
        parsed_datetime = parsed_datetime.replace(tzinfo=timezone.utc)
    return parsed_datetime
