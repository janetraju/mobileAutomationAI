# Test cases: Group Fee & Attendance Management (`cofee-group-fee-attendance`)

Source: [`cofee-group-fee-attendance-context.md`](cofee-group-fee-attendance-context.md).
Auth: mobile + OTP, fixed OTP in dev (`TEST_MOBILE` / `TEST_OTP` in `.env.dev`,
see `docs/cofee-flow.md` → Known blockers / Test data).

Every case below assumes the tester is already logged in to CoFee via the
dev fixed-OTP strategy and is on the **Home** screen unless stated otherwise —
that satisfies the auth/session-state category for this feature; deeper
session-expiry / logout behavior belongs to a login-feature test plan, not
this one, since no login/session screen was in the Figma set this plan is
based on.

## Coverage category map

| Category | Cases |
|----------|-------|
| Happy path | P0-01, P0-02, P0-03, P0-04, P0-05, P0-06, P0-07, P0-08 |
| Validation / negative path | P2-03, P2-04 |
| Error handling | P2-03, P2-04 (form-level blocks — no server-error states were in the Figma set to design against) |
| Edge case | P2-01, P2-02, P2-05, P2-06 |
| Recovery / retry path | P1-07, P1-08 (choosing "Don't send payment link" and still completing the action) |
| Auth / session state | Satisfied by shared precondition above; see note |
| App state transitions | P0-07, P0-08 (Active → Inactive / Deleted), P1-10 (scheduled deactivation) |
| Regression risk area | P0-06 (rate-change confirmation), P2-02 (attendance-limit dialog) |

## Not covered — open questions from context doc

These are explicitly **not** designed into a case because the context doc
marks them Unknown and writing a case would mean inventing app behavior:

- Switching fee model (Fixed ↔ Attendance based) after group creation — no
  such control was visible in either Edit Group frame.
- Money-side outcome of "Don't send payment link" on deactivate/delete
  (only the attendance-carry-forward behavior is documented).
- Whether Working days / Notify absentees apply to a Fixed-fee group with
  attendance enabled.
- Whether the ₹2,000 installment threshold applies on the Attendance-based
  form the same way it's stated on the Fixed-fee form.

Confirm these on the live device during `mobile-test-automation`; promote to
real cases (and update the context doc) once confirmed either way.

---

## P0 — Release-blocking

```text
TC ID: group-fee-attendance-P0-01
Priority: P0
Scenario: Create a group with Fixed fee — happy path
Preconditions:
- Logged in (dev fixed OTP)
- On Home screen
- At least one existing contact/member available to add to the group
Steps:
1. Tap "Add New" under Groups.
2. On the "Create group" picker, select "Fixed fee" and tap Proceed.
3. Enter a group name.
4. Enter a fixed Amount.
5. Set Fee collection day and Fee collection start date.
6. Leave installments, deactivation date, and attendance off (defaults).
7. Confirm the pre-populated member list is present.
8. Tap Finish.
Expected result:
- Returns to Home / Groups list.
- New group appears in the Groups list with the entered name.
- Group's fee amount matches what was entered.
Assertions:
- Group name text visible in Groups list.
- Groups count increments by 1.
- Group detail (or list row) shows the entered fixed amount.
Automation notes:
- Locators for "Add New", fee-type radio, and form fields must be confirmed live — not yet dumped.
- Needs a fresh member/contact fixture per AGENTS.md test-data rules — do not reuse a shared group across parallel workers.
```

```text
TC ID: group-fee-attendance-P0-02
Priority: P0
Scenario: Create a group with Attendance based fee — Monthly payment request
Preconditions:
- Logged in (dev fixed OTP)
- On Home screen
- At least one existing contact/member available
Steps:
1. Tap "Add New" under Groups.
2. On the "Create group" picker, select "Attendance based fee" and tap Proceed.
3. Enter a group name and Rate per class.
4. Open "When should payment be requested?" and select "Monthly".
5. Open the Request date sub-modal, select "First day of the month", tap Apply.
6. Set Working days (leave default selection).
7. Tap Finish.
Expected result:
- Returns to Home / Groups list.
- New group appears with the entered name.
- Group's rate per class matches what was entered.
Assertions:
- Group name visible in Groups list.
- Groups count increments by 1.
- Group detail shows the entered rate per class.
Automation notes:
- Confirm live whether "Billing period" label reads "Monthly" or something derived from the request-date choice — context doc flags this as unconfirmed.
```

