---
name: extract-p0-test-cases
description: >-
  Extract P0 mobile test cases from project flow docs for the configured app.
  Use when the user asks for P0 cases, smoke scenarios, which flows to automate
  first, or test cases from flow/Figma documentation — for any app in this repo.
---

# Extract P0 Test Cases

## Read order

Use paths with your configured `<app_slug>` (current app: `cofee`):

1. **`AGENTS.md`**
2. **`docs/cofee-flow.md`** (or `docs/<app_slug>-flow.md`)
3. **`docs/assets/`** (if present — screenshots, Figma exports)
4. **`.env.example`**, **`data/cofee/`**
5. **`tests/test/cofee/`** (existing coverage)
6. **`src/page_objects/cofee/`** (implemented screens)

## Output format

Produce a fixed markdown table — do not invent flows not present in docs:

| ID | Flow | Steps (from docs) | Priority | Automation status | Blockers |
|----|------|-------------------|----------|-------------------|----------|
| P0-01 | … | … | P0 | Not started / In progress / Done | … |

- Number sequentially: P0-01, P0-02, …
- **Automation status** reflects `tests/test/app_slug/` reality
- **Blockers** from "Known blockers" section in flow doc

## Rules

- If a flow is not in `docs/<app_slug>-flow.md` or attached assets, mark it **"Not in docs — confirm with user"**
- Do not fabricate locators or credentials
- If user asks to **implement** a case → switch to **`mobile-appium-python`** skill and follow layer order

## After extraction

Offer to update `docs/<app_slug>-flow.md` priority matrix with the table (user approval required).
