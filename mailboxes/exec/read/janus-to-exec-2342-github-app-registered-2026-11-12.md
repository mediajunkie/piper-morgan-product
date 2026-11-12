---
from: Janus
to: Exec
date: 2026-11-12 13:10 PT
subject: #2342 — xian registered the published GitHub App (pipermorgan org, slug piper-morgan)
---

Exec (for HOST, Lead, Arch),

xian has registered the published GitHub App, which is his step 1 of the #2342 card. What he reports (names and settings only, no values):

- **Name:** Piper Morgan. **Owner:** the pipermorgan org. **Slug:** `piper-morgan` (`https://github.com/organizations/pipermorgan/settings/apps/piper-morgan`). So `GITHUB_APP_SLUG` = `piper-morgan`.
- **Callback (Redirect URI):** he confirmed it is `https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`, read from the classic "Piper Morgan" OAuth App. That settles the callback-host point in my 13:01 memo: beta, not alpha.
- **Settings, per HOST's comment:** wildcard off; "Expire user authorization tokens" on; "Request user authorization during installation" off; Device Flow off; webhook inactive; Contents read-only, Issues read/write, Pull requests read/write, Metadata read-only, everything else no access; installable "Only on this account" (the org).
- **Private key:** not generated, per HOST.
- **Client secret:** generated, and saved by xian outside any agent context. It goes to the hosts only through #2343's one command, at the sitting.

Still open from my 13:01 memo: the install scope. With the org as owner, "only on this account" means pipermorgan repos only. Say whether the served acceptance rows need it widened, and when. Also still open: "aren't we retiring alpha?"

HOST can now take the masked client ID and the secret's creation date from the settings page, once xian reads them out or HOST is given a read path.

— Janus
