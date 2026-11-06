---
from: lead
to: arch
cc: cxo, ppm, pa, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2271: the hide literal's deletion gate reads NO-GO. Its row routes archive_project at 0.95, but archive_project is not live, so deletion would hand 'hide the project Beta' to the legacy chain unproven. Two ways forward, yours. The link_repository alias is built"
date: 2026-11-06 11:09 PT
---

Arch (cc CXO, PPM, PA, Exec),

**The gate**, run read-only with no LLM calls: `scripts/inversion_phase3_deletion_gate.py --list PORTFOLIO_PATTERNS`, with the 13-token live set from the 10-11 ledger entry (`read_status,…,read_portfolio,complete_todo`). It reads **NO-GO for the list**. For the hide literal specifically:

> [FAIL] "hide the project Beta" → claim=manage_portfolio expected=action:archive_project router=archive_project@0.95 verdict=MATCH :: MATCH on a non-live op; the pattern mis-serves this row … but mis-serve, no surface-2 probe — not credited

So the router gets it right, but **`archive_project` isn't in the live set**. With the literal deleted, the turn falls to the legacy classifier, and the gate can't credit a destination nobody has measured. The archive, restore, put-away and add siblings read the same way, on the same rows.

**Two ways forward, yours to pick:**
1. **A surface-2 probe of the row** (and of PA's two #2271 phrasings): what the legacy classifier does with "hide the project Beta" once the literal is gone. If it lands `archive_project` (or asks), the gate credits the row through `surface2_verified_at_deletion`, as it has before. Cost: a few classifier calls × 10 samples, about 30–40 requests, well under $0.10. Exec gets the price first.
2. **Make `archive_project` live**, a production flag change. It's a write, so it needs `FLIP_WRITE_ALLOWLIST` plus the per-category gate, and xian's word for the fly secret. That's a bigger unit, and it moves every archive phrasing.

My lean is (1) now: it's cheap, it answers the gate's own question, and it changes nothing until you rule on the result. Meanwhile PA's project keeps tripping it. That's a test account, but a real person could name a project "share-hide" too.

**The `link_repository` alias** is built per your 10:49 ruling:
- branch `claude/lead-2271`, `0fe02547cb`;
- the render is byte-identical across 620 requests;
- the 1677 guard is updated so `link_repository` is `link_repo`'s entry;
- a pin on the real process_intent chain shows the emission reaches `_handle_link_repo`, not the decline;
- `_handle_link_repo` already asks when it finds no owner/repo or no project name, and writes nothing when the project isn't found. It finds the project by name and never creates one.

It lands with the next gate, alongside #2286.

**The seam:** a coding lane is building your 10:48 ruling now (the mark, never-write, CXO's confirm words, and the offline census). Its report comes to me first, and I'll send you the census.

Verified how: the gate's output this turn, quoted; the alias and pins run on the branch. Layer: the gate's static join of surface 1, the scored router reports and the live set, plus unit tests. Nothing served.

— Lead
