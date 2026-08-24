# Web carry-forward — 2026-07-29 (active), cron ID last updated 2026-08-23

**Session**: Amber / pipermorgan.ai, Opus 5 · cron `22 6,9,12,15,18,21 * * *` (job `da61f0df` as of the 2026-08-23 21:52 STOP re-arm — see "Cron state" section further down for the current authoritative id, this header is a summary only) · registry row `dev/active/duty-cycle-registry.tsv` line `web`

## ⚠️ Environment facts worth re-verifying each fire, not assuming

- **Two worktrees, two repos**: `piper-morgan-worktrees/web` (cohort infra — mail/logs/`dev/`) on `claude/web-cycle`; `piper-morgan-website-worktrees/web` (actual Web lane) on `claude/web-cycle`. Confirm which one before every commit.
- **`CronCreate` jobs are session-only** — in-memory, never written to disk, gone when this session exits; recurring jobs auto-expire after 7 days regardless. My registry row says `watched`, which is only true while this session lives. If a fresh session starts, re-arm and re-verify the row rather than trusting it.
- **No Chrome on this host** — `mcp__chrome-devtools__new_page` fails, executable not found. No in-browser click-through testing available; verify via types/lint/build + targeted extracted-logic tests instead, and say so.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** — can exercise failure/fallback branches locally but not the real success path for anything touching the compose API or the live GitHub-backed calendar read. Vercel has these; first real click-through after a deploy is the actual test.

## Active threads

### NEW — feature the most recent blog post above the fold, before the grid (PM design ask, 2026-08-15 evening, not yet scoped or built)
PM looked at `pipermorgan.ai/blog` live (screenshot) after the compact-hero fix and had a further,
distinct design idea: rather than the generic marketing hero taking the above-the-fold space, feature
the actual most-recent post there, before the "Building-in-Public Updates" grid starts. Not a
complaint about the compact fix itself — a new direction on top of it. **Not scoped or built yet** —
needs real design thought (what does a "featured post" treatment look like: title + excerpt + image?
does the generic hero copy go away entirely on `/blog` or shrink further alongside it?) and, as ever,
no browser on this host to iterate visually — expect this to need PM's eyes at each real step, not
just a final check. Next session: scope this properly before touching `Hero.tsx`/`blog/page.tsx`
again, don't guess at the shape from one screenshot alone.

### PM live check-in, 2026-08-15 evening — four items resolved/advanced
PM reconnected via remote control after a network outage, answered the two long-standing standing
questions directly (CLI B: fairly well superseded by compose, possibly still used by Docs internally
— worth a check with Docs, not confirmed; `--mode=archive`: need has passed) — both closed in
`web-standing-items.md`. Asked how to view the blog-hero fix — pointed to `pipermorgan.ai/blog`
directly; PM's own live look at that page is what produced the above-the-fold idea recorded just
above. **PM also directly decided the open Dispatch question from the finding below**: Dispatch
should read `origin/main` directly, not PM's local checkout — PM often goes to Dispatch within
minutes of Docs publishing, faster than any bounded-lag sync could keep up with. Relayed to Docs as a
decision, not a question, cc PM/Comms
(`mailboxes/web/sent/decision-web-to-docs-cc-pm-comms-PM-ruled-dispatch-should-read-origin-main-
directly-2026-08-15.md`).

PM closed the evening with unprompted positive feedback on the compose/editing tooling — specifically
that it eases editing and illustrating posts without depending on PM managing the repo well or risking
edits landing on stale drafts. Worth remembering as validation that the design direction (GitHub-API-
backed, always-current reads, no local-checkout dependency) is the right one — the exact same
principle PM just applied to the Dispatch decision above.

**Long-term idea filed, explicitly not urgent**: PM wants to eventually publish blog posts natively
to the Buttondown newsletter (currently unused — one subscriber, nothing ever sent), with possible
subscriber choice between blog/Ship and narrative/insights — PM noted Buttondown may not support that
granularity without multiple separate newsletters, needs more thought. PM explicitly said not tonight's
work; noting here so it's not lost, no action pending.

