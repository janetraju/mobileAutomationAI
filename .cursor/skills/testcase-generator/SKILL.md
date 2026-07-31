---
name: testcase-generator
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
---
# Extract Test Cases

Generate structured, device-observable test cases (P0/P1/P2) from feature documentation.

This skill defines **what to test**. It does **not** capture UI locators. Locator discovery is handled by `discover-mobile-locators`.

Follow repository conventions defined in `AGENTS.md`.

## When to Use

Use this skill when:

- A user requests test cases for a feature
- A user requests P0 or smoke test cases
- `docs/context/<app_slug>-<feature>-context.md` exists
- Test cases need approval before automation begins

> For P0-only requests, generate the complete test suite internally but present only the P0 cases.

## Workflow

### Step 1 — Gather Context

Review the following in order.

**Required**

- `AGENTS.md`
- `docs/context/<app_slug>-<feature>-context.md`

**Fallback** (if no context document exists)

- `docs/<app_slug>-flow.md`
- Screenshots, Figma, or product source shared in the current session

**Reference**

- `tests/test/<app_slug>/` (avoid duplicate coverage)
- `src/page_objects/<app_slug>/` (understand implemented screens)

If no feature documentation exists:

- Ask the user to confirm the feature, or
- Run `get-context` first.

---

### Step 2 — Generate Test Cases

Create test cases using:

- Stable ID: `TC-<feature>-<CATEGORY>-<NN>`
- Priority: `P0`, `P1`, or `P2`
- Shared preconditions (define once and reference)
- Device-observable steps
- Observable expected results

Use the following categories.

| Prefix | Category |
|---------|----------|
| `HP` | Happy Path |
| `NEG` | Negative / Validation |
| `EDGE` | Edge Cases |
| `PERM` | Permissions |
| `STATE` | Navigation / State |
| `A11Y` | Accessibility *(when applicable)* |
| `PLAT` | Platform-specific |
| `REG` | Regression |

Guidelines:

- Mark uncertain behavior as **`[Assumption]`**
- Do not generate locators
- Remove duplicate scenarios
- Combine similar input variations into parameterized cases

---

### Step 3 — Review with the User

Present:

1. Feature slug
2. Source documentation used
3. Manual test reconciliation count (if applicable)
4. Test cases grouped by category

| ID | Priority | Category | Test Case | Steps | Expected Result |
|----|----------|----------|-----------|-------|-----------------|

If assumptions exist, list them separately.

Prompt the user:

> Reply **approve** to write `docs/context/<app_slug>-<feature>-testcases.md`, or tell me what you'd like to change.

Do **not** create the file until approval is received.

---

### Step 4 — Write the Test Case Document

After approval:

- Generate the document using `testcase-template.md`
- Save it as:

```
docs/context/<app_slug>-<feature>-testcases.md
```

Use the approved content exactly.

Do not make additional changes without user approval.

---

### Step 5 — Next Steps

```text
discover-mobile-locators
        ↓
automate-a-flow
        ↓
testscript-generator
```

Prerequisite: `get-context`. Template: `testcase-template.md`. Optionally offer to update the feature's priority matrix in the flow document.

## Rules

- Treat context and flow documents as read-only.
- If documentation is incorrect or incomplete, send the user to `get-context`.
- Preserve all provided manual test cases and report the reconciliation count.
- Never write the output file before explicit approval.
- Avoid web-only concepts such as `data-testid`, routes, or RTK.
- Check existing automation before marking coverage complete.