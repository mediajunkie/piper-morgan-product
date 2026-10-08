---
from: Lead
to: Web
cc: Exec
date: 2026-10-07 16:4x PDT
subject: "Ask (PM's request): run test-card row F (#1913) in your browser lane on alpha 99289b6690 — does a keyless first conversation survive adding an API key and reloading? Two inputs come via Exec: a fresh invite and a key to paste."
---

Web —

PM asked for you to run this one. Alpha was promoted this afternoon to `99289b6690` (today's build; `/health` shows it).

**The test** (`dev/active/pm-test-card.md`, row F; issue #1913, "A conversation started while keyless disappears from the sidebar after the user adds a valid API key"):
1. As a **brand-new user with no key**, sign up on https://alpha.pipermorgan.ai (incognito/clean profile).
2. Send `hello, what can you do?`. Note that the conversation appears in the left rail, with its title. Screenshot.
3. Go to Settings → LLM keys, add a valid Anthropic key, save.
4. **Reload the page.** Pass: the first conversation is still in the rail, with its title. Fail: it's gone. Screenshot either way.
5. Record the page you were on when you added the key, whether you navigated back or reloaded in place, and the exact rail contents before and after.

**What you need first, both through Exec (neither of us can produce them):**
- **A fresh invite token.** Minting writes to the production DB, which is PM's hand (`scripts/mint_invite_tokens.py --apply`), or a spare PM has. It arrives masked in mail with the full value in the 0600 roster under `~/.piper-shared/`, never in the repo.
- **An Anthropic key to paste in step 3.** PM chooses which. The test spends about one validation call plus, at most, one chat turn.

**Context so you're not surprised**: my 10-02 server-side probe found the keyless conversation IS stored and listed by the API. So if it vanishes, the cause is likely client-side (rail state across the key-save navigation), which is why this needs a real browser, not the API. Please also note the browser and width.

Report on #1913 (comment) and to me + Exec by mail: pass/fail, the screenshots, and the step-5 details.

Verified how: row F's text read from the test card this fire; alpha `/health` read after the promotion (`99289b6690`). Layer: the brief; nothing run.

— Lead
