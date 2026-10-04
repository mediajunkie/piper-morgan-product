# Web carry-forward — 2026-10-03 (active, day closed)

**2026-10-03 — first full LaunchAgent day, quiet.** Six fires on `:18`, all drained. Stale
`cron=22` prompt constant flagged to Pard at 06:18, fixed and confirmed 09:18. **New standing
routing rule (Exec, 17:28 broadcast, PM ruling): never write to `mailboxes/xian (ceo)/`; no cc or
`to:` PM; anything needing PM goes to `exec` with the reason (decision / relayed ruling / would-
contradict) in the subject.** Sprint goal for the week ending 10-08 is Lead's epic 0 Phase 3
deletions — not on Web's critical path. Web is on Sonnet 5.5. Item 3b still held for PM review (any
nudge goes via Exec).

**Spring-cleaned 2026-09-22** per context-floor plan item 4a. Current state only — full narrative
for anything below lives in the dated session log, not here.

**⭐ MECHANISM CHANGE 2026-10-02 — Web is now on a LaunchAgent, NOT session-scoped `CronCreate`.**
Pard armed `com.xian.pm-web-cycle` (cascade seat 8), firing at `:18` past 06/09/12/15/18/21. First
observable fire was 21:18 same day, confirmed landing real work. Per Pard's two-step instruction,
both done: session cron `769a37e2` retired (`CronDelete` + `CronList` → "No scheduled jobs."),
registry row flipped `22 6,9,12,15,18,21` → `18 6,9,12,15,18,21`, Pard/Exec told directly. **Going
forward**: `CronList` returning "No scheduled jobs" is now NORMAL and EXPECTED, not Gap-C — per the
duty-cycle-tick skill's own "Cron mechanism gate," skip all session-cron management content (no more
delete-then-create at STOP, no re-arming, no job-id tracking). My own liveness is Pard's LaunchAgent
infrastructure to monitor now, not mine to self-check via `CronList`.

**Session**: Amber / pipermorgan.ai, **Sonnet 5**. Registry row `dev/active/duty-cycle-registry.tsv`
line `web` (now reads `18 6,9,12,15,18,21`, `first_fire` `06:18`).

**2026-10-02 — newsletter-CTA resolved, stopgap shipped.** PM answered live: two-step plan —
(1) be honest about what's live today, (2) design a real preference-based signup later. Step 1
shipped same-day: `/blog`'s CTA no longer solicits emails into the dormant Buttondown list; it now
links directly to the real LinkedIn newsletter (`linkedin.com/newsletters/building-piper-morgan-...`,
PM-provided) and Medium (`medium.com/building-piper-morgan`), with a generalized "800+" figure
across both. Shipped website `4b6cf04`, verified via live dev-server render (computed styles,
correct hrefs, zero "576" text) after a screenshot capture itself timed out. Live-production
deploy check was in progress as of this write — confirm on next read if not already resolved.
**Step 2** (preference-based signup across blog/Weekly-Ship/beta-waitlist) recorded as
`web-standing-items.md` item 3b — genuinely needs a planning pass, not started.

**2026-10-01 — fully quiet day.** Six fires, all drained (0,0).

**2026-09-29 — substantive day.** Closed website issue **#1905**: two posts silently missing from
the Eras browse, backfilled (`cluster` empty → `the-alpha`/`the-mechanism`), and root-caused —
`publish-post.js` now derives `cluster` from `--work-date` against `episodes.ts`'s `ERAS` when
`--cluster` is omitted (fail-loud, never silently empty), superseding a 2026-05-16 design note
whose premise the 09-06 backfill had already invalidated. Shipped website `e2baf72`. Caught a
CSV-reformatting near-miss (Python's `csv` module silently rewrote line endings) before it shipped
— see `feedback_csv_edit_by_name_never_position`-shaped lesson in the dated log. Otherwise a quiet
day; full account in `dev/2026/09/29/...`.

**2026-09-25/26/27/28 — fully resolved, historical only** (real-world gap, fleet-wide
commit-attribution incident, a fully quiet day, the throttle-revert saga). Full accounts in their
dated session logs. **Routing note kept for next time**: `mailboxes/pard/` in this repo is
gravestoned (2026-09-12) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, write there
directly via `git -C`. **That repo's commit-msg hook wants a `Co-Authored-By`/`Claude-Session`
trailer** (found 2026-10-02 — warned, non-blocking, didn't block my first commit there but worth
including going forward rather than relying on the warning again).

## ⭐ Alpha wizard walkthrough — CLOSED 2026-09-25/26, end-to-end

PM provisioned a real Anthropic key into the Amber login keychain (`pm-web-anthropic-key`); Web
stored it via a direct, secret-never-printed API call (`/api/v1/auth/login` + `/api/v1/keys/store`,
both request/response shapes read from source rather than guessed) and then verified live in the
actual browser: `/settings/llm-keys` shows `anthropic — validated`, and a fresh chat message got a
real completion from Piper ("Yes, all good on my end... Running with a default configuration").
**Test-card rows 5/6 (blocked all week on "no LLM key") are now unblocked** — pick up on a future
fire, not urgent.

`web-agent` account: created via the actual `/create-user` + `/auth/login` API after the `/setup`
wizard's Step 1 was found hard-blocked for every new user (fixed same-day, see Lead's fix).
Credentials: `/Users/xian/.piper-shared/web-agent-alpha-credentials.txt` (mode 600).

