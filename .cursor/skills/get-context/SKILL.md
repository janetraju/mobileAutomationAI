---
name: get-context
description: >-
  Collects feature context from PRDs, Figma, screenshots, product repos, and
  walkthroughs; bootstraps new apps when needed. Outputs
  docs/context/<app_slug>-<feature>-context.md. Use when gathering context for
  a new feature, onboarding a new app, starting test design, or refreshing
  requirements before testcase generation or automation.
---
# Get Context

Collect feature context from available product artifacts and generate a discovery document for downstream test design and automation.

Repository conventions (Page Objects, locators, waits, coding standards, etc.) are defined in `AGENTS.md`. This skill focuses only on feature discovery and context generation.

## When to Use

Use this skill when:

- Gathering context for a new feature
- Starting feature analysis before test case generation
- Onboarding a new application
- Refreshing context after feature or requirement changes

## Output

Generate:

```text
docs/context/<app_slug>-<feature-slug>-context.md
```

Commit this file. It serves as the discovery record for downstream skills (see Step 7).

## Supported Sources

This skill can use any combination of:

- PRD
- Figma
- Jira
- Application source
- Existing flow documentation

Missing artifacts are acceptable. Record unavailable sources and continue.

---

# Workflow

## Step 0 — Bootstrap the Application *(if required)*

Skip this step if the application is already configured.

An application is considered configured when:

- `APP_SLUG` exists in `.env`
- The application is registered in `APP_REGISTRY`
- Project folders already exist

Otherwise:

1. Obtain the APK or IPA.
2. Analyze the application.

```bash
invoke app:analyze --apk=builds/<app>.apk
```

3. Configure:

- `APP_REGISTRY`
- `.env`
- Project folders
- `docs/<app_slug>-flow.md`

Mark generated flows as **Unconfirmed**.

Do **not** derive Page Objects or locators from APK analysis.

---

## Step 1 — Collect Inputs

Collect the following information once per session.

| Item | Options |
|------|---------|
| Change Type | New Screen / Flow, Enhancement, Bug Fix, Locator Hardening |
| PRD | Upload, Link, Not Available |
| Figma | Upload, Link, Screenshot, Not Available |
| Jira | Link, Key, Upload, Not Available |
| Application Source | Existing Repository, Upload, Not Available |
| Credentials | Provide test phone/OTP now, Take from `.env`, Not set up yet |

Record each source as:

- Available
- Partial
- Not Available

**Credentials** answered here isn't used by this skill directly — it's
recorded for `automate-a-flow`'s Step 1 login check. OTP strategy reference
and the security rules live in `AGENTS.md` → Test data & credentials, not
here. "Not set up yet" is a valid answer — this skill never blocks on it,
same as PRD/Figma/Jira.

---

## Step 2 — Gather Artifacts

Collect artifacts in the following order:

1. PRD
2. Figma
3. Jira
4. Application Source

Wait until every available artifact has been collected or explicitly skipped.

For Figma screenshots without a link, inspect the image directly.

---

## Step 3 — Discover Existing Implementation

Determine the feature slug.

Review application source and existing flow documentation (see **Supported Sources**), plus:

- Existing Page Objects
- Existing tests

Treat all implementation-derived UI elements as **hypotheses** until verified by `discover-mobile-locators`.

---

## Step 4 — Analyze Artifacts

Analyze each available source.

| Source | Activity |
|---------|----------|
| PRD | Extract requirements and acceptance criteria |
| Figma | Inspect design, screenshots, and metadata |
| Jira | Extract acceptance criteria and linked issues |
| Application Source | Identify implementation hints |

If an integration fails:

- Notify the user immediately.
- Mark the source as **Partial**.
- Continue with the remaining sources.

---

## Step 5 — Resolve Gaps

Ask targeted follow-up questions only when required.

Focus on:

- Business rules
- Success criteria
- Edge cases

Limit follow-up questions to **3–6**.

---

## Step 6 — Generate the Context Document

Create the file at the path in **Output**. Include:

| Section | Description |
|---------|-------------|
| Feature | Name, slug, and source artifacts |
| Artifact Status | Available / Partial / Missing |
| Screens in Scope | Purpose of each screen |
| Happy Path | Screen-to-screen flow |
| Screen Elements | Candidate UI elements *(hypotheses only)* |
| Business Rules | Requirements and acceptance criteria |
| Edge Cases | Known scenarios or **Unknown** |
| Regression Areas | Existing bugs and impacted areas |
| Existing Automation | Current Page Objects and tests |
| Open Questions | Remaining gaps |

Use:

- **Unknown** when information is unavailable.
- **Assumption** when information is inferred.

---

## Step 7 — Next Steps

Recommended workflow:

```text
get-context
      ↓
testcase-generator
      ↓
discover-mobile-locators
      ↓
automate-a-flow          (test data source decided in its Step 1)
      ↓
testscript-generator
```

All locator hypotheses must be validated in `discover-mobile-locators`.

---

## Operating Principles

- Complete application bootstrap before feature intake.
- Collect all available artifacts before generating context.
- Missing PRD, Figma, or Jira should not block progress.
- Infer information only after artifact collection.
- Treat implementation-derived locators as hypotheses until verified.
- Adapt follow-up questions based on available information.
- Surface integration failures immediately while continuing where possible.
- Generate a context document that downstream skills can consume without re-discovering the feature.

---

## Rules

- Never invent business rules, UI text, or acceptance criteria.
- Never generate Page Objects or locators.
- Never write the context document before artifact collection is complete.
- Ask the intake questions only once per session unless the user requests a restart.
- Never commit application source or APK files.
- Reference `AGENTS.md` for repository-wide conventions.