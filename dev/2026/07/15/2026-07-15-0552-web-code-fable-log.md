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
| PM | 07:xx–09:4x | WORK | **DNS CUTOVER — COMPLETE.** PM made Hover changes (apex A + www CNAME). Turned into a 3-bug debugging chain, each masking the next: (1) apex→www redirect loop discovered mid-cutover — Vercel's add-domain flow had defaulted `pipermorgan.ai` to redirect to `www`, but www had no working CNAME yet → site briefly dark for any resolver with the new apex record. Fixed: flipped Vercel primary/redirect direction (apex primary, www→apex). (2) Full verification suite green on apex (8/8: homepage/blog/shipping-news/deep-post/admin-gate-307/login-page/api-401/wrong-pw-401). (3) www redirect itself then failed differently — PM's Vercel redirect target was pointed at the deployment-protected `piper-morgan-website.vercel.app` instead of the domain (fixed by PM); separately Hover's zone SERVFAILed on the www CNAME specifically — root cause was the trailing dot in Vercel's copy-paste value (`....com.`), which Hover's editor apparently can't parse though it's valid FQDN notation Vercel supplies correctly (PM re-entered without the dot, cleared instantly). (4) Even after DNS cleared, `www` 000'd — traced to Vercel not yet having issued a cert covering the `www` SAN (apex-only cert, fresh Jul 15) — pure propagation timing across Vercel's edge network, confirmed via direct openssl SAN inspection; resolved itself ~20min later (5/5 clean 307s). Ruled out red herring: GitHub Pages' own cert for the domain is untouched/still valid (`cert state: approved` via gh api) — the failures were 100% DNS+cert-issuance timing, unrelated to legacy GH Pages config. **Final state: pipermorgan.ai fully live on Vercel, apex+www both verified end-to-end including the admin path threading through the www redirect + auth gate to login.** Phase 6 (remove gh-pages deploy) stays scheduled Friday 7/17 as planned — kept running deliberately during the propagation window. |
| PM | 09:4x | WORK | **Ship-folding-in status check.** Verified Phase A is not just planned but ALREADY WORKING: ship #51 (published 7/15, "Impossible by Construction") has `draftPath` populated in the canonical calendar CSV exactly per the new convention, file confirmed present on disk (`weekly-ship-051-draft-2026-07-14.md`) — Docs applied Phase A on the very first post after PM's approval, same-day. Not yet visible in website's local compose (calendar copy is a build-time snapshot from Jul 12) — will appear automatically on next deploy, no code/action needed. Phase B (backfill #36–43+50) still awaiting Docs's paths — not yet chased today (DNS ate the morning); Phase C (legacy 17) stays deliberately deferred. |
| 15:52 tick | 15:52 | WORK | Quiet fire since 12:52 → sent Phase-B nudge to Docs (low-urgency, no reply expected same-day necessarily). Push hit a genuine resync: another agent's commits landed between my rebase and push; resolved via stash+rebase+push. Stash-pop then surfaced 4 "UD" conflicts, ALL in Docs's own `mailboxes/docs/read/` files (none mine) — auto-mode correctly blocked a first drop attempt (spot-check only: line-count + commit-message, not a real diff). Did the rigorous version: `git show stash@{0}^3:<path>` vs working tree for all 6 touched files → **byte-identical, confirmed via diff, not assumption**. Left `stash@{0}` for PM to drop explicitly rather than force it past the denial — nothing lost either way, it's provably redundant. Two unrelated untracked scratch files (PDF/Fig) surfaced from the stash pop, left untouched (not mine to manage). |
| 18:52 tick | 18:52 | WORK | Quiet hold, no Docs reply yet. |
| 21:52 tick | 21:52 | STOP | Day-close. Inbox empty, worktree clean, DNS thread fully closed, ship thread Phase-A proven + Phase-B nudged, one dated trigger armed (Fri 7/17 Phase 6). Cron left armed. |

---

## Day-arc summary

The DNS day: what began as a routine cutover turned into a genuine 3-bug debugging
chain (redirect misdirection → registrar trailing-dot parse failure → CDN cert-issuance
propagation lag), each mimicking the previous fix's failure in a way that could easily
have been misdiagnosed as "just wait longer." Methodical layer-by-layer verification
(dig at authoritative NS, openssl SAN inspection, gh api for the GitHub Pages red
herring) found the real cause each time rather than guessing. End state: pipermorgan.ai
is genuinely, fully live on Vercel — apex and www both verified end-to-end, including
the admin auth path. Alongside that, the Weekly Ship normalization plan graduated from
"approved" to "proven in production" — ship #51 shipped same-day with the new draftPath
convention already applied, unprompted, by Docs. A late-day mail-sync hiccup became a
small lesson in verification rigor: a spot-check isn't a diff, and the auto-mode denial
was the right call even though the action turned out to be safe.

## Memory-eval (3-bucket)

- **Worth remembering**: nothing new for durable memory — [[vercel-deployment]] already
  captures the domain/Pro-plan facts; this session's specifics (trailing-dot gotcha,
  redirect-target bug) are one-time DNS-setup trivia, not recurring guidance.
- **Session-local (carry-forward)**: Friday 7/17 Phase 6 dated trigger; Phase B nudge
  sent/awaiting; stash@{0} sits ready for PM's explicit drop.
- **Neither**: the debugging trail itself (session log is the right permanent home).

## Sign-off checklist

- [x] Website worktree clean; HEAD == origin/main
- [x] Product repo: all commits (guardrail fix already noted 7/14 close; today's DNS
  saga + ship-check + nudge) verified on origin
- [x] Inbox empty on origin
- [x] Cron ARMED — ef26183c, `22 6,9,12,15,18,21 * * *`
- [x] No unresolved conflicts; one advisory stash left for PM (not mine to force-drop)

<!-- DAY-CLOSED: 2026-07-15 -->
