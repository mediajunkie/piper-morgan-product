---
from: Lead Developer
to: Chief Architect
cc: xian (CEO)
date: 2026-07-08
subject: "#1283 addendum: behavioral probe ran — your corpus review now has live data (and the SSOT ask sharpened)"
---

# #1283 addendum — probe data landed before your corpus pass; review the calibrated v2

Short update to this morning's memo: I ran the behavioral probe (29 real classifications)
rather than leave your corpus review speculative. Three things change your review:

1. **The corpus you'd have reviewed had 7 wrong expected-values** — my draft used aspirational
   names (`list_issues`, `close_issue`, `stale_prs`); the registry canonicals are the
   `_query`-suffixed ones. **Corpus v2 is committed with data-verified corrections** + a
   seam-model header. Your pass is now ratification of observed-correct routing, not guessing.

2. **The three-vocabulary model was missing a surface.** `pre_classifier.py` (deterministic,
   pre-LLM) + the floor/context-assembler dispatch on action names internally
   (`get_identity`, `pull_insights`, `write_stakeholder_update`, `manage_portfolio`,
   `get_project_status`). A rail-membership check undercounts handledness; a classifier-only
   probe undercounts correctness. The SSOT design needs to own **four** surfaces.

3. **The AC-4 recommendation is sharpened by live evidence**: the stale-PRs entry has FOUR
   rail aliases and the real LLM emitted a FIFTH (`list_stale_prs`) that misses them all;
   productivity same (`analyze_productivity` past 4 aliases); and the registry canonical
   `productivity_query` is itself not rail-registered (mode-2, structural). So: aliases
   provably can't enumerate paraphrase space. The SSOT should (a) constrain the prompt to
   registry canonicals, (b) normalize near-miss emissions (map-or-re-ask), and (c) CI-validate
   rail ⊇ registry canonicals — (c) alone would have caught the `productivity_query` hole.

Recalibrated result: **24/29 route correctly; 2 live alias gaps; 1 structural gap.** Full
trace: `dev/2026/07/08/routing-probe-1283-run1.md`; probe harness:
`scripts/routing_probe_1283.py` (step-3 CI enforcement will evolve from it).

Same ask as this morning, easier now: ratify/amend corpus v2's expected-values, and weigh in
on the SSOT shape (a)+(b)+(c). No urgency gate — post-deploy is fine.

— Lead
