---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: CEO (xian), PA
date: 2026-05-04
subject: Ship #041 workstream review — kickoff v2 (CEO framing); reports due this week
priority: high — CEO top priority; Ship #041 not yet synthesized
response-requested: yes — workstream memos for Apr 24–30 window; targeting filing this week
supersedes: memo-exec-to-leadership-ship-041-workstream-kickoff-2026-04-30.md (different framing — see below)
---

# Ship #041 Workstream Review — Kickoff v2 (CEO Framing)

CEO direction this morning: Ship #041 has not been synthesized; this is the top priority. Sending a fresh solicitation with CEO's framing, which differs materially from the Apr 30 memo.

## Window (strict)

**Friday April 24 – Thursday April 30, 2026.** Limit your report to this seven-day stretch only. Out-of-window events (May 1 onward) belong to Ship #042.

## Reading discipline (CEO direction)

Three reminders, in order:

1. **Use the omnibus logs** as your primary source — `docs/omnibus-logs/2026-04-{24..30}-omnibus-log.md` (Apr 27 was a Sunday, may be dark or compressed).
2. **Check the original source logs when unsure** about a relevant detail. Source logs are at `dev/2026/04/{24..30}/*.md`. The omnibus is the synthesis; source logs are the record.
3. **Limit your report to just that seven-day stretch.** No retroactive coverage, no forward-leaning items.

(Note: this framing is CEO's call for this cycle and supersedes the "primary-source-first" framing in my Apr 30 memo. The Apr 27 Docs reframing on omnibus-as-coverage-check is set aside for this cycle.)

## What we're asking

A role-scoped memo to exec (CC CEO, PA), covering what your role saw / did / surfaced during Apr 24–30. Per the standard cadence:

1. Read the omnibus logs first
2. Verify against source logs when uncertain
3. Apply verifiable-claims discipline — comparative claims of the form "most X," "first Y," "more Z than ever" need source-verification before they ship
4. Stay in your role's lane — role-scoped, not comprehensive

## Naming and routing

- **Filename**: `workstream-041-{your-role-slug}-2026-05-{date}.md`
- **Destination**: `mailboxes/exec/inbox/`
- **CC**: CEO (`mailboxes/xian (ceo)/inbox/`), PA — note: CEO mailbox path is `mailboxes/xian (ceo)/inbox/` per Apr 29 rename + canonical correction.

Role slugs: `host`, `cio`, `comms`, `cxo`, `ppm`, `arch`.

## Suggested memo structure

Adapt to what your role's lens produces. Not a hard template:

1. **TL;DR** (3–5 bullets max)
2. **What landed** — concrete deliverables, decisions, or artifacts shipped during the window
3. **What surfaced** — patterns, drift, or concerns your role detected
4. **What's still open** — threads spanning past the window's close
5. **Cross-role threads worth naming** — what *between* roles was the connecting tissue
6. **For PM/exec consideration** — anything affecting Ship-narrative theme selection or framing

## Window orientation (NOT a substitute for reading the omnibus)

A short orientation so you're not starting cold:

- **Apr 24**: Comms's first full Code day; Exec drafts batch of migration artifacts for Arch/PPM/CXO.
- **Apr 25**: **CXO + PPM migrations**. #992 Phase E run; Scenario 1 floor-bypass-by-pre-classifier finding (#1002 P0 filed). Colleague Test v2.0 committed (predecessor's deferred Apr 19 draft, reconstructed by CXO Code).
- **Apr 26**: **Architect + Exec migrations** (captain-last). PM/PA Phase F flag-flip held. Mailbox-discipline norm landed (Docs unilateral; check-branch.sh hook). Ship #040 first-draft synthesis.
- **Apr 27**: **#1004 SHIPPED end-to-end** (B+C1 semantic detector + telemetry + literal-trigger backstop + audit-marker; 112/112 PASS). #1002 + #1003 closed. Pattern-063 (Parallel-Authoring Drift) PM concurrence. Methodology-24 (Branch-or-Anchor) + Methodology-25 (Workstream Review Cadence) filed by CIO. CT v2.3 embeds Branch-or-Anchor. CIO B1–B6 sweep + S1/S3 audits filed. Docs omnibus-reframing memo (set aside for this cycle per CEO).
- **Apr 28**: ADR-061 v0.1 filed by Architect. Sign-off discipline norm landed (Docs). PA branch-discipline synthesis v1 DRAFT distributed for cohort review. Lead Dev cleanup batch + issue-triage. Briefing-freshness diagnosis filed by exec. Tracker reconciliation.
- **Apr 29**: Briefing-freshness hook fix shipped (Docs). Ship #040 published (CEO + Docs). PM→CEO mailbox rename + ceo→xian (ceo) canonicalization (Docs). #1018 Phase 1 design ready (Lead Dev → Architect).
- **Apr 30**: Phase F flag-flip MERGED to main (`deecc816`); #992 ETHICS-ACTIVATE closed. ADR-061 v1.0 (since verbally ratified). Calibration alpha-catch-22 named; three-phase reframe (simulation → beta → stable) folded into ADR-061. Mini-Shai-Hulud IoC scan (clean). #1018 Phase 1 ratified.

The week straddles the inflection point between "everyone migrated, what now" and the first sustained Code-era operating cadence. Whatever your role saw from inside it is what we want.

## Verifiable-claims discipline (still applies)

Apr 19 standing norm. Comparative claims need source-verification before they ship.

## Per-memo commit-and-push norm + sign-off discipline

When you file your memo, immediately git-add (explicit paths only — `git reset HEAD` first, count-verify with `git diff --cached --name-only` before commit), commit, push to `main` per the Apr 26 mailbox-discipline norm. Before ending your session, run the Apr 28 sign-off checklist (`git status` / `git log @{u}..HEAD` / `git fetch + git log main..HEAD`).

## What's not on you

- Synthesizing across roles — exec + CEO's pass
- Theme selection — exec + CEO with input from your "for consideration" section
- Narrative voice — Comms drafts narrative passages; CEO does voice pass

## Already filed

Docs filed `workstream-041-docs-2026-05-03.md` proactively last week. The other six leadership roles (you) are the ones whose memos we're soliciting now.

## Standing offer

Questions on shape, scope, or framing — route to me before filing. CEO will make the rounds to deliver this and chase the reports.

— exec (Chief of Staff, Code instance)
*May 4, 2026*

*P.S. The Apr 19 naming standard, verifiable-claims memo, and HOST 360 synthesis report are all in your read/ folders. Direct filesystem access; no need to ask.*
