# Context: Group Fee & Attendance Management (`cofee-group-fee-attendance`)

## Freshness

| Field | Value |
|-------|-------|
| Last updated | 2026-09-07 |
| Env checked | Unknown — not yet checked against dev/stg/uat |
| Confirmed on device | no |
| Owner | sreeshma@keyvalue.systems |

## Source links (optional — fill when available)

| Source | Link / key | Status |
|--------|------------|--------|
| Jira | — | Not available |
| PRD | — | Not available |
| Figma | 5 screenshots shared in conversation (no Figma file link/key given) | Available |
| App source / walkthrough | — | Not available (only the built APK was provided, no readable source or live device confirmation yet) |

## Feature

| Field | Value |
|-------|-------|
| App slug | cofee |
| Feature slug | group-fee-attendance |
| Platforms | android (Figma frames are mobile-sized, 375×1039 — no iOS frames shown) |
| Account type | Unknown — no account-type indicator visible in the shared frames |

## Screens in scope

| Screen | Purpose |
|--------|---------|
| Home | Entry point — shows Overview (amount collected/due), Groups & Members counts, Dues, Groups list, and "Add New" group CTA |
| Create group — fee type picker | Modal to choose **Fixed fee** or **Attendance based fee** before entering group details |
| Create Group — Fixed fee form | Group name, fixed amount, installments toggle, fee collection day/start date, group deactivation date, enable-attendance toggle, member list |
| Create Group — Attendance based fee form | Group name, rate per class, deactivation date, "when should payment be requested" setting, billing period, installments toggle, working days, notify-absentees toggle, member list |
| Request date picker | Sub-modal off the Attendance-based form — First day of month / Last day of month / Custom day of month (1–28 grid) |
| "When should payment be requested?" modal | Sub-modal off the Attendance-based form — Monthly vs After a specific number of classes |
| Attendance marking | Search + All/Present/Absent/Late filter, alphabetically grouped member list with present/absent toggle per member, Submit |
| Attendance limit reached dialog | Warns when marking attendance past a 10-session limit |
| Edit Group — Fixed fee | Same fields as the Fixed fee create form, pre-filled |
| Edit Group — Attendance based fee | Same fields as the Attendance-based create form, pre-filled |
| Rate per class updated dialog | Confirms a rate change on an Attendance-based group before applying it |
| Member detail | Active/Inactive toggle, editable fee details card, editable contact details card, payment history (All/Paid/Pending tabs) |
| Deactivate member dialog | Confirms deactivation, with a choice to send/not send a payment link first |
| Delete member dialog | Confirms deletion, same payment-link choice, plus a data-loss warning |

## Happy path

Two separate happy paths, since fee model is chosen up front and drives the rest of the form.

**A — Create a Fixed fee group**
1. From Home, tap **Add New** to open the "Create group" fee-type picker.
2. Select **Fixed fee** and tap **Proceed**.
3. Enter group name, fixed amount, optionally enable "Accept payments as installments", set fee collection day and start date, optionally set a group deactivation date, optionally enable attendance.
4. Review/adjust the member list (pre-populated in the screenshots with 4 members and default amounts).
5. Tap **Finish**.

**B — Create an Attendance based fee group**
1. From Home, tap **Add New** to open the "Create group" fee-type picker.
2. Select **Attendance based fee** and tap **Proceed**.
3. Enter group name, rate per class, optionally set a group deactivation date.
4. Choose "When should payment be requested?" — **Monthly** (with a request-date sub-choice: first/last/custom day of month) or **After a specific number of classes** (with a "send payment request when usage reaches" count).
5. Optionally enable installments, set working days, optionally enable "Notify absentees".
6. Review/adjust the member list and per-member rate.
7. Tap **Finish**.

**Attendance marking**
1. Open a group's Attendance screen.
2. Search or filter (All/Present/Absent/Late) and toggle each member Present/Absent.
3. Tap **Submit**.

**Editing a group / member**
1. Open Edit Group (Fixed fee or Attendance based — same field set as the corresponding create form, pre-filled).
2. Change a field (e.g. rate per class) and confirm via the resulting dialog where one appears (e.g. "Rate per class updated").
3. Tap **Finish**.

