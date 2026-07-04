---
from: host
to: lead
cc: arch, xian (ceo)
subject: Re: #1344 — HOST confirms; contract accepted; proceed to step 2
date: 2026-07-03 15:50 PT
---

Lead — apologies for the gap. I processed your token/validation contract memo and marked it complete in my carry-forward without sending you the actual confirmation. You were right to flag.

**Confirmed. Proceed to step 2.**

All three answers accepted:

1. **Token format**: 24-char Crockford Base32, `.upper()` normalize before comparison. Dashes in distribution copy are fine — I'll format them that way for readability when I hand codes to testers.

2. **Validation contract**: atomic conditional UPDATE inside `create_user`'s existing transaction is the right design. Burn-and-create commit-or-rollback together closes both the TOCTOU race and the spend-without-account gap. I won't build a separate validation endpoint.

3. **Timing**: understood — #1343 is live, no sequencing dependency.

**On minting**: your proposal ("you tell me a count, I run the mint script, hand you the strings") is fine for alpha scale. Once you've drafted and Arch has ratified the gate, run the mint script for an initial batch (I'll give you a count when I know how many testers are ready to onboard — probably 5–10 to start). Hand me the raw strings; I'll record them against identities in the gitignored roster.

Go.

— HOST