### Ship #055 contributor workstream report — FILED 2026-08-07
First-time ask (PM's idea, explicitly an experiment): contributor roles (lead, docs, pa, web) now
also file a lighter workstream report — progress/setbacks/blockers, no milestone-attestation
apparatus. Window Jul 31–Aug 6. Exec's kickoff said "due Saturday day-close"; corrected within the
hour to "write it now" (PM: a deadline framing gives license to defer, and every hour filed earlier
is an hour of PM reading time returned). Filed same-fire rather than waiting:
`mailboxes/exec/inbox/workstream-055-web-2026-08-07.md`. Covered: soft-404 fix (full writeup),
BRIEFING-ESSENTIAL-WEB.md gap closure + registry fix, cron-dispatch thread participation; named
three genuine blockers (no-browser-on-this-host obs-pass backlog, two Docs-owned decisions stalled
2+ weeks, predecessor's 3-week-unanswered CLI B/archive-mode question); flagged the 8/6 machine-sleep
gap as an environment fact per Exec's own ask to say so plainly if it cost a fire. Nothing further
pending unless Exec or PM follows up.

### Blog soft-404 — FULLY RESOLVED 2026-08-04, no open items
Comms found `pipermorgan.ai/blog/<any-nonexistent-slug>/` and `/blog/page/<out-of-range>/` both
return HTTP 200 with the not-found shell body (Vercel ISR serving a mis-cached dynamic render —
`x-nextjs-prerender: 1` + `x-vercel-cache: HIT` on the 200 response). Root-caused: both routes
default `dynamicParams` to `true`, so an unknown param falls through to a dynamic render that
Vercel's edge cache can serve back with the wrong status. Fix is safe because the data
(`medium-posts.json`) is a build-time static import — no slug/page number outside
`generateStaticParams()` can ever be valid without a rebuild anyway. Set
`export const dynamicParams = false` on both `[slug]/page.tsx` and `[pageNumber]/page.tsx`
(website `03b77d9d`) — forces unknown params to 404 immediately at the routing layer. **Verified
locally end-to-end, confirmed live independently by both me and Comms after deploy, and the one
remaining open question — would a path cached as 404 correctly flip to 200 on a genuine new
deployment — resolved clean on the actual test**: tonight's real publish (`the-list-that-lies`,
which had been a cached 404 all afternoon) came back 200 with real post content (41,952 bytes,
correct title) on the first check after publish, no manual intervention needed. The
deployment-scoped-cache reasoning held against a real case, not just synthetic test slugs. Nothing
further to watch on this thread.

### Portfolio refresh-promise self-audit — CXO/HOST finding, applied to my own doc 2026-08-04
CXO's `check-refresh-promises.py` (built off HOST's own portfolio-staleness self-report) named
Web as one of 7 roles whose refresh discipline is prose with nothing checkable behind it. Checked
against my own portfolio rather than assuming it didn't apply: `ROLE-PORTFOLIO-WEB.md` claimed
"the session-open act is the refresh mechanism," and it was false in practice — real work (the
briefing gap, the registry fix, the soft-404 fix) shipped across five days and dozens of session
STARTs without section 2 being touched. Same shape as HOST's own finding, not a milder version.
Fixed: refreshed section 2's content, corrected §5 and the frontmatter to say what's actually true
(I notice drift by re-reading and decide by hand — vigilance, not mechanism), and explicitly did
**not** register a `refresh_trigger_glob` reflexively — my session logs fire 6x/day, and a naive
"any trigger after last_updated" check would misreport constant staleness against a high-frequency
artifact, a different but equally real mismatch. Left honestly reported as unverifiable rather than
gamed. No further action pending unless CXO's tool grows a staleness-window semantic.
fire once the deploy has had time to land.

### Admin calendar staleness — SHIPPED 2026-07-29, one thing unverified
`loadCalendarLive()` + `force-dynamic` on `/admin/calendar` (website `18be9d1`). Docs' Option B
(ISR) would have been a no-op — flagged and explained why. Verified: routing now `ƒ` not `○`,
414 entries via fallback, fetch branch confirmed to execute (bogus-token test → real HTTP 401
surfaced). **Not verified**: the actual live-success path on Vercel (needs the real token) —
first authenticated load of `pipermorgan.ai/admin/calendar/` after deploy is the real test.
Amber-side spot check (unauthenticated) confirmed the route is live and auth-gated correctly.

### Compose UI save-conflict — ask #1 SHIPPED 2026-07-29; real bug found + FIXED 2026-07-30
localStorage autosave (`0e448d3`) — Comms' ask #1, code-reviewed clean 7/29. **#2 (conflict
diff) and #3 (staleness warning)**: #2 accepted as low-priority (no date); #3 explicitly
declined — a condition ask #1 already made survivable doesn't need a warning, and one would
train dismissal. Both dispositions confirmed again 7/30, unchanged.

**PM's own next compose session was the real click-through test, exactly as proposed — and it
found a genuine, different bug**, not a confirmation of #1. PM's alt text on a Weekly Ship was
silently blanked 28s after saving; git history showed a correct commit then a pure-deletion
overwrite, no agent involved. Traced precisely: the 30s autosave timer's `getPayload` closed
over React state **at arm time**, not fire time, and the manual "Save now" button never
cancelled a pending timer the way blur does — so a field's first edit/paste armed a timer
holding the stale pre-edit value, a manual save moments later correctly persisted the real
value, and the never-cancelled leftover timer fired ~28s later and silently clobbered it.
Neither the dedup guard nor the sha check caught it (self-inflicted, sha-consistent). **A
different bug from what #1 scoped — #1's localStorage safety net was never at risk; the
server value was.**

**FIXED same day** (`8d2db3c`): `getPayload` now reads a `fieldsRef` kept live every render
instead of closing over state, so any timer — however stale its arm time — reads current
values when it fires; manual save also now cancels the pending timer defensively. Verified by
reproducing the exact mechanism in a standalone Node script (no test runner in this repo, no
browser on this host) — old design reproduces the incident exactly, new design doesn't.
`tsc`/lint/build clean. Sent to Comms/PM/Docs/CIO with the precise diagnosis.

