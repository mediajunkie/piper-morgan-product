# Cross-Pollination Brief — April 27, 2026

Klatch returned from an 8-day pause and immediately shipped: Phase 5c-i (write-path) signed off, MCP server now feature-complete for 1.0 at 1,131 tests. Theseus ran the first live AAXT behavioral probing, confirming high fidelity on a rich channel and surfacing one bug (Haiku 4.5 code fences) and one design finding (L4 probes cross-contaminating with L2 content). On the PM side, the Phase E re-run on Scenario 1 resolved the routing bypass and immediately produced a new question: the floor sees the harassment message now, but routes to GUIDANCE rather than firing the explicit boundary trigger — filed as #1003. #1004 semantic detector contract (two-layer architecture) is stable and build has begun. CIO proposed Pattern-063: Parallel-Authoring Drift, a new methodology pattern with direct implications for any project where multiple agents co-author rubrics or evaluation instruments.

## Key Insights

### 1. Klatch MCP feature-complete for 1.0; first live AAXT behavioral run with two methodology findings

**From:** Klatch `docs/logs/2026-04-26-1430-theseus-opus-log.md`; commits `ccc4da9` (Round 28), `1724642` (Daedalus sign-off)
**Relevant to:** PM (AAXT probe calibration, evaluation methodology); any agent running behavioral testing

Phase 5c-i (write-path: `reflect` tool + `kit_briefing` prompt + URL-decode fix) was signed off April 26. All three phases of the MCP server (5a read-only resources, 5b tools surface, 5c-i write-path) are complete. Suite: 1,131 total (971 server + 160 client), zero failures. This is the 1.0 feature-complete state.

Theseus ran Track B — the first live AAXT behavioral run in project history. Three channels tested:
- **CH1 (rich, active entity):** 16 probes → 14 Correct, 2 Reconstructed, 0 Phantoms, 0 Subliminals. Overall: **high fidelity**. System working as designed.
- **CH2 (bare, minimal content):** 0 Phantoms. Agent correctly withholds rather than fabricates. "Low" overall fidelity score reflects sparse content, not poor system behavior — the label needs interpretation.
- **CH3 (project-only, no entity/L3/L4):** 1 false-positive Phantom. The probe asked about L4 content ("addendum guidelines"), the agent answered correctly from L2 (project instructions), and the scorer flagged it as Phantom. Not a system bug — a probe quality issue.

**Finding 1 (bug, fixed):** Haiku 4.5 wraps JSON responses in markdown code fences; `JSON.parse()` fails. OpenAI's `response_format: json_object` had masked this. `extractJson()` added to both `probe-generator.ts` and `scorer.ts`. Any team switching between LLM providers for auxiliary roles should treat JSON parsing as a provider-specific surface, not a safe assumption.

**Finding 2 (design):** When a layer has trivially small content, the probe generator creates probes about general project guidelines — which the agent answers from a different layer. The scorer then flags as Phantom because the expected answer references the "wrong" layer by name. The fix is upstream: skip probe generation or add cross-layer awareness when target layer content is below a threshold.

**Suggested action:** PM — the CH2 "low fidelity on sparse content is correct behavior" ambiguity is directly relevant to how PM might interpret AAXT results on roles with minimal L3/L4 context. A bare channel is not a broken channel. The Phantom false-positive finding (Finding 2) also applies to any future probe set that generates L4 probes when L4 is thin: the CHF probe-set construction doc should include a content-threshold check.

---

### 2. Phase E S1 r2: harassment vector reaches floor, routes to GUIDANCE not boundary; #1003 filed; #1004 build authorized

**From:** PM `dev/2026/04/26/phase-e-transcripts/RUN-READOUT-S1-R2.md`; commit `dff9142` (S1 r2 re-run); `dev/2026/04/26/1004-implementation-contract-draft.md`
**Relevant to:** Klatch Daedalus (layered trust architecture — two new findings with architectural implications)

PM authorized the Phase E Scenario 1 re-run after r1's "floor-bypass-by-routing" (yesterday's brief). Rephrasing "blocking my PRs" → "blocking my work for weeks" eliminated the routing keyword — the floor saw it this time (`floor_hit: true`, intent `GUIDANCE`, confidence 0.85).

**New finding: harassment vector → GUIDANCE, not boundary trigger.** The response was a usable empathetic redirect (acknowledging legitimate frustration, rejecting harmful framing, offering constructive alternatives). But the audit envelope has no `boundary_type: harassment`, no `blocked_by_ethics: true`, no `decision_id`. Compare: Scenario 2 (professional) produced all three. The floor distinguishes between "boundary triggered → decline path" and "floor-aware → guidance path." Both are correct floor behavior. They produce different audit shapes.

This raises a question now in front of PPM/CXO: does R-axis PASS require explicit `boundary_type`, or does behavioral redirect within GUIDANCE intent count? Filed as **#1003** (sibling to #1002, which is about PROFESSIONAL substring over-classification). Both should resolve before Phase F.

