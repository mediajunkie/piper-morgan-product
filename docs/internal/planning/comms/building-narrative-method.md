# How the Building Narrative Works

**Status**: canonical method doc (Comms-owned). First written 2026-06-03.
**Purpose**: capture the *conceptual model* of the building-narrative blog series as an ongoing practice — what it is, how we write it, how it has evolved — so it stops living only in PM's head and getting re-explained every session. The existing surfaces (template, voice guide, cadence doc, skills) already capture the *execution mechanics*; this doc owns the *model* and points to those for mechanics. It is the source for the `continue-narrative` skill.

**Why this exists** (the gap it closes): loaded surfaces encode how to *execute* a known task (form, voice, cadence) but not the *stance* of the narrative as a serial practice. Without the model written down, each fresh session reconstructs it from mechanics and gets the stance wrong — most commonly by treating an uncovered date span as a "gap to backfill" instead of a story to advance. This doc is the fix.

---

## 1. What the building narrative IS (the load-bearing model)

### 1.1 Two parallel tracks: narrative vs. insight

The blog runs two content tracks that are sequenced by **completely different logic**:

- **Building narratives** (calendar `theme=building`) — the **chronological story** of building Piper Morgan, told in **beats**. A beat may cover one day, several days, or skip a quiet day. They are sequenced **in story order**. The question is never "which narrative is strongest" — it is always **"what is the next beat in the story, in order."**
- **Insight pieces** (`theme=insight`) — **time-decoupled** arguments/lessons. An insight from last November is equally eligible with one from last week; we deliberately mix time-distances and pair them by theme, not by date.

(Source: `memory/feedback_narrative_vs_insight_sequencing.md`.)

A third track, the **Weekly Ship** (`theme=ship`), is a weekly newsletter synthesized by Exec, not part of the building-narrative sequence — out of scope for this doc except where cadence intersects.

### 1.2 The narrative is LINEAR and CONTINUOUS — advance the front, don't backfill

This is the single most important stance, and the one most often gotten wrong:

> **The building narrative is LINEAR and CONTINUOUS. You advance the front; you do not backfill gaps. You wait when the next beat hasn't taken shape.**

A continuous serial story has a *front* (the latest work-day a beat covers), not a *coverage map* with holes to fill. The correct question is always "what's the next beat after the front?" — never "which days are uncovered?" Importing a coverage-audit frame ("we have N uncovered days, let's fill them") onto a serial story is the canonical error.

When the next beat hasn't clearly taken shape — the work since the front hasn't resolved into a story yet, or it's ambiguous how to continue — **you wait.** This is the Time Lord doctrine applied to narrative cadence: we publish when there's a beat to tell, not to hit an arbitrary slot. Waiting for more work to come in is a legitimate, expected state, not a failure.

(Source: `dev/2026/06/03/2026-06-03-0724-comms-code-opus-log.md` §"Methodology note 1"; Time Lord doctrine: `memory/feedback_deadlines_are_triage_tools_not_default_pacing.md`, `feedback_time_lord_doctrine_no_false_urgency.md`.)

### 1.3 Insight-coverage ≠ narrative-coverage

A subtle trap worth naming explicitly: **mining a date range for insight pieces does NOT advance the narrative front.** Insights are time-decoupled (§1.1), so extracting lessons from, say, a May 16–24 window leaves the *narrative* front exactly where it was. The two tracks advance independently. When assessing where the narrative stands, count **beats**, not insights.

(Source: same June 3 log, §"Methodology note 1" — a distinction PM and Comms both briefly conflated.)

### 1.4 The "slate" concept — drafted long, then tightened

A **slate** is a curated sequence of beats covering a build-story span (e.g., the most recent: the **Apr 23 → May 15 build story in 9 beats**, Beat 9 = *The Hook and the Worktree*, covering May 13–15). A slate is **drafted long, then tightened** — you draft generously (e.g., a 13-beat draft), then merge/drop/tighten to the final sequence (9 beats). Beats are not just listed; they are *edited as a set* so the arc reads well.

