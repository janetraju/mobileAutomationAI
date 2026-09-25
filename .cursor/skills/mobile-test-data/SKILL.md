---
name: mobile-test-data
description: >-
  Decides and documents how a feature's tests get the application/backend
  data they need — isolated vs. shared fixtures, seeding, uniqueness, and
  who owns cleanup — before automation writes tests that quietly pollute or
  depend on shared state. Use when a new feature needs test data set up,
  when a shared test account/group/record is accumulating synthetic data
  from repeated runs, or when a test's precondition can't be created
  through the app's own UI in a single deterministic step.
---

# Mobile Test Data

Decide **where test data lives and who cleans it up** — a concern distinct
from `teardown` (device/session/app *runtime* state) and from
`get-mobile-auth` (login credentials). This skill covers everything else a
test needs to exist before it runs: a group, a record, an account, a
product, a historical entry — anything the app's backend has to know about.

This skill documents a **strategy**; it does not write the Page Objects or
steps that create the data (`mobile-test-automation` does), and it does not
review whether existing tests already violate the chosen strategy
(`pr-review-changes` does, once contract rules exist to check against).

## Why this exists

A feature's tests each added a uniquely-named member to the one shared test
group used for that feature. It worked — until the group had accumulated
20+ synthetic members from repeated runs, at which point a *different*
test's assumption ("a fresh day defaults to showing every current group
member") silently broke: with that much accumulated data, nothing was
excludable as "new" without first removing the pollution, which needed a
UI flow that was never automated because no one had decided in advance
whose job cleanup was. The fix wasn't a better locator — it was deciding,
before writing more tests, whether to keep growing shared state or isolate
it. That decision is what this skill exists to force early instead of
after the second test builds on the first one's mess.

## When to Use

- Before `mobile-test-automation` writes the first test for a feature that
  needs backend data (a group, account, record, etc.) to exist
- When a shared fixture (account, group, dataset) used by more than one
  test is visibly accumulating synthetic entries run over run
  - Concretely: content that grows and, in a specific case, means every
    fresh submission enumerates every current entry, breaking a test that
    assumed a short list — pinning the strategy that predicts unbounded
    growth from here is exactly this case
- When a test's precondition (e.g. "attendance already submitted for a
  historical day," "a payment link already generated") can't be produced
  by the app's own UI in one deterministic step — deciding how to fake or
  seed it belongs here, before `mobile-test-automation` improvises one

## Strategy Options

| Strategy | Use when | Trade-off |
|----------|----------|-----------|
| **Isolated fixture** — a dedicated test account/group/record used only by this feature's tests | Default choice. The entity is cheap to create and the feature doesn't need to interact with pre-existing real-looking data | Slower first-time setup (one extra creation step); avoids all pollution and cross-test coupling |
| **Shared fixture, self-contained per test** | Creating a dedicated entity per test is expensive (multi-step, slow) but each test can still make its own uniquely-named child records inside it | Still grows unbounded over time — only viable with either an accepted growth ceiling or a scheduled reset (see Output) |
| **Shared fixture, reused unmodified** | The precondition is read-only or the mutation is trivially idempotent (e.g. "this record exists," re-asserted every run) | Any test that mutates it breaks every other test relying on its original state — the exact failure mode this skill exists to prevent; use only when no test will ever change it |
| **Backend/API seeding** (bypass the UI to create data directly) | The precondition can't be reached via UI in one step (e.g. a payment-link cycle needing real time to elapse), and a backend/API/DB path exists | Fastest and most deterministic, but only as trustworthy as the seeding script — keep it in `data/<app_slug>/`, never invent the schema without confirming it against a real record first |

Default to **isolated fixture** unless there's a specific reason not to.
"It's more setup work" is not a reason — that one-time cost is what the
pollution above cost anyway, just paid later and by someone else.

## Output

Document, in `docs/<app_slug>-flow.md` → a **Test Data** section (add one if
missing) per feature:

- Which strategy was chosen and why
- The fixture's identity (account/group/record name or ID) if isolated or
  shared — so the next person doesn't create a second one by accident
- **Growth expectation**: if the strategy can still accumulate data (shared
  fixture, self-contained per test), say so explicitly and state either an
  accepted ceiling ("fine up to ~N entries because X") or a reset mechanism
  — don't leave it unbounded and undocumented the way the original case
  was
- **Cleanup ownership**: does each test tear down what it created (needs a
  verified removal/deletion flow — confirm live, same as any other locator,
  before relying on it), or is there a separate scheduled/manual reset?
  Never assume cleanup "should" happen without a mechanism that actually
  does it
- Any backend/API seeding scripts, under `data/<app_slug>/` per `AGENTS.md`
  (never invent the schema — confirm against a real record first)

## Workflow

### Step 1 — Identify What the Feature Actually Needs

From the feature's context/test-design docs, list every precondition that
requires backend data to exist before a test can run — not just "a logged
in user" (that's `get-mobile-auth`), but domain entities: groups, records,
historical states, other users/accounts the flow interacts with.

### Step 2 — Check for an Existing Fixture

Before creating anything, check `docs/<app_slug>-flow.md` → Test Data for
whether a suitable fixture already exists for this app. Reuse it if its
documented strategy fits; don't create a second overlapping one.

### Step 3 — Choose a Strategy Per Precondition

Use the table above. Different preconditions in the same feature can use
different strategies — don't force one choice for everything.

### Step 4 — Confirm Any Seeding Path Live

If backend/API seeding is chosen, confirm the actual request/schema against
a real record on a live environment before writing the script — the same
"never invent, confirm live" rule that governs locators applies here to
data shapes.

### Step 5 — Document and Hand Off

Write the Test Data section per Output above, then hand off to
`mobile-test-automation` to implement the setup/teardown steps against the
chosen strategy.

## Rules

- Never let a test assume shared data will stay in the state a previous
  test left it — either isolate, or make the test re-establish what it
  needs itself
- Never leave unbounded growth undocumented — an accepted ceiling or a
  reset mechanism, always one of the two, never neither
- Never invent a backend/API data shape — confirm it against a real record,
  same standard as UI locators
- Cleanup that "should" happen but isn't automated or scheduled isn't a
  strategy — it's the same gap that caused the problem this skill exists
  to prevent

## Related Skills

- `teardown` — device/session/app *runtime* state between runs; this skill
  is application/backend *data* that outlives any single run
- `get-mobile-auth` — the login identity used to reach the data this skill
  is about; a separate concern
- `mobile-test-automation` — implements the setup/teardown steps this skill
  decides the strategy for
- `mobile-coverage-audit` — could flag a feature with no documented Test
  Data section the same way it flags missing coverage categories, if this
  becomes a recurring gap
