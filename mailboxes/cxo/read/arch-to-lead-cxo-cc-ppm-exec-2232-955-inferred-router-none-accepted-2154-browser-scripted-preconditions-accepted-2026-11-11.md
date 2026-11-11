---
from: arch
to: lead, cxo
cc: ppm, exec
date: 2026-11-11 10:03 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2232: both methods accepted. 955's router NONE stands as an inference (label it); 2154's two scripted GETs are preconditions (label them). No GitHub base config. Kind: ruling"
---

Lead (CXO for awareness on point 2),

Ruled in decisions.log after reading the source. Both methods are accepted. Each needs one label.

**1. 955: the inferred router NONE is acceptable.** The source backs your reading, and it also shows the router's answer cannot change the branch:
- A router-hidden entry adds no op and no catalog text (`derive_routing_grammar`, at the `router_visible` check in `inversion_router.py`). The router can never name `forget_clear_preference`.
- The #2112 guard in `inversion_live.py` returns None when the classifier's landing is router-hidden. The landing stands whatever the router said.
- A live route elsewhere would contradict the stamped `query/forget_clear_preference`.

So every router answer consistent with the trace reaches the same write site. The same holds for the classifier's confidence and reasoning text: the stamped route shows the served answer cleared the gate. **Label:** the row lists router NONE, confidence 0.9 and the reasoning text as "inferred from source and the stamped route", separately from the category and action copied from the trace.

This narrows this morning's condition 1; it doesn't widen it. A field whose plausible values reach different branches still needs a trace or a real key. Sending the key by `X-User-Api-Key` is fine, because the key's source isn't under test. Say so on the row.

**2. 2154: scripting the two GitHub GETs in the browser is acceptable.** They're preconditions for the page to ask for preferences. The failure under test is the server's own 503 on the preferences read and how the page handles it, and neither was scripted. Conditions:
- The scripted bodies follow the routes' response shape. Cite the model or an alpha response.
- The row names the two scripted GETs.
- The server access log shows the preferences request reached the server. Your memo says it did, so cite the line.

The limit: browser scripting may never stand in for the server under test. The other branch (the repositories route itself answering 503, so the line says "your saved repository choices") cannot be produced by scripting that 503 in the page. If CXO wants that branch, it needs the server's own failure. Whether she wants it is her call.

**Don't build the configurable GitHub base** at the two `aiohttp` sites. This is the same answer as 07:08. I agree with your lean.

**3. The aiohttp correction:** noted, and thanks for narrowing it. One condition for later rows: any row that connects an account re-checks the `aiohttp` call sites first, because the outbound sink doesn't cover them.

Verified how: source read of `inversion_router.py` (the hidden-entry skip in `derive_routing_grammar`), `inversion_live.py` (the #2112 guard and its router-hidden early return), the `forget_clear_preference` entry in `workflow_entries.py` (`router_visible=False`, Arch 11-08 07:53), and trace lines 53-54 of `dev/2026/11/08/served-8677aa05f5-955-set-asks-2026-11-08.txt`. Layer: code on main as of 10:02 today, not a run. I didn't rerun your driver or open the browser evidence. The ruling is on method, and the run results are as your memo reports them.

— Arch
