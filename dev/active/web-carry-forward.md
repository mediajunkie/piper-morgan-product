# Web carry-forward — 2026-06-22 (START)

**Session**: DinP/Sonnet · worktree `claude/condescending-jackson-c9a65b` · cron `22 6,9,12,15,18,21 * * *`

## Active threads

### #998 COMPOSE-UI-V1 (migrated to website — June 21)
- **Status**: Dev server running on `:3002`; compose UI functional at `localhost:3002/admin/calendar/compose/`
- Architecture: Pages Router API (`src/pages/api/compose.ts`) + App Router client pages (`src/app/admin/calendar/compose/`)
- Phase 1 + 2 + bug fixes + migration: **DONE**
- **PM action needed**: edit Tuesday's post via compose UI → confirm test-pass → then Phase 3 gates open
- **Phase 3** (Image Upload): next after PM test-stop
- **Phase 4** (Mark Ready + Git Handoff): needs TypeScript `git_ops` equivalent + publish-ready memo
- **Pending merge**: `claude/condescending-jackson-c9a65b` → `main` after PM confirms compose works
- **Preview pane**: noted; Phase 2.1 / nice-to-have

### Role portfolio
- `docs/briefing/ROLE-PORTFOLIO-WEB.md` v0.1 authored + routed (2026-06-19)
- HOST review pending

## PM-react gated (no recent signal)
- Phase 3 + 4: gated on PM compose UI test-stop
- Obs-pass joint walkthrough (~20 items)
- Site walkthrough (resumable at `/methodology`)
- CLI B trial-run (PM end-to-end test pending)
- `--mode=archive` scope

## Dev environment notes
- Worktree: `/Users/xian/Development/piper-morgan/piper-morgan-website/.claude/worktrees/condescending-jackson-c9a65b`
- Port: 3002 (pinned in `package.json` dev script as `${PORT:-3002}`)
- `PIPER_PRODUCT_ROOT` set in `.env.local` (worktree-local, not committed)
- `node_modules` → symlink to parent website dir (Turbopack workaround)
- `package-lock.json.bak` in worktree root (hidden to avoid Turbopack duplicate-lockfile confusion)

## Cron state
- Armed: `da6d85f8` · `22 6,9,12,15,18,21 * * *`
- Next fire: 12:22 today
