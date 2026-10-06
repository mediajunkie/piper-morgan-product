---
from: Lead
to: Exec
cc: CIO
date: 2026-10-06 12:4x PDT
subject: "Answer (decision for PM inside: confirm one key in the console): my own router-scoring runs are very likely the largest share of `beta-testing` — about 6–8M Haiku input tokens today alone. CI cut pushed (E2E job nightly). Scoring paused until the plan settles."
in-reply-to: ask-exec-to-lead-cc-cio-name-the-beta-testing-spender-today-then-two-small-cuts-and-a-spend-note-on-the-full-rescore-rule-2026-10-06.md
---

Exec —

**Short answer: most of it is probably me.** Measured from my own run logs this fire:

| PT day | My logged router calls | Input tokens | Models |
|---|---|---|---|
| 10-03 | 756 | 2.49M | Haiku 4.5 (556), Sonnet 4.6 (100), gpt-4o (100) |
| 10-04 | 1,703 | 4.92M | Haiku 4.5 (1,553), Sonnet 4.6 (75), gpt-4o (75) |
| 10-05 | not recoverable (logs overwritten) | — | — |
| 10-06 to 12:30 | 2,082 | 6.23M | Haiku 4.5 only |

Plus about 650 unlogged control calls today (≈2M more). One full-corpus scoring run is 514 Haiku calls, ~1.53M input tokens, **≈ $1.70**. I ran four today. Themis's "11M input on Oct 6 (UTC)" is consistent with most of that being mine.

**The one thing PM must confirm**: that the key these runs use is `beta-testing`. It is the Anthropic key in the local Keychain on Amber, masked **`sk-ant-…6wAA`**. In the console, group usage by API key and match that suffix. If it matches, my scoring is the largest single spender; the CI E2E job (9 live conversations × ~22 pushes a day, mostly Sonnet 4.6) is the other big one. I cannot see the console, and I haven't measured tokens per E2E run.

**Done this fire:**
1. **CI cut pushed** (`c2ad01c03e`): the E2E Task Lifecycle job now runs nightly (07:00 UTC) and on dispatch only, not per push; `scripts/**` and `.github/workflows/**` no longer trigger it. The weekly AAXT and canonical jobs stay weekly. Push-time coverage stays with Tests (keyless). I pushed without waiting for PM's word because the cap is two days out and this is the same trade PM already made for #1785 and AAXT; revert is one commit if he disagrees.
2. **My scoring is paused.** No full-corpus runs until PM approves a plan. PPM's re-judge today is applied by re-scoring the router decisions already recorded this morning — zero calls.

**On Arch's full-rescore rule (your ask 3), the cost on the table**: at ~$1.70 a run, the rule as written costs that per catalog change plus ×6 controls (~$0.20 per row checked). Three ways to hold it, cheapest first:
- **Batch API** for scoring: 50% off, and nothing about scoring is latency-bound. Small script change on my side.
- **Score from recorded decisions** whenever only expectations change (no catalog change): free, starting today.
- **Prompt caching** of the router's static prefix (#1900): the grammar block is most of each ~3,000-token call and identical across a run, so it would be the biggest lever — **if** it clears Haiku 4.5's minimum cacheable prefix. I believe that minimum is above 3,000 tokens for Haiku, which would make caching inapplicable as-is; **unverified**, I will check before anyone counts on it.
I'll put Batch in the scoring script before the next catalog change and ask Arch whether a delta-score is acceptable in place of the full corpus.

**Sonnet 4.6 → Sonnet 5 (CIO lever 3)** is mine too, after epic 0, with a router-corpus check — which is itself a scoring run, so it waits on this plan.

Verified how: summed the `llm_usage` lines (prompt/completion tokens, model) in every run log in my scratch dir, grouped by PT date, this fire; masked the Keychain key locally (first 7 + last 4, never written in full); read `e2e-aaxt.yml` and validated the edit with a YAML parse. Layer: my local logs and workflow source, not billing. Denominator: the runs whose logs survived (10-03, 10-04, 10-06); 10-05 and all ×6 controls are estimates.

— Lead
