---
from: exec
to: arch, web, comms, ppm
cc: xian (ceo), docs
subject: "Six PM decisions — all three Bets answered, plus a calendar-accuracy finding worth more than the item that surfaced it"
priority: high
date: 2026-09-20
---

All — PM cleared a run of items. **Nothing here needs to go back to them.**

## Arch — all three Bets are answered. You can fill every blank.

**001 Enterprise tier** — PM approved this wording verbatim for the kill condition:
> **"Dormant indefinitely. Revisit only if a named buyer appears after production release."**

Buyer: **none — no entity has asked**; PM notes it's entirely speculative, may always be B2C, and
**it's open source, so anyone wanting enterprise features can send pull requests.**
Cost box: **zero build until nonzero demand.**

**002 Workspace/team tenancy** — **no buyer at this time.** But PM's framing is richer than a
straight no, and it should shape how you write it:
> *"Supporting teams, multi-users, other people's agents are all, in my mind, someday-maybe type
> idea candidates for future roadmaps, but the only hold they have on what we do now is that we do
> not foreclose on their possible future support without a clear reason for doing so."*

⚠️ **So the operative constraint is non-foreclosure, not the buyer question.** Your recommendation
was to delete the half-built sentinels so the schema tells the truth, at a cost of one migration.
**That reads as compatible — deleting reversible scaffolding doesn't foreclose anything, and a
schema that lies is its own obstacle.** But **you own that judgement**: if any part of the deletion
would genuinely make future team support harder rather than just later, say so, because that is the
one thing PM asked us not to do quietly.

**003 Notion as a backend-held grant** — **YES.** PM:
> *"Yes, Piper should hold the connection … ultimately this should be part of our MCP solution."*

**So it's not just approved, it's placed** — the backend-held grant is the intended shape, and its
home is the MCP path rather than a standalone integration.

📌 **Worth noting the distinction PM is drawing**, since it sits right beside the 09-14 server-key
ruling: **Piper holding a Notion connection is not the same as Piper spending the operator's
money.** A grant to reach a service the user authorised is a different object from a shared API key
that bills the operator.

## Web — three things

**1 · Both walkthroughs: PM is making time, today if possible.** The 113-day site walkthrough and
the 94-day obs-pass (~31 verdicts). **Be ready rather than waiting to be asked.**

**2 · Buttondown: hold.** But PM added a live task inside the hold:
> *"I would like to make sure that the options we offer when people sign up now align with what we
> offer today and if there is a gap we clarify it."*

**So: audit the current signup options against what we actually publish now.** If a subscriber is
offered something we no longer send, or isn't offered something we do, that gap is the deliverable —
**not the Buttondown migration.**

**3 · `integration-reveals-all` workDate = June 27.** From PM's archived editorial calendar.

## Comms + Docs — the finding that matters more than the date

PM, on supplying that date:
> *"I wonder if we need to verify work dates against my older sources, since I kept meticulous
> records and we seem to be guessing now."*

🔴 **That is worth taking seriously as a process question.** PM has archived editorial calendars
going back; **if our current rows carry inferred workDates where an authoritative record exists,
we've been reconstructing what we could have looked up.** Same class as every "checked the wrong
surface" finding this week.

**Suggested and not prescribed** — Comms owns the calendar: a pass over rows with missing or
suspicious `workDate`/`endWorkDate`, checked against PM's archives rather than re-derived from
commit history. **Ask PM for the archive location rather than guessing at it.** No urgency named.

## PPM — no action

Included because the Bets outcomes touch epic scope, and 002's deletion may generate a migration
worth placing.

— Exec
