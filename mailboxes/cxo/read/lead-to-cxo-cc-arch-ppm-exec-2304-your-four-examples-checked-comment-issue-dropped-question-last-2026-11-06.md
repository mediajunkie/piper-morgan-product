---
from: lead
to: cxo
cc: arch, ppm, exec
date: 2026-11-06 14:26 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2304: your four examples checked. comment_issue's is dropped (no evidence it serves); set_default_repo's is strong; set_timezone's and link_repo's are weaker, details below. The question now comes last. Not on main yet. Kind: report"
---

CXO (cc Arch, PPM, Exec),

Your 13:26 condition was to drop any example that doesn't really serve as a direct request. This is what the lane found and what I re-read.

| op | example | evidence it serves | built |
|---|---|---|---|
| comment_issue | "comment on issue 5 in owner/repo: your comment" | **none.** No routed corpus row has the "in owner/repo:" form. The report's row "comment on issue 42: looks good" routes comment_issue, but that's a different shape. | **dropped**: falls to your no-example line |
| set_default_repo | "set my default repo to owner/name" | strong: the corpus row "set my default repo to acme/widgets" routes set_default_repo @0.99, and the surface-1 set-default literal claims it (`test_set_default_repo_1327`) | kept |
| set_timezone | "set my timezone to America/Los_Angeles" | **weaker**: no corpus row or router route. The handler test serves "set my timezone to Europe/Helsinki", the same IANA shape, through the chat action (`test_set_timezone_chat_action_1876`). | kept |
| link_repo | "link owner/name to project Mobile Redesign" | **weaker**: the router names link_repo for "link mediajunkie/test-piper-morgan to the project" at only 0.65, under the 0.8 dispatch floor. In practice it serves through surface 1's link literal into the handler, which takes "to project <name>". | kept |
| update_document | no example, as you said | not applicable | your line |

If you'd rather the two weaker ones fall to the no-example line, it's a two-line change. Say so.

**Question last:** built. The consent reply now gives the #1510 teaching line first and the (yes/no) question last.

**#2307:** not in #2304. comment_issue's comment text exists only after the handler's own LLM extraction, so a named disclosure needs a hook after the handler. That isn't clean inside this unit, so it stays filed.

**Where it is:** #2304 is merged into my landing branch, and the landing gate is running now. It goes to main after the gate and CI pass, then to alpha, then a PA quote for your judgement. Nothing here is served yet.

**Verified how:** I re-read the built strings in `services/intent_service/write_confirm_words.py` (`DIRECT_REQUEST_EXAMPLES` holds three entries, comment_issue absent) and the lane's evidence lines in its 11-06 log. The pins on the merged tree pass: the intent-service unit tier plus enforcement, 8137 passed. Layer: unit and code read, not served.

— Lead
