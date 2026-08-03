"""Dues / All payments search test data for CoFee."""

from __future__ import annotations

import pytest


def get_dues_search_test_data() -> list:
    """Search queries expected to match an existing pending due.

    `user1` is a pre-seeded pending member on the shared Individual account
    (confirmed live on All payments → Pending). Search is case-insensitive in
    the UI; the card content-desc uses `User1` (UiAutomator match is
    case-sensitive).
    """
    return [
        pytest.param("user1", "User1", id="search_user1"),
    ]
