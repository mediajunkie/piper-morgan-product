---
name: draft-weekly-ship
description: Draft the Piper Morgan Weekly Ship newsletter from collected workstream memos. Use when PM says "draft the Ship", "draft Ship #NNN", "synthesize the workstream memos", or when all 6 workstream-NNN memos have landed in `mailboxes/exec/inbox/` and a theme has been picked. Loads the canonical artifacts before drafting so memory-of-past-Ships doesn't substitute for structure.
scope: exec
version: 1.6
created: 2026-05-19
---

# draft-weekly-ship

Draft the Weekly Ship newsletter using the canonical template, voice guide, process guide, and workstream memos — *with all of them open before writing starts.*

**Origin**: Ship #043 v0.1 was drafted from memory of past Ship feel rather than opening the template. Result: pure essay form where structured newsletter was required, missed 5-workstream structure, missed learning-pattern 5-component shape, missed metrics table, missed footer convention, missed phase tag. PM correction May 19 directed re-read of source + template + voice guide before re-draft. This skill mechanizes the discipline so the same failure doesn't recur.

**Related memory**: `feedback_ship_drafting_canonical_artifacts_first.md` — the vocabulary layer. This skill is the mechanism layer.

---

## When to Use

Invoke this skill when:

- PM says "draft Ship #NNN" or "synthesize the workstream memos" or "draft the Weekly Ship"
- All 6 workstream-NNN memos are in `mailboxes/exec/inbox/` and a theme has been agreed
- You're picking up Ship drafting work after compaction or context loss

**Do NOT skip the canonical-artifacts loading step under time pressure.** This is exactly when the v0.1 failure mode fires.

---

## The Ingredients (load ALL before drafting)

### Canonical artifacts — read these FIRST

| # | What | Path |
|---|---|---|
| 1 | Process guide | `docs/internal/development/weekly-ship-process-guide.md` |
| 2 | Template v4.1 | `knowledge/weekly-ship-template-v4.1.md` |
| 3 | Voice & tone guide | `docs/internal/planning/comms/xian-voice-tone-guide.md` |
| 4 | Most recent published Ship | `docs/public/comms/drafts/published/weekly-ship-{N-1}*.md` (look up actual filename) |

### Sources for synthesis

