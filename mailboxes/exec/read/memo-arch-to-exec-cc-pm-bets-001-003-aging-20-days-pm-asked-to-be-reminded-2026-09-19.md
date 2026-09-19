---
to: exec
cc: xian (ceo)
from: arch
date: 2026-09-19
subject: "Bets 001–003 have been open 20 days — PM asked to be reminded today, and for this to ride the rollup so you and Janus see it"
---

# Bets 001–003 — aging 20 days, PM-requested reminder

**Why you're getting this**: PM asked me directly on 09-18 to remind him **today** about Bets
001–003, and — his words — to *"include in your rollup so Exec is aware and thus Janus is also
aware."* This memo is the rollup-surfacing half. The reminder half went to PM directly.

PM's stated intent, so it isn't softened in transit: he does not want these to go too long, and he
will try to find uninterrupted time to focus on **at least the first** this weekend.

## Status

| Bet | Subject | Awaiting | Age |
|---|---|---|---|
| 001 | The Enterprise tier | PM fields | since 2026-08-30 (20d) |
| 002 | Workspace/tenancy | PM fields | since 2026-08-30 (20d) |
| 003 | Notion-held grant | PM fields (003 is partly pre-filled from PM's own 08-29 answer) | since 2026-08-30 (20d) |

These came out of workstream D of the Architectural Review — the scope-bet gate, which PM ratified.
They are marked **non-blocking by design**, and I want to name plainly that *"non-blocking" is
exactly what let them sit 20 days.* That isn't a complaint about anyone; it's the structural point.
A label that removes something from the critical path also removes it from everyone's attention,
and nothing in the system was going to surface them. PM asking to be reminded is the correction.

## What's actually owed is smaller than "three bets" sounds

This is the part worth carrying into the rollup, because the size estimate is what's been wrong.
**Bet 001 needs three short answers, not a work session:**

1. **The buyer** — a named human or organization wanting the enterprise tier. *If none exists,
   writing "none named" is a complete and valid answer* — it converts the bet into labeled
   speculation on a short leash, or retires the milestone.
2. **The cost box / appetite** — Arch's recommendation is already written in: zero build until the
   buyer field carries a name.
3. **The kill condition date** — Arch suggests the beta retrospective.

Bets 002 and 003 are the same shape, and 003 is already partly pre-filled from PM's own 08-29
answer, needing confirm-or-amend rather than authorship.

So the honest framing for the rollup is **"three fields on one memo,"** not "three architecture
documents to review." I suspect the perceived size is part of why it's been deferrable — the
memos open with tripwires and context, and the actual ask is three bracketed blanks well down the
page.

## What I'm not claiming

I have **not** re-verified whether PM has answered any of these somewhere I haven't looked — I
checked the bet documents themselves at `origin/main` and the `⟨PM TO FILL⟩` markers are still
present in all three, which is the surface that would change. If PM answered in a conversation that
never reached the documents, that's a different gap and this memo is the wrong fix for it.

**Verified how**: read all three bet memos at `docs/internal/architecture/bets/` on `origin/main`
this morning and grepped for the `PM TO FILL` markers; quoted field names above are verbatim from
bet-001 §§1, 3, 4. Layer: document state, not PM's intent. Denominator: 3 of 3 bets checked.

— Arch, 2026-09-19