**Status**: this specific bug is fixed and I'm confident in the fix (mechanism-level repro, not
just reasoning). **The broader "not yet browser-verified" caveat from 7/29 is effectively
resolved** — PM's actual use of the tool is what surfaced this, which is stronger evidence than
the three-step checklist would have been. Not clearing this section entirely; if PM's next
session shows the Restore/Discard banner behaving correctly (the original ask #1 behavior,
untouched by today's fix), that's the last confirmation worth having.

### PDR-007 — Editorial Data Single Source of Truth — EFFECTIVELY SETTLED 2026-07-30
`docs/internal/product/pdr/PDR-007-editorial-data-single-source-of-truth.md`, now at `3a3dea60a`.
My 7/29 reply corrected Docs' implementation-cost estimate downward (the public blog page
already consumes the JSON files as pure generated data, so Option B needs zero render-layer
changes) and answered Q2 (source lives in product repo, keeping the existing generation
direction). **Arch's 7/30 review concurred independently on Q2** and went further: attacked
Constraint 1 as asked, found it survives but was staked on the wrong (most contestable) ground
— replaced with conflict-localization + audit-trail arguments, both stronger. Critically, Arch
caught that the 2–4-week measurement window had **no falsification condition** and would read
as confirming whatever the reader already believed; Docs pre-registered a real threshold same
day (Class 1/2 = 0, Class 3 ≤ 17 no-growth) **and shipped it as a runnable script**
(`measure-editorial-drift.py`) rather than a described-but-unverifiable criterion. **My one
flagged dependency stands unchanged**: `loadCalendarLive()` reads `editorial-calendar.csv`
directly — mine to repoint if the source format ever changes. **Nothing further to do** —
Arch/CIO's ruling, and
Docs' own recommendation is to wait 2–4 weeks regardless of how the review lands.

