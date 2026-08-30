# The Living Core Document Set — B2 draft v0.1

**Author**: Chief Architect, 2026-08-30 (Reorientation Plan workstream B2, due 09-01 — delivered
a day early to feed Monday's B3 disposition kickoff)
**Status**: DRAFT — feedback window through the B3 kickoff; PM ratifies alongside ESSENCE

## The principle

**Current law lives in six documents. Everything else is history, reference, or scratch.** A
decision is not "absorbed" until its operative content lives in one of these six AND its source
ADR carries an "absorbed into X" marker. New ADRs continue to be written — they are the
append-only history and the reasoning record — but nobody should ever need to read eighty of them
to know what is currently true. This is the demote-don't-retire reform, made concrete.

Every core doc carries CXO's tracked-state frontmatter (`last_updated` / `currency_claim` /
`max_age_days`) and joins the existing staleness checker — the staleness contract is machine-read,
not prose-remembered.

## The six

| # | Document | Owner | Staleness contract | Absorbs (decision classes) |
|---|---|---|---|---|
| 1 | **ESSENCE.md** (exists, v0.1) | Arch | 30d, or same-day on any ratification touching identity/boundary | What Piper IS: the commitments, the for-whom, the NOT-boundary, standing architectural rules |
| 2 | **SYSTEM.md** (new — successor to `architecture.md`, which becomes historical) | Arch authors v1 from Leg B's census during the B3 window; Lead maintains | 30d, or same-commit when a change alters entry points / module classification | Current-state structure: entry points, the module classification (essence/extension/experiment/superseded/dead), background services, deploy topology |
| 3 | **intent-routing-stack.md** (exists, already well-maintained) | Lead | already governed by its own update-in-same-commit rule — formalize with frontmatter | Routing/understanding decisions: surfaces, Inversion state, flip coverage, consent-gate wiring |
| 4 | **data-model.md** (exists, needs correction pass) | Lead | 60d, or same-commit on migration | Schema + domain models. Correction pass fixes the WorkItem dual-definition and adds the todo/reminder/user schemas (Leg D UQ-21, UQ-5) |
| 5 | **CONNECTORS.md** (new, deliberately small) | Arch authors v1; Lead maintains | 30d | Per-connector truth: transport reality (real MCP / shim / dead), grant model (backend-held vs host-mediated, with Bet refs), scope status (live/descoped), the C4 decision rule as the standing test |
| 6 | **piper-morgan-glossary** (exists) | Docs | 60d | Terminology; the alpha-distribution history it already uniquely holds |

**Deliberately NOT in the set**: `PIPER.md` (runtime config, already governed by its own
must-be-implemented rule — it stays runtime-true by a stronger mechanism than any doc contract);
`BRIEFING-CURRENT-STATE.md` (sprint status, not law — different cadence, different owner);
PDRs (product decisions keep their own tier per m-38); the review directory itself (a record,
not law).

## The 24 unanswerable questions, homed

Leg D's UQ backlog maps onto the set (drafted here; each becomes a checklist item in its home
doc's correction pass): **SYSTEM.md** takes UQ-1, 3, 22, 23, 24 (product-of-record, deployment,
spatial value, route inventory, scale targets) · **intent-routing-stack** takes UQ-5, 6, 7, 8
(category enum, low-confidence behavior, actual vocabularies, model assignments) · **data-model**
takes UQ-4, 21 (live-data inventory, missing schemas) · **CONNECTORS.md** takes UQ-11, 12 (push
mechanism honesty, auth flow) · **ESSENCE/bets** already answered UQ-2 (for-whom) · the MCP-path
build docs (PDR-006 companion, when Lead specs it) take UQ-13–16 · **UQ-9, 10, 17, 18, 19, 20**
(trust computation, state machines, ethics mechanism, Colleague Test rubric, scenario content,
web auth truth) get explicit homes-or-deferrals during B3 — flagged now as the residual, not
silently dropped.

## Sequencing

1. This draft circulates with Monday's B3 kickoff (CIO + Docs + Lead cc PM).
2. SYSTEM.md v1 and CONNECTORS.md v1: Arch, during the B3 window (this week).
3. data-model correction pass: Lead, when queue allows — not gating B3.
4. Frontmatter + checker adoption on all six: with each doc's first touch.
5. ADR absorption markers: as B3's disposition processes each ADR — absorb-and-mark is one motion.
