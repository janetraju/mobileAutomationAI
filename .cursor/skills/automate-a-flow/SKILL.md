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

## What this skill does

Turns **one approved scenario** into a working E2E test — in the right order,
with **live** locators.

| This skill | Not this skill |
|------------|----------------|
| *When* / *in what order* to automate | *How* each layer file looks → **`mobile-appium-python`** |
| Prereqs → device walk → implement → verify | Editing one PO/step → **`mobile-appium-python`** |
| Repo rules | → **[AGENTS.md](../../../AGENTS.md)** Repo contract |

**Use when:** “automate this”, “implement this flow”, or an approved TC id.  
**Do not invent locators** — walk the flow on device first (Step 3).

---

## Big picture

```text
0. Prereqs OK?          emulator, app, login, credentials
1. Parse the scenario   steps, asserts, data, reuse existing code
2. Read docs            testcases / flow / existing layers
3. Walk on device       Appium MCP (mandatory for new TCs)
4. Implement layers     PO → actions → steps → data → test
5. Verify               login P0 → new test → report
6. On failure           fix code + update skill / flow blockers
```

---

## Before you start — read these

1. [AGENTS.md](../../../AGENTS.md) — Repo contract  
2. Approved `docs/context/<app_slug>-<feature>-testcases.md` **or** flow doc P0 row  
3. `docs/<app_slug>-flow.md`  
4. Existing code under `src/**/<app_slug>/` and `tests/test/<app_slug>/`

---

## Step 0 — Prerequisites

Do **not** write a downstream test (groups, payments, …) until these pass on a
real device/emulator.

| Check | How |
|-------|-----|
| Emulator + Appium | `invoke appium:doctor` |
| Device booted | `scripts/wait-for-device.sh` (`sys.boot_completed`) |
| App installed | `invoke app:install` (`APP_PATH` in `.env`) |
| Login works | Login P0 passes on a clean emulator |
| Home (if needed) | Dump/confirm home tiles |
| Credentials | `TEST_MOBILE` + `TEST_OTP` in `.env` (whitelisted) |

If the flow needs login, **run login first**. Do not rely on
`user_ensures_logged_in_home` to hide broken infra.

---

## Step 1 — Parse the scenario

Write down:

| Item | Example |
|------|---------|
| Feature | `login`, `groups`, `payments` |
| Priority | `p0` / `p1` / `p2` |
| Steps | From approved testcases or flow doc |
| Assertions | Observable UI success criteria |
| Test data | `.env` or `dp_<feature>.py` |
| Preconditions | Logged in? account type? |

**Search before creating** anything new:

```text
src/page_objects/<app_slug>/   src/page_actions/<app_slug>/   src/steps/<app_slug>/
tests/dataprovider/            tests/test/<app_slug>/         docs/locators/
docs/context/
```

Reuse steps when they exist (e.g. `user_ensures_logged_in_home`).  
Product source = **what** to automate; device dump = **how** to find elements.

---

## Step 2 — Gather docs (always before coding)

1. Read approved test cases or the flow P0 matrix.  
2. Grep existing POs / actions / steps / tests for this feature.  
3. List gaps (missing screens, locators, asserts).  
4. Optional: Figma/Jira from `get-context` for **copy only** — not locators.

---

## Step 3 — Walk the flow on device (mandatory for new TCs)

**No new test or PO until the scenario is walked on emulator/device via Appium MCP.**

Config: `.mcp.json` · caps: `environment/appium-mcp.capabilities.json` (keep
aligned with `.env`). Needs `ANDROID_HOME` + `invoke appium:install-drivers`.

### 3a. Quick dump (optional)

Single-screen snapshot via **`discover-mobile-locators`**:

```bash
invoke emulator:start && invoke app:install
invoke ui:dump --screen=<name>    # → docs/locators/<name>.xml (local only)
```

Still do **3b** for a new test case.

### 3b. Appium MCP walkthrough

