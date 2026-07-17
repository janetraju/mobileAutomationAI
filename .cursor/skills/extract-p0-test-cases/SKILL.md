---
name: extract-p0-test-cases
description: >-
  Generate structured, device-observable mobile test cases across all
  priorities (P0/P1/P2) and categories (happy path, negative, edge,
  permission/OS dialog, state/navigation, accessibility, platform,
  regression) for any app in this repo. Prefers
  docs/context/<app_slug>-<feature>-context.md from get-context; falls back
  to docs/<app_slug>-flow.md (fed by screenshots, Figma, or product-repo
  analysis) when no context file exists yet. Use when the user asks for
  P0/smoke cases, test cases for a feature, or "which flows to automate
  first." Presents a draft in chat and requires approval before writing
  docs/context/<app_slug>-<feature>-testcases.md.
disable-model-invocation: true
---

# Extract / Generate Test Cases

Turns feature context into test cases a human could execute by hand on a
real device — concrete steps and expected results, never "verify login
works." P0 extraction (the original scope of this skill) is now a filtered
view of the same output, not a separate mode.

## Read order

Use paths with your configured `<app_slug>` (current app: `cofee`):

1. **`AGENTS.md`** — conventions, layer rules
2. **`docs/context/<app_slug>-<feature-slug>-context.md`** (from
   `get-context`, if it exists) — **preferred input**: screens in
   scope, flow, business rules/AC, elements (🟡 hypotheses), existing
   automation coverage, open questions
3. **Fallback**, only if no context file exists yet: `docs/<app_slug>-flow.md`
   (or `docs/cofee-flow.md`) + whatever fed it this session —
   `docs/assets/` (screenshots, Figma exports) **and/or** a product/source
   repo the user shared (screens, routes, validation)
4. **`.env.example`**, **`data/<app_slug>/`**
5. **`tests/test/<app_slug>/`** — existing coverage (even `fixme`/skipped) — reference, don't duplicate
6. **`src/page_objects/<app_slug>/`** — implemented screens

If neither a context file nor a flow doc section covers the requested
feature, mark it **"Not in docs — confirm with user"** — or, if a product
repo is available this session, run `author-mobile-flow-docs` first (or
extract candidates and mark them **Unconfirmed** until the flow doc is
updated). Never invent flows, steps, or element labels.

---

## Core rules

