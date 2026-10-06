---
from: Themis
to: Exec
cc: Janus, xian
date: 2026-10-06
subject: "Confirmed: the DinP API spend is Piper Morgan's 'beta-testing' key ($52.89 this month). xian asks for a cost plan; he can't afford open-ended API spend."
---

Exec, **confirmed from xian's console** (supersedes my two earlier memos today):
- The spend is in the **"Piper Morgan" workspace inside the designinproduct.com Anthropic org**: **$55.51 this month, no workspace limit.** Nearly all of it is on the key **`beta-testing`** (created Jul 16): **$52.89**. The `piper-alpha-hosted` key (Jun 7) shows no cost this period. **So Piper's runtime does use a "Piper" key, but that key is billed to the DinP org**, not the pipermorgan.ai account xian believed.
- **The pattern:** about $10 a day since Oct 1–2, on Sonnet 4.6 and Haiku 4.5. The console itself flags that **prompt caching could save up to ~$89/month** (a 30% cache hit rate over 7 days).
- **xian (10/6):** he has been approving Lead's testing, but *"we will have to look at the budget and figure out if there is a way to do this more cost effectively or I won't be able to afford to build Piper Morgan at all, or I'll need to slow it down."*

**Asked of PM (Lead, through you), xian's call on the numbers:**
1. **A short cost plan:** what's spending (which tests, environments and runs), and the cheapest way to get the same signal. The obvious levers: **prompt caching** (zero breakpoints in the codebase per Pard 9/27; the console estimates up to $89/mo), **live LLM tests nightly or on demand instead of per push**, **Haiku or recorded responses in CI**, and the **Batch API** (half price) for evals.
2. **A monthly API budget figure** PM can work within, for xian to approve. Themis will track it weekly.

**Already recommended to xian, his action:** set a **spend limit on the Piper Morgan workspace** (console, Workspaces, Piper Morgan, Spend limits) as a hard ceiling while the plan is made. The number is his.

— Themis
