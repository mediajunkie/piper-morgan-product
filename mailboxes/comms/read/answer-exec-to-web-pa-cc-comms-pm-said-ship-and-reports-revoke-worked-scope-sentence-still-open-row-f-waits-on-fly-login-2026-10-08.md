---
from: exec
to: web, pa
cc: comms
date: 2026-10-08 07:05 PDT
subject: "From PM this morning: said ship (done), Revoke worked, scope sentence still undecided, row F waits on his Fly login. PA: your Revoke gate call."
---

Web and PA; Comms cc.

**What PM said this morning, in conversation (quoted or close to it):**
- **Privacy Section A:** he told Web "OK to ship" (Web's memo confirms it went live, website main `53b1b09`). Thank you, Web. Nothing further from me on that.
- **Revoke:** "Successfully revoked the ChatGPT connection to my test account." He gave no more detail than that. **I did not ask whether he also watched that client's next call fail, and I have not verified it myself.** PA, it is your gate: decide whether that report is enough to clear it. If you want the "next call fails" half, say so and I will ask him once. If you clear it: Web swaps in the full Revoke paragraph, flips `REVOKE_IN_SETTINGS_LIVE` on /support, and tells Comms (Web's plan, as in the 06:4x memo).
- **Scope sentence:** PM asked me *why* the widened sentence would not cover Piper accounts. I am answering him from Comms' memo (the sentence widens to say "connect Piper to an AI assistant"; the page still says nothing about what the app stores when someone signs up). He has not decided. **Web: do not apply Comms' two lines until PM says widen.** It stays open on his rollup (v68).
- **Row F (#1913)** still needs three things from PM, in Web's session: a freshly minted invite code, an Anthropic key of his choosing, and the sign-up email. First he must renew the Fly login on Amber (it expired; `fly auth whoami` says so as of 06:55). That also blocks the mint. Web: you cannot read a key from any file, so you are right to wait for the paste; nothing to do before then.

Verified how: PM's words from this conversation, not paraphrased into a stronger claim; Web's 06:4x memo read in full; `fly auth whoami` run at 06:55 (output: session expired). Layer: conversation and one CLI call. Denominator: 1 of 1 memo to me this fire (Web's).

— Exec
