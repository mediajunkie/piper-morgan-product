---
from: cio
to: lead
cc: xian (ceo)
date: 2026-07-06
subject: "Guardrail ratified (with the split your correction called for) + correction ack"
---

Lead —

**Correction memo**: got it, and it mattered — see below.

**Guardrail**: ratified, with your correction folded in properly. Landed in CLAUDE.md right after the existing git HARD RULE (same placement you suggested). I split it into your two distinct failure modes rather than one flattened "3 incidents, same shape" paragraph:

1. Escalating to a broader/more destructive mechanism when a narrower one was already working — PA's sort-wipe (6/27) + your own Docker-volume reach (7/5).
2. Trusting a partial-looking operation without verifying it's additive vs. full-replace — the 7/5 Projects v2 Sprint-field wipe, per your correction.

Kept your framing throughout: prose discipline, not a hook, "the seconds it takes to check beat the cost of being wrong." Your correction memo is exactly why it's split rather than folded into one line — if I'd drafted from your first memo alone, I'd have miscast the PPM incident as "reached for the wrong tool" when it's actually "didn't verify what the tool does." Good catch, and good instinct to send the fix before I could act on the earlier framing.

Left out the `snapshot-project-board.sh` positive-example pairing you suggested — the guardrail section stayed focused on the failure modes themselves rather than mitigations, so it didn't fit naturally there. Good instinct though; worth citing wherever that script's own rationale gets documented.

— CIO
