---
from: pa
to: exec, lead, host, cio
cc: ppm, cxo, arch
date: 2026-10-29 12:51 PT
subject: "URGENT: alpha chat is down for every user since about 12:49 PT. Alpha's OWN Anthropic key hit its workspace usage limit ('regain access on 2026-11-01'); xian's hand to raise it"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**Served:** the last 3 queries of my row 2 run (Q61–63, about 12:49–12:50 PT) got HTTP 200 with `I can't answer right now. The service that writes my replies has reached its usage limit, and it's expected to come back around November 1. Nothing you did caused this.`

**Alpha's log at 19:50:22Z:** `provider: anthropic, task_type: intent_classification, error: 400 … You have reached your specified workspace API usage limits. You will regain access on 2026-11-01 at 00:…`, then `All configured LLM providers failed` and `Intent processing failed: API Error [INTENT_CLASSIFICATION_FAILED]`. So every chat turn on alpha fails for every account, partners included. /health still reads healthy, because it doesn't call the model.

**It's not the scoring key xian raised at 11:2x:** that key works this minute (one Haiku call OK at 12:51). Alpha's `ANTHROPIC_API_KEY` (a Fly secret) is in a workspace that has now hit its own cap.

**Asks:**
- **Exec / xian (in conversation with PA now):** raise the monthly limit on the workspace that holds **alpha's** key. I'm giving xian the console steps.
- **HOST / CIO:** if you know which workspace or key name alpha's secret is, tell xian. I can't look; I don't read secret values.
- **Lead:** row 2's figures are measured on 58 good turns plus 3 limit errors; scoring follows separately.

Verified how: the harness CSV's `error` column for Q61–63 (verbatim above); `fly logs -a piper-morgan` (20 s capture, 19:50:22Z lines); a live Haiku call on the keychain scoring key. Layer: served replies, app log, provider response.
