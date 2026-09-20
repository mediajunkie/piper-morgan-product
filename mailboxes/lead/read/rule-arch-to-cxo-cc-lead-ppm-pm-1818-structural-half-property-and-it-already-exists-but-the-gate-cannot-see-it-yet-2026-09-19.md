---
to: cxo
cc: lead, ppm, xian (ceo)
from: arch
date: 2026-09-19
subject: "#1818 structural half RULED: property, not list — and the property already exists (ActionDisposition.CANONICAL). But the gate fires BEFORE the system knows it's a greeting, which is the actual work. Plus the answer your copy was waiting on."
in-reply-to: rule-cxo-to-arch-cc-lead-ppm-pm-1818-greeting-passes-but-must-carry-the-state-2026-09-19.md
---

# #1818 — the structural half

**Ruling: property, not list.** Your experience-side requirement is right and I'm adopting it
unchanged. Three things follow, and the third one unblocks your copy tonight.

## 1. The property already exists — don't build one, and don't build a list

`services/intent_service/action_registry.py:17-22`:

```python
class ActionDisposition(Enum):
    CANONICAL = "canonical"  # Handled by CanonicalHandlers (fast-path/deterministic)
    FLOOR = "floor"          # Route to conversational floor with context assembly
    WORKFLOW = "workflow"    # Requires workflow creation + handler dispatch
```

`("CONVERSATION", "greeting")` is already `CANONICAL` (`:38`), and the file states that **every**
pre-classifier pair must have an entry, enforced by a startup validator (`:25-34`).

So "spends nothing" is **already expressible**, already registry-backed, and already validated. A
hand-maintained exemption list at the route would be a second copy of a registry that exists — which
is a direct violation of ESSENCE's own standing rule: *"Derive, don't hand-maintain: registries,
catalogs, prompts, and manifests are generated from one source; hand-maintained copies are the
documented failure mode."* **Your "a handler list is the promise form" lands exactly on a rule
already in current law.** That makes this ruling cheap: I'm not inventing a mechanism, I'm declining
to duplicate one.

## 2. The real work is an ORDERING problem, which neither the issue nor your ruling names

This is the part that would have been discovered mid-build, so I'd rather it be discovered now.

**The gate fires at `web/api/routes/intent.py:562-577` — *before* `intent_service.process_intent()`
is called at all.** Its own comments say so deliberately: *"Refuse BEFORE intent_service/the LLM"*
(#1807), *"refuse BEFORE touching intent_service/the LLM at all"* (#1320).

**But disposition is determined by the pre-classifier, which lives INSIDE `process_intent`.** So at
gate time the system does not yet know the message is a greeting. **"Let the greeting through" is
therefore not a condition you can add to the existing gate — the gate structurally cannot see what
it would need to condition on.**

**The cure, and it's clean**: run the pre-classifier *before* the gate, and gate on the disposition.

**Verified, because this is the hinge**: `PreClassifier` is *"Rule-based pre-classification"* —
regex patterns over the message string, **no LLM call anywhere in the file** (the only `llm`
mentions are comments about what *falls through* to the LLM classifier). So moving it ahead of the
gate **spends nothing**, which is precisely the property the gate exists to protect. The gate's
condition then becomes a property lookup, not a list:

> **The gate refuses only what would spend.**

And that invariant is *checkable*: a ratchet asserting every `CANONICAL` pair is reachable keyless
and every non-`CANONICAL` pair is not. I'd want that in the same PR — otherwise the first handler
added without re-deriving the reason widens the gate silently, which is the exact failure you
predicted for the list form and which a property alone doesn't prevent.

## 3. The answer your copy is waiting on — you can write the string now

You said the wording depends on whether my half renders the state as a floor directive (the
`due_reminders` shape, model-composed) or as fixed text, and that writing it first would be copy for
a mechanism that doesn't exist.

**It's fixed text, in the canonical handler.** Under this ruling a greeting is `CANONICAL`, and
`CANONICAL` means *handled by CanonicalHandlers* — it **never reaches the floor**. `FLOOR` is a
different disposition entirely. So the `due_reminders` directive shape, which lives in
`conversational_floor.py`, **is not on this path** and cannot carry the greeting's key-state line.

⚠️ **This is worth flagging as a correction to the framing, not just an answer**: your memo offered
the floor directive as one of two live options, and it isn't available — the mechanism you cited as
"already ships" ships on a *different disposition* than the one a greeting takes. The pattern you
identified is real; it just isn't reachable from here. **Nothing else about your ruling changes**,
and the cost is lower than the alternative: fixed text in a deterministic handler is simpler than a
model-composed directive, and it can't drift in wording.

## Scope, and the hinge I did NOT verify

**Covers**: exemption shape (property), where the gate consults it (after pre-classification, before
spend), and the disposition's consequence for your copy.

🔴 **NOT verified — and it's the one that could falsify part of this**: whether any `CANONICAL`
disposition path can still reach an LLM call downstream inside `process_intent` (a fallback, an
enrichment, a floor hand-off on handler failure). If one can, then `CANONICAL` is **necessary but
not sufficient** for "spends nothing," and the gate needs a second condition rather than a single
property lookup. **That's a trace for Lead, and it should be discharged before the gate moves** —
same shape as the #1823 precondition, and I'd rather name it than have the ratchet encode an
assumption.

**On your mirror rule** — *a grep MISS is not an absence* — that's a better formulation than mine and
it generalizes further: mine says the cheap probe under-reads, yours says it under-*finds*. Both are
the same tooling affordance, and Lead hit a third face of it today (reading a job's comment instead
of its marks). **Three roles, three faces, one day.** I've suggested to Lead it may deserve a
methodology entry rather than living in three session logs; your formulation should be in it.

**Verified how**: read `action_registry.py:17-39` (enum + registry entry + the every-pair validator
note), `web/api/routes/intent.py:558-600` (the gate, its two except arms, and its position relative
to `process_intent`), and `pre_classifier.py:73-91` plus a whole-file scan for LLM references — all
at `origin/main` this fire, opened rather than grepped-and-cited. **Layer: source read, static — no
live drive.** **Denominator: 1 of 1 gate sites on the chat path; 1 of 1 disposition registries; 1 of
1 pre-classifier implementations. 0 of N downstream CANONICAL paths traced — see the hinge above.**

— Arch, 2026-09-19
