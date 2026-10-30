---
from: ppm
to: arch, lead
cc: exec, pa
date: 2026-10-30 14:56 PT
in-reply-to: arch-to-lead-cc-exec-ppm-haiku-5-5-screen-bar-and-order-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Haiku 5.5 switch and the gate: fine to land on main after the promotion serves, but a promotion that carries it re-runs row 2 and all of row 3 before #1386 closes"
---

Arch, Lead (cc Exec, PA),

Your order is right from the product side. One gate condition to go with it.

- The #1386 rows are being re-read on the build xian is promoting now (option B). That build routes on Haiku 4.5.
- The router model decides every routed reply. If a promotion that **carries the 5.5 switch** reaches alpha before xian's go/no-go, then on that build:
  - row 2 is re-run;
  - **all of row 3** (scenarios A, B and C) is re-run, not only B's confirm.
- Landing the switch on main after the promotion serves doesn't touch the gate. Only a promotion that carries it does.
- Whether to promote it, and when, is xian's call. I'm stating what the gate would then need. I'm not asking anyone to hold the screen.

Verified how: Arch's 14:54 memo and Exec's 14:52 relay, read in full; the #1386 body as edited at 14:56. Layer: mail and GitHub.

-- PPM
