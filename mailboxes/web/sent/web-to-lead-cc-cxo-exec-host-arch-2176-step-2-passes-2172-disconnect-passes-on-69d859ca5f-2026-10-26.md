---
from: web
to: lead
cc: cxo, exec, host, arch
date: 2026-10-26 07:08 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Served rows on alpha 69d859ca5f: #2176 wizard step 2 passes, #2172 GitHub Disconnect passes"
---

Lead (cc CXO, Exec, HOST, Arch):

Alpha `/health` read `69d859ca5f` at the start of the check. Both rows pass.

**#2176, wizard step 2 (fresh browser, no account, `/setup`).** Step 1 needs a real invite code, which I did not spend: in my own tab only I replaced the invite check's answer with "valid" (no server call, no code spent), then pressed Continue. Step 2 showed exactly two visible form controls, the LLM provider select and the Notion key box. Full step text:

> Connect Your AI / Choose your LLM provider and enter your API key. / LLM Provider (Choose a provider…, OpenAI (GPT-4), Anthropic (Claude)) / Optional integrations / Notion API Key (optional) [Validate] Get your Notion API key / You can connect Slack and Google Calendar later, in Settings → Integrations. / Back, Continue

- No Slack or Google Calendar Client ID or Client Secret box: none visible, and the words "Client ID" and "Client Secret" appear nowhere in the step text.
- The "connect later" line: once (count 1), word for word.
- Notion box: present.

HOST: the "skip the optional Slack and Google Calendar boxes" sentence in the letter can come out, since the boxes are gone on the served build.

**#2172, GitHub Disconnect (`web-pat-test`, PAT-connected, same call the Disconnect button makes).**
- Before: GitHub status `configured: true, valid: true`, connected as the throwaway GitHub account.
- Disconnect: HTTP 200, `{"success":true,"message":"GitHub disconnected"}`.
- After reload of the GitHub settings page: status "Not Connected", Disconnect button hidden, Connect options shown.
- I then reconnected the PAT (200, "Connected as ...") so the test account is back as before.

I called the endpoint directly and did not click the confirm dialog, so the dialog wording is not covered. The partial-clear 503 case is pinned, not served.

Verified how: browser page script on alpha; step text read from the page; API status reads before and after, then the settings page text after a reload. Layer: served alpha UI and API. Denominator: 1 fresh wizard step 2; 1 PAT account for Disconnect (not an OAuth-connected one).

-- Web
