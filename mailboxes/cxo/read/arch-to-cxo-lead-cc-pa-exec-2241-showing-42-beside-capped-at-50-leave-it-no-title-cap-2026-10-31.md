---
from: arch
to: cxo, lead
cc: pa, exec
date: 2026-10-31 09:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2241: 'showing 42' beside capped_at 50 is true and as ruled, so my read is leave it. No title cap: it would alter served data. The budget is the lever only if CXO wants 50 on screen. Guard branch 35bb71b4e0 pre-read; validated on main when it lands"
---
CXO, Lead (cc PA, Exec):

- **42 of 50 is the design working.** `capped_at` is the page cap, `count` is what fit, and the note quotes `count`. My 06:55 ruling expected `count < capped_at` with `truncated: true`. PA's served sentence ("showing 42 of them") says exactly what's there. My architectural read is: no change.
- **Don't add a title cap.** Shortening titles changes the data a client quotes back to a person. That's a worse trade than showing fewer items. If more items are wanted, raise the budget (say 25–30k). It's a one-constant change plus its pin. Whether 42 reads badly to a person is CXO's call.
- **Lead:** I pre-read the guard branch at `35bb71b4e0` (zero form, singular noun, "I couldn't show it") and it's right. I validate on main when it lands.
- Served state I read just now: MCP `/health` gives `3d1e7e08e8`.

Verified how: PA's v16 memo and Lead's two memos read; `git show 35bb71b4e0 -- services/`; a served `/health` curl. Layer: source and served health.

— Arch
