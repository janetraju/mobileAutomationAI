---
name: create-mobile-framework-structure
description: >-
  Bootstraps a brand-new mobile app into an Appium-based, Page Object
  Model (POM) automation repo: analyzes the APK/IPA, registers the app in
  APP_REGISTRY, wires .env (including Appium capabilities), and scaffolds
  the four-layer POM folder skeleton. Use when onboarding a new app,
  setting up project structure for the first time, or before any feature
  context, auth setup, or test design work can begin for that app.
---

# Create Mobile Framework Structure

Bootstrap a new application into the **app-agnostic** framework so downstream
skills (`get-mobile-context`, `get-mobile-auth`, `mobile-test-design`,
`mobile-test-automation`) have a configured app to work against.

This framework is **Appium 2.x** based and follows a **four-layer Page
Object Model (POM)**: Page Objects (locators) → Page Actions (interactions)
→ Steps (orchestration) → Tests. Every app this skill onboards gets the same
Appium/POM skeleton — no other driver or architecture is supported.

Repository conventions (Page Objects, locators, waits, coding standards, etc.)
are defined in `AGENTS.md`. This skill only sets up the app registration and
folder skeleton — it does not gather feature context, define credentials, or
author any test logic.

## When to Use

Use this skill when an app is **not yet configured**, i.e. any of the
following is true:

- `APP_SLUG` is not present in `.env`
- The app is not registered in `APP_REGISTRY`
- The app's project folders don't exist under `src/`, `tests/`, `data/`, `docs/`

If the app is already configured, skip this skill entirely and go straight to
`get-mobile-context`.

## Output

- App registered in `APP_REGISTRY`
- `.env` populated with:
  - App identity: `APP_NAME`, `APP_SLUG`, `APP_TYPE`, `APP_PACKAGE`,
    `APP_ACTIVITY`, `APP_PATH`
  - Appium capabilities: `PLATFORM`, `APPIUM_HOST`, `APPIUM_PORT`,
    `DEVICE_NAME`
- Empty four-layer **POM** folder skeleton created (no locators, no logic):
  ```
  src/page_objects/<app_slug>/    # Page Object Model — Layer 1
  src/page_actions/<app_slug>/    # Layer 2
  src/steps/<app_slug>/           # Layer 3
  src/constants/<app_slug>/
  tests/test/<app_slug>/          # Layer 4
  data/<app_slug>/
  ```
- `docs/<app_slug>-flow.md` stub, marked **Unconfirmed**

Commit these outputs. They are the prerequisite for every other skill in the
feature lifecycle.

---

# Workflow

## Step 1 — Confirm the App Isn't Already Configured

Check `.env`, `APP_REGISTRY`, and existing folders (see When to Use). If
already configured, stop and hand off to `get-mobile-context`.

## Step 2 — Obtain the Build Artifact

Get the APK (Android) or IPA (iOS) for the app. Ask the user for a path or
upload if not already available under `builds/`.

## Step 3 — Analyze the Artifact

```bash
invoke app:analyze --apk=builds/<app>.apk
```

Extract package name, launch activity, and app type (native / Flutter /
React Native / hybrid).

## Step 4 — Register the App

Configure, in this order:

1. `APP_REGISTRY` — add the new app entry
2. `.env` — set app identity (`APP_NAME`, `APP_SLUG`, `APP_TYPE`,
   `APP_PACKAGE`, `APP_ACTIVITY`, `APP_PATH`) and Appium capabilities
   (`PLATFORM`, `APPIUM_HOST`, `APPIUM_PORT`, `DEVICE_NAME`)
3. Project folders — create the empty four-layer **POM** skeleton listed in
   Output

Do **not** derive Page Objects, locators, or any business logic from the APK
analysis — that requires a live device dump via Appium, done later by
`mobile-test-automation`.

## Step 5 — Create the Flow Doc Stub

Create `docs/<app_slug>-flow.md` with a placeholder structure (sections for
flows, known blockers, test data) and mark its contents **Unconfirmed** until
`get-mobile-context` and `get-mobile-auth` fill them in.

## Step 6 — Hand Off

Once registration, `.env`, folders, and the flow doc stub exist, hand off to:

- `get-mobile-context` for feature/PRD/Figma intake
- `get-mobile-auth` for credential/OTP strategy setup

Do not proceed into feature context, credentials, or automation from this
skill — that is out of scope.
