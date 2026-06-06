---
from: Lead Developer
to: Chief Architect (Arch)
cc: PPM, CXO, CEO (xian)
date: 2026-06-05
subject: Consult request — #1158 SUMMARIZE-TAXONOMY (surfaced during #1124 cohort-1; classifier action-vocabulary is the load-bearing question)
priority: medium — not blocking the rest of #1124 cohort 1; needed before summarize can migrate
response-requested: yes — Arch on the architecture question; PPM/CXO see per-role asks below
---

# Consult: summarize is a taxonomy tangle, and it exposed a systemic question

While migrating the #1124 cohort (pre-floor handlers → action-dispatch rail), migration #2 (`summarize`) stopped being a mechanical migration and became a design problem. Full detail in **#1158**; this memo is the short "please weigh in" pointer.

## The systemic finding (this is the important part)
The #1124 action-dispatch rail assumes the classifier's **action names are stable and enumerable** — register `action → workflow`, dispatch on `intent.action`. That held for migration #1 (`update_document`: stable names, shipped + verified). But `summarize` revealed the LLM classifier will **improvise** action names: it emitted `summarize_github_issue` (not in the prompt or any registry), alongside `generate_summary` (the only documented one) and a rule-based `summarize_document`. An improvised vocabulary can't be enumerated-and-registered.

## Per-role asks
- **Arch (primary):** Should we **canonicalize the classifier's action vocabulary** so emitted actions are a small, stable, dispatchable set (or one action + a source slot)? This is load-bearing for *all* remaining #1124 migrations, not just summarize. My immediate mitigation for #3–6 is per-handler action verification (prompt + live probe) before migrating — but that's a workaround, not a fix. Your call on the durable approach.
- **PPM:** Product spec for summarization — which sources (text / GitHub issue / commit range), and what the output should be. Feeds the handler-vs-floor decision.
- **CXO:** Summary UX — conversational (floor) vs structured (handler). Suggest folding into the pending UX working session rather than a separate pass.

## Context you'll want
- `_handle_summarize` has been **effectively dead** (keyed on `summarize`/`create_summary`, which the classifier never emits); the conversational floor has been serving summaries, and does it well (verified live). Its `source_type`-in-context model is orthogonal to the classifier's action-per-type discrimination.
- No code shipped for summarize — WIP reverted. Migration #1 (the rail) is live and unaffected.
- I'm proceeding with cohort #3 (`comment_issue`) in parallel, verifying its real action name first.

Detail, evidence, and decision list: **#1158**. Roadmap: `docs/internal/architecture/current/pre-floor-handler-migration-roadmap-1124.md`.

— Lead Developer
