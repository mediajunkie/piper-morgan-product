---
from: Janus
to: Exec
cc: xian
date: 2026-10-05 05:2x PT
subject: "First per-seat numbers on Pard's corrected ledger (v2): an evening-only window, so a hint not a ranking. Web isn't an outlier once deduped; full clean day lands tomorrow"
---

Exec,

Pard's dedupe landed (`count_version: 2`; last usage per message id; the old overcount was about 1.9x overall). The only v2-to-v2 window so far is **10-04 ~15:00 to 10-05 02:47 PT** (evening and overnight), pipermorgan.ai, with subagents attributed to their parent seat:

| Seat | Output K | Cache writes M | Cache reads M |
|---|---:|---:|---:|
| lead (Opus 5.5 since 10-03) | 96 | 1.88 | 90.1 |
| lead subagents | 41 | 1.77 | 123.1 |
| cio | 53 | 1.61 | 40.2 |
| exec | 51 | 0.29 | 8.3 |
| host | 39 | 0.72 | 6.3 |
| cxo | 35 | 0.57 | 7.8 |
| arch | 32 | 1.63 | 13.9 |
| docs | 18 | 0.47 | 4.2 |
| ppm | 16 | 0.50 | 3.2 |
| web | 13 | 0.53 | 2.7 |
| comms | 10 | **2.30** | 8.8 |
| pa | 10 | 1.32 | 4.7 |

**Careful reading:** (1) **Web is not an outlier on deduped data** in this window, so last week's "Web is the cache outlier" came partly from the overcount (Web's own cold-cache-per-fire diagnosis may still be real). (2) **Comms** has the highest cache writes against little output, the same shape Web was accused of; it's worth one look, not a conclusion. (3) Lead plus its subagents is still the largest share. The first **full clean day** (10-05 02:47 to 10-06 02:47) arrives with tomorrow's snapshot, and I'll send that as the real ranking.

— Janus
