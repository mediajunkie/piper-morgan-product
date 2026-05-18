---
from: Lead Developer
to: CEO (xian)
cc: Architect (Chief Architect), CIO (Chief Innovation Officer), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: Audit-cascade revisit on demand-gated cluster — per PM "I am the demand" reframe; reset body language to MVP-committed; per-issue sub-sprint disposition asks
priority: low — audit-cascade discipline; revises issue bodies to reflect current reality
response-requested: per-issue M2 sub-sprint disposition (M2g / later M2 sub-sprint / break out / close as obsolete)
in-reply-to: memo-lead-to-ceo-cc-arch-host-cio-exec-pa-demand-gated-cluster-1080-1085-1089-triage-2026-05-17.md
---

# Audit-cascade revisit — demand-gated cluster after PM "I am the demand" reframe

PM clarification this morning (~14:00 PT):
- Descriptions are conditional at filing; audit-cascade revises them
- The MVP-roadmap commitment IS the demand signal — alpha-user retroactive validation is a different (additional, not primary) signal
- *"I am the demand, lol"* — PM provides the demand for MVP-committed work

This memo applies audit-cascade discipline to the 5 issues that carry "demand-gated" body language but are MVP+M2 sprint per the Project Board. Each gets a proposed body revision + a sub-sprint disposition ask.

The cluster (with current state):

| # | Title | Milestone | Sprint | M2g? | Priority | Body framing today |
|---|---|---|---|---|---|---|
| 1080 | NOTION-WRITE: Activate update_document | MVP | M2 | no | low | "demand-gated"; "leave dormant; recovery cost zero" |
| 1081 | NOTION-SLACK-XREF: Verify Slack→Notion cross-references | MVP | M2 | no | low | "(demand-gated)" in title |
| 1085 | CONTEXT-ACTIVITY-SLACK: Slack source to recent-activity | MVP | M2 | no | low | "(demand-gated)" in title + body |
| 1086 | CONTEXT-ACTIVITY-CAL: calendar source to recent-activity | MVP | M2 | no | low | "(demand-gated)" in title + body |
| 1089 | KG-PRIVACY-FILTER: real privacy filtering on KG nodes | MVP | M2 | **yes** | low | "Trigger conditions for shipping" framing |

## What "audit-cascade revisit" means here

For each issue: drop the "ship-when-triggered / demand-gated" framing from the body language (it was conditional-at-filing). Restate as MVP-committed. Surface what's actually outstanding for shipment + propose where in M2 (which sub-sprint) it lands.

I won't edit the bodies until you ratify the dispositions below — but the proposed revisions are concrete enough to apply if you say "approved."

## Per-issue dispositions

### #1080 NOTION-WRITE — Activate update_document

**Current body framing**: "Recovery cost is zero: code stays in tree, gated by USE_SPATIAL_NOTION flag. Activating later costs the same as activating now (~1-2 hr Lead Dev + ~30-60 min PM write smoke)."

**Audit-cascade reality**: 
- Code is fully in tree (router + handler + adapter)
- PM-manual gate: integration token write-scope confirmation
- Cost to activate: ~1-2 hr Lead Dev + PM token-scope step + smoke

**Proposed disposition**: **promote to M2g**; activate this sprint. Concrete path:
- You confirm/widen the write-scope on the Notion integration token (PM-manual)
- Lead Dev flips `USE_SPATIAL_NOTION` flag + verifies write path
- Live smoke against your Notion workspace (you drive; Lead Dev observes for bugs)
- Update `services/integrations/notion/README.md` with write-capability note

**Proposed body revision**: drop "demand-gated" + "Trigger conditions" sections; restate as "Implementation path (when scheduled)" with the 3 steps above.

### #1081 NOTION-SLACK-XREF — Verify Slack→Notion cross-references

**Current body framing**: "(demand-gated)" in title.

**Audit-cascade reality**: this is a verification task contingent on #1080 activation. Once #1080 ships, this becomes "spend ~30-60 min checking that cross-refs render."

**Proposed disposition**: **promote to M2g, blocked-by #1080**. Treat as the verification-pass after #1080 lands. If #1080 stays unscheduled, #1081 stays parked.

**Proposed body revision**: drop "demand-gated"; add "Blocked by #1080 activation; verification pass once that lands."

### #1085 CONTEXT-ACTIVITY-SLACK — Slack source to recent-activity

**Current body framing**: "(demand-gated)"; "Recovery cost zero: when demand surfaces, the recent_activity helper can extend the source list trivially."

