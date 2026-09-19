# The weekly cycle — runbook

**Owner**: Exec (Chief of Staff). **Status**: ratified by PM 2026-09-19, dictated by PM in this form.
**Why this exists**: it wasn't written down anywhere. Two of its nine steps had skills
(`create-omnibus`, `draft-weekly-ship`); the other seven lived only in habit, so a new Exec session
**guessed at them** — produced a markdown synthesis instead of the established internal-report
artifact, and didn't notice that Ship #061 had no calendar row, no workstream files and no internal
report until PM asked. **PM, 2026-09-19: *"we need to capture it so you don't try to guess in the
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
**The calendar row is created at draft time, not publish time** — a Ship with no row is an orphan,
and that's how #061 went unnoticed for two days. Comms is the sole hand-editor of
`editorial-calendar.csv`. Syndication per `reference_syndication_targets_by_category`.

---

## The check that would have caught this being missed

**All three of these were true at once for Ship #061 and nobody connected them:** no calendar row ·
no per-role workstream files · no internal report in the established form. **Any one of the three is
a signal the cycle has stalled; all three together is the pipeline never having started.**

At step 4, verify all three:
```bash
grep -c "Weekly Ship #NNN" docs/internal/planning/comms/editorial-calendar.csv   # expect ≥1
ls dev/active/workstream-NNN-*.md                                                # per-role files
ls dev/active/ship-NNN-internal-report-for-pm-*.html                             # the artifact
```

---

**Verified how**: the nine steps are PM's own, dictated 2026-09-19 and reproduced in their order.
Recipient list read from the `to:` header of the 2026-09-18 sent memo (10 names). Artifact form and
section list read from `ship-060-internal-report-for-pm-2026-09-11.html` directly. The Ship #051
precedent is from memory `feedback_ship_needs_all_workstream_reviews_no_partial_draft`. Skill names
verified present in `.claude/skills/`. **Layer: documents and PM's stated process — this runbook has
not yet been executed end to end, so treat step timings as PM's intent rather than as measured.**
