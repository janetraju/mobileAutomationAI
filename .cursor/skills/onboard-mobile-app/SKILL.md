---
name: onboard-mobile-app
description: >-
  Onboard a new mobile app into this automation framework from an APK or IPA.
  Use when the user provides a new app binary, wants to configure APP_SLUG,
  update settings registry, rename scaffold folders, wire .env, or prepare
  the repo before locator discovery and test authoring.
---

# Onboard Mobile App

## When to use

- User drops APK/IPA in `builds/`
- Switching this repo to a different product
- After scaffold, before `discover-mobile-locators` or `mobile-appium-python`

## Read first

1. **`AGENTS.md`**
2. **`.env.example`**
3. **`src/core/settings.py`** → `APP_REGISTRY`

## Workflow

### 1. Analyze binary

```bash
bash scripts/analyze-apk.sh builds/<app>.apk
# or: invoke app:analyze --apk=builds/<app>.apk
```

Record (never commit secrets from bundled `.env`):

| Field | Source |
|-------|--------|
| `APP_NAME` | `application-label` |
| `APP_SLUG` | lowercase short name (e.g. `cofee`) |
| `APP_TYPE` | `native` / `flutter` / `rn` / `hybrid` from script output |
| `APP_PACKAGE` / `BUNDLE_ID` | badging |
| `APP_ACTIVITY` | `launchable-activity` (Android) |
| `API_BASE_URL` | bundled config or user input — **not** API keys/tokens |

Rename binary to `builds/<app_slug>-<env>.apk` (no spaces).

### 2. Update `APP_REGISTRY` in `src/core/settings.py`

Add entry keyed by `APP_SLUG` with `android` / `ios` env maps (`app_package`, `app_activity`, `bundle_id`, `api_base_url`).

### 3. Rename scaffold folders

If replacing placeholder `app_slug`:

```
src/page_objects/app_slug/   → src/page_objects/<app_slug>/
src/page_actions/app_slug/   → src/page_actions/<app_slug>/
src/steps/app_slug/          → src/steps/<app_slug>/
src/constants/app_slug/      → src/constants/<app_slug>/
data/app_slug/               → data/<app_slug>/
tests/test/app_slug/         → tests/test/<app_slug>/
docs/app_slug-flow.md        → docs/<app_slug>-flow.md
```

### 4. Update config files

| File | Changes |
|------|---------|
| `.env` / `.env.example` | `APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_PATH`, identifiers |
| `AGENTS.md` | Title, slug paths, skills table |
| `.cursor/skills/*/SKILL.md` | Replace `[APP NAME]` / `app_slug` references |
| `docs/<app_slug>-flow.md` | Stub with APK-derived hints (auth API paths, screen names) |

### 5. Seed flow doc (minimal)

From APK strings / manifest, draft **hypothesized** flows — mark as `Unconfirmed` until `discover-mobile-locators` runs.

### 6. Hand off

```
onboard-mobile-app  →  discover-mobile-locators  →  extract-p0-test-cases  →  setup-mobile-test-data  →  mobile-appium-python
```

## Rules

- Never commit real credentials or tokens extracted from APK
- Never hardcode product names outside `APP_REGISTRY` and `.env`
- Do not write `*_po.py` locators from APK alone — Flutter/RN need live dumps
- Keep `APP_TYPE` accurate — locator skill behavior depends on it

## Invoke helpers

```bash
invoke app:analyze --apk=builds/<slug>-dev.apk
invoke app:install --apk=builds/<slug>-dev.apk
invoke emulator:start
```
