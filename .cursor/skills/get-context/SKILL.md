---
name: get-context
description: >-
  Adaptive feature/screen context discovery for the CoFee mobile app
  (Flutter + Appium): mandatory intake first (asks what's available — PRD,
  Figma, Jira, app source) via AskUserQuestion, collects each artifact
  marked available, then infers from this repo's existing docs/page
  objects/tests and the app source, asks gap-targeted questions, and
  writes docs/context/<app_slug>-<feature>-context.md. Never stops on
  missing docs, but always asks what's available before starting
  discovery. Use when the user says "get context for <feature>" or
  "gather context for <feature>".
disable-model-invocation: true
---

# Get Context (CoFee mobile)

Behave as an **AI QA Architect** doing feature/screen discovery for the
CoFee Android/iOS app driven through Appium — not a web operator UI.

**Output:** `docs/context/<app_slug>-<feature-slug>-context.md` — commit
this file; it's the discovery record consumed by `extract-p0-test-cases`
and, downstream, `mobile-appium-python`.

**Repo ground truth:** [AGENTS.md](../../../AGENTS.md) — `APP_TYPE`, layer
rules, locator priority, which app is currently configured. **Load first**
to route; don't re-derive what it already documents.

This project has no product registry (no `docs/index.json` equivalent) —
`docs/<app_slug>-flow.md`, `src/page_objects/<app_slug>/`, and
`tests/test/<app_slug>/` **are** the registry.

---

## Core rules

| # | Rule |
|---|------|
| 1 | **Ask what's available before doing anything else.** Phase 1 Intake runs first, every time, before any grep/read of app source or repo docs. This is the one non-negotiable ordering rule in this skill. |
| 2 | **Never fail** because PRD, Figma, or Jira is missing — record `not_available` and move on. Infer, interview, then generate. |
| 3 | **Infer after intake** — once Phase 2 artifacts are collected, infer from this repo's `docs/<app_slug>-flow.md`, `src/page_objects/<app_slug>/`, `tests/test/<app_slug>/`, `AGENTS.md`, and the app source (`reference/<app_slug>-app-source/`) — then ask only gaps. |
| 4 | **No hallucination** — label gaps as *Unknown* or *Assumption*; never invent screen copy, element labels, or business rules. |
| 5 | **Live session outranks everything for locators** — Figma copy and app-source `Semantics(label:...)`/`Key('...')` hits are both *hypotheses* (🟡) until confirmed against a running session's accessibility tree in `discover-mobile-locators`. Design docs and code go stale; the running app doesn't. |
| 6 | **Adaptive questions** — the gap-interview question set depends on what Phase 2 actually returned, not a fixed script. |
| 7 | **Downstream-ready** — output must feed `extract-p0-test-cases` directly, without it re-deriving context you already gathered. |
| 8 | **Raise MCP failures immediately** — Figma or Jira auth/unavailable → tell the user in chat now, mark `partial`, continue. A user-supplied **Figma screenshot** (no link) is a valid intake choice, not an MCP failure — inspect the image directly instead. |
| 9 | **Phase 2 before Phase 7** — finish collecting every intake artifact marked **available** before writing the context file. High code confidence does not skip this gate. |

---

## Anti-duplicate

| Rule | Detail |
|------|--------|
| **One intake form per session** | Single `AskUserQuestion` for mandatory intake unless the user says `restart get-context`. |
| **Resume** | If intake + artifacts are already in the thread, skip the form; continue from the next step. |
| **Re-run without restart** | *"Intake recorded. Continuing from [step]. Say `restart get-context` to reset."* |

---

## Phase sequence (strict)

```text
Phase 1  Intake (AskUserQuestion) — always first
    ↓
Phase 2  Collect artifacts marked "available" (chat, sequential; wait for reply each time)
    ↓
Phase 3  Infer slug & feature identity
    ↓
Phase 4  Code discovery — app source + this repo's docs/page objects/tests
    ↓
Phase 5  Design & ticket discovery (MCP) — only for artifacts collected in Phase 2
    ↓
Phase 6  Gap interview (if needed)
    ↓
Phase 7  Write docs/context/<app_slug>-<feature-slug>-context.md   ← only after Phase 2 gate
```

**Allowed before Phase 2 finishes:** one-line confirmations.
**Not allowed before Phase 2 finishes:** Phase 4 onward.

---

## Phase 1 — Intake (`AskUserQuestion`, once, always first)

One tool call, all questions together — **do this before reading or
grepping anything**, including the app source that may already be sitting
in `reference/<app_slug>-app-source/` from a prior turn:

| Question | Options |
|----------|---------|
| Change type | New Screen/Flow \| Enhancement \| Bug Fix \| Locator hardening |
| PRD | Upload \| Provide link \| Not available |
| Figma | Provide link \| Upload (screenshot/export) \| Not available |
| Jira story | Provide link or key \| Upload / paste \| Not available |
| App source | Already at `reference/<app_slug>-app-source/` \| I'll provide it \| Not available |

Record each as `available` / `not_available` / `partial`. Never skip this
step because the app source already happens to be present — a *previous*
feature's context-gathering pass may have left it there, but PRD/Figma/Jira
availability is per-feature and must still be asked.

---

## Phase 2 — Collect artifacts (chat, sequential)

Order: **PRD → Figma → Jira → app source** (skip items marked **Not
available**).

| If chosen | Say once, wait for reply |
|-----------|---------------------------|
| Provide link | **Please paste the [artifact] link.** |
| Upload / paste | **Please upload or paste [artifact] in chat, or give a workspace path.** |
| Figma = Upload | **Please upload the Figma screenshot(s)/export image(s)** (PNG/JPG, one per screen/state), or a workspace path. No `figma.com` link or MCP access required. |
| App source = "I'll provide it" | **Please drop the app source (zip or folder) at `reference/<app_slug>-app-source/`, then say `done`.** |

