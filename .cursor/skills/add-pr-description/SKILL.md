---
name: add-pr-description
description: >-
  Drafts reviewer-friendly pull request descriptions from actual commits and
  diffs. Use when creating or updating a PR, preparing gh pr create, or when
  the user asks for a PR description or summary of branch changes.
---
# Add PR Description

Generate or update a reviewer-friendly pull request description from the current branch.

The description must be based on the **actual commits and diff**. Never invent changes or claim tests were run unless they actually were.

## When to Use

Use this skill when:

- Creating a new Pull Request
- Updating an existing Pull Request description
- Preparing a PR before running `gh pr create`

## Workflow

### Step 1 — Understand the Repository

Review:

**Required**

- `AGENTS.md`

**If modified on this branch**

- `docs/cofee-flow.md`
- `docs/context/*.md`

Determine:

- Base branch
- Current branch
- Working tree status

Do **not** push or modify the branch during this step.

### Step 2 — Inspect the Changes

Collect the actual scope of the PR.

```bash
git log --oneline <base>..HEAD
git diff --stat <base>...HEAD
git diff <base>...HEAD
```

If a PR already exists:

```bash
gh pr view
```

Group changes based on the implementation, such as:

- Feature automation
- Framework updates
- Bug fixes
- Documentation
- Test improvements

Avoid creating artificial categories.

### Step 3 — Draft the PR Description

Use the following structure.

#### Summary

- 2–4 bullets
- Explain what changed
- Explain why it changed
- Avoid listing files

#### Changes

Group related work together.

```text
### Automation
- ...

### Framework
- ...

### Documentation
- ...
```

Reference modified documentation instead of repeating its contents.

#### Test Plan

| Test Case | Status | Evidence / Notes |
| ---------- | ------ | ---------------- |
| TC-001 | ✅ Passed | `pytest tests/...` |
| TC-002 | ⚠️ Partial | Failed on retry |
| TC-003 | ⬜ Not run | Not executed |

Rules:

- One row per test case
- Separate parameterized test cases
- Include the execution command or verification evidence
- Never mark a test as passed unless it actually ran

#### Known Blockers / Follow-ups

Include:

- Existing blockers
- Newly discovered issues
- Remaining TODOs
- Follow-up work

### Step 4 — Request Approval

Display the complete PR description.

Wait for explicit user approval before creating or updating the PR.

If revisions are requested, update the draft and present it again.

### Step 5 — Create or Update the PR

If the branch is unpushed or behind the remote, ask for confirmation before pushing.

Create a new PR:

```bash
gh pr create
```

Update an existing PR:

```bash
gh pr edit
```

Return the PR URL after completion.

## Rules

- Describe only the work present in the current branch.
- Never invent implementation details or test results.
- Reference documentation instead of copying it.
- Never create or update a PR without user approval.
- Never force-push or rewrite history.
- Mention unrelated commits if the branch contains mixed work.

## Related Skills

- `pr-review-changes`
- `testscript-generator`
- `generate-test-reports`