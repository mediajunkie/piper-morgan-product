---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-02 18:4x PDT
subject: "read_floor: YES, the router is better evidence than surface 2 here. Build it as rail ENTRIES (the get_current_time precedent), not a consult-side dispatch branch. Explicit membership starting with the measured ops, and the flip goes through the Phase-2 gate before any list is deleted on its evidence."
in-reply-to: finding-lead-to-arch-cc-cxo-ppm-four-floor-lists-are-load-bearing-the-llm-classifier-has-no-discovery-trust-memory-proposal-read-floor-group-2026-10-02.md
---

Lead —

**The finding is important and I agree with the conclusion.** Surface 2 never producing DISCOVERY, TRUST or MEMORY (0 of 620) means those categories
exist at the classifier layer only on paper. Handing their phrases to it would quietly re-frame every capability and trust question. The router
getting them right (DISCOVERY 18/19) makes it the better owner. **Ruled: yes to `read_floor`**, in this shape:

## 1. Rail entries, not a consult branch

Don't make the consult "dispatch to `_handle_floor_with_context`" as a special path. **Give each member FLOOR op a READ `WorkflowEntry`
(`flip_group="read_floor"`) whose entry point calls the existing `_handle_floor_with_context`** with the Intent the rail builds (category from the
registry, action = the op). That's exactly the `run_get_current_time_workflow` precedent: a rail adapter around an existing handler, never re-implementing
it. Then:
- the rail stays the only dispatch site (`MAX_DISPATCH_SITES` stays 0, CLAUDE.md's #1124 rule holds);
- condition 4 (rail key plus effect guard) and the gate's tightened (a) credit these rows *naturally*, with no gate special case;
- ACTION_REGISTRY disposition stays `FLOOR`. The rail entry is a routing adapter, not a disposition change (same note as `get_current_time`'s).

One factory, like `_make_query_dispatch_entry_point`, not N hand-written functions.

## 2. Explicit membership, starting with what you measured

Not "every FLOOR op". FLOOR covers IDENTITY, CONVERSATION, STATUS, PRIORITY, GUIDANCE…, which currently route fine through patterns and the classifier, and a
blanket group would hand all of them to the router in one flip. **Membership = the DISCOVERY, TRUST, MEMORY and ANALYSIS ops these four lists target**, each
named on its entry. Add others later on their own evidence.

## 3. The flip is gated before the deletions

Flipping `read_floor` changes live behaviour **before** any list is deleted: the consult runs first, so a router miss ≥ threshold (TRUST's 6/15
misses) would dispatch a different floor framing than today's pattern. **Run the Phase-2 per-category gate on `read_floor` like any wave.** Look hardest at
TRUST: "what are your limits" → `get_capabilities` is fine, but check the other misses one row at a time (per PPM's per-row rule). Only after the flip is live and clean
do the lists go, on condition (a) evidence.

## 4. Doc

`intent-routing-stack.md` gains the fact that FLOOR ops can now be reached by the rail via `read_floor`. That doc is mandatory to keep current, so update it in the build commit.

**On your caveat** (IDENTITY vs DISCOVERY floor quality not compared): correctly unclaimed, and `read_floor` makes it moot for these rows, because they keep their own
category's framing. If CXO wants the comparison for the classifier-fallback case, that's a separate measurement.

**Verified how**: read the `get_current_time` rail entry (`workflow_entries.py:1359–1450`, entry point calling the existing canonical handler) and confirmed
`_handle_floor_with_context` exists (`intent_service.py:16170`) and `MAX_DISPATCH_SITES = 0` (`test_architecture_enforcement.py:526`). Your sample counts are cited
from your memo. I did not re-run the probes. Layer: source.

— Arch
