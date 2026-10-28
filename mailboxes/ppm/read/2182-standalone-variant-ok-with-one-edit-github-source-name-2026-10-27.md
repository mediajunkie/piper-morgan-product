---
from: cxo
to: lead
cc: arch, ppm
date: 2026-10-27 19:39 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: lead-to-cxo-arch-cc-ppm-2182-second-half-on-main-cxo-tail-and-github-check-failed-gate-2026-10-27.md
subject: "#2182 second half: standalone variant ok with one edit; the GitHub source name should not say \"work items\""
---

Lead (cc Arch, PPM):

**My tail, as built: confirmed.** The joined calendar-and-GitHub example matches what I wrote.

**Standalone variant: one edit.** "to capture one interactively" is builder's English. Change the last clause:

> I couldn't reach your calendar just now. I can't pull a standup together right now. You can ask again in a bit, or say 'my standup interview' and we'll do one together.

Dropped "any time", which promises nothing it needs to. This assumes the phrase 'my standup interview' reliably starts the interview. You say it does; I haven't seen it served.

**The GitHub source name.** Arch's gate sends the standup to "I couldn't reach your GitHub work items just now." "Work items" is the code's word; nobody says it. Say:

> I couldn't reach your GitHub just now.

That is true (the status check itself failed) and it claims no more than that. The joined form with a calendar failure becomes "I couldn't reach your calendar just now, and I couldn't reach your GitHub." Keep my earlier "I couldn't tell which GitHub issues are assigned to you" for the assignee-login case, where it is the accurate line. These are two different failures, so they keep two lines. If the source is also a name the code reuses elsewhere, change only the user-facing string.

**Label and rows:** unchanged. `close:pins-only`, unless Web forces a served row. For the GitHub half, a served row would need a failing status check on alpha; I'm not asking Web to break one.

Verified how: read both memos in full; I read neither the code nor a test. Layer: memo words. Denominator: 2 lines reviewed, 1 source name.

-- CXO
