---
title: MEM-EVAL Corpus Analysis — Findings + Progressive-Loading Recommendations
status: ANALYSIS (CIO, 2026-06-17) — #1272; Phases 2–3 done; Phase 4 (route + child issue) in progress
gameplan: docs/internal/operations/memory-eval-analysis-gameplan-2026-06-17.md
corpus: 134 session logs (3-bucket section), ~11 role-slugs, 2026-05-25 → 2026-06-17
method: 5 parallel per-role gather subagents → normalized per-surface tallies → CIO aggregate+classify
guards: propose-and-diff ONLY (no auto-trim); classified by role-spread not raw count; trust-flags routed to HOST
---

# MEM-EVAL Corpus Analysis — what's load-bearing, what's dead weight, what's missing

**Completeness:** all 134 corpus logs read (clusters 26/26/26/26/30 = 134 ✓). 6 logs had the section present but unfilled (stubs/`(filled at STOP)`) — counted, contributed 0 surfaces. (Phase-1 gather subagent ids retained for re-query/audit: `ac6f97a666be825a5`, `afc6dc75e34cf043a`, `ac92eb2938c184e49`, `a042418843509ff96`, `ab2a5bb50bfdb6839`.)

## The headline (token-efficiency, PM ultra-high)
**`MEMORY.md` is the #1 dead-weight surface — and it's already over its own size limit.** It's loaded every session (all roles) but landed in *loaded-but-not-referenced* 5–11× per cluster, with only ~8–10 pins active per role at any time; the harness itself flags it at **40.7KB vs a 24.4KB limit** (truncated-load warning). Trimming/relocating the index is the single biggest progressive-loading win.

## Load-bearing — KEEP always-loaded (high referenced + broad role-spread)
These earned their always-load slot — referenced across many roles:
- **`duty-cycle-tick` skill** — the most-referenced surface in the corpus (17/6/6/8/4 across clusters; every cycling role).
- **`CLAUDE.md`** (mailbox / worktree / sign-off / Verify-First / keychain / env-strip sections) — heavy, all roles.
- **The 4 load-bearing memory pins** (broad role-spread, high ref): `feedback_pre_authorized_for_unblocked_work_just_do`, `feedback_make_promises_durable_no_happy_talk`, `feedback_investigate_before_extending_all_work`, `feedback_no_confabulating_expected_steps_as_completed`.
- **methodology-30 / -36 / -41** — load-bearing for the methodology-active roles (cio/arch/host/docs/exec).
- **Per-role carry-forward + standing-items** — the primary continuity surfaces (exec-cf 9×, pa-cf 6×, comms-standing 5×). (These are read on demand already, not global — correct.)
- **cron-lifecycle / cron-shape-experiments** — load-bearing for cycling roles.

## Dead-weight — recommend DEMAND-LOAD (high loaded-not-referenced, low ref, across roles)
The token-savings set. **Recommendations are propose-and-diff — owner-gated, no auto-trim.**
| Surface | Signal | Recommendation |
|---|---|---|
| **`MEMORY.md` full index** | loaded-not-ref 5–11×/cluster; ~10 pins active/role; over size limit | **Trim the index + role-condition pins**: keep a small always-load core (the 4 pins above + role-specific actives); demand-load the rest. Biggest win. |
| **`PROJECT.md`** | loaded-not-ref 14× total, **referenced 0** | demand-load |
| **`ROSTER.md`** | loaded-not-ref, ref ~0 | demand-load |
| **`BRIEFING-CURRENT-STATE.md`** | loaded-not-ref 6/2/3/7/9, low ref | demand-load OR see trust-flag below |
| **Role briefings `BRIEFING-ESSENTIAL-*`** | role re-anchor at START then loaded-not-ref (arch 8×!) | acceptable as a one-shot START read; don't keep resident after START |
| **Publishing / blog / voice / Ship-drafting pins** | load-bearing for **comms only**; loaded-not-ref for host/pa/lead/ppm/arch (8× for pa) | **role-condition**: load for comms; demand-load for everyone else |
| **`cross-pollination/current.md`** | load-bearing for PA/CIO cross-project; loaded-not-ref 4–8× elsewhere | role-condition (load for PA/CIO; demand-load others) |
| **MCP toolset catalogs** | loaded-not-ref 6–9× (most roles never invoke them) | harness-level (deferred-tool model already helps); flag, don't own |

## Gaps — Wanted-but-not-found (create / surface)
The biggest cluster was **duty-cycle continuity infra — and most are now CLOSED by recent work**:
- "durable cron survives session suspension / Gap-C watchdog" (wanted **8×** by cxo + others) → **CLOSED**: the launchd freeze-registry (shipped 6/15–17, closed→never-restarted fix today).
- "which-roles-are-migrated authoritative signal" (cio) → **CLOSED**: plan-of-record migration table (now kept current).
- "missing-session-log alarm" (docs), "who-is-cron-live tracker" (cio/docs) → partially covered by the freeze-registry.

Still-open gaps worth filing:
- **Live board-state surface** (`read:project` / live M3 board) — wanted 4× by lead (reconstructs M3-remaining by hand). Real, recurring.
- **canonical-retest history table** (per-date pass/fail/error counts) — wanted 2× by lead ("is 12 env-errors normal?").
- **canonical ops recipes** — ephemeral-worktree server-launch, integrations connect-flow map, GH-Actions-scheduling debug (each reconstructed from tacit knowledge).

## Trust-flags (HOST lens — should-be-load-bearing but under-referenced)
- **`BRIEFING-CURRENT-STATE.md`** — heavily loaded-not-referenced. Two readings: (a) agents trust it's fresh without checking, or (b) it's stale-so-ignored. Either is a HOST trust question, not a clean trim — **routed to HOST** (don't demand-load it purely on the count until HOST weighs in).
- Role briefings loaded-not-ref *after* START = **not** a trust gap (one-shot re-anchor is the correct usage pattern).

## Recommended progressive-loading change set (the proposal)
1. **`MEMORY.md`**: split into a small always-load core (4 cross-role pins + per-role active pins) + a demand-loaded archive; fixes the over-limit + the dead-weight in one move.
2. **Demand-load**: `PROJECT.md`, `ROSTER.md` (ref ~0 across the corpus).
3. **Role-condition**: publishing/voice/Ship pins → comms; cross-pollination → PA/CIO.
4. **HOST review**: `BRIEFING-CURRENT-STATE` (trust-flag, not a pure trim).
5. **File**: the still-open gaps (live board-state, canonical-retest history, ops recipes) as their own issues.

**Token-savings estimate**: dominated by the `MEMORY.md` trim (~16KB+ over-limit already truncating) + `PROJECT.md`/`ROSTER`/non-role pins moved off always-load — a material per-fire reduction across all ~11 cycling roles. (Exact bytes pending the implementation diff.)

## Lane / next (Phase 4)
- Implementation is a **separate owner-gated child issue** (propose-and-diff per surface) — filed off #1272.
- **Docs** (pilot owner) + **HOST** (trust-flags) get this analysis + a voice on disposition.
- Per-surface owners gate their own trims (no unilateral deprecation).

— CIO, 2026-06-17
