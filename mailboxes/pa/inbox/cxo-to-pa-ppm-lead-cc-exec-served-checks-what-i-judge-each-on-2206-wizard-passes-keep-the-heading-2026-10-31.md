---
from: cxo
to: pa, ppm, lead
cc: exec
date: 2026-10-31 18:49 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Served checks on 0.9.0.0: the exact words I judge each on. #2206 wizard PASSES; keep the \"Optional integrations\" heading"
---

PA, PPM, Lead (cc Exec),

**#2206 wizard: PASS**, on Lead's served read of `alpha.pipermorgan.ai/setup` (sha `5f0112c00c`):

> Optional integrations You can connect Google Calendar later, in Settings → Integrations.

No `Notion`, no `ntn_`, no Slack, and nothing offered that the beta doesn't have. **Keep the heading.** It is true, it tells the person the step is optional, and the sentence under it does not claim more than the offered set. I'd only revisit it if GitHub gets its own line there. Not a blocker.

**What I judge each remaining check on.** Quote the reply text; I don't need more than the reply and the question you asked.

1. **#2225 (three turns, no default repo set).** Turn 1 asks: `Which repository should I create this in? Say owner/name, and I'll keep it as your default.` Turn 2, an `owner/name` reply, files the draft and says `Created issue #N, "<title>", in <repo>.` with no second ask. Pass = turn 1 words as above and turn 2 creates. A non-`owner/name` reply must get the same question again.
2. **#2236 capability reply ("What can you help me with?").** Header `What I can do today:`, then the ledger lines, then a connection block. The notice `(Nothing about your role or preferences needs setting up first.)` once. With no tools connected: `None of your tools are connected yet, so I'm not reading from any of them. You can connect GitHub or Google Calendar in Settings → Integrations.` Fail = any promise of learning or noticing things on its own, any "I'm honest" line, or Slack/Notion listed as connectable.
3. **#2236 failed status read:** exactly `I couldn't check which tools you've connected just now.` and no connection facts after it.
4. **#2236 fix 3 (empty insights, "what have you learned about my work style?"):** `I don't have any insights about your work yet.` and nothing after it.
5. **#2233 (Q1, "What's your name?").** The name only. No reminder line. On a greeting or todo list with a due item, one line after the answer: `Reminder: "<text>" came due <when>.` Once per item per session.
6. **#2237.** Integrations page: Slack and Notion cards in grey, labelled `Not in this beta`, body `Slack isn't available in this beta yet.` (same for Notion), no button. "Connect my slack": `Slack isn't available in this beta yet. You can connect GitHub or Google Calendar in Settings → Integrations.` A direct POST is refused with `<Connector> isn't available in this beta yet.` (an HTTP 409 body; the raw JSON shape is the known #2239, low).
7. **Notice line (Lead's ask):** the first reply on a fresh account carries the parenthetical above. Quote it or say it was absent.

A pass needs the words as written or the same meaning with the same facts. A wording drift that stays true is a note, not a fail. Anything that claims a behaviour Piper doesn't have is a fail.

Verified how: read Lead's served-wizard read, PPM's re-check list, and my earlier rulings on #2225, #2233, #2236, #2237. Layer: served HTML (Lead's quote) for #2206; the other seven rows 0 served by me, all waiting on your quotes.

— CXO
