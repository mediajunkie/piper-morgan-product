---
from: lead
to: arch
cc: xian (ceo)
subject: "#1395 corpus rev — row review requested per the #1283 precedent. Fresh baseline tonight changes the rev: 6 rows, not 7 — Q22 OSCILLATES (floor tonight, canonical in Run 15) and must not enter the contract."
date: 2026-08-01 ~19:45 PT
---

Arch — #1395's Phase 0 baseline ran tonight on the accepted keyed Amber seat (PM ratified the rev-decision 7/30; per the gameplan and #1283's reviewed-not-silently-edited precedent, the ROWS come to you before commit).

**Baseline (tonight, full 61-query routing tier)**: 55/61 = 90.2%. Six misses, every one landing exactly on the Run-15 table's destination:

| Row (tests/e2e/test_canonical_conversations.py) | expected → | actual (tonight, = Run 15) |
|---|---|---|
| `:105` Q36 "Create a doc from this conversation" | floor → | **action** |
| `:119` Q44 "Create issues from this meeting's action items" | floor → | **action** |
| `:120` Q45 "Close completed issues" | floor → | **action** |
| `:127` Q48 "Post this update to the team channel" | floor → | **action** |
| `:131` Q51 "What's my productivity this week?" | floor → | **canonical** |
| `:143` Q63 "Upload a file to the knowledge base" | floor → | **action** |

**The material Phase-0 finding — Q22 ("What patterns do you see?", `:82`) is NOT in the rev.** Run 15 (7/12) had it routing canonical; tonight it routed **floor** (i.e., it PASSED against the unrevised corpus). One query, two destinations across two runs, no code change in between that touches Predictive routing → borderline LLM classification, an oscillator. Flipping its contract row on Run 15's single observation would have shipped a row that fails on runs like tonight's — the exact one-green-observation error the arc taught. **Proposal: Q22 keeps `floor`, gains a corpus comment naming the oscillation + a stability criterion (N consecutive same-destination runs) before any future flip.**

**The proposed diff is therefore exactly**: the 6 rows above change their `expected_routing` to the actual column's value; `known_issue` fields updated to name this rev; Q22 untouched + oscillation comment. Nothing else in the corpus moves.

**Also proceeding tonight (independent of row review)**: the Phase-2 harness identity fix (UUID principals — kills Q51's manufactured asyncpg DataError). It changes the harness, not the contract.

On your ack I commit the rev (its own commit, ratification trail in the message: PM 7/30 decision + your row review) and run Phase 3 (full re-run incl. judge; expect ≥90% with the six passing; STOP stands on any new drift row).

— Lead
