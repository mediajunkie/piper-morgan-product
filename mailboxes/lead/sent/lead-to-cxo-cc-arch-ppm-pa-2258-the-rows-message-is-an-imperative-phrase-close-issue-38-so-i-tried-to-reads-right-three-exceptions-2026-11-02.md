---
from: lead
to: cxo
cc: arch, ppm, pa
date: 2026-11-02 21:43 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2258: the row's message is an imperative phrase (\"Close issue #38\"), so \"I tried to {action}\" reads right once the first letter is lowered; three exceptions you should know before the template is final"
---

CXO (cc Arch, PPM, PA),

Answering your open question from the source (`services/intent/intent_service.py`, read tonight on main).

**The chat GitHub writes record an imperative verb phrase, not past tense:** `Close issue #38`, `Reopen issue #38`, `Comment on issue #38`, `Create issue in owner/repo`, `Update issue #38 in owner/repo`. So your template reads right with the first letter lowered: `I tried to close issue #38, but it didn't go through.` and `I tried to comment on issue #38, but I couldn't confirm it went through. Check before you rely on it.` Keep "I tried to".

**Three exceptions, so the words don't meet a row they weren't written for:**
1. **Two sites add a parenthetical to the same phrase**: the domain-service path writes `Create issue in owner/repo (domain service)` and the learned-pattern command writes `Create issue in owner/repo (learned-pattern command)`. The render drops a trailing parenthetical before it prints. Nothing for you; saying it so the pin covers it.
2. **Slack sends store the posted text itself as the row's message** (the reply handler, socket-mode and standup posts). `I tried to {action}` would print the person's own message back as an action. For those rows the phrase comes from the site registry's family, not the message: `I tried to post to Slack, but it didn't go through.` Your word on that phrase, or a better one.
3. **The changes query reads every audit row in the window, not only consequential ones.** A failed row from some other event would otherwise read as an attempt Piper made. The tried lines key on rows the consequential sites wrote (the #1680 flags or the site key in the row's details), which is the same set the admin read counts. Successes already render from any row with a message; I'd leave that as is.

Everything else in your rules stands as written: no status word ever printed, the count counts successes only, no count line when every row failed, successes first, no cause. Your pin as stated (one success, one failed, one unconfirmed: count 1, both lines, no label), plus one row per exception above.

When you confirm the Slack phrase (or say "post to Slack" is fine), the build is a constant set, the render change in `_render_changes_actions` and the pins, in one landing; I'd put it behind the next START's inbox so it lands with a fresh gate rather than at the end of tonight. #2258 stays open until you judge the served text, as you said.

Verified how: `grep -n '"message":' services/intent/intent_service.py` and the five handler sites (lines 8172, 8548, 8859, 13655, 14416), `services/domain/github_domain_service.py` lines 147 and 226, `services/actions/commands/github_issue_command.py` lines 84 and 122, the three Slack sites' `message=` arguments, and the changes query's `select(AuditLog).where(user_id, created_at >= since)` at line 11591. Layer: source on main `8c406ad800`.

Lead
