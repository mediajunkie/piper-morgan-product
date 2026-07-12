# Web carry-forward — 2026-07-12 (active)

**Session**: DinP/Sonnet · cron `22 6,9,12,15,18,21 * * *` · started 15:06

## Active threads

### #1391 Admin editing interface — COMPLETE ✓ (ac7795185)
- Compose API auto-commits after save (no manual git required)
- Split-pane markdown preview in ComposeEdit
- Calendar "Edit post"/"Edit draft" link shown for all draftPath entries
- Next natural enhancement: push-to-remote button in UI; full rendered preview

### #1392 Blog legacy fixes — COMPLETE ✓ (7c2673931 + f55a321be)
- Title prefixes stripped from 2 posts (4 files)
- Duplicate hero images removed from 3 posts

### Phase 3 (Image Upload) — BLOCKED on PM
- PM hasn't yet answered the image storage location question (asked Jul 9 10:22)
- Phase 3 = file picker in ComposeApp + POST /api/compose/upload

### Role portfolio
- `ROLE-PORTFOLIO-WEB.md` v0.1 routed; HOST review pending

## Cron state
- **ARMED** — `22 6,9,12,15,18,21 * * *` (job `f6bf95cb`)
