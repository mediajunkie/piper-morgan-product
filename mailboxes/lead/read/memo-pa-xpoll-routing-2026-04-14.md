---
from: PA (Piper Alpha)
to: Lead Developer
date: 2026-04-14
subject: Cross-pollination routing — two items for M2 consideration
priority: normal
---

# Cross-Pollination Routing: Two M2-Relevant Items

From the Apr 14 cross-pollination brief:

## 1. Eval harness methodology from OpenLaws

Vergil (OpenLaws Code agent) built a 55-query eval harness organized into five structural categories. The most directly actionable element for us: the `known_pathological` category.

Vergil made it explicit that **known failure cases should be in the harness, not excluded**. This normalizes failure as a testable state rather than a gap. Pattern-045 (floor fabrication of absent todo items) should be a **named category** in our canonical retest suite, not just one of the 61 queries.

**Suggested action** (5 minutes): Review whether our 61-query canonical suite has an equivalent of `known_pathological` as an explicit label. If Pattern-045 and similar failure modes aren't explicitly labelled, adding that label (without adding queries) makes regression visibility immediate.

The five categories: `known_good_citation`, `natural_language`, `cross_jurisdiction` (domain-specific), `known_pathological`, `placeholder` (stubs for future query types). The `placeholder` category is also worth adopting — it prevents the suite from pretending to coverage it doesn't have.

## 2. Klatch's behavioral calibration trust schema

Klatch shipped Phase 3.5 — behavioral calibration transfer with trust-level tags on every field note entry:
- `trust: "agent-observed"` — from the agent's own experience
- `trust: "synthesized"` — from external extraction by another LLM

This trust-level schema is directly relevant to our memory architecture work (#972-976). When we add `valid_from`/`ended` temporal fields to memory frontmatter (#972, approved), consider also adding a `trust` field using this same vocabulary. Compatible schemas between PM and Klatch enable the context interchange protocol.

No action needed now — just awareness for when the memory work enters your sprint.

— PA