## Business rules

- A group is created as **either** Fixed fee **or** Attendance based fee — chosen on the fee-type picker before the rest of the form is shown. (Figma: "Create group" modal)
- Fixed fee: "Accept payments as installments" — tooltip states members with an amount **above ₹2,000** can split their payment into installments. (Figma: Fixed fee create form tooltip)
- Fixed fee: fee collection has both a recurring **day** (e.g. "Monthly - 15th day of month") and a **start date**; "Payment links will be sent after the start date." (Figma: Fixed fee create/edit forms)
- Group deactivation date is optional on both fee types; "Group will get deactivated after end date." (Figma: both create forms)
- "Enable attendance" is a toggle available on the **Fixed fee** form too — attendance tracking isn't exclusive to Attendance-based groups. (Figma: Fixed fee create/edit forms)
- Attendance based fee: rate is per class ("Enter the amount to charge per class attended"). (Figma: Attendance based create form)
- Attendance based fee: "When should payment be requested?" has two modes:
  - **Monthly** — "Fee will be calculated for attendance marked till the previous day," paired with a Request-date choice of First day of month / Last day of month / Custom day of month (custom picker shows days **1–28** only).
  - **After a specific number of classes** — "Payment link is sent automatically the next day once a student completes this many classes," paired with a "Send payment request when usage reaches" count input.
  (Figma: "When should payment be requested?" modal + Request date modal)
- Attendance based fee also supports "Accept payments as installments" (same toggle as Fixed fee, no threshold text shown on this form — see Open Questions). (Figma: Attendance based create form)
- Attendance based fee has a **Working days** selector (S M T W T F S) and a **Notify absentees** toggle; neither appears on the Fixed fee form. (Figma: Attendance based create/edit forms)
- Attendance marking has a documented **10-session limit** per billing cycle: marking beyond it shows a dialog — "Any additional attendance, including this entry, will be considered for fee calculation" — with Cancel/Got it, i.e. it warns but does not block the entry. (Figma: Attendance limit reached dialog)
- Changing "Rate per class" on an existing Attendance-based group shows a confirmation dialog — "The updated rate per class will be applied for fee calculation in this billing cycle" — before the change is applied. (Figma: Rate per class updated dialog)
- Member detail shows an Active/Inactive toggle, an editable Fee details card (amount/rate, recurrence/billing period, next request date), an editable Contact details card (WhatsApp number, alternate number), and payment history filterable by All/Paid/Pending. (Figma: Member detail screens, both fee-type variants)
- Deactivating a member prompts a choice to send or not send a payment link for classes already attended first; choosing "Don't send" carries the attendance forward into the next billing cycle instead. (Figma: Deactivate member dialog)
- Deleting a member offers the same payment-link choice, but explicitly warns that **attendance data will not be carried forward** after deletion — unlike deactivation. (Figma: Delete member dialog)

## Edge cases / unknowns

- Whether the fee model (Fixed vs Attendance based) can be changed after a group is created, or is locked in at creation — **Unknown**. Every Edit Group frame shown matches its original fee type; no in-edit toggle between the two is visible.
- What happens to any outstanding/pending dues when "Don't send payment link" is chosen on deactivate or delete — **Unknown** beyond the attendance-carry-forward note; no statement about the money side.
- Whether "Working days" and "Notify absentees" apply to a **Fixed fee** group that also has "Enable attendance" turned on — **Unknown**; those two controls only appear on the Attendance-based form in the shared frames.
- Whether the ₹2,000 installment threshold (stated only via a tooltip on the Fixed fee form) also applies to the same toggle on the Attendance-based form — **Unknown**.
- Two Member-detail frames for the same member show "Billing period: Monthly" in one and "Billing period: Classes" in another — **Assumption**: these correspond to the group's "Monthly" vs "After a specific number of classes" payment-request setting, but the two frames aren't shown side-by-side against a single group's setting to confirm the mapping.
- Account type / tenant model (e.g. multi-org support implied by "Soulful Studios" as an org name on Home) — **Unknown**; no login or account-switch screen was included in the shared frames.
- Small circular avatar badges (initials "K"/"S") and callout tooltips layered on several frames, plus the "375 × 1039" dimension label, are Figma collaboration cursors/annotations, not app UI — excluded from scope.

