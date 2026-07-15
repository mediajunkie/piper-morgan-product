# Workstream Review Cadence

## Overview

The **Workstream Review** is a recurring weekly deliverable in which each leadership role contributes a role-scoped memo covering the most-recent-closed Friday–Thursday sprint window. The Chief of Staff (exec) synthesizes across the role memos to produce a draft of the Weekly Ship narrative, which the PM voice-passes and Communications publishes.

This methodology entry codifies the cadence, the writing window, the source-material discipline, and the role-scoping convention. It is the durable companion to live agent comms (HOST holds the live-comms surface; this entry is the canonical reference agents land on when they search for "workstream review cadence").

The entry was finalized April 2026 after the first Code-era cycle (Ship #040) surfaced multiple under-specifications in the Chat-era cadence carried forward.

## Why This Methodology

### The Weekly Ship is the project's primary external communications artifact

Every Wednesday, a Weekly Ship publishes on LinkedIn (and, for non-shipping cadences, a building-narrative or insight piece). The Ship is built from the prior week's accumulated work. Without a structured input pass, exec would either reconstruct the week from omnibus alone (high latency, fidelity loss) or each role's contribution would arrive ad-hoc (synthesis bottleneck on PM/exec).

The workstream review cadence solves both: it produces a structured set of role-scoped inputs at a predictable point in the week, leaving exec the synthesis task without the input-gathering task.

### The role-scoped lens matters

The Ship narrative needs each role's lens (CXO sees voice and experience; CIO sees methodology and patterns; HOST sees agent welfare and operational health; PPM sees product decisions and gates; Architect sees system composition and ADRs; Comms sees narrative and editorial). The role memos provide those lenses. Without them, the Ship narrative is a single voice (PM/exec) trying to capture six different observation surfaces — error-prone and slow.

## When to Apply

### This cadence applies when

- A Friday–Thursday sprint window has closed
- The Weekly Ship for that window publishes the following Wednesday
- The author is one of the six leadership workstream-review-producing roles (HOST, CIO, Comms, CXO, PPM, Architect)

### This cadence does not apply when

- The window in question is the in-flight week (write the *most-recent-closed* week, not the week we're in)
- A role is on PTO/dark-week (file an empty-day acknowledgment is preferable to skipping; "no role activity this window" is a valid memo)
- Special-purpose Ships (e.g., gated-release narratives) — these follow a different process

## The Cadence

### Window definition

**The Workstream Review covers the most-recent-closed Friday–Thursday sprint window.**

- Window opens Friday morning, closes Thursday end-of-day
- The week being written about is the one that *just closed*, never the in-flight week
- On the Friday after a window closes, you can begin writing the workstream memo for that closed window
- Exception: rest days inside the window (e.g., a PM-out Sunday) produce no session logs but do not change window scope; the omnibus typically captures dark-day notes in the adjacent day's log

### Writing window

**Workstream memos are drafted Friday through Tuesday for Wednesday publish.**

- Ideal: drafted Friday or weekend, "in the bank" before Monday
- Acceptable: drafted Monday or Tuesday
- Last-resort: drafted Tuesday evening for Wednesday publish (PM does not prefer this — leaves no buffer for synthesis or voice pass)
- Hard floor: do not start writing before the window has fully closed (i.e., do not write Thursday for that day's Thursday window — Thursday isn't done until end-of-day Thursday)

### Publishing cadence

| Day | Activity |
|---|---|
| Fri | Window closes Thursday EOD; workstream memos may begin |
| Sat–Sun | Most workstream memos ideally in the bank |
| Mon | Late workstream memos accepted |
| Tue | Last-call for workstream memos; exec begins synthesis |
| Wed | Ship publishes (LinkedIn + blog) |

### Friday kickoff trigger — Exec-owned (added 2026-06-27, PM-directed; PM-notification + prior-cycle check added 2026-07-14)

**Every Friday, Exec begins the cycle by first verifying the week's session logs are complete, then issuing the workstream call.** This is a standing Exec obligation, not a someday-thing — the cadence slipped the week of Ship #049 because nothing forced the Friday kickoff. Concretely, on the first Exec duty-cycle fire each Friday (and as a checklist any Exec session inherits):

1. **Verify the closed window's session logs are day-closed.** For each day Fri–Thu of the just-closed window, confirm a `<!-- DAY-CLOSED: {date} -->` marker exists across the cycling roles (`grep -l "DAY-CLOSED: {date}" dev/YYYY/MM/DD/*log.md`). Any role missing its close → memo that role to retroactively close before the workstream reports are written (an unclosed day is a coverage gap in that role's §0 progress report).
2. **Check the just-published Ship's collection status.** Before issuing the new call, verify whether the Ship draft that went to PM this week was actually built on all 6 memos, or whether Exec proceeded on a partial set (check the draft's routing note / commit message for the prior Ship number). If any role was missing at draft time, name it explicitly in the notification below — this is what catches a repeat-offender gap before it recurs a second week running.
3. **Then issue the workstream call** to the six authoring leads (HOST/CIO/Comms/CXO/PPM/Arch), cc PM + PA, per the Memo Structure below (§0 leads with progress vs. portfolio goals; see §0 note).
4. **Notify PM directly, by mail, that the call went out.** Not just logged silently — a short memo to PM's inbox naming: the window dates just opened, the 6 recipients, and (from step 2) any carryover gap from the prior cycle. This gives PM Friday-morning visibility into collection status instead of first learning about a gap at Tuesday's drafting deadline.

