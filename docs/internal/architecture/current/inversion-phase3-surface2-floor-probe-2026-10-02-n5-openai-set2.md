# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-02 18:21Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category. NOTE (Lead, 2026-10-02 11:0x): 220 rows whose 'phrase' was a whole gate line (a BSD-sed extraction defect in the Lead's shell, not a probe defect) were removed from this file after the run; the remaining rows are the PRIORITY_PATTERNS retro-probe phrases, extracted in Python and valid. The GUIDANCE/STATUS phrases were re-probed in the -set4 reports.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| let's focus on today's priorities | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| let's focus on today's priorities | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| let's focus on today's priorities | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| let's focus on today's priorities | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| let's focus on today's priorities | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| list priorities for the team | 1 | PRIORITY | `list_team_priorities` | 0.9 | openai:gpt-4o |
| list priorities for the team | 2 | PRIORITY | `list_team_priorities` | 0.9 | openai:gpt-4o |
| list priorities for the team | 3 | PRIORITY | `list_team_priorities` | 0.9 | openai:gpt-4o |
| list priorities for the team | 4 | PRIORITY | `list_team_priorities` | 0.9 | openai:gpt-4o |
| list priorities for the team | 5 | PRIORITY | `list_team_priorities` | 0.9 | openai:gpt-4o |
| mark this as priority one | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| mark this as priority one | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| mark this as priority one | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| mark this as priority one | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| mark this as priority one | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| not sure what to do about this | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| not sure what to do about this | 2 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| not sure what to do about this | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| not sure what to do about this | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| not sure what to do about this | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| not sure what to focus next | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| not sure what to focus next | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| not sure what to focus next | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| not sure what to focus next | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| not sure what to focus next | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| should i focus on the bug first | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| should i focus on the bug first | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| should i focus on the bug first | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| should i focus on the bug first | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| should i focus on the bug first | 5 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| show priorities for this sprint | 1 | PRIORITY | `get_sprint_priorities` | 0.95 | openai:gpt-4o |
| show priorities for this sprint | 2 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| show priorities for this sprint | 3 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| show priorities for this sprint | 4 | PRIORITY | `get_sprint_priorities` | 0.95 | openai:gpt-4o |
| show priorities for this sprint | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| this is the highest priority item | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| this is the highest priority item | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| this is the highest priority item | 3 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| this is the highest priority item | 4 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| this is the highest priority item | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| this is top priority for the team | 1 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| this is top priority for the team | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| this is top priority for the team | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| this is top priority for the team | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| this is top priority for the team | 5 | PRIORITY | `set_priority` | 0.9 | openai:gpt-4o |
| what are my critical items | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my critical items | 2 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are my critical items | 3 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are my critical items | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my critical items | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my critical tasks | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my critical tasks | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my critical tasks | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my critical tasks | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my critical tasks | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my current priorities | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my current priorities | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my current priorities | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my current priorities | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my current priorities | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my priorities? | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my priorities? | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my priorities? | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my priorities? | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my priorities? | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my top priorities? | 1 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are my top priorities? | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my top priorities? | 3 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are my top priorities? | 4 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are my top priorities? | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my urgent items | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are my urgent items | 2 | PRIORITY | `get_urgent_items` | 0.95 | openai:gpt-4o |
| what are my urgent items | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my urgent items | 4 | PRIORITY | `get_urgent_items` | 0.95 | openai:gpt-4o |
| what are my urgent items | 5 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what are my urgent tasks | 1 | PRIORITY | `get_urgent_tasks` | 0.95 | openai:gpt-4o |
| what are my urgent tasks | 2 | PRIORITY | `get_urgent_tasks` | 0.95 | openai:gpt-4o |
| what are my urgent tasks | 3 | PRIORITY | `get_urgent_tasks` | 0.95 | openai:gpt-4o |
| what are my urgent tasks | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are my urgent tasks | 5 | PRIORITY | `get_urgent_tasks` | 0.95 | openai:gpt-4o |
| what are the key items on my plate | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key items on my plate | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key items on my plate | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key items on my plate | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key items on my plate | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key priorities this quarter | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are the key priorities this quarter | 2 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are the key priorities this quarter | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are the key priorities this quarter | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what are the key priorities this quarter | 5 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what are the key tasks for this sprint | 1 | PRIORITY | `get_key_tasks` | 0.9 | openai:gpt-4o |
| what are the key tasks for this sprint | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key tasks for this sprint | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key tasks for this sprint | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what are the key tasks for this sprint | 5 | PRIORITY | `get_key_tasks` | 0.9 | openai:gpt-4o |
| what could I focus on | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what could I focus on | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what could I focus on | 3 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what could I focus on | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what could I focus on | 5 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what is my most important work today | 1 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what is my most important work today | 2 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what is my most important work today | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what is my most important work today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what is my most important work today | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what matters most this week | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what matters most this week | 2 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what matters most this week | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what matters most this week | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what matters most this week | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what needs my focus today | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what needs my focus today | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what needs my focus today | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what needs my focus today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what needs my focus today | 5 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what requires attention right now | 1 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what requires attention right now | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what requires attention right now | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what requires attention right now | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what requires attention right now | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I do first | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I do first | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I do first | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I do first | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I do first | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I do next | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I do next | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I do next | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I do next | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I do next | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I focus on today? | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I focus on today? | 2 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what should I focus on today? | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I focus on today? | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I focus on today? | 5 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what should I review first | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I review first | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I review first | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I review first | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I review first | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I tackle next | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I tackle next | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I tackle next | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what should I tackle next | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I tackle next | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I work on next | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I work on next | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I work on next | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I work on next | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what should I work on next | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's critical right now | 1 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what's critical right now | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's critical right now | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's critical right now | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's critical right now | 5 | PRIORITY | `get_top_priority` | 0.9 | openai:gpt-4o |
| what's most important right now | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's most important right now | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's most important right now | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's most important right now | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's most important right now | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my critical work today | 1 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what's my critical work today | 2 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what's my critical work today | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my critical work today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my critical work today | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my most important task right now | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my most important task right now | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my most important task right now | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my most important task right now | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my most important task right now | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my top priority | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my top priority | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my top priority | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my top priority | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my top priority | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my urgent work today | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my urgent work today | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my urgent work today | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my urgent work today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's my urgent work today | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's next for me | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's next for me | 2 | PRIORITY | `get_next_steps` | 0.9 | openai:gpt-4o |
| what's next for me | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's next for me | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's next for me | 5 | PRIORITY | `get_next_task` | 0.9 | openai:gpt-4o |
| what's the most critical thing | 1 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what's the most critical thing | 2 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what's the most critical thing | 3 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what's the most critical thing | 4 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what's the most critical thing | 5 | PRIORITY | `prioritize` | 0.85 | openai:gpt-4o |
| what's the most urgent thing | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's the most urgent thing | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's the most urgent thing | 3 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's the most urgent thing | 4 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's the most urgent thing | 5 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's urgent right now | 1 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's urgent right now | 2 | PRIORITY | `prioritize` | 0.9 | openai:gpt-4o |
| what's urgent right now | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| what's urgent right now | 4 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| what's urgent right now | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should my focus be today | 1 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| where should my focus be today | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should my focus be today | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should my focus be today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should my focus be today | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which project should get my focus today | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which project should get my focus today | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which project should get my focus today | 3 | PRIORITY | `get_top_priority` | 0.95 | openai:gpt-4o |
| which project should get my focus today | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which project should get my focus today | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which task should get my focus next | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which task should get my focus next | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which task should get my focus next | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which task should get my focus next | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| which task should get my focus next | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
