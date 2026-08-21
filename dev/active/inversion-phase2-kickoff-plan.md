# Inversion Phase 2 kickoff plan — the per-category flip

**Lead, 2026-08-18 evening. This is the PREP artifact: written at the tail of a long tactical day
so tomorrow's FRESH session starts building in minutes, not re-deriving. The build itself is
deliberately not started tonight (quality-banking, trigger named: fresh session).**

**Canonical phase naming (per #1595's epic body — do not drift)**: Phase 0 corpus ✅ · Phase 1
shadow-behind-flag ✅ (live, async sampled) · **Phase 2 = flip per-category, queries first,
writes last, writes keep confirmation** · Phase 3 = pattern-router deletion via
delete-module-safely. "SessionSnapshot threading" is Phase 2's FIRST work item, not its name.

## Work items, in order

### 2.0 — SessionSnapshot (the context the router has never had)
A small, deterministic, cheap-to-assemble snapshot threaded into the inversion routing call:
- **Armed state**: pending offer kind + its open question (the #846 store's head), active process
  (registry.any_active), draft-in-compose state. THIS kills the turn-theft/orphaned-answer class
  structurally — the router can finally see "an answer is expected."
- **Recent referents**: the #1394 session ledger heads (last created/touched issue, last reminder
  set) — same source B3 uses, read-only.
- **Declared mode + stored verbs** (the #1510/#1605 stores): so routing respects standing prefs.
- Shape: a frozen dataclass, assembled in process_intent where the shadow-check already runs;
  serialized compactly into the constrained call's context block. Budget: <500 tokens.
- Tests: snapshot assembly unit-pinned per field against real stores (the #1621 idioms); a
  golden serialization pin so prompt drift is visible in diffs.

### 2.1 — Corpus gate rerun with snapshot-aware shadow
Re-run the standing shadow with snapshots attached; the corpus now includes every live deposit
through 08-18 (colon-form, #1527 shapes, exception-clauses, aside-vs-answer turns). Gate to beat,
per Arch's Phase-1b baseline: 33/39 vs baseline 36/39 WITHOUT context — the snapshot should flip
the armed-state cases (the current router's principal loss class). Honest per-category table
(m-44 denominators) before any flip.

### 2.2 — Flip order (queries first, writes last, per the epic)
1. READ/query categories with zero armed-state interaction (status, listings, identity) — lowest
   risk, highest volume.
2. READ categories with referents (issue detail, analyses) — exercises snapshot referents.
3. SYNTHESIS flip includes GRAMMAR REPRESENTATION for issue/commit summarize shapes (PA's
   08-18 crack, verified 08-19: document-summarize entered the grammar with #1624; the
   issue/commit shapes still ride the floor with no operation — a day-one BYOC gap in PM's
   named parity area if left).
4. TEMPORAL/reminder parsing LAST among queries (the #1572 clock work may land meanwhile).
5. WRITE categories last, confirmation-gated exactly as today — decide_consent unchanged; the
   inversion proposes, the consent gate disposes. DESTRUCTIVE flips only after a full green week.
Each flip: per-category flag, shadow-vs-live disagreement telemetry to corpus, one-command revert.

### 2.3 — What Phase 2 must NOT touch (standing rulings)
- Floor-honesty contract work is DECOUPLED (Arch ruling in the epic — ships against current floor).
- #1555 surface-1 self-inconsistency survives the inversion — separate lane, never a copied branch.
- The action rail + handlers + consent gates are the STABLE substrate — the flip changes who
  chooses the key, never what the key does.

## Gates before any category flips live
- 2.1's table shows the snapshot-aware shadow ≥ baseline per category being flipped (not aggregate).
- The supersession-gate ledger stays clean (no new surface-1 patches smuggled in as "prep").
- PM informed per flip wave; flips are deploy-visible in the tracker with revert noted.

## BYOC alignment note (from the 08-18 strategic brief)
Everything in 2.0–2.2 builds the artifact BYOC would expose: the grammar is the tool inventory;
the SessionSnapshot is the tool-context contract; the consent gate is the differentiator. If the
PA conversation chooses BYOC, Phase 2's work re-targets, none of it discards.

## 2.2 CONTRACT ADDENDUM (post-#1663 ruling, Arch 2026-08-19 — binding)

**Emission convention: (b), ratified.** On an armed turn the router may emit the armed flow's
completing operation; the POP SEAM consumes flow-matching emissions as VALIDATED HINTS (binding
the answer via the flow's own answer-handler) — never fresh-dispatched. Non-matching emission on
an armed turn → the seam's existing re-ask. Structural, not conventional: the bad state
(fresh-dispatch off a fragment) stays unrepresentable because pop-before-classify-before-dispatch
is code-verified (intent_service.py:1024, Arch-checked).

**Arch's required condition**: before wiring ANY flow's completing-operation binding, confirm
PER FLOW that the arm-time question is adequate confirmation for the operation's EffectClass.
Never transitively assumed. DESTRUCTIVE-completing flows keep their explicit confirm INSIDE the
binding (the answer routes to the handler, the handler still confirms). #1666 is the cautionary
precedent: delete_todo currently has NO gate — do not build its binding until #1666 lands.

**Flip-1 scope (buildable now)**: zero-armed-state READ categories only (status/listing/identity
class) — live routing call behind a per-category flag set that is DEFAULT-EMPTY (nothing flips
without an explicit config change; revert = unset), legacy fallback on REFUSED or sub-threshold
confidence, disagreement telemetry to the corpus either way. The seam-consumption amendment is
NOT needed for flip-1 (no armed turns in scope) — it builds with the first armed-capable flip.

**Corpus re-expression**: the armed rows' expectations restate per the flow-matching reading
(expected = the armed flow's operation family, with the aside still expecting NONE) — done as
part of the seam-amendment build, with the 2.1 doc left as the historical record of the
convention question.

## FLIP-UNIT DESIGN DECISION (#1667, Lead, 2026-08-20 — measured, not assumed)

**The measurement that forced this**: most rail READ keys are unreachable by a category flag.
⚠️ **My original figure here was 23 of 93 addressable, and it was measured against the wrong
mapping** — the #1667 build's audit caught it (2026-08-20): 23/93 counts ACTION_REGISTRY's own
action names only, but `inversion_live._category_by_operation` ALSO back-maps through
`grammar.alias_to_canonical`, so the number governing LIVE behavior is **33 of 93 addressable,
60 unaddressable**. The conclusion is unchanged (a category flag still can't reach ~2/3 of READ
ops, and #1667's "a few ops" was off by an order of magnitude) — but the corrected figure is the
one to quote. Kept visible rather than silently overwritten: a decision doc that edits its own
evidence without saying so is the shape we keep catching elsewhere.

**Rejected — (a) register 70 ops into ACTION_REGISTRY**: that registry exists for canonical
action vocabulary, not routing policy. Bulk-registering ops to make a flag work bends a
subsystem to a purpose it doesn't hold, and its invariants (canonical/alias discipline, the
#1433 reachability ledger) would absorb 70 rows of pressure for a reason unrelated to them.

**DECIDED — (b) the flip unit is declared ON THE RAIL ENTRY, and the flag accepts either.**
`WorkflowEntry` gains `flip_group: Optional[str]` — declared exactly where `effect` and
`outwardness` already live, per the #1509 precedent (declare on the entry; derive everything
else). `PIPER_INVERSION_LIVE_CATEGORIES` (name kept; semantics widen, documented) accepts
**group names OR individual operation names** — so a surgical one-op flip needs no group, and a
wave flips by naming its group. Registry categories remain valid inputs where they exist (no
regression to flip-1's pins).

**Why this is the honest shape**: the thing being flipped is *routing for an operation*, and the
operation's identity lives on the rail. A flip unit derived from a different subsystem's
taxonomy was a borrowed proxy — it worked for 23 ops and silently covered nothing for 70. The
same m-44 shape as everything else this month: the mechanism reported coverage it didn't have.

**Groups for wave 1** (assigned by risk, not convenience): `read_status` (status/listing/
identity — zero armed-state interaction), `read_referent` (issue/PR detail, analyses — exercises
snapshot referents), `read_synthesis` (summarize family incl. PA's issue/commit gap when built).
Ops not in a group are unaddressable BY DESIGN until someone assigns one — a deliberate opt-in,
and `--audit` output must list them so "unassigned" is never invisible.
