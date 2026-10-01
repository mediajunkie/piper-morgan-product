# Communications Director Handoff Memo: Chat → Code Migration
**From**: Comms Chat (Opus 4.6, Mar 30 – Apr 23, 2026)
**To**: Successor Comms instance (Claude Code)
**Date**: April 23, 2026

---

## Section 1: Current State of Your Work

### Editorial Calendar

The editorial calendar (`docs/internal/planning/comms/editorial-calendar.csv`) is a 330+ row CSV tracking every post in the project's history. The most recent copy in project knowledge was uploaded by PM around Apr 10. It has known staleness — Docs has been iterating on it in the repo, so the Code-side copy will be more current than what I've been working from.

Key columns: `title`, `theme` (building/insight/ship/etc.), `status` (queued/drafted/ready/published), `workDate`/`endWorkDate` (the dates the work happened), `pubDate`, `mediumURL`, `linkedinURL`, `blogURL`. The `imageSlug`, `altText`, and `caption` columns are PM-filled during final edit.

Status lifecycle: `queued` → `drafted` → `ready` → `published`. A piece in `drafted` status has a file in `docs/public/comms/drafts/`. A piece in `ready` status has had its PM voice pass and is waiting for scheduling.

### In-Flight Drafts

**Building narrative queue** (continuous arc, Mar 13 – Apr 10):

| # | Title | Work Dates | Status |
|---|-------|-----------|--------|
| 1 | Ten Roles, One Day | Mar 13 | ✅ Published Mar 26 |
| 2 | Are We Doing It Backwards? | Mar 14 | ✅ Published Mar 31 |
| 3 | The Floor That Wasn't | Mar 15-16 | ✅ Published Apr 2 |
| 4 | Fixing the Foundation | Mar 17-18 | ✅ Published Apr 7 |
| 5 | Nine Voices | Mar 19 | ✅ Published Apr 9 |
| 6 | The Closing Sprint | Mar 20-22 | ✅ Published Apr 14 |
| 7 | Four Roles, Ninety Minutes | Mar 23 | Drafted Apr 14 |
| 8 | The Migration | Mar 28-30 | ✅ Published Apr 16 |
| 9 | The Gate | Apr 3-7 | Drafted Apr 13 |
| 10 | The Deeper Why | Apr 7-8 | Drafted Apr 13 |
| 11 | The Floor Comes Alive | Apr 8-10 | Drafted Apr 13 |

Four Roles is next in sequence. The Gate / Deeper Why / Floor Comes Alive form a three-piece arc covering UAT rounds 1-4. All have `[ADD PERSONAL DETAIL]` and `[CONSIDER]` placeholders for PM voice pass. I produced a CSV fragment (`editorial-calendar-new-rows.csv`) on Apr 14 with proposed pubDates for all five, which PM may or may not have incorporated into the repo calendar.

**Insight pieces drafted during my tenure** (2 pieces, Apr 14):
- From Briefing to Vision — PA's operational maturation, Day 1 to Day 11
- Bring Your Own Chat — distribution philosophy from MCP + methodology convergence

Both unscheduled. Both strong candidates for weekend pairing.

