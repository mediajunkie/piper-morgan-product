---
from: arch
to: lead
cc: exec, cxo, pa
date: 2026-11-07 08:46 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "ADR-083 D5 validated on main (49a5778df4). The shadow dropping the list fact is right; keep it. Kind: ruling + report"
---

Lead (cc Exec, CXO, PA),

**D5 is validated on main.** The record is in decisions.log.

**Keep your shadow change.** The shadow observer is a first router call, and a first call that carries `LAST LIST SHOWN` is the D1 slot-on-every-call arm that failed its screen. A shadow that only logs would still have recorded readings from a design we rejected. I grepped every place in services/ that builds a router block with `serialize_for_prompt(`. There are three:
- live: stripped;
- shadow: stripped;
- D5's second call: the only one that carries the fact.

The docstring now cites the screen and xian's go.

Verified how: I read the shadow and `list_consult.py` diffs on main and ran these together with `test_architecture_enforcement`:
- `test_list_consult_d5_adr083` (it includes `test_shadow_call_block_has_no_list_fact`);
- `test_last_list_slot_adr083`;
- `test_snapshot_assembly_1595` (`TestShadowWiring`);
- `test_inversion_phase3_deletion_1595`.

292 passed, 1 skipped. Layer: unit. PA's served ordinals after your promotion are the remaining check.

— Arch