Confirm each receipt in one line, then immediately prompt the next
artifact. Don't re-ask for an artifact already sitting in the thread or
already unpacked at `reference/<app_slug>-app-source/` — confirm it's the
right one and move on.

### Phase 2 completion gate

Complete when every intake row marked **available** has a link, upload, or
path recorded, **or** the user explicitly says *skip* for a remaining item.
**Only then** start Phase 4 and Phase 7.

**Partial:** link given but unreadable (private repo, 404) → mark
`partial`, extract what you can, continue.

---

## Phase 3 — Infer slug & feature identity

Resolve **before** asking the user:

1. Explicit name in chat this session.
2. Jira summary / key.
3. An existing `src/page_objects/<app_slug>/` or `tests/test/<app_slug>/`
   folder/file name matching the diff/discussion.
4. Figma frame/page name.
5. Git branch — only if it clearly encodes the feature name.

**Slug:** kebab-case (e.g. `login`, `otp-verification`,
`enable-partial-payment`). Only ask if sources conflict.

---

## Phase 4 — Code discovery (app source + this repo)

**Prerequisite:** Phase 2 gate passed.

Confirm `APP_TYPE` from `.env`/`AGENTS.md` before choosing grep patterns.
Scope greps to files matching the feature name/route — don't blindly grep
the whole app.

| `APP_TYPE` | Grep for |
|---|---|
| `flutter` | `Semantics(label:`, `Key('...')`, route/screen widget class names |
| `rn` | `testID=`, `accessibilityLabel=` |
| `native` (Android) | `android:contentDescription`, `android:id` in layout XML |
| `hybrid` | native patterns above + WebView entry points |

Everything found is a **hypothesis** — label 🟡 — never a confirmed
locator. Record file path + line for traceability.

Then cross-reference this repo — report what already exists, don't
duplicate it:

- `docs/<app_slug>-flow.md` — is this flow already documented?
- `docs/locators/` — already-dumped screens for this feature?
- `src/page_objects/<app_slug>/` — existing `*_po.py` for these screens?
- `tests/test/<app_slug>/` — existing test coverage, even skipped?

---

## Phase 5 — Design & ticket discovery (MCP)

Only for artifacts actually collected in Phase 2:

| Source | Action |
|---|---|
| Figma link | `get_design_context`, `get_screenshot`, `get_metadata` — layout, copy, component names, states (empty/error/loading) |
| Figma screenshot (uploaded, no link) | View directly with `Read` — no MCP call. Record as visual reference only, lower confidence than a full MCP read |
| Jira link/key | `getJiraIssue` → acceptance criteria + description. If it lists linked bugs/blockers, fetch each once and note under "Regression areas" — don't recurse further |
| PRD | Map to AC + Suggested Test Areas; preserve any provided manual test cases verbatim |

**Raise MCP failures immediately in chat** — auth error, 404, or
unavailable server — don't silently drop to code-only discovery and don't
retry more than once.

---

## Phase 6 — Gap interview (only if needed)

3–6 targeted questions max, chat only — business rules not visible in code
or Figma/Jira, edge cases, success criteria, mandatory fields, permission/OS
dialogs.

---

## Phase 7 — Write context file

**Prerequisite:** Phase 2 gate passed.

`docs/context/<app_slug>-<feature-slug>-context.md`:

| Section | Content |
|---|---|
| Feature | Name, slug, source (source code / Figma / Jira / PRD / user description) |
| Artifacts received | Honest status per intake item from Phase 1/2 |
| Screens in scope | List, one-line purpose each |
| Flow (happy path) | Numbered steps, screen → screen |
| Elements per screen | Table: element, purpose, 🟡 hypothesis locator + file:line or Figma component name, status |
| Business rules / acceptance criteria | From Jira AC, PRD, or user — cite source — **Unknown** if not found, never invent |
| Edge cases / negative paths | From code branches (validation/error states) or Jira AC where visible, else **Unknown** |
| Regression areas | Jira-linked bugs/blockers, if any |
| Existing automation coverage | Page objects/tests already covering this |
| Open questions | Anything unresolved after the gap interview |

---

## Phase 8 — Hand off

```
get-context → author-mobile-flow-docs → discover-mobile-locators
  → extract-p0-test-cases → setup-mobile-test-data → mobile-appium-python
```

Live session in `discover-mobile-locators` is what actually confirms every
🟡 hypothesis — this skill never writes to `src/page_objects/`.

---

## Rules

- **Always run Phase 1 Intake first** — even if app source is already
  unpacked from a previous feature, PRD/Figma/Jira availability must be
  asked fresh for this feature.
- Never invent business rules, copy, or element labels not present in
  source/docs/user input — mark **Unknown**.
- Source-derived and Figma-derived locators are hypotheses only; never let
  `mobile-appium-python` consume them without a live dump from
  `discover-mobile-locators` first.
- Don't re-derive what `docs/<app_slug>-flow.md` or existing page
  objects/tests already cover — report it instead.
- Never commit the unpacked app source (`reference/` is gitignored) or any
  secrets found inside it.
- Cap the gap interview at 6 questions per round.
- A Figma screenshot (no link) is a valid intake choice, not an MCP
  failure — inspect the image directly instead.
- MCP auth/unavailable failures are reported in chat immediately, never
  silently swallowed.
- Never show mandatory intake twice in one session (unless
  `restart get-context`).
- Never write the context file before Phase 2 completes.

## Related skills

`author-mobile-flow-docs` · `discover-mobile-locators` ·
`extract-p0-test-cases` · [AGENTS.md](../../../AGENTS.md)
