---
name: mobile-build-fetch
description: >-
  Gets the correct APK/IPA for testing from wherever the team actually
  publishes builds — a CI artifact, Google Play internal testing track,
  Firebase App Distribution, TestFlight/App Store Connect, or building from
  source — instead of assuming a build is already sitting locally. Use
  before create-mobile-framework-structure for a brand-new app, or any time
  the local build under test is stale and a fresh one is needed (a new
  release candidate, the latest CI build for regression).
---

# Mobile Build Fetch

Answer "where does the build under test actually come from?" before
`create-mobile-framework-structure` asks for a path. Fetching a build is
not one-time — a growing suite needs a *fresh* build regularly (every CI
run, every release candidate), so this is a recurring skill, not only a
first-bootstrap step.

This skill only acquires the artifact. It does not analyze it
(`create-mobile-framework-structure` Step 3 does) and does not decide
whether the build is the right *version* for a specific test run beyond
what's documented here — that's a team/release-process decision to record,
not infer.

## Why This Matters

Every skill in this framework assumes `builds/<app>.apk` (or `.ipa`)
already exists. That assumption breaks the moment automation needs to run
against something other than a build a developer happened to hand over —
the latest CI build, a specific release candidate, or a build from a
teammate's machine. Without an explicit, repeatable fetch step, the
default failure mode is a stale local build silently drifting from what's
actually shipping, with no one noticing until a test fails against
behavior that changed three versions ago.

## When to Use

- Bootstrapping a brand-new app and no build has been provided yet
- The local build under test is more than a few versions/builds old
- A specific release candidate needs to be tested, not just "whatever's
  local"
- Setting up `mobile-ci-pipeline`, which needs a build-fetch step of its
  own inside the workflow (CI can't rely on a human having placed a file
  under `builds/`)

## Sources

| Source | Android | iOS | Notes |
|--------|---------|-----|-------|
| **CI artifact** | `gh run download <run-id> -n <artifact-name>` (GitHub Actions) or the equivalent for the CI system in use | Same mechanism, if CI produces a signed IPA | Most reliable and reproducible — the build is exactly what CI tested. Prefer this when available. |
| **Google Play internal testing track** | Download from Play Console manually, or `bundletool` + the Play Developer API for programmatic access | — | Requires Play Console access; API access needs a service account |
| **Firebase App Distribution** | `firebase appdistribution:distribution:get` (Firebase CLI), or the console download link | Also supports iOS distribution | Needs the Firebase CLI authenticated and the app's Firebase project ID |
| **TestFlight / App Store Connect** | — | **No standard CLI download of a built IPA for local testing.** Apple's tooling (`altool`/Transporter) is for *uploading* builds, not retrieving one for automation. In practice, an IPA under test on iOS almost always comes from CI (which has the signing identity) or a local Xcode build — not a TestFlight download. | Don't assume iOS build acquisition mirrors Android's — it structurally doesn't, because of Apple's code-signing model. |
| **Build from source** | `invoke app:build` wrapping `./gradlew assembleDebug` (or the project's actual build command) | `xcodebuild archive` + export, which needs a valid signing identity/provisioning profile present on the machine | Only viable when the app's source repo and a working local toolchain are both available — don't attempt this as a fallback without confirming both exist |
| **Manual / already local** | — | — | What `create-mobile-framework-structure` Step 2 already covers when a path is simply handed over |

**iOS honesty note:** every Android row above has a reasonably direct path.
iOS's code-signing model means there usually isn't an equivalent
"just download the build" step — plan for CI or a local Xcode build being
the *only* realistic source, not a gap in this skill's coverage.

## Output

- The artifact saved as `builds/<app_slug>-<version>-<build_number>.apk`
  (or `.ipa`) — include version/build number in the filename, not just
  `<app>.apk`, so a stale build is visible at a glance instead of silently
  overwritten
- A short note in `docs/<app_slug>-flow.md` (or a per-fetch log if this
  runs often) recording: which source it came from, the version/build
  number, and when — enough for someone to answer "is this still the
  build we think we're testing?" without re-deriving it
- Hand off to `create-mobile-framework-structure` (new app) or straight to
  `mobile-test-automation` (refreshing an existing app's build)

## Workflow

### Step 1 — Confirm Where This Team Actually Publishes Builds

Ask, don't assume: CI artifact, an internal distribution service, or
source builds. Different teams differ, and guessing wrong means fetching
from a source no one actually trusts as canonical.

### Step 2 — Fetch Per the Source Table

Use the matching command/process above. For anything requiring
credentials (Play Developer API, Firebase CLI, CI access tokens), confirm
they're available via the CI/secrets system per `mobile-ci-pipeline` —
never hardcode a token into a fetch script.

### Step 3 — Verify What Was Actually Fetched

Before handing off, confirm the artifact is genuinely usable:

```bash
# Android — should print without error
aapt dump badging builds/<file>.apk | head -3
```

For iOS, confirm the IPA has a valid `Payload/*.app/Info.plist` and matches
the expected bundle ID — a corrupted or wrong-variant download is a common
failure mode worth catching here rather than at
`create-mobile-framework-structure` Step 3.

### Step 4 — Record and Hand Off

Write the Output note, then hand off per Output above.

## Rules

- Never silently overwrite a named build file — version/build number in
  the filename is what prevents "which build is this actually testing"
  from becoming an untraceable question later
- Never hardcode a distribution-service credential in a script committed
  to the repo — same rule as any other secret
- Don't assume iOS build acquisition works like Android's — verify the
  actual source per app rather than defaulting to "however Android does
  it"

## Related Skills

- `create-mobile-framework-structure` — consumes the fetched artifact for
  a new app
- `mobile-ci-pipeline` — needs its own build-fetch step wired into the
  workflow, since CI can't rely on a human placing a file locally
- `mobile-test-automation` — the eventual consumer of a refreshed build
  when regression-testing against a new release