1. Boot device + install app.  
2. MCP: `select_device` → `appium_session_management` (`action=create`).  
3. For each scenario step:
   - Navigate (`appium_gesture` / `appium_set_value` / `appium_find_element`)
   - Screenshot (`target/mcp-screenshots/` when `NO_UI=true`)
   - Page source → `docs/locators/<screen>.xml` if new/drifted
   - `generate_locators` — **confirm** every suggestion against page source  
4. Note overlays (permissions, Google picker, debug FAB, network errors).

| Precondition | During MCP |
|--------------|------------|
| Fresh login | Clear app data, then relaunch |
| Already logged in | Reuse home, or walk login first |
| Downstream feature | Login P0 must already pass |

### Before coding — short summary for the user

```text
- Screens visited (order)
- Key UI strings confirmed
- Locator notes (strategy + value)
- Overlays / quirks
- Gaps vs flow doc
```

Only then → Step 4.

---

## Step 4 — Implement

Use **`mobile-appium-python`** + **AGENTS.md** layer rules:

```text
page_objects → page_actions → steps → dataprovider → test
```

| Situation | Do this |
|-----------|---------|
| Steps already exist | Wire test + dataprovider only |
| New screen | Dump → PO → actions → steps → test |
| Locator drift | Fix one PO field; grep for duplicates |
| Multi-screen flow | One step module calling several actions |

**Done when:**

- [ ] MCP walkthrough done (Step 3)  
- [ ] Locators live-confirmed  
- [ ] Steps exist before the test file  
- [ ] Markers / Allure per AGENTS.md  

---

## Step 5 — Verify

Run **upstream first**, then the new flow:

```bash
invoke lint
invoke test --markers "login and p0"
invoke test --markers "<new_feature_marker>"
invoke test --markers "e2e and p0"
invoke report
```

On failure: re-dump the screen. Waits → **AGENTS.md** (no `time.sleep()`).

---

## Step 6 — On failure, update knowledge

Fix the code **and** record what you learned (unless it was a one-off env glitch).

| Failure type | Update |
|--------------|--------|
| Emulator / Appium boot | `mobile-appium-python` or `get-context` Phase 0 notes |
| Locators / Flutter semantics | `discover-mobile-locators` |
| Login / OTP / carousel | this skill’s **Known pitfalls** + discover |
| Layer / assert wiring | `review-changes` / `mobile-appium-python` |
| Triage artifacts | `read-test-reports` |

Append under **Known pitfalls**:

```markdown
### Known pitfalls (updated YYYY-MM-DD)
- **Symptom:** …
  **Cause:** …
  **Fix:** …
```

Also add new quirks to `docs/<app_slug>-flow.md` blockers when relevant.

---

## Don’t do this

Repo-wide rules (sleeps, invented locators, wrong layer imports) → **AGENTS.md**.

Orchestration-only:

- New TC without MCP walkthrough (Step 3)  
- Downstream tests before login P0 passes  
- Skipping Step 0 prereqs  
- Fixing code without updating skills when the failure teaches something reusable  

---

## Appendix — CoFee known pitfalls (updated 2026-07-16)

- **`pm clear` mid-session kills UiAutomator2** — quit session → clear + seed intro + launch → new driver → login with session reuse.  
- **Post-OTP wait** — accept only `home`/`org`, not lingering OTP screen.  
- **Org → home** — left-biased Continue (debug FAB); home = CoFee nav (`Groups`/`Payments`), not launcher “Home”.  
- **Onboarding carousel** — prefer seeding `hasIntroScreenShown` after `pm clear`.  
- **Create group tile** — `ACCESSIBILITY_ID` / `descriptionMatches` for **Add New** / **Create group**.  
- **Phone Continue** — wait until clickable; dismiss Google phone picker; OTP needs network + whitelisted `TEST_MOBILE`.  
- **Emulator** — set `AVD_NAME`; cold boot may need ~300s wait.  
- **Member fee assert** — Indian formatting + newlines → one `descriptionMatches("(?s).*…*")`.  

---

## Related skills

`get-context` · `extract-p0-test-cases` · `discover-mobile-locators` ·
`setup-mobile-test-data` · `mobile-appium-python` · `read-test-reports` ·
`review-changes` · [AGENTS.md](../../../AGENTS.md)
