# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-04 19:46Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| pull up my calendar | 1 | TEMPORAL | `meeting_time` | 0.95 | openai:gpt-4o |
| pull up my calendar | 2 | TEMPORAL | `meeting_time` | 0.95 | openai:gpt-4o |
| pull up my calendar | 3 | TEMPORAL | `meeting_time` | 0.95 | openai:gpt-4o |
| pull up my calendar | 4 | TEMPORAL | `show_calendar` | 0.95 | openai:gpt-4o |
| pull up my calendar | 5 | TEMPORAL | `meeting_time` | 0.95 | openai:gpt-4o |
| schedule check for today | 1 | TEMPORAL | `schedule_check` | 0.9 | openai:gpt-4o |
| schedule check for today | 2 | TEMPORAL | `schedule_check` | 0.9 | openai:gpt-4o |
| schedule check for today | 3 | TEMPORAL | `schedule_check` | 0.9 | openai:gpt-4o |
| schedule check for today | 4 | TEMPORAL | `schedule_check` | 0.9 | openai:gpt-4o |
| schedule check for today | 5 | TEMPORAL | `schedule_check` | 0.9 | openai:gpt-4o |
| show all events | 1 | QUERY | `manage_portfolio` | 0.9 | openai:gpt-4o |
| show all events | 2 | QUERY | `manage_portfolio` | 0.9 | openai:gpt-4o |
| show all events | 3 | QUERY | `list_events` | 0.85 | openai:gpt-4o |
| show all events | 4 | QUERY | `list_events` | 0.85 | openai:gpt-4o |
| show all events | 5 | QUERY | `manage_portfolio` | 0.9 | openai:gpt-4o |
| when's my next free slot | 1 | TEMPORAL | `meeting_time` | 0.9 | openai:gpt-4o |
| when's my next free slot | 2 | TEMPORAL | `find_free_slot` | 0.9 | openai:gpt-4o |
| when's my next free slot | 3 | TEMPORAL | `meeting_time` | 0.9 | openai:gpt-4o |
| when's my next free slot | 4 | TEMPORAL | `meeting_time` | 0.9 | openai:gpt-4o |
| when's my next free slot | 5 | TEMPORAL | `meeting_time` | 0.9 | openai:gpt-4o |
| what's my available time | 1 | TEMPORAL | `check_availability` | 0.9 | openai:gpt-4o |
| what's my available time | 2 | TEMPORAL | `check_availability` | 0.9 | openai:gpt-4o |
| what's my available time | 3 | TEMPORAL | `check_availability` | 0.9 | openai:gpt-4o |
| what's my available time | 4 | TEMPORAL | `check_availability` | 0.95 | openai:gpt-4o |
| what's my available time | 5 | TEMPORAL | `meeting_time` | 0.9 | openai:gpt-4o |
| give me a project status report | 1 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| give me a project status report | 2 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| give me a project status report | 3 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| give me a project status report | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a project status report | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| tell me what I'm working on | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| tell me what I'm working on | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| tell me what I'm working on | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| tell me what I'm working on | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| tell me what I'm working on | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| show my active work | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| show my active work | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| show my active work | 3 | STATUS | `show_active_work` | 0.95 | openai:gpt-4o |
| show my active work | 4 | STATUS | `show_active_work` | 0.95 | openai:gpt-4o |
| show my active work | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| just getting started here | 1 | CONVERSATION | `greeting` | 0.9 | openai:gpt-4o |
| just getting started here | 2 | CONVERSATION | `greeting` | 0.9 | openai:gpt-4o |
| just getting started here | 3 | CONVERSATION | `greeting` | 0.9 | openai:gpt-4o |
| just getting started here | 4 | CONVERSATION | `greeting` | 0.85 | openai:gpt-4o |
| just getting started here | 5 | CONVERSATION | `greeting` | 0.8 | openai:gpt-4o |
| is there a conflict on my calendar | 1 | TEMPORAL | `check_conflict` | 0.9 | openai:gpt-4o |
| is there a conflict on my calendar | 2 | TEMPORAL | `check_conflict` | 0.9 | openai:gpt-4o |
| is there a conflict on my calendar | 3 | TEMPORAL | `check_conflict` | 0.9 | openai:gpt-4o |
| is there a conflict on my calendar | 4 | TEMPORAL | `check_calendar_conflict` | 0.9 | openai:gpt-4o |
| is there a conflict on my calendar | 5 | TEMPORAL | `check_conflict` | 0.9 | openai:gpt-4o |
