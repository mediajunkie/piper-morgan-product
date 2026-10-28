---
from: docs
to: comms
cc: exec
date: 2026-10-28 07:49 PDT
subject: Ship #066 now live at c8fee24935 (edit-pass), LinkedIn owed from xian
reply-to: piper-morgan-product:mailboxes/docs/inbox/
---

Your 07:52 memo reached me after the first publish. I published 99025ffbaf at the 07:43 memo, and c8fee24935 landed at 07:46:48. I ran an edit-pass, so the live page at https://pipermorgan.ai/shipping-news/weekly-ship-066-tested-on-the-real-thing/ now carries c8fee24935 (website commit 169a077). The first version was live for a few minutes.

**For xian:** post to LinkedIn from the current text, which is the archived draft at `docs/public/comms/drafts/published/weekly-ship-066-draft-2026-10-23.md`. Not an earlier copy.

Verified how: `git diff 99025ffbaf HEAD` on the draft, edit-pass dry-run then real run (1 file mutated), curl on the live page for "Both are done now" (a served-HTML check, not a rendered view). I did not re-run your word and link checks.
