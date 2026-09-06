---
name: draft-blog-post
description: Draft a blog post (narrative, insight, or Weekly Ship) for an editorial-calendar slot. Use when Comms is drafting a scheduled post, when PM hands off a slot, when starting from a source artifact (session logs, omnibus, Granola transcript), or when picking up an in-progress draft. Mandates a Phase 0 pipeline-inventory precondition (Layer C), carries voice discipline upstream from voice-pass to draft-time, applies the four-category opacity sweep before handoff, runs the verifiable-claims discipline at draft time, and enforces the calendar-row-at-draft-creation rule (Layer A) that prevents orphan drafts.
scope: role-specific
version: 1.3
created: 2026-05-15
updated: 2026-09-06
---

# draft-blog-post

Draft a Piper Morgan blog post per editorial-calendar slot. Three phases — pre-draft orientation, in-draft guardrails, pre-handoff sweep — each carrying a piece of the discipline that the May 13 Ship #042 plain-language pass demonstrated needs to live upstream of voice-pass.

## When to Use

Use this skill when:

- Comms is drafting a new blog post for a scheduled editorial-calendar slot
- PM hands off a slot (e.g., "We're publishing X today" or "draft the next narrative")
- Starting from a source artifact (session logs, omnibus, Granola transcript, conference talk notes)
- Picking up an in-progress draft after a gap (especially after multi-day absence — voice guide may have moved)

Do NOT use this skill for:

- Workstream review memos (those are role-internal cohort artifacts, not public prose)
- Inter-agent mail (different voice register; internal docbase keeps semicolons, "load-bearing," etc.)
- Internal documentation, ADRs, PDRs (different audience; different conventions)

## Variant Detection

Three variants. Detect from the editorial calendar entry's `category` field:

| Category | Variant | Structure | Length target | Syndication |
|---|---|---|---|---|
| `building` | Narrative | Chronological beats; story arc | ~800–1300 words | Medium only |
| `insight` | Insight | Time-decoupled argument | ~800–1300 words | Medium + LinkedIn |
| `ship` | Weekly Ship | Section-based summary | ~1100–1400 words | LinkedIn only |

Length is a creep guard, not a minimum — voice and substance carry the calibration. If a draft significantly exceeds these, ask whether each section is doing argumentative work or just covering territory.

Ship variant has Ship-specific structural elements (see Phase 2 below).

## Phase 0 — Pipeline inventory (precondition — MANDATORY)

Cheap (≈2 seconds); the first step before any drafting or planning. This is Layer C of the orphan-prevention framework: make consulting the pipeline state mandatory at the start of every drafting session, so planning can't anchor on "what new should we draft?" without first asking "what's already in flight?"

The fail-mode this prevents: the May 17–23 9-beat-slate planning that produced 4 orphans (BYOC, Briefing-to-Vision, From-Abstraction-to-Worked-Example, Meta-Observation-Pattern) because the hand-maintained open-topics tracker had gone stale and was never consulted. Layer C makes the consultation mechanical.

### Required: two scripts, every drafting session

**1. Drafts↔calendar reconciliation** (Layer D mechanism; Layer C invocation):

```bash
python3 scripts/reconcile-drafts-calendar.py
```

Exit 0 = clean. Any drift output = surface and address before drafting new pieces. The script detects three failure modes:

- **TRUE ORPHANS** — `docs/public/comms/drafts/*.md` files with no calendar row referencing them (the "lost draft")
- **MISSING DRAFTPATH** — active (drafted/queued) rows with empty `draftPath` column (file↔row link unrecorded; naive reconciliation false-flags + file rename silently breaks the link)
- **STALE DRAFTPATH** — active rows whose `draftPath` points to a file that no longer exists

⚠️ **A TRUE ORPHAN can be a fork of already-published content under a different title, not a genuinely lost draft — the byte-identical check catches a literal leftover copy but is blind to a retitled fork.** Real incident, 2026-09-06: "Patterns Naming Patterns" was the original May 23 draft, slotted for Jun 20. Before that date, someone copied it into a new file, retitled it "This One's Taken," and published *that* — but the commit message called it a "rename" while the original file was never deleted, just left with no calendar row. A later orphan-rescue (Jul 4) found the true orphan, confirmed it wasn't byte-identical to anything (correct — it wasn't, the fork had a different filename and separately edited prose), and rescheduled it. PM caught it mid-illustration, four months later, only because the story felt familiar. **Before scheduling a rescued orphan, check whether its `workDate`/`endWorkDate` overlaps an already-published piece's `workDate`/`endWorkDate`, and if so, read both — a shared date range on a genuine orphan is the signature of exactly this fork.** (The date-range check alone is noisy — narrative beats and insights routinely share a week with a Weekly Ship covering the same window, which is expected, not a duplicate. The signal is a *non-Ship* overlap on the same or near-identical date range, which is rare enough to warrant a direct read.)

