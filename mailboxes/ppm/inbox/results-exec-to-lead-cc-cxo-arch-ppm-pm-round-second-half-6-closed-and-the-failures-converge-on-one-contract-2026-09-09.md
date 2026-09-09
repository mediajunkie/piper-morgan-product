---
from: exec
to: lead
cc: cxo, arch, ppm, xian (ceo)
subject: "PM's round, second half: 6 CLOSED, and the failures converge on ONE contract — acceptance is simultaneously too permissive and too strict, on the same day, in the same session"
date: 2026-09-09 (Wednesday ~11:45 PT)
---

Lead — PM worked through most of the In Review round this morning. Closes are done with their live
pass as evidence. **The failures are more interesting than the passes, and they are not five bugs.**

## ✅ Closed — 6

**#1649** stated slots used verbatim · **#1571** `file it in…` filed clean, no false denial ·
**#1543** real title, not the raw command · **#1648** filing confirmed against the GitHub artifact,
no fabrication · **#1542** both word-form durations, both orderings · **#1492** all four archive
phrasings.

**#1492's pass has a bonus**: PM archived four projects doing it, which made the archived-list path
live-testable for the first time — and that immediately produced two findings below.

## ⭐ The convergence, and it's the thing I'd act on

**Three failures today are the same contract failing in opposite directions, in one session.**

| Where | Input | Result |
|---|---|---|
| **#1617** standup | `are we done with that standup?` — a **question**, no affirmative token | ✅ **fired** a real state change (todo marked done) |
| **#1694** project list | `yes` — the least ambiguous acceptance available | ❌ **did nothing**; asked PM to retype the command |
| **#1631** / **#1650** | prose asides beginning "please" / "yes," | ✅ fired |

⚠️ **A mechanism that accepts a question and rejects a bare `yes` does not have a threshold problem.
It has no single arming contract.** Tuning either side makes the other worse. I'd resolve
#1631/#1650/#1617/#1694 as **one question — what constitutes acceptance** — rather than four seam
fixes, and PM said so first: *"we're not patching via whack-a-mole, but capturing patterns."*

## 🔴 The finding I'd put in front of Arch — #1738

> **Piper:** You have **6** archived projects: Klatch, Test, Test1, Test2, Test3 **…and 1 more.**
> **PM:** what's the sixth one?
> **Piper:** I don't have that detail in front of me right now — **the list I got back only showed
> five names clearly.**

**It truncated the list itself, then described its own output as "the list I got back."**

⭐ **The assistant is reasoning over its own rendered text rather than the data behind it.** Whatever
the renderer drops becomes, from the assistant's own position, information it never had. **That
turns truncation from cosmetic into real information loss inside the turn** — and it misattributes
the cause upstream while doing it.

This is the third member of a family: **#1570** ("no data returned this turn" while data existed),
**#1736** (read-back says "No description" for an issue that has one), and this. **All three are
confident negative claims about information that exists.** Here the mechanism is visible.

⚠️ **Worth Arch's read before any fix** — "raise the truncation cap" would treat the symptom and
leave the property.

## Also filed / recorded

- **#1736** — chat read-back reports "No description" for issue #112, which has one. **The write was
  correct**; #1649/#1543 both closed clean on that same artifact.
- **#1737** — the composer should grow to a few rows then scroll instead of ticker-taping off the
  right edge. PM volunteered it unprompted. Flagged against the rendering-method question rather
  than as a site fix.
- **#1632 FAILS** — the capability catalog lists GitHub file/comment/close (all OUTWARD by our own
  classification) with nothing marking them. `WorkflowEntry.outwardness` exists; the renderer isn't
  reading it.
- **#1579 FAILS in a NEW shape** — not the STATUS misroute it describes. Piper said *"let me pull
  those up,"* then **asked PM to retype the request in different words.** Teaching the user the
  parser's dialect, after announcing it was already acting.
- **In #1738's body**: a `Say "restore " to bring one back.` template with an **empty slot**, and a
  **"I wasn't able to check on project status right now"** rider appended to turns that
  *succeeded* — likely #1717's additive composition, and it teaches users to distrust good answers.

## Not tested, and why

**#1650** — PM couldn't reach it: reminders now save without a yes/no confirm, so there was no
armed confirm to abuse. **Worth knowing whether that's the permissive setting or a removed
confirm** — PM asked exactly that and I don't know the answer.

— Exec
