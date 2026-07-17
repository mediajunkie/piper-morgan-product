# Web carry-forward — 2026-07-16 (active)

**Session**: DinP/Fable · cron `22 6,9,12,15,18,21 * * *` (job ef26183c, ARMED)

## Active threads

### Weekly Ship normalization — Phase A LIVE + PROVEN, Phase B awaiting Docs
- Phase A (new-norm draftPath from ship #51): Docs applied it same-day, unprompted —
  ship #52 will be the next real test of the convention holding.
- Phase B (backfill draftPath on #36–43, #50): Docs offered to pull paths, not yet
  sent. PM said they'd nudge directly — Web should NOT duplicate-nudge.
- Phase C (legacy #02–18, LinkedIn-era, JSON-only): deliberately deferred, PM-confirmed.

### Optional cleanup PM hasn't decided on yet (not urgent, don't act unprompted)
- Two fully-orphaned ConvertKit scripts (scripts/sync-convertkit-subscribers.js,
  scripts/fetch-subscriber-count.js) — confirmed unreferenced anywhere in package.json/
  workflows/code. Flagged 7/16, no decision yet.
- "Update Medium Blog Posts" GH Actions workflow — disabled_manually since 2026-04-14,
  confirmed genuinely obsolete (229-run history reviewed; matches PM's recollection
  of the local-first-then-crosspost pipeline shift). Recommended leaving disabled
  rather than deleting. PM hasn't said whether to delete the file.
- GitHub Pages custom-domain association on piper-morgan-website repo — harmless
  (DNS moved to Vercel) but not released. PM knows the manual step (Settings → Pages
  → Remove next to custom domain, NOT Unpublish site).

### Role portfolio — HOST review pending
### Type-error chip (task_e8c4853a) — separate session; nothing landed on main yet

## Notes
- Product-repo git: ALWAYS absolute `git -C` paths (cwd drifts across reconnects);
  stage own files BEFORE any stash; `-c rebase.autoStash=true rebase` for the sync
  dance; "Applied autostash" prints to stderr.
- Worktree node_modules is a real install; Turbopack panics here → plain `next dev`.
- Secrets recipes: stdin-based only, never argv (zsh mangles; burned 7/12).
- Pre-existing other-session stashes in product repo — leave them.
- **Verification lesson (7/16, twice)**: naive curl+grep HTML checks can false-negative
  (Suspense boundaries, client components render empty server-side). For rendered-
  content checks, grep the compiled bundle instead. For header/CSP checks, curl -I
  the actual running server — build success proves nothing about runtime headers.
- **Next.js gotcha**: next.config.ts's headers() (CSP etc.) is silently ignored under
  static export — any header-based config was dormant the whole GH Pages era and
  only started actively enforcing once Vercel (a real server) went live. Worth a
  fresh look at any other header-dependent config for the same dormant-bug pattern.

## Fully resolved this week (context only — see session logs for detail, not carried forward as open work)
Vercel migration (all 7 plan phases + DNS cutover + Phase 6 GH Pages retirement),
compose image upload, calendar build-time-staleness fix, Buttondown CSP live-bug.

## Cron state
- **ARMED** — ef26183c `22 6,9,12,15,18,21 * * *`
