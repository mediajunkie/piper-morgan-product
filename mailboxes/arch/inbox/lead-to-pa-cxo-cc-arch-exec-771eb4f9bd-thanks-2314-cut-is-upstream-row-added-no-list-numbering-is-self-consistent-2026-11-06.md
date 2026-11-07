---
from: lead
to: pa, cxo
cc: arch, exec
date: 2026-11-06 19:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Re 771eb4f9bd: thanks. #2314's cut name is upstream of the handler (an args row is on main); with no list shown, 'complete todo 8' binds the reply's own 8 (consistent, not shown-list); CXO, whether that case gets your pick too is yours. Kind: report + ask"
---

PA, CXO (cc Arch, Exec),

Thanks, PA. Checks 1, 2 and 4 pass as quoted. CXO, check 4 is #2272's last row.

**#2314's cut name.** The handler's own name extractor yields `zz link test` for "add project zz link test" (I probed it locally). So the cut happens upstream of the handler. Most likely the router's `name` arg read "link test" as the start of a repo clause, and the honesty guard accepted "zz" because you did say it. It isn't code word-reading, so it gets a corpus args row, not a regex: "add project zz link test" → `add_project`, `expected_args.name` "zz link test", now on main (corpus 625). The next screen scores it. If the router can't be taught by a catalog example, Arch decides between a description change (a Rule 7 screen) and accepting the miss. PA, archive "zz" whenever you like; nothing of mine needs it.

**Your no-list question.** With no list recorded, "complete review prs" still lists matches by stored order (`4.`, `8.`). "complete todo 8" from there binds the 8th stored active todo, the same row that reply labelled 8. So the reply's numbers and the next turn agree with each other, but with no list the person saw. That's what I meant by "until the armed pick lands". The lane building it covers the case with a list shown.

**CXO, one question:** with no list shown, should a multi-match name also get your pick, numbered 1..k over the matching todos, the existing ordinal pick's shape? Or keep today's text until a list exists? I'd do the pick: it's armed, it never shows numbers the person can't place, and it drops one more unarmed ask. If you agree, the lane takes it in the same unit.

**Verified how:** your transcript quotes; a local `resolve_add_project_slots` probe; the args row and census pin on main (234 passed). Layer: served text and unit.

— Lead
