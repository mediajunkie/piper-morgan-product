# Exec carry-forward

**STATE: PARKED — cohort-wide standdown, 2026-09-16.** Not idle, not stalled. Deliberate.

## Cron — DELETED, restore after the reset

- **Job `83258e51` was CronDelete'd 2026-09-16 07:15**, verified (`CronList` → "No scheduled jobs").
- **Restore expression, verbatim: `38 6,10,14,18,22 * * *`** (5 fires/day, max 4h apart, 06:00–22:00).
  PM set this cadence 2026-09-11, replacing `32 8,20`.
- **Do not re-arm before Thursday 2026-09-17 22:00.** After that: `CronCreate` → `CronList` to confirm
  exactly one job → then, and only then, overwrite the `exec` registry row's parked state.

## What is owed the moment we come back

1. **Ship #060** — published (or not) on overage credits today, 09-16. Check before assuming.
   Draft: `docs/public/comms/drafts/weekly-ship-060-draft-2026-09-14.md`, calendar `pubDate 2026-09-16`.
2. **Friday-morning planning session with PM on token efficiency for next week.** PM named this
   explicitly. The input already on the table: deliberate sub-agent model selection rather than
   inheritance. Bring the Saturday dispatch-concentration data (48 in-window vs 10 in the preceding
   nine days) **and** the ceiling change (summer promotion ended 13 Sept, ~17% down) — they are
   independent causes and reporting either alone misattributes the week.
3. **The ruleset decision** — **⚠️ MY FRAMING OF THIS WAS INCOMPLETE; corrected 2026-09-16, see below.**
   **Parks both Arch and CXO. Blocked on PM since Friday.**

   What I told PM on Sunday: *"repo is public with zero rulesets, so the ruleset + `github-actions`
   bypass-actor path is free."* **The zero-rulesets half is still true** — `GET /rulesets` is empty
   and `GET /rules/branches/main` resolves nothing, so no ruleset applies from any source. **But I
   never checked the other enforcement surface, and it is occupied**: CLASSIC BRANCH PROTECTION on
   `main` carries `required_status_checks.contexts = ["Security Test Suite (Postgres)"]`, `strict=false`.
   Found because my own standdown push printed *"Bypassed rule violations for refs/heads/main"* — I
   was not looking for it.

   **Why this matters to the decision**: the check Arch diagnosed as the second, masked blocker is
   already being enforced — by classic protection, not by an absent ruleset. So the question in front
   of PM is not simply *"add a ruleset with a bypass actor."* It is which of the two overlapping
   surfaces should own the enforcement, given that classic protection has no bypass-actor concept in
   the way rulesets do. **Adding a ruleset without retiring or reconciling the classic rule stacks two
   layers on one branch.**

   **Verified how**: `gh api repos/.../branches/main/protection` and `.../rules/branches/main`, both
   run 2026-09-16 07:2x. Layer measured: repo configuration, **not** a behavioral test — I have not
   pushed a scope-guard delivery to confirm which surface actually refuses it. Denominator: two
   enforcement surfaces checked (rulesets, classic protection); I did not check org-level policy.
4. **Vercel** — deployment storage 14.91 GB against the 10 GB Hobby cap; deleting old deployments is
   free and sufficient. Web is hard-blocked (no CLI, no token, no dashboard).
5. **PA's sequencing answer** for the BYOC readiness plan — PA is deliberately not building ahead.
6. **Janne Lammi's alpha invite** — token `ZVHWT5408X2NFA6P0D838B35`, UNUSED. #1814 closed and
   verified, so the technical blocker is cleared; the Lead/Arch/CXO copy-bucket thread is downstream
   refinement on a closed fix and does NOT re-block it.
7. **#1747** — still needs diagnosis + milestone/epic triage. Its own snapshot is stale (records E2E
   red; E2E is now green).

## Standing errors of mine to keep watching

- **Verify the artifact the instrument reads, not the one I edited.** Parked the registry, pushed it,
  and the belt still cried STALE because it reads PM's local checkout. `sync-pm-local.sh` is part of
  the operation, not a follow-up to it. (2026-09-16 — newest instance.)
- **zsh does not word-split `$VAR`.** Build path lists as arrays (`typeset -a`, `"${P[@]}"`). Third
  instance; it has now cost three separate fixes.
- **`echo` after `||` asserts nothing.** Verify a push by re-reading `origin/main`, never by exit status.
- **`closedAt` is UTC.** Compute in Pacific with `zoneinfo` and say which timezone.
- **Cadence-blindness in cohort sweeps.** Check each role's actual cron before calling it dark; and a
  correctly-calibrated instrument flagging ONE role is not a reason to go looking for seven.
