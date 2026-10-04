# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-04 19:50Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): anthropic:claude-sonnet-4-6

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| pull up my calendar | 1 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| pull up my calendar | 2 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| pull up my calendar | 3 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| pull up my calendar | 4 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| pull up my calendar | 5 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| schedule check for today | 1 | TEMPORAL | `meeting_time` | 0.9 | anthropic:claude-sonnet-4-6 |
| schedule check for today | 2 | TEMPORAL | `meeting_time` | 0.9 | anthropic:claude-sonnet-4-6 |
| schedule check for today | 3 | TEMPORAL | `meeting_time` | 0.9 | anthropic:claude-sonnet-4-6 |
| schedule check for today | 4 | TEMPORAL | `meeting_time` | 0.9 | anthropic:claude-sonnet-4-6 |
| schedule check for today | 5 | TEMPORAL | `meeting_time` | 0.9 | anthropic:claude-sonnet-4-6 |
| show all events | 1 | TEMPORAL | `meeting_time` | 0.72 | anthropic:claude-sonnet-4-6 |
| show all events | 2 | TEMPORAL | `meeting_time` | 0.72 | anthropic:claude-sonnet-4-6 |
| show all events | 3 | TEMPORAL | `meeting_time` | 0.72 | anthropic:claude-sonnet-4-6 |
| show all events | 4 | TEMPORAL | `meeting_time` | 0.72 | anthropic:claude-sonnet-4-6 |
| show all events | 5 | TEMPORAL | `list_events` | 0.72 | anthropic:claude-sonnet-4-6 |
| when's my next free slot | 1 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| when's my next free slot | 2 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| when's my next free slot | 3 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| when's my next free slot | 4 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| when's my next free slot | 5 | TEMPORAL | `meeting_time` | 0.92 | anthropic:claude-sonnet-4-6 |
| what's my available time | 1 | TEMPORAL | `meeting_time` | 0.85 | anthropic:claude-sonnet-4-6 |
| what's my available time | 2 | TEMPORAL | `meeting_time` | 0.88 | anthropic:claude-sonnet-4-6 |
| what's my available time | 3 | TEMPORAL | `meeting_time` | 0.88 | anthropic:claude-sonnet-4-6 |
| what's my available time | 4 | TEMPORAL | `meeting_time` | 0.88 | anthropic:claude-sonnet-4-6 |
| what's my available time | 5 | TEMPORAL | `meeting_time` | 0.88 | anthropic:claude-sonnet-4-6 |
| give me a project status report | 1 | STATUS | `get_project_status` | 0.85 | anthropic:claude-sonnet-4-6 |
| give me a project status report | 2 | STATUS | `get_project_status` | 0.85 | anthropic:claude-sonnet-4-6 |
| give me a project status report | 3 | STATUS | `get_project_status` | 0.85 | anthropic:claude-sonnet-4-6 |
| give me a project status report | 4 | STATUS | `get_project_status` | 0.85 | anthropic:claude-sonnet-4-6 |
| give me a project status report | 5 | STATUS | `get_project_status` | 0.85 | anthropic:claude-sonnet-4-6 |
| tell me what I'm working on | 1 | STATUS | `get_project_status` | 0.95 | anthropic:claude-sonnet-4-6 |
| tell me what I'm working on | 2 | STATUS | `get_project_status` | 0.95 | anthropic:claude-sonnet-4-6 |
| tell me what I'm working on | 3 | STATUS | `get_project_status` | 0.95 | anthropic:claude-sonnet-4-6 |
| tell me what I'm working on | 4 | STATUS | `get_project_status` | 0.95 | anthropic:claude-sonnet-4-6 |
| tell me what I'm working on | 5 | STATUS | `get_project_status` | 0.95 | anthropic:claude-sonnet-4-6 |
| show my active work | 1 | STATUS | `get_project_status` | 0.92 | anthropic:claude-sonnet-4-6 |
| show my active work | 2 | STATUS | `get_project_status` | 0.92 | anthropic:claude-sonnet-4-6 |
| show my active work | 3 | STATUS | `get_project_status` | 0.92 | anthropic:claude-sonnet-4-6 |
| show my active work | 4 | STATUS | `get_project_status` | 0.92 | anthropic:claude-sonnet-4-6 |
| show my active work | 5 | STATUS | `get_project_status` | 0.92 | anthropic:claude-sonnet-4-6 |
| just getting started here | 1 | CONVERSATION | `greeting` | 0.9 | anthropic:claude-sonnet-4-6 |
| just getting started here | 2 | CONVERSATION | `greeting` | 0.9 | anthropic:claude-sonnet-4-6 |
| just getting started here | 3 | CONVERSATION | `greeting` | 0.9 | anthropic:claude-sonnet-4-6 |
| just getting started here | 4 | CONVERSATION | `greeting` | 0.9 | anthropic:claude-sonnet-4-6 |
| just getting started here | 5 | CONVERSATION | `greeting` | 0.9 | anthropic:claude-sonnet-4-6 |
| is there a conflict on my calendar | 1 | TEMPORAL | `check_calendar_conflicts` | 0.92 | anthropic:claude-sonnet-4-6 |
| is there a conflict on my calendar | 2 | TEMPORAL | `check_calendar_conflicts` | 0.92 | anthropic:claude-sonnet-4-6 |
| is there a conflict on my calendar | 3 | TEMPORAL | `check_calendar_conflicts` | 0.92 | anthropic:claude-sonnet-4-6 |
| is there a conflict on my calendar | 4 | TEMPORAL | `check_calendar_conflicts` | 0.92 | anthropic:claude-sonnet-4-6 |
| is there a conflict on my calendar | 5 | TEMPORAL | `check_calendar_conflicts` | 0.92 | anthropic:claude-sonnet-4-6 |
