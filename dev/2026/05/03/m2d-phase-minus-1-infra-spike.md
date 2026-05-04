# M2d Phase -1 Infrastructure Spike — 2026-05-03

**Author**: Lead Developer (Claude Code Opus)
**Purpose**: Pre-gameplan infrastructure verification across the 6 M2d implementation issues (#704, #714, #1030, #1031, #1032, #1033). Per gameplan-template v9.3 Phase -1 ("Infrastructure Verification Checkpoint") — done once across the cohort rather than re-investigated per gameplan.

---

## Summary of findings

| Surface | Existence | State | Gap-shape relevant to gameplans |
|---------|-----------|-------|---------------------------------|
| Insight model + `SurfaceableInsight` class | ✅ Exists | `services/mux/composting_pipeline.py:35` | Persistence pattern same as pre-#1018 audit_transparency: in-memory `Dict[str, SurfaceableInsight]` (line 185). |
| `InsightJournal` class | ✅ Exists | `services/mux/composting_pipeline.py:171` | In-memory only. No repository, no DB schema, no migration. |
| `CompostingPipeline` class | ✅ Exists | `services/mux/composting_pipeline.py:400` | Logic complete; needs to be invoked. |
| `CompostingScheduler` class | ✅ Exists | `services/mux/composting_scheduler.py:153` | Logic complete; "filing dreams" framing baked in (line 39+). |
| `COMPOSTING_FRAMES` framing constants | ✅ Exists | `services/mux/composting_scheduler.py:39-47` | "Having had some time to reflect..." / "Looking back at our work together..." / etc. — exactly what #1033 calls for. |
| **Composting wired into startup/scheduler** | ❌ NOT WIRED | — | Nothing in `web/startup.py` or `services/scheduler/` references CompostingScheduler or CompostingPipeline. The classes exist; they don't run. |
| **Insight persistence to DB** | ❌ MISSING | — | InsightJournal storage is `Dict[str, SurfaceableInsight] = {}` — same shape as pre-#1018 audit log. Process restart = full insight loss. |
| `LifecycleState` enum + `lifecycle_state` field on WorkItem/Feature/Project/Todo | ✅ Exists | `services/domain/models.py:217, 287, 441, 1451` | Backend ready. |
| Lifecycle indicator components | ✅ Built | `templates/components/lifecycle_indicator.html` (8.9KB), `lifecycle_detail.html` (10.6KB), `lifecycle_notification.html` (7.3KB) | `LifecycleIndicator.create()` JS API at line 297. |
| `templates/standup.html` | ✅ Exists | 10.1KB, last touched Mar 24 | Renders `standup.yesterday_accomplishments`, `today_priorities`, `blockers` as `<li>${item}</li>`. |
| **`StandupResult.yesterday_accomplishments`** | ⚠️ **String list, not WorkItem list** | `services/features/morning_standup.py:51` (`List[str]`) | Pipeline pre-formats: `yesterday_accomplishments.append(f"✅ {commit.get('message', '')}")` and `f"📋 {work}"`. **Template-only wiring cannot surface `lifecycle_state` because the structured WorkItem is gone by the time it reaches the template.** |
| `templates/lists.html` | ✅ Exists | 28.2KB | Substantial template; phase-0 of #714 needs to read this carefully before designing. |
| Lists API endpoint | ✅ Exists | `services/api/todo_management.py:644` (`GET /lists`), :548 (`/lists/{list_id}`), etc. | Routes exist on `todo_management_router`. |
| `/insights` UI route + template | ✅ EXISTS | `web/api/routes/ui.py:349` + `templates/insights.html` (20.3KB) | **Built under #424 MUX-IMPLEMENT-COMPOST (closed Jan 2026)**. The Insight Journal navigation surface that #1031 calls for is partly already there — needs assessment of what's wired vs scaffold. |
| Trust stage API | ✅ Wired | `services/trust/trust_computation_service.py:118` `get_trust_stage(user_id) -> TrustStage`; used in `services/intent/intent_service.py:577` | Backend ready for trust-gating on Push (#1032). |
| `TrustStage` enum | ✅ Exists | `services/shared_types.py:333` (`IntEnum` with stages 1-4) | |

---

## Gap-shapes that affect gameplan scope

### Gap A: #704 standup wiring is bigger than the issue assumes

**The issue body** says "compact indicator, JS render when `lifecycle_state` present, template tests" — implying the template just needs to call `LifecycleIndicator.create(item.lifecycle_state, true)` per item.

**The reality**: `StandupResult` exposes `yesterday_accomplishments: List[str]` and `today_priorities: List[str]`. The standup pipeline at `services/features/morning_standup.py:213-234` formats WorkItems into pre-rendered strings (`f"✅ {commit.message}"`, `f"📋 {work}"`) before they reach the API response. There is no path for `lifecycle_state` to reach the template under the current pipeline.

**Implication**: #704 is either:
- **(a)** A larger issue than its current body suggests — needs `StandupResult` schema change to carry structured items + API contract update + template wiring.
- **(b)** Scope-trimmed to "lifecycle indicator on a different surface where WorkItems flow through structured" (e.g., `/items` page, or wherever WorkItems are listed with `to_dict()`).
- **(c)** Pre-work issue: "Standup pipeline carries structured WorkItems through to API response" filed first; #704 then becomes the wiring step.

**My recommendation**: option (c) — file the pre-work as a new issue, keep #704 scoped to template wiring once items flow through structured. PM call.

### Gap B: Composting pipeline classes exist but don't run

`CompostingPipeline`, `CompostingScheduler`, `CompostBin`, `InsightJournal` all exist in `services/mux/`. None of them are referenced from `web/startup.py`, `services/scheduler/`, or `services/api/`. Process startup does not register a composting cycle.

**Implication for #1033**: #1033's Phase 0 STOP condition ("If pipeline doesn't exist, STOP and surface as blocker") is not strictly met — the pipeline *exists*, but it isn't *running*. The work to wire the existing scheduler into startup is real and substantial; comparable to the wiring work `EthicsAuditCleanupPhase` did in #1018 Phase 2.

**Implication for #1030/#1031**: those issues assume insights exist when the user queries / browses. Without composting running, the Insight Journal will be empty.

**Recommendation**: factor a shared "composting pipeline activation" pre-work issue. Could be:
- New issue: "Wire CompostingScheduler into web/startup.py phases + persist InsightJournal to DB" (parallel to #1018's pattern)
- Then #1030/#1031/#1032/#1033 can assume composting + insight persistence are live.

This is also a P0 strategic consideration — without composting running, no insights ever exist, regardless of how well Pull/Passive/Push are implemented. Worth surfacing to PM before drafting four gameplans that all sit on top of it.

### Gap C: #1031 (Passive mode) may already be partly done

`templates/insights.html` (20KB) was built under #424 MUX-IMPLEMENT-COMPOST (closed Jan 2026) and `/insights` route is live. The audit-cascade May 2 didn't surface this because the question framed was "split #707 — what's the work?" rather than "what already exists?".

**Implication**: #1031's "Insight Journal UI page" is largely scaffolded. The actual work may be:
- Wire to a real insight-listing endpoint (vs. stub data, if that's what's there)
- Add correction / explanation / source-inquiry affordances per spec
- Integrate with the (currently in-memory) InsightJournal

**Recommendation**: Phase 0 of #1031's gameplan should be a careful read of `templates/insights.html` + any existing endpoints that back it. Could meaningfully shrink the issue.

### Gap D: Lists model DB schema vs. domain model split

Lists exist in two places:
- `services/domain/models.py:1250` `class List` (domain dataclass)
- `services/database/models.py:1494` `class ListItemDB` (DB model for items)

**Implication for #714**: Phase 0 needs to verify which model is the system-of-record for List timestamps the staleness signal will read from. If staleness needs to read both List metadata + ListItem activity, the join across these two layers is part of the design.

---

## What's GREEN for gameplan-writing

These can proceed without further investigation:

- **Lifecycle indicator component + JS API** — built, tested under #423, ready to use.
- **WorkItem/Feature/Project/Todo `to_dict()` includes `lifecycle_state`** — confirmed across multiple models (#705 closed, #708/#709 reference comments suggest similar wiring done for Todo + Project).
- **Trust-stage API** — wired and used in production code (`intent_service.py:577`); reading `TrustStage` from `user_id` is solved.
- **Insights UI route exists** — `/insights` returns `templates/insights.html`.
- **`COMPOSTING_FRAMES` framing constants** — match the spec verbatim; #1033's Phase 1 surfacing-path work has the framing list already in code.

---

## Questions for PM (before drafting gameplans)

1. **Gap A — #704 scope**: scope-trim, file pre-work, or expand #704? My lean: file pre-work issue; keep #704 small.
2. **Gap B — composting activation**: file as a single shared pre-work issue, or fold the wiring into each of #1030/#1031/#1032/#1033 individually? My lean: single shared pre-work — this is foundation, not feature.
3. **Gap C — #1031 prior art**: should #1031's scope be re-read against what `templates/insights.html` already does before drafting its gameplan? My lean: yes, half-hour read could meaningfully shrink the issue.

If the answers are roughly "file pre-work for A and B; verify before drafting C": I'd file two new issues today (a "standup pipeline structured items" + "composting pipeline activation"), then resume gameplan-drafting with cleaner foundations under each issue.

---

## Files referenced in this spike

- `services/mux/composting_pipeline.py` (CompostingPipeline, InsightJournal, SurfaceableInsight)
- `services/mux/composting_scheduler.py` (CompostingScheduler, COMPOSTING_FRAMES)
- `services/mux/compost_bin.py` (CompostBin, meets_composting_criteria)
- `services/mux/composting_models.py` (CompostingTrigger, ExtractedLearning, Insight)
- `services/mux/lifecycle.py` (LifecycleState enum, CompostingExtractor)
- `services/features/morning_standup.py` (StandupResult — line 45+)
- `services/domain/models.py` (List, WorkItem, Feature, Project, Todo lifecycle_state)
- `services/database/models.py` (ListItemDB)
- `services/api/todo_management.py` (Lists endpoints)
- `services/trust/trust_computation_service.py` (get_trust_stage)
- `services/intent/intent_service.py:577` (trust API consumer)
- `services/shared_types.py:333` (TrustStage enum)
- `web/api/routes/ui.py:282, 349` (standup, insights UI routes)
- `web/api/routes/standup.py` (standup API + StandupResponse schema)
- `web/startup.py` (phase registry — does NOT include composting)
- `templates/standup.html`, `templates/lists.html`, `templates/insights.html`
- `templates/components/lifecycle_*.html`

---

## Standing observations

- The same architectural anti-pattern that #1018 fixed (persistent state held in-memory in a service class) shows up again in `InsightJournal._insights: Dict[str, SurfaceableInsight] = {}`. Pattern-049 (Audit Cascade) caught it at the issue-audit phase rather than the gameplan-execute phase, which is the early catch we want.
- The composting infrastructure is impressively complete in code-not-running form. Someone built CompostingScheduler with quiet-hours configuration and reflection framing constants — the *behavior* spec is realized; the *deployment* isn't. The pattern of "build the box, leave the wiring to a follow-up" shows up repeatedly in MUX work; worth surfacing as a methodology observation if it's a recurring shape.
