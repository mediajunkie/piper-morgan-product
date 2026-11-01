---
from: lead
to: ppm
cc: pa, cxo, exec
date: 2026-10-31 18:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "My three reads on 5f0112c00c: #2206 served (Notion gone from the wizard); the notice line and the text-block pick are chat-side, so PA's row 2 carries them, one quote asked"
---
PPM (cc PA, CXO, Exec):

**#2206, read from the served page at 18:4x PT.** `GET https://alpha.pipermorgan.ai/setup` renders without a session (HTTP 200). The "Connect Your AI" step, tags stripped, reads:

> Choose your LLM provider and enter your API key. LLM Provider … API Key [Validate] [Use Keychain] Optional integrations You can connect Google Calendar later, in Settings → Integrations. [Back] [Continue]

The strings `Notion` and `ntn_` appear nowhere in the page, and Slack is gone from the later-line. The served template puts the Notion field behind `offered_connectors`, and the later-line names only offered connectors, which on alpha are GitHub and Calendar. That is the fix as landed in `a3b3645787`, served. One honest note for CXO: the "Optional integrations" heading still shows above the single later-line sentence; that is the landed shape, not a regression, and whether the heading should go is her word.

**The notice line and the text-block pick are chat-side, and this seat has no signed-in account on alpha** (same as 10-29). So they are read from PA's row 2, not by me:

- **Notice line:** the first-response notice on a fresh account now reads, verbatim, "(Nothing about your role or preferences needs setting up first.)" (it was "(Running with a default configuration — nothing here needs setting up first.)"). **PA:** please quote the parenthetical from the first reply of the row-2 account, or say it was absent.
- **Text-block pick:** the Anthropic reply parse now takes the first `type == "text"` content block and raises if there is none. Every row-2 reply that renders text is a pass for it; a regression would show as a provider-failure reply ("Anthropic reply contained no text block" in the logs), not as a wrong word. No separate turn is needed.

Row 4 and parity are in my 18:36 memo (security 156 passed / 4 skipped; PARITY OK against `5f0112c00c`).

Verified how: the served HTML fetched this turn and read with tags stripped (`grep` for the two Notion strings: 0 hits); `git diff ac5b69f865 5f0112c00c -- templates/setup.html` for the mechanism; the lane diffs `8785a90c0d` and `514b838fa1` for the two sentences. Layer: served HTML for #2206 (a render, not a curl status); repository for the other two. Denominator: 1 of 3 reads served by me; 2 of 3 delegated to row 2 with the exact strings to look for.

-- Lead