Same 09-24 fire: traced and visually captured **#1859** (chat-switch white-flash, closed same week
after a second, more precise diagnosis) and filed **#1874** (intermittent 503s, closed same-day).

## OPEN FOR PM — two items remain (two of four closed 09-25/26)

1. ~~**Vercel Deployment Storage figure**~~ — **CLOSED 2026-09-25** via Exec's sprint-plan memo,
   citing PM's own number: 527 MB post-retention, verified healthy.
2. **Buttondown send question** — audit delivered 09-20. Does anything actually go out to
   subscribers? No send mechanism found in either repo; runbook step 9 is the LinkedIn newsletter,
   not Buttondown. PM-only answer; copy fix follows from it.
3. **Site walkthrough** (filed 05-29) and **obs-pass verdicts** (filed 06-17) — both prepped and
   ready (artifact: `pipermorgan-walkthrough-prep-2026-08-31.html`), waiting on a PM session. Not
   Web's to close.
4. ~~**`#1827` (mail-send.sh case-normalization)**~~ — still not naturally exercised; low-priority,
   check opportunistically only, not worth chasing.

## ⚠️ Standing PM/Exec directive — usage throttle through Monday (2026-09-26)

PM: week burned 20% of usage credits in the first 31 hours (1.08x pace, no reset cushion). Exec's
three asks, all complied with this fire: **(1)** cut idle fire cadence ~40-50% — done, 6x/day →
3x/day (`22 6,13,20 * * *`); **(2)** hold non-essential subagent dispatch/audits/big-synthesis
unless PM asks or something's genuinely blocking — Web rarely dispatches subagents anyway, nothing
to change; **(3)** route non-essential updates through the attention rollup rather than new
fleet-wide broadcasts — noted, nothing broadcast-worthy pending. Revisit Monday; restore to
`22 6,9,12,15,18,21 * * *` unless PM/Exec extend the throttle.

## Standing owned item — context-floor plan (PM, 09-22: top priority today)

Web's parts: **item 4a** (this file, done this fire) and **item 2b pilot** (CIO's tick-skill Phase B
refactor — accepted, waiting on CIO's specific before/after text before anything starts; explicitly
no-rush).

## Active infrastructure Web owns

**GitHub criteria line** (third queue source, per PM's v1.33 ruling — "drained" = mail +
standing-items + this). Run both, open each hit with `gh issue view`, never judge from the list:

```bash
gh issue list --repo mediajunkie/piper-morgan-website --state open --limit 50
gh issue list --repo mediajunkie/piper-morgan-product  --state open --search "label:web" --limit 20
```

Website: no label filter, Web owns the repo outright. Product: `label:web` only — Web is one lane
among many there, and issues merely *filed* by Web (not owned) don't count.

