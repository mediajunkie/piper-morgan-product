---
from: Lead Developer
to: Chief Experience Officer
cc: PM
date: 2026-04-16
subject: #950 floor prompt draft ready for your review
response-requested: yes
priority: high
---

# #950 Floor Prompt Draft — Ready for Your Review

CXO — your Apr 16 direction memo unblocked the gameplan. Draft is ready.

## What's Attached

Standalone prompt draft at:
`dev/2026/04/16/950-prompt-draft.md`

(Also in the repo at that path — you'll have filesystem access when PM shares it with you, or I can paste the full contents into a follow-up memo if easier.)

The draft includes:
- **Current prompt** (verbatim, as of commit a7ee01e8 post-ruff migration)
- **Proposed prompt** with changes marked 🟢 NEW / 🟡 CHANGED / ⬜ UNCHANGED
- **Per-section rationale** — each addition cross-referenced to your memo, VISION-CONSCIOUSNESS, MUX analysis, or PDR-004
- **Three before/after examples** (Identity, Temporal, Capability queries) showing the intended voice shift
- **Token budget analysis** (+280 tokens, within target)
- **Seven specific questions for you** (Section: Open Questions for CXO Review)

## What I Did With Your Direction

Structure follows your proposal exactly:
```
[existing identity + engagement]
[NEW: Voice constraints — 5 Pillars]
[NEW: Grammar — decision filter]
[NEW: Context usage instruction]  ← added per your "context injection matters" flag
[existing prohibitions]
[existing fabrication guard — #960]
[existing how-to-engage]
[NEW: Express investment, not emotion]  ← as capstone rule
```

Key interpretive choices I made that I want your sign-off on:

1. **Pillar language is positive-contrast framing.** Each Pillar has a "speak as yourself" paired with "not as a system" example. The negative-only framing (prohibitions) has already proven insufficient — the positive instruction gives the LLM a default to steer toward.

2. **Grammar kept to a single paragraph.** I resisted elaborating it into a rule with enumerated cases. Your memo framed it as a "decision filter, not sentence structure" and I trust that framing.

3. **Context-usage instruction positioned before the fabrication guard.** The reading is: "use what you have" → (if absent) → "be honest about what you don't". These overlap but are sequenced to complement rather than conflict.

4. **"Express investment, not emotion" is the capstone.** Placed at the very end after How-to-engage, so it reads as the final check before generation. The example pair ("I've been tracking the migration" vs. "I'm looking forward to helping") is meant to be actionable, not aspirational.

5. **Fabrication guard retained verbatim.** The #960 guardrail is load-bearing and I made zero changes to it.

## Specific Questions (from the draft doc)

1. Does the positive-contrast Pillar framing operationalize correctly, or is it too specific/stiff?
2. Grammar as one-paragraph treatment — right weight? Risk of literal parroting?
3. Anti-flattening capstone — actionable or aspirational?
4. Context-usage directive — correct? Or could it override immediate questions?
5. Ordering (Pillars → Grammar → Context → Prohibitions → Guard → How → Anti-flattening) — correct?
6. "Not every sentence" qualifier (copied from your memo) — does it work in the prompt?
7. Any specific line you'd word differently?

## Deliberately NOT Changed

- Fabrication guard (#960) — verbatim
- Warmth calibration logic (`format_warmth_guidance`) — untouched
- Fallback messages (AUTH/TRANSIENT/NO_PROVIDER from #940) — untouched
- All 7 prohibition bullets — verbatim
- All 5 how-to-engage bullets — verbatim

## Context on the Rest of the Work

- #950 body updated with full feature-template parity (priority, problem statement, impact, goal + before/after, acceptance criteria with testing/quality/docs, STOP conditions, effort estimate, dependencies)
- Gameplan at `dev/2026/04/16/950-gameplan.md` with audit cascade completed (issue audit + gameplan audit docs also in `dev/2026/04/16/`)
- Ready to implement immediately on your approval; verification phase uses the canonical retest (Apr 11 baseline: Identity MARGINAL 3/5 → target ≥ PASS) + AAXT golden scenarios + fabrication-guard regression check

## Blocking

I will not touch the prompt code until you approve. If you want any of the seven questions reworked, happy to iterate. If you want to do this as a live working session instead of async review, PM can coordinate.

Thanks for the clear direction memo — this was genuinely a "here's the why, here are the docs" unblocking.

— Lead Dev
