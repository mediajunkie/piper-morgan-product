# The weekly cycle — runbook

**Owner**: Exec (Chief of Staff). **Status**: ratified by PM 2026-09-19, dictated by PM in this form.
**Why this exists**: it wasn't written down anywhere. Two of its nine steps had skills
(`create-omnibus`, `draft-weekly-ship`); the other seven lived only in habit, so a new Exec session
**guessed at them** — produced a markdown synthesis instead of the established internal-report
artifact — missing the very section the Ship gets drafted from — and then misread two *normal*
absences (no calendar row, no per-role workstream files) as further symptoms of the same failure. **PM, 2026-09-19: *"we need to capture it so you don't try to guess in the
future."*** That is the whole motivation; nothing here is new policy.

---

## The nine steps

| # | Step | Owner | When |
|---|---|---|---|
| 1 | Docs synthesizes the Thursday omnibus | **Docs** | Friday morning |
| 2 | Exec sends update-request memos to the team | **Exec** | Friday morning, after step 1 |
| 3 | All ten roles reply | **each role** | ASAP — "due at your next fire" |
| 4 | Exec synthesizes; shares the artifact with PM | **Exec** | once all ten are in |
| 5 | PM + Exec discuss and make plans | **PM + Exec** | — |
| 6 | Exec drafts the Weekly Ship | **Exec** | after step 5 |
| 7 | PM reviews it | **PM** | — |
| 8 | Publish | **Docs** | the following **Wednesday** |
| 9 | Share in the LinkedIn newsletter | **Comms / Docs** | after publish |

### The window

Sprint weeks run **Friday → Thursday**. The review always covers the **most-recent-CLOSED** week,
never one still in flight. On Friday 19 Sept the closed week is **Fri 11 → Thu 17**.

---

## Step-by-step, with the traps

### 1 · Docs synthesizes the Thursday omnibus — Friday morning
Skill: `create-omnibus`. **Step 2 depends on this**: the omnibus is the cross-role record the
week's asks are grounded in. Not Exec's to do; Exec's to notice if it's missing.

### 2 · Exec sends the update-request memos
**Ten recipients. Six leadership — `arch, cio, cxo, ppm, host, comms`. Four contributors —
`lead, pa, docs, web`.** Exec is the sender, not a recipient; PM is cc.

**A template exists and is tweaked most weeks.** Do not compose from scratch and do not reuse last
week's wording blind — **open the most recent sent memo, read it, and carry forward the current
shape**: `mailboxes/exec/sent/closeout-exec-to-leadership-*.md` is the 2026-09-18 instance.

What it asks for: **one** top priority or primary goal · progress · **on-track as a yes/no word** ·
next steps · portfolio update · contributor update. Capped ~400 words.

⚠️ **Send them even to roles that are dark.** In the 09-18 run five roles were deliberately parked;
their copies sat unread *by design*, and **silence from a parked role is not non-compliance.** Check
the registry's parked rows before reading anything into a non-reply.

### 3 · All ten reply
**Chase only roles that are awake and past the stated due point.** The 09-18 run went 6/10 by
mid-morning — every *awake* role — then to 10/10 within an hour of PM waking the other four
one-on-one. **State the denominator when reporting progress: "6 of 10, and the 4 missing are exactly
the 4 that are dark" is a different claim from "6 of 10."**

### 4 · Exec synthesizes and shares the artifact
🔴 **The deliverable is `dev/active/ship-NNN-internal-report-for-pm-YYYY-MM-DD.html`** — not a
markdown summary. Precedents: `ship-059-…-2026-09-04.html`, `ship-060-…-2026-09-11.html`.

**Established sections** (keep them; PM reads this at a glance):
- **At a glance** — dashboard tiles + milestone status + days to the milestone date
- **The week's three arcs** — narrative, numbered
- **The pattern worth the Ship's theme**
- **🔴 The honest counterweight**
- **Needs you** — table: item / what's needed / age
- **What didn't move**

⚠️ **Do not draft the report until all ten are in.** PM overrode a 5-of-6 draft for Ship #051:
*"we cannot write the ship without all the workstream reviews."* **PM is the first audience, not a
downstream reviewer.** If a reply is genuinely missing near drafting time, **escalate to PM for the
call** — extend, draft-partial-with-the-gap-named, or PM nudges — rather than deciding alone.

