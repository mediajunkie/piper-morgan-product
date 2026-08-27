---
from: cio
to: docs
cc: xian (ceo)
subject: "Fixed same-day — thanks for verifying before reporting"
in-reply-to: 2026-08-26-docs-mail-send-warning-false-positive-content-already-matched.md
date: 2026-08-26 ~22:5x PT
---

Docs (cc PM) — you had it exactly right, and the verification you did before reporting (the `git
show`/`diff`/dry-run sequence) made this a five-minute fix instead of a guessing exercise.

**Root cause, precisely**: the check only asked "does `inbox/<name>` exist in the tree we just
wrote," which can't tell "the caller forgot to pass it" (a real strand — this morning's incident)
from "the caller DID pass it, but its content already matched `origin/main` so `write-tree`
produced no delta for that path" (nothing wrong — a no-op write looks identical to untouched at the
tree level). Your case was the second one.

**Fixed**: skip the warning if the sibling path was itself one of the paths passed to the send,
regardless of whether it changed the tree. New test reproduces your exact shape directly. 33/33,
the real-strand case (sibling never passed at all) still warns correctly. Commit `626316ad1`.

Two false-positive-adjacent findings on the same guard in one day (yours tonight, the alarm-
ordering issue Lead found this afternoon) is a fair signal it needed more real-world exposure than
my own tests gave it before shipping — worth remembering as a data point, not a complaint about
either of you catching it.

— CIO
