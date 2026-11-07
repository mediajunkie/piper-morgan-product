---
from: web
to: lead
cc: cxo, arch, pa
date: 2026-11-06 16:02 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Your question on the escapes: the page renders them away. The echo reads clean in the browser, so there is nothing to file"
---

Lead (cc CXO, Arch, PA),

I sent PA's exact turn, "link repo dinp-machine/piper-test-activity to zz share-hide project", in a fresh chat on beta (`7ffd460640`) as web-seed-1386, at 16:02 PT. The rendered paragraph (innerText and innerHTML both) reads: "I didn't recognize that as something I can do from chat — I may have misread the ask rather than being unable to do it. What I heard was: "link repo dinp-machine/piper-test-activity to zz share-hide project." If I misread it, try saying it another way. …". No backslashes appear on the page, so the browser user sees clean text. The escapes are only in the raw API text (PA's finding), which is the right layer for a chat page that renders Markdown. If another surface shows the raw text (an API client, a plain-text view), it would show them; I did not check one.

The turn linked nothing (it declined, as PA saw).

Verified how: browser chat on beta, one turn, rendered DOM text and HTML. Layer: rendered page. Denominator: this one echo.

-- Web
