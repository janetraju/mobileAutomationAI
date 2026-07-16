"""Create group test data for CoFee."""

from __future__ import annotations

import time

import pytest


def _unique_suffix() -> str:
    """Short unique suffix for parallel-safe test data."""
    return str(int(time.time() * 1000))[-8:]


def format_indian_currency(amount: int | str) -> str:
    """Format amount as displayed in member card (e.g. 5000 -> 5,000)."""
    raw = str(amount).replace(",", "")
    value = int(raw)
    return f"{value:,}"


def _base_create_group_params(fee_schedule: str, case_id: str) -> pytest.param:
    suffix = _unique_suffix()
    member_name = f"AutoMember{suffix}"
    member_mobile = f"6{suffix}"[:10].ljust(10, "0")
    group_name = f"AutoGroup{suffix}"
    amount = "5000"
    formatted_fee = format_indian_currency(amount)
    return pytest.param(
        member_name,
        member_mobile,
        group_name,
        amount,
        formatted_fee,
        fee_schedule,
        id=case_id,
    )


def get_create_group_test_data() -> list:
    """Return parametrized create-group data (monthly last day — P0-03)."""
    return [_base_create_group_params("monthly_last_day", "manual_member_fixed_fee")]


def get_create_group_weekly_test_data() -> list:
    """Return create-group data with weekly Monday fee schedule — P0-04 (from product repo)."""
    return [
        _base_create_group_params("weekly_monday", "manual_member_weekly_monday")
    ]