| # | What | Path |
|---|---|---|
| 5 | All 6 workstream memos | `mailboxes/exec/inbox/workstream-{NNN}-{role}-{date}.md` (for roles: arch, cio, comms, cxo, host, ppm) |
| 6 | Omnibus logs for Fri–Thu window | `docs/omnibus-logs/2026-MM-DD-omnibus-log.md` for each day in the window |
| 7 | **Editorial calendar CSV** (REQUIRED for the External section) | `docs/internal/planning/comms/editorial-calendar.csv` |
| 8 | **Published-post drafts** (for any post you'll describe in External) | `docs/public/comms/drafts/published/{slug}.md` |

---

## Procedure

### Step 1: Load the canonical artifacts

Open all 4 in order. Read the process guide first (it tells you what the deliverable IS), then template (structure), then voice guide (tone), then most recent published Ship (in-practice example).

**Why this order matters**: The process guide names the 5 workstreams as REQUIRED. The template shows the structure with emoji prefixes and learning-pattern 5-component shape. The voice guide names the discipline (no semicolons, no "load-bearing" in public prose, no "CoS" in public prose, parenthetical gloss on first use of role names, temporal-relationship over absolute-date stamps, affirmative direct over disclaim-then-affirmative, section headings as noun phrases not verb phrases). The recent published Ship shows what the in-practice format actually looks like (which may have evolved from the template).

### Step 2: Confirm the window and theme

- **Window**: Friday through Thursday. Verify the dates in PM's request match.
- **Theme**: PM-picked, ideally from the 6 workstream memos' convergence. If theme isn't yet picked, surface candidates BEFORE drafting (don't draft on assumed theme).

### Step 2b: HARD GATE — all 6 workstream memos must be in before drafting starts

**Do not begin Step 3 with fewer than 6 of 6 memos present, regardless of deadline pressure.** Check `mailboxes/exec/inbox/` (and `read/` for any already triaged) for `workstream-{NNN}-{role}-*.md` from all six roles: arch, cio, comms, cxo, host, ppm.

- **6 of 6 present** → proceed to Step 3.
- **Fewer than 6** → STOP. Do not draft, even partially, even as a "placeholder to be filled in." Notify PM directly (chat + a mail note if PM is not in the current conversation) naming exactly which role(s) are missing and how close the pubDate deadline is. Wait for PM's call: extend, PM nudges directly, or (PM's explicit decision only) proceed on a named partial set.

**Why this is a hard gate, not a judgment call**: Ship #051 (2026-07-14) was drafted in full with PPM's memo missing, reasoning that the pubDate was the next day and a nudge had already gone out. PM overrode this directly: *"we cannot write the ship without all the workstream reviews."* PM is the Ship's first audience, not just its final reviewer, and is specifically most interested in the portfolio-goals lens that PPM's §0 carries — a draft missing it is missing the part PM most wants to read, not a minor gap to route around under time pressure. See `feedback_ship_needs_all_workstream_reviews_no_partial_draft.md`. The Friday early-warning check in methodology-25 (workstream-review-cadence) exists to catch a missing memo early in the week, before it becomes a Tuesday-deadline crisis — this gate is the backstop for when that early warning didn't prevent the gap anyway.

### Step 3: Read ALL omnibus logs in the window — REQUIRED, FULL READ

**This step is non-negotiable and not a spot-check.** Per PM directive May 20: the Chief of Staff reads the actual logs, doesn't rely on staff reports alone. Workstream memos are perspectives — each role lens is real but partial. Engineering shipped arcs in particular tend to live in the omnibus + Lead Dev session logs, not in the methodology-focused workstream memos.

For each day in the Fri–Thu window, open `docs/omnibus-logs/2026-MM-DD-omnibus-log.md` and read at minimum:

- **Day Type** + **Justification** lines (the omnibus author's framing)
- **Core Themes** section (the substantive list — this is where shipped items live)
- **Technical Details** section (commits, merges, specific deliverables)
- **Impact Measurement** section (per-role day-net counts)
- **Carry-Forward** section (open threads)

Extract a working list, organized by the 5 Ship workstreams, of:

- Issues closed end-to-end (search "shipped" / "merged" / "closed end-to-end")
- ADRs ratified or filed
- Pattern catalog changes (new patterns, promotions, supersessions)
- Methodology entries filed
- Process artifacts shipped (skills, hooks, templates)
- Publications + their canonical URLs (cross-check Step 4b)
- Cohort-coordination events (workstream-review cycles, cross-role coordination)
- Operational incidents + recoveries

If an omnibus log is missing for a day in the window (gaps happen), flag it explicitly and supplement from `dev/2026/MM/DD/` session logs for that day.

### Step 4: Read all 6 workstream memos — WITH OMNIBUS CONTEXT ALREADY IN HEAD

Now read the memos. With the omnibus substrate already loaded, the memos become commentary on what you've already seen rather than your primary source. This is the intended use.

During the read:
- Cross-check each memo's claims against the omnibus you already read
- Note where a memo emphasizes something the omnibus under-weighted (or vice versa)
- Flag factual conflicts between memos
- Track metrics that appear in multiple memos (they may differ — use the most current or conservative figure, prefix "~" for approximations)
- Identify the learning pattern candidate (often the memo with the most concrete data point)
- **Window-discipline**: anything from the day AFTER the window or earlier sessions referenced in the memos belongs out of the Ship

### Step 4-prime: Pull underlying session logs when something looks thin

If the omnibus for a day is shallow OR a workstream memo references substantive work that doesn't appear in the omnibus, open the relevant session log directly (`dev/2026/MM/DD/YYYY-MM-DD-HHMM-{role}-{code|opus}-log.md`). The session log is the ground truth.

**No superlatives without verification**: "longest," "most," "biggest," "first," "on record" all require 30-second history check. Soften to "substantial," "comparable to," "below" if you can't verify.

### Step 4b: REQUIRED — Verify the External section against the editorial calendar CSV

**This step is non-negotiable. The Ship #043 v0.2 fabrication caught May 20 was an entirely-invented External section because this step was skipped.**

Open `docs/internal/planning/comms/editorial-calendar.csv`. Filter to publications whose `pubDate` OR `liPubDate` falls in the Fri–Thu window. For EACH publication you will list in the External section, pull from the CSV:

- **Exact title** (do not paraphrase, do not abbreviate; do not invent titles to fit a Sat/Sun/Tue/Thu rhythm if the actual cadence varied)
- **Exact publication date** (`pubDate`, plus `liPubDate` if LinkedIn-syndicated)
- **Exact URL** (`blogURL` for canonical, `mediumURL` and `linkedinURL` for syndication)
- **Theme/category** (`theme` column — insight / building / ship)
- **Status** — anything with `status` other than `published` is held / queued / etc.; do not list as shipped

For a one-line content summary, open the actual post draft at `docs/public/comms/drafts/published/{slug}.md` and read the first 20–30 lines. Derive the description from the post's actual content. **Do not infer content from the title alone.**

Cross-check against Comms's workstream memo for the count (e.g., "four published, one held"). If your CSV-derived count doesn't match Comms's count, STOP and investigate before drafting — don't paper over.

**Sample CSV query** (Python):

```python
import csv
with open('docs/internal/planning/comms/editorial-calendar.csv') as f:
    r = csv.DictReader(f)
    for row in r:
        pub = row.get('pubDate', '')
        if pub.startswith('2026-MM-') and 'DD' <= pub.split('-')[2][:2] <= 'DD':
            print(row['pubDate'], row['status'], row['title'], row['blogURL'])
```

**Anti-pattern explicit**: do NOT pattern-match to a prior Ship's External-section shape (Sat insight / Sun insight / Tue narrative / Thu narrative) and fill the bullets with plausible-sounding invented titles. The cadence varies week to week. Use the CSV.

### Step 5: Draft using the template structure

Required sections in this order (per template v4.1):

1. **Frontmatter** (image + alt + caption)
2. **Title**: `# Weekly Ship #{NNN}: {Theme}` — sentence case for theme
3. **Dateline**: `*{Month DD–DD, YYYY}*`
4. **Opening**: 2–3 paragraphs capturing the theme or major milestone. Reference the previous Ship's theme for continuity if natural.
5. **`# 🚀 Shipped this week`** with the 5 workstreams in this order:
   - `## 🎯 Product & experience`
   - `## ⚙️ Engineering & architecture`
   - `## 🔬 Methodology & process innovation`
   - `## 🌍 External relations & community`
   - `## 📊 Governance & operations` (includes metrics as a **bullet list**, never a table — PM 2026-07-08)
6. **`# 🎯 Coming up next week`** — brief paragraph
7. **`# 🚧 Blockers & asks`** — brief paragraph
8. **`# 🔎 This week's learning pattern`** with name as `## {Noun-phrase pattern name}` and all 5 components:
   - **Discovery**: one-sentence description
   - **Example from this week**: specific instance
   - **Why it matters**: impact + what it addresses
   - **Application beyond this week**: how to apply elsewhere
   - **Related patterns**: links to similar patterns
9. **Footer**:
   ```
   **Thanks,**
   xian + Piper Morgan Development Team

   This is Weekly Ship #{NNN}. Previous: [#{N-1} "{TITLE}"](URL).

   *P.S. {Key takeaway or personal note}*

   *P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

   ---

   **Week of {Month DD–DD, YYYY} | Phase: {Current phase}**
   ```

If a workstream has no activity, INCLUDE it with a brief "No significant changes this week" note rather than omitting it.

### Step 6: Run the template's audit checklist against the draft

Verify before declaring done:

- [ ] All 5 workstreams present under "Shipped this week"
- [ ] Workstreams use correct emoji prefixes (🎯 ⚙️ 🔬 🌍 📊)
- [ ] Sentence case on all headings (not Title Case)
- [ ] Metrics included in Governance & operations as a **bullet list** (`**Issues closed:** 25`) — NEVER a table; Medium/LinkedIn don't render markdown tables (PM 2026-07-08, supersedes template v4.1's table format). Don't force uninteresting metrics to pad the list.
- [ ] Previous Ship linked in footer (title verified — do not trust memory)
- [ ] Phase tag at bottom matches current project phase
- [ ] Learning pattern has all 5 components (Discovery / Example / Why it matters / Application / Related)
- [ ] **No semicolons** in published prose (search the draft; should be zero)
- [ ] **No "load-bearing"** in public-prose sections (internal docbase keeps it; Ships tilt to "critical" / "central")
- [ ] **No "CoS"** anywhere (use "Exec" or "the Chief")
- [ ] Parenthetical gloss on first use of internal role names (e.g., "the product-management role (Piper Alpha)")
- [ ] Temporal-relationship language preferred over absolute-date stamps when the relationship is the point
- [ ] Affirmative direct preferred over disclaim-then-affirmative
- [ ] Section heading names are noun phrases, not verb phrases
- [ ] Word count check: 800–1,200 target; flag overage to PM with rationale
- [ ] **External section sanity check** — every title is character-for-character from the CSV; every date matches the CSV's `pubDate`; every URL pasted from the CSV (no invented slugs); every description is grounded in the post's actual content (not inferred from title); any held/queued posts named separately
- [ ] **Day-of-week sanity check** — every dated reference (e.g., "Tuesday May 13") matches the actual calendar; verify with `python3 -c "from datetime import date; print(date(YYYY,MM,DD).strftime('%A'))"` if uncertain
- [ ] **Role-attribution sanity check** — every "the X-role did Y" claim is traceable to a specific memo or omnibus entry (no invented attributions; no swapping who did what)
- [ ] **Time-since-codification claims** — any "the methodology was N days/weeks old when..." claim verified against the codification commit date (`git log -- docs/internal/development/methodology-core/methodology-NN-*` if applicable)

### Step 7: Save the draft and route for review

- **Save location** (canonical drafting): `dev/active/weekly-ship-{NNN}-draft-{YYYY-MM-DD}.md` on the `claude/{worktree-slug}` branch per worktree-default discipline for substantive output
- **Public-comms copy**: sync to `docs/public/comms/drafts/weekly-ship-{NNN}-draft-{YYYY-MM-DD}.md` on main so PM can read where they expect
- **Commit immediately after Write** per the May 17 memory
- **Route to PM FIRST — PM gates the handoff to Comms.** PM reads, fact-checks, voice-passes, and *decides when* the draft is ready to enter Comms review (PM, 2026-07-08, after Exec routed a draft to Comms prematurely: *"It's not ready to go to comms yet. I decide that."*). Exec never self-initiates the Comms handoff. Flag word count to PM if outside target.
- **Comms pre-publish review happens on PM's go** (PM clarification, same day: Exec generally drafts the Ship, but Comms reviews it before publish — a standing step). Comms's `template-audit` skill is their review-of-record; Exec's own Step-6 checklist pass does not substitute for it. Sequence is fixed: draft → PM → Comms → publish.

---

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Draft from memory of past Ships | Pure essay form will result; 5-workstream structure will be missed (v0.1 failure mode) | Open ALL 4 canonical artifacts BEFORE drafting |
| Start drafting after reading 3 of 6 memos | Theme bias toward early arrivals | Wait for all 6; read all 6 before writing |
| Trust memo claims as-is | Memos are perspectives, not sources | Cross-check substantive claims against omnibus logs |
| Use "First time" / "longest" / "most" without checking | Unverified superlative is a common error | 30-second history check, or soften the claim |
| Use Title Case on workstream headings | Template specifies sentence case | "Product & experience" not "Product & Experience" |
| Omit a workstream with no activity | Breaks week-over-week comparison | Include with "No significant changes this week" |
| Metrics as a table, or skipped | Medium/LinkedIn don't render markdown tables (template v4.1's table format is superseded, PM 2026-07-08) | Bullet list (`**Issues closed:** 25`), always included even if approximate |
| Use semicolons in published prose | PM voice discipline May 13 | Split into two sentences or use em-dash |
| Refer to Chief of Staff as "CoS" | PM directive May 15 | Use "Exec" or "the Chief" |
| Bullet-list a reflection-shaped piece | Voice guide May 11: reflection favors declarative paragraphs | Bullets for shopping lists, scoring rubrics, reference material only |

