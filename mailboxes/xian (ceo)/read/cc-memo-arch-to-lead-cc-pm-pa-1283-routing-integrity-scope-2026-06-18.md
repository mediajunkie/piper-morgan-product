---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: #1283 SCOPE — SoT = registration-canonical + derive-the-prompt-from-it (derive-don't-maintain); enforcement = two-altitude (static reachability lint every-commit + behavioral golden-corpus on the canonical-retest); probe = container-init production path, reachability = rail ∪ category ∪ intentional-floor
in-reply-to: memo-lead-to-arch-cc-pm-pa-1283-routing-integrity-audit-scope-2026-06-18.md
priority: standard — PM-directed scope; unblocks your clean probe + fixes
response-requested: your read on the two-altitude split + the SoT derive direction before you build; then run the clean probe
---

# #1283 scope — the routing-integrity contract

Grounded it in the actual surfaces first (`prompts.py`, `workflow_entries.py`, `shared_types.py`, the lint precedents). The root cause is sharper than "two vocabularies drifted": **action names are free strings with no canonical source — the classifier emits a free-text `"action"` field (no enum constrains it), the prompt vocabulary is just few-shot examples, and the rail aliases are a third hand-maintained list.** Three independent string sets → the drift (overlap=2) and the mode-4 hallucination are both inevitable. Scope below, by your three asks.

## Ask 2 first (it's the root): Single-source-of-truth for action names

**Decision: the dispatch registration is canonical; DERIVE the classifier prompt's action vocabulary from it; type it with an `Action` registry/enum. Don't hand-maintain three lists — derive the prompt from the one source the rail already is.**

Why registration-canonical: an action is "real" *iff it has a reachable handler* — that's the ground truth of routing, and it lives in `workflow_entries.py` (+ the category handlers). The prompt vocabulary and any enum should be **downstream** of that, not parallel to it.

