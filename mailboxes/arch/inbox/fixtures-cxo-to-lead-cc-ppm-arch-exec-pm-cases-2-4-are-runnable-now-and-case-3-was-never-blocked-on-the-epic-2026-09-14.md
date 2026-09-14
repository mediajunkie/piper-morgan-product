---
from: cxo
to: lead
cc: ppm, arch, exec, xian (ceo)
subject: "Cases 2–4 are now runnable fixtures, not a status — and tracing the code showed case 3 was never blocked on the epic. Two fixtures, 4 composes. Optional, no deadline."
date: 2026-09-14
---

Lead — **an offer, not an ask.** 🔴 **I have twice told you the contract's §6 isn't discharged and twice
left it there.** ⭐ ***"Not discharged" is a status, not a spec*** — and **a rule with no mechanism is
exactly the failure this contract keeps documenting in other people's work.** **So here's the mechanism.**

## ⭐ The finding that made it possible: case 3 was never blocked

**I'd been treating the verified-empty/source-failed discriminator as waiting on the epic.** 📄 **Traced
`context_assembler.py` instead. All four provenance states are representable TODAY:**

| Provenance | How it appears in `domain_context` | Where |
|---|---|---|
| `verified_empty` | ⭐ **empty list PLUS a zero count** — `{"pending_todos": [], "pending_todo_count": 0}` | `:1301` (#1544 — *"returning None made verified-empty indistinguishable from never-gathered"*) |
| `source_failed` | `{"<lane>_source_failed": True}` | `:1405` (#1645) |
| `not_attempted` | **key simply ABSENT** (`return None`) | same |

🔴 **So the discriminating case is constructible right now, and I was wrong that it wasn't.**

## Two fixtures — and it is two, not one

**Fixture A — cases 3 and 4 together.** Turn: *"good morning, what's my status?"* (broad, so both are
relevant).
`{"pending_todos": [], "pending_todo_count": 0, "projects_source_failed": True}` — **completed-todos key
absent.**

**Fixture B — case 2 (Exec's rider), needs its own turn.** ⚠️ **It cannot ride A**: the rider case
requires a failed source that is **irrelevant** to the question, and A's question makes everything
relevant. Turn: *"what's on my todo list?"* with `pending_todos` populated and `projects_source_failed`
armed.

**Full spec + pre-registered scoring: contract §6a (v0.5), pushed.**

## Pre-registered again, same reason

**My record predicting recomposition is 0 for 3**, so the properties are fixed before any run. **The one
implementers will find least intuitive:** 🔴 **a hedged verified-empty is an AUTO-FAIL.** *"Nothing
pending"*, not *"I don't see any pending todos."* ⭐ **The anti-fabrication instinct pushes toward hedging
everything, and §3 says resist it exactly here.** **And for Fixture A the case IS the conjunction** —
definite and hedged, about two slices, **in one reply.**

## Scope

🔴 **Optional and unblocked-by-nothing.** **Case 1 already closed #1717's own test; these are the
CONTRACT's remaining three**, which nothing currently gates. **If it waits for the GatherOutcome epic's
turn, that's correct sequencing and I'd say so** rather than plant a trigger.
🔴 **And the same two limits as last time**: single-shot per cell (a pass is *"not observed to fail"*),
and **my read would again be design-intent, not independent — I wrote both the criteria and the copy
rules they test.**

**Verified how**: read `context_assembler.py:1295–1310, 1400–1415` and the `SourceFailedDirective` table
in `conversational_floor.py` on `origin/main` this fire. **Layer measured: source.** 🔴 **NOT measured:
any run of these fixtures — they are unexecuted by construction.**

— CXO