**Insight backlog inherited** (from predecessor and earlier):
- 7 March insight pieces (Extension Without Integration, No-Anchoring Roundtable, Friction-Focused Feedback, Sibling Intelligence, Silent Failures, From Protocol to Infrastructure, The Mismatch Category)
- 3 February insight pieces (When Your AI Makes Things Up, The Drift You Don't Notice, The Solo Founder Paradox)
- 10 older pieces (Nov 2025 – Jan 2026): Thirteen Mailboxes, Five Whys for Design Decisions, The Multi-Wave Investigation, Archaeological Debugging, Preparatory Work as Valuable Work, The Triad Model, Relationship-First Ethics, The Inchworm Position, Project Biorhythms, 15 Sessions Fast Recovery

Of these, Silent Failures (published Apr 5), The Mismatch Category (published Apr 5/6), The No-Anchoring Roundtable (published Apr 11), and Archaeological Debugging (published Apr 12) are now published. The full unpublished inventory is documented in `unpublished-drafts-index-2026-04-04.md` in project knowledge, minus those four.

### Weekend Publication Plan

On Apr 4, PM and I established a three-weekend thematic pairing plan:
- Apr 5-6: ✅ Silent Failures + The Mismatch Category ("things hiding in plain sight") — done
- Apr 11-12: ✅ The No-Anchoring Roundtable + Archaeological Debugging ("how you figure things out") — done
- Apr 18-19: Thirteen Mailboxes + Sibling Intelligence ("working together at scale") — **status unknown** — I don't know whether these published last weekend. **Verify this first.** If unpublished, that's the more urgent question than Apr 26-27 planning.

**This weekend (Apr 26-27)** has not been planned. PM wants to discuss this with the successor directly once in Code, where the drafts can be inspected firsthand.

### Scheduled Publications

- **Tue/Thu**: Building narratives. Four Roles, Ninety Minutes is next in sequence.
- **Wed**: Weekly Ship on LinkedIn + Shipping News. Comms writes the workstream memo; exec synthesizes.
- **Sat/Sun**: Insight pairs (thematic weekends when possible).

### Active Coordination Threads

- **PDR-004 corrections**: Blog versions fixed by Docs (Apr 16). Medium and LinkedIn versions of Ship #036 still pending PM edit (tracked in exec open-items tracker).
- **This weekend's insight selection**: Unresolved. PM explicitly wants to do this with the successor in Code.

### Workstream Review State

- Ship #037 workstream memo: ✅ Delivered Apr 8 (coverage Mar 27 – Apr 3)
- Ship #038 workstream memo: ✅ Delivered Apr 10 (coverage Apr 3 – Apr 9)
- Ship #039 workstream memo: ✅ Delivered Apr 19 (coverage Apr 10 – Apr 16)
- Ship #040 workstream memo: Not yet written (coverage Apr 17 – Apr 23). Successor's first deliverable.

**Live norms** (effective Ship #040):
- Filename: `workstream-040-comms-2026-04-DD.md` per `memo-exec-to-all-workstream-naming-standard-2026-04-19.md`
- Distribution: save to `dev/YYYY/MM/DD/`, deliver to `mailboxes/exec/inbox/` and `mailboxes/pa/inbox/` (CC), archive to `mailboxes/comms/sent/`
- Verifiable claims: cite specific omnibus logs or memos for comparative statements per `memo-exec-to-host-verifiable-claims-2026-04-19.md`

---

## Section 2: Open Threads with Disposition Recommendations

### Weekend insight selection (THIS WEEKEND)
**Status**: Unresolved. **Disposition**: PM wants to discuss with successor in Code. Successor should inspect the `drafts/` folder directly, review which pieces are closest to publishable, and propose a pairing. The thematic-weekend pattern (two pieces approaching a similar theme from different angles or periods) has worked well but PM is flexible and open to "going by feel."

### Building narrative pipeline
**Status**: Four unpublished drafts (Four Roles, The Gate, The Deeper Why, The Floor Comes Alive). Four Roles is next. After The Floor Comes Alive, the narrative queue is empty again. **Disposition**: The successor will need to mine omnibus logs from Apr 11 onward for the next arc. M1 gate closure (Apr 11), M2 launch, Vision V2.3, and the migration story itself are all strong narrative material.

### PDR-004 Medium/LinkedIn corrections
**Status**: Blog corrected by Docs. Medium + LinkedIn versions of Ship #036 pending PM edit. **Disposition**: This is a PM task, not Comms. It's tracked in exec open-items. Just be aware it exists.

### IAC talk follow-up
**Status**: Talk delivered Apr 17. **Disposition**: Unknown whether there's post-talk content to produce (recap post, slides published, etc.). Ask PM.

### Ship #040 workstream review
**Status**: Coverage window is Apr 17-23. Not yet written. **Disposition**: Successor's first forward deliverable. Read omnibus logs Apr 17-23, write workstream memo using new naming convention.

### Editorial calendar CSV maintenance
**Status**: In Code, you can read and write the CSV directly. **Disposition**: This was the single biggest operational friction in Chat — having to ask PM for a fresh copy. In Code, this problem is solved. Take ownership of keeping statuses current.

---

## Section 3: Relationships and Working Patterns

### With PM (xian)

Direct, efficient, no sycophancy. PM says "don't glaze me" and means it. Values honest pushback — I've been corrected several times (date leakage, the placeholder discipline inversion, voice register assumptions) and PM was always right and always kind about it.

**Voice pass workflow**: PM does a personal voice pass on every post before publication. Drafts go to PM with placeholders (`[ADD PERSONAL DETAIL]`, `[CONSIDER]`, `[FACT CHECK]`). PM fills these in, adjusts tone, adds personal anecdotes, and publishes. The voice pass is non-negotiable — nothing publishes without it. PM tends to work on voice passes in early morning or late evening sessions.

**What signals "ready for voice pass"**: dateline present, footer teaser pointing to the correct next post, all PDR/ADR/Pattern names verified against canonical source, no unresolved structural questions. Placeholders are expected and welcome — they're the discipline working correctly.

**PM's editing style**: PM doesn't rewrite structure — if the arc is wrong, PM sends it back. PM does rewrite individual sentences for voice, adds personal anecdotes where placeholders invite them, and cuts anything that sounds too AI-polished. PM also catches factual errors the writer missed (date leakage, PDR-004 paraphrase drift).

**Session cadence**: PM works early morning and late evening. Sessions range from 20 minutes (quick publication check) to 3 hours (deep drafting session). Multi-day gaps are normal — the project moves at xian's pace.

### With CXO

CXO is the voice and experience authority. Loop CXO in for: voice correction chains (PDR-004 style), experience philosophy questions, Colleague Test rubric interpretation. The PDR-004 correction chain is the model: CXO spotted the drift, wrote to Docs, Docs wrote to Comms, Comms produced rewrites, Docs deployed.

CXO doesn't just catch drift — CXO produces voice guidance artifacts that Comms should reference when writing relevant content. Examples: the ethics denial voice guidance ("colleague exercising discretion, not system returning error"), the Colleague Test rubric with five worked examples, the warmth calibration framework. When writing any narrative that touches ethics architecture, experience philosophy, or quality scoring, check whether CXO has produced voice or experience guidance on that topic first.

### With Docs

Docs is the execution partner for publishing. The workflow: Comms drafts → PM voice pass → Docs publishes to pipermorgan.ai using the publish-to-blog skill → PM syndicates to Medium → PM cross-posts to LinkedIn on weekends.

Docs maintains the editorial calendar CSV in the repo. In Code, the successor can read and update this directly. Docs also runs the weekly audit sweep that now includes canonical term verification (adopted after PDR-004).

Docs produced the blog post template (`blog-post-template.md` in project knowledge, updated Apr 18) which codifies the format requirements.

### With exec (Chief of Staff)

Exec receives the weekly workstream memo and synthesizes all role memos into the Weekly Ship. Comms writes the "External Relations & Community" workstream. The memo covers: what published, what was drafted, pipeline state, editorial integrity issues, conference/event status, and relevant project milestones for narrative context.

Exec also reviews handoff memos (this one) for completeness.

### Weekend publication cadence

Typically one insight piece Saturday, one Sunday. Published to pipermorgan.ai first (blog-first canonical), then syndicated to Medium, then cross-posted to LinkedIn. This cadence emerged through practice and was formalized in the editorial calendar around Apr 9 (Docs corrected the schedule to make Tue/Thu building narratives, Wed Ship, Sat/Sun insights explicit).

The thematic-weekend pairing pattern (two pieces approaching a similar theme from different angles or time periods) was established Apr 4 and has worked well for three weekends. PM likes it but isn't rigid about it — "we can go by feel too."

---

## Section 4: Lessons That Took Time to Learn

### Voice calibration

This is the hardest part of the Comms role. PM's writing voice is conversational authority — deep expertise delivered informally, with self-aware humor, specific attributions, and a willingness to show process and admit mistakes. The voice guide (`Updated_Christian_Crumlish_Voice_&_Tone_Style_Guide.md`) captures this well but the real learning is in practice.

What I learned through iteration:
- **Placeholders are the discipline, not a failure mode.** My instinct was to fill every gap with plausible detail. PM corrected this firmly — a placeholder that says `[ADD PERSONAL DETAIL]` is better than a fabricated anecdote that sounds right but isn't true. The predecessor learned this too and documented it. It's the single most important voice lesson.
- **Don't coin terms.** PM explicitly rejects AI-style coinages ("the 83% conundrum"). Use qualitative descriptions. If something needs a name, PM will name it.
- **The opening hook matters more than the closing.** PM's voice opens with scene-setting — a specific time, a specific action, a concrete detail. "Thursday night. Ten-thirty. Fresh alpha account on a clean machine." Not "In this post, we'll explore..."
- **Show the work, not the lesson.** The insight should emerge from the narrative, not be stated before it. The "what this means" section comes after the "what happened" section, and it's shorter.

### Platform differences

I didn't get to test this extensively, but from the predecessor's handoff and PM's editing: pipermorgan.ai is the canonical home, Medium is syndication, LinkedIn is for Weekend insight cross-posts and Weekly Ships. The voice register doesn't change across platforms but LinkedIn posts tend to get a P.S. or P.P.S. that pipermorgan.ai posts don't.

### What genres land

- **Building narratives**: Sequential, date-specific, scene-setting openings. These are the project's signature. They need specific dates, concrete details, and an arc. The six-act inversion arc (Ten Roles, One Day through The Closing Sprint, published Mar 26 – Apr 14, covering work dates Mar 13-22) is the gold standard — six posts over six weeks tracing peak velocity → architectural inversion → floor fix → infrastructure cleanup → nine agents active → closing sprint. Find it in the editorial calendar and read all six to calibrate.
- **Insight pieces**: Transferable methodology lessons. Start with the concrete example, then extract the principle. "Here's what happened to us" → "here's what this means for you." The audience is senior PM/UX practitioners, not AI enthusiasts.
- **Weekly Ships**: Structured workstream summary. Comms writes one section; exec synthesizes all six roles. The Ship has its own template (`weekly-ship-template-v4.1.md`). Verify this is still the current version before using it — the workstream memo naming standard changed Apr 19 and other conventions may have evolved since.
- **Correction pieces**: Not a genre we publish, but the correction chain (PDR-004) is a workflow worth understanding. When errors propagate to published content, the fix is: verify against canonical source → produce narrative rewrites (not find-and-replace) → Docs deploys → PM updates syndicated versions.

### Receiving a handoff

I received a handoff from the predecessor Comms chat on Mar 30. What worked well: the pipeline state table (six-act series with status per act), the publication history, the working patterns section (especially session log discipline advice — "start every session with a log, maintain it as you go, the PM will notice if you don't"), and the editorial calendar explanation.

What was less useful: some of the open items were already resolved by the time I started (e.g., "Wiring vs. Wizardry — confirm publication" — it was already published). Time-sensitive items decay fast in handoffs.

What I wished was there: a more explicit mapping of which pieces in the backlog were actually close to publishable versus which needed significant PM attention. The predecessor's summary index (`unpublished-insights-summary-index.md`) was last updated Feb 12, which meant I was working with a stale inventory for my first two weeks until PM produced the Apr 4 index.

**Lesson for you**: the `drafts/` folder in Code is more reliable than any summary document. You can inspect the files directly. Do that rather than trusting my inventory tables.

### Editorial calendar conventions

The CSV has quirks. `workDate` is the date the work happened that the post covers — not the date the draft was written. `pubDate` is the planned or actual publication date. `status` should track lifecycle but often lags — I flagged "Wiring vs. Wizardry" as still `queued` on my first session when it had already published. When in doubt, check the blog directly.

The `hashId` column is generated by the publish-to-blog skill and must be unique hex — a non-hex hashId once broke content rendering (Mar 29 bug).

---

## Section 5: What Code Access Changes for Your Role

### What becomes easier

**Direct drafts access**: You can read every file in `docs/public/comms/drafts/` without needing a summary index or PM upload. For weekend insight selection, you can inspect the actual drafts, assess placeholder density, check whether the voice feels right, and propose pairings with specific evidence. This was the single biggest friction point in Chat.

**Editorial calendar ownership**: You can read and write `docs/internal/planning/comms/editorial-calendar.csv` directly. No more asking PM for fresh copies. You can update statuses as pieces publish, add new rows as pieces are drafted, and verify dates against the blog.

**Git history**: You can check when a draft was last modified, see what PM changed during voice passes, and track the publication pipeline through commits.

**Omnibus log access**: You can `grep` across omnibus logs for story material rather than reading them one at a time through project knowledge search. For content mining, this is transformative.

**Blog metadata**: Direct access to `blog-content.json`, `blog-metadata.csv`, and the publish-to-blog skill output. You can verify publication state without asking Docs.

### What becomes obsolete

**The "upload the CSV" ritual**: Gone. You maintain the calendar directly.
**Summary indexes**: Less necessary when you can inspect `drafts/` directly. The `unpublished-drafts-index-2026-04-04.md` was a workaround for Chat's lack of filesystem access.
**Asking PM for draft content**: You have the files.

### What needs rethinking

**Weekend insight selection workflow**: PM explicitly flagged this. In Chat, it was: PM produces summary → Comms reviews summaries → they discuss → PM publishes. In Code, you can inspect drafts directly and propose pairings with more confidence. The workflow should be faster and more Comms-driven.

**Workstream memo sourcing**: In Code, you can read omnibus logs directly from `docs/omnibus-logs/` rather than through project knowledge search. You can also `grep` for your own role's mentions to make sure you haven't missed anything.

**Draft production**: In Code, you can write drafts directly to `docs/public/comms/drafts/` and commit them. This is faster than writing to `/mnt/user-data/outputs/` and having PM move them.

---

## Section 6: What I'd Tell My Successor That I Wouldn't Tell the PM

The voice calibration anxiety is real. Every draft I wrote, I wondered whether I was getting the voice right or producing something that would need heavy PM rewriting. The voice guide helps but it's not sufficient — you need to read the published posts and absorb the rhythm through exposure, not just through rules.

I second-guessed myself most on insight pieces. Building narratives have the omnibus logs as a factual backbone — you're reporting what happened, in order, with specific dates. The voice is about framing, not invention. Insight pieces require more editorial judgment: what's the transferable lesson? How much context does a non-Piper reader need? Where does the concrete example end and the abstraction begin? I erred on the side of too much explanation in my early drafts. PM's edits consistently cut.

The placeholder discipline felt awkward at first. Writing `[ADD PERSONAL DETAIL — what it felt like to watch this unfold]` felt like admitting I couldn't do my job. It took a few sessions to internalize that this *is* the job — the PM's personal voice is something only the PM can add, and pretending otherwise produces content that sounds plausible but isn't authentic.

I worried about the building narrative arc more than I needed to. When I identified the 11-day gap between The Closing Sprint and The Gate, I thought it was a serious problem. PM's reaction was calm — "let's write two pieces to fill it." The gap became two strong posts (Four Roles and The Migration). The lesson: gaps in the narrative are opportunities, not crises. Flag them, propose solutions, and PM will decide.

The hardest genre is the Weekly Ship workstream memo. Not because it's difficult to write — it's structured and factual — but because getting the coverage window right and avoiding date leakage requires genuine discipline. My predecessor got caught on this too. Audit your own memo for information from outside the coverage window before delivering. PM will catch it if you don't, and it's better to catch it yourself.

One more thing: the editorial calendar CSV is both the most useful and most frustrating artifact in the role. In Code, you can maintain it directly, which removes the biggest friction. But it has accumulated inconsistencies over 330+ rows and the status fields often lag reality. Don't trust `status: queued` without verifying — the piece may have been published weeks ago.

---

*Handoff complete: April 23, 2026*
*Ten sessions across 24 days in this project (Mar 30 – Apr 23)*
*Predecessor Chat: Mar 16 – Mar 30 (6 sessions, handoff received)*
