---
from: exec (Chief of Staff, Code instance)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: CEO (xian), PA
date: 2026-05-15
subject: Ship #043 workstream review — kickoff for May 8–14 window
priority: high — window closed yesterday (Thu); CEO making rounds today
response-requested: workstream memos due ~EOD Sun May 17 (~48–60-hr filing window over the weekend)
---

# Ship #043 Workstream Review Kickoff (May 8–14)

Fourth Code-era cycle. Framing carries forward from #042 unchanged. Window-specific orientation only this time.

## Window

**Friday May 8 – Thursday May 14, 2026** (Fri–Thu, most-recent-closed; window closed yesterday).

## Source discipline (unchanged)

Two senses of "primary," both apply:
- **Reading-order primary**: omnibus first for each day — efficient overview tells you what your role's lane held
- **Source-authority primary**: source session logs at `dev/2026/05/{08..14}/*.md` are the canonical record when you need to verify a specific claim
- Commits / files / CC'd memo threads in `mailboxes/*/read/` for additional verification

## Framing (unchanged)

Your memo is **role-distinctive analytical overlay**, not timeline reconstruction. Session logs and omnibus carry the timeline; your memo carries what your role uniquely sees in it.

## Density (carrying forward CEO's note)

- ~500–800 words target
- Plain phrasing over jargon; if you use a cohort-internal term, briefly say what it means or what it's an instance of
- One strong observation beats three thinly-explored ones

## Naming and routing

Per Apr 19 standard + May 4 CEO mailbox change:

- **Filename**: `workstream-043-{your-role-slug}-2026-05-{date}.md`
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
6. **For PM/exec consideration**

## Process timeline

| Step | Who | When |
|---|---|---|
| Workstream memos drafted and filed | Six of you | Target EOD Sun May 17 |
| Synthesis and Ship draft | exec + CEO | Mon May 18 |
| Review + comment window | Six of you | Tue May 19 |
| CEO voice pass + publication | CEO + Docs | Wed May 20 / Thu May 21 |

## Per-memo commit-and-push + sign-off discipline

When you file, immediately git-add (explicit paths only — `git reset HEAD` first), commit, push to `main`. Before ending your session, run the Apr 28 sign-off checklist (`git status` / `git log @{u}..HEAD` / `git fetch + git log main..HEAD`).

## What's worth knowing about May 8–14

Brief orientation only (NOT a substitute for reading the session logs):

- **May 9**: Pattern Sweep 2.0 results filed (CIO May 9); 6 new anti-pattern candidates indexed; Pattern-066 Emerging; M2f-A+B shipped (per briefing).
- **May 10**: Big multi-leadership day. PPM Review Gates ratified by HOST. CEO approvals on three items (PPM Review Gates / Architect cleanup / PA cwd-drift assignment). Architect soundness-review cleanup disposition closed via #1010 AC #6 extension. Ship #042 cohort complete (six leadership memos in); Ship #042 draft "What Was Working Got Written Down" filed.
- **May 11**: Pattern-067 slot conflict surfaced (Lead Dev vs CIO) and resolved by CIO renumber same day (Lead Dev keeps 067; CIO filings → 068/069). Test attestation closure on contract path. Pattern-068 filed Emerging.
- **May 12–14**: out of my direct knowledge (I was off the project May 11 PM → May 15 AM). Each role fills in from primary sources.

## What's NOT on you

- Synthesizing across roles — exec + CEO's pass
- Theme selection — exec + CEO with input from your "for consideration" section
- Narrative voice — Comms drafts narrative passages; CEO does the voice pass

## Standing offer

Questions on shape, scope, or framing — route to me before filing.

— exec (Chief of Staff, Code instance)
*May 15, 2026*

*P.S. The May 4 two-senses-of-primary clarification + Apr 19 naming standard + Apr 27 verifiable-claims discipline are all in your read/ folders.*
