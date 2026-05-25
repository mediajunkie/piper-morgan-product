# Web Handoff — 2026-05-25 (mid-session)

**For**: Future-web (post-compaction recovery, or fresh-session pickup)
**Reason**: PM noted context was getting full; writing this as a safety net so the in-flight thread can resume if compaction loses detail.

## What just happened (this session, May 16 → May 25)

A 10-day arc that built and shipped the **three-layer publishing tooling** (Engine / CLI / Web GUI). Plus today: site obs pass + visual scan pass, mid-walkthrough.

Major shipments (in order):
- `publish-post.js` (Engine, 5/16) — mechanical publish pipeline
- `publish-to-blog` skill v0.10 → v0.16 — pointed at the script; lots of cohort-driven refinement
- `/admin/publish-queue` dashboard (Web GUI v1, read-only, 5/16)
- Route-group refactor for admin SSR (5/17) — `(public)/` for marketing routes, `admin/` outside
- CLI B walking-skeleton + enrichment (5/18) — `npm run publish` opens the full interactive flow
- 4 markdown-conversion Gap fixes (1–4, shipped 5/17 → 5/20)
- Feature-corpus harness (5/18) — `npm run test:corpus`
- Site observation pass (5/24) — 31 items at `dev/active/site-observation-pass-2026-05-24.md`
- 4 obs-pass polish items shipped (5/24)
- Visual scan report (5/25) — `dev/active/visualscanpipermorgan20260525.md`

## Where things are right now (5/25 ~10:35)

**Mid-walkthrough with PM**:
- Just shipped VA-9 footer typo at website `5601b0486`
- Visual scan exposed a **Tailwind v3-config-being-ignored-by-v4** root cause that explains VA-1, VA-11, VA-22, possibly VA-3
- PM is about to discuss path forward + planning to do a compaction

**The Tailwind finding** (load-bearing — read this first if recovering):
- `package.json` has `"tailwindcss": "^4"` and `"@tailwindcss/postcss": "^4"` — v4 is installed.
- `tailwind.config.ts` exists with custom colors (`primary.teal`, `primary.orange`, `primary.teal-text`, etc.).
- `src/app/globals.css` has only `@import "tailwindcss";` — NO `@theme` block.
- Confirmed via `grep -oE "bg-(primary|teal|orange)[a-z0-9-]*" out/_next/static/css/*.css | sort -u`: built CSS has `bg-teal-600`, `bg-orange-100`, etc. (standard palette), but ZERO `bg-primary-teal`, `bg-primary-orange`, `bg-primary-teal-text`, etc.
- Conclusion: custom `primary.*` color classes referenced throughout the codebase silently produce no CSS. Site has been working because many places use standard-palette classes, but `variant="primary"` on CTAButton (uses `bg-primary-teal text-white`) renders with no background → looks like an invisible/transparent button.
- **Fix**: migrate `tailwind.config.ts` custom theme to a `@theme` block in `globals.css`. ~30-60 min done carefully. Need to replicate every custom color + font + spacing + shadow + animation + typography block. Verify by rebuild + grep on out/ for the previously-missing classes.

## Active queues

**Visual scan items** (full list in `dev/active/visualscanpipermorgan20260525.md`):
- **P1 still open**: VA-1 (invisible beta button — pending Tailwind migration), VA-2 (hero logo white-bg in dark mode), VA-3 (dark-mode contrast on section headings)
- **P2 open**: VA-5, VA-6, VA-7, VA-8 (post count discrepancy), VA-10 (privacy date), VA-11 (CTA hierarchy regression — also pending Tailwind migration)
- **P3 open**: VA-16 (404 page regression — possibly from my route-group refactor), VA-17, VA-22 (alpha/beta orange differentiation invisible — pending Tailwind migration)

**Obs pass items** (`dev/active/site-observation-pass-2026-05-24.md`, 25 of 31 still awaiting PM react):
- PM judgment cluster: #1, #7, #17, #19, #27
- Polish reactable: #6, #8, #10, #12–14, #16, #20–23, #25–28, #30
- See SHIPPED markers for what's done

**Standing PM-side decisions** (outside both docs):
- Lint policy — disable `react/no-unescaped-entities` vs mechanically escape 74 warnings
- `--mode=archive` scope approval (per Docs's 5/18 memo signal #6)
- CLI B trial-run (PM still hasn't end-to-end-tested the enriched flow)
- Formspree form ID (held per PM "too distracted"; doubly irrelevant until VA-1 / Tailwind fix lands)

## Where things live

- **Canonical plan**: `dev/active/web-publishing-admin-plan.html` — HTML render of the multi-layer architecture + status snapshot
- **CLI B design sketch**: `dev/2026/05/17/2026-05-17-0747-cli-b-design-sketch.md`
- **Obs pass**: `dev/active/site-observation-pass-2026-05-24.md`
- **Visual scan**: `dev/active/visualscanpipermorgan20260525.md`
- **This handoff**: `dev/active/web-handoff-2026-05-25.md`
- **Today's log**: `dev/2026/05/25/2026-05-25-0942-web-code-opus-log.md`
- **Skill (Docs owns)**: `.claude/skills/publish-to-blog/SKILL.md` (currently v0.16)
- **Inbox**: `mailboxes/web/inbox/` (empty — just triaged 5/24)
- **Read mail with dispositions**: `mailboxes/web/read/MANIFEST.md`

## Standing principles (refresher)

All in `~/.claude/projects/-Users-xian-Development-piper-morgan-piper-morgan-website/memory/`:

- Human-first, agent-aware
- Conservative deletion (quarantine > rm; audit before delete)
- Unblocked work, batched questions
- Bias to immediate action (don't sit on small unblocked items)
- Deferral requires PM approval (don't silently defer)
- Extend existing mechanisms until they overload
- Three-layer publishing architecture (Engine / CLI / Web GUI)
- Two-repo operating pattern (website code in piper-morgan-website; logs/mailbox in piper-morgan-product)
- Triage-to-read after each memo processed (cohort hygiene — PM flagged web was non-compliant 5/24; corrected)

## Recommended pickup sequence (if recovering cold)

1. Read this handoff
2. Read the visual scan + obs pass quickly to know the current item shape
3. Confirm git state matches (`git -C piper-morgan-website log --oneline -5` should show `5601b0486` at top)
4. Check `mailboxes/web/inbox/` for anything new
5. If the Tailwind migration is the active task: read `tailwind.config.ts` + `src/app/globals.css` + the Tailwind v4 @theme docs; plan the migration as one cohesive commit; build + grep verify
6. If unsure of direction: ask PM where to pick up — they'll either continue the walkthrough or redirect

---

*Self-archive when the publishing-admin work closes out OR when the next pickup-state memory supersedes.*
