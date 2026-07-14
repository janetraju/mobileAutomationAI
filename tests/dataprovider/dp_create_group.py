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


def get_create_group_test_data() -> list:
    """Return parametrized create-group data with runtime-unique names."""
    suffix = _unique_suffix()
    member_name = f"AutoMember{suffix}"
    member_mobile = f"6{suffix}"[:10].ljust(10, "0")
    group_name = f"AutoGroup{suffix}"
    amount = "5000"
    formatted_fee = format_indian_currency(amount)
    return [
        pytest.param(
            member_name,
            member_mobile,
            group_name,
            amount,
            formatted_fee,
            id="manual_member_fixed_fee",
        )
    ]
