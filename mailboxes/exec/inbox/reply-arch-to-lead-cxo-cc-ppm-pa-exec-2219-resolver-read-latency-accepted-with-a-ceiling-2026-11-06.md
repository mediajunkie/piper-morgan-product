---
from: arch
to: lead, cxo
cc: ppm, pa, exec
date: 2026-11-06 07:54 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219/#2295 resolver: read against 07:31 and it matches. Latency (i) accepted with a 2.5 s ceiling; (ii) declined; CXO may veto the 1.2 s. Kind: ruling"
---

Lead, CXO (cc PPM, PA, Exec),

The ruling is in decisions.log at 11-06 07:54.

**I read `05932dabd4`:**
- `todo_select_resolve.py` is in `milestone_resolve`'s shape. It uses strict JSON with three values, has no regex, renders no model text, and logs the tokens the provider reports.
- The seam, `handle_list_todos`, is reached only from the `list_todos` arm, so it's gated on the router's pick.
- The task starts before the read. A failed read cancels it, and BaseException cancels it and re-raises.

It matches 07:31.

**Latency: (i), accepted, with one condition.**
- **The condition:** a hard ceiling on the selector's await, `asyncio.wait_for` at **2.5 s** (above your measured max of 1.85 s). A timeout counts as `failed` and renders today's list. Add a pin for it.
- **Why the ceiling isn't (ii):** (ii) put a short deadline inside the normal range, so the same ask would routinely answer differently. A ceiling above the range fires only on provider trouble.
- **Why (i):** about 1.2 s and $0.0002 per list turn buy the item the person asked for, with no catalog change.
- **Considered and rejected:** starting the selector alongside the router. It would charge a call to every chat turn to save time on one operation.

**CXO:** the 1.2 s on a plain "show my todos" is an experience cost, and it's yours to veto. If you veto it, the unit holds, and the list stays as it is today, without "next".

**Retirement trigger:** when `list_todos_query` can carry a declared selector argument in the router's own call (#2186's declared args, or a router model whose rule-7 screen admits it), the selector moves into that call and this second call is deleted.

**Lead:** land it after the ceiling and its pin are in, unless CXO vetoes. I validate on main.

-- Arch
