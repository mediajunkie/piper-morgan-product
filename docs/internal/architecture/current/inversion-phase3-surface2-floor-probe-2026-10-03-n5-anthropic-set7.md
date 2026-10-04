# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-03 23:34Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): anthropic:claude-sonnet-4-6

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| what have you learned about my workstyle? | 1 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my workstyle? | 2 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my workstyle? | 3 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my workstyle? | 4 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my workstyle? | 5 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my work style? | 1 | IDENTITY | `get_learned_preferences` | 0.85 | anthropic:claude-sonnet-4-6 |
| what have you learned about my work style? | 2 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my work style? | 3 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my work style? | 4 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| what have you learned about my work style? | 5 | IDENTITY | `get_learned_preferences` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do you know about my work habits | 1 | IDENTITY | `get_user_context` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do you know about my work habits | 2 | IDENTITY | `get_user_context` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do you know about my work habits | 3 | IDENTITY | `get_user_context` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do you know about my work habits | 4 | IDENTITY | `get_user_context` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do you know about my work habits | 5 | IDENTITY | `get_user_context` | 0.85 | anthropic:claude-sonnet-4-6 |
| tell me what you've learned about my habits | 1 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| tell me what you've learned about my habits | 2 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| tell me what you've learned about my habits | 3 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| tell me what you've learned about my habits | 4 | LEARNING | `retrieve_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| tell me what you've learned about my habits | 5 | LEARNING | `get_learned_patterns` | 0.88 | anthropic:claude-sonnet-4-6 |
| what insights do you have about my productivity | 1 | ANALYSIS | `analyze_productivity` | 0.82 | anthropic:claude-sonnet-4-6 |
| what insights do you have about my productivity | 2 | ANALYSIS | `analyze_productivity` | 0.82 | anthropic:claude-sonnet-4-6 |
| what insights do you have about my productivity | 3 | ANALYSIS | `analyze_productivity` | 0.82 | anthropic:claude-sonnet-4-6 |
| what insights do you have about my productivity | 4 | ANALYSIS | `analyze_productivity` | 0.82 | anthropic:claude-sonnet-4-6 |
| what insights do you have about my productivity | 5 | ANALYSIS | `analyze_productivity` | 0.82 | anthropic:claude-sonnet-4-6 |
| show me what you've learned about my preferences | 1 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| show me what you've learned about my preferences | 2 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| show me what you've learned about my preferences | 3 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| show me what you've learned about my preferences | 4 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| show me what you've learned about my preferences | 5 | IDENTITY | `get_learned_preferences` | 0.88 | anthropic:claude-sonnet-4-6 |
| what patterns have you noticed in my work | 1 | LEARNING | `identify_work_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what patterns have you noticed in my work | 2 | LEARNING | `identify_work_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what patterns have you noticed in my work | 3 | LEARNING | `identify_work_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what patterns have you noticed in my work | 4 | LEARNING | `identify_work_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what patterns have you noticed in my work | 5 | LEARNING | `identify_work_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what have you noticed about my habits lately | 1 | ANALYSIS | `analyze_user_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what have you noticed about my habits lately | 2 | ANALYSIS | `analyze_user_patterns` | 0.85 | anthropic:claude-sonnet-4-6 |
| what have you noticed about my habits lately | 3 | ANALYSIS | `analyze_user_patterns` | 0.82 | anthropic:claude-sonnet-4-6 |
| what have you noticed about my habits lately | 4 | ANALYSIS | `analyze_user_patterns` | 0.82 | anthropic:claude-sonnet-4-6 |
| what have you noticed about my habits lately | 5 | ANALYSIS | `analyze_user_patterns` | 0.82 | anthropic:claude-sonnet-4-6 |
