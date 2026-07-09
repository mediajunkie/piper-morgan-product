# Web carry-forward — 2026-07-09 (active)

**Session**: DinP/Sonnet · cron `22 6,9,12,15,18,21 * * *` · started 10:22

## Active threads

### #998 COMPOSE-UI-V1 — SHIPPED
- PR #30 merged 2026-06-23; live on pipermorgan.ai
- Phase 3 (Image Upload): **UNBLOCKED** — Exec GO 2026-07-06, inbox-proxy pilot active
  - Scoping question posed to PM (10:22 fire): image storage location (product/drafts/images vs assets/images vs other)
  - **BLOCKED on PM response** before implementation begins
- Phase 4 (Mark Ready + Git Handoff): queued after Phase 3

### July-1 site minimums — BOTH COMPLETE ✓
- [x] Footer byline: "Built by Christian Crumlish · designinproduct.com" — SHIPPED (ef9881df0)
- [x] Book-citation `/about`: "Author of Product Management for UX People (Rosenfeld)" — SHIPPED (d925aa68c)

### Newsletter "Now What?" — CLOSED ✓
- No website code updates needed (no placeholder copy found)

### Blog dedup fix — COMPLETE ✓ (12:52 fire)
- `scripts/fetch-blog-posts.js` — title-match dedup added (commit 8f8474a47, deployed)
- Reply sent to Docs

### Role portfolio
- `ROLE-PORTFOLIO-WEB.md` v0.1 routed; HOST review pending

## PM-react gated
- Phase 3 (Image Upload) — image storage location decision

## Cron state
- **ARMED** — `22 6,9,12,15,18,21 * * *`
- Re-armed at 12:52 fire after Docs work complete
