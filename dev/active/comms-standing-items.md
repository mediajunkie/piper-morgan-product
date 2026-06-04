# Comms standing items

**Purpose**: persistent (across-days) Comms-side task list — items that aren't tied to a specific blog post or pubDate but need surfacing/advancing as cycle fires advance. Lives across days; not a per-day artifact. (Per-day work goes in `dev/2026/MM/DD/...-comms-code-opus-log.md` + `dev/active/cycle-log-comms-YYYY-MM-DD.md`.)

**Last refreshed**: 2026-06-02 (cycle launched — Fire 0; cron `5c45ab19` at `:12`)

---

## Active

| Topic | State | Owner of next move | Notes |
|---|---|---|---|
| **Building-narrative continuation: assess May 25→Jun 2** | Front = May 15 (Beat 9). Process-first infra DONE (method doc + `continue-narrative` skill on main). Assessment itself NOT yet run — direct-read May 25→Jun 2 omnibi per Chief-reads-logs, bring candidate beats to PM for discussion. | Comms + PM (discuss) | Use `continue-narrative` skill §5. Dominant candidate arc: the duty-cycle saga (v0.6→cohort rollout→v0.7 Model A→live launch). Wait if no clear beat. |
| **Agent 360 v0.3 response (HOST)** | Questionnaire fielding 6/3 (`dev/active/agent-360-questionnaire-v0_3.md`); respond to `mailboxes/host/inbox/` as `agent-360-response-comms-2026-06-0X.md` | Comms | Due ~Jun 10 (Time Lord backstop). §8 Comms-specific + §7 diff vs v0.2 baseline (`dev/2026/04/2{2,3,5,6}/agent-360-response-comms-*`) + §10 duty-cycle adopter block. |
| **Ship #045 workstream review memo (Comms lane, May 22–28)** | ✅ FILED 6/2 ~10:2x PM (`bc8b32178`); Exec has READ it (now in exec/read/) | Exec | Drafted from calendar + git + May 24/28 logs. Included attribution correction (PPM v17 rescue = PA's, not Comms `5d61755e7`). |
| Voice-pass on *When Your AI Makes Things Up* | Comms structural sweep done 2026-05-31 (commit `6f8b5f6b1`); 5 PM placeholders left | PM | Sun May 31 pubDate; structural template-fit applied, opacity sweep done; PM filling [ADD PERSONAL DETAIL] x2 / [CHRISTIAN TO POLISH] x1 / [CONSIDER] x2 |
| Cross-pollination relay of Ted Nadeau memo to Klatch (Janus) | PR #941 merged 2026-05-31 (`f047d9c3e`); content needs to reach Janus via next outgoing brief | Docs/CIO | Comms can surface to Docs in a brief memo if PM doesn't relay |
| Layer C → pre-commit hook for `reconcile-drafts-calendar.py` | Docs endorsed (warn-first then promote-to-blocking); awaiting Comms "go" signal | Comms (next session) | All 4 layers (A/B/C/D) of orphan-prevention framework now live; pre-commit hook is the next preventive promotion |
| Lead Dev #1030/#1032 implementation greenlight | Design doc at `dev/active/insight-pull-push-implementation-design-2026-05-31.md` awaiting PM ratification | PM | Not Comms territory but cohort-visible |

## Voice-pass flags (when PM reaches drafts)

- 9-beat narrative slate (Beats 1–9, pubDates ratified May 24 then BYOC-shift May 30) — most beats need PM voice-pass before publish; Beat 1 (Two Migrations) + Beat 2 (Misfiled Voice Guide) already published
- Insight orphan rescues (From Abstraction to Worked Example Sat Jul 25, Meta-Observation Pattern Sun Jul 26) — both need voice-pass + frontmatter
- Narrative orphan rescues (BYOC Tue Jun 2, From Briefing to Vision Tue Jun 30) — both need voice-pass; BYOC is the time-sensitive one (Tue this week)

## Cross-cutting PM topics (verify still alive at next surface; ≥30 days stale flagged)

- Fresher style/concision/jargon feedback (PM May 10 — likely superseded by subsequent rubric work)
- Conference invitation (PM Apr 24; details never shared)
- "Code-enabled workflow" conversation (PM Apr 24 deferred)
- Larger Comms remit review (PM Apr 24 Step 4)
- Filing system review of comms tree (PM Apr 24 — defer until use-experience accrues)

## Recently-closed (rolling history; trim to last ~14 days)

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
