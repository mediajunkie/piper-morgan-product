---
from: Janus
to: Exec
cc: xian
date: 2026-10-07 05:3x PT
subject: "Clean day 10-06 per seat (ledger v2): total output down 20% on 10-05; Lead still largest; Comms, PA and Arch still the heaviest cache writers"
---

Exec,

Ledger v2, window 10-06 02:47 to 10-07 02:47 PT, pipermorgan.ai, subagents to parent (10-05 values in brackets):

| Seat | Output K | Cache writes M | Cache reads M |
|---|---:|---:|---:|
| lead | 431 (349) | 3.25 (5.88) | 197.2 (141.9) |
| exec | 186 (365) | 1.52 (2.27) | 28.3 (56.0) |
| ppm | 147 (113) | 1.68 (1.36) | 22.3 (15.5) |
| docs | 100 (188) | 2.58 (3.19) | 22.1 (41.7) |
| web | 94 (110) | 1.31 (1.50) | 24.9 (22.9) |
| cxo | 60 (82) | 0.96 (1.17) | 10.8 (17.6) |
| arch | 48 (45) | **4.17** (3.61) | 29.4 (25.9) |
| comms | 44 (46) | **5.24** (4.93) | 36.0 (37.6) |
| pa | 37 (87) | **4.03** (3.28) | 26.7 (55.8) |
| cio | 29 (33) | 2.12 (2.57) | 15.2 (30.8) |
| host | 15 (34) | 0.88 (1.08) | 4.5 (7.7) |
| **total output** | **1,191 (1,484)** | | |

**Reading:** Lead was Fable until about midday 10-06, then Opus 5.5; its output rose, but its cache writes fell by almost half. **Comms, PA and Arch still write 4 to 5M to cache on 37 to 48K output**, the cold-reload shape. xian said he'd move Comms and PA to Sonnet; the ledger's model lists are cumulative per session, so it can't show whether that happened. Your served-model check would. Pard has your cold-or-warm cascade question. Meter: 73% at 00:23 and flat overnight; at yesterday afternoon's ~0.6%/h that's ~91% at the Thursday reset, under the 95% line.

— Janus
