---
name: author-pr-description
description: >-
  Draft (or update) an accurate, detailed pull request description from the
  current branch's real commits/diff — summary, grouped changes, test plan,
  known blockers/follow-ups — before running `gh pr create`/`gh pr edit`.
  Use when the user asks to raise, open, or create a PR, or wants an
  existing PR's description written/improved for this repo.
disable-model-invocation: true
---

# Author PR Description

Turns the actual commits/diff on a branch into a PR description a reviewer
can act on without re-deriving it themselves — never a vague "various
fixes" summary, and never a claimed test result that wasn't actually run.

## When to use

- User asks to raise/open/create a PR for the current branch
- User asks to improve, rewrite, or fill in an existing PR's description
- Before `gh pr create` — description must be drafted and approved first

## Read first

1. **`AGENTS.md`** — repo conventions, current feature/lifecycle context
2. `git log <base>..HEAD` and `git diff <base>...HEAD` — the actual scope,
   not assumptions carried over from chat
3. `docs/cofee-flow.md`, `docs/context/*.md`, `docs/locators/*.md` touched
   on this branch — reference these, don't re-explain their content
4. `gh pr view` (if a PR already exists for this branch) — update in place,
   don't duplicate

## Workflow

### 1. Determine base and scope

Confirm the base branch (usually `master`) and that the working tree is
clean. If the branch isn't pushed yet or is behind, that's a separate,
confirmable step (see Phase 4) — don't silently push as a side effect of
drafting.

### 2. Gather real changes

```bash
git log --oneline <base>..HEAD
git diff --stat <base>...HEAD
```

Group commits/files by concern the way this repo's own commit messages
already do — e.g. feature automation, skill/pipeline changes, docs,
bug fixes discovered along the way. Don't invent a grouping that doesn't
match what's actually in the diff.

### 3. Draft the description (fixed shape)

- **Summary** — 2–4 bullets: what changed and why, not a file listing
- **Changes** — grouped by area, naming specific files/skills/tests touched
- **Test plan** — a table, not a checklist, of what was *actually* run or
  verified this session:

  | Test Case | Status | Notes |
  |---|---|---|
  | `test_name` (TC id if applicable) | ✅ Passed / ❌ Failed / ⚠️ Partial / ⬜ Not run | Command/session evidence, caveats |

  One row per test case (parametrized cases get their own row, not a
  collapsed summary). Cite the specific `pytest` invocation or live-device
  check (`discover-mobile-locators`/manual exploration) as evidence. Mark
  anything not verified as **⬜ Not run** — never imply a check happened
  when it didn't, and never collapse a partial/flaky result into ✅
- **Known blockers / follow-ups** — carried over from `docs/cofee-flow.md`'s
  Known Blockers section when relevant, or newly discovered ones

### 4. Present draft, get approval

Show the full draft body in chat. Wait for explicit approval before running
`gh pr create` or `gh pr edit`. Revise on feedback — no re-asking needed
for iteration, only for the final go-ahead.

### 5. Raise or update the PR

- Confirm before pushing an unpushed/behind branch (standard risk-action
  check — pushing is visible to others)
- New PR: `gh pr create --title "<70 chars>" --body "$(cat <<'EOF' ... EOF)"`
- Existing PR: `gh pr edit <number> --body "..."`
- Report the PR URL back to the user

## Rules

- Never invent a test-plan item that wasn't actually run — cite the exact
  command/session evidence, or mark it **Not run**
- Keep the title under ~70 characters; put detail in the body
- Reference every relevant doc this branch touched
  (`docs/context/`, `docs/locators/`, `docs/cofee-flow.md`) by name/link —
  don't restate their content
- Approval gate is mandatory — never call `gh pr create`/`gh pr edit`
  before the user approves the draft
- Never force-push or rewrite history to "clean up" the PR — describe what
  is actually there
- If commits mix unrelated work (e.g. a merge pulling in someone else's
  feature), say so explicitly in Summary rather than presenting it as your
  own change
- Never push to a remote the user doesn't have write access to without
  confirming first — check `gh repo view --json viewerPermission` if unsure

## Related skills

`pr-review-changes` · `mobile-appium-python` · `read-test-reports` ·
[AGENTS.md](../../../AGENTS.md)