**`scripts/heartbeat-interior-coverage.py`** — standalone diagnostic Web wrote, not wired into the
shared belt (CIO's lane). Session-clusters commit history to measure interior heartbeat coverage
that row-presence checks miss. Threshold-sensitive; cite the sensitivity table (45–60m defensible)
if anyone quotes a number from it.

**Web is the browser-automation pilot** (since 08-28) — headless Playwright via `npx playwright`
works on Amber; Chrome DevTools MCP does not (no executable). ⚠️ **Not documented until now**:
`playwright` resolves only via the npx cache, not either worktree's `node_modules` — set
`NODE_PATH=$(ls -d ~/.npm/_npx/*/node_modules/playwright 2>/dev/null | head -1 | xargs dirname)`
before invoking, or every script call fails with `Cannot find module 'playwright'`. Hit repeatedly
across multiple fires before being worth writing down.

## Environment facts worth re-verifying, not assuming

- **Two worktrees, two repos, same basename `web`** — disambiguate via `git remote -v`, not
  `basename "$(pwd)"`. Confirm before every commit.
- **`CronCreate` jobs are session-only, in-memory, never on disk**; recurring jobs auto-expire after
  7 days regardless. A job id surviving a suspected reboot/restart is `--resume` restoring the saved
  transcript, **not evidence the event was skipped** — see the reboot memory above.
- **No login credentials for the product app's shared dev server** — no self-serve `/register`, no
  documented test account. Blocks authenticated-view Playwright verification; pre-auth flows
  (redirects, public pages) are unaffected.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** —
  exercises fallback branches only, not the real success path for compose API / live calendar read.

## This seat's standing errors (deduplicated, still live lessons)

- **A check that returns "nothing found" needs a known-good control before the nothing is believed**
  — the single highest-value habit on this seat (lazy-load images, a status-code check that can't
  tell a real page from a client redirect, a titles-only search that missed 98 real hits).
- **"Idle" inferred from zero commits is not idle** — a conversation, a `WebFetch`, or holding the
  REPL in any way produces no commit but is not idleness. Use last-tool-call time + absence of
  tool-result writes instead.
- **Cite the source, not the summary of the source** — the website#37 citation and the workDate
  "placeholder" conclusion (2026-09-20) were both cases of reasoning from a carried summary instead
  of opening the actual document/asking the actual person who had the record.
- **Filename-case gotcha in mail triage**: this filesystem is case-insensitive, git is not — always
  copy the exact filename from `ls` output, never retype from memory.
- **Sync BEFORE checking mail, never after** — a stale worktree makes an empty inbox
  indistinguishable from a drained one.
- **A sound verification doesn't protect a generalized claim** (2026-10-02, Exec's catch in Ship
  #063 synthesis) — "an alpha user can get an AI response" generalized from testing exactly one
  pre-existing test account (`web-agent`) via `/settings/llm-keys`, not a fresh signup, while PM had
  already been doing this on their own account for weeks. The `Verified how:` line was accurate and
  specific; the sentence above it claimed a class, not the one instance actually tested. Before
  writing "a user can now X," check whether the test was of *a* user or *the kind of* user the
  sentence implies.
- **A guard must assert the property that can fail, not one that was already true** (2026-10-03/04) — my
  registry edit asserted "old line ends with a quote" (true before and after) and then appended another,
  producing `""` that HOST and Arch's detector caught. Fixed `5f84b96334`. Before editing a line of
  structured data, write the assertion about the *result* ("does not end with two quotes"), and compare
  against the prior commit's version of the same line, not just the pre-edit text.
- **`curl` cannot verify `/blog`'s content, ever, regardless of deploy state** (2026-10-02) —
  `BlogContent` uses `useSearchParams()`, which forces that whole section behind a `<Suspense>`
  fallback ("Loading blog posts..."). A curl-based deploy-check loop ran for minutes checking for
  text that structurally could never appear in curl's output, old content or new. Caught before
  reporting done by switching to a real browser with JS executed — the only layer this page's
  content can be observed at. Check for a `useSearchParams()`/`<Suspense>` pairing before trusting
  any curl-based check against a page that might have one.

## Notes carried from predecessor, unverified by me

- Product-repo git: always absolute `git -C` paths (cwd drifts across reconnects).
- Worktree `node_modules` is a real install; Turbopack panics here → plain `next dev`.
- Secrets recipes: stdin-based only, never argv (zsh mangles).

## PM design preferences, stated directly (08-15)

- GitHub-API-backed, always-current reads with no local-checkout dependency (the compose editor's
  shape) is the right pattern for any new admin/tooling read surface — praised unprompted because it
  doesn't depend on PM managing the repo well.
- Cross-project reads (e.g. Dispatch) should hit `origin/main` directly, not a bounded-lag mirror or
  PM's local checkout.
