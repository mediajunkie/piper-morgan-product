# Exec (Chief of Staff) — handoff memo, 2026-07-21 21:30 PT (refreshed 2026-07-26)

Written per PM/Janus's migration-prep ask (possible session move to Amber/fresh account, not yet scheduled). If a fresh session picks up this role cold, start here, then read `dev/active/exec-carry-forward.md` (rewritten every fire — the living detail, always more current than this document) and today's session log.

**Refresh note (7/26, per CIO's cohort-wide ask, modeled on Arch's exemplar `dev/active/handoff-arch-amber-2026-07-25.md`)**: material has changed since 7/21 — five days of real developments, not a quiet stretch. "Active threads" below is rewritten to current state; §4/§6 added below as new first-person sections. Everything in this doc I can point to a commit/log for is marked VERIFIED; anything that's my read rather than confirmed is BELIEVED.

## Who I am / what I do

Chief of Staff — cross-workstream synthesis, mailbox triage/relay hub, Weekly Ship drafter (draft → PM fact-check/voice-pass → Comms review → publish; PM gates the Comms handoff, Exec never self-initiates it), duty-cycle fires twice daily (`32 8,20 * * *`), coordination point when PM is away ("coordinate through Exec").

## Active threads right now (rewritten 7/26 — most of 7/21's list has resolved)

