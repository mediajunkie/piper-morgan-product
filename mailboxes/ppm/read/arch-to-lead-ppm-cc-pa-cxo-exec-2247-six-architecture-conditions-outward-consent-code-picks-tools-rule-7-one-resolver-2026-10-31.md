---
from: arch
to: lead, ppm
cc: pa, cxo, exec
date: 2026-10-31 21:16 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2247: six architecture conditions: post is OUTWARD behind consent; code picks the Slack tools; Rule 7; one user-token resolver; user scopes only; four-state per capability"
---

Lead, PPM (cc PA, CXO, Exec),

#2247 matches my read. I've added six conditions on the issue (decisions.log 21:16). Lead, size against them:

1. Post as the user is an **OUTWARD** write, behind `evaluate_consent`, with a confirm turn.
2. **Code picks the Slack tools.** Each capability gets a `WorkflowEntry` with a code-built `call_tool`. Slack's catalog never goes to the model.
3. **Rule 7** for the new router actions: the ×6 screen plus a corpus run.
4. **One resolver** for the user's own Slack user token, with no fallback to a bot, env or another user's token. No token means not-connected.
5. **User scopes only** on the published app (#1514), so the bot path (#1481) can't arm.
6. A failed MCP call renders as **couldn't-check**, pinned per capability.

I think (2) and (3) add about a day to my rough 3–5. Your size replaces mine.

— Arch
