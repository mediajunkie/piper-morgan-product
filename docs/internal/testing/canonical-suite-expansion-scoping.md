# Canonical Regression Suite — Coverage + Scoring Expansion (Scoping)

**Author**: Lead Developer · 2026-06-13
**Tracked as**: [#1213](https://github.com/mediajunkie/piper-morgan-product/issues/1213)
**Status**: SCOPING (proposal for PM go-ahead — most items change regression *semantics*, so PM-gated before implementation)
**Motivating concern (PM, 2026-06-12)**: *"if we now pass the canonical queries regression suite 100% but still have wiring bugs, we may need to expand the list of queries or raise the difficulty of the scoring."*
**Proof case**: **Q16** ("Create a GitHub issue about testing") — a real graceful-degradation gap (→ #1212) that was **cascade-hidden in every prior run** and only surfaced once the #1165 boot-once fix let the suite run end-to-end. PM's concern is not hypothetical; the suite *did* let a wiring bug coexist with a green-looking run.

---

## 1. What the suite is today (baseline 2026-06-12)

`tests/e2e/test_canonical_conversations.py` — **61 queries** (Q1–Q63, gaps at 15/39), four tiers:

| Tier | What it asserts | Coverage | LLM cost | Runs on |
|---|---|---|---|---|
| **Routing** | `actual_routing == expected` (floor/canonical/action) from intent metadata | all 61 | none | every PR |
| **Structure: not-empty** | `len(message) > 10` | all 61 | none | every PR |
| **Structure: no-template** | floor responses lack 3 canned-template fingerprints | 28 floor | none | every PR |
| **Structure: no-error** | response lacks 4 error fingerprints (`"something unexpected happened"`, `"internal server error"`, `"traceback"`, `"exception"`) | all 61 | none | every PR |
| **Quality (LLM judge)** | Colleague Test rubric R/C/T 0–3 each; `verdict in (PASS, MARGINAL)` | **25 only** (floor **AND** `known_issue is None`) | ~$0.40/run | scheduled (gated by `CANONICAL_JUDGE_ENABLED`) |

Baseline after the boot-once fix: **242 pass / 1 fail / 0 err**; routing 61/61; quality 25/25. The 1 fail = Q16 no-error-fingerprint (the gate working as designed, once it could run).

---

## 2. Why 100%-pass and wiring-bugs coexist (the coverage holes)

The concern is structurally correct. Five gaps, in descending order of how many real wiring bugs they hide:

### Hole 1 — Canonical & action queries get NO content/quality check at all
The quality judge runs on **floor + non-known-issue only (25 of 61)**. Every `canonical`-routed (e.g. Q41 "What did we ship this week?", Q56 "Show my todos") and every `action`-routed query (Q16, Q32, Q49, Q54/55, Q58) is checked for *routing-correct + non-empty + no-error-string* and **nothing about whether the content is right**. A canonical query can return stale, empty, generic, or fabricated data and pass — this is exactly where last-mile/wiring bugs live (the response is structurally fine; the *data* is wrong).

### Hole 2 — "Routing-correct" ≠ "executed-correctly"
The routing tier checks the *label* (`category == execution` → "action"), not the *effect*. Q16 routes to "action" perfectly **and the action failed**. No tier verifies an action-routed query actually attempted/produced its effect. This is the precise shape of PM's "wiring bug."

### Hole 3 — Error detection is 4 hardcoded strings
Q16 was caught only because its degradation happened to emit `"something unexpected happened"`. A wiring failure that degrades with *different* wording ("I wasn't able to do that", "I don't have access to", "let me try that again") sails through. Detection-by-string-allowlist is brittle by construction.

### Hole 4 — Zero multi-turn coverage (the #1122/#1207 surface is untested)
`send_canonical_query` uses a unique `session_id` per call — **every query is single-turn by design**. The entire antecedent-resolution surface we spent 2026-06-11/12 fixing (#1122 floor antecedents, #1207 hydration, in-flight-turn exclusion) has **no canonical regression guard**. A change that re-breaks "comment on it" / "close that one" would pass the suite 100%.

### Hole 5 — Scoring threshold is lenient
`verdict in ("PASS", "MARGINAL")` → a 5/9 response passes. No per-dimension floor (a response scoring Context=1 "generic" still passes if R+T carry it). "Raise the difficulty" = tighten this.

---

## 3. The load-bearing constraint: why the judge is floor-only (don't naively "expand the judge")

**#1131** (CANONICAL-TODO-JUDGE-ARTIFACT) documents it: the LLM judge is **stateless** — it has no ground truth for the canonical-test user's real state, so it flags an *honest* "you have 4 todos" response as fabrication. The judge can only score **floor** responses fairly *because* floor responses don't assert user-specific data.

**Implication for the expansion**: "extend the judge to canonical/action queries" is the **wrong** move — it would multiply #1131-class false-fails. Data-bearing responses need **deterministic ground-truth assertions** seeded from known fixture state, not an LLM judge. This also happens to be a *stronger* wiring-bug catcher (a judge can't tell "5 issues" from "3 issues"; an assertion against known fixture state can).

So the expansion splits by routing class, not "more judge everywhere."

---

## 4. Proposal (priority order)

Each item notes: **what wiring-bug class it catches**, **effort**, **PM-gated?** (changes pass/fail semantics → yes).

### P1 — Ground-truth assertions for canonical/action queries *(catches Holes 1 + 2; the biggest hole)*
Seed the canonical-test user with a **known fixture state** (N todos, specific issues, a known milestone, etc. — partly exists for #1131's "4 todos"). For data-bearing canonical/action queries, assert the response **reflects that known state** (e.g. Q56 "Show my todos" → response mentions the seeded todo titles; Q41 "what did we ship" → references seeded shipped items). Deterministic, no LLM cost, runs every PR.
- **Effort**: M (fixture seeding harness + ~15 assertions). **PM-gated**: yes (new pass/fail surface).
- This is the single highest-value item — it's where "wiring bugs that pass 100%" actually live.

### P2 — Honest-degradation assertion for action queries *(catches Holes 2 + 3; the Q16 class)*
For `action`-routed queries, assert the response **either** demonstrates the action succeeded with evidence **or** degrades with a *specific, honest* message — and **never** a generic catch-all. Replace the 4-string allowlist with a "generic-degradation" detector (broaden the list now; longer-term, a small judge pass scoped to *"did this silently swallow a failure?"* — a yes/no the stateless judge *can* answer without ground truth).
- **Effort**: S (broaden fingerprints now) → M (degradation detector). **PM-gated**: partial (broadening fingerprints is safe; the assertion is semantics).

### P3 — Multi-turn antecedent-resolution conversations *(catches Hole 4; regression guard for #1122/#1207)*
Add a small **scripted multi-turn** tier (5–10 conversations, shared `session_id` across turns): e.g. "Create an issue about X" → "add a comment to it" → "close it"; assert each turn resolves the antecedent and the floor receives non-empty history. This is the *missing regression guard* for the two days of work we just shipped.
- **Effort**: M (new conversation-script harness + the turn-chaining the single-turn helper deliberately avoids). **PM-gated**: no (pure additive coverage, doesn't change existing semantics) — but worth flagging because it's the most architecturally interesting.

### P4 — Raise judge scoring difficulty *(catches Hole 5)*
Drop `MARGINAL`-as-pass (require `verdict == "PASS"`, total ≥ 7) **and/or** add a per-dimension floor (e.g. Context ≥ 2 to fail generic responses). Make threshold + model explicit env knobs.
- **Effort**: S. **PM-gated**: yes (directly "raise the difficulty" — but I'd recommend doing this *after* P1, since tightening the judge on the narrow floor subset catches fewer wiring bugs than closing Holes 1/2).

### P5 — Corpus breadth *(catches: marginal)*
More single-turn queries. **Deliberately lowest priority**: adding queries that get the same shallow checks (Holes 1–2 unfixed) multiplies green checkmarks without multiplying caught bugs. Breadth matters *after* depth (P1–P3) lands. PM's framing offered "expand the list **or** raise the difficulty" — the analysis says **deepen scoring + close coverage holes** beats **lengthen the list**.

---

## 5. Recommended sequence

1. **P3 (multi-turn)** first — it's non-PM-gated (pure additive), it guards the freshly-shipped #1122/#1207 work that's currently unprotected, and it's the highest regression-risk surface right now. I can start this without changing any existing pass/fail.
2. **P1 (ground-truth assertions)** — biggest wiring-bug catcher; needs PM go (new semantics) + coordinates with #1131's fixture state.
3. **P2 (honest-degradation)** — broaden fingerprints immediately (safe); degradation detector after.
4. **P4 (raise judge difficulty)** — last; tighten once coverage holes are closed.
5. **P5 (breadth)** — opportunistic, ongoing.

## 6. What's PM-gated vs. what I can just do
- **Just do (non-gated, additive)**: P3 multi-turn scaffold; P2's fingerprint broadening.
- **PM go needed (changes pass/fail semantics)**: P1 ground-truth assertions; P4 difficulty raise; P2's degradation assertion.

## 7. Cross-references
- **#1212** — Q16 graceful-degradation gap (the proof case; P2 is its regression guard).
- **#1131** — stateless-judge false-fail (the constraint shaping §3; P1 coordinates with its fixture state).
- **#1165** — the UAT/M3 closing gate this suite backstops.
- **#1200** — prior canonical routing-expectation fix (Q25), precedent for corpus maintenance.
- **#1138** — `ActionDisposition.CANONICAL` naming (tangential; the "canonical" routing label this suite asserts on).
