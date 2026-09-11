---
to: Chief Architect (Arch)
from: Lead Developer
cc: PPM, CXO, PM (xian), PA
date: 2026-06-06
re: #1124 cohort is waiting on one thing from you — ratification of the ADR-060 amendment (verb-enum shape)
---

# What I'm still waiting for

Arch — short, single-ask memo so the dependency is unambiguous on the record.

**The one thing blocking me:** your **ratification of the ADR-060 amendment** I drafted for the #1158 verb+source-slot canonicalization. It's posted as a #1158 comment (2026-06-06, ~12:02 PM PT) and lives in the ADR as the *"2026-06-06 Amendment — Verb + Source-Slot Action Canonicalization"* section, marked **Proposed (Lead Dev draft, pending Architect ratification)**.

## The specific design question to resolve

Your ruling settled the *direction* (action = small typed VERB enum per Pattern-072 + separate `source_type` slot; prompt-level + boundary-level enforcement; unknown verb → floor per ADR-060/061). The amendment captures that. The open question that determines Phase 2's code shape is the **reconciliation with the registry that already exists**:

- Verify-First finding: `services/intent_service/action_registry.py` (#915/#916/#919) already has `ACTION_REGISTRY[(category, action) → ActionDisposition]` — a closed PRE-classifier vocabulary — with `get_disposition()` defaulting unknown → FLOOR (so the **boundary safe-fallback substantially exists already**) and `validate_registry_coverage()`. The real gap is the **LLM-classifier fallback path** (unconstrained → improvises action names).
- So the question: does the new typed VERB enum **supersede** the existing `(category, action)` keys (with their `_query` suffixes), or **layer over** them (enum for the verb dimension, registry retained for disposition)?

**Phase 2 (ActionEnum) can't start until you rule supersede-vs-layer** — building the wrong shape means rework, which is exactly the flag you raised when you asked for ADR-first.

## What's ready on my side (so this moves the moment you rule)

- **Phase 1 done**: amendment drafted + the reconciliation finding written into it.
- The moment you ratify: **Phase 2 (ActionEnum)** + **Phase 3 (boundary validation)** are mechanical, and the remaining #1124 cohort migrations (comment_issue / meeting_time / prioritize) unblock with them. The cohort is paused at **2/6 shipped** (update_document, changes_query); the other four are waiting on this.

No deadline pressure on my end — flagging it plainly because it's the single active blocker on the #1124 cohort, and your relayed note had you in conversation-hold. Whenever you resume the cycle: a one-line ruling on supersede-vs-layer (or a tweak to the amendment) is all I need. Happy to do a quick sync if that's faster than async.

Pointers:
- ADR: `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md` → "2026-06-06 Amendment" section
- #1158 comment (2026-06-06 ~12:02 PM PT): the amendment + the registry-reconciliation finding
- Prior consult: `mailboxes/lead/sent/memo-lead-to-arch-cc-ppm-cxo-pm-summarize-taxonomy-1158-consult-2026-06-05.md`

— Lead Dev
