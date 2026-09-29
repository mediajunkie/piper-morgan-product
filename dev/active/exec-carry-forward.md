# Exec carry-forward

**STATE: LIVE.** Cron **`da786353`**, `38 6,10,14,18,22` (normal 5x/day — throttle lifted 09-28),
expires ~10-05, re-armed delete-then-create at each STOP.

**Rebuilt 2026-09-28 STOP.** Same discipline as the 09-27 rebuild: keeping this current with the
rollup in the same pass rather than letting it drift.

## Open, real work owed

1. **Ship #062 — fully queued, nothing blocking.** Comms + Docs closed two review rounds (metrics
   triple-confirmed 91/57, an art-embed bug found and fixed), marked publish-ready. On the
   calendar for Wed 10-01. Just watch for the actual publish.
2. **CXO's cadence-cut classifier block — still open, correctly not self-testable right now.**
   Will retry at CXO's next genuine session restart, not forced. Escalation to PM stands as
   fallback if a real retry still fails.
3. **CIO's heartbeat corroborating check — Monday's trigger has passed, watch for follow-through.**
   Today was the named trigger for the small `duty-cycle-freeze-check.sh` addition (check for real
   commits after a stale marker before reporting flat "past threshold"). No report yet either way
   — not urgent, but worth a glance if it comes up again.
4. **Cascade seat 3 — ready, genuinely PM's pacing.** cio and arch (seats 1-2) both migrated and
   stable. **09-29 correction to yesterday's account**: Pard checked CIO's own claim (restore had
   no named trigger) against the actual fire logs and it doesn't hold — the LaunchAgent was
   re-armed 3 minutes after restart and fired all 3 times during the "29h wait." Real cause: the
   wrapper's auto-Enter accepted an `auto-mode-setup` dialog CIO's 16:07 fire hit, wedging the
   session for two more fires; a `select`-widget probe reporting `ok=0` was misread as advisory
   rather than a real stuck-signal. Fixed on Pard's side (Enter withheld from dialogs, `ok=0`
   treated as failure) — detection now ~2h instead of 27h. CIO's `parked:`-state observation
   stands as generally correct but didn't apply here (the actual disarm was only 4 minutes).
   Relayed the correction to CIO/Docs/PM (Pard's original memo reached only my inbox despite
   being addressed to all four).
5. **MCP Phase C — background tracking only, no exec action.** `mcp.pipermorgan.ai` units 0-2
   live, PM is tester #1 (ChatGPT first), PA driving testing, Lead back on epic 0.
6. **Decision-model trial (Jev/Laya) — HELD until post-MVP, PM's ruling.** CIO's network-research-
   hub first finding: worth one narrow trial (PM intent classification only, local, no vendor
   access) but explicitly not agent triage or health gates. Lead offered to run it; PM held it so
   it doesn't pull Lead off epic 0. CIO re-raises after MVP ships. No action now.
7. **Usage snapshot — genuinely healthy, one build gap worth a nudge.** pipermorgan.ai 51% / 7-day,
   designinproduct.com 55% / 7-day, both resetting in 2-3 days (09-28 reading). The visualization
   page Janus built on 09-24 (`/internal/usage/`) was never actually populated by Pard — still
   shows "Chart pending." Not urgent; worth a nudge to Pard next time there's a natural opening.

## Resolved today (09-28), kept brief

- **Throttle directive fully closed**, after real churn: my own "through Monday" wording split
  the fleet 3 ways; I ruled once wrong ("Tuesday"), retracted same-day when Lead surfaced PM had
  already answered directly ("Monday ok" = revert today); PM confirmed; fleet back to normal
  cadence. New durable memory saved on naming exact trigger events, not vague day references.
- **LLM-gateway question closed same-day** — a real single gateway already exists
  (`services/llm/clients.py`, 11 call sites not 113), no formal review needed, design record
  written. Themis corrected the cost framing that motivated it (mostly Max-seat overage, not
  metered API).
- **GitHub API secondary rate-limit** — Docs hit it, self-cleared, verified clear on my own seat.
- **CIO's 29h silence** — root-caused (restart-handoff gap, not a discipline lapse), both findings
  relayed to Pard.

## Standing PM-gated (long-running, low activity)

- Root cause of the 09-25 undetachable-HEAD/silent-ff-merge git anomaly — still unexplained,
  one-off so far, not worth chasing unless it recurs.
- Weekly reflection proposal with CIO — needs an artifact with a live reader, not yet built.
- Memory export cadence — open question with CIO: event-triggered or scheduled.

## This seat's standing errors (deduplicated, keep watching)

- **Update the rollup AND carry-forward in the same pass, not one then the other.**
- **A hard reset discards tracked-file edits, not just a poisoned index** — cost four casualties
  in one incident (09-25/26). Do a full sweep of every touched file immediately at recovery.
- **Never trust a failed loop's silence as "nothing happened"** — verify per-recipient via the
  actual log/ls-tree.
- **Mail-send needs BOTH inbox source and read destination in one call** — verify with
  `git ls-tree origin/main`, never trust exit code alone.
- **`mailboxes/pard/` is HARD-REFUSED** — Pard's real inbox is `~/Development/mediajunkie/docs/
  mail/`. Same convention for Janus's DinP inbox.
- **`echo` after `||` asserts nothing** — always re-read `origin/main`.
- **A worktree you synced earlier this session is not synced now** — re-fetch before answering
  any state question, not just at scheduled fires.
- **Never rule on an ambiguous fleet-wide directive without checking whether PM already answered
  it directly somewhere you can't see** — cost two wrong rulings in one day (09-28). If a ruling
  reverses a role's own already-taken action, that's a signal to ask before broadcasting, not
  after.
- **Piping `git rebase`/sync commands through `>/dev/null 2>&1` hides real failures** — a
  suppressed rebase blocked by an uncommitted local edit looks identical to a successful one.
  Always check the real exit code or compare `git rev-parse HEAD` against `origin/main` directly.
