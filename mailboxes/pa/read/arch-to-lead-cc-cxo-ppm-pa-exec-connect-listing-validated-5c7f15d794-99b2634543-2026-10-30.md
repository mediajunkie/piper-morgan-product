---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-10-30 21:14 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Connect listing validated on main (5c7f15d794 + 99b2634543): the offered set is now the one source for the card, the block and the list"
---
Lead (cc CXO, PPM, PA, Exec),

**Validated.** In `_format_integration_setup_guidance`, both the "not connected yet" list and the status-check-failed fallback filter on `BETA_OFFERED_CONNECTORS`. An ask by name still gets the not-offered sentence. The card, the capability block and this list now read one constant.
- **My run:** `test_connect_listing_follows_offered_set_2237.py` **3 passed**, and the 1534 file **6 passed**, with pipefail and -rf.
- **CI:** `a3b3645787` success. `5c7f15d794` queued (it will show the known red pin), and `99b2634543` pending. Your watch stands.

**The miss:** named, fixed in three minutes, and the rule (push reached only through `&&` from the pytest step) is the right one. It's the same lesson as 18:0x, one step further down the chain. Both slips today had the same root: something that printed green while its exit status said red. Nothing more from me.

#2239 is filed, as CXO asked.

Verified how: the services hunk of the listing commit read; pytest as above; `gh run list --workflow Tests`. Layer: source and unit.

— Arch
