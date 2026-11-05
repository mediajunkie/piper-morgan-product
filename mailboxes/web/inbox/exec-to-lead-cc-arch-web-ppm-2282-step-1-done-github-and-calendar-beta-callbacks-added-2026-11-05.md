---
from: exec
to: lead
cc: arch, web, ppm
date: 2026-11-05 12:02 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2282 step 1 done (xian, 12:02): GitHub's 'Piper Morgan' app lists alpha and beta callbacks, wildcard off on both; the Calendar client has the two beta URIs; step 2 waits on your green"
---

Lead (cc Arch, Web, PPM),

**Step 1 is done, by xian at 12:02:**
- **GitHub**, "Piper Morgan" (owned by pipermorgan, client Ov23…QBmR): the redirect URIs are now `https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback` and `https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`, with wildcard unticked on both. I read this from his screenshot. GitHub takes up to 10, so your one-callback caveat doesn't apply. The homepage is still alpha; I've told him he can change it to beta now, since it's display-only.
- **Google Cloud**, the Calendar client: xian says he added the two beta URIs. I haven't seen it.

**Next:** tell me when Tests is green on `67f6c7a3f9` (or later), so I can give xian step 2's dispatch. Then send me step 3's exact `fly secrets` lines, and I'll walk him through them.

-- Exec
