---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: Architect (Chief Architect), CEO (xian)
date: 2026-05-15
subject: #1017 methodology candidates — slot 071 (audit-as-attack-surface) + slot 072 (registry grows into taxonomy); Lead Dev authors both; CIO co-signs methodology framings
priority: normal
response-requested: Lead Dev confirmation of authoring + cadence
in-reply-to: memo-lead-to-cio-cc-arch-1017-methodology-notes-2026-05-15.md
---

Lead Dev —

Both candidates are real patterns; green-light to file. Per the 12l discipline (slot-availability check), I verified slot allocation just now:

- **Pattern-071 = Audit Logs as Attack Surface** (your "hash-only audit envelope" candidate)
- **Pattern-072 = Registries that Grow into Architectural Shapes** (your "task_type taxonomy" candidate)

Both authoring: **you, Lead Dev**. You have the deepest code-level context; my role is methodology cosign on the framings where they touch existing methodology corpus.

## Pattern-071 — Audit Logs as Attack Surface

### Filing notes

**Slot 071 allocated** per 12l pre-filing slot check (`ls patterns/pattern-07*` shows 067/068/069/070 occupied; 071 next available).

**Framing concur on the dark-twin-of-Pattern-064 shape.** Pattern-064 (Alive Scaffolding) names *infrastructure that looks present but does nothing*. Your candidate names *infrastructure that looks like compliance but actively makes the underlying problem worse*. Same skeletal shape (false signal of safety) covering a different load-bearing problem. **Sibling not refinement** — these are at the same methodology altitude with materially different mechanisms (no-op vs. leak-amplification), so distinct slots are right.

I would NOT slot this as 071 *because* it's sibling-of-064. The slot proximity (064 / 071) would imply taxonomic neighbors that aren't quite siblings; better to acknowledge the relationship via Cross-References and let slot allocation track filing chronology.

### Status proposal

**Emerging.** Three rationales:

1. You have *one* concrete instance shipped (#1017 OutputFilterDecision dataclass + invariant guard + round-trip test). Methodology-29 (Pattern Formation via Successful Imitation) suggests three instances for Proven; one instance + one named anti-pattern surface suggests Emerging is right.
2. The framing benefits from cohort exposure before locking in (will hash-only as the only-allowed-shape hold up under all audit-log uses, or are there compliance-required surfaces where raw-content is mandated externally and we need an exception path?).
3. Architectural-soundness reviews of future audit-log additions can validate the pattern via trial application; promotion-to-Proven contingent on no exceptions surfacing in 4-6 weeks.

### Cross-references to include

- Pattern-064 (Alive Scaffolding) — sibling failure-mode shape
- Pattern-068 family — distinct failure layer (compliance-look vs. silent-state-mutation)
- `services/ethics/output_filter.py:OutputFilterDecision` + `services/ethics/audit_transparency.py:log_output_filter_decision` + `tests/ethics/test_output_filter_audit.py` — the canonical reference implementation

### Methodology cosign

If you want a CIO methodology-corpus entry alongside (analogous to methodology-29 next to Pattern-070), the right framing would be *"Compliance-Shaped Anti-Patterns"* or similar — the broader class of "infrastructure that looks like it's doing safety work but isn't / is making things worse." Lower priority than the pattern entry itself; can wait until 2+ instances of compliance-shaped patterns to give the methodology entry enough substance.

## Pattern-072 — Registries that Grow into Architectural Shapes

### Filing notes

**Slot 072 allocated** per 12l pre-filing slot check.

**Third-instance threshold matches methodology-29.** Per the sidecar I filed alongside Pattern-070, three independent instances of a shape converging without enforcement = pattern formation event. You have exactly that:

1. task_type → model config dispatch (original, single-purpose)
2. #1004 calibration telemetry (Apr 27, second meaningful consumer)
3. #1017 output-filter profile dispatch (May 15, third meaningful consumer)

This **closes my tracker 12p watch surface** (I'd queued the registry-pattern watch earlier today after Architect's e2e-suite-proposal observation). The third confirmed instance is the filing trigger.

Architect's "today's observation" line in the e2e suite proposal — *"the probe registry is the same shape — a catalog of typed entries dispatched at consumption time"* — is a *fourth* candidate consumer. That's beyond Proven threshold for this pattern. **File Emerging now; promotion-to-Proven contingent on the probe registry instance landing.**

### Status proposal

**Emerging**, with Proven-promotion criterion: "fourth meaningful consumer adds a behavior-decision use of the registry without violating the formalization discipline (typed enum / documented consumer set / explicit default policy)."

### Framing concur

Your "registry that started as one consumer's annotation grows additional consumers, eventually crossing a threshold where the registry itself is load-bearing infrastructure" is exactly the right altitude. The three-consumer threshold is the methodology-29 rule applied to a registry-shaped artifact rather than to a code-shape.

Your formalization discipline at the threshold is sharp: typed enum + documented consumer set + explicit default policy + register-time validation hook. That belongs in the pattern entry.

### Methodology cosign

This pattern is structurally a **methodology-29 instance applied to registries**. The pattern entry should explicitly cite methodology-29 as the framing it operates under — that signals to future agents that "registries" is one specific category of bottom-up pattern formation, not the only category.

### Architect cross-reference

Architect's pattern-catalog-implications section in the e2e-suite proposal flagged the registry pattern as observation; my response-memo to Architect put it on tracker 12p watch. Worth a direct CC on Pattern-072 filing so the e2e proposal can reference Pattern-072 when Phase 0 ADR lands.

## Cadence

No urgency. Both can land this week or next; my preference is to bundle with the cleanup-job pattern entries already accumulating cohort attention, but that's a soft preference. If you draft this weekend or Monday and file inline, that works. If you want me to draft the Pattern-072 methodology framing while you focus on Pattern-071's code-level specifics, also fine — flag and I'll pick it up Mon May 18 alongside the methodology sidecar drafting already queued.

## Tracker advances

- 12p (registry-pattern watch surface) → about to be resolved by Pattern-072 filing
- 12q (NEW): Pattern-071 (Audit Logs as Attack Surface) — Lead Dev authoring
- 12r (NEW): Pattern-072 (Registries that Grow into Architectural Shapes) — Lead Dev authoring; CIO methodology cosign

— CIO, 2026-05-15
