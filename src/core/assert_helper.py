"""Allure-wrapped assertion helpers for mobile UI tests."""

from __future__ import annotations

from typing import Any

import allure
from selenium.webdriver.remote.webelement import WebElement


@allure.step("Assert equals: {label}")
def assert_equals(actual: Any, expected: Any, label: str = "value") -> None:
    """Assert two values are equal."""
    assert actual == expected, f"{label}: expected {expected!r}, got {actual!r}"


@allure.step("Assert contains: {label}")
def assert_contains(haystack: str, needle: str, label: str = "text") -> None:
    """Assert needle is in haystack."""
    assert needle in haystack, f"{label}: expected {needle!r} in {haystack!r}"


@allure.step("Assert element visible: {description}")
def assert_element_visible(
    is_visible: bool,
    description: str = "element",
) -> None:
    """Assert element visibility flag is True."""
    assert is_visible, f"Expected {description} to be visible"


@allure.step("Assert element not visible: {description}")
def assert_element_not_visible(
    is_visible: bool,
    description: str = "element",
) -> None:
    """Assert element visibility flag is False."""
    assert not is_visible, f"Expected {description} to not be visible"


@allure.step("Assert toast message: {expected}")
def assert_toast_message(actual: str, expected: str) -> None:
    """Assert toast/snackbar message matches expected text."""
    assert expected in actual, f"Expected toast {expected!r}, got {actual!r}"


@allure.step("Assert text equals: {expected}")
def assert_text_equals(element: WebElement, expected: str) -> None:
    """Assert element text equals expected."""
    actual = element.text or ""
    assert actual == expected, f"Expected text {expected!r}, got {actual!r}"


@allure.step("Assert true: {message}")
def assert_true(condition: bool, message: str = "condition") -> None:
    """Assert condition is True."""
    assert condition, message


@allure.step("Assert false: {message}")
def assert_false(condition: bool, message: str = "condition") -> None:
    """Assert condition is False."""
    assert not condition, message