**Audit-cascade reality**:
- No code yet
- Building requires: new aggregator helper analogous to GitHub's `_compute_recent_activity` + schema unification (extend `recent_activity` items with `source: 'slack'|'github'`) + fail-graceful per-source + tests
- Cost: ~4-6 hr Lead Dev

**Proposed disposition**: **promote to M2g, but break into 2 chips**:
- Slice 1: schema unification (add `source` field; refactor GitHub case to use it) — ~1 hr; bounded
- Slice 2: Slack source aggregator + tests — ~3-5 hr

Slice 1 alone lets #1086 (Calendar) follow the same pattern cheaply. Slice 2 is the actual Slack lift.

**Proposed body revision**: drop "demand-gated"; restate as a 2-slice implementation plan; cross-ref #1086 as same-shape.

### #1086 CONTEXT-ACTIVITY-CAL — calendar source to recent-activity

**Current body framing**: "(demand-gated)" in title.

**Audit-cascade reality**: same shape as #1085 (different source). Once #1085 slice 1 (schema unification) lands, calendar source is a ~2-3 hr add following the established pattern.

**Proposed disposition**: **promote to M2g, blocked-by #1085 slice 1** (schema unification). Lands cheaply after that.

**Proposed body revision**: drop "demand-gated"; add "Blocked by #1085 slice 1; pattern-follow once schema unifies."

### #1089 KG-PRIVACY-FILTER — Real privacy filtering

**Current body framing**: "Trigger conditions" + "Ship this when..."

**Audit-cascade reality**:
- Design substrate **substantially complete** (Architect Q3+Q4 ratified `73cf571b5`; HOST Q2 ratified with `filter_reason` enum refinement)
- Only outstanding: CIO Q5 (Pattern-073 numbering — held per your direction); PM Q1 (this disposition)
- Cost to implement: multi-day per the Phase 0 memo

**Proposed disposition**: **stays M2g** (already labeled); restate as **MVP-committed, scheduled when CIO Q5 lands + Lead Dev capacity allows after #1080+#1081+#1085+#1086 cluster work**. The defense-in-depth value grows with KG-write surface area (which #1080+#1085 expand).

**Proposed body revision**: drop "Trigger conditions for un-deferring"; restate as "Implementation phase (when scheduled)" with the Architect Q3/Q4 + HOST Q2 ratified design as the blueprint section.

## Summary disposition table (Lead Dev proposed)

| # | Current | Proposed |
|---|---|---|
| 1080 | Unlabeled M2, demand-gated framing | **M2g**; PM token-scope step + flag-flip + smoke |
| 1081 | Unlabeled M2, demand-gated framing | **M2g, blocked-by #1080** |
| 1085 | Unlabeled M2, demand-gated framing | **M2g**, 2 slices (schema-unify + Slack aggregator) |
| 1086 | Unlabeled M2, demand-gated framing | **M2g, blocked-by #1085 slice 1** |
| 1089 | M2g, trigger-conditions framing | **stays M2g**; implement after #1080-1086 cluster + CIO Q5 |

## Sequencing if you ratify

Most-bounded-first chain:
1. **#1080** (your token-scope step gates start)
2. **#1081** (post-#1080 verification pass)
3. **#1085 slice 1** (schema unification) — Lead Dev does standalone
4. **#1086** (uses #1085 slice 1)
5. **#1085 slice 2** (Slack source aggregator)
6. **#1089** (after CIO Q5; Lead Dev capacity check)

Total: ~3-5 working days for the cluster if all run sequential.

## What this memo IS

- Audit-cascade revision proposal for 5 issues that share the demand-gated body framing
- Per-issue sub-sprint disposition (M2g across the board)
- Sequencing plan with blocked-by relationships named
- Cost estimates for each

## What this memo is NOT

- Not editing the issue bodies yet — waiting for ratification
- Not asking PM to do the token-scope step today — that's a "when scheduled" PM-manual step
- Not gating other Lead Dev work — memory-layer Phase 0 audit memo (per your (3) directive) coming next

## Cross-references

- Original demand-gated cluster triage: `mailboxes/lead/sent/memo-lead-to-ceo-cc-arch-host-cio-exec-pa-demand-gated-cluster-1080-1085-1089-triage-2026-05-17.md`
- M-sprint backlog snapshot v2: `dev/active/M-backlog-snapshot-2026-05-17-v2.md`
- #1089 Phase 0 design memo: `ef8db4168`
- Architect Q3+Q4 reply: `73cf571b5` (in lead/read)
- HOST Q2 reply with `filter_reason` enum: `73cf571b5` (in lead/read)

— Lead Developer, 2026-05-17 14:20 PT
