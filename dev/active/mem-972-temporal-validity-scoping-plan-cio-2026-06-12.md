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
| `last_verified: YYYY-MM-DD` | optional | when content was last *confirmed current* (distinct from `last_updated` = last *edited*); drives the staleness check |

*Why minimal, not the academic gold standard*: the Zep/Graphiti bi-temporal model (valid-time + transaction-time, the issue's arxiv reference) is more than we need. Our actual question is "still true? / what replaced it?" — these 4 fields answer it. Field **names** get aligned with Janus before we apply (below).

## The real lever — detection, not just fields (m-36: mechanism beats vigilance)

Fields alone do nothing if no one reads them. The payoff is a **`check-staleness.py` lint** that flags: any doc past its `valid_until`; any doc whose `last_verified` is older than its staleness horizon; any doc with `superseded_by` set that is *still being referenced*. Wire it the way `check-acronyms.py` (glossary lint) and the delta hook already work. This converts staleness from "hope an agent notices" into "the check tells you" — the same mechanism-over-vigilance move that's worked everywhere else.

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

## Open questions — yours to call

1. **Lint severity**: warn-only (like the delta signal) or block-on-stale (like the `check-branch` hook)? *I lean warn-only first, escalate if it's ignored.*
2. **Scope**: just "memory files" (the issue's literal wording) or all operating-instruction docs (briefs, prompts, plan-of-record, CLAUDE.md)? *The incidents argue for the broader scope; I lean broad — the staleness that hurt us today was in operating docs, not memory files.*
3. **Required vs optional**: I propose only `valid_from` is effectively-expected (on operating docs); the other three optional. *OK, or do you want `last_verified` expected too (it's what makes the lint useful)?*

---

*Next step on PM nod: I execute P0 (ratify spec + Janus memo), then P1. Docs picks up P2's briefing/memo-guide pieces.*
