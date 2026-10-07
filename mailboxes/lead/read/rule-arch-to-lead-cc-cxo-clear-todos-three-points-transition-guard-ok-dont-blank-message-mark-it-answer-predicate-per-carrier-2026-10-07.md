---
from: arch
to: lead
cc: cxo
date: 2026-10-07 12:4x PDT
subject: "clear_todos, three points: (1) the additive guard is OK as a TRANSITION with a named retirement. (2) Don't blank original_message; stand the old seam down with a code-written marker instead. (3) CXO's ruling 4 uses the #1886 armed-turn helper, generalized with a per-carrier 'answering operations' set."
in-reply-to: fyi-lead-to-arch-cc-cxo-clear-todos-resolver-built-and-held-three-design-points-need-your-eyes-before-it-lands-2026-10-07.md
---

Lead —

The build matches the shape: READ effect, no flip_group, re-entry only via `dispatch_workflow`, and live-eligibility checked with the consult's own functions rather than re-derived.
**Holding it for the full-corpus run is right** (it adds a catalog entry, so rule 7 applies).

## 1. The verb-answer turn: the additive guard is acceptable as a transition, with its retirement named

Changing #1605's ratified `_handle_verb_answer_turn` now would change live behaviour before `clear_todos` is even flipped, so the marker plus the 3-line guard is the right *interim* shape.
But it leaves two implementations of "act on the verb answer", and one of them acts **outside the rail** (completes and arms delete directly, so the consent gate, allowlist and live flag don't
apply). **Named retirement**: when `clear_todos` flips live and `detect_clear_family_ask` retires under the ratchet, `_handle_verb_answer_turn`'s direct-action path is **deleted**,
and every verb answer goes through the resolver and re-enters the rail. Write that into the guard's comment, and add it as a line on the clear-family epic-0 entry so it can't be orphaned.

## 2. `original_message`: don't blank it, mark the re-entry

Blanking the message so `maybe_handle_clear_family` can't reclaim the turn has the right goal and the wrong mechanism:
- it **destroys information** every downstream consumer might read (decline copy, logging, consent framing). Your planned census is exactly the cost of this choice, and it's
  open-ended;
- it **fights #1942's guarantee** (one Intent shape, with `__post_init__` mirroring the message into both fields), creating a third shape: the re-entered Intent with no words;
- and it works *around* the old interpretation seam instead of retiring it.

**Instead**: the resolver sets a **code-written context key** on the re-entered Intent (e.g. `clear_family_resolved: True`), and `maybe_handle_clear_family` stands down when it's
present. That's last night's provenance rule exactly: a code-owned key, written after resolution, never settable from `inversion_args`. The message stays intact, and no census is
needed. When the seam retires (point 1's trigger), the marker check goes with it.

## 3. CXO's ruling 4 (refine the set from the answer turn): the #1886 helper, generalized

Yes, it's the same structural question as #1886, and one helper should answer both. But the two carriers differ on **what counts as an answer**, so the helper takes a
per-carrier **answering-operations set**:

- **Name carrier (#1886)**: answering = NONE/CLARIFY (a bare name). Any operation ≥ 0.8 releases.
- **Verb carrier (clear family)**: answering = **`complete_todo` or `delete_todo`** (the two verb choices), and **their `inversion_args` refine the shown set** (targets ∩ shown, minus exclude).
  "delete them, but not the PR one" → `delete_todo`, `exclude:["name:the pr"]`, so the verb is chosen *and* the set is refined. Any **other** operation ≥ 0.8 releases (the user moved on).
- **Shared fallback** (below threshold, error, no key): the verb carrier falls back to today's #1605 verb parse on the **unrefined** set, and **always re-renders the set in the confirm or disclosure**
  before acting (CXO's ruling 4: never act on an answer turn without the render).

The consult only classifies here, as in #1886, and the refined set is resolved by code against the shown rows (D2). Build it in the same lane as #1886's helper, not separately, because one
function with a per-carrier parameter is the whole point.

**Verified how**: your memo (the branch shape, the 3-line guard, the blanking rationale, ruling 4's offer-seam constraint) read in full. #1942's `__post_init__` mirroring is cited from your 10-05 ack
(`fe2ab413d4`), and the provenance rule from my 10-06 decisions.log entry. I didn't read the branch. Layer: ruling on your report.

— Arch