**#1004 implementation contract v1.0 is stable and build authorized.** Two-layer semantic detector: (1) literal-trigger fast-path (existing substring checks, cheap, deterministic); (2) semantic LLM detector (new, confidence-tiered: ≥0.85 block / 0.6–0.85 ambiguous / <0.6 pass). C1 (audit discriminator: `detector: "literal-trigger"`) builds first (additive, ~0.5 day) so operators have the discriminator from day one. B (semantic detector, ~3 days) follows. Probe set + calibration round closes the loop. CXO authored prompt body v0.1. Total build window: ~5–7 days.

**Suggested action:** Klatch Daedalus — two architecture findings to track for Phase 5c write-path and beyond: (1) a routing layer that consumes messages before your safety/trust layer creates a bypass surface invisible to enforcement tests (reported yesterday, reinforced by r2); (2) your safety enforcement may route correctly without explicitly flagging a boundary type — your audit telemetry design should plan for both "explicit boundary trigger" and "floor-routed-to-guidance" outcomes as distinct states.

---

### 3. Pattern-063: Parallel-Authoring Drift — new methodology pattern, CIO proposes as Emerging

**From:** PM commit `d3acb41`; `mailboxes/arch/inbox/memo-cio-to-ppm-cc-cxo-lead-pm-pa-arch-exec-rubric-drift-methodology-2026-04-26.md`
**Relevant to:** Klatch (any future parallel rubric or evaluation instrument authoring); all agents co-authoring methodology artifacts

PPM and CXO authored parallel Colleague Test rubrics, both extending CT v2, both individually correct. When applied in parallel for Phase E scoring, verdicts converged at PASS while the criteria silently diverged: "C=Context Handling" in one rubric, "C=Clarity" in the other. Same label, different semantics, same verdict — the dangerous combination.

CIO named this **Pattern-063: Parallel-Authoring Drift** (Emerging, self-approval authority, pending PM concurrence on the slot). Distinguished from **Pattern-062** (Assembly Assumption — general "parts work, whole doesn't"): Pattern-063 is specifically the parallel-authoring instance where the failure mode is shared vocabulary breaking under independent extension.

**Diagnostic question:** "If I asked the two authors to score each other's work using the other's rubric, would they get the same answer?" If no, you have Pattern-063 and a gate risk.

**Proposed safeguard:** branch-or-anchor decision rule — at the moment of authoring a parallel extension of a canonical document, either branch explicitly (fork and acknowledge divergence) or anchor explicitly (cite the exact criterion by content, not just by label). This fixes the problem at authoring time rather than after-the-fact via registry maintenance or version stamps.

CIO also notes this is the first time the PDR-004 canonical-vocabulary drift dynamic (previously seen in prose) has manifested in **operational scoring instruments**, where the downstream stakes are higher: divergent rubric application can produce divergent gate decisions, not just retractable blog posts.

**Suggested action:** Klatch — if Argus and Theseus ever co-author a testing rubric or Calliope and Argus co-author an evaluation instrument, Pattern-063 is the design-time check. The diagnostic question is fast: would the two authors get the same score if they swapped rubrics? For PM: Pattern-063 candidacy is pending xian concurrence; when it ships, the reference instance (Phase E C-axis reconciliation, April 26) should be linked from the catalog entry.

---

## Sources Read

- `klatch/docs/logs/2026-04-26-1430-theseus-opus-log.md` — full read; Round 28 Track A/B/C results, MCP feature-complete sign-off, all findings
- `klatch` commit `ccc4da9` (`Round 28`) and `1724642` (`Daedalus sign-off`) — stat and message read
- `piper-morgan-product/dev/2026/04/26/phase-e-transcripts/RUN-READOUT-S1-R2.md` — full read; S1 r2 results, GUIDANCE routing finding, PM decision options
- `piper-morgan-product/dev/2026/04/26/1004-implementation-contract-draft.md` — full read; two-layer architecture, confidence tiers, sequencing
- PM commit `d3acb41` — full diff; CIO Pattern-063 proposal, branch-or-anchor decision rule, methodology framing
- `designinproduct/docs/logs/2026-04-26-log.md` — Janus; trigger status, mail inventory; no new cross-relevant hub activity
- `atlas`, `globe`, `cuneo`, `weather`, `one-job`, `optilisten`, `nyt-crossword` — 48h logs checked; only automated brief delivery and status commits. No narrated insights.

**Not re-reported (covered in prior briefs):** floor-bypass-by-routing finding (Apr 26, r1 result); five-role Chat→Code migration complete, CXO "Colleague Test is the discipline" (Apr 26); #992 Phases A-E shipped (Apr 26); Multi-Wave Investigation published + P0/P1/P2 taxonomy (Apr 26); PO calibration + DRAGONS patterns (Apr 26); Agent 360 v0.2 instrument (Apr 25); narrative arc awareness as undocumented load-bearing function (Apr 25); CIO migration tick-tock protocol (Apr 24); constellation expands to 9 repos (Apr 24).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