## Test data needs (no secrets)

| Need | How supplied |
|------|----------------|
| Logged-in user | Mobile + OTP, fixed OTP in dev — `TEST_MOBILE`/`TEST_OTP` in `.env.dev` (see `docs/cofee-flow.md` → Known blockers / Test data) |
| A group with 4+ members, to exercise both fee-type create flows | Unknown — no seeding/API strategy confirmed yet; likely created in-test via the flow itself |
| A member with 10 recorded attendance sessions, to trigger the attendance-limit dialog | Unknown — needs either a seeded fixture or 10 in-test attendance submissions |
| A member with recorded attendance + pending dues, to exercise deactivate/delete payment-link choices | Unknown |

## Known product quirks

- **Live device confirmation (2026-09-07, dev build `builds/cofee-dev.apk`, versionName
  `c15dceda7c75edbd955de7d42e4fd2eebd6a8d26-dev`, versionCode 116) found this dev build
  does not yet contain most of this feature.** Confirmed via a real Appium session against
  a booted emulator, logged in as the dev test account (see `TEST_MOBILE` in `.env.dev`):
  - "Add New" → "Create group" opens a **"Select members"** step (From Contacts / Manually)
    *before* any group-details form — not a fee-type picker with a pre-populated member list
    as shown in Figma.
  - After adding a member, the app goes straight into a **Fixed-fee-only** "Create group"
    form. There is **no Fixed fee vs Attendance based fee choice anywhere** — no radio, no
    tab, no toggle.
  - The Fixed-fee create/edit form has no **"Enable attendance"** toggle either.
  - Checked an existing group's **Edit Group** screen too (`QA Group S1Q34L`, 0 members) —
    same result: "Fixed fee details" only, nothing attendance-related.
  - Checked the hamburger menu (Account Details / About CoFee / Help Center / Send feedback
    / Dark Theme / Log out) for a hidden flag or account-type switch — nothing relevant.
  - **Conclusion: Attendance based fee, the fee-type picker, "Enable attendance," attendance
    marking, the rate-per-class-updated dialog, working days, notify absentees, and the
    attendance-limit dialog are not implemented in this build.** Only Fixed fee group
    create/edit exists today. The Figma set this context doc was written from appears to be
    a forthcoming design, not yet shipped to dev.
  - Also live-confirmed as working: login (mobile + OTP, fixed dev OTP), Home screen
    structure, Groups tab / group list, group detail screen with Deactivate / Edit Group
    kebab menu, and the Payments tab (All/Paid/Pending filters, payment detail view).

## Existing automation

| Layer | Path |
|-------|------|
| Tests | None yet |
| Steps / actions / POs | None yet — `src/page_objects/cofee/`, `src/page_actions/cofee/`, `src/steps/cofee/` are empty skeletons from `create-mobile-framework-structure` |

## Open questions

- Is the fee model (Fixed fee vs Attendance based) editable after group creation?
- What happens to pending dues (not just attendance) when "Don't send payment link" is chosen on deactivate/delete?
- Do "Working days" and "Notify absentees" apply to a Fixed-fee group with attendance enabled, or only to Attendance-based groups?
- Does the ₹2,000 installment threshold shown on the Fixed fee form also gate installments on the Attendance-based form?
- Does "Billing period: Classes" vs "Billing period: Monthly" on the member-detail screen map 1:1 to the group's "After a specific number of classes" vs "Monthly" setting?
- What account/org model is this ("Soulful Studios")? Single-org per login, or multi-org switch? No login/account screens were in the shared Figma set.

## Handoff

`get-mobile-auth` done (mobile + OTP, fixed OTP in dev). Next: `mobile-test-design` →
approve `cofee-group-fee-attendance-testcases.md` → `mobile-test-automation`.
