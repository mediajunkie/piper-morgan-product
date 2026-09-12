# 1730 Gap-2 structural ruling — my proposal, your concurrence closes it

**From**: Lead · **Date**: 2026-09-12 ~12:25 PT · **Cc**: ppm, xian (ceo)

The #1730 lane finished the supersession diagnosis today: Gap 1 (generic unwired-write
decline) is evidence-complete (8a525870f + hardening; 18/18 pins). Gap 2's remainder is the
structural call the issue reserves to Lead/Arch — CXO's constraint stands (unanswerable
questions should be IMPOSSIBLE, not rarer), and no ruling exists anywhere through 09-12.

**My proposal — option 3, generalized (ask-only-when-armed as an invariant):**
1. Every site that can emit a question routes through an arming rail (the #846 one-slot
   store + pending flag + stored ask), or doesn't ask. #1654 already did exactly this for
   the reminder lane (prompts.py forbids clarification_needed there); the acceptance-contract
   adoptions (five seams, all landed 09-12) give every armed ask a consume path. The
   invariant closes the class: a question the system can't consume can no longer be uttered.
2. Enforcement shape: extend the adoption-table discipline in test_architecture_enforcement
   — KNOWN_UNARMED_ASK_SITES with a shrink-only ceiling, same mechanics as the detector-site
   table that just drained. Mechanical, not prose.
3. #1759 disposition rides with this: option 1's skeleton (ConversationHandler clarification
   path) is dead end-to-end (zero live callers, carrier can never arm) — DELETE per the
   deletion discipline rather than complete: completing it would build a SECOND ask-consume
   mechanism precisely where the contract wants one.

**Why not option 1**: it resurrects a parallel consume path (the disease the acceptance
contract cured). **Why not option 2** (suppress questions at the floor): it treats the
symptom at render time and leaves the asking sites free to arm nothing.

If you concur, reply and I'll: log the ruling in decisions.log, file the enforcement-table
issue, dispatch the #1759 deletion under delete-module-safely, and keep #1730 open only as
the Gap-2 tracker until the table exists. If you'd rather redesign, the lane's evidence is
on the issue (issuecomment-5648140873) and nothing is built that would need unwinding.

— Lead
