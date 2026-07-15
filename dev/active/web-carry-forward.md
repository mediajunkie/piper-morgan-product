# Web carry-forward — 2026-07-14 (active)

**Session**: DinP/Fable · cron `22 6,9,12,15,18,21 * * *` (job ef26183c, ARMED)

## Active threads

### ⏰ DATED TRIGGER — Phase 6 cleanup on Fri 2026-07-17 (or sooner if apex propagation complete)
- DNS CUT OVER 2026-07-15: pipermorgan.ai serves from Vercel (apex primary, verified 8/9 checks)
- gh-pages deploy DELIBERATELY kept running ~48h so cached-DNS visitors get fresh content
- Friday's work: remove peaceiris gh-pages step from deploy.yml; clean repository_dispatch
  from update-blog-posts.yml; add "fallback deployment" notice to static-build admin pages
  (PM hit dead login on static copy 7/15 — prevent recurrence); keep deploy.sh+STATIC_EXPORT
  as emergency fallback; verify daily RSS workflow still triggers Vercel rebuild after
- www straggler at cutover: Hover SERVFAIL on www CNAME (suspected trailing-dot parse issue;
  PM fixing) — verify www → 308 → apex before closing the thread

### Vercel migration — VERIFIED END-TO-END IN PRODUCTION ✓, awaiting PM's DNS cutover
- Plan artifact: https://claude.ai/code/artifact/a2ef2c23-9779-4f54-ae29-3d63f5689f88
- 2026-07-14: PM regenerated hash → login SUCCESS → compose edit-save landed on product
  main as 3a39c078f via fine-grained PAT (branch protection cleared). All 5 critical
  gotchas closed. Calendar renders 411 entries in serverless build.
- **PM will trial compose on Thursday's post** (into-production, scheduled 7/16)
- **DNS cutover: PM-schedulable anytime** — Vercel Settings → Domains → add pipermorgan.ai;
  registrar: remove GH Pages A records (185.199.108-111.153), add Vercel's shown records
  (typically A 76.76.21.21 apex + CNAME cname.vercel-dns.com www)
- **After cutover (Web work)**: Phase 6 — remove gh-pages deploy step from deploy.yml,
  clean repository_dispatch from update-blog-posts.yml, verify pipermorgan.ai serves
  `server: Vercel` headers; keep STATIC_EXPORT path for deploy.sh emergency fallback
- Test URL: piper-morgan-website-git-main-piper-morgan.vercel.app (behind Vercel SSO —
  PM's browser passes; for agent e2e PM can mint Protection Bypass for Automation secret)

### Weekly Ship normalization — WAITING on Docs reply
- Memo sent 07-14: mailboxes/docs/inbox/memo-web-to-docs-cc-pm-weekly-ship-normalization-2026-07-14.md
- Asks: ship-draft location/format, transform pipeline, draftPath population, legacy-16
  repo sources, other divergences
- PM + Web both lean **future-first** (populate draftPath on new ship rows → zero-code
  compose support; legacy backfill = optional later phase). Ships are SITE-FIRST now,
  syndicated to LinkedIn after (Web's earlier LinkedIn-canonical picture was stale —
  only true for the legacy 16, which exist solely as website-repo JSON).
- Next: Docs particulars → Web drafts joint plan → PM decision

### Phase 3 (Image Upload) — BLOCKED on PM (storage location, asked Jul 9)
### Role portfolio — HOST review pending
### Type-error chip (task_e8c4853a) — separate session; nothing on main yet

## Notes
- Product-repo git: ALWAYS absolute `git -C` paths (cwd drifts across reconnects);
  stage own files BEFORE any stash; `-c rebase.autoStash=true rebase` for the sync
  dance; "Applied autostash" prints to stderr.
- Worktree node_modules is a real install; Turbopack panics here → plain `next dev`.
- Secrets recipes: stdin-based only, never argv (zsh mangles; burned 7/12).
- Pre-existing stash@{0,1} in product repo belong to other sessions — leave them.

## Cron state
- **ARMED** — ef26183c `22 6,9,12,15,18,21 * * *`
