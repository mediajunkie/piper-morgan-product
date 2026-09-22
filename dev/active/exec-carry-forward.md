# Exec carry-forward

**STATE: LIVE, day closed 2026-09-20.** Cron **`c4d9399e`**, `38 6,10,14,18,22`, delete-then-create
at STOP, CronList-verified exactly one, expires ~09-27.
⚠️ **Offset is per-job and re-rolls on every create** — this seat has seen +31, +30, +7, +13, +14.
**Use the documented bound (slot + up to 15 min), never a remembered figure.**

## ✅ The reboot mechanism — RESOLVED by Pard, primary evidence (11:2x)

**CORRECTS this section's own prior framing.** What I wrote this morning ("crons survive a reboot,
n=4, mechanism unknown") was wrong in exactly the way Pard's memo warns about. Pard's account, from
`sysctl kern.boottime` (Sun 09-20 18:38:39) and `ps lstart` on all 25 claude processes (every one
started 18:50:31–18:57, none existed 18:38:39–18:50): **the reboot reached every seat.** What
survived is the SESSION TRANSCRIPT — `claude --resume <uuid>` restored the conversation, and the
cron job recorded inside it came back with it. Job-id continuity is consistent with a reboot
happening, not evidence against one. **"The reboot never reached this seat" is retracted** — six
seats (including me) wrote some version of that sentence and it was quoted as fact before being
checked against primary evidence.

**Why this matters more than the semantics**: Pard's own point — *"a seat that believes no reboot
happened will not go looking for what it lost."* Model tier and permission mode did NOT come back
with the resumed transcript. This is very likely the actual mechanism behind Janus's separate
finding that arch/cxo/web/Janus/Themis resumed on Sonnet 5 instead of Opus 5 — not a deliberate
switch, an artifact of what `--resume` does and doesn't restore.

## Where things stand

## Where things stand

✅ **JANNE'S INVITE — HOLD LIFTED** by HOST, 22:4x. Lead's full driven flow on alpha met the bar;
HOST verified independently (checked #1824 open, confirmed quoted log lines are verbatim real code at
named file:line) before ruling. **PM is free to send it.**

✅ **FLY MIGRATION — RULED, no longer pinned.** PM tonight, in-conversation, recorded in
`decisions.log`: *"the real question is just when and how... not whether."* Decided 2026-07-10,
reaffirmed repeatedly since. Lead proposes **execution tomorrow (Tue 09-22) morning**, ~half-day,
short write-freeze on alpha — full step table in
`mailboxes/exec/read/2026-09-21-lead-hosting-ruling-recorded-migration-execution.md`. **Correction to
Arch's plan**: droplet has 6 users (one registered TODAY — Janne) and is now the real source of
truth; Fly is stale (4 users frozen since 07-13). Step 2 is a real data migration, not a no-op.
**One thing to confirm with PM**: the migration itself is ruled, but I don't have explicit
confirmation PM has said "go" on *tomorrow morning specifically* — item 3 (DNS cut + OAuth callback)
is PM-owned and time-boxed. Flagged to PM directly, not assuming silence is approval.

## Owed by me

1. ★ **MONDAY 10:00 — usage reassessment.** PM's test: closer to 50% than 33% = converging.
   ⚠️ **Do NOT bring a commit estimate** — commits understate conversational load. **PM holds the only
   real number; interpret theirs.**
2. **Answer PA's question** on the calibration shape for the usage-correlation model. **Mine, not PM's.**
3. **Ship #061** — PM close-reads Mon/Tue; **Comms reviews before Wed 09-23 publish**; PM gates that
   handoff.

## This seat's standing errors

- **Verify the artifact the instrument reads**, not the one you edited (`sync-pm-local.sh`).
- **`echo` after `||` asserts nothing** — re-read `origin/main`.
- **Don't write a decision brief on another role's surface without them reading it first.** Four now:
  scope-guard options, the credential mechanism, Vercel retention, and the Fly framing Arch improved.
- **Nine consistent observations is what makes a confound invisible.** Repeatability felt like validity.
- **A request with a deadline inside my own fire gap cannot arrive on time** (Pard's B3, 09-20).
- 🔴 **A park without a computed deadline is not falsifiable.** I parked 11 rows naming who may clear
  them and what to verify, but never *when it should have happened*. The watchdog caught it in two
  hours. **Preregistration §5 predicted it.**

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
