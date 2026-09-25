# Mobile Automation Skillset

A portable set of **15 Claude Code / Cursor skills** plus a governance doc
(`AGENTS.md`) that together drive end-to-end mobile UI automation — Appium
2.x + Pytest + Allure, four-layer Page Object Model — for **any** mobile
app, not just the one this skillset was originally built against.

This repo is the **source** of the skillset. This README is about getting
it *into your own project's repo*. Once it's there, `AGENTS.md` is the
document your agent (and your team) actually works from day to day — this
file doesn't repeat its content.

## What you get

| Category | Skills |
|---|---|
| Environment & setup | `mobile-env-doctor`, `mobile-build-fetch`, `create-mobile-framework-structure` |
| Feature lifecycle | `get-mobile-context`, `get-mobile-auth`, `mobile-test-data`, `mobile-test-design`, `mobile-test-automation` |
| Reference | `mobile-common-scenarios` |
| Results & quality gates | `mobile-test-report`, `teardown`, `mobile-coverage-audit`, `mobile-ci-pipeline`, `pr-review-changes`, `add-pr-description` |

Full role/output for each — and the order they run in — is in `AGENTS.md`
→ **Skills (execution helpers)** once you've added it to your repo.

**Honest status:** every Android path here has been exercised end-to-end
against a real app. iOS is implemented per Appium/Apple conventions
throughout but has not been run on a real macOS host — `AGENTS.md` flags
this explicitly rather than assuming parity. `mobile-ci-pipeline`'s
workflow is likewise generated from documented CI conventions, not a run
that's actually been watched pass.

## Prerequisites

- **Claude Code or Cursor** — skills are authored once under `.cursor/skills/`;
  `.claude/skills/` are symlinks to the same folders, so both tools see the
  same definitions
- **Python 3.10+**, **Node.js** (Appium runs on Node)
- **Android**: Android SDK (`adb`, `emulator`), `ANDROID_HOME` set
- **iOS**: an actual **macOS host** with Xcode's command-line tools — there
  is no simulator fallback on Linux/Windows, and no skill here can work
  around that

## Add this skillset to your repo

From a checkout of this repo (or a clone of it), copy two things into your
target repo's root — the skill folders and the governance doc:

```bash
# 1. Clone this skillset repo somewhere temporary
git clone https://github.com/janetraju/mobileAutomationAI.git /tmp/mobile-skillset
cd /tmp/mobile-skillset
git checkout mob-grpB-finalruncj   # or whichever branch has the version you want

# 2. Copy into your project (adjust the destination path)
YOUR_REPO=/path/to/your/repo

mkdir -p "$YOUR_REPO/.cursor" "$YOUR_REPO/.claude"
cp -a .cursor/skills "$YOUR_REPO/.cursor/skills"
cp -a .claude/skills "$YOUR_REPO/.claude/skills"
cp AGENTS.md "$YOUR_REPO/AGENTS.md"
```

**If your repo already has its own `.cursor/skills/` or `.claude/skills/`**
(other, unrelated skills already in place), merge instead of overwriting:

```bash
rsync -a .cursor/skills/ "$YOUR_REPO/.cursor/skills/"
rsync -a .claude/skills/ "$YOUR_REPO/.claude/skills/"
```

**Symlinks matter here** — `.claude/skills/<name>` is a relative symlink to
`../../.cursor/skills/<name>`, not a copy. `cp -a` and `rsync -a` both
preserve symlinks correctly; a plain `cp -r` on some systems will not, and
`git add` handles them natively as long as `core.symlinks` isn't disabled
(true by default on Linux/macOS; Windows users should confirm it via
`git config core.symlinks`).

**If you already have an `AGENTS.md`** with your own project-specific
content, don't overwrite it blindly — merge the **Skills**, **Repo
contract**, and **Pipeline** sections in manually, since those are what
the skills above actually depend on.

Then commit:

```bash
cd "$YOUR_REPO"
git add AGENTS.md .cursor/skills .claude/skills
git commit -m "Add mobile automation skillset"
```

## First run in your repo

1. **`mobile-env-doctor`** — confirm your host/device/Appium stack can
   actually run automation before anything else. This isn't optional
   ceremony: a real session was lost chasing failures that turned out to
   be host-level, not code-level, before this check existed.
2. **`mobile-build-fetch`** (if you don't already have an APK/IPA handy)
   → **`create-mobile-framework-structure`** — registers your app and
   scaffolds the four-layer POM skeleton, one time.
3. From there, follow `AGENTS.md` → **Getting started** — it's written to
   be run by a non-coder, one skill at a time, in order.

## Updating the skillset later

This is a copy, not a live link — pulling improvements made in this source
repo later means repeating the copy step above (or `rsync -a` again to
merge updates) and re-committing. There's no automatic sync.
