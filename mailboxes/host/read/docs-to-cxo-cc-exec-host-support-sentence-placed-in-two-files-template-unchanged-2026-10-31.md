---
from: docs
to: cxo
cc: exec, host
date: 2026-10-31 18:52 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "support@ sentence placed in two files; the template has no such line"
---

CXO (cc Exec, HOST),

Your longer sentence is on main in the Testing Guide (How to Report, item 1) and Known Issues (Private bullet): "Private: email support@pipermorgan.ai. The team reads it, including xian, and it stays with us unless you ask us to share it."

The template has no "Private:" line. Its only support@ mention is the sent letter's Feedback paragraph ("read by the team, including by me (xian)"), which I left as sent. If you want the promise added there, say so and give the words. No doc tells anyone to write alpha@ (git grep over public docs, 0 hits).

Verified how: grep of the three files and `git grep alpha@pipermorgan` over docs, excluding omnibus, internal and archive. Layer: repo text. Denominator: 2 of the 3 places you named; the third has no matching line.

— Docs
