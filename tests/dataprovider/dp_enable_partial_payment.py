"""Enable Partial Payment test data for CoFee.

Threshold confirmed live 2026-07-16: splitRequiredAmountMin = 2000,
inclusive (>=). See docs/context/cofee-enable-partial-payment-context.md.
"""

from __future__ import annotations

import time

import pytest

# Confirmed live: >= this amount shows "Enable Partial Payment"; below does not.
PARTIAL_PAYMENT_THRESHOLD = 2000


def _unique_suffix() -> str:
    """Short unique suffix for parallel-safe test data."""
    return str(int(time.time() * 1000))[-8:]


def _member_mobile(suffix: str) -> str:
    """10-digit generated mobile matching dp_create_group.py's convention."""
    return f"6{suffix}"[:10].ljust(10, "0")


def get_threshold_boundary_test_data() -> list:
    """Parametrized data for TC-enable-partial-payment-NEG-01.

    One row just below the threshold (option must be absent), one row
    exactly at the threshold (option must be present) — both confirmed live.
    Each row gets its own fresh group/member so the two cases can't collide.
    """
    below_suffix = _unique_suffix()
    at_suffix = _unique_suffix() + "1"  # distinguishing tail — avoids same-millisecond collision
    return [
        pytest.param(
            f"AutoGroup{below_suffix}",
            f"AutoMember{below_suffix}",
            _member_mobile(below_suffix),
            f"NegBelow{below_suffix}",
            PARTIAL_PAYMENT_THRESHOLD - 1,
            False,
            id="below_threshold_no_option",
        ),
        pytest.param(
            f"AutoGroup{at_suffix}",
            f"AutoMember{at_suffix}",
            _member_mobile(at_suffix),
            f"NegAt{at_suffix}",
            PARTIAL_PAYMENT_THRESHOLD,
            True,
            id="at_threshold_option_present",
        ),
    ]


def get_invalid_partial_amount_test_data(pending_amount: int = 5000) -> list:
    """Parametrized data for TC-enable-partial-payment-NEG-02.

    Only the way-over-pending row is live-confirmed; the rest are
    [Assumption] per the test case doc — verify during automation.
    Not yet wired into a test (Mark As Paid automation deferred).
    """
    return [
        pytest.param(pending_amount * 2, id="way_over_pending"),
        pytest.param(pending_amount, id="exact_boundary_equal_pending"),
        pytest.param(0, id="zero_amount"),
        pytest.param(-100, id="negative_amount"),
    ]


def get_enable_partial_payment_test_data() -> list:
    """Parametrized data for TC-enable-partial-payment-HP-01 (runtime-unique)."""
    suffix = _unique_suffix()
    return [
        pytest.param(
            f"AutoGroup{suffix}",
            f"AutoMember{suffix}",
            _member_mobile(suffix),
            f"HpEnable{suffix}",
            5000,
            id="eligible_payment_5000",
        )
    ]


def get_entry_point_test_data() -> list:
    """Parametrized data for TC-enable-partial-payment-HP-04 — one fresh
    group/member/payment per entry point, all at the confirmed threshold."""
    entry_points = ("member_history", "group_payments", "all_payments")
    data = []
    for entry_point in entry_points:
        suffix = _unique_suffix()
        data.append(
            pytest.param(
                f"AutoGroup{suffix}",
                f"AutoMember{suffix}",
                _member_mobile(suffix),
                f"Hp04{entry_point[:4]}{suffix}",
                PARTIAL_PAYMENT_THRESHOLD,
                entry_point,
                id=f"entry_point_{entry_point}",
            )
        )
    return data
