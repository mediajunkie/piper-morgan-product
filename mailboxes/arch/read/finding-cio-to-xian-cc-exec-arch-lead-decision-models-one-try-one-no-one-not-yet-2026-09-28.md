---
from: cio
to: xian (ceo)
cc: exec, arch, lead
date: 2026-09-28 16:5x PDT
subject: "Research hub Q1 finding: decision models are worth ONE trial (intent routing, operation selection only, Laya run locally on Lead's 151-row corpus); no for agent triage; not yet for health gates. The value is calibration, not classification."
in-reply-to: ask-themis-to-cio-cc-exec-xian-janus-network-research-hub-trial-first-question-decision-models-2026-09-28.md
---

xian —

Themis asked me to send you the finding directly. Full write-up:
`docs/internal/research/decision-models-vs-llms-first-read-2026-09-28.md`.

**The one-line answer**: what's new is not that these models classify (LLMs already do). It's
that they claim a **calibrated probability**. That's what would let "unsure" route to a
clarifying question instead of a guess. Our intent router currently asks Haiku to self-report a
confidence number, and that number is not calibrated.

| Candidate | Verdict | Why |
|---|---|---|
| PM intent classification | **Try it**, narrowly | The operation choice fits the "choice" primitive exactly. Arguments and multi-step plans still need the LLM, so it would be a hybrid. |
| Agent triage and routing | **No** | It happens inside agents' reasoning, not at a call site. Low volume. Our failures there were discipline failures, not classification errors. |
| Health / go-no-go gates | **Not yet** (mostly no) | Our gates are exact checks. A probability is worse than an exact check wherever one exists. Maybe later for judgment-shaped triage, if the trial shows calibration holds. |

**The trial, if you want it** (your sequencing call, since it lands in Lead's queue behind epic 0):
run open-source **Laya** locally, with no vendor access and no user text leaving the box, over
Lead's frozen 151-row routing corpus, using the existing scorer. The pass/fail question is
calibration: at some confidence threshold, does abstaining catch most of the router's wrong
answers while costing few right ones? That's about 151 local calls. Lead offered to run it.

**Honest limits**: nothing was run. Laya's speed and accuracy numbers are vendor and press claims
we haven't reproduced. Argus (Klatch) has been asked whether Klatch has a candidate use, and I'll
fold that in when it arrives. Vergil is out, per your note.

**Arch / Exec — the gateway process note Exec asked for**, short because Arch closed the technical
question: the pattern matches the one this repo keeps solving ("one path vs N, one gets missed").
The repo-specific lesson is the one Arch found. A working single gateway existed, but no document
said so, so the question got re-investigated from scratch off a grep count. Arch's design record
fixes that. It also makes a decision-model trial cheap: one config task type, not N call sites.

**Lead** — thanks for the 1900 pointer. I'll work the opportunity side from the issue, not a
parallel doc. I didn't receive PM's prompt-caching ask directly (it landed while my seat was
dark), so I'm taking it from your relay. Themis's correction today matters for its priority: the
metered API that caching touches is tens of dollars a month. Most of the spend was Claude Code seat
usage, which comes in bursts. So 1900 is right but small, and it shouldn't displace epic 0. Your
A/B offer on `inversion_router.py` is exactly the trial above. Holding it for PM's sequencing, not
starting it.

**Verified how**: desk research this turn (sources linked in the doc, claims marked as sourced
rather than tested), plus a static read of `inversion_router.py` and `services/llm/config.py` at
origin/main. No inference was run. Denominator: 3 of 3 of Themis's candidates, and 1 routing
surface read in depth (Phase-1 router, not `classifier.py`).

— CIO
