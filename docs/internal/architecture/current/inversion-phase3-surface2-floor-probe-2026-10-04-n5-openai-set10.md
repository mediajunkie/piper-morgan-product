# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-04 23:12Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| unlink octocat/hello-world from my project | 1 | EXECUTION | `unlink_project` | 0.9 | openai:gpt-4o |
| unlink octocat/hello-world from my project | 2 | EXECUTION | `unlink_project` | 0.9 | openai:gpt-4o |
| unlink octocat/hello-world from my project | 3 | EXECUTION | `unlink_project` | 0.85 | openai:gpt-4o |
| unlink octocat/hello-world from my project | 4 | EXECUTION | `unlink_github_project` | 0.9 | openai:gpt-4o |
| unlink octocat/hello-world from my project | 5 | EXECUTION | `unlink_project` | 0.9 | openai:gpt-4o |
| remove mediajunkie/piper-morgan from the Piper Morgan project | 1 | EXECUTION | `remove_project_association` | 0.9 | openai:gpt-4o |
| remove mediajunkie/piper-morgan from the Piper Morgan project | 2 | EXECUTION | `remove_project_association` | 0.9 | openai:gpt-4o |
| remove mediajunkie/piper-morgan from the Piper Morgan project | 3 | EXECUTION | `remove_project_link` | 0.9 | openai:gpt-4o |
| remove mediajunkie/piper-morgan from the Piper Morgan project | 4 | EXECUTION | `remove_project_association` | 0.9 | openai:gpt-4o |
| remove mediajunkie/piper-morgan from the Piper Morgan project | 5 | EXECUTION | `remove_project_association` | 0.9 | openai:gpt-4o |
| disconnect octocat/hello-world from Atlas | 1 | EXECUTION | `disconnect_repository` | 0.85 | openai:gpt-4o |
| disconnect octocat/hello-world from Atlas | 2 | EXECUTION | `disconnect_repository` | 0.9 | openai:gpt-4o |
| disconnect octocat/hello-world from Atlas | 3 | EXECUTION | `disconnect_repository` | 0.85 | openai:gpt-4o |
| disconnect octocat/hello-world from Atlas | 4 | EXECUTION | `disconnect_repository` | 0.85 | openai:gpt-4o |
| disconnect octocat/hello-world from Atlas | 5 | EXECUTION | `disconnect_repository` | 0.85 | openai:gpt-4o |
