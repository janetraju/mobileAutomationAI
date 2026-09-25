---
name: mobile-ci-pipeline
description: >-
  Packages this framework's test run for CI (GitHub Actions by default)
  instead of a human running `invoke test` on a local dev machine —
  provisions a hardware-accelerated emulator/simulator, runs
  mobile-env-doctor's checks first, executes the suite, and publishes the
  Allure report as a build artifact. Use once a suite is established and
  local execution on a shared dev machine is becoming unreliable or
  doesn't scale, or when setting up automation for a new app that should
  run in CI from the start.
---

# Mobile CI Pipeline

Move test execution off a shared local machine and onto a runner dedicated
to it. This is the direct answer to a real, evidenced problem: local
emulators compete for host CPU/memory with everything else running on a
dev machine (an IDE, a browser, other tools), and under sustained load that
degrades into device-level unreliability — an actual Android "System UI
isn't responding" ANR was observed, not simulated — independent of any
test code. A dedicated CI runner doesn't have that competition.

**Honesty note, matching this skill's own standard:** the workflow file
below is written from GitHub Actions' documented Android-emulator and
macOS-runner support, not from a run this skill has actually executed and
watched pass. Treat it as a correct starting point to adapt, not a
proven pipeline — run it once and fix whatever's actually wrong before
trusting it as CI gate.

## When to Use

- A suite has grown past "one person runs it locally" and needs to run on
  every PR
- `mobile-env-doctor` keeps reporting host resource pressure on the
  machine tests have been running on locally
- Setting up a new app's automation and CI should exist from day one
  rather than bolted on later
- An existing CI workflow's emulator step is unreliable (software
  rendering, no hardware acceleration, wrong API level)

## Output

- `.github/workflows/mobile-tests.yml` (or the equivalent for another CI
  system, if asked) that:
  1. Checks out the repo, sets up Python + Node (for Appium)
  2. Installs dependencies (`invoke install`, `appium`,
     `appium driver install uiautomator2`)
  3. Boots a **hardware-accelerated** Android emulator (KVM-backed on
     Linux runners — software rendering is the thing that caused today's
     unreliability locally; don't repeat it in CI) or an iOS simulator on
     a `macos-latest` runner
  4. Runs an environment check equivalent to `mobile-env-doctor` Steps 1–3
     before the suite, so a bad runner fails fast with a clear message
     instead of producing confusing test failures
  5. Runs `invoke test` (or a marker-scoped subset)
  6. Uploads `target/allure-results/` (or the generated
     `target/allure-report/`) as a build artifact regardless of pass/fail
- A short section in `docs/<app_slug>-flow.md` noting CI is set up, which
  workflow file owns it, and which markers/subset it runs by default

## Workflow

### Step 1 — Confirm the Suite Is Ready to Run Headless

Before wiring CI, confirm locally:

- `invoke test` passes with no manual/interactive steps required (no
  `@pytest.mark.manual_otp` tests in the default marker set)
- Credentials the suite needs (`TEST_MOBILE`, `TEST_OTP`, etc., per
  `get-mobile-auth`) are available as CI secrets, not only in a local
  `.env`

### Step 2 — Choose the Runner Per Platform

| Platform | Runner | Emulator/simulator |
|----------|--------|---------------------|
| Android | `ubuntu-latest` (GitHub-hosted) or a self-hosted Linux runner | `reactivecircus/android-emulator-runner` (or equivalent) — **must** confirm hardware acceleration (KVM) is actually available on the runner; a software-rendered CI emulator inherits the same unreliability as the local one that motivated this skill |
| iOS | `macos-latest` (GitHub-hosted) | `xcrun simctl` boot — GitHub-hosted macOS runners include Xcode; confirm the specific Xcode/simulator versions available match what the app needs |

### Step 3 — Write the Workflow

Adapt this starting point rather than inventing structure from scratch —
this is what "not yet proven end-to-end" in the header refers to, so
re-verify each step's exact syntax/action version against current
documentation before trusting it:

```yaml
name: Mobile Tests
on: [pull_request]
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: pip install -e .
      - run: npm install -g appium && appium driver install uiautomator2
      - name: Run Android emulator + tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          arch: x86_64
          force-avd-creation: false
          emulator-options: -no-snapshot -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none
          disable-animations: true
          script: |
            appium --address 127.0.0.1 --port 4723 &
            sleep 5
            invoke test --markers "e2e and p0"
        env:
          TEST_MOBILE: ${{ secrets.TEST_MOBILE }}
          TEST_OTP: ${{ secrets.TEST_OTP }}
      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: target/allure-results
```

Note `-gpu swiftshader_indirect` above is a CI-runner fallback (GitHub-hosted
Linux runners' KVM support varies) — check `reactivecircus/android-emulator-runner`'s
current docs for the actual hardware-acceleration flag available on the
runner tier in use; don't silently accept software rendering as the default
if a faster option exists, per the same reasoning as the local host issue
this skill exists to solve.

### Step 4 — Run It Once and Fix What's Actually Wrong

Push the workflow, watch the first real run, and treat any failure here as
a CI-config bug, not a test bug — a suite passing locally and failing only
in CI points at the pipeline (missing secret, wrong API level, no hardware
acceleration), not the automation.

### Step 5 — Hand Off

- `mobile-test-report` still triages any test-level failures the same way
  it would locally, from the uploaded artifact
- `pr-review-changes` / `add-pr-description` proceed once CI is green

## Rules

- Never accept software-rendered emulation in CI without checking whether
  hardware acceleration is available first — that's the exact condition
  that produced an unreliable local environment
- Never skip Step 4 — a workflow file that "looks right" and a workflow
  that has actually completed a real run are different claims
- Secrets belong in the CI system's secret store, never committed into the
  workflow file or a checked-in `.env`

## Related Skills

- `mobile-env-doctor` — the same host/device readiness checks, run inside
  CI instead of manually on a dev machine
- `mobile-test-report` — triages failures from the CI-produced artifact
  the same way as a local run
- `create-mobile-framework-structure` — the app this pipeline runs against
  must already be bootstrapped
