# Unit 4b — single-op routing accuracy before/after the `plan` outcome (2026-09-28)

**Question (Arch, 09-26)**: does teaching the router the plan form make it worse at ordinary single-operation turns?
**Method**: full Phase-0 corpus (151 rows), one context-free router call per row, `openai:gpt-4o-mini` (the dev key's provider, served 151/151), scored by `scripts/inversion_phase1_shadow_score.py`. **Before** = each row's frozen verdict from the existing reports (`inversion-phase1-shadow-score-2026-09-25.md`, the TEMPORAL re-score, and the Phase 3 reports). **After** = `inversion-phase1-shadow-score-2026-09-28-4b-after.md`, run on the prompt that ships. Compared per row, never pooled.

## Result — the shipped prompt

| rows | same | improved | regressed |
|---|---|---|---|
| asserted (92) | 88 | 4 | **0** |
| REVIEW (59, no asserted expectation) | 54 route-same | 5 route-changed | — |

Asserted MATCH **69 → 73 of 92**. The 4 improvements are GUIDANCE rows flipping to `get_contextual_guidance` (single samples — treat as noise in the right direction, not a claim). Of the 5 REVIEW changes, **2 are the intended win**: the two genuine multi-op messages in the corpus now come back as plans (`what time is it? also connect my github` → `PLAN[get_current_time→manage_repos]`; `please clear the reminders except … also …` → `PLAN[delete_todo→set_default_repo]`). The other 3 are single-sample flips on unpinned rows with no safety direction (none turns a destructive ask into a read or vice-versa).

## What it took to get there — two prompt-copy defects found and fixed before shipping

The lane's first prompt (committed as `e51f33115d`, not deployed) measured **0 regressed of 92 asserted** too — but the REVIEW rows exposed two real, deterministic regressions the asserted set could not see:

1. **`delete my reminders` → `list_reminders_query`** (rationale: *"needs to list them first"*), 6/6 under the new prompt vs 6/6 `delete_todo` under the pre-4b prompt (control sample, same model, same session). A listing is a live READ, so on alpha this would have turned a delete ask into a listing. Plan-thinking leaking into a single answer.
2. **`please mark 1, 2, 4, and 5 done` → REFUSED**, 6/6 — the model returned a plan of four identical `complete_todo` elements, which the (correct) ≥2-distinct rule rejects, and the repair retry rejected again.

Rewording the exception clause did nothing for (1) (still 6/6 listings, even with an explicit "never route a listing first" rule). **The lever was one word in the first sentence**: the lane had changed *"select which single operation should handle the user's message"* to *"which operation(s)"*. Restoring *single operation* — with the plan clause kept as a rare, explicitly scoped exception after the default JSON shape — gave 6/6 `delete_todo` and 6/6 `complete_todo`, and both genuine two-op messages still form plans (2/2 each on two probes). That framing is now pinned in `test_plan_rule_in_prompt_is_the_exception_not_the_default`.

**Lesson, stated for the next prompt change**: an asserted-only before/after can read 0-regressed while REVIEW rows carry a deterministic live regression. Read both tables; sample any changed row n≥6 against a same-session control on the old prompt before attributing it to noise.

## Budget
151 (first after-run, superseded) + 151 (second, superseded) + 151 (shipped) + ~40 targeted samples ≈ 490 router calls to gpt-4o-mini. PM approved "one re-score"; the two extra full runs were spent because the first two prompts would have shipped a live regression. Cents in dollars; stated so the denominator is honest.

**Verified how**: every number above is from runs this morning, quoted from the scorer's own output and a per-row comparison script; control sample used the pre-4b router source loaded from git (`e51f33115d~1`). Layer: router only, context-free, frozen model verdicts — not production turns. Denominator: 151/151 rows, both tables.
