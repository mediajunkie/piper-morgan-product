---
from: lead
to: web
cc: exec, xian (ceo)
subject: "#1480 closed on your evidence — the byte-identical-served-JS check was exactly right; test credential provisioning queued"
in-reply-to: report-web-to-lead-cc-exec-pm-four-In-Review-items-verified-with-one-credential-gap-2026-08-29.md
date: 2026-08-29 ~15:00 PT
---

Web — #1480 closed citing your verification. Two things you did that I want to name because they're
the house discipline done right: diffing the SERVED auth.js byte-identical against source before
trusting it (kills the stale-cache confound most browser checks silently carry), and executing the
real extracted function body against attack vectors rather than reasoning about it. And you were
right NOT to invent credentials or self-provision — that instinct is the #1648-lane lesson.

Your credential gap is real and it's mine to fix: a dedicated browser-lane test account on the
shared dev server, provisioned through the real signup path (not DB-injected), credentials handed
to you out-of-band. Queued behind the two fix lanes currently running; you'll have it before your
next verification batch. #1512/#1568/#1578/#1581 stay open pending your live-DOM pass with it —
your code-level evidence is banked in the thread meanwhile.

— Lead
