---
from: lead
to: arch
cc: pa, exec, ppm
date: 2026-11-01 09:20 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149 step 3: your two additions are built into the runner; one batch holds parity and the three per-delta corpus runs; the runs start on your step-2 validation"
---

Arch (cc PA, Exec, PPM),

Both additions from 09:13 are in (local commits `2c2f3938b0` and `6d6267fe7d`, pushing behind `e24cf93b00`'s Tests run).

- **Corpus once per delta.** The isolation batch will hold: parity's no-delta two-stage corpus run (616 rows ×1), the three per-delta two-stage corpus runs (each rendered from its own tree with the one delta applied), and the 23-phrase ×6 sets per delta; all stage-1 requests in one batch, then all stage-2 requests in a second batch, so every arm shares the two windows. Pass as preregistered: no row outside the edited op's group moves, on the corpus and on the screen alike.
- **The runner.** `scripts/router_batch.py` gains `render-stage1`, `render-stage2` and `parse-two-stage`. Stage-2 requests are rendered by `build_stage2_prompt` from the parsed stage-1 pick, unaltered: pinned by `test_render_stage2_renders_one_request_per_pick_by_build_stage2_prompt_unaltered` (the rendered content equals the function's output for the pick, including a plan part). `parse-two-stage` reconstructs every decision by running the real `route()` with the flag set for the duration, against a replay that answers by stage and, at stage 2, by the group on the prompt's first line and the plan part on its last, never by the user's words; the report carries the stage-1 picks, the OTHER_GROUP and CLARIFY counts with the stage-1 error rate, and with `--expected` the group-confusion table.
- **Tokens from the batch.** `submit` now records each result's own `usage` (input and output tokens); the two-stage report totals them per stage and per decision, and prints 0 where a result carries none (never estimated). `served["usage"]` on the live `complete()` path stays owed, as you said; that is a `LLMClient` change and I'll take it as its own small unit unless you want it elsewhere.
- **Sequence:** nothing is rendered until your step-2 validation. Then: render from main (flag on) and from three delta trees, submit, render stage 2, submit, parse; the cost report from the parse plus `stage_metrics`; results to you first, the cost numbers to Exec and xian with them. Price unchanged from your 09:13 read: under $5.

Verified how: the runner's four pins and the three existing runner pins, 7 passed; enforcement + ratchets + `tests/unit/scripts`, 466 passed; ruff; mypy at ceiling; literal census 89. Layer: unit tests on the tree; no LLM calls made.

— Lead
