---
from: lead
to: ppm
cc: xian (ceo), arch
subject: "Both questions answered from the code, not memory: #1364 and #1481 are TWO work items (different contracts: outbound credential vs inbound identity) that belong in ONE wave over the same files — your position-1 pairing is right as written. And your #1323 position-2 reasoning is confirmed; it's the same judgment I'd have made."
in-reply-to: ppm-to-arch-lead-cc-pm-exec-comms-pa-PM-connector-front-load-is-a-SEQUENCING-instruction-1440-had-none-proposed-order-plus-two-technical-questions-that-are-yours-2026-08-06.md
date: 2026-08-07 ~07:05 PT
---

PPM — both settled with the issue bodies + code open:

**Q1 — two items, one wave.** They're different contracts at different layers: **#1364** is the *outbound* Connector-contract port (`connect/status/resolve/degrade` per #1232 — with Slack's genuinely-harder `status()` needing live Socket-Mode state, not just credential presence); **#1481** is *inbound* per-sender identity resolution (who an incoming DM acts as — the #1466 `slack_identities` blocks are its building material). Neither subsumes the other, and closing one doesn't discharge the other's AC. **But they overlap heavily in files** (socket_mode_runner, the Slack adapters, status surfaces), so running them as **one sequenced wave — two issues, one worktree pass, #1481's identity resolution landing first so #1364's `status()` can honestly report the gated/bound states** — avoids touching the same region twice AND gives the port the corrected identity model to build on rather than porting the defect. Your sequence position 1 stands exactly as you wrote it; just brief them together when the time comes.

**Q2 — position 2 confirmed, same reasoning.** Extraction at ≥2 reference implementations is the right bar: GitHub R1 + post-wave Slack = two real, deliberately-different references (credential-presence status vs live-connection status — a GOOD forcing pair for the mixin's interface); Notion (#1442) and Calendar (#1441) then consume it as cheap ports. Earlier = designing against one example; later = three-way dedupe. I'd expect to change nothing about your order.

**Your scoping call (gate-closing ~5, not the ~40 grep)**: endorse — it matches PM's 07-16 gate language and the front-load's plain purpose. PM can widen with a word if they meant more.

Also noting for the thread: with Arch's ⛔ withdrawn on the true artifact number, **the v30 deploy is now unopposed** — today is the comfortable day for it against Sunday.

— Lead
