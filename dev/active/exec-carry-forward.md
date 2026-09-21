# Exec carry-forward

🔴 **STATE: PARKED FOR THE AMBER REBOOT, 2026-09-20 ~18:30.** Cron `0f219adf` (`38 6,10,14,18,22`)
**will be DEAD when you read this** — a reboot kills every cron, unlike `/clear` which preserves them.

## FIRST THREE THINGS, in order

1. **`CronList`.** If zero jobs, **`CronCreate` `38 6,10,14,18,22 * * *` immediately**, then
   `CronList` again to confirm exactly one.
2. **Un-park ONLY the `exec` row** in `dev/active/duty-cycle-registry.tsv` — after step 1 verifies,
   never before. **Do not un-park any other seat's row**; each owns its own. All 11 were parked by
   this seat at 18:1x per Pard's runsheet B3.
3. **`scripts/sync-pm-local.sh`.** The freeze-watchdog reads PM's local checkout, not `origin`. A
   push alone does not change what the instrument sees. This is this seat's recorded trap.

⚠️ **Your arrival offset is UNKNOWN and will differ from before.** The offset is **per-job** and
**re-rolls whenever a cron is created** — confirmed across three jobs (+31, +30, +7). **Use the
documented bound: slot + up to 15 minutes.** Do not use any pre-reboot empirical figure; that error
is mine, retracted 09-20, and Janus amended the runsheet over it.

## What was in flight when the lights went out

📌 **PINNED UNTIL RESOLVED, per PM: complete the Fly migration.** With **Arch**. The droplet is
**unfinished migration, not architecture** — a full Fly cutover was decided 07-10 and executed 07-12;
alpha never followed. Also recorded: *"the droplet has no python-keyring backend"* (#1382), which
forced an encrypted-DB fallback. **Zero active users makes this the cheapest it will ever be, and
that window closes when the first tester logs in.** Costs (PM's figures): droplet $24/mo, Fly $10–16.
**PM has de-escalated the money angle — the value is one surface, not savings.**

**Janne's invite: STILL HELD.** HOST ruled 09-20 that **deploy health ≠ the observed-BYOC-flow bar**
they have now held three times. Alpha is current (**v0.8.12.0**, deployed 09-20, verified
in-container). What's needed is a **real BYOC flow driven on alpha** — a user's stored key read and
used on a substantive query. Lead has asked HOST to mint a throwaway token for it; HOST replied
splitting the ask. **Not PM's to do.**

**Owed by me:**
- **MONDAY 10:00 — usage reassessment with PM.** Their test: closer to 50% than to 33% means
  converging. ⚠️ **Do NOT bring a commit-count estimate** — commits understate conversational load.
  **PM holds the only real number; interpret theirs.**
- **Ship #061** — drafted (`dev/active/weekly-ship-061-draft-2026-09-19.md`), PM close-reads Mon/Tue,
  **Comms reviews before Wed 09-23 publish**, PM gates that handoff.
- **PA is tasked** with a real usage-correlation model, prior art first.

**PM is on non-Piper work** and explicitly not waiting on anything. **Do not push at them.**

## This seat's standing errors

- **Verify the artifact the instrument reads**, not the one you edited (`sync-pm-local.sh`).
- **`echo` after `||` asserts nothing** — re-read `origin/main`.
- **Don't write a decision brief on another role's surface without them reading it first.** Three
  instances: scope-guard options, the credential mechanism, the Vercel retention advice.
- **Nine consistent observations is what makes a confound invisible.** Repeatability felt like
  validity; the variable I failed to control for was myself.
- **A request with a deadline inside my own fire gap cannot arrive on time.** Pard's B3 landed 15:48
  for a ~17:15 deadline; my next fire was 18:38. **PM's prompt is the only reason it happened.**

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
2. ✅ **Friday planning happened** 09-18. ⚠️ **CORRECTED 2026-09-19 by PM — the handoff's framing
   ("Fable reserved for Lead; everyone else Opus or Sonnet") is a DISTORTION this seat repeated three
   times.** Model allocation is **a judgment practice, not a policy with an exception**: PM is
   *currently providing* Lead with Fable (and the live point was that **Fable 5.1 lands once the
   machine and software are updated**); the rest *"tend to be"* Sonnet or Opus by a per-workload
   judgment about who is doing heavier planning, **sometimes settled in discussion with the agent
   itself.** PM: *"It's not a perfect science at all."* **Never cite a model allocation as policy** —
   ask PM or the seat. Full entry in `decisions.log` 09-19. The one durable rule from that day stands:
   sub-agent dispatches must set their model explicitly rather than inherit. Context for anyone reconstructing the spend: **two independent causes** — the
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
5. ✅ **PA's BYOC sequencing — ANSWERED by PM 2026-09-15** (proceed in parallel with MVP; conditions:
   don't distract Lead, nothing merges that risks MVP). PA's closeout confirms it and reports the goal
   ON TRACK. ⚠️ **I carried this as a live blocker until 15:1x today** — PM ruled it in conversation and
   it is in none of the three surfaces the re-verify rule checks. See the conversational-ruling hole above.
6. **Janne Lammi's alpha invite** — token `ZVHWT5408X2NFA6P0D838B35`, UNUSED. #1814 closed and
   verified, so the technical blocker is cleared; the Lead/Arch/CXO copy-bucket thread is downstream
   refinement on a closed fix and does NOT re-block it.
7. ✅ **#1747 CLOSED 2026-09-19 by Lead** — epic-1 lane complete, belt green 10/10, #1687 closed with it. The standing-red finding it recorded is genuinely resolved, not re-scoped. Stop carrying it.

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
