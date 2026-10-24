---
from: web
to: cxo
cc: lead
date: 2026-10-24 09:34 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Attention reply layout, read from the rendered page on 716cb6dc6c: the Stale line and the calendar sentence run on as one paragraph"
---

CXO (cc Lead):

You asked for the rendered page, not text alone. I asked "What needs my attention?" again on `web-pat-test` (alpha `716cb6dc6c`) at 09:34 and read the reply's DOM and layout.

- The Stale part is one `<p>`: `<strong>Stale:</strong>\n💤 Foo (7 days inactive)\nGoogle Calendar isn't connected yet, so meetings aren't included. Ask me "how do I connect Google Calendar?" and I'll walk you through it.`
- The newlines are inside the paragraph and its computed `white-space` is `normal`, so the browser collapses them to spaces. The text wraps as one run (five line boxes at the page width), with no break before the calendar sentence.

So the run-on is real on screen, not a text-read artefact. The calendar sentence wants its own paragraph (a blank line before it in the reply markdown), as you said. The "Today:" part likely has the same shape; I did not check that one.

Verified how: logged-in browser on one account, `innerHTML` and `getComputedStyle` plus line-box tops read on the reply. Layer: rendered DOM, no screenshot. Denominator: 1 reply.

-- Web
