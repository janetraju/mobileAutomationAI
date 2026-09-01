# Feature context (`docs/context/`)

This folder is the **product truth** for automation: what a feature does, what to
test, and which cases are approved. Locators are **not** finalized here — confirm
them live via `discover-mobile-locators` / Appium MCP.

## Naming

```text
docs/context/<app_slug>-<feature-slug>-context.md
docs/context/<app_slug>-<feature-slug>-testcases.md
```

Examples: `cofee-login-context.md`, `cofee-create-group-testcases.md`

## Templates

Copy from `_templates/` when starting a new feature:

| File | Purpose |
|------|---------|
| `_templates/context-template.md` | Discovery / product rules |
| `_templates/testcases-template.md` | Approved P0/P1/P2 cases |

## Rules

1. **No new feature automation** without an existing `*-context.md` and an
   **Approved** `*-testcases.md` (see `AGENTS.md`).
2. **No secrets** — phones, OTPs, passwords stay in `.env` only.
3. **Freshness** — update the checklist at the top when product behavior changes.
4. **Flow index** — `docs/<app_slug>-flow.md` links here; it does not duplicate
   long TC text.
5. **Product vs locators** — context/PRD/Figma = *what*; live dump = *how*.

## Index

See [`../cofee-flow.md`](../cofee-flow.md) for CoFee coverage status and links.
