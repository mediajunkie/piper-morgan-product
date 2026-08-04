# Web carry-forward — 2026-07-29 (active)

**Session**: Amber / pipermorgan.ai, Opus 5 · cron `22 6,9,12,15,18,21 * * *` (job `fafad118`, ARMED, session-only — see caveat below) · registry row `dev/active/duty-cycle-registry.tsv` line `web`

## ⚠️ Environment facts worth re-verifying each fire, not assuming

- **Two worktrees, two repos**: `piper-morgan-worktrees/web` (cohort infra — mail/logs/`dev/`) on `claude/web-cycle`; `piper-morgan-website-worktrees/web` (actual Web lane) on `claude/web-cycle`. Confirm which one before every commit.
- **`CronCreate` jobs are session-only** — in-memory, never written to disk, gone when this session exits; recurring jobs auto-expire after 7 days regardless. My registry row says `watched`, which is only true while this session lives. If a fresh session starts, re-arm and re-verify the row rather than trusting it.
- **No Chrome on this host** — `mcp__chrome-devtools__new_page` fails, executable not found. No in-browser click-through testing available; verify via types/lint/build + targeted extracted-logic tests instead, and say so.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** — can exercise failure/fallback branches locally but not the real success path for anything touching the compose API or the live GitHub-backed calendar read. Vercel has these; first real click-through after a deploy is the actual test.

## Active threads

### Blog soft-404 — SHIPPED + LIVE-VERIFIED 2026-08-04; one watch item for tonight
Comms found `pipermorgan.ai/blog/<any-nonexistent-slug>/` and `/blog/page/<out-of-range>/` both
return HTTP 200 with the not-found shell body (Vercel ISR serving a mis-cached dynamic render —
`x-nextjs-prerender: 1` + `x-vercel-cache: HIT` on the 200 response). Root-caused: both routes
default `dynamicParams` to `true`, so an unknown param falls through to a dynamic render that
Vercel's edge cache can serve back with the wrong status. Fix is safe because the data
(`medium-posts.json`) is a build-time static import — no slug/page number outside
`generateStaticParams()` can ever be valid without a rebuild anyway. Set
`export const dynamicParams = false` on both `[slug]/page.tsx` and `[pageNumber]/page.tsx`
(website `03b77d9d`) — forces unknown params to 404 immediately at the routing layer. **Verified
locally end-to-end** (`next build && next start`), **and confirmed live independently by both me
and Comms** after Vercel's auto-deploy landed (~2hr): known slug/page unchanged at 200, unknown
slug/page now genuinely 404.

**One open, genuinely uncertain question, not mine to resolve alone**: tonight's real publish
(`the-list-that-lies`) is currently a cached 404 (Comms' observation, `age: 5642`). My reasoning
(written up in mail, cc Docs/Comms/PM/HOST/PA) is that this is a build-time/routing-layer 404, not
Vercel's fetch-based Data Cache, so a genuine new deployment should serve the new static page
directly rather than needing individual cache-entry invalidation — but I don't have Vercel's
internals and said so plainly rather than overclaiming. **Docs/Comms are checking status + content
at tonight's actual publish** — that's the real test, not something I can force. If it comes back
stale, the fix is known and cheap (manual Vercel redeploy, or add `revalidatePath()` going
forward) — watch for the result next fire, don't re-derive the reasoning if it holds.

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

### Two Docs-flagged gaps from the calendar work, routed not fixed
1. `/admin/publish-queue` — same staleness class, different data path (prebuild-generated
   JSON, not `loadCalendar()` directly) — Docs' call whether to convert it too.
2. `copy-editorial-calendar.js`'s local-sibling-checkout path resolves `../piper-morgan-product`
   from the website repo root — **broken from a worktree** (`piper-morgan-website-worktrees/{role}`
   has no such sibling). Falls through to the GitHub API; with no local token, writes a
   **header-only placeholder CSV**. Hits Docs' publish flow before mine. Offered to fix
   (walk-up-to-find vs. prefer-API); awaiting their preference.

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
- **ARMED** — `fafad118`, `22 6,9,12,15,18,21 * * *` — **session-only, see env-facts caveat above**