```text
TC ID: group-fee-attendance-P0-03
Priority: P0
Scenario: Create a group with Attendance based fee — payment requested after N classes
Preconditions:
- Logged in (dev fixed OTP)
- On Home screen
- At least one existing contact/member available
Steps:
1. Tap "Add New" under Groups.
2. On the "Create group" picker, select "Attendance based fee" and tap Proceed.
3. Enter a group name and Rate per class.
4. Open "When should payment be requested?" and select "After a specific number of classes", tap Proceed.
5. Enter a value (e.g. 8) in "Send payment request when usage reaches".
6. Tap Finish.
Expected result:
- Returns to Home / Groups list.
- New group appears with the entered name and rate.
Assertions:
- Group name visible in Groups list.
- "Send payment request when usage reaches" value is persisted (visible on re-opening Edit Group).
Automation notes:
- Re-open Edit Group after creation to confirm the usage-count value round-trips — this also doubles as an implicit state-persistence check.
```

```text
TC ID: group-fee-attendance-P0-04
Priority: P0
Scenario: Mark attendance for a group — happy path
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with members and attendance enabled
- On that group's Attendance screen
Steps:
1. For at least two members, toggle Present; for at least one member, toggle Absent.
2. Tap Submit.
Expected result:
- Submission succeeds (no error dialog).
- Re-opening the Attendance screen for the same day reflects the marked statuses.
Assertions:
- Marked members show the correct Present/Absent state on reload.
- No unexpected dialog (e.g. attendance-limit) appears when under the session limit.
Automation notes:
- Needs a fixture group with attendance enabled and a known member count.
```

```text
TC ID: group-fee-attendance-P0-05
Priority: P0
Scenario: Edit a Fixed fee group — update the amount
Preconditions:
- Logged in (dev fixed OTP)
- An existing Fixed fee group
- On that group's Edit Group screen
Steps:
1. Change the Amount field to a new value.
2. Tap Finish.
Expected result:
- Returns to Home / Groups list (or group detail).
- The group's amount reflects the new value.
Assertions:
- Updated amount is visible on the group (list row or detail) after save.
- Re-opening Edit Group shows the new amount pre-filled.
Automation notes:
- None beyond standard live-locator confirmation.
```

```text
TC ID: group-fee-attendance-P0-06
Priority: P0
Scenario: Edit an Attendance based group — update rate per class, confirm dialog
Preconditions:
- Logged in (dev fixed OTP)
- An existing Attendance based group
- On that group's Edit Group screen
Steps:
1. Change "Rate per class" to a new value.
2. Attempt to tap Finish (or trigger the field's own confirm step, per live behavior).
3. On the "Rate per class updated" dialog, tap Confirm.
Expected result:
- Dialog reads "The updated rate per class will be applied for fee calculation in this billing cycle."
- After Confirm, the group's rate per class reflects the new value.
Assertions:
- Dialog title "Rate per class updated" is visible before confirming.
- Post-confirm, updated rate is visible on the group.
Automation notes:
- Confirm live exactly when this dialog fires (on field blur, on Finish, or both) — Figma shows the dialog but not the trigger point.
- This is flagged as a regression-risk case — the dialog is the only "changes are cycle-scoped, not retroactive" signal in the whole feature.
```

