---
title: "Cross-Pollination Brief — April 5, 2026"
date: 2026-04-05
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "48h (April 3–5, 2026)"
---

# Cross-Pollination Brief — April 5, 2026

Klatch shipped **AAXT Scaffolded Probing Phase 1** — a probe generator, scorer, and auxiliary LLM client that automate the gap between structural testing (AAXT) and behavioral testing (MAXT). This is the tooling that would have caught **Pattern-045** before it reached PM's M1 gate. The design draws directly from Argus's **AuditBench methodology review**, which found that Anthropic's alignment auditing benchmark validates the same insight MAXT Session 01 discovered: tools that surface accurate evidence in isolation often fail to improve agent performance in practice. On the PM side, Lead Dev **fixed #940** (single-provider LLM setup, no hardcoded providers, error differentiation) — clearing the primary M1 gate blocker — and PA drafted **Piper Open**, the first "Piper" PM assistant role for a sibling project (OpenLaws at Kind). Klatch's test suite reached **849 with zero failures** after Round 18 covered file injection on imported channels; PM's suite stands at 6303 with one pre-existing failure (#942). Both projects are shipping at pace.

---

## Key Insights

### 1. AAXT Scaffolded Probing Phase 1 — Automating the AAXT/MAXT Gap
**From:** Klatch (Daedalus + Argus, April 4)
**Relevant to:** Piper Morgan (testing methodology)

Daedalus shipped three new components implementing the first phase of scaffolded probing — the automation layer between AAXT (structural) and MAXT (behavioral):

- **Probe generator** reads `prompt-debug` layer status, sends assembled prompt to an auxiliary LLM, and generates 3-5 targeted questions per active layer (up to 19 total). The probes come from actual layer content, not hand-crafted test questions.
- **Scorer** classifies responses against the six-failure-mode taxonomy (Correct, Reconstructed, Confabulated, Absent, Phantom, Subliminal).
- **Auxiliary LLM client** calls GPT-4o-mini (fallback: Haiku) for both generation and scoring — deliberately external to the target agent to avoid self-evaluation bias.

Phase 1 outputs probes for manual review. Phases 2-3 (planned) will wire the full pipeline: generator → target agent → scorer, with multi-probe aggregation using pass@k and pass^k metrics.

**For PM:** This is the tooling gap PM's M1 gate UAT exposed. The gate caught Pattern-045 because a human (CXO) tested real infrastructure with a fresh account. Scaffolded probing automates the equivalent: generate context-aware questions from actual prompt content, send them to the agent, and score whether the agent can *use* the information — not just whether it's structurally present. PM doesn't need to adopt Klatch's implementation, but the methodology (auxiliary-LLM-generated probes scored against a failure taxonomy) is directly applicable to PM's planned E2E/AAXT track (#927-930).

**Suggested action:** When scoping the E2E/AAXT track, evaluate whether scaffolded probing (auxiliary model generates context-aware test questions) would complement the existing unit test suite. The key insight: probes generated from actual content catch gaps that hand-crafted tests miss.

### 2. AuditBench Review — External Validation of the AAXT/MAXT Split
**From:** Klatch (Argus, April 4)
**Relevant to:** Piper Morgan (methodology)

Argus completed a deep review of Anthropic's AuditBench — a 56-model alignment auditing benchmark testing investigator agents across 13 tool configurations. The critical finding for cross-pollination:

> "Tools that surface accurate evidence in isolation often fail to improve agent performance in practice. Agents may underuse the tool, struggle to separate signal from noise, or fail to convert evidence into correct hypotheses."

This maps directly to both MAXT Session 01's subliminal injection finding (agent has context, can't attribute it) and PM's Pattern-045 (tests confirm data is present, user can't access it). AuditBench's most effective approach: **scaffolded black-box probing**, where an auxiliary model generates diverse prompts — exactly what Phase 1 implements.

Four recommendations for Klatch's AXT framework:
1. Automated scaffolded probing (shipped in Phase 1)
2. Multi-probe aggregation (3 passes, reduces false positives)
3. Model-based grader tier (LLM scores behavioral responses — new middle layer between AAXT and MAXT)
4. pass@k and pass^k metrics (capability vs. consistency)

No changes recommended to the six-failure-mode taxonomy or to MAXT itself — the human element remains irreplaceable.

**For PM:** The AuditBench evidence strengthens the case for the E2E/AAXT track. PM's current test suite mocks at the service boundary (Pattern-045's root cause). The scaffolded probing approach — auxiliary LLM generating probes, scored against a taxonomy — is validated by Anthropic's own research as the most effective black-box testing strategy.

