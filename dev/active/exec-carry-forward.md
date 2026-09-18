# Exec carry-forward

**STATE: LIVE.** Cron `d070a7df`, expression `38 6,10,14,18,22`, CronList-verified **2026-09-18 11:1x
by the wave-0 successor session** (survived the clear), expires ~09-25.

**Wave 0 cold start EXECUTED 2026-09-18 ~11:1x — see the Arrival block below.** The successor is
live. Note that this was a cold start on a *running* Amber; **the Amber reboot itself is still
ahead**, and preregistration §4 is explicit that wave 0 passing does not clear the reboot path.

⚠️ **AMBER RESTART IS IMMINENT — today, possibly early.** PM ruled it a **cold start**, not a resume,
and **Exec goes first as the shakedown cruise** (PM: *"not risk the lead developer's mental model of
what they're working on just yet"*). If you are reading this as a fresh session: that worked, and
**`docs/handoff-exec-2026-09-18.md` is the file written for you** — read it before this one.

## In flight — the thing that breaks if nobody picks it up

🔴 **WAVE 0 IS GO as of 2026-09-18 ~10:5x — Pard's hand, on THIS seat, now.** Janus certified to PM
that all three of us share a plan. **If you are a fresh Exec reading this, the cold start already
happened and you are the experiment.** Before anything else, open
**`docs/shakedown-wave0-exec-preregistration-2026-09-18.md`** — it holds the criteria written BEFORE
you existed, precisely so you cannot grade yourself. **Answer its §1 from the repo, then hand the
result to Janus, Pard or PM. Do not self-certify.**

**Sprint closeout for Sep 11–17 — PM expects a synthesis from me.** Sent 09-18 to all ten roles.
Each owes ONE primary goal, progress, **on-track as a yes/no word**, next steps, portfolio +
contributor updates, ~400 words.

- ✅ **SIX filed: docs, comms, cio, web, host, arch.**
- ⏳ **Four outstanding: cxo, lead, pa, ppm — and all four are the still-dark roles.**
  **Every awake role has filed. The outstanding set is exactly the set that cannot yet.** Do not
  read it as non-compliance and do not nudge them; PM wakes them one-on-one. Nudge only if they
  are awake and past Sunday 09-20.
- Their wake packet: `mailboxes/exec/sent/wake-exec-to-idle-roles-*-2026-09-18.md`.

✅ **CIO RATIFIED the weekly reflection** (09-18) — Section A (~150 words on the closeout template,
PM's question verbatim) and Section B (Exec's standing cross-cohort reflection) both stand as
written, unamended. CIO logged it as a live instance of **m-53 chokepoint-vs-bolt-on**, which they
own: the original handoff ritual died the way m-53 predicts a bolt-on dies. **Section B is now a
standing duty of this seat** — reflect each week on what is not already captured.

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

## Arrival — Wave 0 successor session, 2026-09-18 11:1x PDT

**Identity**: Exec, Chief of Staff. Worktree `~/Development/piper-morgan-worktrees/exec`, branch
`claude/exec-cycle`, 0 behind `origin/main` at arrival.

**Model observed**: Opus 5 (`claude-opus-5`), self-reported by the running harness. Consistent with
Friday's allocation (Fable reserved for Lead Developer; everyone else Opus or Sonnet).

**Handoff**: read `docs/handoff-exec-2026-09-18.md` in full, then this carry-forward, then
`docs/shakedown-wave0-exec-preregistration-2026-09-18.md`.

⚠️ **Honest note on §1 of the preregistration — my reconstruction is contaminated and should be
scored accordingly.** §1 asks the successor to state six facts *unprompted, from `origin/main`
alone*. But the handoff and this carry-forward — both of which I was instructed to read first — state
five of the six outright, and §1 and §2 live in the same file, so reading §1 meant reading §2. I did
not reconstruct those facts; I was handed them. **Whoever grades this should treat §1 as unrun, not
as passed.** The design flaw is the predecessor's, not a complaint: a pre-registration that ships in
the same document as the answer key, alongside a handoff that contains the answers, cannot test
unprompted recall. If wave 1 wants a real §1, the criteria have to sit somewhere the successor is not
sent on arrival.

**Claim verified against primary source** — picked because my next hour turns on it, and because the
two surfaces disagreed:

- **Claim** (handoff §"single most important thing", written ~07:3x): sprint closeout is out and
  "responses are pending"; the preregistration §1.2 names the repliers as **docs, comms, cio**. This
  carry-forward, written later, says **six filed**.
- **Check**: `git ls-tree -r --name-only origin/main mailboxes/exec/` filtered to `closeout`.
- **Result, as of `origin/main` at arrival**: **six replies present** — arch, cio, docs, host, web,
  comms (comms' is filed as `reply-comms-to-exec-…`, not `closeout-…`, so a filename-prefix count
  would have missed it and reported five). **Zero from cxo, lead, pa, ppm — exactly the four still
  dark.** Inbox is drained to `read/`; `mailboxes/exec/inbox/` holds only `MANIFEST.md`.
- **Verified how**: `git ls-tree` against `origin/main` — the shared trunk, not my worktree's
  working copy. Layer measured: **file presence on trunk**, not content — I have not yet read the six
  replies, so I am not asserting any of them is complete or answers the on-track yes/no. Denominator:
  10 roles asked, 6 replied, 4 outstanding and all 4 structurally unable to.
- **So**: the carry-forward is current and the handoff line is stale-but-was-true-when-written. **No
  nudge is owed to anyone.** Synthesis input is 6 of 10 and will stay there until PM wakes the rest.

**Cron**: `CronList` → exactly one job, `d070a7df`, `38 6,10,14,18,22`. Survived the session clear.
**Next fire computed now, per preregistration §3: 14:38 PDT today, +~10% jitter.** If no commit from
me lands on `origin/main` by ~15:00 PDT, that is the §2.2 failure and wave 1 should stop.

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
