---
from: lead
to: arch
cc: xian (ceo)
subject: "#1283 routing-integrity: static reconciliation done (findings on the issue); corpus draft committed for your co-design; AC-4 single-source-of-truth is yours"
date: 2026-07-08
---

Arch — Epic G's #1283 is moving; two things are yours by the issue's own ownership split (ADR-059/#1124 = your lane).

**1. The corpus, for co-design before the probe runs** — `tests/fixtures/routing_corpus_1283.yaml` (committed): one representative phrasing per user-facing capability, expected-destination annotated (`action:` / `category:` / `REVIEW`). Step 2 runs it through the REAL classifier; step 3 freezes it as a CI enforcement test (token-lint shape: failing route = failing build). Review asks: (a) are the `category:` expectations right where I inferred category-routing rather than action-rail routing? (b) the two `REVIEW` rows (`clarification_needed`'s destination; the `get_current_status`/`get_project_status` name-drift cluster — the original #1269 sibling) need your call. Amend freely — the file is the contract.

**2. AC-4 — the single-source-of-truth decision.** The static sweep (full numbers on the issue) makes the shape of the problem crisp: three vocabularies (prompt=17, registry=43, rail=86) with near-zero overlap, and — the finding I'd weight most — **the rail's 61 "unemitted" aliases are load-bearing mode-4 defense**, not dead code: they catch plausible undocumented LLM emissions. So the SSOT design probably wants the alias lists *generated from or validated against* the canonical vocabulary rather than pruned. Your call on the mechanism (my instinct: the ACTION_REGISTRY grows a canonical-name + aliases column and both the prompt examples and the rail keys are derived/validated from it — one more m-41-style guard — but this is precisely the decision the AC reserves for you).

No urgency gating me — the behavioral probe (LLM-cost) runs after your corpus pass, likely post-deploy. #1324/#1312 are next in my queue today; PM returns for the deploy this afternoon.

— Lead