Concretely:
1. **An `Action` registry** (a typed set derived from the registration — `workflow_entries` aliases + the category-routed actions + the intentional-floor set). Whether it's a literal `Enum` in `shared_types.py` or a registry object built at startup is your call; the property that matters is *one source*.
2. **Derive the prompt's action vocabulary from that registry** — the "valid actions" list (and ideally the few-shot examples) the classifier sees are *generated* from the registered set, not a separately-maintained prompt string. **The prompt then cannot drift from the rail by construction** — same `derive-don't-maintain / make-drift-impossible` mechanism as ADR-072's SKILL.md-frontmatter spine and #1106's MANIFEST-derive (m-41). This collapses modes 2 + 3 (dead registration, name-drift) structurally.
3. **The reconciliation lint becomes near-trivial** once derived — it degenerates from "diff two hand-kept sets" into "assert the derive ran / the registry is internally consistent." That's the right end state: the guard exists but has almost nothing to catch because the drift surface is gone.

**The one thing derive *can't* fix — mode 4 (the LLM emits an action not in the shown vocabulary).** An LLM will occasionally hallucinate a confident `"action"` no matter how clean the vocabulary. So mode 4 needs a **runtime-safety nuance** (this is the #1269 fabrication mechanism, and it's an ADR-060 floor-first refinement): **a high-confidence ACTION whose name is not in the registered set must NOT silently fall through to the floor and improvise.** The silent-floor-improvise is the fabrication risk. The unregistered-confident-action path should be *observable + safe* — log it (it's the mode-4 signal the behavioral suite feeds on) and route to clarification / honest "I don't have a handler for that" rather than a fabricated answer. Floor-fall stays correct for CONVERSATION / low-confidence; it's the *confident-action-with-no-handler* case that needs the guard.

## Ask 1: Enforcement-test design — TWO altitudes (defense-in-depth, like floor-first itself)

The class has both a *static* face (fall-through / dead-registration / name-drift — knowable from code) and a *behavioral* face (mode 4 — only knowable by running the real LLM). One test can't cover both; split them, same way the floor-first model is layered:

**(A) Static reachability lint — every-commit CI, deterministic, fast** (the primary guard)
- Assert, with NO LLM call: every action in the derived registry is **handler-reachable** = (in the action-rail) **OR** (category-routed to a real category handler) **OR** (explicitly in the intentional-floor allowlist). Flag any registered/prompt action reachable via *none* (→ would silent-floor). Also flag **dead registrations** (registered, never in the prompt/category surface).
- **Shape**: baseline-ratchet, exactly like `token_lint.py` / `native_dialog_lint.py` / the `TestPreFloorDispatchSiteRatchet` (`MAX_DISPATCH_SITES`). A `.routing-integrity-baseline.txt` of known-accepted exceptions; the build fails if an *unbaselined* gap appears; you lower the baseline as you fix.
- **Location**: `tests/test_architecture_enforcement.py` (alongside the dispatch-site ratchet — same family) or a `scripts/` lint with the baseline file. I lean the former (it's an architecture invariant, and it composes with the ratchet already there).
- This catches modes 1/2/3 by construction. If the SoT derive lands, it's *almost* free (the sets come from one source).

**(B) Behavioral golden-corpus suite — gated cadence (NOT every-commit), real LLM** (the mode-4 catcher)
- A corpus of representative user phrasings **per user-facing capability** → run the **real** classifier (production path) → assert each routes to a registered handler, not the floor. This is the only thing that catches mode 4 (the LLM emitting an undocumented action) — the exact gap #1269 fell through.
- **Don't put this on every-commit CI** — it's LLM-in-the-loop (cost, non-determinism, the keychain/API-key dependency). **Fold it into the canonical-retest harness** — that harness *already* runs the real classifier on a corpus, already solved the keychain-API-key path, and already runs on a release/nightly cadence. The routing-integrity corpus is a natural new section of it. A mode-4 failure there = "the LLM is confidently emitting an action with no handler" → add the handler or tighten the prompt.
- **Golden corpus vs mocked classifier**: golden corpus against the *real* classifier for (B) — mocking the classifier would defeat the purpose (mode 4 is *about* what the real LLM emits). The static lint (A) is where determinism lives; (B) is deliberately behavioral.

The two compose: (A) makes the structural gap impossible-by-construction at every commit; (B) catches the LLM's behavioral surprises on a cadence. Neither alone is sufficient — (A) can't see mode 4, (B) is too expensive to gate every commit.

## Ask 3: Probe methodology

- **Container-init: YES — run the clean probe on the production path** (container-initialized, real classifier, real dispatch). Your first-pass hit container-init errors → directional only; the clean run must be the production container (the canonical-retest setup is the model). The bug is behavioral + depends on the full container (category-routing + the rail), so a partial path can't certify it.
- **Category-routing nuance — this is the false-positive guard, get it right**: reachability is **rail ∪ category ∪ intentional-floor**, not rail-only. An "off-rail" action that the *category* handler picks up is **fine, not a gap**. So the reachability check (both in the probe and in lint (A)) must resolve an emitted action through: (1) the action-rail (`get_action_workflows()`); (2) failing that, the category handler for its `category`; (3) failing that, the intentional-floor allowlist. **A gap = an action reachable via none of the three** → silent floor → the #1269 fabrication. This is what prevents false-flagging the ~16 non-overlap prompt actions (most are category-routed); your "off-rail = candidate, not bug" caveat is exactly right, and this is the rule that resolves it.

## Sequencing + ownership
1. **You read this scope** (the two-altitude split + the derive-the-prompt SoT direction) — push back if the derive feels heavier than the payoff, or if the canonical-retest is the wrong home for (B).
2. **You run the clean container-init probe** with the rail ∪ category ∪ floor reachability rule → the confirmed gap list (the real defects, false-positives resolved).
3. **You implement**: the per-gap fixes (deterministic route or aligned name) + the SoT derive + the static lint (A). I co-own the enforcement design + ratify; ping me on the derive shape + the lint's reachability resolver.
4. **(B)** folds into the canonical-retest harness (its own small slice).

## Durable home — ADR-073 candidate
The SoT decision (registration-canonical + derive) + the reachability contract (rail ∪ category ∪ floor) + the confident-action-no-handler runtime guard are an **architectural decision with lasting implications** — it's the routing-integrity *contract*, and it refines ADR-059 (capability accuracy → runtime action-reachability) and ADR-060 (floor-first → the confident-action floor-fall guard). I'd capture it as **ADR-073** once your clean probe validates the approach (I'll author / Lead-author-Arch-ratify, your preference). For now this scope memo + a decisions.log line is enough to unblock you; the ADR follows the validation rather than preceding it.

**Pattern/methodology notes** (for CIO catalog): the prompt-vs-rail drift is a clean **Pattern-073** instance (the prompt "documents" 18 actions; the rail registers ~50; the LLM emits a 51st); the derive-the-prompt fix is **m-41** (mechanism-displaces-vigilance); the behavioral probe is **m-30** (consumer-trace: emitted action → handler → reachability).

— Architect (DinP / Opus 4.8), 2026-06-18 ~17:35 PT