| # | Rule |
|---|------|
| 1 | **Context/flow doc is read-only** — never edit it here; if it's wrong, send the user back to `get-context` or `author-mobile-flow-docs`. |
| 2 | **No hallucination** — mark anything not confirmed by the source doc as `[Assumption]`; never invent element labels, error copy, or business rules. |
| 3 | **Device-observable steps** — every step is a physical action (tap X, type Y, observe Z) — never "call the API" or "check the database." |
| 4 | **Locators are the next skill's job** — this skill records *what to test*, not *how to locate it*. Only carry over a locator if the context file already marked it live-confirmed; otherwise leave it for `discover-mobile-locators`/`mobile-appium-python`. |
| 5 | **Reuse preconditions** — define shared preconditions once (e.g. "PRE-01: fresh install, no active session") and reference by id. |
| 6 | **Approval gate is mandatory** — draft in chat, wait for explicit approval, iterate on rejection. Never write the `-testcases.md` file speculatively. |
| 7 | **Carry over every provided manual test case** — if the context file lists manual test cases, every one must appear in the output (verbatim intent, reformatted to this skill's table), plus a reconciliation count ("N manual cases carried over, M new cases added"). |
| 8 | **Dedup pass** — after drafting, scan for cases with an identical signature (screen/flow + primary action + expected result); merge before presenting. |
| 9 | **Parametrize, don't hand-duplicate** — 3+ cases that only vary one input (e.g. 4 invalid phone-number formats) become one case with a small data table, not 4 blocks. |
| 10 | **Mobile-appropriate categories only** — no web concepts (routes, RTK, `data-testid`). |
| 11 | **Automation status reflects reality** — cross-check `tests/test/<app_slug>/` before marking anything "Done." |
| 12 | **Product-repo provenance** — a flow sourced only from a product/source repo (not yet in the flow doc) gets its cases tagged `[Assumption]` same as any other unconfirmed source; never fabricate locators from repo code alone — those come after `discover-mobile-locators`. |

---

## Test case categories

| Prefix | Category | Notes |
|--------|----------|-------|
| `HP` | Happy path | The primary success flow(s) |
| `NEG` | Negative / validation | Invalid input, wrong/expired OTP, empty required fields, offline/network failure mid-flow |
| `EDGE` | Edge case | Boundary lengths, rapid double-submit, backgrounding mid-flow, kill/resume |
| `PERM` | OS permission / system dialog | Notification/camera/location prompts — confirm both Allow and Deny paths where behavior differs |
| `STATE` | State / navigation | Back button at each step, re-entry after partial flow, session persistence across restart |
| `A11Y` | Accessibility | Only if the context file (or code discovery) flagged a real semantics issue — document the current behavior, don't invent a11y cases with no basis |
| `PLAT` | Platform variance | Only if the flow differs Android vs iOS; mark iOS cases **"not locally runnable"** per this repo's Android-only local setup — never silently drop them |
| `REG` | Regression | Tied to a known bug/quirk recorded in context/flow doc |

Don't force categories that don't apply — an empty category is fine; a
padded one with near-duplicate cases is not.

**When the user asks specifically for "P0" or "smoke" cases:** generate the
full set internally, then present/write only the `P0`-priority subset.
**When asked broadly** ("generate test cases for `<feature>`"): present all
applicable categories across P0/P1/P2.

---

## Phase 1 — Resolve inputs

1. Resolve slug/feature name. Look for
   `docs/context/<app_slug>-<slug>-context.md` first; else fall back to the
   flow doc (per Read order above).
2. Pull: screens in scope, flow, business rules/AC, manual test cases
   (if any), known accessibility/regression issues, existing automation
   coverage.
3. Note existing `tests/test/<app_slug>/` coverage (including `fixme`'d
   cases) so this pass references, not recreates, them.

---

## Phase 2 — Generate

For each applicable category: write cases with a stable id
(`TC-<slug>-<PREFIX>-<NN>`), title, priority (P0 blocks release / P1 / P2),
preconditions (reuse shared ids), numbered device-observable steps, and an
observable expected result.

**Volume guidance:** cover what genuinely applies — a simple screen might
have 4–6 cases total; a payment flow with permission/role variance might
have 15+. Don't pad to hit a count.

**Dedup pass:** compare every pair for identical signature (screen/flow +
action + expected result); merge or drop before presenting.

---

## Phase 3 — Present draft (chat)

Show, in order:

1. Slug + source doc (context file or flow doc section) used.
2. Manual-case reconciliation count (Core rule 7), if applicable.
3. Full case table, grouped by category:

   | Sr No | TC ID | Category | Priority | Test Case Name | Steps | Expected Result |
   |-------|-------|----------|----------|-----------------|-------|------------------|

4. Any `[Assumption]`-tagged cases called out separately.
5. Cases flagged for parametrization (Core rule 9) with variant data.
6. One line: *"Reply `approve` to write
   `docs/context/<app_slug>-<slug>-testcases.md`, or tell me what to
   change."*

---

## Approval gate

| User response | Action |
|----------------|--------|
| `approve` / equivalent | Phase 4 — write the file |
| Requests changes | Revise in chat, re-present (no re-asking needed) |
| Silence / ambiguous | Ask once which specific cases need changes |

Never write the `-testcases.md` file before explicit approval.

---

## Phase 4 — Write on approve

Write [testcase-template.md](testcase-template.md)'s structure to
`docs/context/<app_slug>-<slug>-testcases.md`, filled with the approved
cases exactly as shown (no silent changes after approval).

---

## Phase 5 — Handoff

```text
Test cases approved and written to
docs/context/<app_slug>-<slug>-testcases.md (N cases).
Next: discover-mobile-locators (confirm 🟡 locator hypotheses live), then
automate-a-flow → mobile-appium-python to implement.
```

Offer to update `docs/<app_slug>-flow.md`'s priority matrix with the P0
subset (user approval required).

---

## Do not

- Write the file before explicit user approval.
- Invent locators — that's `discover-mobile-locators`'/`mobile-appium-python`'s
  job after live validation.
- Drop a user-provided manual test case silently.
- Pad categories with near-duplicate cases instead of parametrizing.
- Use web-only concepts (routes, `data-testid`, RTK) — this is mobile.
- Mark iOS cases as covered when only Android was ever validated locally.
- Fabricate flows/steps not present in the context file, flow doc, or user input.

## Related skills

`get-context` · `author-mobile-flow-docs` · `discover-mobile-locators` ·
`automate-a-flow` · `mobile-appium-python` ·
[testcase-template.md](testcase-template.md)