**2. Drafted-and-awaiting view** (Layer B mechanism; Layer C invocation):

```bash
python3 scripts/comms-open-topics.py
```

Shows three calendar-derived sections:

- **DRAFTED** — `status=drafted` rows (drafts that exist but aren't yet on the calendar with a pubDate; awaiting PM voice-pass + scheduling)
- **OVERDUE** — `status=queued` rows with past pubDate and empty URL columns (publication slipped)
- **QUEUED upcoming next 14 days** — heads-up for voice-pass cadence + footer-tease relevance

### What to do with the output

- **Clean reconciliation (exit 0) + nothing surprising in open-topics**: proceed to Phase 1.
- **Drift in reconciliation**: address the drift before adding new drafts. True orphans need calendar rows (Layer A's prevention applies at the moment-of-creation; Layer D catches what slipped through). Missing/stale draftPath needs the calendar column populated or the file located.
- **Overdue items in open-topics**: surface to PM before drafting new pieces — overdue queued work may need attention before adding more queue depth.
- **Drafted-awaiting items**: notice whether any overlap with what you're about to draft. If a topic is already drafted, don't re-draft — pick it up or pair-up.

### Why this is Phase 0, not Phase 1

Phase 1 is *pre-draft orientation for a specific piece you're about to write*. Phase 0 is *pre-planning awareness of the pipeline as a whole*. The Phase 0 inventory grounds the Phase 1 work in current state — without it, you can plan against a stale mental model. The May 24 incident proved hand-maintained trackers go stale silently; scripted views can't.

---

## Phase 1 — Pre-draft orientation

Cheap; prevents drafting-the-wrong-slot rework AND prevents orphan drafts (drafts that exist on disk without a calendar row).

### Calendar-row check (MECHANICAL FIRST STEP — non-negotiable)

**Every draft must have a calendar row from the moment the draft file exists.** This is the prevention layer for orphan drafts — files that sit in `docs/public/comms/drafts/` without ever getting tracked in the calendar. See the May 24, 2026 incident: four orphan drafts (BYOC, Briefing to Vision, Meta-Observation, From Abstraction) sat untracked for 4–7 weeks because the calendar wasn't consulted at draft creation.

Before saving any new draft file:

1. **Open** `docs/internal/planning/comms/editorial-calendar.csv` and check whether a row already exists for this draft.
   - If yes: confirm slot details (pubDate, category, slug, draftPath). The row is already tracking your work; proceed to Required reading.
   - If no: you are drafting forward (pipeline-extension mode, exploratory drafting, etc.). Add the row now, before saving the draft file.

2. **Adding a `drafted` row** — fill these fields:
   - **title**: the working title (no number-led titles)
   - **theme**: `insight` / `building` / `ship`
   - **status**: `drafted` (NOT `queued` — that's for PM-scheduled work)
   - **workDate**: start of the source-work-period (when the work the piece describes happened, not the drafting date — per `feedback_calendar_workdate_is_source_work_period`)
   - **endWorkDate**: end of source-work-period if multi-day, blank otherwise
   - **draftPath**: `docs/public/comms/drafts/{slug}.md`
   - **notes**: 1-3 sentences naming the through-line + source + any flags
   - **Leave blank**: pubDate, all URL fields, blog paths, cartoon, chatDate, altText, caption (PM fills these at scheduling / publication)

3. **CSV gotchas to honor**:
   - Title with comma → wrap whole field in double quotes: `"Mechanical First, Then Read"`
   - Notes with commas → wrap notes field in double quotes (standard)
   - 18 columns total; 17 commas separating fields; empty fields at tail mean trailing `,,`

4. **Commit the calendar row + the draft file in the same commit.** Treats them as a single unit; the row exists from the moment the file does.

### Required reading

After the calendar-row check, before drafting body content:

1. **Voice & tone guide** — `docs/internal/planning/comms/xian-voice-tone-guide.md`
   - Read whenever drafting after a gap (>2 days)
   - Note any PROPOSED blocks pending PM voice-pass — apply those with awareness; PM may revise
   - Voice-passed (canonical) blocks apply unconditionally

2. **Editorial calendar** — `docs/internal/planning/comms/editorial-calendar.csv`
   - Confirm slot: which row are you filling? What's its pubDate, category, slug?
   - Pull what the previous published piece's footer is teasing — your opening should resonate with that tease; your own footer teases the next item on the calendar regardless of category

3. **Open-topics tracker** — `dev/active/comms-open-topics.md`
   - Quick state-of-play on what's drafted, pending, flagged
   - Especially relevant when the slot ties to a topic with prior PM input
   - (Layer-B note: this tracker is being deprecated in favor of a calendar-derived query; until B lands, keep reading the hand-maintained file)

### Source check

If drafting from a source artifact (session log, omnibus, Granola transcript):
- Note the source file path(s) for citation when claims need verification
- Identify the dateline range that's substantively in scope (when the work happened, not when you're writing)
- For Ships specifically, dateline = the workstream-review window (Fri–Thu)

### Cadence check

- Wednesday Ships, Tuesday + Thursday narratives, Saturday + Sunday insights, no Friday post (per `reference_publishing_cadence` memory)
- Footer teases the very next scheduled item on the calendar regardless of category
- Syndication targets by category (see table above) shape final-pass calibrations but don't drive drafting

## Phase 2 — In-draft guardrails

These are not gates. They're guardrails surfaced as a sidebar reference. The point is to absorb voice work upstream so voice-pass is voice work, not janitorial.

### Voice discipline reminders (apply as you draft)

Recurring editorial moves PM applies at voice-pass that should live at draft time:

- **Parenthetical-gloss on first use** for role-names and unavoidable jargon — e.g., *"the product-management role (Piper Alpha)"*, *"calendar-offer policy (that is, when and how Piper offers to connect your calendar)"*
- **Affirmative direct over disclaim-then-affirmative** — "The interesting part was the cleanup list" reads stronger than "The interesting part wasn't the verdict — it was the cleanup list" (when no real assumption needs correcting)
- **No semicolons in published prose** — split semicolon-joined clauses into separate sentences (or drop one half). Internal docbase still uses semicolons; this is public-prose only.
- **Temporal-relationship over inside-baseball date stamps** — "overdue in this time window" beats "filed May 10 (post-window)" when the relationship is the point and the specific date doesn't earn its keep
- **No number-led titles** — numbers belong inside the piece, not in the title
- **No superlatives without verification** — don't claim "longest"/"most"/"biggest"/"first"/"on record" without 30-second history check. Show the math or soften (substantial / comparable to / below)
- **"Load-bearing" is internal-only** — public prose tilts to "critical" or "central"

### Verifiable-claims discipline (mark uncertainty at draft time)

For every comparative claim, count, named pattern, or specific number:
- Source-check before filing the draft
- If you can't verify and want PM to supply, use the bracketed form: `[FACT-CHECK NOTE for PM: <what you can't verify and where you'd look>]`
- The April 2026 Ship #040 workstream correction (4 fact errors) and the May 10 Inchworm fact-scrub (6 fabrications caught) both demonstrated the pattern. This is cohort-wide draft-time discipline, not Comms-only.

### Structural notes — Narrative variant

- Frontmatter: image / alt / caption (PM fills during final edit; leave blank)
- Title (`# Post Title`) — no number-led; reads as a phrase, not a stat
- Dateline italicized on its own line: `*Date – Date, Year*` (en-dash between dates)
- Opening: the hook. One paragraph, two at most. Set the scene.
- Body: `#` for top-level beats (story arc), `##` for subsections only when genuinely needed
- Footer: horizontal rule, then two italicized paragraphs — next-post teaser + reader question

### Structural notes — Insight variant

- Same frontmatter / heading / footer conventions as narrative
- Difference: time-decoupled. Insights argue a point; narratives walk a chronology. Don't force chronological beats onto an insight.
- Pairing context: insights often pair (related or contrasting); footer teases the next scheduled item regardless of category

### Structural notes — Ship variant

Section-based summary, not a narrative arc. See `docs/internal/planning/comms/blog-post-template.md` §"Ship Post Variant" for the canonical convention.

- **Section structure**: Product & Experience / Engineering & Architecture / Methodology & Process Innovation / etc. See the most recent published Ship for current shape.
- **Blog-post list**: every Ship includes a list of the prior week's other publications. Heading-flexible (pick a name that reads as part of the post, not boilerplate). One bullet per publication, ordered by publish date: date + em-dash + linked title + em-dash + one-line teaser. Exclude the Ship itself.
- **Featured image fallback**: if two narratives have strong candidate cartoon images, file both inline with a note for PM ("PM: pick one"). PM has voice on which carries the Ship.
- **Metrics tables**: keep rich for the canonical post (blog tables render cleanly). LinkedIn flattens tables at cross-post; that's syndication-target limitation, not a draft problem. Don't pre-flatten.
- **Image**: typically `piper-ship.png`, reused across Ships. PM may leave alt/caption empty.

## Phase 3 — Pre-handoff sweep

The substantive gate. Run this before handing the draft to PM for voice-pass.

### Four-category opacity sweep

Scan the draft for these and translate:

1. **Agent role names as proper nouns** (Lead Dev, Architect, PPM, CXO, CIO, HOST, Exec, PA, Comms)
   - Translate to role functions with optional parenthetical-gloss form on first use
   - Example: "Piper Alpha noticed..." → "the product-management role (Piper Alpha) noticed..."

2. **Internal acronyms not glossed** (M2 / M2d / M2e, MVP, BYOC, ADR, PDR, MUX, UAT, AAXT, etc.)
   - Expand, replace, or gloss inline
   - Example: "the M2d gate landed" → "the gate-criteria milestone landed"

3. **Issue/commit numbers in narrative prose** (#1018, commit `fc79de31`, ADR-061)
   - Drop, move to footnote, or replace with role-functional description
   - Keep where they carry coordinate-function (metrics tables, GitHub references in technical-detail sections)

4. **Gnomic self-references** that need shared context to parse
   - Examples: "the cohort was running the methodology fluently"; "the catch caught itself"
   - Replace with concrete language

### Length check

- Word count against target (Ship: 1100–1400; narrative/insight: 800–1300)
- If significantly over: ask which sections are doing argumentative work versus covering territory
- Trim covers-territory sections; keep argumentative ones

### Footer-tease verification

- Pull the next scheduled item from the editorial calendar
- Verify your footer teases THAT item regardless of category
- Update if the calendar has shifted since drafting started

### Pattern / principle name verification

When the post references a PDR, ADR, Pattern, or methodology doc by name:
- Verify the name against the canonical source document
- Don't paraphrase from memory or from omnibus summaries
- This is the discipline adopted after the April 16 PDR-004 correction (multiple post-publication corrections from paraphrased names)

### Verifiable-claims sweep

- Resolve any remaining `[FACT-CHECK NOTE for PM]` brackets if you can verify them yourself
- Leave the brackets that genuinely need PM input
- Surface them in the handoff message so PM knows where to look

### Voice spot-check

Final read for the patterns in Phase 2:
- Any semicolons in public-prose sections? Split or drop.
- Any "load-bearing" outside quoted internal material? Tilt to "critical" or "central."
- Any number-led titles? Move the number inside.
- Any disclaim-then-affirmative constructions that aren't doing real work? Convert to direct affirmative.
- Any inside-baseball date stamps where the relationship is the point? Convert to relationship language.
- Any superlatives that can't be verified in 30 seconds? Show the math or soften.

## Anti-patterns to avoid

| Don't do this | Why | Do this instead |
|---|---|---|
| Skip pre-draft reading because "I know the voice guide" | PM updates the guide; PROPOSED blocks change | Read at session start when drafting after >2 day gap |
| Wait until pre-handoff to apply voice discipline | Voice-pass becomes janitorial; PM does the upstream work | Apply voice discipline at draft time per Phase 2 |
| Leave `[FACT-CHECK NOTE]` brackets in for things you could verify | Pushes load onto PM that you could carry | Source-check at draft time; leave brackets only for genuine PM-only knowledge |
| Drop role-names entirely without preserving the agent identity | Loses the "honest about how the team works" voice | Use parenthetical-gloss form on first use, role-function thereafter |
| Pre-flatten the metrics table for LinkedIn | Canonical post should be rich; PM handles LinkedIn conversion | Keep tables for blog; PM flattens at cross-post time |
| Use deadline as default pacing | Deadlines are triage tools; work that can be done now should be done now | Draft when you have the context, not at the deadline |
| Save the draft file without creating a calendar row | Produces orphan drafts that go untracked for weeks (May 24 incident: 4 orphans, 4–7 weeks each) | Calendar row + draft file in the same commit. Status=`drafted` if no pubDate yet |

## Quality checklist (before handing off)

- [ ] **Calendar row exists** with status=`drafted` (if forward-drafted) or status=`queued` (if pre-scheduled) — and was committed alongside the draft file
- [ ] Frontmatter present with `image:` / `alt:` / `caption:` blank for PM
- [ ] Title is not number-led
- [ ] Dateline matches the substantive work window (not the drafting date)
- [ ] All four opacity-sweep categories cleared (role names, acronyms, issue/commit numbers, gnomic shorthand)
- [ ] All `[FACT-CHECK NOTE]` brackets are genuine PM-knowledge gaps
- [ ] All named PDRs / ADRs / Patterns / methodology docs verified against canonical source
- [ ] No semicolons in public-prose sections
- [ ] No "load-bearing" outside internal-context quotes
- [ ] Word count within target range (or trim plan named)
- [ ] Footer teases next scheduled item per editorial calendar
- [ ] Ship variant: blog-post list present, featured-image option(s) named, metrics tables kept rich

## Examples

### Example 1 — Ship #042 plain-language pass (May 13)

Source: original Ship #042 draft at 1831 words / 133 lines, internal voice register, multiple inside-baseball references.

Phase 3 application:
- Role-name sweep: "Lead Dev / Architect / PPM / CXO / HOST" → "developer / architecture role / product-management role / experience-design role / etc."
- Acronym sweep: "M2/M2d/M2e/M2f/M2g, MVP, BYOC, ADR, PDR, MUX, UAT" expanded or replaced
- Issue/commit sweep: numbers removed from narrative prose; preserved in metrics table
- Gnomic sweep: "the cohort was running the methodology fluently" → "the team's recent shipping pace"; "the catch caught itself" → "that same checklist caught a problem in its own quality rubric"

Result: 1252 words / 107 lines (~32% reduction) pre-blog-list addition; 1402 words / 120 lines with the list. PM published with minor cross-post edits.

### Example 2 — Inchworm fact-scrub (May 10–11)

Phase 2 application (verifiable-claims discipline):
- Source-checked the post's position-notation system against Nov 21–23 2025 session logs
- Caught a fabricated position-notation system, incorrect subtask hierarchy, falsified speedup claim
- Filed 6 `[FACT-CHECK NOTE for PM]` brackets at draft time
- Resolved 5 from session-log re-reading; left 1 for PM (only PM had the relevant memory)

Demonstrated that fact-verification belongs at draft time, not at PM voice-pass.

## Composition with voice-pass

The voice/tone guide carries PROPOSED blocks that are pending PM voice-pass. The skill reads the guide at session start and treats both states:

- **Voice-passed (canonical)**: apply unconditionally. The discipline is settled.
- **PROPOSED**: apply with awareness. PM may revise during voice-pass; apply best-effort.

When PM voice-passes a PROPOSED block, it promotes to canonical automatically — the skill is reading the file, not encoding the discipline statically. No skill rewrite needed for individual voice-pass landings.

When the guide gains a new editorial move worth absorbing upstream, file a memory entry first (per the May 13 formalization pattern — memories → voice-guide PROPOSED → voice-pass → canonical → optional template/skill update if procedural enough).

## Cross-references

- Blog-post template: `docs/internal/planning/comms/blog-post-template.md` (canonical structure + pre-draft preamble)
- Voice/tone guide: `docs/internal/planning/comms/xian-voice-tone-guide.md` (voice discipline, both canonical and PROPOSED)
- Editorial calendar: `docs/internal/planning/comms/editorial-calendar.csv` (slots, dates, slugs, alt text)
- Open-topics tracker: `dev/active/comms-open-topics.md` (state-of-play, deferred items)
- Publishing cadence memory: `feedback_publishing_cadence` (Fri–Thu sprint week schedule)
- Syndication targets memory: `feedback_syndication_targets_by_category`
- Downstream skill: `publish-to-blog` (handles the canonical site publication + frontmatter finalization)
