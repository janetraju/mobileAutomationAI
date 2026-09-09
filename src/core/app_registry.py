"""Registry of every app this repo has been bootstrapped for.

`.env` (`APP_SLUG`) selects which one is *active* for a given run — this
registry is the durable record `create-mobile-framework-structure` writes to
each time a new app is onboarded, so re-running it for a second app doesn't
require rediscovering package/activity/type from scratch, and so other
tooling (docs, CI) can enumerate every app the repo knows about without
parsing `.env`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppEntry:
    slug: str
    name: str
    app_type: str  # native | flutter | rn | hybrid
    package: str | None = None  # Android application id
    activity: str | None = None  # Android launch activity
    bundle_id: str | None = None  # iOS bundle identifier
    min_sdk: int | None = None
    target_sdk: int | None = None


APP_REGISTRY: dict[str, AppEntry] = {
    "cofee": AppEntry(
        slug="cofee",
        name="CoFee",
        app_type="flutter",
        package="cofee.life.app.dev",
        activity="cofee.life.app.MainActivity",
        min_sdk=24,
        target_sdk=36,
    ),
}


def get_app_entry(slug: str) -> AppEntry:
    try:
        return APP_REGISTRY[slug]
    except KeyError as exc:
        known = ", ".join(sorted(APP_REGISTRY)) or "<none>"
        raise KeyError(f"App '{slug}' is not registered. Known apps: {known}") from exc
