# Web carry-forward — 2026-07-19 (active)

**Session**: DinP/Fable · cron `22 6,9,12,15,18,21 * * *` (job ef26183c, ARMED)

## Active threads

### Weekly Ship normalization — FULLY RESOLVED 2026-07-19 ✓
Phase A (live+proven, #51), Phase B (Docs backfilled 8/9 ships same-day, commit
d87b01878; #050 asked to move to published/, #040 has no recoverable source —
expected), Phase C (deliberately deferred) — all done. Watch for ship #52 as the
next natural test that Phase A's convention keeps holding on its own.

### Cleanup — 2 of 3 done 2026-07-19
- [x] ConvertKit orphaned scripts — deleted.
- [x] Disabled Medium RSS workflow — deleted (was `disabled_manually` since
  2026-04-14; corrected an inaccuracy in Web's own 7/16 Phase-6 notes, which had
  assumed this workflow was still active).
- [ ] GitHub Pages custom-domain release on piper-morgan-website repo — still
  needs PM's manual browser click (Settings → Pages → "Remove" next to custom
  domain, NOT "Unpublish site"). Harmless either way; PM knows the step.

### Questions batched for PM (asked 2026-07-19, no rush)
- **CLI B** (`scripts/publish-cli.js`, `npm run publish`): still exists and
  works, but has it actually been end-to-end tested since May? Or superseded by
  compose for PM's real workflow now?
- **`--mode=archive` scope**: the referenced Docs 5/18 memo no longer exists in
  any live mailbox — still wanted, or has the need passed?

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
