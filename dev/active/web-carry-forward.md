# Web carry-forward — 2026-07-12 (active)

**Session**: DinP/Fable-trial (Sonnet base) · cron `22 6,9,12,15,18,21 * * *` · PM session from 15:06

## Active threads

### Vercel migration — phases 1–3 SHIPPED ✓, phases 0/4/5 PM-GATED
- Plan artifact: https://claude.ai/code/artifact/a2ef2c23-9779-4f54-ae29-3d63f5689f88
- Phase 1 ✓ static export behind STATIC_EXPORT flag (CI-verified green)
- Phase 2 ✓ GitHub Contents API draft storage, dual-mode compose, SHA concurrency
  - Branch-protection bypass via owner token CONFIRMED live (commit 323ceefdb on product main)
- Phase 3 ✓ password login + JWT cookie + fail-closed APIs + Edge middleware + AdminGate
- **Waiting on PM** (checklist delivered in chat 2026-07-12 evening):
  1. Vercel account + project (Hobby-vs-Pro decision; Pro $20/mo recommended)
  2. Fine-grained PAT for piper-morgan-product (Contents R/W) → GITHUB_DRAFT_TOKEN
  3. Generate ADMIN_SESSION_SECRET + ADMIN_PASSWORD_HASH (commands in .env.example)
  4. Vercel env vars (incl. NEXT_PUBLIC_GA_MEASUREMENT_ID=G-SVPLRHEEBP)
  5. Test on *.vercel.app preview, THEN DNS cutover
- After cutover (Web work): remove gh-pages deploy step + repository_dispatch cleanup (plan Phase 6)

### #1391 Admin editing interface — COMPLETE ✓ (ac7795185, extended by Vercel phases)
### #1392 Blog legacy fixes — COMPLETE ✓ (7c2673931 + f55a321be)

### Phase 3 (Image Upload) — BLOCKED on PM
- Image storage location question still open (asked Jul 9 10:22)

### Role portfolio
- `ROLE-PORTFOLIO-WEB.md` v0.1 routed; HOST review pending

## Notes
- Worktree node_modules is now a real install (was symlink; npm i jose replaced it). Turbopack panics in worktree — use plain `next dev` if needed.
- Pre-existing type errors (7, searchParams/pathname nullability in blog/nav components) — spawn-task chip filed; not blocking (ignoreBuildErrors).
- fs-mode auto-commit now pathspec-scoped (can't sweep other agents' staged files).

## Cron state
- **ARMED** — `22 6,9,12,15,18,21 * * *` (re-armed end of Vercel build session)
