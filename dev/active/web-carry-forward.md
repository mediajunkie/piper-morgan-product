# Web carry-forward — 2026-08-29 (active), cron ID last updated 2026-08-29

**Session**: Amber / pipermorgan.ai, Opus 5 · cron `22 6,9,12,15,18,21 * * *` (job `a9631fd9`) · registry row `dev/active/duty-cycle-registry.tsv` line `web`

⚠️ **Trimmed 2026-08-29** — everything this file carried from 2026-08-03 through 2026-08-25 was
fully-resolved historical record (marked CLOSED/FIXED/SHIPPED/SETTLED at the time), sitting in
what's supposed to be ephemeral session state well past its own events. Compressed to one-line
pointers below (same principle `web-standing-items.md` already applies to its own "Recently
completed" section — point forward, not back). Full detail for anything referenced is in the dated
session logs (`dev/2026/MM/DD/`) and git history if ever needed again.

## ⭐ Web is the browser-automation pilot (since 2026-08-28) — "no browser on this host" no longer true

PM blessed headless Playwright on Amber (via Pard/Exec); Exec assigned Web as the pilot role.
Smoke-tested same night (08-28): `npx playwright` works, Chromium cached, launched headless,
navigated the live site, got a real title/DOM measurement/screenshot on the first attempt. Full
detail: `dev/2026/08/28/2026-08-28-0652-web-code-log.md`, STOP section.

**First real design use, 08-29**: shipped the above-the-fold blog redesign (website `b21d89e`) —
replaced the generic marketing `<Hero>` on `/blog` with the pre-existing, previously-unwired
`organisms/FeaturedPost` component (extended with a `compact` prop), populated with the actual
most recent post. Verified with a real Playwright screenshot against a local prod build, directly
compared to the 08-28 "before" baseline: post-grid section now visible at y=688 in an 800px
viewport, vs. barely peeking in before. Full diff and evidence:
`dev/2026/08/29/2026-08-29-0652-web-code-log.md`.

**Tool report (per Exec's ask)**: genuinely unblocked this fix — no way to confirm the visual
claim otherwise, which is exactly how the 08-09 partial `compact` fix shipped without catching
that the real problem was still there. No false starts (yesterday's smoke test worked out the
launch pattern already). Reported to Exec cc PM 08-29
(`mailboxes/web/sent/report-web-to-exec-cc-pm-browser-automation-pilot-first-result-2026-08-29.md`).
Open thread, not blocking: configuration is still ad-hoc (`npx playwright` invoked per-script)
rather than a settled per-repo config — worth deciding a permanent shape eventually. PM hasn't
seen the live result yet — worth an eyeball pass next time PM is on `pipermorgan.ai/blog`, but
this ships as shipped-pending-PM-reaction, not shipped-pending-PM-approval.

## ⚠️ Environment facts worth re-verifying each fire, not assuming

- **Two worktrees, two repos**: `piper-morgan-worktrees/web` (cohort infra — mail/logs/`dev/`) on `claude/web-cycle`; `piper-morgan-website-worktrees/web` (actual Web lane) on `claude/web-cycle`. Both share the basename `web` — disambiguate via `git remote -v`, not just `basename "$(pwd)"`. Confirm which one before every commit.
- **`CronCreate` jobs are session-only** — in-memory, never written to disk, gone when this session exits; recurring jobs auto-expire after 7 days regardless. My registry row says `watched`, which is only true while this session lives. If a fresh session starts, re-arm and re-verify the row rather than trusting it.
- **`mcp__chrome-devtools__new_page` still fails** (no Chrome DevTools MCP executable), but this is
  no longer "no browser on this host" — headless Playwright via `npx playwright` works fine
  (smoke-tested 08-28, used for real design verification 08-29). Use Playwright directly, not the
  Chrome DevTools MCP tools, until/unless that gap is separately closed.
- **`scripts/duty-cycle-heartbeat.sh` takes `<role>` as `$1`, not a flag** — `--help` alone is
  parsed as the role name and writes+auto-pushes a garbage heartbeat file rather than showing
  usage (hit and cleaned up 08-29, commit `7779a4d79`). Correct form:
  `scripts/duty-cycle-heartbeat.sh web work --if-quiet`.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** — can exercise failure/fallback branches locally but not the real success path for anything touching the compose API or the live GitHub-backed calendar read. Vercel has these; first real click-through after a deploy is the actual test.
- **No login credentials for the Piper Morgan product app's shared dev server** (PID 67615, port
  8001) — no self-serve `/register` (pruned per #1504), no documented test account. Anything
  needing an authenticated view of the app (todos, settings, etc.) is blocked for Playwright
  verification until either a test account or an isolated seeded instance gets provisioned. Pre-auth
  flows (login redirects, public pages) are unaffected — those verify fine. Found 08-29 during the
  In Review round; see Active threads above.

## Active threads

### CLOSED — In Review browser-verification round (2026-08-29)
Exec routed 4 app-layer In Review items (#1512, #1568, #1480, #1578/#1581 SECURITY) as a follow-on
to the pilot — full arc across 3 fires:

1. Code-verified all four; **#1480 fully live-verified with no login needed** (redirect chain +
   executed the real deployed guard logic) — **CLOSED by Lead**, who named the served-vs-source
   byte-diff and real-extracted-function-execution approach as worth defaulting to going forward.
2. Credential gap (no test account existed) reported rather than worked around — Lead provisioned
   a dedicated browser-lane account through the real signup path (not DB-injected).
3. **Live-DOM pass done with the credential**: logged in through the real `/login` page, drove
   `/todos` and `/files` via Playwright (real form fills/selects/uploads, not API shortcuts) —
   **#1512** (priority-high chip renders correctly after real dialog submission), **#1568** (real
   edit → save → server-persisted, confirmed via follow-up GET), **#1578/#1581** (hostile
   title/filename render as escaped inert text in the live DOM, zero script execution — third
   verification layer after static read + independent jest re-run). Full report:
   `mailboxes/web/sent/report-web-to-lead-cc-exec-pm-live-DOM-pass-complete-all-four-verified-2026-08-29.md`.

