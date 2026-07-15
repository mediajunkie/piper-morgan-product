# Web session — 2026-07-15 (Wednesday)

**Role**: Unicorn Web Designer (piper-morgan-website)
**Account**: DinP (xian@designinproduct.com)
**Model**: Claude Fable 5 (continued session)
**Trigger**: PM prompt 05:52
**Branch**: claude/condescending-jackson-c9a65b worktree → pushes to main

---

## Boot (05:52)

Jul-14 DAY-CLOSED confirmed. PM opened with two items: ship-UI status + a login
failure report on pipermorgan.ai/admin.

---

## Fire log

| Fire | Time | Action | Notes |
|------|------|--------|-------|
| PM | 05:52 | START/WORK | **405 mystery solved in minutes**: PM tried pipermorgan.ai/admin — still GitHub Pages (server: GitHub.com verified; DNS never cut). Static site has the login page but no APIs → hung session check + 405 on POST. Not a regression; password fine; correct URL is the vercel.app alias until cutover. Delivered exact Hover DNS steps (NS = hover.com verified; 4× 185.199.x A records → Vercel's records; www CNAME mediajunkie.github.io → cname.vercel-dns.com). Post-cutover TODO noted: static-fallback admin pages should show "fallback deployment" notice instead of dead login. |
| Docs reply | ~06:1x | WORK | **Ship particulars landed** (memo 2026-07-15). Key facts: ship drafts = same markdown+frontmatter format/location as blog drafts; same publish-post.js (--category ship); 4 populations (17 LinkedIn-era JSON-only / 2 with draftPath / 9 blog-published untracked / 6 fully normalized — those 6 ALREADY compose-editable via calendar edit links). Drafted joint plan: Phase A new-norm draftPath at draft time from #51 (Docs, zero code) / Phase B backfill 9 (calendar-only) / Phase C legacy-17 deliberately deferred / Web guardrail check. **PM APPROVED** ("Phase A is critical. Please do check that guardrail!"). |
| Guardrail | 06:2x | WORK | **Checked + fixed.** Docs's feared hazard absent: ship branch ignores frontmatter image entirely (unconditional piper-ship.webp, no prepImage). Real adjacent gap found: ships exempt from Gap-3 empty-meta guard while their CSV rows DO carry imageAlt to production (all 15 published ships have alt — latent, not active). Fix: alt checked for all categories, caption stays ship-exempt (11/15 ships have no caption by convention). Dry-run verified both branches; 19-case corpus green. Website commit pushed. Plan-approved memo → Docs (Phase A theirs, Phase B paths requested, guardrail findings + compose image-field note documented). |