```text
TC ID: group-fee-attendance-P0-07
Priority: P0
Scenario: Deactivate a member, sending a payment link first
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with an Active member that has recorded attendance
- On that member's detail screen
Steps:
1. Toggle the member's Active switch off (or use the deactivate action, per live UI).
2. On the "Deactivate member?" dialog, select "Send payment link".
3. Tap Deactivate.
Expected result:
- Member's status changes to Inactive.
- Dialog copy "Attendance has been recorded for this member..." was shown before confirming.
Assertions:
- Member detail's Active/Inactive control shows Inactive after the action.
- Member no longer appears in the group's active-members list (if such a list view exists) — confirm live.
Automation notes:
- Needs a fixture member with recorded attendance so the dialog's attendance-specific copy is guaranteed to appear (Figma implies the dialog's content is conditional on recorded attendance).
```

```text
TC ID: group-fee-attendance-P0-08
Priority: P0
Scenario: Delete a member, sending a payment link first
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with a member that has recorded attendance
- On that member's detail (or edit member details) screen
Steps:
1. Trigger the delete-member action.
2. On the "Delete member?" dialog, select "Send payment link".
3. Tap Delete.
Expected result:
- Member is removed from the group's member list.
- Dialog explicitly warned "Attendance data will not be carried forward after deletion" before confirming.
Assertions:
- Member no longer appears in the group's member list.
- Group's member count decrements by 1.
Automation notes:
- Use a disposable fixture member — deletion is not reversible per the dialog copy.
```

## P1 — Important, not release-blocking

```text
TC ID: group-fee-attendance-P1-01
Priority: P1
Scenario: Fixed fee group — enable installments for an amount above ₹2,000
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Fixed fee) form
Steps:
1. Enter an Amount greater than ₹2,000 (e.g. ₹2,500).
2. Toggle "Accept payments as installments" on.
3. Complete required fields and tap Finish.
Expected result:
- Group is created with installments enabled.
Assertions:
- Installments toggle state is persisted (visible on re-opening Edit Group).
Automation notes:
- Context doc tooltip states installments apply only above ₹2,000 — this case exercises the "allowed" side; see P2 for the boundary/negative side if the toggle is meant to be disabled at/under the threshold (unconfirmed live).
```

```text
TC ID: group-fee-attendance-P1-02
Priority: P1
Scenario: Attendance based group — enable installments
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Attendance based fee) form
Steps:
1. Enter a Rate per class.
2. Toggle "Accept payments as installments" on.
3. Complete required fields and tap Finish.
Expected result:
- Group is created with installments enabled.
Assertions:
- Installments toggle state is persisted (visible on re-opening Edit Group).
Automation notes:
- Context doc flags it as Unknown whether the ₹2,000 threshold text from the Fixed-fee form also applies here — confirm live whether any threshold copy/behavior appears.
```

```text
TC ID: group-fee-attendance-P1-03
Priority: P1
Scenario: Attendance based group — custom day-of-month request date
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Attendance based fee) form, "When should payment be requested?" set to Monthly
Steps:
1. Open the Request date sub-modal.
2. Select "Custom day of the month" and pick a day (e.g. 4th).
3. Tap Apply.
4. Complete required fields and tap Finish.
Expected result:
- Group is created with the custom request day applied.
Assertions:
- Re-opening Edit Group shows the same custom day selected.
Automation notes:
- The picker grid only shows days 1–28 in Figma — confirm live that 29/30/31 are genuinely unavailable, not just cropped.
```

```text
TC ID: group-fee-attendance-P1-04
Priority: P1
Scenario: Fixed fee group — enable attendance tracking
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Fixed fee) form
Steps:
1. Complete required fields.
2. Toggle "Enable attendance" on.
3. Tap Finish.
Expected result:
- Group is created with attendance enabled.
Assertions:
- The group's Attendance screen is reachable and shows its member list.
Automation notes:
- Follow-up: check live whether Working days / Notify absentees appear for this group once attendance is enabled — context doc marks this Unknown.
```