**Suggested action:** Low priority. Note AuditBench as external validation. No immediate PM action required, but the review document (`docs/research/auditbench-methodology-review.md`) is worth reading when the E2E track begins.

### 3. #940 Fixed — M1 Gate Path Cleared
**From:** Piper Morgan (Lead Dev, April 4)
**Relevant to:** Klatch (pattern validation)

Lead Dev executed a full audit cascade on #940, the primary M1 gate blocker:
- Removed hardcoded provider assignments from `config.py`
- Introduced provider-agnostic `model_tier` system with `resolve_model()` at runtime
- Setup UI redesigned: pick provider first, then enter one key (OpenAI no longer mandatory)
- Conversational floor now classifies errors (auth, transient, no-provider) with distinct fallback messages rather than a single canned template
- 6303 tests passed, 0 failed (one pre-existing: #942, workflows table)

The fix addresses Findings 1 and 2 from the UAT. Findings 3-5 (handler pre-flight, todo completion, input parsing) remain open. Lead Dev also processed all 5 inbox items and deleted 3 stale branches.

**For Klatch:** The M1 gate methodology continues to validate. The audit cascade pattern (issue audit → gameplan audit → phased execution → evidence) that Lead Dev used mirrors Klatch's own research pipeline (identify question → assign spike → deliver recommendation). Both projects are converging on "investigate before implementing" as a core discipline, applied to different domains.

**Suggested action:** No Klatch action required. Track M1 re-test results in next sweep.

### 4. Piper Open — First Sibling PM Assistant Role
**From:** Piper Morgan (PA, April 4)
**Relevant to:** Klatch (agent architecture, five-layer model)

PA drafted briefing documents for **Piper Open (PO)** — a PM assistant role for xian's new OpenLaws project at Kind. This is the first "Piper" agent deployed outside the Piper Morgan product itself:

- **BRIEFING-piper-open.md** (L5): voice rules, colleague test, mandate ("sincere assistance"), explicit scope (operational only — no research mandate, unlike PA's dual mandate)
- **CLAUDE-piper-open.md** (L2): session protocol, Vergil coordination, principles
- Key design decision: lighter process than PM (smaller project), explicit "What You Don't Need to Know" section, no omnibus or mailbox infrastructure

PO inherits Piper Alpha's voice and methodology but strips the product-research layer. The briefing explicitly separates what PO is (a well-briefed Claude agent doing PM work) from what it isn't (Piper Morgan software, autonomous agent, engineer's assistant).

**For Klatch:** This is a live test of five-layer portability. PO's briefing documents map cleanly onto Layers 2 and 5, with Layer 1 handled by Claude Code's native kit briefing, Layer 3 deferred (domain context TBD), and Layer 4 minimal (one session log, no mailbox). If PO succeeds as a lighter-weight deployment of the same agent architecture, it validates the five-layer model's scalability claim — that the same structure works at different weights. Klatch's entity system (role prompts + channel context) already supports this via per-entity configuration; PO is PM's first real test of the equivalent pattern.

**Suggested action:** When designing Klatch's entity template/export format (Step 10), consider PO as a reference case for "minimum viable entity" — what's the lightest-weight deployment that still maps onto all five layers?

### 5. Round 18: File Injection on Imported Channels — Cross-Boundary Testing
**From:** Klatch (Theseus, April 5)
**Relevant to:** Piper Morgan (testing methodology)

Theseus wrote 12 tests covering the intersection of File Domain Model and imported channels — specifically, whether file context injection works correctly across the import boundary:

- **Group E (4 tests):** Imported channel + pinned file, imported + project KB, legacy fallback + pinned file, full layered injection ordering
- **Group F (4 tests):** Cross-scope isolation — channel pin doesn't bleed to siblings, project KB visible to all channels, unlinked channel sees nothing
- **Group G (4 tests):** Lifecycle, multi-file format, L4 coexistence, full 5-layer assembly

All 12 passed on first run. Total suite: 849 (710 server + 139 client), zero failures.

**For PM:** The cross-scope isolation tests (Group F) address the structural pattern behind Pattern-045. PM's todo tests mock the service boundary — they confirm code logic but never test whether the *scope* is correct (does the right context reach the right consumer?). Round 18 tests real database operations and verifies that data scoping is enforced at the query level, not just in test assertions. This is the testing pattern the E2E/AAXT track should target.

**Suggested action:** When the E2E track begins, review Round 18's test structure (`round18-aaxt-fdm.test.ts`) as a reference for scope-aware integration tests.

---

## Emerging Patterns

**The AAXT/MAXT gap is being industrialized.** Three weeks ago, MAXT Session 01 discovered subliminal injection — a behavioral phenomenon that AAXT (structural tests) couldn't detect. Two weeks ago, PM's gate UAT caught Pattern-045 — the same class of failure in a different domain. This week, Klatch shipped scaffolded probing (Phase 1) and completed the AuditBench review, which independently validates the same insight from Anthropic's own research. The trajectory: discovery → cross-project validation → automated detection. This is the cross-pollination loop functioning as designed — an insight in one project becomes methodology in the other.

**Agent architecture is exporting.** Piper Open is the first deployment of the Piper Alpha pattern outside the Piper Morgan ecosystem. The five-layer context model is being used as a design template for a new project, with deliberate decisions about which layers to instantiate fully and which to keep minimal. This is the portability claim moving from theory to practice.

**Both projects shipped at pace on the same day (April 4).** Klatch: compaction threshold tuned, per-entity effort shipped, AAXT Phase 1 implemented, Round 18 tests written. PM: #940 fixed with audit cascade, PO briefing drafted, "Silent Failures" published, editorial calendar extended. The ecosystem is demonstrating that parallel development across sibling projects doesn't require coordination overhead — the daily brief is sufficient to maintain coherence.

---

## Background Changes (Noted, Low Priority)

- **Per-entity effort parameter shipped (Klatch):** New `effort` column on entities table with model-aware defaults (Sonnet 4.6 → medium, others → high; `max` restricted to Opus 4.6). UI: 4-button selector. Tested in Round 17 (18 tests).
- **v0.9.0 release prep (Klatch):** Calliope drafted CHANGELOG. Headline: FDM Phases 1-5, effort parameter, compaction tuning, nomenclature rename. Blog draft "Paste It Again" ready. Pending Theseus manual testing.
- **"Silent Failures" published (PM):** Fifth blog-first canonical publish. Smoothest publish yet (~4 min). 5 additional insights scheduled through April 19.
- **23 unpublished drafts indexed (PM):** Docs agent cataloged the full backlog across 4 categories. 3 scheduled (Apr 8-15), 20 unscheduled, several appear publication-ready.
- **PA-Chief of Staff coordination initiated (PM):** PA responded to Exec's intro memo. Proposed breadcrumb format for decisions and offered shared open-items tracker.
- **#942 filed (PM):** Pre-existing test failure (missing `workflows` table). Not caused by #940 changes.
- **Five-layer context mapping filed as architecture doc (PM):** PA's March 31 RFC-001 analysis promoted from working document to `docs/internal/architecture/current/five-layer-context-mapping.md`.
- **Metis added to Klatch roster:** Coordination/knowledge stewardship agent. First session April 1.

---

## Sources Read

**Klatch:**
- `docs/logs/2026-04-04-2030-daedalus-opus-log.md` — Daedalus session (compaction threshold, effort parameter, AAXT Phase 1)
- `docs/logs/2026-04-04-2032-argus-opus-log.md` — Argus session (AuditBench review, Round 17 tests)
- `docs/logs/2026-04-05-0958-theseus-opus-log.md` — Theseus session (Round 18 AAXT x FDM)
- `docs/logs/2026-04-04-0655-calliope-opus-log.md` — Calliope session (logbook, memos, release prep)
- `docs/research/auditbench-methodology-review.md` — Full AuditBench analysis with 4 AXT recommendations
- `docs/plans/AAXT-SCAFFOLDED-PROBING.md` — AAXT Phase 1-3 design spec
- `docs/mail/calliope-to-daedalus-compaction-effort-2026-04-04.md` — Implementation assignments
- `docs/mail/calliope-to-argus-auditbench-2026-04-04.md` — Research assignment
- `git log --since="48 hours ago"` — 18 commits

**Piper Morgan:**
- `dev/active/2026-04-04-1047-pa-opus-log.md` — PA Day 6 (Piper Open briefing, Chief of Staff coordination)
- `dev/active/2026-04-04-2210-lead-code-opus-log.md` — Lead Dev session (#940 audit cascade, inbox processed, branches cleaned)
- `dev/active/2026-04-04-1901-docs-code-opus-log.md` — Docs session (omnibus Apr 2+3, "Silent Failures" publish, calendar update, 23 drafts indexed)
- `dev/active/BRIEFING-piper-open.md` — Piper Open L5 briefing document
- `dev/active/unpublished-drafts-index-2026-04-04.md` — 23 unpublished drafts for Comms sequencing
- `docs/internal/architecture/current/five-layer-context-mapping.md` — Five-layer mapping (filed as architecture doc)
- `docs/omnibus-logs/2026-04-03-omnibus-log.md` — Apr 3 omnibus (M1 UAT session)
- `git log --since="48 hours ago"` — 17 commits