⚠️ **Don't reach for the theme before the substance.** PM, 2026-09-19: *"Let's not slop ahead to
themes before we discuss the substance."* The theme section exists in the artifact, but it is a
**proposal for step 6**, not a conclusion — and step 5 may replace it. **Check it against the
previous Ship's theme before proposing: #060's was "the week the cohort spent correcting itself,"
and a near-repeat is a reuse, not a theme.**

**Numbers**: run `scripts/sprint-truth.py` **once** and quote it. Since 2026-09-19 it writes a
snapshot to `dev/state/` and reports the **delta** — arrived/left **by issue number**, not just a
net. Use the delta, because a level ("57 not done") is always true and never informative.
**If a figure is taken after the window closed, label it "as of <date>" rather than passing it off
as a window-close number.**

⚠️ **PM can pull GitHub data directly. Ask rather than burn the API** — the GraphQL limit is shared
across the whole cohort and exhausting it breaks `sprint-truth.py` for everyone. **A query that
returns 0 against a week of obvious activity is a broken instrument, not a result: report it as
unmeasured, never as zero.**

### 5 · PM and Exec discuss, and plan
Where "how do we get a goal back on track" belongs. **Before the discussion, re-verify the
PM-facing items** — the board is a snapshot and ten awake roles move faster than it. On 09-19 a
four-minute re-verify pass caught two items that had already been resolved.

### 6 · Exec drafts the Weekly Ship
Skill: `draft-weekly-ship`. **Only after step 5.** The theme comes out of that discussion.

### 7 · PM reviews · 8 · Publish Wednesday · 9 · LinkedIn newsletter

⚠️ **CORRECTED 2026-09-19, same day this file was written — the first version of this section had the
order backwards and it is worth knowing why.**

**The Ship is written AFTER the step-5 discussion, and the calendar row is added after that.** PM,
verbatim: *"We write the Ship **after** this step and then we add it to the calendar."*

🔴 **So an absent calendar row for an undrafted Ship is CORRECT, not a defect.** I read #061's
missing row as a stalled pipeline and put that in this runbook as a rule. It was the normal order.
**The error underneath it: I generalised the blog-post pattern — where the row does come at draft
creation — onto the Ship, which has a different sequence.** Two adjacent workflows, one habit, wrong
transfer.

★ **PM's improvement, which removes the ambiguity entirely**: *"it would be fine to prepopulate the
Wednesday slot on the calendar for the foreseeable future with the sequential Ships. That is our
cadence after all."* **With the slots pre-seeded, an empty Wednesday becomes a real signal instead of
an unreadable one** — today it means nothing, because absence is the default state until late in the
cycle. Routed to Comms (**sole hand-editor of `editorial-calendar.csv`**).

Syndication per `reference_syndication_targets_by_category`.

---

## What actually went wrong for #061 — and what didn't

**One real gap**: the internal report existed only as a markdown synthesis, not in the established
`ship-NNN-internal-report-for-pm-*.html` form — so it was missing **the section the Ship is drafted
from**. That is the failure this runbook exists to prevent, and step 4 above is the fix.

⚠️ **Two things I wrongly called gaps, recorded so nobody re-flags them:**
- **No calendar row** — correct at that stage. The row follows the draft, which follows the
  discussion. See step 7 above.
- **No `workstream-061-*` files** — the ten update memos ARE the input. There is no separate per-role
  workstream artifact owed in this cycle, and asking for one is inventing a step.

★ **The generalisable error**: I found three absences at once, assumed they were one failure, and
wrote a "any of these three is a stall signal" check into the first draft of this file. **Two of the
three were the process working normally.** A cluster of absences is not evidence of a stall unless
you know which absences are *supposed* to be there at that point in the cycle — and the runbook not
existing is exactly why I didn't know.

---

**Verified how**: the nine steps are PM's own, dictated 2026-09-19 and reproduced in their order.
Recipient list read from the `to:` header of the 2026-09-18 sent memo (10 names). Artifact form and
section list read from `ship-060-internal-report-for-pm-2026-09-11.html` directly. The Ship #051
precedent is from memory `feedback_ship_needs_all_workstream_reviews_no_partial_draft`. Skill names
verified present in `.claude/skills/`. **Layer: documents and PM's stated process — this runbook has
not yet been executed end to end, so treat step timings as PM's intent rather than as measured.**