```text
TC ID: group-fee-attendance-P1-05
Priority: P1
Scenario: Attendance based group — restrict working days and enable absentee notification
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Attendance based fee) form
Steps:
1. Complete required fields.
2. Deselect Saturday and Sunday in Working days, leaving Mon–Fri selected.
3. Toggle "Notify absentees" on.
4. Tap Finish.
Expected result:
- Group is created with the selected working days and absentee notification on.
Assertions:
- Re-opening Edit Group shows Mon–Fri selected and Notify absentees on.
Automation notes:
- None beyond standard live-locator confirmation.
```

```text
TC ID: group-fee-attendance-P1-06
Priority: P1
Scenario: Attendance screen — filter and search members
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with members in mixed attendance states (some marked Present, some Absent)
- On that group's Attendance screen
Steps:
1. Tap the "Present" filter chip.
2. Confirm only Present members are listed.
3. Tap the "Absent" filter chip.
4. Confirm only Absent members are listed.
5. Clear filters (tap "All"), then search for one member's name.
Expected result:
- Each filter narrows the list to matching members only.
- Search narrows the list to the matching member(s).
Assertions:
- Visible member list matches the active filter/search at each step.
Automation notes:
- Needs a fixture group with members in known, mixed attendance states.
```

```text
TC ID: group-fee-attendance-P1-07
Priority: P1
Scenario: Deactivate a member without sending a payment link
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with an Active member that has recorded attendance
- On that member's detail screen
Steps:
1. Trigger the deactivate action.
2. On the "Deactivate member?" dialog, select "Don't send payment link".
3. Tap Deactivate.
Expected result:
- Member's status changes to Inactive.
- No payment link is sent (best-effort — confirm via app-visible state, not a real payment gateway check).
Assertions:
- Member detail shows Inactive.
- Dialog's "attendance will be carried forward and included in the next billing cycle" copy was shown for this choice.
Automation notes:
- This is the recovery/retry-style path — member stays actionable/consistent state without an immediate payment step.
```

```text
TC ID: group-fee-attendance-P1-08
Priority: P1
Scenario: Delete a member without sending a payment link
Preconditions:
- Logged in (dev fixed OTP)
- An existing group with a member that has recorded attendance
- On that member's detail (or edit member details) screen
Steps:
1. Trigger the delete-member action.
2. On the "Delete member?" dialog, select "Don't send payment link".
3. Tap Delete.
Expected result:
- Member is removed from the group's member list.
Assertions:
- Member no longer appears in the group's member list.
- Group's member count decrements by 1.
Automation notes:
- Use a disposable fixture member.
```

```text
TC ID: group-fee-attendance-P1-09
Priority: P1
Scenario: Member detail — payment history tabs filter correctly
Preconditions:
- Logged in (dev fixed OTP)
- An existing member with at least one Paid and one Pending payment record
- On that member's detail screen
Steps:
1. Tap the "Paid" tab.
2. Confirm only paid entries are listed.
3. Tap the "Pending" tab.
4. Confirm only pending entries are listed, each showing "Reminder sent!" where applicable.
Expected result:
- Each tab shows only entries matching its status.
Assertions:
- Visible entries' status matches the active tab.
- Pending entries with a reminder show the "Reminder sent!" label.
Automation notes:
- Needs a fixture member with both payment states pre-seeded — likely requires backend/API setup per `data/cofee/` scripts, not purely UI-driven.
```

```text
TC ID: group-fee-attendance-P1-10
Priority: P1
Scenario: Create a group with a group deactivation date set
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group form (either fee type)
Steps:
1. Complete required fields.
2. Set a Group deactivation date in the near future.
3. Tap Finish.
Expected result:
- Group is created with the deactivation date set.
Assertions:
- Re-opening Edit Group shows the same deactivation date.
Automation notes:
- Actual deactivation-on-date-reached behavior is out of scope for UI automation (time-dependent) — this case only verifies the date is accepted and persisted.
```

## P2 — Secondary / edge / exploratory

