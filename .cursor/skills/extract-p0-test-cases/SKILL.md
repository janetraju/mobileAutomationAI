---
name: extract-p0-test-cases
description: >-
  Extract P0 mobile test cases from project flow docs for the configured app.
  Use when the user asks for P0 cases, smoke scenarios, which flows to automate
  first, or test cases from flow docs, screenshots/Figma, or product-repo–backed
  documentation — for any app in this repo.
---

# Extract P0 Test Cases

## Read order

Use paths with your configured `<app_slug>` (current app: `cofee`):

1. **`AGENTS.md`**
2. **`docs/cofee-flow.md`** (or `docs/<app_slug>-flow.md`)
3. Context that fed the flow doc (if still available this session):
   - `docs/assets/` (screenshots, Figma exports), **and/or**
   - Product/source repo the user shared (screens, routes, validation)
4. **`.env.example`**, **`data/cofee/`**
5. **`tests/test/cofee/`** (existing coverage)
6. **`src/page_objects/cofee/`** (implemented screens)

If the user shares a product repo but flow doc is stale/missing, run **`author-mobile-flow-docs`** first (or extract candidates and mark them **Unconfirmed** until the flow doc is updated).

## Output format

Produce a fixed markdown table — do not invent flows not present in docs (unless marked Unconfirmed from repo):

| ID | Flow | Steps (from docs) | Priority | Automation status | Blockers | Context |
|----|------|-------------------|----------|-------------------|----------|---------|
| P0-01 | … | … | P0 | Not started / In progress / Done | … | screenshots / product repo / both |

- Number sequentially: P0-01, P0-02, …
- **Automation status** reflects `tests/test/<app_slug>/` reality
- **Blockers** from "Known blockers" in flow doc
- **Context** notes whether steps came from screenshots, product code, or both

## Rules

- Prefer **`docs/<app_slug>-flow.md`** as the source of truth for extraction
- If a flow is only in a product repo and not yet in the flow doc, mark **"Not in docs — confirm with user"** or run author-mobile-flow-docs
- Do not fabricate locators or credentials — locators come after **`discover-mobile-locators`**
- If user asks to **implement** a case → switch to **`mobile-appium-python`** (after locator discovery)

## After extraction

Offer to update `docs/<app_slug>-flow.md` priority matrix with the table (user approval required).
