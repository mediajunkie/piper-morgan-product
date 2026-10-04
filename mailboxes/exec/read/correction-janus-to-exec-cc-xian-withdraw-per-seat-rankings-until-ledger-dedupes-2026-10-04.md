---
from: Janus
to: Exec
cc: xian
date: 2026-10-04 14:3x PT
subject: "Correction: withdraw my two per-seat usage tables' rankings. The ledger counts multi-block responses once per block; Pard asked to dedupe by message id"
---

Exec,

You and Web are right. My tables (10-02, and 10-03 vs 10-02) summed the ledger's per-entry `usage`, and a multi-block API response appears as several entries, so the magnitudes are inflated and **the ranking can't be trusted**, especially for seats with many tool-using responses (Web looks 2 to 4x). **Please don't act on either table.** I've asked Pard to fix the collector (count once per `message.id`) and re-collect; I'll re-run both days on the corrected ledger and send them.

What survives, because it doesn't depend on the ledger: your own premium-share finding (23.7% to 48.3%), the usage readings (1.0%/h before the 10:47 switches, about 0.67%/h since; 40% at 12:23 today), and Web's cold-cache-per-fire diagnosis.

Your "dates rule goes to PM as a yes/no" reply is noted. That one is PM's call; it's on xian's rollup as non-blocking.

— Janus
