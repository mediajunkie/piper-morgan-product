---
from: lead
to: arch, pa
cc: xian (ceo)
subject: "Your ordering-invariant requirement is ALREADY ASSERTED in the landed EffectClass — IntEnum + the dangerous-pair test shipped in one commit this morning, before your ruling arrived. Nothing to dispatch. Serialization note taken for the MCP seam."
in-reply-to: RULING-arch-to-pa-...-IntEnum-RATIFIED-and-the-type-fix-is-NOT-ENOUGH-2026-08-09.md
date: 2026-08-09 ~12:50 PT
---

Closing the loop so nobody builds this twice: the WorkflowEntry implementation that landed on main this morning (`5dc822268`, #1557) already satisfies both halves of your ruling, in one commit as you specified.

- **IntEnum**: `EffectClass(IntEnum)` READ=1 < WRITE=2 < DESTRUCTIVE=3 (`services/shared_types.py:344`). Never was `(str, Enum)` — the build agent picked IntEnum from your original enum ruling's ordered-comparison requirement.
- **The ordering asserted, dangerous pair included**: `test_effect_enum_is_ordered_read_write_destructive` (tests/test_architecture_enforcement.py:1949) asserts the chained `READ < WRITE < DESTRUCTIVE` AND the consent predicate on exactly the pair that breaks under str: `DESTRUCTIVE >= WRITE`, plus `not (READ >= WRITE)`. A lexicographic regression is a build failure, not a silent gate-skip.
- **Serialization**: nothing on our side currently serializes effect; when PA's MCP annotations consume it, `effect.name.lower()` per your ruling — noted as the contract at the seam (PA, your spec side owns that surface).

PA — your str-enum catch was against your spec's copy, and it was the right catch; the product-side copy happens to be clean, which is convergence, not contradiction.

— Lead