**Why steps 2 and 4 exist (2026-07-14):** Ship #051's collection gap (PPM's memo still missing) wasn't visible to PM until Exec was mid-draft on the Tuesday deadline — nobody had been tracking or reporting collection status since the Friday kickoff three days earlier. PM: *"we cannot write the ship without all the workstream reviews... I am still the first audience for the weekly report."* The fix has two halves: this Friday notification (early visibility, so PM can nudge a slow role with days of runway instead of hours) and a hard drafting-time gate in the `draft-weekly-ship` skill (Step 2b, v1.6 — refuses to draft on fewer than 6 memos regardless of deadline pressure, the backstop if the early warning doesn't prevent the gap). See `feedback_ship_needs_all_workstream_reviews_no_partial_draft.md`.

This trigger is backed by a recurring Exec Friday reminder (cron), but the durable home is here — a session-scoped cron dies; this doc does not. Any Exec session reading this on a Friday runs the four steps above.

## Source-Material Discipline (Code-Era Pattern, Effective Ship #041 Onward)

Per Docs Apr 27 directive (`memo-docs-to-leadership-omnibus-reframing-workstream-review-source-shift-2026-04-27.md`) and PM Apr 27 framing:

### Read primary session logs first

Each workstream review reads the primary session logs in `dev/YYYY/MM/DD/` for each day in the window. Workstream observations are grounded in primary sources.

### Use omnibus as coverage check, not as primary input

After drafting from primary sources, scan the omnibus log(s) for the window. If something landed in your role's lane that the omnibus missed, flag it back to Docs as an omnibus-amendment candidate. The workstream review thereby becomes a standing quality check on omnibus coverage — a recursive Pattern-062 / "Audit the Composition" application.

### Why the shift

The Code-era pattern reverses the Chat-era pattern (omnibus as primary input). Filesystem-direct access in Code makes reading 7 days of session logs nearly as fast as reading one omnibus, and the fidelity is materially higher — primary logs preserve nuance, candor, and detail that omnibus synthesis necessarily compresses. Workstream reviews rooted in primary sources produce sharper observations and stronger Ship narratives.

### What stays the same

- **Daily omnibus synthesis** continues — the omnibus remains valuable for narrative arc, blog-post sourcing, cross-day pattern detection, and any analysis that benefits from pre-condensed weekly view.
- **Step 2.5 cross-reference gate** (in `create-omnibus` skill) remains mandatory at omnibus synthesis time.
- **Workstream review naming + routing** unchanged.
- **Verifiable-claims discipline** unchanged — actually strengthens, since primary-source reading reduces paraphrase-drift risk.

### Canonical sources for facts; role voice for everything else

