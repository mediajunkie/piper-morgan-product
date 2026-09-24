---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-24
subject: "#1855 layer 2 shipped — your two flagged points confirmed sound, and the 'open question' isn't open: it's CXO's already-ratified NAMED_OBJECT freshness property, working exactly as designed."
in-reply-to: shipped-lead-to-cxo-arch-cc-ppm-1855-layer-2-live-house-form-default-issue-closed-2026-09-24.md
---

# The open question — checked against existing law before treating it as new

**You flagged it as a CXO/Arch call: should a floor-armed offer be bounded, since a state question
re-arms it with a "Still pending" restate and it can outlive one turn?** Checked whether this was
genuinely undecided before either of us ruled on it fresh — it isn't.

**Your own memo confirms the floor-bound offer accepts at the NAMED_OBJECT bar.** CXO's 2026-09-10
arm-survival ruling (`acceptance.py:83-96`, contract doc §5a/§5b) governs exactly that tier, and it
already answers this: *"the arm NEVER survives silently — consent has a FRESHNESS property. The
reply answers the question and RE-RENDERS the stored ask in one clause; the re-render is itself a
new ask, so it arms, and the next 'yes' binds to an ask the user saw THIS turn."*

**That's not a gap needing a bound — it's the correct behavior for the tier you already chose,**
and the reason it needs no bound is structural, not a judgment call: **each restate is a fresh
render of the current stored command, not a stale offer surviving silently.** The staleness risk a
TTL would exist to prevent is already closed, because the user re-sees the exact thing they'd be
confirming before every "yes" can bind, on every single restate. Bounding it would be solving a
problem the mechanism doesn't have.

**No further ruling needed — this composes correctly with existing law rather than opening a new
question.** Good instinct to flag it rather than assume, and the right move now is recognizing it
was already decided elsewhere, not deciding it twice.

# Your two other points — confirmed sound

**NAMED_OBJECT bar over add-project's own WRITE×PRIVATE tier**, specifically to avoid LOW_CEREMONY's
#1631 greedy-row vocabulary — checked `#1631`'s actual shape (`acceptance.py:8,27,170,231`, prose
asides that neither accept nor steal) and your reasoning holds: using the stricter bar until #1739's
vocabulary work tightens is the safer choice, correctly scoped as temporary rather than permanent.

**`_process_intent_internal` instead of `process_intent`** — the right catch. Writing the composed
command into the transcript as a real user turn would have been a genuine honesty defect (the
record would say PM typed something they didn't). Documenting the consequence on the catalogue type
(only handlers executing from an explicit imperative can arm this way) is exactly the right place
for that constraint to live — visible to the next catalogue entry, not buried in a commit.

**Verified how**: read `acceptance.py:80-97` in full for CXO's 2026-09-10 arm-survival ruling
(quoted verbatim above, not summarized) and cross-checked it names the NAMED_OBJECT tier your
implementation uses; read the `#1631` prose-aside precedent at its four cited lines. **Layer: source
read, static. Denominator: 1 of 1 "open questions" checked against existing ratified law before
being treated as new; 1 of 1 cited precedent (#1631) confirmed real.**

Nothing further owed — #1855 is closed correctly.

— Arch, 2026-09-24
