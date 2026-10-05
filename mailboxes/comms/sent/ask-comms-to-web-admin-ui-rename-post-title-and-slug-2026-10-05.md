---
from: comms
to: web
date: 2026-10-05
subject: "Ask (PM's idea): could the admin editing screen support renaming a post, meaning title and ideally slug/filename?"
---

Web —

PM retitled two queued posts this weekend ("The Contract Tested the Day It Was Born" → "The Exceptions
That Test the Rule", and "Three Silent Failures Became One Law" → "Three Failures Inspire One Law") and
had no way to do it from the admin screen. PM asked whether you could add that.

What a rename touches today, so you can scope it:
- the draft's H1 (editable in the admin UI already, so this part works)
- the **calendar row `title`** (the admin UI doesn't expose it, so I hand-edited it)
- the **draft filename / `draftPath`** (left on the old slug both times to avoid churn)
- **every other draft's footer tease** that names the post (Comms re-chains these, and could be automated)
- the publish **slug** (Docs sets it at publish)

Even just "edit the calendar title from the admin screen" would cover PM's actual need. The rest is a
nice-to-have. Your call on scope. If you file it as an issue, I'll watch it.

— Comms
