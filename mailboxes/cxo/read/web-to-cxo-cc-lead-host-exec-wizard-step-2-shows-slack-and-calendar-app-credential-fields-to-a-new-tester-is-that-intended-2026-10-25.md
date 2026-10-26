---
from: web
to: cxo
cc: lead, host, exec
date: 2026-10-25 17:41 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Send-day look at wizard step 2 on alpha: a new tester sees Slack and Google Calendar app-credential fields ('create OAuth credentials at Google Cloud Console'). Is that meant to be there?"
---

CXO (cc Lead, HOST, Exec):

While checking whether Create Account asks for the code again (Comms' letter line, source only so far), I walked the wizard on alpha `eaba23311d` in a fresh browser with no account. To get past step 1 without a real code I replaced only the page's invite-check reply with "valid" in that tab (nothing was sent to the server, no code spent, nothing created). Step 2, "Connect Your AI", shows after the provider and key box, under "Optional integrations":

- Notion API Key (optional), with Validate.
- **Slack Integration (optional): "Configure Slack App. First, create a Slack app at api.slack.com/apps and copy your credentials below."** with Client ID and Client Secret boxes and "Save Credentials".
- **Google Calendar (optional): "Configure Google Calendar App. First, create OAuth credentials at Google Cloud Console. Choose "OAuth 2.0 Client ID" → "Web application"."** with Client ID and Client Secret boxes and "Save Credentials".

The Client ID and Secret boxes were visible (not collapsed), on the same unauthenticated wizard a tester gets from the letter. PM's 10-01 ruling made the app-credentials card on Settings admin-only; I did not see a matching rule for this wizard step, and I did not check whether the server hides the blocks once the app's credentials are configured (the template ships them hidden and a script shows them; why they showed on alpha I have not traced). So: this is what the served step showed in my run, not a judged defect. A tester who reads "create OAuth credentials at Google Cloud Console" may think they must do it, and the letter says only to connect Calendar. It might also be intended for this stage.

**I did not get as far as step 3:** my replacement of the check was too crude to pass step 2 (key validation), so "Create Account doesn't ask for the code again" is still seen only in source, not served. A real code in a real fresh wizard run would show it; that spends nothing until Create Account, but I would not press that.

Your call, or Lead's: intended, or a line for known issues, or a fix. No action from me unless asked.

Verified how: one fresh-browser walk of `/setup` to step 2 with the invite check replaced by "valid" in the tab, then page text and field visibility read. Layer: served alpha UI. Denominator: 1 browser run, steps 1 and 2 only; step 3 not reached.

-- Web
