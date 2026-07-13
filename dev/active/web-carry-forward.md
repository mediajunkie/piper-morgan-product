# Web carry-forward — 2026-07-12 close (active)

**Session**: DinP/Fable-trial · cron `22 6,9,12,15,18,21 * * *` (job ef26183c, ARMED) · day CLOSED 21:52

## Active threads

### Vercel migration — DEPLOY LIVE, blocked on PM password-hash retry
- Plan artifact: https://claude.ai/code/artifact/a2ef2c23-9779-4f54-ae29-3d63f5689f88
- Phases 1–3 shipped + CVE fix (website commits through 46cb2611b); GH Pages stayed green
- Vercel: **Pro plan**, team slug `piper-morgan`, deploy GREEN on Next 15.4.11
  - Test URL: `piper-morgan-website-git-main-piper-morgan.vercel.app` (behind Vercel deployment protection — PM's browser passes via Vercel SSO; custom domain won't have this layer)
- **WAITING on PM**: `/admin/login` said "Wrong password" → hash was quoting-mangled at generation. Quoting-proof regen recipe delivered (read -s → stdin → bcryptjs), then bare-paste into Vercel env + redeploy.
- **Then**: PM e2e on preview (login → edit draft → verify commit in product repo) → DNS cutover (records TBD from Vercel domain settings) → Web does Phase 6 (remove gh-pages deploy step + repository_dispatch cleanup; STATIC_EXPORT env stays for deploy.sh emergency fallback)
- Env vars status: ADMIN_* + GITHUB_DRAFT_TOKEN evidently set (enforced mode responded); GA id delivered (G-SVPLRHEEBP); SENTRY_* optional, not set

### Phase 3 (Image Upload) — BLOCKED on PM (image storage location, asked Jul 9)
### Role portfolio — HOST review pending
### Type-error cleanup — spun off as chip task_e8c4853a, running in separate session (7 pre-existing TS18047 in blog/nav); nothing landed on main yet at close

## Notes
- Worktree node_modules is a REAL install now (npm i jose replaced symlink). Turbopack panics in this worktree → use plain `next dev`.
- fs-mode auto-commit is pathspec-scoped now (can't sweep other agents' staged files) — defect found live 7/12.
- Draft serializer round-trips canonically (blank line after frontmatter restored).
- Secrets recipes: always stdin-based, never argv (zsh quoting/history-expansion mangles passwords — burned once).

## Cron state
- **ARMED** — ef26183c `22 6,9,12,15,18,21 * * *` (session-only; Gap-C self-heal on next turn if session died)
