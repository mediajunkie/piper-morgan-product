# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-02 14:29Z · 3 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a FLOOR-destination row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

| phrase | sample | surface-2 category | surface-2 action | confidence |
|---|---|---|---|---|
| what are my focus areas this sprint | 1 | PRIORITY | `get_focus_areas` | 0.95 |
| what are my focus areas this sprint | 2 | PRIORITY | `get_focus_areas` | 0.95 |
| what are my focus areas this sprint | 3 | PRIORITY | `get_focus_areas` | 0.95 |
| what's my focus this week | 1 | PRIORITY | `prioritize` | 0.95 |
| what's my focus this week | 2 | PRIORITY | `get_top_priority` | 0.95 |
| what's my focus this week | 3 | PRIORITY | `prioritize` | 0.95 |
| I could use some guidance on this | 1 | GUIDANCE | `provide_guidance` | 0.85 |
| I could use some guidance on this | 2 | GUIDANCE | `provide_guidance` | 0.85 |
| I could use some guidance on this | 3 | GUIDANCE | `provide_guidance` | 0.85 |
| do you have a recommendation | 1 | GUIDANCE | `provide_guidance` | 0.8 |
| do you have a recommendation | 2 | GUIDANCE | `provide_recommendation` | 0.85 |
| do you have a recommendation | 3 | GUIDANCE | `provide_recommendation` | 0.85 |
| what's your advice here | 1 | GUIDANCE | `provide_guidance` | 0.85 |
| what's your advice here | 2 | GUIDANCE | `provide_guidance` | 0.8 |
| what's your advice here | 3 | GUIDANCE | `provide_guidance` | 0.85 |
| ok that's merged, what now? | 1 | GUIDANCE | `provide_guidance` | 0.85 |
| ok that's merged, what now? | 2 | GUIDANCE | `provide_guidance` | 0.85 |
| ok that's merged, what now? | 3 | GUIDANCE | `next_steps_guidance` | 0.85 |