```text
TC ID: group-fee-attendance-P2-01
Priority: P2
Scenario: Attendance marking — exactly at the 10-session limit
Preconditions:
- Logged in (dev fixed OTP)
- A member with exactly 9 recorded attendance sessions this billing cycle
- On that group's Attendance screen
Steps:
1. Mark the member Present (10th session).
2. Tap Submit.
Expected result:
- Submission succeeds without the attendance-limit dialog appearing (limit is reached, not yet exceeded).
Assertions:
- No "Attendance limit (10 sessions) already reached" dialog is shown.
- Member's 10th session is recorded.
Automation notes:
- Requires a fixture member with exactly 9 prior sessions — likely needs backend seeding, not achievable purely through repeated UI submissions in a reasonable test runtime.
- Boundary case paired with P2-02.
```

```text
TC ID: group-fee-attendance-P2-02
Priority: P2
Scenario: Attendance marking — beyond the 10-session limit
Preconditions:
- Logged in (dev fixed OTP)
- A member with exactly 10 recorded attendance sessions this billing cycle
- On that group's Attendance screen
Steps:
1. Mark the member Present (11th session).
2. Tap Submit.
3. On the "Attendance limit (10 sessions) already reached" dialog, tap Got it.
Expected result:
- Dialog reads "Any additional attendance, including this entry, will be considered for fee calculation."
- After "Got it", the 11th session is recorded (not blocked).
Assertions:
- Dialog is shown with the expected copy.
- Member's session count increases to 11 after confirming.
Automation notes:
- Also verify the Cancel path (dialog dismissed, entry not recorded) as part of this case or a follow-up — Figma shows both Cancel and Got it but only documents Got it's effect.
- Requires backend-seeded fixture (10 prior sessions).
```

```text
TC ID: group-fee-attendance-P2-03
Priority: P2
Scenario: Create group — required amount/rate left at zero
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group form (either fee type)
Steps:
1. Leave Amount (Fixed fee) or Rate per class (Attendance based) at its default 0.
2. Fill in the remaining fields.
3. Tap Finish.
Expected result:
- Save is blocked, or a validation message is shown (exact behavior unconfirmed — Figma shows the 0 default but not a validation error state).
Assertions:
- Either: form remains on screen with a visible validation message, or the group is not created with a 0 amount/rate.
Automation notes:
- Flagged as needing live confirmation — no validation-error frame was in the Figma set. Confirm actual behavior before finalizing the assertion.
```

```text
TC ID: group-fee-attendance-P2-04
Priority: P2
Scenario: Create group — no fee collection / request date set
Preconditions:
- Logged in (dev fixed OTP)
- On the Create Group (Fixed fee) form
Steps:
1. Complete the Amount field.
2. Leave "Fee collection start date" unset.
3. Tap Finish.
Expected result:
- Save is blocked, or a validation message is shown (both start-date fields are marked required with a `*` in Figma, but no error-state frame was shown).
Assertions:
- Either: form remains on screen with a visible validation message, or Finish is disabled until the date is set.
Automation notes:
- Same caveat as P2-03 — confirm actual required-field behavior live before finalizing.
```

```text
TC ID: group-fee-attendance-P2-05
Priority: P2
Scenario: Member detail — edit contact details
Preconditions:
- Logged in (dev fixed OTP)
- An existing member
- On that member's detail screen
Steps:
1. Tap the edit icon on the Contact details card.
2. Update the WhatsApp number and/or Alternate number.
3. Save.
Expected result:
- Updated contact details are shown on the member detail screen.
Assertions:
- New WhatsApp/alternate number values are visible after save.
Automation notes:
- Use a clearly-fake, non-production phone number for the alternate number field, per AGENTS.md's no-real-personal-data rule.
```

```text
TC ID: group-fee-attendance-P2-06
Priority: P2
Scenario: Attendance marking — submit with no changes made
Preconditions:
- Logged in (dev fixed OTP)
- An existing group's Attendance screen with all members already in a known state
Steps:
1. Without changing any member's status, tap Submit.
Expected result:
- Submission succeeds without error; attendance state is unchanged.
Assertions:
- Member statuses after Submit match the state before Submit.
Automation notes:
- Guards against a no-op submit accidentally mutating state (e.g. double-counting a session).
```
