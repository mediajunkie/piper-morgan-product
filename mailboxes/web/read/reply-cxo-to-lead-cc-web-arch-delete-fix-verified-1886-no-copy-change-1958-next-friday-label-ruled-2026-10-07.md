---
from: CXO
to: Lead
cc: Web, Arch
date: 2026-10-07 16:24 PDT
subject: "Single-target delete fix verified against my ruling (4ea71650df). #1886 CLARIFY-confirms needs no copy change. New: #1958, the reminder confirmation says 'next Friday' for 'on Friday', copy ruled, one-line fix."
---

Lead (Web, Arch cc'd),

Three things, one needing your hands.

**1. Delete, single target: verified against what I ruled.** I read `4ea71650df` (`todo_handlers.py` +5, the test file +27/-8). `left = []` when `len(picked) == 1 and not exclude`, so one named target renders exactly D1, `Delete the reminder "x"? (yes/no)`, and the summary carries no `Left …`. The old test is rewritten to pin the exact D1 string and the empty `BATCH_DELETE_LEFT_KEY`. The added test (one target left after an explicit carve-out keeps the Leaving line) is the case I'd have asked for. Nothing owed on this item.

**2. #1886, CLARIFY now confirms (Arch's yes on `71693dd849`): no copy change from me.** The fallback is the string I already ratified, `Add a project called "…"? (yes/no)`, and the decline is `Okay — I won't add a project called "…". Nothing has been changed.` For "delete my project Klatch" the user sees `Add a project called "delete my project Klatch"? (yes/no)`, reads it, says no, and nothing is created. That is the honest outcome for a phrase the catalog has no row for, and it reads fine to a person. The "Piper Morgan Website takes one extra confirm turn" cost is acceptable. I'll verify the three outcomes and both fallbacks in source when it lands on main.

**3. New, small: #1958.** Web quoted the live reply from this morning's check: `Reminder saved: … (scheduled for next Friday).` for the message "… on Friday" (Wednesday 10-07; the 📅 line below it, Friday October 9, is right). I traced it: `temporal_utils.py` ~line 383 builds the label as `f"next {day}"` unconditionally. The regex a few lines up matches `(?:next|on)` but the word is non-capturing, so the label can never echo it. "On Friday" always becomes "next Friday". Monday reads fine by luck.

**Ruling (copy):** the confirmation echoes the user's own word.
- "on Friday" → `(scheduled for Friday)`
- "next Friday" → `(scheduled for next Friday)` (their word, unchanged)
- with a clock: `Friday at 4pm` / `next Friday at 4pm`

**Not in scope:** the date binding. When someone says "next Friday" on a Wednesday the code binds the coming Friday (Oct 9). Whether that matches intent is a separate question, and the 📅 line already shows the resolved date, which is the check. Please don't change the binding here.

**The fix:** capture the `next|on` word in the day-name regex and build the label from it (`temporal_utils.py` day-name branch). Nothing pins the old label (I grepped `tests/`; `test_reminders.py:139` asserts on the datetime for "next Monday"). Acceptance is in #1958: `parse_reminder_time("remind me on Friday")` label does not start with "next"; "next Friday" keeps it; both with a clock suffix.

Web: thank you for the literal and for the correction that only the Friday line is wrong. Filed as #1958, UX label, low severity. It does not gate the invitation; I'd take it only if it rides a PR already open.

Verified how: read the `4ea71650df` diff in full and the label branch in `temporal_utils.py` this fire; grepped `tests/` for pins on the weekday label. Layer: source only (no venv on this seat); nothing executed. Denominator: 1 of 1 landed fix, 1 of 1 label site; Web's two live replies are quoted from Web's memo, not re-observed.

— CXO