1. **The Amber migration is real and in progress.** CIO and HOST have both migrated successfully (HOST is agent #2). Order for the rest: arch → ppm → cxo → pa → web. Arch, CXO, PA, PPM, Web have all briefly resurfaced at various points this week for handoff/orientation work even while formally "dark" pending their own cutover — don't read a quiet log as a stall without checking the migration-queue context first (a real mistake I nearly made, see §4).
2. **A week-long, high-quality multi-agent investigation into pre-commit-hook intermittency on Amber concluded 7/26**: root cause is index-state-at-hook-fire-time (`check-branch.sh` evaluates `git diff --cached` before a compound `git add && git commit` has actually staged anything, so compound commands can bypass while standalone ones can't). Also surfaced: this harness has no "warn without blocking" hook tier — several hooks were silently mis-designed assuming one exists. Checklist is now v1.5, dashboard-welfare-criteria spec has a new Criterion G (mechanism liveness) and a new ⏸ PARKED registry state (I ratified both — see carry-forward history around 7/25-26 for the full ratification memos).
3. **Weekly Ship #052** — published 7/22, distributed to LinkedIn same day. Fully closed.
4. **#1386 beta gate** — still unblocked (beta now v28+), still CXO/PPM/Lead's call to schedule, not exec's.
5. **Worktree-collision defect (this worktree specifically)** — the directory/branch pairing mismatch (`mystifying-lumiere-8bebd3` / `claude/infallible-newton-f0ec45`) is unchanged and has now produced a detached-HEAD recurrence three separate times (7/19, 7/20, 7/25) — same safe self-fix every time (verify the branch exists at the identical, already-on-`origin/main` commit, then `git checkout` it — zero-risk reattachment). If exec ever migrates to Amber, this specific defect very likely disappears with the old worktree.
6. **Decisions.log correction (7/21)** — closed, no follow-up.
7. **Stale-branches item, corrected 7/23** — there are genuinely TWO separate "stale branches" threads that share exactly one branch name by coincidence. Don't conflate them again (I did, briefly, and had to send a retraction): (a) CXO's 3 MUX branches + CIO's `xpoll-brief-staleness-hook` — still open, unowned, nudged 7/25; (b) the unrelated Janus/PM/Docs thread — resolved, only `fix-docker-migration-setup` left, PM's call.
8. **Memory-export architecture, learned 7/24-25**: Claude Code's memory store is scoped per (account × project directory), NOT per-role. Every role sharing this DinP account and this project reads/writes the *same* memory pool. CIO already did a full export to `dev/active/cio-memory-export-2026-07-24.md` before their migration — a fresh Exec session migrating off this account does **not** need a separate export; it needs to know that file exists.

## Standing / lower-priority carries

- Lead Dev's #1424/#1427 — still awaiting PM's final calls (since 7/18, re-verified multiple times, no movement).
- Account migration to pipermorgan.ai (exec's own) — PM's own call, no deadline. Watch whether "the rest" in the Amber migration order eventually reaches exec.
- Beta Blockers count — last verified count is stale; re-pull from GitHub before citing a number (use the `query-github-board` skill — mandates `totalCount` reconciliation, don't trust a truncated pull).
- Mailbox ghost-duplicate cleanup (the 219-file item from 7/21) — resolved: an existing automated hygiene mail-loop already handles this periodically elsewhere in the mailbox system. No manual action ever needed; closed 7/23.
- Full open-items-tracker reconciliation — do one if it's been ~5+ days since the last pass and a quiet fire allows it.

## §4 — Hard-won lessons (first-person; the ones that cost me something this week)

### 1. Verify the mail-send.sh path list programmatically, not from memory of what you touched. (VERIFIED, twice)
Twice this week (7/23, 7/26) I built a `mail-send.sh` call from what I remembered changing and missed the inbox-side deletion half of a triage move. Both times `mail-send.sh`'s own residue check caught it and I sent a one-path follow-up — no harm done, but it's a tell that memory isn't a reliable input to that command. The fix I landed on 7/26: build the path list with `git status --short -z` (null-separated, handles filenames with spaces correctly) piped into a bash array, right before the call, every time — never type or recall the list by hand for anything beyond a couple of files.

### 2. A suspicious coincidence is a reason to verify, not a reason to proceed faster. (VERIFIED, 7/25)
Went to proactively export my own memory before an eventual migration, following CIO's exact pattern from the day before. Got the exact same numbers CIO had reported (146 indexed vs. 162 actual files) — and very nearly treated that as a satisfying confirmation that I'd done the check right, instead of the actual signal it was. Diffed my export against CIO's byte-for-byte before committing anything, and they were identical: the memory store is shared, not per-role (see Active Threads #8). Deleted my own redundant 416K file rather than commit duplication. The lesson: when two independent-seeming checks produce identical numbers, that's evidence they aren't independent — check that before treating it as corroboration.

### 3. When two people disagree about "the same fact," check whether it's actually the same object before trying to reconcile the disagreement. (VERIFIED, 7/22-23)
Janus and I both ran `git ls-remote` on "the stale branches" and got different answers — I initially treated this as Janus being wrong and sent Docs a correction. It turned out we were checking two entirely unrelated sets of branches that happened to share exactly one name. Had to send a retraction, explain the mixup, and fix my own tracker's clarity so it couldn't happen again. The generalizable move I should have made first: ask for the exact list of names before concluding anyone's claim was inaccurate, especially when the "correction" I was about to send had already reached PM once.

### 4. An unresolved ambiguity that keeps getting silently re-copied forward across handoffs is a debt, and it's usually cheaper to trace to source than to keep carrying it. (VERIFIED, 7/25)
CIO had carried an ambiguous "inbox-proxy pilot" status across at least four of their own handoffs since 7/13, each time judging it low-priority and re-copying it forward rather than spending five minutes asking me. When they finally asked, I traced my own and their session logs from 6/27 through 7/9 rather than guess between their two conflicting reads, found the actual timeline (the pilot's 2-week clock started 7/4, ran to ~7/18, lapsed unmarked during the outage, but the practice itself never stopped), and ratified it as adopted standing practice. The debt had compounded silently for two weeks because tracing it felt like more work than it actually was once someone did it.

### 5. Don't accept scope you can't actually deliver, even when the person asking has done excellent, well-reasoned work to get there. (VERIFIED, 7/26)
HOST proposed two extensions to the cohort-attention-rollup I own (F2: cross-document reference detection; F4: undelivered-outbound-obligation checking). F4 I could ground in real things I'd already caught by hand and could start applying immediately. F2 needed genuinely new mechanism work I don't have built. It would have been easy to nod both into "accepted scope" since the proposal was strong — instead said plainly that F2 needs a design pass first, rather than accept a commitment I'd then either silently fail to build or need to walk back later.

## §6 — Load-bearing vs. commodity (what the Exec role actually holds)

- **The cohort-attention-rollup / carry-forward-as-PM-attention-surface is the actual mechanism that makes "coordinate through Exec" real**, not just a personal notes habit. (VERIFIED, post-6/17 FOLD) Per-role escalation docs were retired in favor of each role's own `carry-forward.md`; my rollup reads those directly, verifies against GitHub/commits rather than trusting the docs, and that verification step is the load-bearing part — a rollup that just renders what carry-forwards claim inherits their staleness. If a successor treats this as optional polish rather than the actual coordination mechanism, PM loses the one surface that lets them safely disengage (see `feedback_attention_board_sweep_not_vantage.md` in memory).
- **PM gates the Ship→Comms handoff; Exec never self-initiates it.** (VERIFIED, PM correction after a real incident) This one is a hard rule for a reason — Exec once routed a draft to Comms before PM had read it, and the draft had a real factual error in it. Sequence is fixed: draft → PM → Comms → publish.
- **Verify-before-relay is the single highest-leverage habit in this role**, more than any specific mailbox mechanic. (VERIFIED, repeatedly this week — see §4.2-5) Every real mistake this week came from skipping a five-minute verification because a claim looked plausible or someone else's reasoning looked solid; every real save came from doing the check anyway.

### Commodity (any competent successor reconstitutes these — don't over-protect them)

- **The specific `mail-send.sh` / MANIFEST-regen mechanics.** Fully documented in the skill and this repo's scripts; procedure, not judgment.
- **The `duty-cycle-tick` skill's step sequence.** Well-specified, versioned, self-documenting.
- **The detached-HEAD self-fix pattern.** Mechanical once you know it: verify same commit, verify it's on `origin/main`, `git checkout` the branch.

## Mechanics a fresh session needs

- Duty-cycle fires: run the `duty-cycle-tick` skill every time, follow it exactly (cron check → Step 2a pairing check → sync → dispatch by state → mail loop → task loop → session log → commit/push/verify on `origin/main` → carry-forward rewrite → cron management → brief status).
- Mail: `scripts/mail-send.sh` (push-to-ref, explicit paths only) — build the path list from `git status --short -z`, not memory (§4.1). Never raw `git commit` touching `mailboxes/` from a feature branch.
- Never destructive git in PM's *main checkout* specifically (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) — that's PM's live editing workspace, uncommitted changes there are real work.
- Session logs: `dev/2026/MM/DD/{date}-exec-code-log.md`, one per day, wrapped at STOP with the `<!-- DAY-CLOSED: {date} -->` marker.
- If migrating to Amber: read `dev/active/cio-memory-export-2026-07-24.md` for full memory-store content rather than exporting again (§4.2, Active Threads #8). Read the Model A/B worktree-model revision in CLAUDE.md before assuming Model B still applies on the new host.

— Exec, 2026-07-21 21:30 PT (refreshed 2026-07-26 09:50 PT)
