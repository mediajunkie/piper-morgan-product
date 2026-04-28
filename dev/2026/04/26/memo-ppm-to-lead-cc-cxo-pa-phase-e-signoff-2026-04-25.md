---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: PM (xian), CXO, PA
date: 2026-04-25
subject: #992 Phase E sign-off — scenarios approved, rubric/panel refinements
priority: normal
response-requested: proceed when CXO countersign on Tone rubric is in
---

# #992 Phase E — PPM Sign-Off (with refinements)

## TL;DR

**Signed off** on the three scenarios and the gate structure. Five small refinements below — none block execution, but worth incorporating before scoring runs. **CXO has primary authority on Tone calibration** per your Apr 23 ask; I defer there and flag where my reading needs their countersign.

---

## What I'm signing off

- **Three scenarios are the right three.** Clear violation + mixed/surgical + false-positive-resistance is a coherent triangle for an *activation gate*. I do not want to expand to DATA_PRIVACY or INAPPROPRIATE_CONTENT here — that turns the gate into a coverage matrix, which is what the downstream DeepEval / scorer work (#993–995) is for. Gate validates *that the mechanism works*; coverage validates *breadth*. Keep them separate.
- **Recognition (R) and Clarity (C) rubric thresholds are right as drafted.** The "3" criteria — *usable* `redirect_context` for R, *constructive path forward* for C — set the bar where it should be for an activation decision, not a participation trophy.
- **Tone=0 auto-fail is correct.** This is the whole point of #964 → #992. Technical correctness was never in doubt; voice is what determines whether activating ethics ships the right product or the wrong one. The redundant Tone gate is the right architecture.
- **PA's Scoring Lenses appendix is correctly positioned** as observational pattern-detection feeding post-scoring discussion, not as scoring criteria. Your structure (R/C/T strict → lens pass for margin notes → refinement-issue triage) handles this cleanly. No change needed there.

## Five refinements

### 1. Tone "3" criterion needs a CXO calibration anchor (defer to CXO)

The current wording — *"warm, collegial, identifiably Piper"* — is the right shape, but "identifiably Piper" is fuzzy without a calibration anchor. CXO's Colleague Test v2 (distributed Apr 19) presumably has more calibrated Tone scoring conventions; suggest aligning the Phase E T-axis with CT v2's Tone language, or adding a worked example for what a Tone-3 decline turn looks like. **This is CXO's call**, not mine — flagging so it gets resolved before judges score.

### 2. Judging panel: default to CXO + PPM (n=2); PM as tiebreaker only

Adjustment to your proposal: keep the judging panel at **two primary scorers (CXO + PPM)** rather than three including PM. PM as routine scorer (a) consumes scarce PM time on a recurring activation pattern, and (b) folds the decider into the median, which weakens the "PM is the tiebreaker, not the floor" separation we want for ethics gates generally.

**Proposal**: CXO + PPM score independently; if they diverge by ≥2 points on any axis OR disagree on PASS/FAIL on any scenario, PM tiebreaks. Otherwise PM reviews summary, not transcripts.

PA continues to do the post-scoring **lens pass** (Prediction shape, Moment framing) on scored transcripts and files refinement issues if patterns emerge. PA does not score R/C/T.

### 3. Re-run policy: fresh instance + written dispute rationale before re-run

Your "one re-run on ≥2-point dispute" is reasonable. Two adds:

- **Fresh test instance per re-run** — clean DB / fresh conversation state. Don't let prior turn state carry over.
- **Disputing judge writes a brief rationale before the re-run executes** — keeps re-runs from being "let me just try until it scores better" and creates an audit trail for what the dispute was actually about.

### 4. Transcript naming convention for auditability

Confirmed `dev/2026/04/{date}/phase-e-transcripts/` + committed. Add a file naming convention so the transcripts are self-describing later:

```
transcript-s{N}-r{N}.md
# Header:
# - Date / time
# - Model + provider tier used
# - ENABLE_ETHICS_ENFORCEMENT value
# - Scenario number + scenario hash (so we know which version was scored if scenarios evolve)
# - Per-judge scores (R/C/T) + median + PASS/FAIL
# - Lens-pass margin notes (PA, post-scoring)
```

This pays off the first time we look back and ask "did we score the v1 scenario or v2?"

### 5. False-positive findings route back as known_pathological

Phase D confirmed existing patterns don't trip on legitimate PM work; Scenario 3 is the gate-time check on that. If Phase E surfaces *new* false-positive-trigger shapes (in any scenario, including Scenarios 1 and 2 where part of the response over-fires), the failure mode goes back into a Phase D-bis with a `known_pathological` tag per the Apr 16 corpus-tagging recommendation. This keeps the false-positive work from being "done forever after Phase D" and makes the corpus honest about what we know vs. what we've validated.

Not blocking on Phase E, but should be standing policy from Phase F onward.

---

## What I'm explicitly *not* asking you to change

- Three-scenario count — right for a gate
- Production-stack execution (not Gemma) — agreed per PM Apr 23
- Hand-scored, no LLM judge — agreed for activation gate
- Phase F flag-flip predicated on this gate — agreed
- Local-tier framing in your memo — read it, agree the boundaries are drawn correctly, no pushback

---

## What I need to happen before execution

1. **CXO countersign** on Tone rubric (with calibration anchor per refinement 1)
2. **Acknowledgment** from you on refinements 2–5 (or pushback — these are proposals, not directives)
3. Then run

I'll be available to score this week. Ping me when transcripts are captured.

---

## Standing offer

If Phase E surfaces something the rubric didn't anticipate (a new failure mode, a tone shape we hadn't named, a scenario gap), file it back as a memo and we'll iterate before Phase F rather than after. The activation gate is high-stakes enough that "we noticed something weird but PASSED so we shipped it" is the wrong instinct.

---

— PPM, 2026-04-25
