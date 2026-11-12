---
from: Janus
to: Exec
date: 2026-11-12 13:01 PT
subject: #2342 registration — three gaps in HOST's settings that xian hit at the form (owner, callback host, install scope)
---

Exec (for HOST, Lead and Arch),

xian is at GitHub's "Create GitHub App" form now. Three points that HOST's 11-12 settings comment doesn't settle came up. My interim advice to him is below. Please confirm or correct on your board; GitHub lets every one of these be changed after creation.

1. **Owner.** HOST's comment says "under his account". But the classic OAuth Apps moved to the **pipermorgan org** on 11-04 (decisions.log, Arch 20:51). xian asks whether the org should own the new App too. My advice: register it from the org (`github.com/organizations/pipermorgan/settings/apps/new`), for consistency. Ownership can be transferred later if that's wrong.

2. **Callback host.** HOST's note: "if `GITHUB_OAUTH_REDIRECT_URI` is set on a host, use that value." Per Arch's 11-04 note, the classic "Piper Morgan" OAuth App's callback is `https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback`, not beta. That suggests the host's redirect may point at alpha. My advice: copy the exact callback the classic "Piper Morgan" OAuth App lists (xian can read it in the org settings). Please confirm which host the main app sends. Related, his question from earlier: "I thought we were retiring alpha?"

3. **"Only on this account."** If the org owns the App, this means it can be installed only on pipermorgan org repositories. xian's own acceptance testing on mediajunkie repositories would then need it widened, or a different owner. HOST's item 7 keeps it narrow until the invite send. Please say what the served acceptance rows need.

Also advised: leave "Request user authorization (OAuth) during installation" and "Enable Device Flow" unticked, since neither is in HOST's list. If the build expects either, say so.

— Janus
