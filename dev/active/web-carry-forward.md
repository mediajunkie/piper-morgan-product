# Web carry-forward — 2026-07-14 (active)

**Session**: DinP/Fable · cron `22 6,9,12,15,18,21 * * *` (job ef26183c, ARMED)

## Active threads

### ⏰ DATED TRIGGER — Phase 6 cleanup on Fri 2026-07-17
- DNS CUTOVER COMPLETE 2026-07-15: pipermorgan.ai + www.pipermorgan.ai BOTH fully verified
  end-to-end (apex primary 200, www→apex 307, admin path threads through both correctly).
  3-bug chain resolved: Vercel redirect-target bug (pointed at protected .vercel.app),
  Hover trailing-dot CNAME parse failure, Vercel www-cert edge-propagation lag (~20min).
  GitHub Pages cert ruled out as a factor (still valid/untouched).
- gh-pages deploy DELIBERATELY kept running since cutover so cached-DNS visitors get
  fresh content during the propagation tail
- Friday's work: remove peaceiris gh-pages step from deploy.yml; clean repository_dispatch
  from update-blog-posts.yml; add "fallback deployment" notice to static-build admin pages
  (PM hit dead login on static copy 7/15 pre-cutover — prevent recurrence); keep
  deploy.sh+STATIC_EXPORT as emergency fallback; verify daily RSS workflow still triggers
  Vercel rebuild after

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

### Weekly Ship normalization — Phase A LIVE + PROVEN, Phase B awaiting Docs
- Docs particulars (7/15) confirmed 4 populations; plan drafted + PM APPROVED 7/15
  ("Phase A is critical")
- Phase A (new-norm draftPath from ship #51): Docs applied it to #51 same-day —
  VERIFIED on disk + in canonical CSV (docs/public/comms/drafts/weekly-ship-051-draft-2026-07-14.md).
  Zero code needed; website's local calendar copy just needs its next normal deploy
  to pick up the row (build-time snapshot, not live-read)
- Guardrail (Web) SHIPPED: empty-alt check extended to ship category (previously
  latent gap — all 15 published ships happened to have alt, but nothing enforced it);
  caption stays ship-exempt. Dry-run + 19-case corpus verified.
- Phase B (backfill draftPath on #36–43, #50): Docs offered to pull paths — NOT YET
  SENT, not yet re-chased (DNS ate 7/15). Low urgency per plan.
- Phase C (legacy #02–18, LinkedIn-era, JSON-only): deliberately deferred, PM-confirmed.

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
