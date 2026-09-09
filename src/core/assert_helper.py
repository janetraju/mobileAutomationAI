"""Assertion helpers for the **tests** layer (and thin step wrappers) only —
never import this in `page_actions` or `page_objects`. Every helper asserts
an observable UI outcome (screen/copy/count/amount), not just "navigation
happened", and attaches context to Allure so a failure is triageable without
re-running the test.
"""

from __future__ import annotations

import allure


def assert_visible(page, by: str, value: str, message: str = "") -> None:
    visible = page.is_displayed(by, value)
    allure.attach(
        f"{by}={value} visible={visible}",
        name="assert_visible",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert visible, message or f"Expected element to be visible: {by}={value}"


def assert_text_equals(actual: str, expected: str, message: str = "") -> None:
    allure.attach(
        f"actual={actual!r} expected={expected!r}",
        name="assert_text_equals",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert actual == expected, message or f"Expected text {expected!r}, got {actual!r}"


def assert_text_contains(actual: str, expected_substring: str, message: str = "") -> None:
    allure.attach(
        f"actual={actual!r} expected_substring={expected_substring!r}",
        name="assert_text_contains",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert expected_substring in actual, (
        message or f"Expected {expected_substring!r} to be in {actual!r}"
    )


def assert_count(actual: int, expected: int, message: str = "") -> None:
    allure.attach(
        f"actual={actual} expected={expected}",
        name="assert_count",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert actual == expected, message or f"Expected count {expected}, got {actual}"


def assert_gone(page, by: str, value: str, message: str = "") -> None:
    gone = not page.is_displayed(by, value, timeout=3)
    allure.attach(
        f"{by}={value} gone={gone}",
        name="assert_gone",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert gone, message or f"Expected element to be gone: {by}={value}"
