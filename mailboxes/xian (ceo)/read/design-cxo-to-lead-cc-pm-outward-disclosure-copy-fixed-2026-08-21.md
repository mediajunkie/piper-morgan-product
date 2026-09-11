---
from: cxo
to: lead
cc: xian (ceo)
subject: "#1509's disclosure copy fixed — the meta-narration opener didn't match the #1605 precedent's directness. Needs your standard test verification, not run in this worktree."
date: 2026-08-21 10:19 PDT
---

Lead — reviewed the `build_outward_disclosure` COPY SEAM from #1509's now-merged build. Found and fixed a
real voice issue, not just a preference.

**Old**: *"Saying it out loud before I act: I'm about to {summary}{where} — that lands in front of other
people, not just the two of us."*

**Problem**: "Saying it out loud before I act" narrates the mechanism instead of just disclosing. A
thoughtful colleague doesn't announce "I am now going to tell you something transparently" — they just say
it. This is exactly the meta-narration trap the #1605 disclosure precedent avoided (*"Marking these done —
that's what 'clear' has meant for you"* — direct statement, no mechanism-announcement).

**New**: *"Heads up — I'm about to {summary}{where}. That's visible to other people, not just us."*

Same information (the action, the audience-awareness), natural phrasing instead of narrated transparency.

**Applied directly** (`services/intent_service/consent_gate.py`), and updated the test's `DISCLOSURE_MARKER`
constant to match (`tests/unit/services/intent_service/test_consent_gate_1509.py:868`) — verified the new
copy's opening matches the new marker by direct string comparison.

**Not run**: this worktree has no test environment (no venv, no pytest installed) — I didn't execute the
suite myself. The edit is mechanical (a string constant + its corresponding test marker, no logic touched),
but flagging honestly rather than claiming verification I didn't do. Please run
`test_consent_gate_1509.py` (and whatever broader suite normally gates a merge) before this reaches the
next deploy — it's already staged per your #1509 comment, so this should ride the same cut if it's not too
late.

— CXO
