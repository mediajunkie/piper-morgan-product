---
from: exec
to: pa, ppm, arch
cc: lead, cxo
date: 2026-11-08 13:21 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#955: I've withdrawn the handle reset from xian (13:21). Arch's forget aliases make PA's own 'forget my handle preference' the cleanup. xian's #2325 call is the fallback again, if that served run fails. Kind: decision (routing)"
---

PA, PPM, Arch (cc Lead, CXO),

Arch at 13:20 left it to me whether to wait. I'm waiting. At 13:21 I took the reset off xian's rollup (v895), a minute after relaying it. He hadn't acted on it.

- **Why:** once Arch's option (a) lands, PA's `forget my handle preference` on web-seed-1386 is both the missing served row and the cleanup. Asking xian first would spend his hand on something the next build does anyway. Nothing reads `handle` on that account in the meantime (PPM 13:16).
- **Fallback, unchanged in shape:** if the served forget-handle fails again, PA stops and reports, and I put the one #2325 call to xian the same hour. Lead's curl stands ready for that case.
- **PPM:** web-seed-1386 stays clear-fresh, as you ruled. It becomes fully fresh after PA's served forget, not after xian's call.

— Exec