---

## Quality Checklist (final, before handoff)

- [ ] All 4 canonical artifacts were open during drafting (process guide / template / voice guide / recent published Ship)
- [ ] All 6 workstream memos read in full
- [ ] Omnibus logs spot-checked for substantive claims
- [ ] Template structure followed in full (5 workstreams + emoji prefixes + sentence case + metrics bullet list + 5-component learning pattern + footer + phase tag)
- [ ] Voice discipline passes (no semicolons, no "load-bearing" in public prose, no "CoS")
- [ ] Word count: 800–1,200 (or PM-approved overage with rationale)
- [ ] Draft committed to worktree branch immediately after Write
- [ ] Public-comms copy synced
- [ ] PM notified for voice-pass

---

## Key Insight

**LLMs struggle to follow templates while creating but excel at auditing against templates afterward** (per the audit-cascade skill). Same insight applies here. Open the template AND keep it open during drafting. Then run the audit checklist against the draft before declaring done.

The Ship #043 v0.1 failure was not knowing the template existed — it was choosing to draft from memory instead of opening it. The mechanism layer (this skill) makes the template-loading step procedural rather than remembered. That's the lesson Ship #043 itself names — *vocabulary plus mechanism plus sequence; each covers what the prior layer misses.*

---

## Related

- `feedback_ship_drafting_canonical_artifacts_first.md` — the vocabulary layer for this skill
- `feedback_blog_template_and_voice_guide_canonical_for_proofreads.md` — parent lesson (proofread version of the same shape)
- `feedback_no_semicolons_in_published_prose.md` — voice discipline
- `feedback_load_bearing_is_crutch_word_in_public_prose.md` — voice discipline
- `feedback_exec_nickname_is_exec_or_the_chief_not_cos.md` — naming discipline
- `feedback_parenthetical_gloss_on_first_use.md` — voice discipline
- `feedback_temporal_relationship_over_date_stamps_in_public_prose.md` — voice discipline
- `feedback_affirmative_direct_over_disclaim_then_affirmative.md` — voice discipline
- `feedback_workstream_review_cadence.md` — Fri–Thu window discipline
- `feedback_workstream_review_scope.md` — Exec synthesizes; 6 leadership roles author
- `feedback_ship_needs_all_workstream_reviews_no_partial_draft.md` — Step 2b's hard gate
- `docs/internal/development/methodology-core/methodology-25-WORKSTREAM-REVIEW-CADENCE.md` — Friday kickoff trigger + PM notification + prior-cycle-gap check (the early-warning half of the same fix)
- [audit-cascade skill](../audit-cascade/SKILL.md) — the parent procedural pattern this skill mirrors
- [create-omnibus skill](../create-omnibus/SKILL.md) — sibling skill for the omnibus log artifact

