---
name: automate-a-flow
description: >-
  Orchestrate turning an approved test case or scenario into working E2E
  automation: validate prereqs, walk the flow on device via Appium MCP, then
  hand off layer coding to mobile-appium-python. Use when the user says
  "automate this", "implement this flow", or gives a TC to automate — not for
  editing a single PO/step file (use mobile-appium-python for that).
disable-model-invocation: true
---

# Automate a Flow

**Task:** turn **one approved scenario** into a working E2E test, in the
right order, with **live** locators — never invented ones.

**Repo contract:** [AGENTS.md](../../../AGENTS.md) (architecture, locators,
waits, markers). This skill owns *sequencing and gating* only — it does not
redefine how a layer file looks (`mobile-appium-python`), how to discover
locators (`discover-mobile-locators`), or how to read a report
(`read-test-reports`). Each is linked at the point it applies, not restated.

## When to use

- User says "automate this", "implement this flow", or hands you an approved TC id
- **Not** for editing a single PO/action/step file — go straight to `mobile-appium-python`

## Read first

1. [AGENTS.md](../../../AGENTS.md) — repo contract
2. Approved `docs/context/<app_slug>-<feature>-testcases.md`, **or** the flow doc's P0 row
3. `docs/<app_slug>-flow.md`
4. Existing code under `src/**/<app_slug>/` and `tests/test/<app_slug>/` — reuse before creating

---

## Step 0 — Prerequisites

Do not write a downstream test (groups, payments, …) until these pass on a
real device/emulator:

| Check | How |
|-------|-----|
| Emulator + Appium healthy | `invoke appium:doctor` |
| App installed | `invoke app:install` |
| Login works | Login P0 passes on a clean emulator — see `setup-mobile-test-data` for credentials/OTP strategy |

If the flow needs login, **run login first**. Don't rely on
`user_ensures_logged_in_home` to silently paper over broken infra.

---

## Step 1 — Parse the scenario

Write down: feature, priority (`p0`/`p1`/`p2`), steps (from approved
testcases or flow doc), assertions (observable UI success criteria), test
data source, preconditions.

**Search before creating anything new:**

```text
src/page_objects/<app_slug>/   src/page_actions/<app_slug>/   src/steps/<app_slug>/
tests/dataprovider/            tests/test/<app_slug>/         docs/locators/
docs/context/
```

Reuse existing steps when they exist (e.g. `user_ensures_logged_in_home`).
Product source tells you **what** to automate; the device dump tells you
**how** to find elements — don't conflate the two.

---

## Step 2 — Gather docs

1. Read the approved test cases or the flow doc's P0 matrix.
2. Grep existing POs/actions/steps/tests for this feature — list gaps
   (missing screens, locators, assertions), don't rebuild what exists.
3. Optional: Figma/Jira via `get-context` for **copy only** — never for locators.

---

## Step 3 — Walk the flow on device (mandatory for new TCs)

**No new test or PO until the scenario has been walked on a live
emulator/device.** The *how* (Appium MCP session setup, gestures, page
source capture, `generate_locators`) is entirely **`discover-mobile-locators`**'s
job — run it now if you haven't. This step is only the orchestration gate:

| Situation | Action |
|-----------|--------|
| New test case | Run `discover-mobile-locators`'s MCP walkthrough before Step 4 — no exceptions |
| Existing screen, no drift suspected | A quick re-check is still cheaper than a failed run — confirm before assuming |
| Downstream feature (e.g. payments after login) | Login P0 must already pass first |

Before moving to Step 4, summarize for the user: screens visited, key UI
strings confirmed, locator notes, any overlays/quirks hit, gaps vs. the flow doc.

---

## Step 4 — Implement

Layer order and file conventions are **`mobile-appium-python`**'s job —
don't restate them here, just follow its "Feature add order":

```text
page_objects → page_actions → steps → dataprovider → test
```

| Situation | Do this |
|-----------|---------|
| Steps already exist | Wire test + dataprovider only |
| New screen | Dump (Step 3) → PO → actions → steps → test |
| Locator drift | Fix the one PO field that drifted; grep for duplicate definitions elsewhere |
| Multi-screen flow | One step module calling several actions |

**Done when:** Step 3's walkthrough is complete, every locator is
live-confirmed (not guessed), steps exist before the test file, and
markers/Allure labels follow `AGENTS.md`.

---

## Step 5 — Verify

Run **upstream regressions first**, then the new flow — this ordering is
this skill's job; the actual `invoke` commands and report generation live
in `AGENTS.md` and **`read-test-reports`**:

```bash
invoke test --markers "login and p0"      # upstream — must stay green
invoke test --markers "<new_feature_marker>"
invoke test --markers "e2e and p0"        # full regression
```

Then see `read-test-reports` to generate/open the Allure report. On
failure: re-dump the screen (Step 3), don't add `time.sleep()` — see
`AGENTS.md` for wait strategy.

---

## Step 6 — On failure, update knowledge

Fix the code **and** record what you learned — unless it was a one-off
environment glitch. **Which skill owns which kind of failure knowledge is
`read-test-reports`'s triage table ("On failure — update skills")** — use
that, don't re-derive a second mapping here.

This skill's own share of that knowledge is process/orchestration-level
pitfalls (see **Known pitfalls** below) — not app-specific UI quirks, which
belong in `docs/<app_slug>-flow.md`'s Known Blockers instead.

Append under **Known pitfalls**:

```markdown
### Known pitfalls (updated YYYY-MM-DD)
- **Symptom:** …
  **Cause:** …
  **Fix:** …
```

---

## Don't do this

Repo-wide rules (sleeps, invented locators, wrong layer imports) live in
**AGENTS.md** — don't re-litigate them here. Orchestration-specific:

- Writing a new TC without the Step 3 device walkthrough
- Writing downstream tests before login P0 passes
- Skipping Step 0 prerequisites
- Fixing code without updating the owning skill when the failure teaches something reusable (see Step 6)

---

## Known pitfalls (process-level, app-agnostic — updated 2026-07-30)

App-specific quirks (e.g. CoFee's onboarding carousel, home nav labels, fee
assertions) live in `docs/<app_slug>-flow.md`'s Known Blockers, not here.

- **`pm clear` mid-session kills the UiAutomator2 server** — quit the
  Appium session before clearing app data, then create a fresh driver
  session after relaunching; don't `pm clear` under a live session.
- **Emulator cold boot can take ~300s** — set `AVD_NAME` explicitly; don't
  assume a fixed short timeout in `wait-for-device.sh`.
- **Android's phone-number autofill picker** (Google account phone
  suggestions) can intercept a phone-entry field — dismiss it before typing,
  don't assume the field is immediately interactable after screen load.

---

## Related skills

`get-context` · `testcase-generator` · `discover-mobile-locators` ·
`setup-mobile-test-data` · `mobile-appium-python` · `read-test-reports` ·
`pr-review-changes` · [AGENTS.md](../../../AGENTS.md)
