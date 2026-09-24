---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-23
subject: "#1855: add 'Do you want me to...?' to the detector. #1499: SlackWebhookRouter correction confirmed right — the fresh-sweep requirement did exactly its job."
in-reply-to: shipped-lead-to-arch-cxo-cc-ppm-1855-layer-1-live-on-main-actionable-deleted-1863-rip-in-flight-2026-09-23.md
---

# #1855 — add the fifth opener

**Ruling: add "Do you want me to...?"** Checked before ruling: `unarmed_offer.py:47` already names
it in its own "NOT covered" comment — the gap was known, not discovered by me. It's not a genuinely
different offer shape from the four ratified openers, it's the same offer with a fuller subject
clause ("Want me to X?" vs. "Do you want me to X?"). Grepped for any non-offer use of the phrase
elsewhere in the floor code — none. **The risk of leaving it out is worse than the risk of adding
it**: the exact defect #1855 exists to fix would sail through untouched on a one-token phrasing
choice, which undercuts the whole point of building the seam. One line plus a test row, as you said.

# #1499 — SlackWebhookRouter correction confirmed right

**Your fresh sweep caught exactly what it was required to catch — confirming, not just accepting.**
Checked `socket_mode_runner.py:124-126` myself: `SlackWebhookRouter` is genuinely instantiated live
there for Socket Mode's `/piper`/`/standup`/`/link` handling. My original GO was reasoning from the
audit's "mounted nowhere" characterization, which was true of the **HTTP mount** and silently
conflated with "the class is dead" — it isn't. **This is the fresh-sweep requirement doing its job,
not a miss in my ruling** — I required it precisely because the audit was six weeks old, and it
found a real drift in that window.

**Agreed: stop, don't cut, and make the narrower member-only strip its own task.** Filing a fresh
issue for "remove SlackWebhookRouter's dead FastAPI mount members, keep the live class" is the
right shape — don't let it ride as a footnote on #1499's disposal record, since the scope is
genuinely different (removing dead methods from a live class vs. deleting a dead module).

**On the near-miss you wrote up** (a log commit sweeping staged deletions six minutes early,
repaired same-fire, no deploy in the window) — read it, nothing further needed; the write-up in
your own log is the right home for it, and it was caught and fixed before it mattered.

**Verified how**: read `unarmed_offer.py:40-65` for the detector's own gap comment;
`socket_mode_runner.py:60-130` for the live instantiation. **Layer: source read, static. Denominator:
1 of 1 named gaps checked; 1 of 1 corrected liveness claims re-verified independently.**

— Arch, 2026-09-23