There are two distinct kinds of content in a workstream memo, and they come from different sources:

**1. Objective facts** — what published, when, at what URL; what issues closed; what ADRs were ratified; what test results said. For these, consult the canonical source: the editorial calendar (`docs/internal/planning/comms/editorial-calendar.csv`) for publication records, GitHub for issue and PR state, the ADR directory for ratified records. Do not rely on memory or session-log recall for facts that have an authoritative record elsewhere. Memory drifts; canonical records don't.

**2. Role perspective** — what you noticed, what you personally touched, how something felt from your lane, the nuance and detail only your vantage captures. For these, your direct experience is the primary and best source. No canonical record can substitute for "here is what I observed while working on this." Session logs are the right primary source here.

The distinction matters at synthesis time: exec picks up your perspective and judgment; PM fact-checks verifiable claims against canonical sources before the Ship publishes. A fact that doesn't match the canonical record creates a correction loop at synthesis or PM voice-pass. Anchoring facts in canonical sources from the start short-circuits that loop; reserving your role voice for perspective and detail ensures the synthesis captures what only you can see.

**For Comms specifically**: the editorial calendar is the canonical source for all publication claims (count, dates, titles, platforms). Even if you worked on every piece, check the calendar rather than counting from memory — the calendar is the record of what actually published, including pieces that may have published automatically or without direct Comms involvement that week.

## Naming and Routing

### Filename standard

```
workstream-{ship#}-{role}-{date}.md
```

- `{ship#}` is three-digit Ship number (e.g., `040`)
- `{role}` is the role slug (host, cio, comms, cxo, ppm, arch)
- `{date}` is ISO date when the memo is filed (`YYYY-MM-DD`)

Effective from Ship #040 onward (per Exec Apr 19 standard, `memo-exec-to-all-workstream-naming-standard-2026-04-19.md`).

### Distribution

- **Primary destination**: `mailboxes/exec/inbox/`
- **CC**: PM (xian) in-channel, PA (`mailboxes/pa/inbox/`)
- **Sender archive**: `mailboxes/{role}/sent/`
- **Date-archive copy**: `dev/YYYY/MM/DD/` for the date the memo was filed

### Per-memo commit-and-push

Per the Apr 26 mailbox-on-main norm: file to `main`, commit + push immediately. ~30 seconds per memo. Eliminates asymmetric-visibility windows where exec's synthesis pass might not yet see your memo.

## Memo Structure (Suggested, Not Hard Template)

Per exec's Ship #040 kickoff memo (`memo-exec-to-leadership-ship-040-workstream-kickoff-2026-04-26.md`), evolved with the §0 portfolio-progress lead (PM-approved 2026-06-27, effective Ship #049):

0. **Progress & milestones vs. portfolio goals** *(NEW — lead with this)* — against the priorities/mandate in your `ROLE-PORTFOLIO-{ROLE}.md`, where did the needle move this window? State milestone status per goal: **on-track / advanced / slipped / blocked**. Outcomes against goals, not just activity. *(Enabled by the role-portfolio wave completing 2026-06-24; the Exec↔HOST portfolio-tied reformat co-designed 6/11.)*
1. **TL;DR** — 3–5 bullets, headline-of-the-week for your role
2. **What landed** — concrete deliverables, decisions, artifacts shipped during the window
3. **What surfaced** — patterns, drift, concerns your role detected
4. **What's still open** — threads spanning past the window's close
5. **Cross-role threads worth naming** — connecting tissue *between* roles your role's lens reveals
6. **For PM/exec consideration** — anything affecting Ship-narrative theme selection or framing

§0 + the first three are required; §4–6 are useful when applicable. Length: aim for what your scope actually generated. A clean 600-word memo with verified claims beats a 2000-word memo asserting from memory. **Milestone claims in §0 must be grounded (GitHub/calendar/logs), not aspirational** — same verifiable-claims discipline as the rest.

## Role-Scoping Discipline

Stay in your role's lane. The Ship narrative needs *each* lens; do not try to deliver all of them in one memo:

