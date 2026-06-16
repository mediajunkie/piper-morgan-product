# Comms standing items

**Purpose**: persistent (across-days) Comms-side task list — items that aren't tied to a specific blog post or pubDate but need surfacing/advancing as cycle fires advance. Lives across days; not a per-day artifact. (Per-day work goes in `dev/2026/MM/DD/...-comms-code-opus-log.md` + `dev/active/cycle-log-comms-YYYY-MM-DD.md`.)

**Last refreshed**: 2026-06-16 (building-narrative HOLD lifted; 3 candidate beats surfaced to PM; First Subagent in Production awaiting PM voice-pass for Jun 16 publish)

---

## Active

> **✅ MIGRATION COMPLETE (2026-06-13 18:02 PT).** DinP/Sonnet session underway. comms-cycle worktree retired. Cron `b6c7e1c0` armed (`12 6,9,12,15,18,21 * * *`) — re-armed at STOP Jun 13. Adaptive-interval pilot PAUSED (PM leisurely-cadence directive; spec ratified; resume when lifted). Building-narrative HOLD until ~June 16. *Critical vs Commodity* **PUBLISHED** today (calendar updated with all URLs).

| Topic | State | Owner of next move | Notes |
|---|---|---|---|
| ***The Solo Founder Paradox* (Jun 14 insight)** | ✅ COMPLETE. Published + calendar fully updated by Docs/Dispatch (all 3 URLs; draft moved to drafts/published/). | CLOSED | |
| **Ship #047 v0.1 editorial pass** | ✅ PASS DONE 6/13 (`02206edf2`); Exec notified (`mailboxes/exec/inbox/ship-047-editorial-pass-comms-2026-06-13.md`). Mechanically clean (0 semicolons / 0 load-bearing / 0 compounding). One redundancy trim applied (methodology §). **One open accuracy item for Exec/PM**: "six agents at once" (intro ¶3 + blockers) — named cluster was *four* (cxo/ppm/exec/comms, June 8 omnibus `ef0d45373`); "six" matches the cumulative "6/9 roles needed PM intervention" week-total (`5e4ff4753`). Two fixes offered (four-at-once vs six-of-nine-across-week). Publish Wed Jun 17. | Exec (six/four call) → then PM voice-pass | Hosted-alpha "open internet/first external tester" claim verified ACCURATE (June 7 PA log: alpha.pipermorgan.ai live + Beatrice). |
| **PP-002 rename proposal** | ✅ RATIFIED 6/14 — CIO confirmed option-1 (name-only): "Critical vs. Commodity Work in a Role"; "load-bearing" kept as internal term-of-art. CIO owns execution pass (no-rush). Comms closed. | CLOSED | CIO memo in comms/read/ |
| **BYOC marketplace narrative (Comms ask, PA skunkworks Phase 2)** | PA's 6/12 skunkworks-Phase-2 memo asks Comms: "how do we talk about 'Piper on the Anthropic marketplace'? What's the narrative?" | Comms (when skunkworks Phase 2 advances) | Dovetails with the BYOC external-language frame already in PDR-005. Not urgent — open prompt within the Phase-2 ratification discussion; develop the marketplace-positioning narrative when PM/skunkworks greenlights. |
| **Next building-narrative slate — HOLD LIFTED 6/16; candidates surfaced** | `continue-narrative` assessment complete. Front = June 2 (*The Migration Wave*). 14 days of work (Jun 3–16) reviewed via omnibi. **3 candidate beats identified** — awaiting PM to shape slate (count, merges) before drafting. Beat A (Jun 6-7): "Into Production" — v0.8.7 production release, DigitalOcean hosted, alpha.pipermorgan.ai live, Beatrice = first external tester. Beat B (Jun 9+11): "What the Running System Found" — 6/9 agents silently drifted from logging discipline, self-healed same day (m-31); cron-halt mystery empirically resolved; Routines watchdog triggered. Beat C (Jun 12-14): "Almost Beta" — re-migration wave, M3 gate CLOSED, PM: "alpha — almost beta — Piper Morgan is a good PM assistant!" | PM (shape slate: count + merges) then Comms drafts | Beats 10-13 already drafted (Jul 2/7/9/14, awaiting PM voice-pass). New slate will extend beyond Jun 2 front. |
| **Duty-cycle slate (Beats 10–13) — first drafts** | ✅ DRAFTED + calendared 6/3 (`91458c53c`). 4 narratives May 25→Jun 2 at Jul 2/7/9/14. Mechanically clean, footer teases filled, fact-checks resolved. **Awaiting PM voice-pass** before publish (like all beats). | PM (voice-pass) | Beat 11 runs ~1990w — Model A section marked most-cuttable. PM-voice-pass markers in Beats 10/11/13. Assessment doc: `dev/active/comms-narrative-assessment-may25-jun2-2026-06-03.md`. |
| **Agent 360 v0.3 response (HOST)** | ✅ DELIVERED 6/3 ~8:40 PM — `mailboxes/host/inbox/agent-360-response-comms-2026-06-03.md` + sent mirror | HOST (synthesis ~Jun 12) | Full §1-10; diff vs v0.2 baseline. Headline: skill-drift (model-not-migrating) was the surprise; fixed same day. §9.4 flagged tacit-vs-documentable for HOST synthesis. Delivered ahead of ~Jun 10 backstop. |
| **Ship #045 workstream review memo (Comms lane, May 22–28)** | ✅ FILED 6/2 ~10:2x PM (`bc8b32178`); Exec has READ it (now in exec/read/) | Exec | Drafted from calendar + git + May 24/28 logs. Included attribution correction (PPM v17 rescue = PA's, not Comms `5d61755e7`). |
| Voice-pass on *When Your AI Makes Things Up* | ✅ PUBLISHED 2026-06-01 per calendar (all URLs present). Standing-items entry was stale. | CLOSED | |
| Cross-pollination relay of Ted Nadeau memo to Klatch (Janus) | PR #941 merged 2026-05-31 (`f047d9c3e`); content needs to reach Janus via next outgoing brief | Docs/CIO | Comms can surface to Docs in a brief memo if PM doesn't relay |
| Layer C → pre-commit hook for `reconcile-drafts-calendar.py` | ✅ GO SIGNAL SENT 6/13 (`mailboxes/docs/inbox/layer-c-go-signal-comms-2026-06-13.md`, `58823d721`). Docs to land warn-first + promote to blocking when ready. | Docs (execute) | All 4 layers (A/B/C/D) of orphan-prevention framework now live |
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
