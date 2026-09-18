# Exec carry-forward

**STATE: LIVE.** Cron `d070a7df`, expression `38 6,10,14,18,22`, CronList-verified 2026-09-18 07:1x,
expires ~09-25. Resumed from the cohort standdown on PM's direct instruction.

⚠️ **AMBER RESTART IS IMMINENT — today, possibly early.** PM ruled it a **cold start**, not a resume,
and **Exec goes first as the shakedown cruise** (PM: *"not risk the lead developer's mental model of
what they're working on just yet"*). If you are reading this as a fresh session: that worked, and
**`docs/handoff-exec-2026-09-18.md` is the file written for you** — read it before this one.

## In flight — the thing that breaks if nobody picks it up

**Sprint closeout for Sep 11–17 is OUT; responses are arriving and PM expects a synthesis from me.**
Sent 2026-09-18 to all ten roles. Each leadership role owes ONE primary goal, progress, **on-track as
a yes/no word**, next steps, plus portfolio + contributor updates, ~400 words.

- ✅ **Docs filed** (first in). Standing goal, on track, sprint-truth fresh, `Verified how:` present.
  Flags an unanswered 09-13 routing offer to Lead — two stale audit clusters sitting on nobody.
- ⏳ Nine outstanding. **Five of those roles are deliberately dark** (cio, lead, cxo, ppm, pa) and PM
  is waking them one-on-one. **Their silence is the plan, not non-compliance.** Nudge Sunday 09-20.
- The wake packet they each get on rousing: `mailboxes/exec/sent/wake-exec-to-idle-roles-*-2026-09-18.md`.

## Also live

- **Reboot gate** — `amber-fleet gate` (in the `mediajunkie` repo) is the pre-reboot check. Was
  **0 GREEN / 24 RED** this morning; exec and docs are GREEN now. ⚠️ **Run it FRESH immediately before
  any reboot** — the roster itself moves (`zephyr` appeared within two hours) so a stale count
  under-reports. Handoff filename must match `handoff[-_]{role}([-_.]|$)`; a good doc misnamed reads
  as missing.
- **Memory export** — `dev/2026/09/18/memory-export-2026-09-18-pre-restart.md`, 195 files verbatim,
  integrity-checked. **One shared pool keyed to the git common dir**, not per-role, not per-worktree,
  living in `~/.claude-pm/` outside the repo. First export not tied to a prune. **Open question I
  raised and PM has not ruled on: should this be a cadence rather than an event?** CIO's surface.
- **Weekly reflection proposal is with CIO** (PM-approved to draft, CIO's to ratify) — a section on
  the closeout carrying PM's question verbatim: *"what would I want to know that I might not get from
  the automated processes?"* The design constraint, which matters more than the wording: **it must
  ride an artifact with a live reader.** The 2025 handoff ritual died when its reader disappeared,
  not from laziness — ten months dark, 2025-10-01 → 2026-08-11.
- **Registry rule established today**: anyone may PARK any row; **only the owning session may UN-PARK
  its own**, because only it can CronList-verify. Routed to CIO for the registry header.

## Standing PM-gated items (unchanged by the standdown)

1. ✅ **Ship #060 published** Wednesday 09-16 on overage credits.
2. ✅ **Friday planning happened** 09-18. Outcome: **Fable reserved for Lead Developer; everyone else
   Opus or Sonnet**, plus the standing rule that sub-agent dispatches must set their model explicitly
   rather than inherit. Context for anyone reconstructing the spend: **two independent causes** — the
   dispatch concentration (48 in-window vs 10 in the preceding nine days, all inheriting Fable) AND
   the ceiling dropping ~17% when the summer promotion ended 13 Sept. Neither subsumes the other.
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