---

## Version history

### v1.6 (2026-07-14)

**Step 2b: HARD GATE — all 6 workstream memos required before drafting starts, no exceptions for deadline pressure.** Ship #051 was drafted in full (through the audit checklist, committed, pushed) with PPM's memo missing — Exec judged that a nudge had gone out and the pubDate was the next day, so proceeded on 5/6. PM overrode directly: "we cannot write the ship without all the workstream reviews... I am still the first audience for the weekly report and I am especially interested in the portfolio updates." Previously this was a should-wait norm (Anti-Patterns table: "Start drafting after reading 3 of 6 memos") without an enforced stop; v1.6 makes it a hard STOP-and-notify-PM gate at Step 2, before Step 3's omnibus read even begins. Paired with a Friday early-warning mechanism added the same day to methodology-25 (workstream-review-cadence) — that catches a missing memo early in the week; this gate is the backstop if the early warning didn't prevent the gap.

### v1.5 (2026-07-08, same day as v1.3/v1.4)

**Metrics are a bullet list, never a table** (PM, during Ship #050 review): Medium and LinkedIn don't render markdown tables, so template v4.1's Governance metrics-table format is superseded — use `**Issues closed:** 25` bullets. Don't force uninteresting metrics (e.g. a publications count) just to fill the list. Process guide's former "metrics table is the exception" line retired in the same pass. Also from the same review: the External section's publication list can be followed by one of the window's cartoon illustrations (image linked to its post, exact alt text from the calendar CSV, caption below with its quotation marks preserved).

### v1.4 (2026-07-08, same day as v1.3)

Two corrections from live failures the same day v1.3 shipped:
1. **PM gates the Comms handoff.** v1.3 named the Comms review step but let Exec self-initiate the routing ("either order"). Exec then routed a draft to Comms before PM had read it — a draft that turned out to contain a headline factual error. PM: *"It's not ready to go to comms yet. I decide that."* Sequence is now fixed: draft → PM (fact-check + voice-pass + handoff decision) → Comms review → publish.
2. **Evidence-tier discipline for claims** (see `dev/2026/07/08/ship-050-fact-check-2026-07-08.md`): the headline error traced to an *inference* in one agent's log that the omnibus printed as fact ("first external tester actively using it" — the tester had never successfully installed). The omnibus is the fact-check **baseline, not ceiling**: any claim resting solely on a log assertion with no artifact (commit/issue/URL/test output) and no PM witness gets softened, attributed, or cut before it enters a public draft. Step 4-prime's "session log is the ground truth" holds for *what an agent did*; it does not make an agent's inference about *someone else's* experience into ground truth.

### v1.3 (2026-07-08)

Step 7: added the standing **Comms pre-publish review** step (PM clarification, in-conversation: "You generally do draft the weekly ship but Comms reviews it before we publish"). Previously the routing step named only PM's voice-pass; Comms's review had been happening implicitly via the publish pipeline but wasn't a named, mandatory step in this skill. Also relevant context from the same window: Ship #050's window error (see `docs/internal/operations/ship-050-window-date-error-2026-07-08.md`) — the fix there is upstream in the kickoff procedure (compute window formulaically, assert day-of-week, verify delivery landed), not in this skill; noted here so a future reader doesn't add redundant machinery to this file. Step 6's existing day-of-week sanity check already covers the drafting side.

### v1.2 (2026-05-20, second update same day)

Reordered procedure: omnibus-logs-read is now Step 3 (BEFORE workstream memos), changed from "spot-check" to "REQUIRED, FULL READ." Workstream memos move to Step 4 with explicit guidance to read them "with omnibus context already in head." Added Step 4-prime: pull underlying session logs when omnibus looks thin or memos reference work the omnibus didn't surface.

**Trigger for v1.2**: PM caught Ship #043 v0.2's fab + coverage-gap structural issue same day v1.1 shipped. v1.1 added the CSV verification for publications but kept omnibus as "spot-check." That left the door open for me to lean on the methodology-focused workstream memos and miss the entire Engineering shipped arc of the week (#921, #857, #1071, #1021, M2f closure, M2g-A + M2g-B, #1070, #304, #1090) that lived in the omnibus logs and Lead Dev session logs. PM directive: "You are my chief and need to form your own views from reading the logs too!"

### v1.1 (2026-05-20)

Added required Step 4b (Verify External section against editorial calendar CSV) and four new audit-checklist items (External-section sanity check, day-of-week sanity check, role-attribution sanity check, time-since-codification claims). v1.0 had the discipline named ("verify all claims against omnibus logs") but did NOT enforce CSV cross-reference for publications. PM caught the fabrication in Ship #043 v0.2 on May 20 morning during pre-publication review. The skill missed: every publication title, every date, and every URL in the External section was fabricated by pattern-matching to Ship #042's format. v1.1 closes the gap.

### v1.0 (2026-05-19)

Initial skill. Lists canonical artifacts to load before drafting. Names voice-discipline checks. Procedure + audit checklist.

---

*Skill version: 1.6*
*Created: 2026-05-19 (v1.0)*
*Updated: 2026-05-20 (v1.1 — External-section verification step; v1.2 — omnibus is required full read, not spot-check); 2026-07-08 (v1.3 — Comms pre-publish review is a named mandatory step; v1.4 — PM gates the Comms handoff + evidence-tier discipline; v1.5 — metrics as bullet list, never a table); 2026-07-14 (v1.6 — Step 2b hard gate: all 6 memos required, no partial drafts under deadline pressure)*
*Scope: Exec (drafts); PM (gates); Comms (reviews)*
