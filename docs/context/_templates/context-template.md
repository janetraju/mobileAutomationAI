<!--
Copy to: docs/context/<app_slug>-<feature-slug>-context.md
Delete this comment block in the written file.
-->

# Context: <Feature name> (`<app_slug>-<feature-slug>`)

## Freshness

| Field | Value |
|-------|-------|
| Last updated | YYYY-MM-DD |
| Env checked | dev / stg / uat |
| Confirmed on device | yes / no |
| Owner | <name or team> |

## Source links (optional — fill when available)

| Source | Link / key | Status |
|--------|------------|--------|
| Jira | | Available / Partial / Not available |
| PRD | | Available / Partial / Not available |
| Figma | | Available / Partial / Not available |
| App source / walkthrough | | Available / Partial / Not available |

## Feature

| Field | Value |
|-------|-------|
| App slug | |
| Feature slug | |
| Platforms | android / ios |
| Account type | e.g. Individual |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| | |

## Happy path

1. …

## Business rules

- …

## Edge cases / unknowns

- … or **Unknown**

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | `TEST_MOBILE` / `TEST_OTP` in `.env` |
| | |

## Known product quirks

- …

## Existing automation

| Layer | Path |
|-------|------|
| Tests | |
| Steps / actions / POs | |

## Open questions

- …

## Handoff

Next: `testcase-generator` → approve `*-testcases.md` → `discover-mobile-locators` → `testscript-generator`.
