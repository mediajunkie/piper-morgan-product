# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-03 23:31Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| what have you learned about my workstyle? | 1 | IDENTITY | `get_workstyle_insights` | 0.85 | openai:gpt-4o |
| what have you learned about my workstyle? | 2 | IDENTITY | `get_workstyle_insights` | 0.85 | openai:gpt-4o |
| what have you learned about my workstyle? | 3 | LEARNING | `learn_workstyle` | 0.8 | openai:gpt-4o |
| what have you learned about my workstyle? | 4 | IDENTITY | `get_workstyle_insight` | 0.85 | openai:gpt-4o |
| what have you learned about my workstyle? | 5 | IDENTITY | `get_workstyle_insights` | 0.85 | openai:gpt-4o |
| what have you learned about my work style? | 1 | LEARNING | `learn_user_work_style` | 0.8 | openai:gpt-4o |
| what have you learned about my work style? | 2 | LEARNING | `understand_work_style` | 0.85 | openai:gpt-4o |
| what have you learned about my work style? | 3 | LEARNING | `learn_work_style` | 0.8 | openai:gpt-4o |
| what have you learned about my work style? | 4 | IDENTITY | `learn_work_style` | 0.85 | openai:gpt-4o |
| what have you learned about my work style? | 5 | LEARNING | `learn_work_style` | 0.85 | openai:gpt-4o |
| what do you know about my work habits | 1 | IDENTITY | `get_work_habits` | 0.85 | openai:gpt-4o |
| what do you know about my work habits | 2 | IDENTITY | `get_work_habits` | 0.85 | openai:gpt-4o |
| what do you know about my work habits | 3 | IDENTITY | `get_work_habits` | 0.85 | openai:gpt-4o |
| what do you know about my work habits | 4 | IDENTITY | `get_work_habits` | 0.85 | openai:gpt-4o |
| what do you know about my work habits | 5 | IDENTITY | `explain_work_habits` | 0.85 | openai:gpt-4o |
| tell me what you've learned about my habits | 1 | LEARNING | `habit_analysis` | 0.85 | openai:gpt-4o |
| tell me what you've learned about my habits | 2 | LEARNING | `analyze_user_habits` | 0.85 | openai:gpt-4o |
| tell me what you've learned about my habits | 3 | LEARNING | `analyze_user_habits` | 0.85 | openai:gpt-4o |
| tell me what you've learned about my habits | 4 | LEARNING | `learn_user_habits` | 0.85 | openai:gpt-4o |
| tell me what you've learned about my habits | 5 | LEARNING | `habit_analysis` | 0.85 | openai:gpt-4o |
| what insights do you have about my productivity | 1 | ANALYSIS | `analyze_productivity` | 0.85 | openai:gpt-4o |
| what insights do you have about my productivity | 2 | ANALYSIS | `analyze_productivity` | 0.85 | openai:gpt-4o |
| what insights do you have about my productivity | 3 | STATUS | `analyze_productivity` | 0.85 | openai:gpt-4o |
| what insights do you have about my productivity | 4 | ANALYSIS | `analyze_productivity` | 0.85 | openai:gpt-4o |
| what insights do you have about my productivity | 5 | STATUS | `get_productivity_insights` | 0.85 | openai:gpt-4o |
| show me what you've learned about my preferences | 1 | IDENTITY | `show_preferences` | 0.85 | openai:gpt-4o |
| show me what you've learned about my preferences | 2 | IDENTITY | `show_preferences` | 0.85 | openai:gpt-4o |
| show me what you've learned about my preferences | 3 | IDENTITY | `show_preferences` | 0.85 | openai:gpt-4o |
| show me what you've learned about my preferences | 4 | IDENTITY | `show_preferences` | 0.9 | openai:gpt-4o |
| show me what you've learned about my preferences | 5 | IDENTITY | `get_preferences` | 0.9 | openai:gpt-4o |
| what patterns have you noticed in my work | 1 | LEARNING | `pattern_analysis` | 0.85 | openai:gpt-4o |
| what patterns have you noticed in my work | 2 | LEARNING | `identify_patterns` | 0.85 | openai:gpt-4o |
| what patterns have you noticed in my work | 3 | LEARNING | `pattern_analysis` | 0.8 | openai:gpt-4o |
| what patterns have you noticed in my work | 4 | LEARNING | `identify_patterns` | 0.8 | openai:gpt-4o |
| what patterns have you noticed in my work | 5 | LEARNING | `pattern_analysis` | 0.8 | openai:gpt-4o |
| what have you noticed about my habits lately | 1 | LEARNING | `habit_analysis` | 0.85 | openai:gpt-4o |
| what have you noticed about my habits lately | 2 | LEARNING | `habit_analysis` | 0.8 | openai:gpt-4o |
| what have you noticed about my habits lately | 3 | LEARNING | `analyze_habits` | 0.85 | openai:gpt-4o |
| what have you noticed about my habits lately | 4 | LEARNING | `habit_analysis` | 0.85 | openai:gpt-4o |
| what have you noticed about my habits lately | 5 | LEARNING | `habit_analysis` | 0.8 | openai:gpt-4o |
