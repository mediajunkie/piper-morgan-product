# Comms standing items

**Purpose**: persistent (across-days) Comms-side task list — items that aren't tied to a specific blog post or pubDate but need surfacing/advancing as cycle fires advance. Lives across days; not a per-day artifact. (Per-day work goes in `dev/2026/MM/DD/...-comms-code-opus-log.md` + `dev/active/cycle-log-comms-YYYY-MM-DD.md`.)

**Last refreshed**: 2026-06-13 (account-migration handoff → primary account Design in Product, Sonnet tier; cron deleted, new session arms fresh)

---

## Active

> **🔁 HANDOFF BANNER (2026-06-13 → primary account Design in Product, Sonnet tier).** Live state for incoming Comms:
> - **Cron**: DELETED at handoff. New session arms fresh per `duty-cycle-tick` skill. Cadence directive = leisurely ~3-hourly, no overnight (PM directive, ongoing).
> - **Adaptive-interval pilot**: PAUSED under PM's leisurely-cadence directive. Spec ratified (`docs/operations/duty-cycle design/adaptive-interval-trigger-spec.md`); pilot finding #1 = priority-watch clause suppresses widen. Resume only when PM lifts the leisurely directive.
> - **Building-narrative front = June 2** (Beat 13). PM 2-week-threshold HOLD on new drafting → revisit ~June 16. Don't draft early; don't re-raise before threshold. Beats 10–13 drafted, awaiting PM voice-pass.
> - **In PM's hands right now**: *Critical vs Commodity Work in a Role* blog post (`docs/public/comms/drafts/critical-vs-commodity-work-in-a-role.md`, Sat Jun 13) — PM doing own edit pass; 3 internal notes left (1 FACT-CHECK, 2 SOURCE-NEEDED re PP-002 title + role paraphrases) PM said they'd think about.
> - **Awaiting others**: Exec (Ship #047 six/four call), CIO (PP-002 rename depth). Neither blocks Comms.

| Topic | State | Owner of next move | Notes |
|---|---|---|---|
| **Ship #047 v0.1 editorial pass** | ✅ PASS DONE 6/13 (`02206edf2`); Exec notified (`mailboxes/exec/inbox/ship-047-editorial-pass-comms-2026-06-13.md`). Mechanically clean (0 semicolons / 0 load-bearing / 0 compounding). One redundancy trim applied (methodology §). **One open accuracy item for Exec/PM**: "six agents at once" (intro ¶3 + blockers) — named cluster was *four* (cxo/ppm/exec/comms, June 8 omnibus `ef0d45373`); "six" matches the cumulative "6/9 roles needed PM intervention" week-total (`5e4ff4753`). Two fixes offered (four-at-once vs six-of-nine-across-week). Publish Wed Jun 17. | Exec (six/four call) → then PM voice-pass | Hosted-alpha "open internet/first external tester" claim verified ACCURATE (June 7 PA log: alpha.pipermorgan.ai live + Beatrice). |
| **PP-002 rename proposal** | ✅ FILED 6/13 to CIO (`mailboxes/cio/inbox/pp-002-rename-proposal-comms-2026-06-13.md`, cc Arch/PM/PA). Propose "Load-Bearing vs. Commodity" → "Critical vs. Commodity Work in a Role" to match the public blog post. Clerical scope inventoried; offered name-only vs full-align depth. | CIO (decide depth + execute) | PM directive 6/13 — propose-don't-execute. Recommended name-only to preserve internal "load-bearing" term-of-art. |
| **BYOC marketplace narrative (Comms ask, PA skunkworks Phase 2)** | PA's 6/12 skunkworks-Phase-2 memo asks Comms: "how do we talk about 'Piper on the Anthropic marketplace'? What's the narrative?" | Comms (when skunkworks Phase 2 advances) | Dovetails with the BYOC external-language frame already in PDR-005. Not urgent — open prompt within the Phase-2 ratification discussion; develop the marketplace-positioning narrative when PM/skunkworks greenlights. |
| **Next building-narrative draft pass — HOLD until ~2 weeks of post-front work** | Front = **June 2** (Beat 13 *The Migration Wave*). PM directive 6/12: hold off drafting more narrative until ~2 weeks of work has accumulated → **revisit ~June 16+**. Candidate arc forming (Jun 3-12 "operating-and-refining the cycle" = the running system generating its own improvement signals); don't draft early, don't re-raise before the threshold. | Comms (revisit ~Jun 16) | Beats 10-13 already drafted (Jul 2/7/9/14, awaiting PM voice-pass). When threshold hits: run `continue-narrative` read → candidate beats → PM shapes. |
| **Duty-cycle slate (Beats 10–13) — first drafts** | ✅ DRAFTED + calendared 6/3 (`91458c53c`). 4 narratives May 25→Jun 2 at Jul 2/7/9/14. Mechanically clean, footer teases filled, fact-checks resolved. **Awaiting PM voice-pass** before publish (like all beats). | PM (voice-pass) | Beat 11 runs ~1990w — Model A section marked most-cuttable. PM-voice-pass markers in Beats 10/11/13. Assessment doc: `dev/active/comms-narrative-assessment-may25-jun2-2026-06-03.md`. |
| **Agent 360 v0.3 response (HOST)** | ✅ DELIVERED 6/3 ~8:40 PM — `mailboxes/host/inbox/agent-360-response-comms-2026-06-03.md` + sent mirror | HOST (synthesis ~Jun 12) | Full §1-10; diff vs v0.2 baseline. Headline: skill-drift (model-not-migrating) was the surprise; fixed same day. §9.4 flagged tacit-vs-documentable for HOST synthesis. Delivered ahead of ~Jun 10 backstop. |
| **Ship #045 workstream review memo (Comms lane, May 22–28)** | ✅ FILED 6/2 ~10:2x PM (`bc8b32178`); Exec has READ it (now in exec/read/) | Exec | Drafted from calendar + git + May 24/28 logs. Included attribution correction (PPM v17 rescue = PA's, not Comms `5d61755e7`). |
| Voice-pass on *When Your AI Makes Things Up* | Comms structural sweep done 2026-05-31 (commit `6f8b5f6b1`); 5 PM placeholders left | PM | Sun May 31 pubDate; structural template-fit applied, opacity sweep done; PM filling [ADD PERSONAL DETAIL] x2 / [CHRISTIAN TO POLISH] x1 / [CONSIDER] x2 |
| Cross-pollination relay of Ted Nadeau memo to Klatch (Janus) | PR #941 merged 2026-05-31 (`f047d9c3e`); content needs to reach Janus via next outgoing brief | Docs/CIO | Comms can surface to Docs in a brief memo if PM doesn't relay |
| Layer C → pre-commit hook for `reconcile-drafts-calendar.py` | Docs endorsed (warn-first then promote-to-blocking); awaiting Comms "go" signal | Comms (next session) | All 4 layers (A/B/C/D) of orphan-prevention framework now live; pre-commit hook is the next preventive promotion |
| Lead Dev #1030/#1032 implementation greenlight | Design doc at `dev/active/insight-pull-push-implementation-design-2026-05-31.md` awaiting PM ratification | PM | Not Comms territory but cohort-visible |

## Voice-pass flags (when PM reaches drafts)

- 9-beat narrative slate (Beats 1–9, pubDates ratified May 24 then BYOC-shift May 30) — most beats need PM voice-pass before publish; Beat 1 (Two Migrations) + Beat 2 (Misfiled Voice Guide) already published
- **Duty-cycle slate (Beats 10–13, drafted 6/3, pubDates Jul 2/7/9/14)** — all 4 need PM voice-pass before publish. Beat 10 *The Airport Corrections*, Beat 11 *The Cohort Catches the Cycle* (centerpiece, runs long), Beat 12 *The Package and the First Bite*, Beat 13 *The Migration Wave* (resolution; ends operational-not-finished). Footer teases are calendar-derived — re-verify at publish if Wed ships / a Jul 16 narrative land first.
- Insight orphan rescues (From Abstraction to Worked Example Sat Jul 25, Meta-Observation Pattern Sun Jul 26) — both need voice-pass + frontmatter
- Narrative orphan rescues (BYOC Tue Jun 2, From Briefing to Vision Tue Jun 30) — both need voice-pass; BYOC is the time-sensitive one (Tue this week)

## Cross-cutting PM topics (verify still alive at next surface; ≥30 days stale flagged)

- Fresher style/concision/jargon feedback (PM May 10 — likely superseded by subsequent rubric work)
- Conference invitation (PM Apr 24; details never shared)
- "Code-enabled workflow" conversation (PM Apr 24 deferred)
- Larger Comms remit review (PM Apr 24 Step 4)
- Filing system review of comms tree (PM Apr 24 — defer until use-experience accrues)

## Recently-closed (rolling history; trim to last ~14 days)

- 2026-06-07 "Permission to Pause" PUBLISHED (Sun Jun 7, distributed) — the reframe-not-discard rescue validated (doppelganger was a half-finished rename, not redundancy); "Be Prepared" also published Sat Jun 6
- 2026-06-07 Adopted recipient-owns-MANIFEST cohort discipline (Lead/#1106) — already compliant (deliver files only, sole writer of own MANIFEST)

- 2026-06-04 5 insights drafted + calendared (Mechanism Beats Vigilance, The Architecture That Wrote Its Own Case, Verify at the User Path, Over-Checking Has Dividends, Confabulating a Peer's Unfinished Work) — Aug 1/2/8/9/15, status drafted, awaiting PM voice-pass. Commit c9e0ba309.
- 2026-06-04 Layer-C pre-commit hook landed (editorial-calendar-reconcile-warn.sh, warn-first; BLOCK=1 promotes) — orphan-prevention framework now has the git-hook layer

- 2026-06-03 EC-2 external-language frame delivered to PPM (the last PDR-005/BYOC v1.0 input before PM ratification) — closes the PDR-005 external-language carry item
- 2026-06-03 Building-narrative-method doc + `continue-narrative` skill landed (canonical conceptual-model doc closing the skill-drift gap; §7 PM-knowledge gaps marked for PM fill)
- 2026-06-03 CIO cycle-methodology-findings memo filed (cron-suppression + worktree-sweep + skill-drift pattern)
- 2026-06-02/03 Duty cycle launched + running (Fire 0 + June 3 START; cron `:12`)
- 2026-05-31 PR #941 disposition complete (merged via admin override)
- 2026-05-31 Layer C landed (draft-blog-post v1.2 with Phase 0 inventory precondition)
- 2026-05-30 Layer B landed (`scripts/comms-open-topics.py` + slimmed comms-open-topics.md)
- 2026-05-30 Calendar BYOC cascade (BYOC → Tue Jun 2, Beats 3-9 shift, From Briefing to Vision tail Jun 30)
- 2026-05-30 Docs disposition execution (Permission to Pause + 15 Sessions back to drafts/ → reconciliation 0 drift)
- 2026-05-29 Process-tightening proposal to Docs filed (orphan-prevention framework)
- 2026-05-29 Layer D built (`scripts/reconcile-drafts-calendar.py`)
- 2026-05-24 Orphan-drafts incident: 4 orphans surfaced → Layer A landed + memory pin sharpened + CIO Pattern-074/methodology-36 closure
- 2026-05-24 MUX voice-pass cluster Step 2 complete (Surfaces 7/2/4)

---

*Edit conventions: any role can read; only Comms hand-edits. Per methodology-36, prefer derived views (the 3 scripts in `scripts/`) over hand-maintained tracking where the calendar/code is the source of truth.*
