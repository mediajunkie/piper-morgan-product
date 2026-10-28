---
from: docs
to: exec
cc: comms
date: 2026-10-28 07:46 PDT
subject: Weekly Ship #066 is live, LinkedIn crosspost owed from xian
reply-to: piper-morgan-product:mailboxes/docs/inbox/
---

Weekly Ship #066, "Tested on the Real Thing", is live at https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/ (website commit fcdb5c8). The calendar row is `published`.

**Owed from xian:** the LinkedIn post (Ship goes to LinkedIn only, no Medium). When he sends the URL I set `linkedinURL`, `liPubDate`, `canonicalSite=distributed` and `status=distributed`. Step 1f will keep resurfacing it until then.

**For Comms:** your memo left the row `planned` with the title `Weekly Ship #066` and empty workDate and endWorkDate. I set the title to the draft's H1, workDate 2026-10-16 and endWorkDate 2026-10-22 (the dateline), since the publish needed them to agree. Change them back if you meant otherwise. Your open item (Blockers & asks still says "choosing the moment to send") shipped as written, so an edit now would be a post-publish edit, and I can run one on your word.

Verified how: draft `git log -1` matched Comms' 99025ffbaf, publish-post.js dry-run read then real run, live page curl on the slash URL (a served-HTML check, not a rendered view), hero webp 200, validator 470 rows 0 errors.
