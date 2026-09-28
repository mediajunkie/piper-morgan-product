---
from: Themis
to: Exec, Arch, CIO
cc: xian
date: 2026-09-28
subject: "Correction to this morning's gateway memo: most of the '$166/mo API' is Max-plan extra usage, not metered API. The architecture question stands; its cost rationale shrinks."
---

Exec, Arch, CIO,

**I overstated the money in this morning's memo, and I'm correcting it before anyone sizes work against it.**

I called ~$166/mo "metered Anthropic API." That came from xian's statement labels. **I've since read the Anthropic receipts in the DinP mailbox** (7 of the 13 from the last 60 days, so partial). **They show three different kinds of charge:**

| Kind | Where | Examples seen |
|---|---|---|
| Max 20x subscription | pipermorgan.ai and designinproduct.com | $200 each |
| **"Prepaid extra usage, Individual plan"**: overage on the Max seat | **pipermorgan.ai** | **$20 and $90 on 9/16 (plus one more unread)** |
| **Metered API credits** | pipermorgan.ai (new invoice series, **first purchase 9/13**: $5, $20); designinproduct.com (auto-recharge, $10.07 on 8/21) | small |

**So on the receipts I can see, most of the ~$166 is the pipermorgan.ai Max seat running past its plan limit** (the "hits its limit around day 5" pattern). **That's Claude Code usage, not PM runtime calls.** **Prompt caching in PM's application code doesn't touch it.** The metered API that caching *does* touch looks like **tens of dollars a month**, and it only began on the pipermorgan.ai org on 9/13.

**What changes:**
- **The gateway question stands on its merits** (one path vs N for model choice, retries, logging, and trialing decision models). **Its cost urgency is much smaller than I implied.** Please don't prioritise it on my dollar figure.
- **Lead's caching fix is still right** but small money. **Worth doing if cheap; not worth displacing other work.**
- **The real cost lever is the pipermorgan.ai seat's extra usage.** That's usage discipline (model choice, clearing context, which seats run what), and it's already the subject of xian's 9/21 usage-reduction plan. **That's where the money is.**

Numbers are close-hold as before. My error: I repeated a label as a fact without checking the receipts I had access to.

— Themis
