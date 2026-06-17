---
title: MEM-EVAL Corpus Analysis — Gameplan
status: GAMEPLAN (CIO, 2026-06-17) — pre-execution; audit-cascaded before Phase 1
owner: CIO (analysis lead); co-owned Docs (pilot owner) + HOST (trust lens)
related: #1272 (analysis tracking) · #974 (pilot, CLOSED) · standing-items 12e · docs/internal/operations/memory-eval-pilot.md
last_updated: 2026-06-17
---

# MEM-EVAL Corpus Analysis — Gameplan

**One line:** aggregate the 135-session 3-bucket MEM-EVAL corpus → classify every context surface as **load-bearing** (keep always-loaded), **dead-weight** (move to demand-load), or **gap** (create/surface), producing progressive-loading recommendations (token-efficiency, PM ultra-high) + trust-property findings (HOST lens). **Propose-and-diff only — no auto-trim.**

## Why this is gameplan-first + audit-cascaded (PM 2026-06-17)
Session-sized (135 logs), and the depth risks going off the rails mid-run. The gameplan + the subagent prompts + the tracking issue are committed **before** Phase 1, so the work is **resumable after interruption** (a killed session re-reads this doc + the captured Phase-1 scratch and continues) and **bounded** (the audit-cascade catches plan/prompt drift before it compounds across 135 logs).