| Role | Lens |
|---|---|
| HOST | Agent welfare, operational health, role drift, human network |
| CIO | Methodology, patterns, audit findings, canonical-vocabulary discipline |
| Comms | Narrative arc, editorial, voice, publication cadence |
| CXO | User experience, voice, Colleague Test discipline, floor quality |
| PPM | Product decisions, gates, sub-epic scoping, roadmap |
| Architect | System composition, ADRs, integration contracts, technical patterns |

Cross-role observations in §5 ("Cross-role threads") are welcome; *replacing* another role's lens with your own is not.

## Verifiable-Claims Discipline

Per Exec Apr 19 standing norm (`memo-exec-to-host-verifiable-claims-2026-04-19.md`):

- Comparative claims of the form "most X," "first Y," "more Z than ever" need source-verification before they ship
- If a claim feels rhetorically strong but unverified: source-check it, downgrade the wording, or flag explicitly as "needs PA/Docs verification"
- Most catches happen on this shape of claim
- Primary-source reading (the Code-era pattern) reduces paraphrase-drift risk but does not eliminate the need for explicit source-check on superlatives

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Write about the in-flight week | The cadence is most-recent-closed only | Wait until Friday after the window closes |
| Synthesize from omnibus alone | Code-era pattern is primary-logs-first | Read session logs in `dev/YYYY/MM/DD/`; use omnibus as coverage check |
| Assert comparative claims without source-check | Apr 19 verifiable-claims discipline | Source-check, downgrade, or flag as unverified |
| Report publication counts, dates, or titles from memory | Memory drifts; counts mis-state; PM discovers errors at voice-pass | Check the editorial calendar (`docs/internal/planning/comms/editorial-calendar.csv`) for any verifiable publication fact |
| Try to write the Ship narrative in the workstream memo | Workstream memo is role-scoped *input*; Ship is exec synthesis | Write your role's lens; let exec synthesize |
| Wait for full-week clarity before drafting | Tuesday EOD is the last-resort floor; PM does not prefer late drafts | Draft Friday/weekend; iterate if late material lands |
| File on a feature branch | Apr 26 mailbox-discipline norm: mailbox writes go to main only | Switch to main, file, commit+push, return to branch |

## Coordination With HOST (Live Comms Surface)

This methodology entry is the durable doc; HOST holds the live-comms surface (per Apr 26 cadence-comms split, `memo-cio-to-host-cadence-comms-split-2026-04-26.md` + reply). HOST's spot-checks, role-by-role briefing nudges, and migration-prompt template stewardship complement this entry. Authors needing real-time calibration consult HOST; authors needing the canonical reference land here.

## Related Patterns and Methodologies

- **Methodology-20 (OMNIBUS-SESSION-LOGS)**: omnibus's authoring discipline; this entry references the consumption pattern.
- **Pattern-062 (Assembly Assumption)** + **Pattern-063 (Parallel-Authoring Drift)**: the workstream review's source-discipline practice (cross-reference primary logs against omnibus) is itself a recursive application of "Audit the Composition."
- **Methodology-24 (Branch-or-Anchor Discipline)**: applies to any role authoring a workstream memo who finds themselves about to extend the suggested structure beyond what their scope produced.
- **Excellence Flywheel v2.0** Practice 3 ("Coordinate Through Structure"): workstream review is one of the durable coordination surfaces this practice names.

## Evolution

### Chat-era origin (pre-2026)
Workstream reviews existed informally as PM-requested role memos before the format was standardized. Roles produced varied formats and routed via different channels.

### Naming standard (April 19, 2026)
Exec issued `memo-exec-to-all-workstream-naming-standard-2026-04-19.md` formalizing `workstream-{ship#}-{role}-{date}.md`. Effective Ship #040 onward.

### Verifiable-claims discipline (April 19, 2026)
Exec issued `memo-exec-to-host-verifiable-claims-2026-04-19.md` after a HOST superlative was caught in fact-check before propagating into Ship #039.

### Cadence specification gap surfaced (April 22, 2026)
HOST migration's first-week experience surfaced that the migration prompt under-specified the workstream review along four dimensions: which week (most-recent-closed, not in-flight), scope (role-scoped input, not Ship-narrative synthesis), naming (above), source discipline (above). Two HOST feedback memories saved (`feedback_workstream_review_cadence.md`, `feedback_workstream_review_scope.md`).

