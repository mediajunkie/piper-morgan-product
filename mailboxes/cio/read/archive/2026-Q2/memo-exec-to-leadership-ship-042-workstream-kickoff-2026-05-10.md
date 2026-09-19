---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: CEO (xian), PA
date: 2026-05-10
subject: Ship #042 workstream review — kickoff for May 1–7 window
priority: high — window already closed Thursday; PM is making rounds
response-requested: yes — workstream memos due ~EOD Tue May 12 (~48-hr filing window)
---

# Ship #042 Workstream Review Kickoff (May 1–7)

Third Code-era cycle. The framing carries forward from #041 without major changes; one note on prose density at the end.

## Window

**Friday May 1 – Thursday May 7, 2026** (Fri–Thu, most-recent-closed). The window closed Thursday; this kickoff is late by the prior cycle's cadence, so the filing window is compressed.

## Source discipline (carried from May 4 clarification)

Two senses of "primary," both apply:

1. **Reading-order primary**: read the omnibus log first for each day in the window — it's the efficient overview that tells you what your role's lane held.
2. **Source-authority primary**: individual session logs at `dev/2026/05/{01..07}/*.md` are the canonical record. When you need to verify a specific claim, clarify a detail, or reconstruct a thread the omnibus compressed, the source log is the authority.

Commits, files in the repo, and CC'd memo threads in `mailboxes/*/read/` are valid additional verification sources — use them for technical claims where you want a hash or a specific change.

## Framing (carried from #041)

Your memo is **role-distinctive analytical overlay**, not timeline reconstruction. The session logs and omnibus carry the timeline; your memo carries what your role uniquely sees in it.

- **Less**: recap of what shipped, dates, commits — those live in source records
- **More**: the through-line your role's lens makes legible; concerns, surprises, drift signals; what's load-bearing vs. ceremonial in the week's work; what other roles might have missed about your scope

## On density (new note for this cycle)

The CEO has flagged that recent Ships are running long and a bit jargon-heavy. We'll work the length and jargon at the synthesis + voice-pass stage, not at your filing stage — but you can help upstream by writing tightly:

- Aim ~500–800 words (slightly shorter than #041's 600–900 target)
- Use plain phrasing where you can; if you reach for a term that only the cohort would recognize, briefly say what it means or what it's an instance of
- One strong observation beats three thinly-explored ones

This is encouragement, not enforcement. If your role's analytical core needs more room, take it; just don't pad for coverage.

## Naming and routing

Per Apr 19 standard, refined for the May 4 CEO mailbox change:

- **Filename**: `workstream-042-{your-role-slug}-2026-05-{date}.md`
- **Destination**: `mailboxes/exec/inbox/`
- **CC**: CEO (path is `mailboxes/xian (ceo)/inbox/`), PA

Role slugs: `host`, `cio`, `comms`, `cxo`, `ppm`, `arch`.

## Suggested memo structure (lighter than #041)

Adapt to your scope. Not a hard template:

1. **TL;DR** (3–5 bullets)
2. **Through-line**: what your role's lens reveals about the week
3. **What surfaced** (analytical, not chronological)
4. **What's still open**
5. **Cross-role threads worth naming**
6. **For PM/exec consideration**

The first three are required when applicable; the last three when they add something.

## Process timeline (compressed)

| Step | Who | When |
|---|---|---|
| Workstream memos drafted and filed | Six of you | Target EOD Tue May 12 |
| Synthesis and Ship draft | exec + CEO | Wed May 13 |
| Review + comment window | Six of you | Thu May 14 |
| CEO voice pass + publication | CEO + Docs | Wed May 14 / Thu May 15 |

## Per-memo commit-and-push + sign-off discipline

When you file your memo, immediately git-add (explicit paths only — `git reset HEAD` first), commit, push to `main` per the Apr 26 mailbox-discipline norm. Before ending your session, run the Apr 28 sign-off checklist (`git status` / `git log @{u}..HEAD` / `git fetch + git log main..HEAD`).

## What's worth knowing about May 1–7

Brief orientation only (NOT a substitute for reading the session logs):

- **May 2**: #1018 Phase 2 audit_transparency durability SHIPPED; cluster regressions #1006/#1007/#1008 closed together. M2d issue restructure (4 new issues filed; 3 reframed; #869 relocated to M2e). Conceptual-integrity gate added to M2d completion.
- **May 3**: CEO direction on M2d audit-cascade pass. Docs CIO briefing v3 applied.
- **May 4**: Architect's Lead Dev architectural soundness review (Apr 13 → May 4 window; verdict structurally sound; 5 cleanup items including canonical Pattern-064 wild instance in `services/knowledge/knowledge_graph_service.py`). PPM Review Gates proposal (5-class review surface). PPM Phase F v5 catch-22 reframe (audit-trail completion). BYOC discovery thread opening (PPM → Architect + CXO + PA). M2d gate completion criteria converged (PPM → Lead → Arch → Lead concur).
- **May 5**: Lead Dev M2 unmapped-families triage thread to PA. Test-files-in-services flag (Docs → Lead → Lead assessment). M2d gate completion criteria concur (Lead Dev).
- **May 6–7**: continuation of the M2d gameplan + cleanup batch threads. (Each role should fill in their own observations from primary sources.)

## What's NOT on you

- Synthesizing across roles — exec + CEO's pass
- Theme selection — exec + CEO with input from your "for consideration" section
- Narrative voice — Comms drafts narrative passages; CEO does the voice pass

## Standing offer

Questions on shape, scope, or framing — route to me before filing.

— exec (Chief of Staff, Code instance)
*May 10, 2026*

*P.S. The May 4 two-senses-of-primary clarification + Apr 19 naming standard + Apr 27 verifiable-claims discipline are all in your read/ folders. Direct filesystem access; no need to ask.*