Slate work is tracked **in the editorial calendar at creation** (every beat gets a calendar row when drafted) — this is the orphan-prevention discipline (a May 2026 incident produced 4 orphan drafts because a hand-maintained tracker went stale; the fix was calendar-row-at-creation, now enforced in `draft-blog-post` Phase 0/1).

(Source: `dev/2026/05/18/2026-05-18-0815-comms-code-opus-log.md`; `draft-blog-post` SKILL.md Phase 0.)

---

### 1.5 A beat is a STORY, not a digest of its window (PM, 2026-08-01)

> *"One thing I want to resist is feeling like we have to narrate every single thing that happens in a five- or seven-day period… We certainly can have an A plot and a B plot… but sometimes you really have to pick and choose what the actual story is."* — PM

**The wider spans are working and should continue.** PM's read: *"the story does an inch a day or so at a time, but often takes leaps of a week or five days. I think that's a good trend."* The leaps are the win. **What must not come with them is the obligation to account for everything inside the leap.**

**Structure to use**: an **A plot** — the actual story, the thing the beat is about — and optionally a **B plot**, plus room for something funny or strange. **Not** a section per workstream. A beat that touches every thread of its window is a digest wearing a story's clothes, and it reads like one.

The selection question at draft time is *"what is the story here?"* — not *"what happened here?"* Material that doesn't serve the A or B plot is **cut, not compressed**. It is not lost: it stays available to the insight track (time-decoupled, §1.1), or to a later beat, or to the Weekly Ship, which is the surface that legitimately *is* comprehensive.

#### ⚠️ The measured version, because the causal story is not the obvious one

Length is rising, and by more than "creeping" (measured 2026-08-01 across 57 published narratives + insights):

| month | n | mean words | max | over 1,300 | over 1,600 |
|---|---|---|---|---|---|
| 2026-03 | 4 | 797 | 1,085 | 0 | 0 |
| 2026-04 | 14 | 1,038 | 1,459 | 2 | 0 |
| 2026-05 | 4 | 1,106 | 1,345 | 1 | 0 |
| 2026-06 | 18 | 1,265 | 1,796 | 9 | 2 |
| **2026-07** | **17** | **1,399** | **2,526** | **9** | **6** |

Mean is up **75%** in five months, and **July's average (1,399) is itself above the 1,300 target ceiling** — so it is no longer a matter of outliers.

**But span is NOT the cause.** Correlation between covered span and word count across 21 published building narratives is **+0.10** — effectively none. The extremes make it plainly:

- *The Team Catches the Cycle* — **2 days**, **2,093 words**
- *RECONNECT's Keystone* — **9 days**, **1,680 words**

**So the tradeoff people assume — cover more time, accept more words — does not exist in our data.** Length growth is a **drafting habit**, not a structural consequence of wider windows. That is the encouraging version: **keep the leaps AND cut the length**, because they were never actually coupled. A long beat is long because everything got in, not because the window was wide.

*(Caveat, stated so nobody over-reads it: n=21 and a weak correlation is soft evidence for no-relationship. The 2-day/2,093-word case is the decisive one on its own.)*

**Practical test at draft time**: if you can't name the A plot in one sentence, the beat isn't a beat yet — it's a window with material in it. And if a section exists mainly because something happened, that's the cut.

---

## 2. How we write it (mechanics — owned elsewhere, pointed to here)