## Objective + the two downstream decisions (from the pilot tracker)
1. **Progressive-loading optimization** — which surfaces are load-bearing vs dead weight? Trim/relocate what nobody references → fewer always-loaded tokens/fire (PM ultra-high priority).
2. **Trust-property surfacing (HOST lens)** — when "loaded but not referenced" is a *trust gap* (a surface that SHOULD be load-bearing but isn't being used) vs a stable dead-weight signal.

## Scope + inputs
- **Corpus**: 135 session logs under `dev/2026/` carrying `## Memory & briefing surfaces referenced this session` (3 buckets: Referenced / Loaded-but-not-referenced / Wanted-but-not-found), across ~10 roles, 2026-05-25 → 2026-06-17.
- **Reference**: `docs/internal/operations/memory-eval-pilot.md` (pilot design); #974 (closed).
- **Out of scope**: actually trimming/relocating surfaces (that's the *implementation* follow-up issue, propose-and-diff, owner-gated). This analysis RECOMMENDS only.

## Lane
CIO leads (progressive-loading + token-efficiency = CIO innovation lane). **Co-owned**: Docs (pilot owner — "what Docs does at evaluation time" is in the tracker; I loop Docs with findings + offer co-authorship) + HOST (trust-lens half — the should-be-load-bearing-but-unreferenced findings). Neither is a blocker to the analysis; both get the findings + a voice on disposition. Don't unilaterally deprecate a surface another role owns — recommend + route.

## Method (4 phases; each commits → resumable)

### Phase 1 — Gather (parallel subagents; the heavy, parallelizable part)
Split the 135 logs **by role** (clean partition; role-spread is a key classifier so per-role tallies are needed anyway). Dispatch one gather-subagent per role-cluster. Each returns **structured data only** (no prose, no session log) → a per-surface tally. Capture each subagent's return to a durable scratch file (`dev/active/mem-eval-gather-{cluster}-2026-06-17.json`) immediately on return, so a mid-Phase-1 interruption loses at most one cluster.

**Gather-subagent prompt (template — parameterize {ROLE-CLUSTER} + {LOG-GLOB}):**
> You are a data-extraction subagent (no session log needed; return structured data only). Read every session log matching `{LOG-GLOB}` (these are {ROLE-CLUSTER}'s logs). In each, find the `## Memory & briefing surfaces referenced this session` section and its three sub-buckets (Referenced / Loaded but not referenced / Wanted but not found). Extract each named surface. **Normalize surface names** to a canonical form: a file path (`docs/briefing/PROJECT.md`), a memory pin slug, a methodology/pattern id (`m-36`, `Pattern-072`), or a CLAUDE.md section — collapse paraphrases of the same surface ("the worktree discipline" → `CLAUDE.md#worktree`). Return JSON: `{role, sessions_count, surfaces: [{name, referenced, loaded_not_ref, wanted, example_note}]}` where the three counts are how many of this role's sessions placed the surface in each bucket. Flag any surface you couldn't confidently normalize in a `ambiguous: []` list. Do NOT trim/judge — just tally.
> **Acceptance criteria (address each in your return):** (a) every log matching the glob was read; (b) the 3-bucket section was located in each log (or the log noted as lacking it); (c) every named surface in all three buckets was extracted + normalized to canonical form; (d) un-normalizable surfaces are in `ambiguous`. **Evidence to include in the return:** `logs_read` (int), `logs_with_section` (int), `surfaces_extracted` (int), plus the `ambiguous` list. Return **data only** — no prose, no session log, no code, no judgement of trim-worthiness (that's Phase 3, CIO).

### Phase 2 — Aggregate (CIO, in-session)
Merge the per-cluster JSON → a master per-surface table: `surface → {total_referenced, total_loaded_not_ref, total_wanted, role_spread (# distinct roles referencing), first_seen, last_seen}`. Reconcile the `ambiguous` lists into the canonical surface set. Commit the master table to the analysis doc.

### Phase 3 — Classify (CIO)
Per surface, assign:
- **Load-bearing** — high referenced + broad role_spread → keep always-loaded.
- **Dead-weight** — high loaded_not_ref + low referenced (across roles, not one) → recommend demand-load (move out of always-load).
- **Gap** — appears in Wanted-but-not-found → recommend create/relocate/surface.
- **Trust-flag (HOST lens)** — *should* be load-bearing (safety/discipline/identity surface) but consistently loaded-not-referenced → not a trim candidate; a trust/surfacing problem for HOST.

### Phase 4 — Recommend + route (CIO)
Write the analysis report: the master table + the four classification lists + concrete progressive-loading recommendations (the proposed always-load set / demand-load set / create set) + token-savings estimate. File the **implementation follow-up issue** (propose-and-diff; owner-gated per surface). Memo Docs (pilot owner, co-author offer) + HOST (trust-flags).

## Assumptions verified before building (Phase-1 analog — audit-cascade)
- **Corpus exists + size**: 135 logs carry the 3-bucket section (`grep -rl "Memory & briefing surfaces referenced" dev/2026/` confirmed 2026-06-17).
- **Format**: the `## Memory & briefing surfaces referenced this session` 3-bucket schema (pilot tracker confirms).
- **Inputs readable**: pilot tracker + #974 read.

## Success criteria
- Every surface appearing in the corpus is classified into exactly one of {load-bearing, dead-weight, gap, trust-flag}.
- A concrete recommended **always-load set / demand-load set / create set**, each with the evidence (counts + role_spread) behind it.
- A **token-savings estimate** for the demand-load recommendations (the PM-ultra-high payoff).
- Docs (pilot owner) + HOST (trust lens) looped with findings.
- Implementation filed as a **separate owner-gated child issue** (propose-and-diff) — this analysis ships recommendations, not removals.

## Phase estimates (rough) + validation
~5 gather subagents (P1, parallel/minutes) · P2 aggregate ~1 fire · P3 classify ~1 fire · P4 recommend+route ~1 fire; phase-boundary commits → spans fires safely. **Validation ("test" analog):** normalization spot-check (~10 names across clusters collapsed correctly + `ambiguous` reconciled not dropped); role-spread sanity (no load-bearing call on a single role's count); recency check (flag May-only surfaces); total reconciliation (Σ per-cluster sessions == 135 — no cluster silently dropped).

## STOP conditions (escalate to PM, don't push through)
- >~20% of surfaces un-normalizable → canonical approach too loose; STOP before classifying on noise.
- 3-bucket format varies enough across roles that extraction is unreliable → STOP + report the format-drift (itself a finding).
- A recommendation would trim a **safety / identity / discipline** surface on low-reference-count → STOP; that's a HOST trust-flag, never an auto-trim.

## Outputs
- `docs/internal/operations/memory-eval-analysis-2026-06-17.md` (master table + classification + recommendations).
- Phase-1 scratch: `dev/active/mem-eval-gather-*.json` (durable; resumability).
- A GH issue for the analysis (tracking) + a child issue for **implementing** the progressive-loading changes (propose-and-diff).
- Memos to Docs + HOST with findings.

## Risks / off-the-rails guards (what the audit-cascade must check)
1. **Surface-name normalization** — agents name the same surface many ways; without normalization the aggregation is garbage. → the gather prompt mandates canonical normalization + an `ambiguous` list; Phase 2 reconciles.
2. **Raw-count ≠ load-bearing** — a surface referenced 50× by ONE role isn't cohort-load-bearing. → classify by **role_spread**, not raw count.
3. **Recency** — early-pilot (May) data may reference now-stale surfaces. → record first_seen/last_seen; weight recent; flag surfaces only-referenced-early.
4. **No auto-trim** — the output is propose-and-diff; never auto-remove a surface (a load-bearing-but-rarely-logged surface, e.g. a safety guard, could look dead). HOST trust + careful-with-shared-state. Implementation is a separate owner-gated issue.
5. **Lane** — don't deprecate surfaces other roles own; recommend + route to owners.
6. **Subagent token blowup** — 135 logs is large; per-cluster splits bound each subagent; subagents return tallies (small), not log contents.

## Resumability (the resilience contract)
- This gameplan is committed before Phase 1. A resumed session reads it + the `mem-eval-gather-*.json` scratch to see which clusters are done.
- Phase boundaries commit. Phase 1 captures each cluster's JSON on return.
- The tracking issue records phase status.

— CIO, 2026-06-17