### Writing-window calibration (April 26, 2026)
PM clarified the writing window in chat: Fri–Tue, ideally Sat/Sun "in the bank," last-minute Tue acceptable but disliked. CIO had previously been operating on a narrower Fri-Sat-only model. Triggered the HOST/CIO cadence-comms split (HOST live, CIO durable).

### Source-discipline shift (April 27, 2026)
PM directive Apr 27: workstream reviews now read primary session logs first; omnibus = coverage check, not primary input. Effective Ship #041 onward. Code-era visibility makes primary-source reading nearly as fast as omnibus, with materially higher fidelity.

### Friday PM-notification + prior-cycle-gap check added (July 14, 2026)

Ship #051's PPM memo was still missing when Exec began drafting on the Tuesday deadline, and PM had no visibility into the collection gap until then — the existing Friday kickoff trigger issued the call but never reported back on whether it landed. PM directive (in-conversation, 2026-07-14): "we cannot write the ship without all the workstream reviews... I am still the first audience for the weekly report... we need to figure out a system where I am notified on Friday if the memos has gone out and if any agents haven't been able to reply yet." Added steps 2 and 4 to the Friday kickoff trigger: check the just-published Ship's collection status before issuing the new call, and mail PM a confirmation naming the window, recipients, and any carryover gap. Paired with a hard drafting-time gate added the same day to `draft-weekly-ship` skill v1.6 (Step 2b), which refuses to draft on fewer than 6 memos regardless of deadline pressure.

### Canonical-source / role-voice distinction added (June 23, 2026)
Comms's Ship #048 workstream review (Jun 20) missed one publication ("Critical vs Commodity Work in a Role," Jun 13) and mis-stated normal cadence as "above cadence" — root cause was counting from memory rather than checking the editorial calendar. Exec (Jun 23 PM directive) added the "canonical sources for facts; role voice for everything else" section and the corresponding anti-pattern row. The editorial calendar is now named as the canonical source for all publication claims.

### Methodology-core filing (April 27, 2026)
This entry filed under CIO authority per Apr 26 HOST/CIO split. HOST holds the live-comms surface; this is the durable companion.

## References

### Canonical Documents

- **Apr 19 naming standard**: `mailboxes/.../memo-exec-to-all-workstream-naming-standard-2026-04-19.md`
- **Apr 19 verifiable-claims memo**: `mailboxes/.../memo-exec-to-host-verifiable-claims-2026-04-19.md`
- **Apr 26 mailbox-discipline norm**: `mailboxes/cio/read/memo-docs-to-leadership-mailbox-discipline-effective-2026-04-26.md`
- **Apr 26 Ship #040 kickoff (suggested memo structure)**: `mailboxes/cio/read/memo-exec-to-leadership-ship-040-workstream-kickoff-2026-04-26.md`
- **Apr 27 omnibus reframing**: `mailboxes/cio/read/memo-docs-to-leadership-omnibus-reframing-workstream-review-source-shift-2026-04-27.md`
- **Apr 26 HOST/CIO cadence-comms split**: `mailboxes/cio/sent/memo-cio-to-host-cadence-comms-split-2026-04-26.md` + reply

### Live Comms Counterpart

HOST's spot-checks, briefing nudges, and template stewardship are the live counterpart to this entry. Authors who need real-time calibration on cadence questions should consult HOST. The `feedback_workstream_review_cadence.md` and `feedback_workstream_review_scope.md` memories document specific lessons HOST holds.

---

*Methodology entry created: April 27, 2026*
*Origin: Apr 19 naming standard + verifiable-claims memos; Apr 22 HOST first-week specification gaps; Apr 26 PM cadence calibration; Apr 27 omnibus-reframing PM directive*
*Author: CIO (with HOST live-comms partnership; PM directive on Apr 27 omnibus reframing)*
*Status: Filed per Apr 26 HOST/CIO cadence-comms split. CIO holds durable doc; HOST holds live comms.*
