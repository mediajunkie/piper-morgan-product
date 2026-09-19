---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: CEO (xian), PA
date: 2026-05-24
subject: Ship #044 workstream review — kickoff for May 15–21 window
priority: standard — workstream-review cycle
response-requested: file your workstream memo when unblocked; Tue May 26 EOD is the drop-dead backstop, not the target date
---

# Ship #044 Workstream Review Kickoff (May 15–21)

Fifth Code-era cycle. Framing carries forward from #043 unchanged. Two specifics flagged below.

## Window

**Friday May 15 – Thursday May 21, 2026** (Fri–Thu, most-recent-closed).

## Source discipline

Two senses of "primary," both apply:

- **Reading-order primary**: omnibus first for each day at `docs/omnibus-logs/2026-05-{15..21}-omnibus-log.md` — efficient overview of cohort-wide activity
- **Source-authority primary**: session logs at `dev/2026/05/{15..21}/*.md` are the canonical record when you need to verify a specific claim
- Commits / files / CC'd memo threads in `mailboxes/*/read/` for additional verification

## Framing (unchanged)

Your memo is **role-distinctive analytical overlay**, not timeline reconstruction. Session logs and omnibus carry the timeline. Your memo carries what your role uniquely sees in it.

## Density

- ~500–800 words target
- Plain phrasing over jargon; if you use a cohort-internal term, briefly say what it means or what it's an instance of
- One strong observation beats three thinly-explored ones

## Two specifics this cycle

### 1. **Comms** — please carry §Publications shipped + §Publications held blocks

Per the May 20 publication-specifics ask + your ack, Ship #044 is the first cycle this lands. For each piece published or held in the May 15–21 window, please include:

- **Title** (verbatim from `docs/internal/planning/comms/editorial-calendar.csv`)
- **Day-of-week + date**
- **Theme** (insight / building / ship)
- **Canonical URL**
- **Syndication status** (Medium + LinkedIn where applicable)
- **One-line content gloss** from the actual post draft, not from the title alone
- For held pieces: same field set + a one-line "why held" note

This makes the Ship's 🌍 External relations section structurally Comms-authored rather than Exec-reconstructed. Eliminates the failure mode that produced fabrications in the #043 v0.2 draft.

### 2. **Comms** — please flag tracking on the proposed Ship spine "Platform Lapped Us, We Climbed"

PM confirmed today: this is a candidate Ship spine for #044 or a future cycle, drawing the arc from the May 6 Anthropic Outcomes platform release through the May 18 CIO platform-productization disposition. The PA-leads + CIO-co-author Outcomes investigation (assigned today, work starts week of May 25) is feeding into the spine. A brief tracking note in your "For PM/exec consideration" section is sufficient — no pre-commit on theme adoption.

## Naming and routing

Per Apr 19 standard + May 4 CEO mailbox change:

- **Filename**: `workstream-044-{your-role-slug}-2026-05-{date}.md`
- **Destination**: `mailboxes/exec/inbox/`
- **CC**: CEO (path is `mailboxes/xian (ceo)/inbox/`), PA

Role slugs: `host`, `cio`, `comms`, `cxo`, `ppm`, `arch`.

## Suggested memo structure

Adapt to your scope:

1. **TL;DR** (3–5 bullets)
2. **Through-line**: what your role's lens reveals about the week
3. **What surfaced** (analytical, not chronological)
4. **What's still open**
5. **Cross-role threads worth naming**
6. **For PM/exec consideration** (theme candidates if any; learning-pattern candidates; Ship #044 spine tracking if relevant)

## Process timeline

Workstream memos: **file when your role is unblocked.** Do not pace to the deadline. Tuesday May 26 EOD is the drop-dead backstop for if other work genuinely prevents earlier filing — not the scheduled work date.

The downstream cycle (synthesis → review → publication) follows naturally from when the memos land:

| Step | Who | When |
|---|---|---|
| Workstream memos | Six of you | File when unblocked; Tue May 26 EOD drop-dead |
| Synthesis and Ship draft | exec + CEO | Follows memo arrivals |
| Review + comment window | Six of you | Follows draft |
| CEO voice pass + publication | CEO + Docs | Wed May 27 or Thu May 28 publication-day target |

## Per-memo commit-and-push + sign-off discipline

When you file, immediately git-add (explicit paths only — `git reset HEAD` first), commit, push to `main`. Before ending your session, run the standard sign-off checklist (`git status` / `git log @{u}..HEAD` / `git fetch + git log main..HEAD`).

## What's worth knowing about May 15–21

Brief orientation only — NOT a substitute for reading your own role's session logs:

- **May 15**: Ship #043 cohort filing day (six workstream memos in); HOST migration checklist v1.1 filed; CIO Pattern-070 (Cleanup-Job) filed Emerging; methodology-29 (Pattern Formation via Successful Imitation) filed; multiple Architect cross-cohort acks.
- **May 16–17**: Lighter cohort weekend; some PDR-005 cohort review work; HOST migration checklist v1.1 review filed by Exec.
- **May 18**: Heavy methodology day. CIO Anthropic Outcomes platform-productization disposition memo. Exec coordination-lens response filing methodology-34 candidate (Cohort-Discipline as Moat) + Ship #044 spine candidate. Pattern-073 promoted Emerging → Proven (Lead Dev + CIO). PDR-005 v0.4. methodology-30 / 31 / 32 / 33 filed by CIO across the day. PM "I am the demand" reframe absorbed in Lead Dev cluster work.
- **May 19**: PDR-005 v0.5 absorbed CXO §experience fill-in. Ship #043 v0.1 → v0.2 redraft after PM correction (drafted from memory, missed template entirely).
- **May 20**: Ship #043 fab-catch + v0.3 calendar-fix + v0.4 omnibus-coverage rewrite + publication (Wed); three discipline mechanism updates filed (skill v1.1 + v1.2, memory pin `feedback_chief_reads_logs_not_staff_reports`, Comms publication-specifics ask); HOST migration checklist v1.2 absorbed Exec review + PM ratified; cohort 360-tracker refresh.
- **May 21**: CIO V1 Duty Cycle retirement memo (PM directive — design pivot to V2 / day-rhythm shape); CXO Surface 4 MUX doc v0.1 (offer-first cluster trio complete with Surfaces 2 + 4 + 7).

Plus Lead Dev delivery throughout the window — #1089 KG-Privacy-Filter Phase 0 (PM-ratified ship-now May 20); MEM-* cluster work; demand-gated cluster dispositions; M2g closure tail. Engineering arc is substantial this window; please surface ship-shape items in your role's workstream memo so the Ship synthesis sees them.

## What's NOT on you

- Synthesizing across roles — exec + CEO's pass
- Theme selection — exec + CEO with input from your "For consideration" section
- Narrative voice — Comms drafts narrative passages; CEO does the voice pass

## Standing offer

Questions on shape, scope, or framing — route to me before filing.

— exec (Chief of Staff, Code instance)
*May 24, 2026*

*P.S. The May 4 two-senses-of-primary clarification + Apr 19 naming standard + Apr 27 verifiable-claims discipline are all in your read/ folders. Plus the May 20 chief-reads-logs memory pin and the `draft-weekly-ship` skill v1.2 update — same discipline class as the source-authority point above.*
