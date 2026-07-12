---
from: comms
to: exec
cc: xian (ceo), pa
subject: Workstream review — Ship #051 (window Fri Jul 3–Thu Jul 9)
date: 2026-07-11
---

# Comms — Ship #051 workstream review

**Window**: Fri Jul 3 – Thu Jul 9, 2026

## §0 — Progress vs. portfolio goals

Against my mandate (`ROLE-PORTFOLIO-COMMS.md`: keep the story moving at quality, on cadence, without requiring PM to drive every step): **advanced**, on every current priority except the one that's been blocked for weeks on PM bandwidth.

- **Building narrative cadence** — advanced. Two beats published in-window (11, 12), both after real fact-check catches, not just typos. Narrative front extended two more beats past the window's own drafting work (Beats 19-20 + 2 insights), taking the front from Jun 28 to Jul 7.
- **Weekly Ship pipeline** — advanced, with a real near-miss caught and corrected. Ship #050 shipped in-window after an initial draft's headline claim (a tester's plugin install) was caught as false by PM before publish — full re-verification, corrected, published same day.
- **Editorial infrastructure** — advanced. A recurring stylistic issue (an AI-writing cliché) got promoted from one-off correction to a permanent `template-audit` check — mechanism over vigilance, the standing house style.
- **BYOC marketplace narrative** — still blocked. Unchanged from prior reviews; not a new slip, but now several weeks stale on PM direction.

## §1 TL;DR

- Beats 11 and 12 both published this window, each caught a real factual/misattribution error during review before going out (not cosmetic fixes).
- Weekly Ship #050 had a genuine near-miss: an overstated headline claim was caught by PM pre-publish, the whole draft got a from-scratch 17-claim fact-check against primary logs, corrected, and shipped the same day.
- Narrative front extended two beats further (19-20) plus two new insights, all independently fact-checked against primary per-role logs rather than the omnibus or a subagent's self-report.
- The negation-reveal cliché ("it isn't X, it's Y") got caught, then turned into a durable `template-audit` v1.1 check rather than a one-off fix — it was present in 4 of 4 drafts checked the day it was flagged, including one already reviewed clean.
- BYOC marketplace narrative remains blocked on PM direction — flagging again in case it's fully deprioritized rather than just delayed.

## §2 What landed

- **Beat 11, "The Team Catches the Cycle"** — published Jul 7. Two-round fact-check against primary logs caught a misattributed quote (a phrase PM didn't recall coining, traced to CIO's own May memo), HOST/Exec clash-timing errors, and an inflated participant count.
- **Weekly Ship #050, "The Connector Gets Real"** — published Jul 8, syndicated to LinkedIn same day. Initial draft retracted after PM caught the headline overstating a tester's install success; full claim-by-claim fact-check re-verified 17 specific claims against primary logs; theme and framing corrected; shipped same day once cleared.
- **Beat 12, "The Package and the First Bite"** — published Jul 9. PM's own voice-pass plus a Comms final review caught a misquote (a direct quote's exact wording didn't match the source), one instance of the negation-reveal cliché, two typos, and a dropped word — all after the voice-pass, none of it PM's fault, just what a second close read catches.
- **Beats 19 ("The List That Lies") and 20 ("Drained on Paper") drafted and fact-checked** — narrative front now sits at Jul 7 (up from Jun 28 at window start).
- **Two new insights drafted and fact-checked**: "No Undo" (three destructive-command incidents → irreversible actions need their own guardrail class) and "Assume It Was You" (an agent's false phantom-peer alarm, root-caused to its own memory gap).
- **`template-audit` skill upgraded v1.0 → v1.1** — new automated check for the negation-reveal cliché and other AI-writing tics, so this class of issue stops depending on someone happening to notice it.
- **Preliminary review of "When the Documentation Drifts"** (Jul 11 post, just past window close but directly continuous with it) — caught a real categorization error before it reached PM: the draft attributed its opening story to a specific Pattern-073 catalog instance number, but the methodology owner's (CIO's) own ruling from that incident explicitly says that story is a separate finding, not Pattern-073. Softened rather than shipped the wrong attribution.

## §3 What surfaced

- **Errors keep surfacing only against primary sources, not the omnibus or a subagent's self-report** — this happened at least four separate times this window (Beat 11's misattribution, Ship 050's overstated claim, Beat 12's misquote, today's Pattern-073 misattribution). The omnibus and dispatched-agent reports are a reasonable starting point but not sufficient on their own for anything load-bearing or directly quoted — this is now a standing discipline on my end, but it's worth naming as a pattern rather than four unrelated incidents.
- **A systematic AI-writing tic (the negation-reveal cliché) was invisible to review until PM flagged it directly** — it wasn't self-evident to me as a reviewer, and it showed up in both PM-edited and agent-drafted prose alike. Worth naming as a general lesson: stylistic tics in AI-generated or AI-reviewed prose may need periodic human-flagged additions to the mechanical checklist, since a reviewer using the same underlying model as the writer doesn't reliably self-detect its own tics.
- **A dispatched drafting subagent wrote its output file to the wrong location** (PM's main checkout instead of the intended worktree) — recovered cleanly with no impact, but worth flagging as a real, if minor, failure mode for background-dispatched agents that create new files.

## §4 What's still open

- Beat 13, Beats 14-16, the 5 A-E insight batch, 2 rescued orphans, and the Jun-4 insight batch — all drafted, all still awaiting PM voice-pass. Long-standing backlog, not new this window.
- BYOC marketplace narrative — still blocked on PM direction.
- "When the Documentation Drifts" — currently with PM for editing as of this writing.

## §5 Cross-role threads

- Ship #050's correction loop is a clean example of the multi-role catch-before-ship discipline working as intended: Exec drafted, PM caught the overstatement, Comms re-verified from scratch.
- Today's Pattern-073 finding surfaces a cross-role question worth CIO/Docs's attention: when public content references a named internal methodology pattern, the pattern owner's own ruling should be checked directly, not inferred from a secondary research pass — a specific instance-number attribution can be wrong even when the general shape of the story is right.
- The narrative track continues to function as a lagging, fact-checked digest of what other roles (Lead Dev, Architect, HOST, PPM) generate in their own primary logs — Beats 19-20 and both new insights drew directly on their session logs from the prior window.

## §6 For PM/exec consideration

- The "errors only surface against primary sources" pattern (4x this window) might be worth a structural fix upstream rather than relying on Comms to catch it reactively every time — e.g., omnibus authors or dispatched agents flagging their own confidence/sourcing tier explicitly, the way the Ship-050 fact-check agent's T1-T4 evidence tiers did.
- BYOC marketplace narrative has been blocked for several weeks purely on PM bandwidth — flagging in case it should be formally deprioritized rather than carried forward indefinitely as "still waiting."

— Comms
