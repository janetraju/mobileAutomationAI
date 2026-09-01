"""Map pytest-xdist workers to devices / Appium ports for safe parallel runs.

One parallel worker must own one device. Configure pools in env, for example:

    DEVICE_POOL=emulator-5554,emulator-5556,emulator-5558
    APPIUM_PORT_POOL=4723,4725,4727   # optional; one Appium server per worker

If APPIUM_PORT_POOL is unset, workers share APPIUM_HOST:APPIUM_PORT but get a
unique Android systemPort (and iOS wdaLocalPort) so UiAutomator2/WDA do not clash.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkerDeviceAssignment:
    """Resolved device/Appium binding for one xdist worker."""

    worker_id: str
    worker_index: int
    device_name: str
    udid: str
    appium_port: int | None
    android_system_port: int | None
    ios_wda_local_port: int | None


def parse_pool(raw: str | None) -> list[str]:
    """Split a comma-separated pool string into non-empty entries."""
    if not raw or not str(raw).strip():
        return []
    return [part.strip() for part in str(raw).split(",") if part.strip()]


def xdist_worker_index() -> int | None:
    """Return worker index (0 for gw0) or None when not under xdist."""
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    if not worker:
        return None
    if worker.startswith("gw") and worker[2:].isdigit():
        return int(worker[2:])
    raise ValueError(f"Unrecognized PYTEST_XDIST_WORKER value: {worker!r}")


def resolve_assignment(
    *,
    worker_index: int,
    device_pool: list[str],
    appium_port_pool: list[str],
    fallback_device: str | None,
    fallback_appium_port: int,
    system_port_base: int = 8200,
    wda_port_base: int = 8100,
) -> WorkerDeviceAssignment:
    """Pick device (and optional Appium port) for a worker index."""
    devices = device_pool or ([fallback_device] if fallback_device else [])
    if not devices:
        raise ValueError(
            "Parallel runs require DEVICE_POOL (or DEVICE_NAME). "
            "Example: DEVICE_POOL=emulator-5554,emulator-5556"
        )
    if worker_index >= len(devices):
        raise ValueError(
            f"Worker gw{worker_index} has no device: pool has {len(devices)} "
            f"device(s). Start more emulators or use -n {len(devices)} (or lower)."
        )

    device = devices[worker_index]
    appium_port: int | None = None
    android_system_port: int | None = None
    ios_wda_local_port: int | None = None

    if appium_port_pool:
        if worker_index >= len(appium_port_pool):
            raise ValueError(
                f"Worker gw{worker_index} has no Appium port: APPIUM_PORT_POOL has "
                f"{len(appium_port_pool)} port(s). Match DEVICE_POOL length or lower -n."
            )
        appium_port = int(appium_port_pool[worker_index])
    else:
        # Shared Appium server: isolate driver backends per worker.
        appium_port = fallback_appium_port
        android_system_port = system_port_base + worker_index
        ios_wda_local_port = wda_port_base + worker_index

    return WorkerDeviceAssignment(
        worker_id=f"gw{worker_index}",
        worker_index=worker_index,
        device_name=device,
        udid=device,
        appium_port=appium_port,
        android_system_port=android_system_port,
        ios_wda_local_port=ios_wda_local_port,
    )


def apply_device_pool_for_worker() -> WorkerDeviceAssignment | None:
    """Bind this process to a pool device when running under pytest-xdist.

    Mutates os.environ so Settings / capabilities pick up the assignment.
    Returns None for sequential (non-xdist) runs.
    """
    index = xdist_worker_index()
    if index is None:
        return None

    assignment = resolve_assignment(
        worker_index=index,
        device_pool=parse_pool(os.environ.get("DEVICE_POOL")),
        appium_port_pool=parse_pool(os.environ.get("APPIUM_PORT_POOL")),
        fallback_device=os.environ.get("DEVICE_NAME"),
        fallback_appium_port=int(os.environ.get("APPIUM_PORT", "4723")),
        system_port_base=int(os.environ.get("ANDROID_SYSTEM_PORT_BASE", "8200")),
        wda_port_base=int(os.environ.get("IOS_WDA_LOCAL_PORT_BASE", "8100")),
    )

    os.environ["DEVICE_NAME"] = assignment.device_name
    os.environ["UDID"] = assignment.udid
    if assignment.appium_port is not None:
        os.environ["APPIUM_PORT"] = str(assignment.appium_port)
    if assignment.android_system_port is not None:
        os.environ["ANDROID_SYSTEM_PORT"] = str(assignment.android_system_port)
    if assignment.ios_wda_local_port is not None:
        os.environ["IOS_WDA_LOCAL_PORT"] = str(assignment.ios_wda_local_port)

    return assignment
