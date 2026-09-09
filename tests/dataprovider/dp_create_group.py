"""Test data for the Create Group (Fixed fee) scenario. No secrets — member
mobile numbers here are clearly-fake, non-production placeholders (per
AGENTS.md), not real accounts.
"""

from __future__ import annotations

import uuid

import pytest


def get_create_fixed_fee_group_test_data() -> list:
    return [
        pytest.param(
            {
                "member_name": f"QA Auto Member {uuid.uuid4().hex[:6]}",
                "member_mobile": "9000000099",
                "group_name": f"QA Auto {uuid.uuid4().hex[:8]}",
                "amount": "1500",
            },
            id="fixed_fee_group_happy_path",
        ),
    ]
