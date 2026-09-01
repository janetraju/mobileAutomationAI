---
name: mobile-test-design
description: >-
  Reviews the feature context, app flow, and auth strategy, then produces an
  approved, automation-ready test plan with explicit P0/P1/P2 prioritization,
  complete coverage across the happy path and failure paths, and clear
  preconditions, expected results, and automation notes. Use before writing
  automation to turn product intent into a reviewable, test-ready plan.
---

# Mobile Test Design

Translate feature context, flow intent, and auth strategy into a test plan
that is reviewable, prioritized, and ready for automation.

This skill is the decision gate before `mobile-test-automation` writes any
Page Objects, actions, steps, or tests. It does not implement the automation
itself; it defines the exact behaviors that should be automated.

Repository conventions (wait policy, assertions, markers, credential rules,
layer boundaries) are defined in `AGENTS.md`. This skill follows them; it
does not redefine them.

## When to Use

Use this skill when:

- a new feature or user flow needs planned coverage
- a product flow is not yet translated into executable scenarios
- the team needs to approve a test strategy before writing automation
- the app behavior has changed and the expected test plan must be refreshed
- the feature depends on a login/auth method that needs a clear test strategy

## Inputs Required Before Designing Tests

This skill should only proceed when the following are available:

- `docs/<app_slug>-flow.md`
- `docs/context/<app_slug>-<feature>-context.md` from `get-mobile-context`
- auth / OTP / credential strategy recorded by `get-mobile-auth`
- any product source material: PRD, Figma, Jira, walkthrough, customer notes

If required inputs are missing, stop and resolve them first. Do not invent
requirements, flows, or expected outcomes.

## Output Required

Create or update:

- `docs/context/<app_slug>-<feature>-testcases.md`

This file must contain a reviewable, approved set of scenarios with:

- stable case IDs
- priorities (`P0`, `P1`, `P2`)
- user story or scenario name
- preconditions
- test data requirements
- step-by-step flow
- expected observable result
- assertions and UI outcome checks
- automation notes and blockers

The testcases file is the source of truth for the automation team.

---

## Design Readiness Gate

Before writing any cases, confirm all of the following are true:

- the feature goal is understood
- the flow is described in product context / flow doc
- the app state at test start is defined
- the auth strategy is known
- the expected observable UI result is known
- no secret or production account data is required

If any of the above is false, stop and clarify the gap instead of writing a
weak or misleading test plan.

---

## Priority Rules: P0 / P1 / P2

Use the following rules consistently:

### P0 — Release-blocking

A case is `P0` when:

- the user cannot complete the core business flow without it
- the feature is critical to a release decision
- a crash, incorrect navigation, auth failure, or invalid transaction would block usage
- it covers the primary happy path or a critical failure path the app must support

Typical examples:

- login or onboarding completion
- purchase / booking / submit / approve flow
- critical validation errors
- major state transitions the app depends on

### P1 — Important but not release-blocking

A case is `P1` when:

- it covers common user behavior or a likely regression path
- it's valuable but not essential for the app to be functionally usable
- it validates secondary business flows within the feature

Typical examples:

- alternate path within the same feature
- common edge case that affects many users
- recovery or retry behavior

### P2 — Secondary / exploratory / low risk

A case is `P2` when:

- it is minor, edge-case, convenience, or extremely low-risk coverage
- it is useful for robustness but not required for release confidence
- it is a rare or low-frequency path

Typical examples:

- minor UI states
- cosmetic consistency checks
- low-risk edge behavior
- exploratory regression checks

---

## Required Coverage Categories

Every approved feature test plan should cover at least:

- happy path
- validation / negative path
- error handling
- edge case
- recovery / retry path
- auth/session state
- app state transitions
- regression risk area

Do not stop at only the happy path. A feature with no failure-path coverage is
an incomplete automation plan.

---

## Mandatory Test Case Template

Use a consistent template for every case.

```text
TC ID: <feature>-P0-01
Priority: P0
Scenario: <short user flow name>
Preconditions:
- <required app state>
- <logged in / logged out state>
- <required environment or test data>
Steps:
1. <step>
2. <step>
3. <step>
Expected result:
- <visible UI outcome>
- <screen or state change>
- <message, count, amount, or status>
Assertions:
- <screen title or visible copy>
- <element state / count / amount>
- <error or success message>
Automation notes:
- <locator strategy notes if known>
- <auth or device constraints>
- <known blocker / dependency>
```

Rules for writing cases:

- write in user-observable terms
- avoid “navigation happened” as a final assertion
- prefer screen text, state, visibility, count, amount, and enabled/disabled conditions
- never include real secrets, real account credentials, or production data
- use existing approved data strategy, not invented values

---

## Good vs Weak Test Case Behavior

### Good test case

- clear preconditions
- specific steps
- observable expected results
- realistic user behavior
- unique and reviewable assertions

### Weak test case

- “user logs in successfully” with no visible expected state
- “app navigates to dashboard” with no screen or copy verification
- generic text like “should work” or “should be fine”
- missing preconditions or assumptions not stated
- no failure or edge path coverage

Weak cases waste automation time because the automation team has to guess what
counted as success.

---

## Review and Approval Gate

Before handing a test plan to `mobile-test-automation`, confirm the following:

- every case has a clear objective
- every case is assigned a priority
- the happy path is covered
- at least one failure path is covered
- the expected UI result is observable
- blockers or unknowns are documented
- no assumptions are hidden
- the plan is approved by the stakeholder or reviewer

This approval gate is intentional: the automation layer should not start from
unclear or unapproved assumptions.

---

## Validation Checklist Before Finalizing

Before closing the testcase file, run this checklist:

- Does every case have a unique ID?
- Is every case tagged with the correct priority?
- Is the flow aligned with product context and flow docs?
- Are the preconditions explicit?
- Are the expected results observable and testable?
- Are failure or edge cases represented?
- Are auth strategies accounted for?
- Are there no hardcoded secrets or production values?
- Are there no duplicate or ambiguous scenarios?
- Is the file ready for implementation by `mobile-test-automation`?

If any answer is `no`, fix the plan before proceeding.

---

## Handoff to Automation

Once the testcases file is approved, hand it off to
`mobile-test-automation`.

The automation skill should use the approved list as the source of truth for:

- live UI dump and locator validation
- Page Object creation
- Actions and step orchestration
- data provider setup
- actual E2E test implementation

---

## Rules

- Never invent a flow not supported by product context or the live app
- Never assume a login or auth method without confirming the recorded strategy
- Do not mix product intent with implementation detail
- Keep the test plan grounded in observable outcomes, not internal assumptions
- Mark blockers explicitly instead of silently skipping a scenario
- Keep `P0` cases focused on business-critical release confidence
- Do not commit secrets, tokens, or real account data

## Related Skills

- `get-mobile-context` — provides the product/feature context and flow input
- `get-mobile-auth` — defines the login / OTP / SSO strategy used by the plan
- `mobile-test-automation` — implements the approved test cases on the live app
- `mobile-test-report` — validates the executed automation after implementation