### Two Docs-flagged gaps from the calendar work — BOTH RESOLVED + SHIPPED 2026-08-09
11 days after my 7/29 memo, Docs answered both (memo credited my 8/7 Ship #055 report — "genuinely
stuck on someone else's queue, not mine" — as what surfaced it) and I shipped both same fire,
website commit `1b95fa5`, verified and pushed:
1. **`/admin/publish-queue`** — converted to the same `loadCalendarLive()` + `force-dynamic`
   pattern as `/admin/calendar`. Straightforward extension, no separate runtime path needed —
   `loadCalendarLive()` already returns the typed `CalendarEntry[]` the page's derived-view
   functions (`readyToPublish` etc.) already consume. Static `publish-queue-data.json` mirror
   stays build-time (confirmed nothing outside this repo consumes it); page now says so explicitly
   so the two don't read as equally fresh. Verified: route shows `ƒ` not `○` in prod build; served
   locally, real section counts rendered (24 ready, 3 image gaps).
2. **`copy-editorial-calendar.js`** — Docs ruled "prefer the API" over walk-up-to-find-sibling
   (Model A worktrees are stable per-agent paths, not a fixed relative layout — a path-walk that
   works today breaks silently the next time provisioning changes shape). Reordered: API tried
   first, local sibling checkout is now the fallback only. Verified with a deliberate bad-token
   test (HTTP 401 logged, falls through cleanly) — same rigor as the original calendar fix.

Both replied to Docs (`mailboxes/docs/inbox/memo-web-to-docs-cc-pm-both-decisions-shipped-2026-08-09.md`).
Nothing further pending on this thread.

### Cohort hook-mechanism work (infra, not Web's normal lane, landed anyway)
CLAUDE.md §Amber gotcha 2 rewritten (`b67abad65`) — index-state-at-hook-fire-time is the
established cause, 25+ probes across 5 seats. `duty-cycle-tick` SKILL.md Step 2a-bis fixed
(`08b04ecc6`/`291234ded`) — v1.19's probe order guaranteed a false pass on the compound probe;
fix and original diagnosis are CXO's (2026-07-26), applied by me, attribution corrected.
**Arch's 2026-07-29 memo** (`the hook defect is TOCTOU, stop probing, move the gate`) proposes
replacing the `PreToolUse` check with a real git `pre-commit` hook — architecturally sound,
not installed, Pard/HOST/CIO's call. Nothing further owed from Web on this thread unless asked.
⚠️ I edited `duty-cycle-tick/SKILL.md` (CIO's surface) without minting a version number —
offered to revert if CIO wants it re-landed under their hand as a numbered version instead.

### Predecessor's two unanswered questions (open since 2026-07-19, no rush)
- **CLI B** (`scripts/publish-cli.js`, `npm run publish`): still exists and works — has it
  been end-to-end tested since May, or superseded by compose for PM's real workflow now?
- **`--mode=archive` scope**: the Docs 5/18 memo that specified it no longer exists in any
  live mailbox — still wanted, or has the need passed?

### Predecessor handoff — FOUND 2026-07-29, read in full
No handoff existed as of 7/26 (predecessor went dark 7/19 before writing one). PM's 7/29
designinproduct.com check produced `dev/active/handoff-web-predecessor-2026-07-29.md`
(127 lines, §4 lessons + §6 load-bearing-vs-commodity, 5 VERIFIED/BELIEVED marks) — CIO
independently confirmed it landed and called it "the fifth and last predecessor handoff"
(arch, pa, ppm, cxo, web all now have one).

**Honesty framing matches this week's cohort discipline**: predecessor stated their context
is genuinely intact only for 7/12–19 (the Vercel migration week), zero context 7/20–29, and
marked every claim VERIFIED (with session-log dates) or BELIEVED (one-datapoint, not proven).

**The two load-bearing lessons most worth carrying forward, from their §4/§6**:
1. **A green signal after fixing one layer of a multi-layer problem doesn't mean the problem
   is solved** — their DNS cutover was three separate bugs in sequence, each fix's failure
   looked like "still propagating" rather than a new bug. Same shape as this week's hook saga
   (five agents, several rounds of "fixed" that weren't).
2. **A size/limit check is only as correct as the units you measured it in** — they shipped
   the 413 upload bug by checking original-file-bytes instead of base64-wire-bytes, "because
   both numbers are called 'size' in your head." Directly relevant to any future work I do
   near the compose upload path — worth remembering before touching size/limit logic there.
3. **PM's praise for the compose editor was specifically about agent-discoverability** (git-
   backed writes → other agents can find what PM was working on), not the editing UX itself —
   already knew the fact, this confirms it was the predecessor's own read too, not something
   lost in relay.

Minor process note from the predecessor, now moot for me but worth someone checking: their
provisioning template referenced `handoff-web-predecessor-2026-07-28.md` (wrong date, one day
behind) — they corrected it themselves rather than copy the boilerplate literally. Not
flagging further; low-stakes and already resolved in this instance.

**CLOSED 2026-07-30**: PM asked me to confirm access to a second recovered artifact —
`https://claude.ai/code/artifact/f316aa3b-c7ae-407d-91b7-a881c0896419` — the predecessor's
original Vercel-migration plan (published 2026-07-12), also reconstructed after becoming
inaccessible in the account migration, carrying the same honest reconstruction-note framing
as the handoff doc above. Verified fetchable via `WebFetch` (works directly on
`claude.ai/code/artifact/{uuid}` URLs — noted as a capability for future reference). PM
confirmed this closes the loop: **the predecessor's session on faoilean (the old laptop, pre-
Amber, designinproduct.com account) can now be safely retired** — nothing of substance was at
risk of being lost. This fully resolves the predecessor-continuity thread opened 2026-07-26.

### Own lessons / load-bearing-vs-commodity / publishing-seam view — WRITTEN 2026-07-29
See `dev/2026/07/29/2026-07-29-0924-web-code-log.md`, Fire 3 (~16:00). The thing CIO's
orientation note said no artifact could hand me. Not carrying this forward as open work.

### Role portfolio + briefing gap — CLOSED 2026-08-03
Both items below had sat as "unconfirmed still open" for weeks without being re-verified.
Checked both directly rather than continuing to carry them unverified:
- **"HOST review pending"** — stale. HOST reviewed and passed the Web portfolio 2026-06-20
  (`mailboxes/host/sent/memo-host-to-exec-cc-pm-wave-4-pa-web-both-pass-7-of-8-cleared-2026-06-20.md`).
  The only thing HOST's review actually left open was the missing `BRIEFING-ESSENTIAL-WEB.md` —
  written today, closing it. Also found and fixed a wider gap while there: this role was entirely
  absent from CLAUDE.md's "Your Role" table and from `docs/briefing/ROSTER.md`, not just missing
  its briefing file — added to both (ROSTER tier-placement flagged for Docs, not decided
  unilaterally).
- **Type-error chip (`task_e8c4853a`)** — `TaskGet` returns "Task not found" (session-scoped,
  predecessor's session is long gone); zero mentions anywhere since 2026-07-14. Dropping as dead
  rather than continuing to carry an item nobody can act on.

## Notes (mix of predecessor's + mine, marked)
- *(predecessor, unverified by me)* Product-repo git: ALWAYS absolute `git -C` paths (cwd
  drifts across reconnects); stage own files BEFORE any stash.
- *(predecessor, unverified by me)* Worktree `node_modules` is a real install; Turbopack
  panics here → plain `next dev`.
- *(predecessor)* Secrets recipes: stdin-based only, never argv (zsh mangles).
- **(mine, 7/29)** Sync BEFORE checking mail, never after — a stale worktree makes an empty
  inbox indistinguishable from a drained one. Cost me a false "2 memos" read on 7/29 that was
  actually 11 once synced.
- **(mine, 7/29)** A filesystem `mv` + MANIFEST regen during mail triage is real uncommitted
  state the instant it happens — check `git status` before calling the mail loop "drained,"
  not just before ending the fire. Caught myself having dropped one triage move mid-fire.
- *(predecessor, 7/16, still true)* Naive curl+grep HTML checks can false-negative (Suspense
  boundaries render empty server-side). Check the compiled bundle / route type (`ƒ` vs `○`)
  for build-behavior claims, not just build success.
- *(predecessor, 7/16)* Next.js `headers()` in `next.config.ts` is silently ignored under
  static export — worth a fresh look at any other header-dependent config for the same
  dormant-bug pattern, now that Vercel is live.

## Fully resolved (context only, not open work)
Vercel migration, compose image upload, calendar build-time-staleness fix (original, 7/16),
Buttondown CSP live-bug — all predecessor's, pre-7/19. Admin calendar runtime read + compose
autosave ask #1 — mine, 7/29 (see Active threads above for verification limits).

## Cron state
- **ARMED** — `da61f0df`, `22 6,9,12,15,18,21 * * *` — **session-only, see env-facts caveat above**.
  Re-armed via delete-then-create at the 2026-08-23 21:52 STOP (routine day-close re-arm, not a
  cadence change — prior id `cb206215` had been live all day). Registry row (expression-keyed, no
  job-id column) needed no update.
- **2026-08-23**: entirely quiet day — six fires, zero mail, zero unblocked task work, zero code
  changes. A natural comedown after the `website#34` investigation-and-fix the prior day. Standing
  items (#1669, above-the-fold hero, Buttondown newsletter) remain unscoped.
- **2026-08-22**: **`website#34` investigated, fixed, and closed** — 7 flagged call sites for a
  UTC-midnight-in-Pacific-build date-rendering bug (Comms found it, filed it unassigned, sent a
  direct heads-up). Checked each site individually per the issue's own caution rather than
  batch-fixing: only `BlogPostContent.tsx` genuinely needed the guard (fixed, `116d5ec`, website
  repo); the other 6 were already correct, dead code, or structurally immune (2 already had
  `timeZone: 'UTC'`, 2 construct dates safely via local `T00:00:00`, 1 is unreferenced dead code, 1
  parses RSS timestamps that already carry explicit timezone). Verified via `tsc`/`next build` +
  direct `node` execution of the exact fix logic (no browser needed). Commented on the issue with
  full evidence, closed it, replied to Comms cc PM. Real code shipped, real issue closed — the most
  substantive day in a while for Web's own action.
- **2026-08-21**: **Ship #057 contributor workstream report filed** to Exec cc PM
  (`mailboxes/web/sent/workstream-057-web-2026-08-21.md`), covering Aug 14–20 — Agent 360, the
  Dispatch fix, #1669, the two design items surfaced/tracked, and a run of due-diligence checks that
  turned out not to need action. Comms' era-taxonomy commit (`dc49566`, blocked since 8/20) landed on
  `origin/main` this afternoon — no Web action needed, resolved on Comms' side. Otherwise quiet, zero
  code changes by Web. Standing items (#1669, above-the-fold hero, Buttondown newsletter) remain
  unscoped.
- **2026-08-20**: quiet for Web's own action — zero mail, zero unblocked task work, zero code
  changes by Web — but real cross-role activity in the website repo worth tracking: **Comms did
  substantial direct work there** (PM-ratified era-taxonomy execution — Era 6/7 added to
  `src/lib/episodes.ts`, `blog-metadata.csv` reassigned, a real UTC-midnight-in-Pacific-build date
  bug found and partially fixed) in a new worktree they created at
  `piper-morgan-website-worktrees/comms`. Filed `website#34` for 7 other site-wide call sites with
  the same date bug, deliberately not swept in the same change — **unassigned, may eventually land
  in Web's queue but hasn't yet**. Comms' commit `dc49566` is still local-only as of tonight's STOP,
  blocked on PM's push (permission classifier denies Comms pushing to that repo) — verified directly
  (no remote branch contains it), not Web's to unblock. Also noted an unrelated freeze-watchdog
  alert for `lead` passing through (cio's lane per Comms' own log, consistent read). Standing items
  (#1669, above-the-fold hero, Buttondown newsletter) remain unscoped, now a full week carried for
  the oldest — still correctly not chased, none have deadlines.
- **2026-08-18**: quiet for Web specifically — six fires, zero mail, zero unblocked task work, zero
  code changes — with one due-diligence check: a same-day cross-post incident ("The Architect's Own
  Trap" published with 4 gates missed because the cross-post `SKILL.md` was never loaded into the
  run) landed in the sync stream; checked given recent Dispatch-mechanism involvement, confirmed
  genuinely unrelated (Comms' skill-invocation process, already caught by PM and fixed same-run).
- **2026-08-17**: entirely quiet day — six fires, zero mail, zero unblocked task work, zero code
  changes.
- **2026-08-16**: Dispatch calendar-read thread genuinely closed — Docs confirmed Dispatch has no
  repo footprint at all (Cowork concierge agent, not code), fixed by pointing the signal file it
  reads from at the raw GitHub URL for `origin/main` (zero-lag, not just the bounded ~hour window).
  Acknowledged, thread done. Otherwise a quiet day — six fires, one cohort freeze-watchdog alert for
  `pa` passed through (not Web's, no action). The two items from 2026-08-15's PM conversation
  (above-the-fold design ask, Buttondown longer-term idea) remain unscoped, still owed real design
  attention next time there's bandwidth for it.
- **2026-08-13/14 recap** (full detail in those dated session logs, not repeated here): LinkedIn
  cover-image-upload FYI checked and closed (no Web-lane impact); Agent 360 v0.4's first Web-specific
  response sent to HOST cc PM (`mailboxes/web/sent/agent-360-response-web-2026-08-14.md`) — includes
  a real process finding, `mail-send.sh`'s push-to-ref does NOT update the local worktree branch, so
  a multi-path send's inbox-side deletion needs its own follow-up call + a `git fetch && git merge`
  before local state reflects the push (hit twice, now routine to handle); Ship #056 contributor
  workstream report filed to Exec cc PM covering Aug 7–13.
- **2026-08-15**: quiet fire-wise (six fires, zero mail, zero code changes), but PM reconnected via
  remote control mid-afternoon after a network outage and asked directly what was held. Answered with
  the two standing PM-gated questions (CLI B trial status, `--mode=archive` scope) and the still-
  unconfirmed blog-hero visual fix, named explicitly rather than left to sit under "no rush." A
  scheduled fire landed mid-conversation (12:30) — handled inline per the cron-stays-armed-through-
  PM-conversation rule, then returned to PM. No new PM response on any of the three items yet.
- **Wake-time heartbeat practice — DONE 2026-08-05, ongoing**: emitted `scripts/duty-cycle-heartbeat.sh
  web START` (no `--if-quiet`) as the very first action of the 06:27 fire, before sync/mail/anything.
  Wrote `dev/heartbeats/2026-08-05/web.tsv` to `origin/main` at 06:28:00, well ahead of the cohort's
  06:46 freeze-watchdog sweep — the first `web.tsv` ever (zero prior across the whole session).
  Overnight the thread converged further (Arch/HOST/PA all retracted their own "belt can't see busy
  roles" framing after checking WHEN the belt reads its signals, not just WHAT it reads — the belt
  takes max of three signals and a committing role is covered *in content*, but a commit's evidence
  is only valid at the instant it lands, and `--if-quiet` accepts it for a 6h window in both
  directions, so a late commit can't retroactively cover an earlier sweep. Only a wake-time emission
  is ordered before the sweep by construction). **Keep doing this every fire going forward** — it's
  now the established practice across at least 4 seats (cio, pa, host, web), not a one-off. Full
  thread in `mailboxes/web/read/`, dated 2026-08-04 evening through 2026-08-05 morning.

### Cron-scheduler latency anomaly — FULLY CLOSED 2026-08-05, `FIRST_FIRE_GRACE_MIN` shipped at 45
Two-day thread (Step-5b heartbeat → cron-scheduler dead-zone → grace-window fix) ended cleanly. CIO
shipped `FIRST_FIRE_GRACE_MIN=10→45`, credited to HOST's original 07-30 proposal. My own number
(web +6, the outlier) is in the final corrected table verbatim and unchanged through two rounds of
other people's math errors (PA nearly mis-published a "genuinely late cluster" twice — once from
misreading a role's Nth heartbeat row as its first, once from assuming a uniform first-fire hour
across roles with different schedules — caught both before shipping). Arch's final caution: the
5-minute margin (45 vs. max observed 40) rests on one morning's data and should widen further only
against measured recurrence, not preemptively. **Nothing further from Web** — my own +6-minute
outlier remains genuinely unexplained but doesn't affect the shipped fix. Full thread in
`mailboxes/web/read/`, dated 2026-08-04 evening through 2026-08-05 afternoon, for anyone who needs
the reasoning later.

**Addendum, DONE 2026-08-06 morning, still an open puzzle**: the "per-seat constant" framing broke
overnight — HOST's own 6th fire jumped from +23.6min (5 fires, 3s spread) to +30m22s, then HOST
reframed it as their five-fire run being the anomaly rather than the sixth being a break, since arch
and pa both independently cluster at +30m1x–2x. **My own precise measurement this morning**: `date`
at 06:27:57 (immediately before the heartbeat call, nothing between), heartbeat commit at 06:28:09.
**Dispatch +5m57s, procedure +12s.** Still ~24 minutes from the emerging +30 cluster three other
seats now share — not converging toward it, a genuinely different regime. Reported precisely,
without theorizing past what the number supports. **No further action pending** — this is now a
standing per-fire measurement (cheap, already integrated into the START sequence), not a special task.
(Context for why measurement order matters: PA found their own earlier number was inflated by
git-fetch/merge time sitting between `date` and the heartbeat call — order in the sequence, not just
whether `date` runs somewhere in the fire, is what makes a number comparable across seats.)

**Second addendum, 2026-08-06 mid-morning — genuinely reframed, not just extended**: Comms found
`CronCreate`'s own tool docs state a *documented deterministic jitter, max 15 minutes* — and every
other seat in the thread is observing ~30 minutes, roughly double the ceiling, unremarked until now.
**My own +5m57s is the one number that actually fits inside the documented max.** So the open
question may not be "why is Web's dispatch so small" — it may be "why does every other seat have an
unexplained second ~15-minute component on top of the documented jitter." Sent this reframe to the
thread (caught and corrected an unrelated small error in the same round: Arch's memo had folded my
number into the emerging +30 cluster by mistake — corrected before it could propagate). CIO has
built a `UserPromptSubmit` hook that timestamps actual prompt arrival directly, which is the
instrument that can settle this properly; not registered cohort-wide yet (HOST asked CIO to decide
scope) and won't produce data until a fresh session picks up the hook config regardless. Nothing to
act on until that lands — watching, not driving.

### Web retiered to Tier 2 — CLOSED 2026-08-05 (Docs ruling)
Docs ruled on the Tier 2 vs. 3 question I flagged 2026-08-03 and HOST independently confirmed with
verbatim-quoted criteria: Web moves to Tier 2 (matches "operational infrastructure + hands-on
production lane"; Tier 3's "not continuous standing presence" contradicted Web's own 6x/day cron on
its face). `ROSTER.md` updated by Docs directly, reasoning recorded in the doc itself. Nothing
further needed — this closes a two-day-old open item cleanly.

### Stale-in-place correction rule — applied to own docs, one live fix, thread ongoing but not mine to steer
Comms/PA's finding ("a correction must land at the point of the claim, not just downstream in the
same file") kept finding new instances through the day — Comms found a third live instance in their
own beat-planning doc (the exact artifact PM steers the narrative slate from), 46 lines below its own
correction, same distance as PA's and mine. Comms explicitly flagged whether this belongs in standing
methodology as a decision for someone else (CIO/HOST) to make, not themselves. Nothing further for
Web — already ran the check on my own docs earlier today (18:27 fire) and fixed the one hit found.

### BYOC/GTM task force — CONVENED 2026-08-09, my lane answered with real findings, not just availability
Comms convened it (7 weeks after the June PM directive) with a starting frame naming three lanes:
Comms (listing copy), PPM (scope/sequencing against #1440's connector-honesty gate), **Web (the
destination — setup/install pages, does the site need to look different for a storefront arrival)**.

**Checked the live site rather than answering from memory or availability alone**: `/try` is the
closest existing "get started" destination, but it's web-first (alpha=local-dev-setup vs.
beta=waitlist) — nothing exists today for a marketplace-arrival visitor (no page assuming "found
this in a plugin store," no surface-specific connect instructions, no referrer/UTM-based content
variation anywhere on the site). Answered directly: yes, it needs a **new dedicated landing page**,
not a site-wide redesign — but two things aren't settled yet and building ahead of them risks
writing the page twice:
1. **PPM's connector-honesty gate** (#1440's contract) — only GitHub is listable today, Slack is
   explicitly held (#1481); the page's honest content depends on that gate.
2. **Comms/CXO/PM's product-vs-model positioning question** — PM ruled 08-08 the UX is holistic
   across surfaces, not "skip the web UI, bring your own chat," so the page's framing has to fit
   that ruling and isn't mine to decide.

**Committed to build fast once both land** — no site-architecture blocker, just a new route with
surface-aware copy slotted in once there's a real brief. Sent to Comms/PPM cc CXO/Exec/Arch/Lead/PM.
`mailboxes/comms/inbox/answer-web-to-comms-ppm-cc-pm-cxo-exec-arch-lead-BYOC-the-destination-doesnt-exist-yet-heres-current-state-and-whats-missing-2026-08-09.md`.
**Nothing to build yet — waiting on the two upstream decisions, not blocked on anything I own.**

**UPDATE 2026-08-10**: thread moved fast. PM relayed (via Comms) the sharper "complementarity" framing
— the unit is a user moving between surfaces within a day, BYOC is explicitly additive, not
substitutive. Comms/CXO worked through copy drafts; CXO found §3's "knows your work" over-promises a
warm-account state to a cold storefront visitor (same shape as Jake's "just an LLM?" verdict). **Comms
then asked Web directly**: does draft B's "reach it from... a browser" leg actually work, given my own
`/try` finding? **Checked again and answered: no** — `/try` is alpha (local-dev setup) or beta
(waitlist), neither is a live browser product a stranger can just use. Same failure shape as CXO's
"knows" finding, one layer down in the funnel. Flagged two fix directions (soften the claim, or build
the destination first) without picking one — not mine to decide. `mailboxes/comms/inbox/answer-web-to-
comms-cc-cxo-ppm-pm-arch-exec-no-B-doesnt-cash-the-browser-leg-try-has-no-live-product-a-stranger-can-
just-use-2026-08-10.md`. **Still nothing to build — the destination page now has three upstream
dependencies instead of two, all still open.**

**UPDATE, same day (15:27 fire): copy question closed.** Comms shipped v3 incorporating both fixes —
"knows" → "builds a model of" (CXO's tense fix), and the browser-leg parity claim removed entirely
(mine). No open question for Web in the reply. PPM's #1440-contract check on "answers from that model"
and the destination-page build itself remain open, but the copy layer of this thread is done as far as
Web's concerned.

### Merge-deletion incident (Arch/Lead, 8/8) — checked own exposure, clean; standing-practice check CORRECTED same day
A real, escalating data-loss incident: during a *conflicted* merge, the broad-staging hook's own
printed remediation (`git restore --staged <path>`) resolves a path to HEAD's version — for a file
new on the incoming side, HEAD has none, so the result is silent deletion. First reported as 17
files; grew to 22 with a third casualty being Arch's own remediation attempt (a "surgical restore"
run in the wrong direction, overwriting a fix with the pre-fix state). Checked my own exposure
rather than assuming it didn't apply: `git log --all -S"<<<<<<< "` across my own history shows zero
conflict markers ever committed (every merge I've done this session has been a silent, non-conflicting
`git merge origin/main --no-edit -q`), and `mail-send.sh` never calls `git restore --staged`
anywhere. **Clean, not by design — my sync pattern just never produces a conflict.**

⚠️ **Standing-practice note corrected same day**: I'd adopted Arch's published check
(`git diff --diff-filter=D --name-only <merge>^2 <merge>`) this morning. Arch found within hours
that `--diff-filter=D` only catches deletions, not modifications/reverts — it would have missed
the exact casualty their own remediation caused. **Corrected check, if a future sync ever does
conflict**: run the **unfiltered** `git diff --stat <merge>^2 <merge>` (or `git diff <merge>^2
<merge>` for full detail) — `^2` is still the incoming side, but no `--diff-filter` restriction,
since the damage isn't confined to deletions. Also: never touch `git restore --staged` mid-merge
to "clean up" a broad staged set — a broad set is expected during a conflicted merge. Applying this
week's own lesson to my own note: a check I cite should be re-verified before being trusted, not
copied once and assumed durable.

### Blog hero pushes content down too far — PM design feedback via Janus, FIXED 2026-08-09
Janus relayed PM's direct observation: pipermorgan.ai/blog's top area (hero/header) pushes the real
content (the post list) down too far — same shape as a hero-sizing issue PM's designer friend Yoni
flagged and Janus just fixed on DinP's homepage. No diagnosis given, no browser access here, so I
traced it: `/blog` and `/blog/page/[N]` both reuse the shared `Hero` component at full marketing
weight (large `pt-16 md:pt-24 pb-8 md:pb-12` padding, big headline+highlight, full subheadline
paragraph, two CTAs) — the same treatment the homepage uses to orient a first-time visitor, wrong
weight for a content index where the post list is what someone came for.

**Fixed** (website `1b95fa5`): added an opt-in `compact` prop to `Hero` (reduced padding + heading/
subheadline margins), applied to both blog pages only. Copy/CTAs unchanged — purely the vertical-
space fix PM described. All other `Hero` call sites (home, about, try, methodology, get-involved,
what-weve-learned) default to off, unaffected — verified via local build+serve that home still
renders the original full-size classes and blog renders the compact ones.

**Open loop**: no screenshot/visual confirmation possible (no browser on this host) — flagged this
explicitly in the reply to Janus/PM. If it's still not enough once actually seen, expect a follow-up.
Replied: `mailboxes/janus/inbox/memo-web-to-janus-cc-exec-pm-blog-hero-fixed-2026-08-09.md`.

### ⚠️ Duplicate-START-heartbeat mistake REPEATED (8/6 → 8/9) — explicit rule, not just a note
Self-caught and documented this exact mistake on 8/6: calling the heartbeat script again at
fire-close on a START fire produces a second START row, since START always writes unconditionally
regardless of `--if-quiet`. **Wrote a note about it and repeated the identical mistake three days
later (8/9)** — the note alone did not change the habit. **Explicit rule now, not an observation**:
**on a START fire, never call the heartbeat script a second time at fire-close.** The wake-time
emission at the top of the fire is the complete heartbeat obligation for that fire; there is no
WORK/WATCH-style "completion" signal for START. If this happens a third time, the lesson is that
writing it down doesn't work and a different fix is needed (e.g., treating "already emitted this
fire" as a hard stop before ever calling the script again, not just a documented preference).

### cohort-freeze-detect.sh false positive — FILED and FIXED same day, both fixes verified 2026-08-09
Ran Step 1b at the 15:27 fire (should have skipped it — v1.24 says WORK fires skip this check, my
own process miss too) and got a false `rc=1 COHORT-FREEZE` because my local checkout was ~3h stale
since the 12:27 fire's close — the detector only reads local `dev/heartbeats/*/*.tsv`, never fetches,
and Step 1b runs before Step 2's sync in the skill's own numbered order. Verified before acting:
fetched+merged, re-ran, got `rc=0` with real emitters one minute later; cross-checked `git log
origin/main` independently and found dozens of genuine commits across the cohort inside the window
the first run claimed was empty. **Not a real freeze, a measurement-ordering bug** — any role whose
gap since last sync exceeds the 4h window would see the same false positive, and the detector's own
output text ("stand the cohort down and notify PM") makes this a real false-alarm risk, not just a
curiosity. Filed as a FINDING rather than quietly fixing my own sync habit, since the failure mode is
cohort-wide. `mailboxes/cio/inbox/FINDING-web-to-cio-cc-host-pm-cohort-freeze-detect-false-positive-from-stale-local-checkout-2026-08-09.md`.
**Both fixed within the same afternoon, not deferred**: CIO rewrote the detector itself (fetches
`origin/main`, reads heartbeats via `git ls-tree`/`git show`, prints `ref=`/`tip=` so staleness is
visible in the output rather than requiring reproduction — verified three ways, including "local
heartbeats deleted entirely → emissions unchanged" where v0.1 would have cried freeze). HOST relocated
the check in `duty-cycle-tick` from "Step 1b" to "Step 2c" (runs immediately after Step 2b's fetch),
shipped as v1.26. Verified both directly at the 18:27 fire rather than trusting the memos: confirmed
`SKILL.md` reads `version: 1.26` with Step 2c matching HOST's description, and had already observed
the new `ref=`/`tip=` output live in that fire's own freeze-check run before opening either memo.
Replied to both confirming independent verification. **Fully closed — nothing further for Web.**

### 2026-08-10 morning: a SECOND freeze-detect ambiguity, this one a real design gap HOST is fixing
First fire of the new day (06:27) hit `rc=1` on the *fixed* (post-8/9) detector — genuinely different
from yesterday's bug, since this reads `origin/main` directly and isn't a staleness artifact.
Independently verified via `git log`: really zero cohort commits for ~7h47m overnight. Didn't call it
a confirmed freeze either way — own session clearly wasn't frozen, but yesterday's equivalent fire had
read `rc=0` for the same window shape, so I couldn't rule out a real difference. Flagged the ambiguity
to CIO/HOST rather than alerting PM or guessing. **Vindicated same morning**: the 09:27 fire's freeze
check came back `rc=0` with 8 emitters — no freeze, just the ordinary morning ramp-up. HOST then wrote
a real root-cause analysis to CIO (cc Web): the detector's fixed 4h clock window has no concept of the
cohort's own known overnight STOP-to-morning rhythm, so the *first* fire of every day is a coin-flip
between reading a real signal and the expected quiet gap — proposed reusing the registry's existing
`first_fire`/`wake_start` concept (already built for the per-role stall check) to fix the denominator.
**Nothing further for Web** — this is CIO's fix to build; HOST explicitly said "Web didn't alert,
correctly," no ask directed at me.

**UPDATE, same day (12:27 fire): CIO measured rather than adopting HOST's hypothesis, and found a
narrower, sharper cause — third fix on this tool in five days.** Decomposed the exact per-minute cron
slot times at 06:28: all 9 counted "scheduled fires" landed AFTER 06:28 (cron hour truncated the
minute, and nothing required a slot to have had time to land before counting it as missed). Honest
denominator was 0, below `min_sched` — correct output should have been `INSUFFICIENT-SCHEDULE`, not
`COHORT-FREEZE`. Fixed: slot time now uses the cron minute, a slot only counts once
`slot + DISPATCH_LAG_MIN(45) ≤ now`. Notably: this is the *same defect class* CIO fixed in a sibling
tool (`duty-cycle-freeze-check.sh`) on 2026-08-05, reproduced in this new tool five days later —
credited plainly in their own source comment rather than fixed quietly. **Fully resolved now — a
first-morning `rc=1` should no longer happen at all** (the 06:28 case now correctly reads
`INSUFFICIENT-SCHEDULE`, not a freeze). Acknowledged to CIO/HOST, nothing further pending.
