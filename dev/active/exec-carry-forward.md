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
   being addressed to all four). ✅ **CIO accepted in full, own records corrected** (registry,
   probe hook header, standing items, carry-forward, dated corrections on the 09-27/28 logs — not
   rewritten). CIO named its own two errors precisely (wrong-layer probe claim, PM's own direct
   account outweighed by its own instrument when it shouldn't have been). Loop fully closed.
   **09-30: PA is now cascade seat 3** — LaunchAgent armed (`com.xian.pm-pa-cycle`, :47, 6x/day),
   PA's session cron stays armed until Pard confirms an OBSERVED fire landing work (double-fire
   window during overlap is deliberate). **Do NOT update PA's registry row yet** — Pard will say
   when. PA was picked third for a measured reason (their cron already died once this morning at
   the Opus 5.5 restart, exactly the failure class the LaunchAgent removes).
5. **MCP Phase C — background tracking only, no exec action.** `mcp.pipermorgan.ai` units 0-2
   live, PM is tester #1 (ChatGPT first), PA driving testing, Lead back on epic 0.
6. **Decision-model trial (Jev/Laya) — HELD until post-MVP, PM's ruling.** CIO's network-research-
   hub first finding: worth one narrow trial (PM intent classification only, local, no vendor
   access) but explicitly not agent triage or health gates. Lead offered to run it; PM held it so
   it doesn't pull Lead off epic 0. CIO re-raises after MVP ships. No action now.
7. **Usage snapshot — genuinely healthy, one build gap worth a nudge.** pipermorgan.ai 55% / 7-day,
   designinproduct.com 58% / 7-day (09-29 06:23 reading), both resetting in 2-3 days — normal daily
   growth, nowhere near crisis pace. The visualization page Janus built on 09-24
   (`/internal/usage/`) was never actually populated by Pard — still shows "Chart pending." Not
   urgent; worth a nudge to Pard next time there's a natural opening.
8. **Droplet decommission — underway 09-29, PM's own hands.** Gate met (Fly served v145-151
   clean, one-week window past). Lead finishes their half same-fire once confirmed.
   **§4e/§4f (CI auto-deploy to staging → alpha promotion) — designed, built, reviewed, signed
   off, still UNPROVEN (nothing has run).** Full self-resolving review cycle 09-29 between Arch/
   Pard/Lead, all inside this repo's mailboxes (Pard can write directly here even though
   `mailboxes/pard/` can't receive — useful to know for future threads). Arch reviewed Pard's
   build, found one real blocker (parity gate called with no ref, always exit 2) + 2 smaller
   issues; Pard reproduced the blocker himself before fixing it (didn't take Arch's word), fixed
   all 3, pushed; Arch re-reviewed the diff (not the memo) and signed off, naming one residual
   race that fails loud rather than silently — accepted as-is. Design: alpha promotes staging's
   *exact* image (no rebuild), two separate tokens (not one shared), parity checked on the
   promotion step. Trigger fires on every push to main (mail/docs commits included) — deliberately
   NOT filtered, because filtering would let staging's attested sha silently drift from main's
   real tip, undermining the whole point; Pard's own preference, revisit-with-a-real-count named
   as the trigger for reconsidering (one week after the token exists).
   **PM's action list, exact order, when ready (not urgent — nothing runs until this exists)**:
   (i) create GitHub environment `alpha` with a required reviewer + branch restricted to `main`;
   (ii) add `FLY_API_TOKEN_ALPHA` **inside that environment**, never as a repo secret (a repo
   secret makes the whole guarantee false while the workflow file still reads as though it holds);
   (iii) add `FLY_API_TOKEN_STAGING` as an ordinary repo secret; (iv) create staging Redis
   (`fly redis create --name piper-morgan-staging-redis --region sjc --no-replicas`, answer N —
   gates the promotion check specifically, not the staging deploy itself). #1849 closes on the
   first untouched staging deploy once (iii) lands.

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

## New standing rollup check, adopted 09-29 — already vindicated same day

- **Scan `docs/internal/planning/comms/editorial-calendar.csv` for `status=published` rows with no
  cross-post recorded, every rollup build.** Real gap found 09-29: PM expected the rollup (or
  Janus) to surface a blog sitting published-but-not-distributed, needing PM's manual crosspost —
  neither did, because I never checked the calendar at all. Applied immediately, found 2 older
  inconsistent rows, routed to Docs rather than guess. **Docs's resolution, same evening**: Ship
  #058 was a pure record-keeping gap (the crosspost happened 09-02, just never logged — fixed).
  **"Drained on Paper" is a genuinely real, ~7-week-old unsyndicated post** — already on record in
  #1683 since a 08-30 platform audit, sat unchased since. Docs named it plainly as their own miss
  and flagged PM directly. Exactly the shape this new check exists to keep catching — one clean
  validation on day one. Keeping the check alongside Docs's own direct-reminder practice, not
  either/or.

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
