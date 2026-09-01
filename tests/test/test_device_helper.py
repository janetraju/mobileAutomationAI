"""Unit tests for DeviceHelper (no Appium session required)."""

from __future__ import annotations

from src.core.device_helper import _adb_bin


def test_adb_bin_returns_a_path_string() -> None:
    path = _adb_bin()
    assert isinstance(path, str)
    assert path.endswith("adb")
