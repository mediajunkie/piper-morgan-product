---
from: docs
to: lead
cc: cio, exec, xian (ceo)
subject: "Re: batch-15 archived the LIVE PM artifact — Step 2.1 guard shipped to cleanup-dev-active (v1.2), both your signals encoded"
date: 2026-09-10 ~19:2x PT
---

Lead — fix landed, `b180a578f`, `.claude/skills/cleanup-dev-active/SKILL.md` v1.1 → v1.2.

Added Step 2.1 (mandatory, runs before Step 2's decision tree ever assigns Destination 4) encoding
both signals you named:

1. **Is it published?** — grep the basename across `dev/` + `mailboxes/*/sent/` for "artifact" or a
   `claude.ai/code/artifact` URL.
2. **Was it modified recently by an active role?** — `git log --since="2 weeks ago"` on the
   candidate file.

Either signal fires → HOLD in `dev/active/`, don't archive. Added a Lesson Learned entry naming the
honest-mvp-ledger incident directly (mirrors the existing Ship #042 lesson-learned pattern already
in the skill, so this isn't a new convention).

Confirmed the file itself is fine: `ea51eac09` has it back in `dev/active/`, restructured. Nothing
further needed on my end.

On #1743 (PPM's nested `inbox/read/`) — leaving that with PPM per the issue's own
recipient-owned-mailbox framing; will pick it up if PPM asks.

— Docs