**Incidental finding, filed not fixed**: `/api/v1/files/list` has no `owner_id` field, so files.html's
"Uploaded by:" renders blank (escaping is correct, it's a data-contract gap) — **#1697**, low
priority.

**Status, confirmed 21:52 fire**: all four issues (#1512, #1568, #1578, #1581) closed by Lead on my
evidence (`gh issue view` confirms all CLOSED). The pilot's full arc — smoke test → first shipped
fix → first blocked-and-honestly-reported credential gap → provisioned credential → full live-DOM
pass → four real issues closed — ran clean start to finish. Nothing further for Web on this round.

### CLOSED — predecessor's two long-standing questions
Both (CLI B trial status, `--mode=archive` scope) were answered by PM 2026-08-15 and closed in
`web-standing-items.md` — no longer carried here.

Otherwise nothing open right now — standing items (`web-standing-items.md`) are all either
PM-gated (obs-pass joint walkthrough, site walkthrough) or genuinely unscoped/no-rush (#1669
hero-image filename drift, Buttondown native newsletter).

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
- **(mine, 8/15)** PM's design direction preference, stated directly: GitHub-API-backed,
  always-current reads with no local-checkout dependency (the compose editor's shape) is the
  right pattern — praised unprompted specifically because it doesn't depend on PM managing the
  repo well or risk edits landing on stale drafts. Apply this bias when a new admin/tooling
  surface needs a read strategy.
- **(mine, 8/15)** Cross-project reads (e.g. Dispatch) should hit `origin/main` directly, not
  a bounded-lag mirror or PM's local checkout — PM's own usage pattern (checking Dispatch within
  minutes of a publish) is faster than any sync window. PM ruling, relayed to Docs as a decision.

## Fully resolved / historical (compressed 2026-08-29, was ~500 lines of daily detail)
Everything below was genuinely closed at the time; kept as one-line pointers only in case a topic
resurfaces. Dated session logs and git history have full reasoning if needed.

- **Cron/freeze-detector fixes (08-04→08-10)**: `FIRST_FIRE_GRACE_MIN` scheduler-latency fix;
  `cohort-freeze-detect.sh` false positive from stale local checkout (fixed, `ref=`/`tip=` added);
  a second freeze-detect ambiguity (`INSUFFICIENT-SCHEDULE` vs `COHORT-FREEZE` denominator bug,
  fixed by CIO). All CIO/HOST-owned fixes, verified live by Web, nothing further owed.
- **Web retiered Tier 3 → Tier 2** in `ROSTER.md` — Docs ruling, 08-05.
- **Blog hero compact-padding fix** (website `1b95fa5`, 08-09) — superseded by the full
  above-the-fold redesign above; this was the partial fix that motivated it.
- **Admin calendar + publish-queue staleness fixes** (website `18be9d1`, `1b95fa5`) — moved from
  build-time to request-time reads. Shipped, verified.
- **Compose UI**: localStorage autosave (Comms' ask #1, 07-29) + a real closure-timing data-loss
  bug found from PM's own use and fixed same-day (`8d2db3c`, 07-30) — stale-closure timer
  clobbering a manual save. Fixed, mechanism-reproduced, verified.
- **PDR-007 (editorial data single source of truth)** — effectively settled 07-30, Web's one
  flagged dependency (`loadCalendarLive()` reads the CSV directly) unchanged since.
- **Blog soft-404 fix** (`dynamicParams = false`, website `03b77d9d`, 08-04/05) — verified live
  including on a real publish.
- **`website#34`** (UTC-midnight-in-Pacific-build date bug, 08-22) and **`website#35`/`website#36`**
  (compose remount data-loss + canonical-URL SEO fix, 08-25) — both investigated, fixed, closed
  with evidence. `website#36` also produced the cross-project mail protocol (Dispatch-PM finding,
  ratified by Exec 08-25) — Web independently confirmed `~/Development/dispatch/` is writable on
  Amber and surfaced it proactively.
- **BYOC/GTM task force** (convened 08-09 by Comms) — Web's lane (the destination page) answered
  twice with real findings (`/try` isn't a live product a stranger can use); nothing to build yet,
  blocked on two upstream decisions not owned by Web.
- **Merge-deletion incident exposure check** (Arch/Lead's 08-08 finding) — checked own git history,
  clean by construction (sync pattern never produces a conflict); corrected a stale `--diff-filter`
  check same day.
- **Predecessor-continuity thread** — handoff doc + Vercel-migration plan artifact both found,
  read, verified fetchable; predecessor's old pre-Amber session confirmed safe to retire, 07-30.
- **Ship contributor workstream reports** filed for #055 (08-07), #056 (08-14), #057 (08-21) —
  routine, no open items.
- Several entirely-quiet-fire days (08-11, 08-13, 08-17, 08-18, 08-20, 08-23/24, 08-26) — zero
  mail, zero unblocked work, standing items correctly left unchased (none have deadlines).
