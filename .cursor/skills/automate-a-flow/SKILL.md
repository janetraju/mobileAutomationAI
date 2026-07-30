# Automate a Flow

Orchestrate one approved test scenario into working E2E automation: validate prerequisites, walk the flow on device, then hand off layer coding.

This skill owns **sequencing and gating** only. Locator discovery → **`discover-mobile-locators`**. Layer files → **`mobile-appium-python`**. Repo rules → **AGENTS.md**.

## When to Use

Use this skill when:

- The user says "automate this" or "implement this flow"
- You have an approved test case id from `docs/context/*-testcases.md`
- Starting a new end-to-end scenario from scratch

Do **not** use for editing a single PO or step file — go directly to **`mobile-appium-python`**.

## Workflow

### Step 1 — Review Inputs

Read:

**Required**

- `AGENTS.md`
- Approved `docs/context/<app_slug>-<feature>-testcases.md` or flow doc P0 row
- `docs/<app_slug>-flow.md`

**Search before creating**

```text
src/page_objects/<app_slug>/   src/page_actions/<app_slug>/   src/steps/<app_slug>/
tests/dataprovider/            tests/test/<app_slug>/         docs/locators/
docs/context/
```

Reuse existing steps when they exist (e.g. `user_ensures_logged_in_home`).

### Step 2 — Validate Prerequisites

Do not author downstream flows (groups, payments, …) until upstream passes on device:

| Check | How |
| ----- | --- |
| Emulator + Appium | `invoke appium:doctor` |
| App installed | `invoke app:install` |
| Login P0 | Login tests pass on clean emulator |
| Credentials | Whitelisted `TEST_MOBILE` · `TEST_OTP` in `.env` — see `setup-mobile-test-data` |

Run login first if the flow depends on it. Do not assume session-reuse helpers mask infra gaps.

### Step 3 — Parse the Scenario

Record: feature, priority (`p0`/`p1`/`p2`), steps, observable assertions, test data, preconditions.

Product source tells you **what** to automate; the device dump tells you **how** to find elements.

### Step 4 — Walk Flow on Device (mandatory for new TCs)

**No new test or PO until the scenario is walked live.**

Run **`discover-mobile-locators`** MCP walkthrough. Summarize before coding:

```text
- Screens visited (order)
- Key UI strings confirmed
- Locator notes per screen
- Overlays / quirks
- Gaps vs flow doc
```

Optional: Figma/Jira from `get-context` for **copy only** — never for locators.

### Step 5 — Implement Layers

Hand off to **`mobile-appium-python`**:

```text
page_objects → page_actions → steps → dataprovider → test
```

| Situation | Action |
| --------- | ------ |
| Steps already exist | Wire test + dataprovider only |
| New screen | Dump → PO → actions → steps → test |
| Locator drift | Fix one PO field; grep duplicates |

**Done when:** MCP walk complete, no invented locators, steps before test, markers per **AGENTS.md**.

### Step 6 — Verify

Run upstream regressions first:

```bash
invoke test --markers "login and p0"
invoke test --markers "<new_feature_marker>"
invoke test --markers "e2e and p0"
```

Then **`read-test-reports`** for Allure triage. On failure: re-dump — do not add `time.sleep()`.

### Step 7 — Update Knowledge on Failure

Fix code **and** record reusable learnings — see **`read-test-reports`** for which skill owns which failure type.

Append process-level pitfalls under **Known pitfalls** in this skill. App-specific quirks → `docs/<app_slug>-flow.md` Known Blockers.

## Rules

- Never write a new TC without Step 4 device walkthrough.
- Never write downstream tests before login P0 passes.
- Do not restate layer or locator rules — **AGENTS.md** owns those.
- Skip skill updates only for one-off environment issues.

## Known Pitfalls (process-level)

- **`pm clear` mid-session kills UiAutomator2** — quit session before clearing app data; recreate driver after relaunch.
- **Emulator cold boot ~300s** — set `AVD_NAME`; don't assume short boot timeouts.
- **Google phone picker** can intercept phone fields — dismiss before typing.

## Related Skills

- `get-context`
- `extract-p0-test-cases`
- `discover-mobile-locators`
- `setup-mobile-test-data`
- `mobile-appium-python`
- `read-test-reports`
- `pr-review-changes`
