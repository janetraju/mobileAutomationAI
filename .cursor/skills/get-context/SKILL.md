# Get Context

Collect feature context from available product artifacts and generate a single discovery document for downstream test design and automation.

**Output**

```
docs/context/<app_slug>-<feature-slug>-context.md
```

This skill gathers feature context only. Repository conventions (Page Objects, locators, waits, etc.) are defined in `AGENTS.md`.

---

## When to Use

Use this skill when:

- A user asks to gather context for a feature
- Starting feature analysis before writing test cases
- Onboarding a new application (bootstrap)

---

## Inputs

Possible sources:

- PRD
- Figma
- Jira
- Application source
- Existing flow documentation

Missing artifacts are acceptable. Record what is unavailable and continue.

---

# Workflow

## Step 0 — Bootstrap the Application *(if required)*

Skip if the application is already configured.

An application is considered configured when:

- `APP_SLUG` exists in `.env`
- The application exists in `APP_REGISTRY`
- Project folders already exist

Otherwise:

1. Obtain the APK or IPA
2. Analyze the application

```bash
invoke app:analyze --apk=builds/<app>.apk
```

3. Configure:

- `APP_REGISTRY`
- `.env`
- Project folders
- `docs/<app_slug>-flow.md`

Mark all generated flows as **Unconfirmed**.

Do not derive Page Objects or locators from APK analysis.

---

## Step 1 — Collect Inputs

Ask the user for the following once per session.

| Item | Options |
|------|---------|
| Change Type | New Screen / Flow, Enhancement, Bug Fix, Locator Hardening |
| PRD | Upload, Link, Not Available |
| Figma | Upload, Link, Not Available |
| Jira | Link, Key, Upload, Not Available |
| App Source | Existing Repository, Upload, Not Available |

Record each source as:

- Available
- Partial
- Not Available

---

## Step 2 — Gather Artifacts

Process sources in this order:

1. PRD
2. Figma
3. Jira
4. Application Source

Wait until every available source has been collected or explicitly skipped.

For image-only Figma exports, inspect the screenshots directly.

---

## Step 3 — Discover Existing Implementation

Determine the feature slug.

Search:

- Current repository
- Application source
- Existing flow documents
- Existing Page Objects
- Existing tests

Treat all code-derived UI elements as **hypotheses** until verified by `discover-mobile-locators`.

---

## Step 4 — Analyze Artifacts

Use available integrations where appropriate.

| Source | Activity |
|---------|----------|
| PRD | Extract requirements and acceptance criteria |
| Figma | Inspect design, screenshots, metadata |
| Jira | Collect acceptance criteria and linked issues |
| Source Code | Identify implementation hints |

If an integration fails:

- Notify the user
- Mark the source as **Partial**
- Continue

---

## Step 5 — Resolve Gaps

Ask only the questions needed to complete missing information.

Focus on:

- Business rules
- Success criteria
- Edge cases

Limit follow-up questions to **3–6**.

---

## Step 6 — Generate Context Document

Create:

```
docs/context/<app_slug>-<feature-slug>-context.md
```

Include:

| Section | Description |
|---------|-------------|
| Feature | Name, slug, source artifacts |
| Artifact Status | Available / Partial / Missing |
| Screens | Scope and purpose |
| Happy Path | Screen-to-screen flow |
| Screen Elements | Candidate UI elements (hypotheses only) |
| Business Rules | Acceptance criteria and requirements |
| Edge Cases | Known or Unknown |
| Regression Areas | Existing bugs or affected areas |
| Existing Automation | Current tests and Page Objects |
| Open Questions | Remaining gaps |

Use:

- **Unknown** when information is unavailable
- **Assumption** when inferred

---

## Step 7 — Next Steps

Recommended workflow:

```text
get-context
      ↓
extract-p0-test-cases
      ↓
discover-mobile-locators
      ↓
setup-mobile-test-data
      ↓
automate-a-flow
      ↓
mobile-appium-python
```

All locator hypotheses must be confirmed during `discover-mobile-locators`.

---

## Rules

- Read feature inputs before searching the implementation.
- Never fail because an artifact is missing.
- Never invent business rules or UI text.
- Never generate Page Objects or locators.
- Never write the context document until artifact collection is complete.
- Ask the intake questions only once per session unless the user requests a restart.
- Never commit application source or APK files.

---

## Related Skills

- `extract-p0-test-cases`
- `discover-mobile-locators`
- `automate-a-flow`
- `mobile-appium-python`