# Exec carry-forward

**STATE: LIVE.** Cron **`07c331ea`**, `37 7,14,21` (THROTTLED 3x/day, PM usage directive since
09-26), expires ~10-04, re-armed delete-then-create at each STOP.

🔴 **Throttle-revert timing: RETRACTED my own "Tuesday" ruling 09-28 14:5x, genuinely unresolved.**
Lead surfaced PM had ALREADY answered this directly to Lead at ~06:5x ("Monday ok") — BEFORE my
08:0x fleet-wide ruling went out, and pointing the opposite direction (Lead read it as "revert
today is fine," acted on it). Retracted fleet-wide, told everyone to hold current state, told Docs
NOT to re-throttle down (their original early revert was right). **Did not guess a third time —
asked PM directly in-conversation this fire.** This is now TWO wrong rulings on the same question
in one day; do not issue a third without PM's explicit words in hand.

**Rebuilt 2026-09-27 START.** The prior version had badly accreted over Saturday — I was updating
the attention rollup in real time as things resolved but not syncing this file in parallel, so it
still read like Saturday morning while everything in it had actually closed. Lesson for myself:
**when a fire resolves something, update BOTH surfaces (rollup AND carry-forward) in the same
pass, not just whichever one the immediate conversation is about.** Full detail on anything below
lives in the 09-25/09-26 session logs, already on `origin/main`.

## Open, real work owed

1. **Ship #062 — ready for Comms's final editorial pass, not yet published.** All 10 workstream
   reviews synthesized, sprint plan PM-approved and distributed, numbers triple-confirmed (91
   closed / 57 filed, corrected from an initial 43/34 `gh`-tooling bug), narrative corrected with
   real day-by-day data. Publish target Wed 10-01 per calendar. Nothing blocking — watch for
   Comms's draft to move to `ready-for-docs`.
2. **CXO's cadence-cut classifier block — still open, correctly not self-testable right now.**
   Blocked twice 09-26 (`[Self-Modification]`); PPM's same class of block cleared in a fresh
   session next morning. CXO's own reasoning, agreed: retrying in THIS same session tests
   nothing (it's the session that already failed twice) — will retry at the next genuine session
   restart, not force one artificially. Escalation to PM stands as fallback if a real fresh retry
   still fails. No exec action pending; watching passively.
3. **CIO's heartbeat corroborating check — deferred to Monday 09-28, named trigger.** Ruling:
   heartbeat stays the sole required liveness signal; a small addition to
   `duty-cycle-freeze-check.sh`'s STALE branch will check for real commits after a stale
   last-invoked marker (exactly this seat's freeze-specific case) before reporting a flat "past
   threshold." Not urgent, not mine to implement — watching for CIO's Monday follow-through.
4. **Docs's Step 1d/1e omnibus fix — adopted 09-26, watch it hold.** First real-use day was
   Saturday; no report yet either way. If Sunday's/Monday's omnibus production looks routine
   (no repeat of the 09-24 lapse), this item closes itself without needing a status check.
5. **Cascade seat 3 — ready, genuinely PM's pacing.** cio and arch (seats 1-2) both migrated and
   stable. Pard's ready for whichever seat comes next whenever PM says so.
6. **MCP Phase C — background tracking only, no exec action.** `mcp.pipermorgan.ai` units 0-2
   live, PM is tester #1 (ChatGPT first), PA driving testing, Lead back on epic 0. OAuth
   authorization server (unit 4) now on the critical path per Arch's fired Q1 trigger.
7. ✅ **LLM-gateway question — CLOSED same-day.** Arch investigated: a real single gateway already
   exists (`services/llm/clients.py`'s `LLMClient`), only 2 files construct a raw provider client
   anywhere in the tree, 11 real call sites (the 113 figure was almost entirely tests/config/non-
   call-site references). No formal architecture review needed — design record written
   (`docs/internal/architecture/current/design-record-llm-client-single-gateway-2026-09-28.md`).
   Replied to Themis directly. Themis separately corrected the cost framing that motivated the
   question: most of the "~$166/mo" is Claude Code Max-seat overage usage (episodic, 3 bursts in
   6 months, not monthly), not metered API — the gateway question stands on its architectural
   merits, its cost urgency was overstated. The real cost lever remains the usage-throttle work
   already in progress. No further exec action.
8. **GitHub API secondary rate-limit — Docs hit it, self-cleared by this fire.** Blocked even
   reads for a window this morning (confirmed real, account-wide, not seat quota exhaustion —
   Docs checked `gh api rate_limit` first). Verified clear on my own seat this fire. No action
   needed unless it recurs.
## Standing PM-gated (long-running, low activity)

- Root cause of the 09-25 undetachable-HEAD/silent-ff-merge git anomaly — still unexplained,
  one-off so far, not worth chasing unless it recurs.
- Weekly reflection proposal with CIO — needs an artifact with a live reader, not yet built.
- Memory export cadence — open question with CIO: event-triggered or scheduled.

## This seat's standing errors (deduplicated, keep watching)

- **Update the rollup AND carry-forward in the same pass, not one then the other** — this file's
  own 09-27 rebuild is the direct evidence: real-time rollup updates all Saturday, zero
  carry-forward syncs, resulting in a file that read like Saturday morning at Sunday START.
- **A hard reset discards tracked-file edits, not just a poisoned index** — cost four casualties
  in one incident (09-25/26): carry-forward, registry, a session-log STOP section, and the
  heartbeat last-invoked marker. When describing "queued disk work" during any future freeze,
  name explicitly which files are untracked (survive) vs tracked-with-local-mods (do not) — and
  do a full sweep of every touched file immediately at recovery, don't wait for other roles'
  mechanisms to find the casualties one at a time.
- **Never trust a failed loop's silence as "nothing happened"** — verify per-recipient via the
  actual log/ls-tree, not by re-running the loop and assuming a clean pass means catch-up.
- **Mail-send needs BOTH inbox source and read destination in one call** — verify with
  `git ls-tree origin/main`, never trust exit code alone.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`, written via manual file + commit there, verified via `git log origin/main -1` in *that*
  repo. Same convention for Janus's DinP inbox.
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **A worktree you synced earlier this session is not synced now** — re-fetch before answering
  any state question, not just at scheduled fires.
