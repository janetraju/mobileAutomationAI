"""Unit tests for worker → device mapping (no Appium required)."""

from __future__ import annotations

import pytest

from src.core.device_pool import parse_pool, resolve_assignment


def test_parse_pool_splits_and_strips() -> None:
    assert parse_pool("emulator-5554, emulator-5556 ,") == [
        "emulator-5554",
        "emulator-5556",
    ]
    assert parse_pool(None) == []
    assert parse_pool("  ") == []


def test_resolve_assignment_maps_worker_to_device() -> None:
    assignment = resolve_assignment(
        worker_index=1,
        device_pool=["emulator-5554", "emulator-5556"],
        appium_port_pool=[],
        fallback_device="emulator-5554",
        fallback_appium_port=4723,
    )
    assert assignment.worker_id == "gw1"
    assert assignment.device_name == "emulator-5556"
    assert assignment.udid == "emulator-5556"
    assert assignment.appium_port == 4723
    assert assignment.android_system_port == 8201
    assert assignment.ios_wda_local_port == 8101


def test_resolve_assignment_uses_appium_port_pool() -> None:
    assignment = resolve_assignment(
        worker_index=0,
        device_pool=["emulator-5554", "emulator-5556"],
        appium_port_pool=["4723", "4725"],
        fallback_device=None,
        fallback_appium_port=4723,
    )
    assert assignment.appium_port == 4723
    assert assignment.android_system_port is None
    assert assignment.ios_wda_local_port is None


def test_resolve_assignment_fails_when_pool_too_small() -> None:
    with pytest.raises(ValueError, match="no device"):
        resolve_assignment(
            worker_index=2,
            device_pool=["emulator-5554", "emulator-5556"],
            appium_port_pool=[],
            fallback_device=None,
            fallback_appium_port=4723,
        )
