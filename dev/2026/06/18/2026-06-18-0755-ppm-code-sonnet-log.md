# Session Log: 2026-06-18-0755-ppm-code-sonnet

**Role**: Principal Product Manager (PPM)
**Tool**: Claude Code · **Model**: Sonnet 4.6 · **Worktree/branch**: `claude/pensive-kepler-02a0f6` (Option B ephemeral — correct)
**Account**: DinP (xian@designinproduct.com) — migration session (Opus→Sonnet)
**Date**: Thursday, June 18, 2026
**Start**: 07:55 PDT — fresh migration session
**Prior session**: `dev/2026/06/18/2026-06-18-0621-ppm-code-opus-log.md` (DAY-CLOSED; all deliverables on origin/main)

## START

Migration session: Opus account → DinP account, model Opus→Sonnet. Option B ephemeral worktree `claude/pensive-kepler-02a0f6`. Prior Opus session fully closed.

**Inbox at START**: 2
- `memo-lead-to-ppm-cc-pm-1240-phase0-no-people-source-pick-the-beta-source-2026-06-18.md` — HIGH: #1240 Phase-0 STOP, no people source exists; pick beta source (or defer post-beta). Response requested.
- `memo-exec-to-cohort-escalations-docs-deprecated-stop-maintaining-2026-06-18.md` — Standard: escalations docs deprecated; stop maintaining `duty-cycle-escalations-ppm.md`. No reply needed.

**Fire-0 deliverable send-state inherited (from Opus session)**:
All 4 Fire-0 deliverables from the Opus session fully sent and on origin/main:
- People entity-model (RadarEntity contract) → Lead ✅
- Trust-model sweep + #1270 ArtifactSourceType reconcile → Lead + CXO ✅
- #1269 standup data model → Lead + CXO ✅
- Inbox race condition analysis → CIO ✅
No unsent memos owed.

## Work Log

### Fire 0 — 07:55 PDT (START — DinP migration)

#### Mailbox sweep

**Exec cohort notice** (escalations docs deprecated): Acknowledged. Stop maintaining `dev/active/duty-cycle-escalations-ppm.md`. Carry-forward + mail are the homes now. No reply needed.

**Lead #1240 Phase-0 STOP** (People source): High priority — needs PPM decision. Analysis below.

#### People-source decision (#1240)

Lead's Phase-0 finding: no source exists matching the People entity-model. Four options offered (session extraction / introduce-person flow / GitHub-derived / defer post-beta). Lead explicitly flagged option 4 (defer) as a PM milestone/partial-ship call.

**PPM recommendation: Option 4 — Defer People entity model to post-beta.**

Rationale:
1. **No source to build against**: Options 1 (session extraction) and 2 (introduce-person flow) both require new extraction infrastructure or a new intent/UI flow. With M4→RECONNECT→M5 remaining and Jul 4 as the hard deadline, there's no sprint slot for this work.
2. **Option 3 (GitHub-derived) creates model debt**: `github_collaborator` is not in the People entity-model spec and narrows the concept to "people who touched your repo" — wrong scope. Post-beta we'd need to reconcile the model deviation. The expedience buys little; the debt is real.
3. **3-of-4 is a strong beta story**: Documents, WorkItems, and Conversations are the core daily-use cases for Piper's beta value proposition. People is additive but not central to the Jul 4 0.9.0 beta MVP claim.
4. **The spec is complete and ready for 1.0**: People entity-model is fully designed (lifecycle states, provenance mapping, meta fields). This is a timing deferral, not a design gap — 1.0 picks it up with a proper source.

Routing to PM for milestone/partial-ship confirmation (Lead explicitly flagged this). Memo sent to Lead + cc PM.

