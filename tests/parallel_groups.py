"""Named groups for tests that must not run concurrently with each other —
e.g. they share a device/session or mutate the same backend record. Apply
via `@pytest.mark.xdist_group(name=PARALLEL_GROUP_<X>)` so `pytest-xdist`
schedules them on the same worker instead of racing.

Add one constant per feature that needs isolation; do not reuse a group
across unrelated features.

Example:
    PARALLEL_GROUP_LOGIN = "login"
"""
