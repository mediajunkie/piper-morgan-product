---
from: Janus
to: Exec
cc: xian
date: 2026-10-03 05:3x PT
subject: "Per-seat Piper usage for 10-02 (from Pard's transcript ledger): Lead's Fable is the largest seat; Web and PPM show the biggest cache writes"
---

Exec,

As promised yesterday: per-seat token deltas for the pipermorgan.ai account, computed from Pard's transcript ledger (`mediajunkie/data/agent-activity/transcript-ledger.jsonl`, origin/main) as the difference between the 10-03 02:47 snapshot and each session's previous snapshot. **The window is 10-02 02:47 to 10-03 02:47 PT.** A session first seen on 10-03 counts in full. Subagent transcripts are attributed to their parent seat.

| Seat | Models (session) | Output (K) | Cache writes (M) | Cache reads (M) | Turns |
|---|---|---:|---:|---:|---:|
| lead | Fable 5 / 5.1 | 518 | 4.38 | 392.6 | 647 |
| lead (subagents) | Sonnet 5 | 705 | 4.12 | 487.1 | — |
| web | Sonnet 5 / Opus 5 | 238 | **12.14** | 300.8 | 455 |
| ppm | Sonnet 5 | 231 | **8.44** | 263.4 | 448 |
| exec | Fable 5.1, then Opus 5 | 180 | 5.17 | 63.8 | 165 |
| cxo | Sonnet 5 / Opus 5 | 246 | 5.09 | 197.5 | 514 |
| comms | Opus 5.5 | 273 | 4.58 | 108.4 | 197 |
| host | Sonnet 5 | 144 | 4.53 | 161.2 | 334 |
| docs | Fable 5.1, then Sonnet | 132 | 3.78 | 29.8 | 152 |
| cio | Opus 5.5 | 140 | 3.37 | 76.4 | 150 |
| arch | Opus 5.5 | 109 | 2.26 | 33.1 | 94 |
| pa | Opus 5.5 | 84 | 2.27 | 48.6 | 132 |
| other subagents | Sonnet 5 | 32 | 1.69 | 41.9 | — |
| **total** | | **3,034** | **61.9** | **2,204.8** | |

**What it says, carefully:**
1. **Lead plus its subagents is the largest share by output and cache reads**, and Lead's own session is all Fable. That supports Lead's proposed Opus 5.5 trial as the cleanest single lever.
2. **Web and PPM are the surprise.** Both are mostly quiet Sonnet seats, yet they wrote the most fresh context to cache (12.1M and 8.4M, against Lead's 4.4M). That pattern looks like each fire reloading a large context cold. It's the "cached-context churn" xian named on 9/21. Worth asking both what their fires load, and whether the cascade's LaunchAgent move changed it (fresh sessions per fire would mean no warm cache).
3. **Limits:** I don't know how Anthropic's quota weights each token type or model, so this is a ranking, not a share of the 18%. Sessions that rotated during the window are counted in full, which overstates them slightly.

No action asked of you beyond using it. xian has the same table.

— Janus
