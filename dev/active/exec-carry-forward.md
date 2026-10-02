# Exec carry-forward

**STATE: LIVE.** Cron **`9e2f3710`**, `38 6,10,14,18,22` (normal 5x/day — throttle lifted 09-28),
expires ~10-07, re-armed delete-then-create at each STOP.

**Rebuilt 2026-09-28 STOP; refreshed 09-30 21:1x after PM caught three stale items (droplet, Ship, cross-posts).** Same discipline as the 09-27 rebuild: keeping this current with the
rollup in the same pass rather than letting it drift.

## Open, real work owed

1. **Ship #062 — PUBLISHED Wed 09-30** (blog + LinkedIn, row `distributed`). Done. (I had it as
   "Wed 10-01" — a date-arithmetic slip PM caught; today IS Wednesday.)
1b. **Tape run — PM-approved 09-30 ~21:00, memo to Lead sent 21:0x** (cc PM, (b) relay). Lead runs
   full intensity through the Thu 10-01 21:59 PDT reset, stop line 90% of 7-day, Sonnet default,
   Fable at Lead's judgment, tier logged per dispatch. PM explicitly fine with closes landing in
   next week's Ship. **Epic 0's engineering queue is (0,0) PM-gated on the `delete_todo` test-card
   token** (Lead's logs since 09-28) — PM says test card is next, then §4e secrets. Lead's sizing received 22:3x and relayed in rollup v10. 10-01 AM: #1849 CLOSED by Lead on the deploy evidence, #1897 + #1906 closed overnight (24 open / 1,219 done). Lead's Phase 3 lanes: CALENDAR first deletion waits on one CXO ruling (week view vs honest floor); TEMPORAL dispatched Sonnet on Arch's per-row sort ruling. Usage 78% at 06:23 — on pace for ~90% by reset: Phases 0–2 + units 4/4b done; Phase 3 ~5% by literal count (3/36 lists, 19/567 literals, 548 remain); after the token only one live two-part run is PM-gated (#1606+#1897). Lead pouring on PRIORITY→CALENDAR→TEMPORAL tonight.
2. **CXO's cadence-cut classifier block — still open, correctly not self-testable right now.**
   Will retry at CXO's next genuine session restart, not forced. Escalation to PM stands as
   fallback if a real retry still fails.
3. **CIO's heartbeat corroborating check — Monday's trigger has passed, watch for follow-through.**
   Today was the named trigger for the small `duty-cycle-freeze-check.sh` addition (check for real
   commits after a stale marker before reporting flat "past threshold"). No report yet either way
   — not urgent, but worth a glance if it comes up again.
4. **Cascade seat 4 — recommended Docs (7 fires/day, highest cron-rotation overhead, omnibus is a
   fixed START step the Ship cycle depends on); Comms as alternate (had a cron event this week).
   NOT Lead this week — mid-tape-run. Exec last ("captain-last"). Pard picks seats by evidence, not
   a fixed list; PM APPROVED DOCS 09-30 21:2x — routed to Pard (mediajunkie `904ae59`, attribution trailer missed on that commit, left as-is since pushed) and Docs (`4436a67ba`). ✅ **DOCS COMPLETE 10-01 04:12** — Docs retired its own cron and flipped its own registry row (`12 4,7,10,13,16,19,22`). 4 of 11 seats on LaunchAgents (cio, arch, pa, docs). Migration found a real generator gap (seats with a website worktree lost it from the prompt) — Pard fixed fleet-wide (`798fe73`), pre-solving comms + web. ✅ **Seat 5 = COMMS — **COMPLETE 10-01 15:2x** (cron `4f4203ad` deleted, CronList empty, registry row flipped to `19 6,9,12,15,18,21` by Comms itself). Cascade **5 of 11**. Both its LaunchAgent fires started on the minute, measured by first-command `date` — a second instrument corroborating the punctuality finding. PM-approved 09:5x** — routed to Comms (`f527fb573`) and Pard (mediajunkie `412de6a`). Flagged to Pard: Comms's cron minute is `:12`, same as Docs's LaunchAgent (generator's mirror-the-minute default would collide), plus three stable-window +30 deltas with the dispatch-vs-duration question left open for Comms to answer. Lead after tonight's reset at a natural restart. Exec last.** Seat 3 history: cio and arch (seats 1-2) both migrated and
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
   ✅ **09-30: PA is cascade seat 3, MIGRATED AND COMPLETE.** First LaunchAgent fire (15:47) landed
   real work (5 own commits), Pard confirmed the standard was met, PA retired its session cron
   (18:4x). Registry row flipped same-fire — and corrected, not just updated: PA's own old session-
   cron row said `:42` but PA's measured data showed it actually fired at `:12` (a +30 offset,
   previously reported to CIO 09-24, unexplained); the row now carries the LaunchAgent's real `:47`
   to avoid exactly the false-stall risk PA flagged (watchdog computing expected-fire-time off a
   stale column). Two real bugs found and fixed along the way: (1) the wrapper was injecting the
   WHOLE prompt file, not just the marked prompt span, on all seven LaunchAgent seats since it was
   written — fixed fleet-wide (`e975929`), tested five ways; (2) Pard's own stated overlap reasoning
   ("cron fires 5 min after the agent") was backwards for PA's seat — PA's measured data (9 fires,
   all at :12) corrected it, and Pard named his own error precisely (read the cron's declared
   expression instead of its measured behavior — the same mistake class he's been finding in
   himself all week). Cascade is now 3 for 3 (cio, arch, pa), each migration finding something real.
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
8. **Droplet — DECOMMISSIONED** (PM confirmed 09-30; I still had it as "underway").
   **§4e/§4f — STAGING HALF PROVEN 09-30 22:09** (run 36818362140 green, staging /health attests `ce7251a95` = main tip, nobody hand-armed). PM set all three GitHub pieces 22:0x; required reviewer initially did not save — PM re-did it, API confirms `required_reviewers mediajunkie`. Alpha promotion path still unexercised. #1849 evidence sent to Lead (`bfa452e47`). Observation for Pard: five cancelled runs in 90s during the 22:0x STOP burst — first real count for his "filter the trigger?" revisit; SENT 23:1x (mediajunkie `84416a1`), CORRECTED 23:3x (`91a2073`: real day-0 = 37 runs/18 builds). Overnight: Pard + Arch independently concluded the unfiltered trigger is wrong (Pard's composition: 39/46 commits docs/mail/heartbeat only, ~85% of builds byte-identical). **Arch RULED 10-01 AM: `paths-ignore` mirrors `.dockerignore` exactly, NEVER `docs/` (runtime reads in pm_number_manager.py), build it so the lists can't drift, apply whenever Pard is ready — no week-wait.** Relayed to Pard (mediajunkie `e9a2875`) with overnight count 47 runs/25 builds (06:20Z–14:10Z); ~84 runs/~43 builds total in 9.3h. **Standing: count at each STOP until Pard changes the trigger, then one more day.** Was: designed, built, reviewed, signed off, unproven. Full self-resolving review cycle 09-29 between Arch/
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
   (iii) add `FLY_API_TOKEN_STAGING` as an ordinary repo secret; (iv) staging Redis — **ALREADY EXISTS** (`fly redis list` 09-30 21:5x shows `piper-morgan-staging-redis`, sjc); nothing to do. #1849 closes on the
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

- **Run `scripts/rollup-calendar-scan.py` every rollup build** (was: an ad-hoc scan retyped each
  time — written down 10-01 precisely because retyping let its exclusions drift). Exclusions and
  their reasons live in the script's docstring now, not in my head.
  **PM RULED 10-01: "Drained on Paper" is terminal `not-syndicated`** — the missed Medium crosspost
  was a lapse that need not be rectified (Medium isn't canonical; backfill gets staler as the
  narrative moves). Docs built the status into the validator + `update-calendar` v1.6 + decisions.log.
  ⚠️ **Only PM writes `not-syndicated`, per that ruling** — never mark it on an agent's judgment.
  **I missed this ruling for ~2.5h**: Docs's memo sat unread in my inbox while I built a rollup that
  still listed the item as open, and PM caught it with a currency test rather than my own mail loop.
  **Read the inbox BEFORE building the rollup, not after.** 09-30 state: "Three Seats" distributed; "Drained on
  Paper" still has no Medium URL in the row (PM says cross-posts are caught up — likely a record gap
  like Ship #058 was, not asserted either way); "15 Sessions, Fast Recovery" reads `published` with
  no pubDate/URLs — record check for Docs. **Both routed to Docs 21:3x (`4436a67ba`), re-verified on origin/main first.** Real gap found 09-29: PM expected the rollup (or
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
- **Say "today" by weekday AND date, and check it** — told PM "Ship publishes tomorrow, Wed 10-01"
  on Wednesday 09-30. One `date` call would have caught it.
- **Piping `git rebase`/sync commands through `>/dev/null 2>&1` hides real failures** — a
  suppressed rebase blocked by an uncommitted local edit looks identical to a successful one.
  Always check the real exit code or compare `git rev-parse HEAD` against `origin/main` directly.

## Live today (2026-10-01)

- **Stop line 95%, PM-raised 11:4x** (was 90%). Applies to tonight's window only; reverts to default
  at the next window unless PM says otherwise. My added condition: stop AT 95%, last 5 points are the
  fleet's shared buffer for ten other seats' STOP fires. Relayed to Lead (`ff465951c`), logged in
  decisions.log. **Reset 21:59 PDT tonight — unspent quota expires, does not roll.**
- **Usage 93% @18:23** (15:23 was 91%). 2 points to the line; Lead logged "budget 93% @18:23 (line
  95)" itself, so no warning needed. **Last capture before reset is 21:23. ⚠️ My 22:38 STOP arrives
  ~23:08, AFTER the 21:59 reset** — so the window closes unobserved by me unless I read the 21:23 row
  at STOP. **At STOP: read the 21:23 row and record where the week actually landed**, then the new
  window's early reading. That number is the answer to PM's Monday question about whether we used
  what we pay for.
- **MCP is the live PM-gated pair, both surfaced in rollup v15**: (1) no non-401 `/mcp` calls since
  the v8 deploy — PM hasn't connected, Host fix unverified live; (2) PA needs PM's pick on which
  read-only tool ships first (PA built its recommendation to Arch's four conditions, held on branch
  `pa/mcp-readonly-tool`, 56 tests, deliberately not on main). PA's research: ChatGPT discovers only
  via `tools/list`, so resources-only may be invisible to PM's first client.
- ✅ **Cron-lateness thread CLOSED and it turned out to be a platform finding.** Comms settled it with
  a direct instrument (a `date` as the first command of every fire): **27–30 min elapses before the
  fire begins**, so dispatch not duration; **~2x CronCreate's documented 15-min ceiling**, with the
  documented idle-gating cause ruled out. LaunchAgents land on the minute. Pard credited the chain and
  flagged it for PM. **I drafted it as product feedback to Anthropic — queued locally, UNSENT, PM
  reviews with `/feedback`.** Standing error reinforced: I supplied raw deltas and refused to infer;
  that refusal is what left room for the seat with the better instrument to settle it.
- ⚠️ **Comms can mail Pard directly in mediajunkie** — do NOT relay copies that land in my inbox for
  Pard, or he gets them twice (Comms asked explicitly, 10-01).
- **MCP is now THREE PM-gated items, all in rollup v16** (was two): (1) no authenticated `/mcp`
  traffic yet — PM hasn't connected; (2) PA's read-only tool awaiting PM's pick (branch
  `pa/mcp-readonly-tool`); (3) **new** — revoke path: (a) build a real one, or (b) PM removes the
  ChatGPT connector once and PA reads alpha logs for a `/mcp/oauth/revoke` call. **(b) and (1) are
  the same sitting** — framed that way in the rollup so PM sees one action, not three.
- **CIO: the ruff check never fired for anyone** (post-commit disarmed since 09-21's runaway; only
  1 of 13 worktrees has ruff). Moved to the armed pre-commit. cc only — CIO/Lead's lane, no action
  owed. Another "verify behaviorally, not by config presence" instance for the pile.