This doc deliberately does **not** duplicate mechanics (that's how docs go stale). The canonical mechanics files:

| Concern | Canonical file |
|---|---|
| Post structure, frontmatter, dateline, footer, length | `docs/internal/planning/comms/blog-post-template.md` |
| Voice & tone (semicolons, "load-bearing", comma splices, etc.) | `docs/internal/planning/comms/xian-voice-tone-guide.md` |
| Publishing cadence (which category publishes which day) | `docs/internal/planning/comms/publishing-cadence.md` |
| Blog-first target state | `docs/internal/planning/comms/publishing-workflow-target.md` |
| The live tracking artifact (18-col schema) | `docs/internal/planning/comms/editorial-calendar.csv` |
| Drafting workflow (variant detection, orphan-prevention) | `.claude/skills/draft-blog-post/SKILL.md` |
| Editing the calendar (only sanctioned way) | `.claude/skills/update-calendar/SKILL.md` |
| Publishing to the website | `.claude/skills/publish-to-blog/SKILL.md` |

**The few conventions worth restating because they're load-bearing AND easy to get wrong:**

- **`workDate` / `endWorkDate` = the source-work-period the post is ABOUT, not the drafting date.** These derive the dateline italics. (PM-ratified 2026-05-17; `memory/feedback_calendar_workdate_is_source_work_period.md`.) ⚠️ The `update-calendar` SKILL.md currently mislabels this field as "when the piece was written" — that line is **stale and wrong**; anchor to the source-work-period convention. *(Fix that skill line — see §6.)*
- **Cadence** (Fri–Thu sprint week): Sat/Sun insights, **Tue/Thu narratives**, Wed Ship, no Fri/Mon post.
- **Syndication by category**: building → **Medium only**; insight → **Medium + LinkedIn**; ship → **LinkedIn only**. Canonical for all is **pipermorgan.ai** (§4).
- **Footer teases the very next scheduled calendar item, regardless of category.** (`memory/feedback_footer_teases_next_post_on_calendar_any_category.md`.)
- **Voice discipline is applied at draft-time**, not deferred to voice-pass (no semicolons in published prose, "load-bearing"→"critical" in public, comma splices are PM's deliberate voice, no number-led titles, no unverified superlatives).

---

## 3. How it has evolved (the eras)

Understanding the history matters because the *current* model is a reaction to the earlier one.

### Era 1 — Chat-era, high-volume daily building posts (mid-2025 → ~Feb 2026)
- Source = **chat sessions**; titles literally encoded it ("7/16 chat: …"). Near-**daily, high volume** with backlog publishing (Aug–Oct 2025: ~153 posts across 92 days; a July work-day might publish in August). This is the "one-per-day" era the narrative-vs-insight memory refers to as *no longer the rule*.
- **`robot-*` cartoons** dominated (peak Aug 2025–Feb 2026).

### Era 2 — Blog-first transition + Code-era (Mar 2026 onward)
- **Blog-first decision Mar 22 2026** (`publishing-workflow-target.md`): make **pipermorgan.ai canonical**; Medium/LinkedIn become syndication, not primary. First blog-canonical publish ~Mar 17 2026.
- **Editorial CSV becomes a git-tracked artifact** (~Mar 17 2026); earlier tracking was the `.xlsx` / chat-era spreadsheets. *(Pre-March tracking workflow = PM-head; see §7.)*
- **Cartoon shift `robot-*` → `ai-*`** (March 2026 onward).
- **Cadence written down Apr 26 2026** (`publishing-cadence.md`) — previously verbal/PM-head.
- **Migration to Claude Code Apr 22–26 2026** (all leadership roles incl. Comms; slugs `-opus`→`-code-opus`).
- **Shift from daily-volume to curated beat-slates** — the current model. Beats are deliberately sequenced and tightened (§1.4) rather than published one-per-chat-session.

(Sources: CSV-derived counts; `publishing-workflow-target.md`; `publishing-cadence.md` SHA `97b831ef0`; `CLAUDE.md` migration note; comms logs May 2026.)

---

## 4. Canonical hosting + publish pipeline

- **pipermorgan.ai is canonical.** `/blog/{slug}` for building/insight, `/shipping-news/{slug}` for ships. Medium/LinkedIn syndicate back with a canonical-link tag pointing to us. When PM says "the canonical link," they mean the pipermorgan.ai URL. (`memory/feedback_canonical_link_meaning.md`.)
- **Two-repo pipeline**: drafts + tracking live in this product repo (`docs/public/comms/drafts/`, `editorial-calendar.csv`); publishing pushes to the **website repo** (`../piper-morgan-website`) via the `publish-to-blog` skill / `publish-post.js` CLI (markdown→HTML, image→webp, append website `blog-metadata.csv` [separate 13-col schema], build, push). The website carries an era **`cluster`** taxonomy (curated era-slugs) — a site-side era model, flagged as overdue for an update (§7).

---

## 5. The continuation discipline (this becomes the `continue-narrative` skill)

When picking up "where's the narrative, what's next" — the recurring step — run this:

1. **Find the front.** In the calendar, identify the most recent work-day covered by a building-narrative *beat* (drafted or published). Use the beat's source-work-period (notes / workDate), not pubDate. Count beats, not insights (§1.3).
2. **Read the work since the front.** Review logs/omnibi for the days after the front (omnibi live in `docs/omnibus-logs/`; per-day session logs otherwise).
3. **Assess whether a next beat has taken shape.** Has the post-front work resolved into a story beat (a clear arc, tension, turn)? Is it clear how to continue the sequence?
   - **Yes** → draft it (hand to `draft-blog-post`); add the calendar row at creation; tighten as part of a slate if multiple beats are forming.
   - **No / ambiguous** → **wait.** Say so plainly. Waiting for more work to take shape is correct, not a miss (§1.2).
4. **Never backfill.** If a span between the front and now was skipped at the beat level (e.g., mined only for insights), do not retroactively fill it unless PM decides a specific beat is worth telling. Advance from the front.

---

## 6. Canonical source pointers

- **Model (this doc + its roots)**: this file; `memory/feedback_narrative_vs_insight_sequencing.md`; `dev/2026/06/03/2026-06-03-0724-comms-code-opus-log.md` §Methodology notes.
- **Mechanics**: the table in §2.
- **Cross-cutting memory pins**: `feedback_calendar_workdate_is_source_work_period.md`, `reference_publishing_cadence.md`, `reference_syndication_targets_by_category.md`, `feedback_canonical_link_meaning.md`, `feedback_footer_teases_next_post_on_calendar_any_category.md`, `feedback_insight_pairing_criteria.md`.
- **Briefing**: `docs/briefing/BRIEFING-ESSENTIAL-COMMS.md`.
- **Skill to build from this doc**: `continue-narrative` (the §5 discipline) → hands off to `draft-blog-post`.

**Known doc-debt to fix**: `update-calendar` SKILL.md mislabels `workDate` as "when the piece was written" — correct it to the source-work-period convention.

---

## 7. Gaps — PM-knowledge needed (do NOT confabulate these)

These came back from the grounding research as things only PM can confirm. Marked here so the doc is honestly incomplete rather than invented:

1. **Pre-March-2026 calendar workflow.** The CSV is git-tracked only from ~Mar 17 2026; earlier tracking was the `.xlsx` / chat-era spreadsheets. How the calendar was actually maintained pre-Code is PM-head. **[PM TO CONFIRM]**
2. **Exact daily→curated transition.** The cadence was *written* Apr 26 2026, but the "we stopped doing one-per-day" decision date isn't in any artifact — gradual Feb→Mar shift. **[PM TO CONFIRM the decision/turning point]**
3. **The slate-construction method.** Drafted-long-then-tightened (§1.4) is inferred from one May 18 log; is that the canonical process, and how do you decide beat boundaries / what merits a beat? **[PM TO CONFIRM / elaborate]**
4. **The era/`cluster` taxonomy.** Who maintains the website era-slugs, how eras get named, whether it's still maintained. **[PM / web-side TO CONFIRM]**
5. **Anything in §3 history I mischaracterized** — the eras are reconstructed from git + CSV, not from your memory. **[PM TO CORRECT]**

---

*First draft 2026-06-03 by Comms, grounded in a full-project research sweep (comms logs + process-doc commit history + website pipeline). Sections 1–2 + 5 are the load-bearing model; sections 3–4 are reconstructed history; section 7 awaits PM. This doc should be the thing PM points to instead of re-explaining — update it when the model evolves rather than re-teaching verbally.*
