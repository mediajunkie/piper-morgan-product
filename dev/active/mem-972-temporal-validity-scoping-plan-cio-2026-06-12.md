# MEM-972 Temporal Validity — Scoping Plan (CIO)

**Author**: CIO · **Date**: 2026-06-12 · **For**: PM review → then execute · **Issue**: [#972](https://github.com/mediajunkie/piper-morgan-product/issues/972) (CIO-owned)

**What this is**: a concrete plan for *how* to add "is this still true / what replaced it" metadata to our docs, so stale guidance becomes detectable instead of a trap an agent steps in. Not the implementation — the plan + the decisions that are yours.

---

## Why now — two drivers

1. **Internal staleness is actively biting.** The 6/12 migration *alone* threw three incidents where an agent acted on, or nearly acted on, guidance a newer doc had already superseded: the stale §5 worktree instruction (9h out of date vs. the same-day plan-of-record), the stale "Model A" operating-model line, and a stale cron-prompt embedding the old schedule. Each would have been caught instantly by a "this was superseded on DATE by X" marker.
2. **It's a precondition for the BYOC multi-user work.** Once Piper serves more than PM, "whose fact, and is it still valid?" becomes a real governance gate (flagged in the phase-2 ratification). Temporal validity is the structural floor under cross-user synthesis.

## The core design — a lightweight field set (not full bi-temporal)

Four fields, extending what briefings already carry. Keep it minimal:

| Field | Required? | Meaning |
|---|---|---|
| `valid_from: YYYY-MM-DD` | expected on operating docs | when the fact/guidance became true (briefings already have this) |
| `valid_until: YYYY-MM-DD` | optional | when it stops being true / a review horizon. Absent = "current until superseded" |
| `superseded_by: <path or id>` | optional | pointer to what replaces this. **The load-bearing one** — a stale doc that names its replacement is self-correcting |
| `last_verified: YYYY-MM-DD` | **expected** (PM 6/13: flipped to B) | when content was last *confirmed current* (distinct from `last_updated` = last *edited*); drives the staleness check — **this is what catches *silent* staleness** (un-reviewed-too-long), the most common kind |

*Why minimal, not the academic gold standard*: the Zep/Graphiti bi-temporal model (valid-time + transaction-time, the issue's arxiv reference) is more than we need. Our actual question is "still true? / what replaced it?" — these 4 fields answer it. Field **names** get aligned with Janus before we apply (below).

## The real lever — detection, not just fields (m-36: mechanism beats vigilance)

Fields alone do nothing if no one reads them. The payoff is a **`check-staleness.py` lint** that flags: any doc past its `valid_until`; any doc whose `last_verified` is older than its staleness horizon; any doc with `superseded_by` set that is *still being referenced*. Wire it the way `check-acronyms.py` (glossary lint) and the delta hook already work.

**Behavior — PM-ratified 2026-06-13: warn + capture-a-task + fix-asap.** Not block-on-commit, but stronger than warn-only: each finding doesn't just print a warning — it **produces a tracked, fix-asap task** so the warning can't be ignored (the warn-only failure mode, closed). Task-sink is a P1 design detail (candidates: the finding role's `standing-items` / `duty-cycle-escalations`, a GH issue, or a session-surfaced task). This converts staleness from "hope an agent notices" into "a prioritized task lands in the queue" — mechanism-over-vigilance, *with teeth*.

## Surface inventory — prioritized by staleness-risk (i.e., where the incidents happened)

| Surface | Has it now? | Action | Executes |
|---|---|---|---|
| Operating-model docs (CLAUDE.md worktree/cron §, plan-of-record) | no | **highest priority** — incidents were here; add `valid_from` + `superseded_by` | CIO |
| Cron prompts / bootstrap briefs | no | add `valid_from` (the stale-§5 / stale-cron-prompt class) | CIO |
| Briefings (CURRENT-STATE, ESSENTIAL-*) | **partial** (`valid_from` + `last_updated`) | formalize + add `superseded_by` / `last_verified` | Docs |
| Memo format guide | no | add temporal fields to the template | Comms/Docs |
| Session-log instructions | no | reference temporal validity | CIO/Docs |
| Agent auto-memory (`.md` frontmatter) | no (has `type:`) | add `valid_from` / `superseded_by`; **3 examples** (satisfies the issue AC) | CIO |
| Methodology / ADR / patterns | varies | opportunistic backfill | CIO |

## Sequencing (phased)

- **P0 — spec + Janus align (~½ session)**: ratify the 4-field convention; one memo to Janus to align field names (Klatch's Step 10 Phase 1 adopts the same structure → compatible schemas = the cross-project context-interchange protocol works).
- **P1 — highest-risk surfaces + the lint (~1 session)**: stamp operating-model docs + cron prompts/briefs; ship `check-staleness.py`. This is where the incidents happened → biggest ROI, do it first.
- **P2 — briefings + memo guide + session-log instructions (~1 session, Docs-led)**: formalize on briefings; memo template; session-log convention; the 3 agent-memory examples.
- **P3 — opportunistic backfill + cohort norm**: methodology / ADR / patterns as touched; a CLAUDE.md norm line.

## Effort + what's already done

~3 working sessions for P0–P2; P3 is ongoing. **Not greenfield** — briefings already carry `valid_from` + `last_updated`, so most of this is formalize-and-extend. The one real build is the lint (~a `generate-delta.py`-sized script).

## Decisions — PM-ratified 2026-06-13

1. **Lint severity → warn + capture-a-task + fix-asap.** Not block-on-commit; stronger than warn-only — every finding produces a tracked, fix-soon task. (See "The real lever" above.)
2. **Scope → all operating docs** (briefings, bootstrap briefs, cron prompts, plan-of-record, CLAUDE.md) + memory files. Not memory-files-only.
3. **Required fields → `valid_from` + `last_verified`** expected (on operating docs); `valid_until` / `superseded_by` optional. **(PM flipped to B, 6/13.)** `last_verified` is what lets the lint catch *silent* staleness — a doc nobody's re-confirmed — which is the most common kind and the one that bit us. The upkeep (bump `last_verified` when you confirm a doc still current) is a small habit, worth it.

*This plan + these decisions are the ratified spec. P0–P1 execute against it.*

## Status (2026-06-13)
- **P0 — spec ratified** ✓ (the 4-field convention + the 3 decisions above). **Remaining in P0**: Janus field-name alignment memo — *needs PM's cross-project bridge or the cross-pollination channel; CIO doesn't have a direct Janus mailbox.* Flagged for PM.
- **P1 (next, top CIO-queued)** — stamp the operating docs + build `check-staleness.py` with the warn+capture-task behavior. A focused build pass (not a tail-of-session task).
- **P2** — Docs-led (briefings formalize, memo-guide, session-log instr, 3 memory examples).

---

*Next step on PM nod: I execute P0 (ratify spec + Janus memo), then P1. Docs picks up P2's briefing/memo-guide pieces.*

---

## Janus/Klatch field-name alignment — RESOLVED via direct dinp read (2026-06-15)
PM authorized reading the dinp repo directly (`~/Development/designinproduct`), so the alignment no longer needs a Janus mailbox. The canonical cross-project memory schema is the **April 12 Janus synthesis** (six-tier framework; `valid_from`/`type`/`source`/`trust_level` field set), and the dinp briefs carry an explicit standing intent: *"share the spec so PM and Klatch memory schemas stay compatible."* So #972 should be **mutually compatible with Klatch** (the dinp memory system, built by Daedalus), not just internally consistent.

**Field-by-field (PM #972 vs Janus/Klatch):**
| concept | PM #972 | Janus/Klatch | verdict |
|---|---|---|---|
| becomes-valid date | `valid_from` | `valid_from` | ✅ exact match |
| staleness re-confirm | `last_verified` | `last_verified` / `last_checked` | ✅ match (`last_verified`) |
| stops-being-valid date | **`valid_until`** | **`ended`** (synthesis) / `validUntil` (one variant) | ⚠️ **the one divergence** |
| replaced-by link | `superseded_by` | (none — Janus uses `ended` to invalidate) | PM extension; keep |
| provenance | (not in #972) | `type` / `source` / `trust_level` | beyond #972's temporal scope — note for a future provenance pass (ties to HOST trust boundaries + BYOC consent) |

**The one decision (needs PM's cross-project bridge to Janus/Daedalus): `valid_until` vs `ended`.** Recommendation — **keep PM's `valid_until`**: the symmetric snake_case pair `valid_from`/`valid_until` is clearer than `valid_from`/`ended` ("ended" is ambiguous), and Janus's own usage is already inconsistent (`ended` in the synthesis, `validUntil` elsewhere) so there's no firmly-settled name to defer to. Propose Janus/Klatch adopt `valid_until` for symmetry. (Accept `ended` only if Daedalus has shipped it irreversibly.)

**Action**: share the #972 4-field spec to the dinp side for mutual compatibility (the standing intent) — needs PM's bridge to Janus/Daedalus, or routing via the cross-pollination channel.

**Status**: Janus-align *investigation* DONE (this finding). Two bits remain, both PM-bridged: (a) the `valid_until`-vs-`ended` decision, (b) sharing the spec to dinp. P0 otherwise complete; **P1 (stamp operating docs + build `check-staleness.py`) is unblocked + next.**
