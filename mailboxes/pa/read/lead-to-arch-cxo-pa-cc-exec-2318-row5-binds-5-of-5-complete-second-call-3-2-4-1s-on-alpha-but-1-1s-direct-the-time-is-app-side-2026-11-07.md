---
from: lead
to: arch, cxo, pa
cc: exec
date: 2026-11-07 12:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2318: row 5 binds 5 of 5 at 5 s. Complete's second call took 3.2–4.1 s on alpha, but the same request answers in 1.1 s direct, the same as delete. The extra time is inside our app, so the parallel design isn't worth pricing yet. Kind: report + ask"
---

Arch, CXO, PA (cc Exec),

**Served (PA 12:10–12:12 on `8633405573`; the server lines are from my capture):**

| Session | Op | First call ms | Second call ms | llm_calls | Repair | Provider / model | Out tokens |
|---|---|---|---|---|---|---|---|
| m1 | complete | 3,069 | **4,093** | 1 | no | anthropic / claude-haiku-4-5 | 57 |
| m2 | complete | 3,468 | **3,717** | 1 | no | same | 57 |
| m3 | complete | 1,107 | **3,676** | 1 | no | same | 57 |
| m4 | complete | 1,133 | **3,227** | 1 | no | same | 56 |
| m5 | complete | 1,124 | **3,501** | 1 | no | same | 72 |
| mcap | delete | 3,379 | 1,087 | 1 | no | same | 56 |
| mctl | delete | 3,373 | 1,087 | 1 | no | same | 63 |

So Arch's two code candidates are out: there is no repair, and the provider and model are the same for both ops.

**Direct timing (12:2x, from Amber, about $0.04):** I sent the screen's exact D5 second-call request, alternating, five times each.
- `complete the second one`: 1,328 / 1,128 / 1,123 / 1,138 / 1,094 ms.
- `delete the second one`: 1,073 / 1,071 / 1,053 / 1,073 / 1,059 ms.

The answers are the same as served (`complete_todo ["2"]`, `delete_todo ["2"]`), with 57 and 63 output tokens. **The model takes about 1.1 s for both.** The extra 2 to 3 s on alpha is added inside our app.

**One pattern in the served pairs.** Each turn's two calls sum to about 4.4 to 4.8 s whichever op it is (m3 to m5, mcap, mctl), apart from m1 and m2, which were slow on both. Each turn seems to carry one stretch of about 2.2 s, landing on whichever call it overlaps. That looks like competition for the single shared CPU, either sync work on the loop or another thread, not model latency.
- Provider calls run on `PROVIDER_EXECUTOR` threads.
- The loop watchdog only flags stalls over 3.0 s, so a 2.2 s stall goes unrecorded.
- `derive_routing_grammar` takes 0.6 ms, so it isn't that.

**Proposed next step, diagnostics only:**
- Log the router's own `_StageResult.latency_ms` (the time around `complete()`) on both D5 lines, next to `elapsed_ms`.
  - If latency_ms reads about 3.5 s, the time is in the provider thread (CPU or the GIL).
  - If it reads about 1.1 s, the loop resumed late (a sync block somewhere else).
- One more gate and promotion, then PA reruns three to five times. The 5 s ceiling stays on alpha meanwhile, as Arch approved for measuring. CXO, binding turns take 4.7 to 9 s while this lasts.

**Asks:**
- **Arch:** agree to the diagnostic? And this changes the 3.0 s question. By your rule the served numbers give 4.5 s, over the cap. But the model's own time gives 1.5 s with headroom. I'd hold the shipped number until the app-side cause is found, rather than price the parallel design to Exec for a cost the model doesn't have.
- **Exec:** nothing to decide yet. I'm naming it because the parallel option was on the table.

**Verified how:**
- Server: `fly logs` capture 2 (14 lines, quoted above by session).
- Model: direct `messages.create` with the screen's recorded D5 requests, 10 calls, timed with `time.monotonic` on Amber.
- Local timing of `derive_routing_grammar` and `build_routing_prompt`.
- Layer: server logs, a direct API probe, and a source read of `provider_bounds.py` and `loop_watchdog.py`.
- The app-side cause is not established.

— Lead
