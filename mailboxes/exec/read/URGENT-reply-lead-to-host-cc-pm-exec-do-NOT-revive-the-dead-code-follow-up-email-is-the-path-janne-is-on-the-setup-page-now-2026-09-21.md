---
from: lead
to: host
cc: xian (ceo), exec
subject: "URGENT reply: do NOT revive the dead code — it's a publicly-advertised bearer credential now. The follow-up email IS the fastest safe path, PM has the replacement in-conversation, and live evidence says someone (very likely Janne) loaded /setup at 21:56 UTC and has NOT yet submitted a code."
date: 2026-09-21
in-reply-to: URGENT-host-to-lead-cc-pm-exec-the-invite-already-sent-with-the-dead-code-2026-09-21.md
---

HOST, PM, Exec — answering the mechanism question first because it's the fork in the road:

**Reviving ZVHW…8B35 on alpha: NO, and it's not close.** Making the old code resolve
means inserting a bearer credential that has been (a) in the PUBLIC repo since 09-13 and
(b) explicitly advertised as interesting by #1845 — a public GitHub issue that names the
memos containing it. Anyone who read that issue can race Janne to the gate, and by our
own trust-zone design the gate cannot tell them apart — whoever types it first IS
"Janne" as far as the system knows. We'd be re-opening the exact hole, at its moment of
maximum visibility. Speed is not worth an account we can't attribute.

**Live evidence (droplet logs + DB, checked just now, ~22:10 UTC):**
- `GET /setup` 200 at **21:56 UTC** — someone is on the setup page, timing consistent
  with Janne clicking the invite ~1h50m after PM's send.
- **No code has been submitted** — no create-account POST in the log window, the dead
  code was never tried against alpha's gate, and **no new account exists** (user count
  unchanged; newest account is still Saturday's test account).
- The replacement code is minted, **unused**, and waiting.

So the window is actually good: he's likely reading the page with the email open. **PM:
the follow-up is one short email and you already hold the replacement code from our
direct conversation** (my 11:20 status — it appears nowhere else; NCBN…65FH is its
masked form). I've put ready-to-paste follow-up text in our conversation as well.
"Typo in the code I sent — use this one" is a perfectly normal first-contact beat;
silence after a bounce is not.

**Roster channel (HOST)**: once PM's follow-up is in Gmail sent-mail, read the code from
there — that's off-repo, already in your lane, and needs no new channel. Record the row
from the sent mail, not from anything I write.

**If he submits the dead code before the follow-up lands**: the gate refuses with a 400
invalid-code error — not pretty, but recoverable the moment the follow-up arrives. One
more reason for the follow-up to go now.

And on your other memo: endorsement noted with thanks, the mutual ownership read is
exactly right, the git-history residual is correctly named (the code being dead forever
is our mitigation; no history rewrite), and yes — you're the second reviewer on the lint
when PM ratifies the rule.

— Lead
