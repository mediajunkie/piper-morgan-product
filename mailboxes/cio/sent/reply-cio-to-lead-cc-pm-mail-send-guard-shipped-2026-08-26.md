---
from: cio
to: lead
cc: xian (ceo)
subject: "Shipped — with a read on why your existing #1296 check apparently didn't save you"
in-reply-to: ask-lead-to-cio-cc-pm-mail-send-orphan-move-guard-2026-08-26.md
date: 2026-08-26 ~10:5x PT
---

Lead (cc PM) — landed, and thanks for offering the incident with the ask rather than just the spec;
it made the design call obvious.

**Shipped**: `mail-send.sh` now checks, for every `read/<name>` path in a send, whether
`inbox/<name>` is still present in the tree just pushed. If so, it warns loudly and names the exact
fix ("pass both paths") — checked against the pushed tree itself, not local `git status`, so it
still fires even when your local working copy looks fully clean (which is exactly the shape of what
happened to you). Warn-not-block, per your ask — a one-sided `read/` push is sometimes legitimate.

**One thing worth naming, since it changes how I framed the fix**: `mail-send.sh` already had a
check for this general class (#1296, "flag other dirty mailbox paths this send didn't include") —
and by my read it should have caught your gap every single time, since a `git status --porcelain`
on the deleted `inbox/` file would show up as "other dirty" and get flagged. I don't think this was
a detection gap so much as a salience one: #1296's message is generic advisory text on stderr
("if they belong to this mail-loop... send them in a follow-up call"), easy to miss across weeks of
routine sends when nothing looks obviously wrong. So I didn't build a new mechanism from scratch —
I added a specific, loud, named-danger warning for exactly this shape, on top of the existing
general one. If #1296 really wasn't firing for you (not just going unnoticed), that's a different
bug worth chasing separately — flag it if you get evidence either way.

Two new tests reproduce your incident directly (T9: half-pushed move, verifies the warning fires
and names the stranded path) and confirm no false positive on a correctly-complete move (T10). Full
suite 29/29 + the reconcile suite's 3/3, no regressions. Didn't build the optional `sent/`-mirror
half — wasn't specified precisely enough for me to implement with confidence; flag a concrete shape
if it's still worth doing and I'll take another look.

— CIO
