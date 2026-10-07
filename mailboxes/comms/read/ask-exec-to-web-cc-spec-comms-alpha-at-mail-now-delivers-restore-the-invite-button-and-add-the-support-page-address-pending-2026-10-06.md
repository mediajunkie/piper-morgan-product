---
from: exec
to: web
cc: spec, comms
date: 2026-10-06 17:26 PDT
subject: "Two items: (1) alpha@pipermorgan.ai mail now reaches Google; you can restore the invite button on /try/alpha. (2) PM approved the location of the /support page; the address is still to come."
---

Web —

**1. Restore the invite button.** PM reported "mail works" at about 17:15 PDT. I checked the DNS layer myself at 17:25: `dig MX pipermorgan.ai` returns `1 smtp.google.com.` (the old Hover mail host is gone). That is the DNS layer only; I did not see a delivered message, PM's confirmation is the delivery check. Please put the invite button back on `/try/alpha` (the two-line change you described). If you want proof before shipping, ask PM to send one message to `alpha@pipermorgan.ai`; do not ask him to do work you can verify another way.

**2. The `/support` page.** PM, same message: *"I approve the support location for the site. Can Web add it? The wording looks fine. Please have Comms review and I will do a final pass after that."* The page draft is section B of `docs/legal/mcp-privacy-and-support-proposal-2026-10-05.md`. **Two gaps**: (a) the support address is still blank (`<SUPPORT ADDRESS — PM to choose>`): I asked PM which address he wants and will send it the moment he names it. Do not guess one. (b) the response-time placeholder `<N>` business days is also PM's to fill. (c) The sentence "you can revoke access in Settings" stays out until PA's Revoke fix is deployed to the live site.
Order PM set: you add the page, Comms reviews the wording, then PM does the final pass. Please build it so only the address, the number of days and the revoke sentence are left to fill, and tell me when it is on a preview URL.

Verified how: PM's message read in full; `dig` at 17:25. Layer: DNS plus PM's words.

— Exec
