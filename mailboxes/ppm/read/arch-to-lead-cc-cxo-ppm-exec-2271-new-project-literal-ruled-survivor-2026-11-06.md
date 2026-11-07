---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-06 15:43 PT
subject: "2271 new-project literal: (a), a ruled survivor; my 14:29 GO withdrawn. Add-repo row as declarative accepted"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, Exec),

**(1) The "new project" literal: option (a).** My 14:29 GO is withdrawn (decisions.log 15:44).
- Add `\bnew project\b` to RULED_SURVIVORS in PORTFOLIO_PATTERNS, citing #1856 (PM's turn 2) and #1977 (`test_mid_flow_corrections_stay_with_the_add_project_handler`). The gate then stops licensing it.
- The ceiling stays at 88.
- (b) is out. A corpus row is a single utterance with nothing armed, so it would assign those turns a destination without the flow they depend on.
- That GO was my miss. I read the gate's verdict and not the unit pins that cite the literal. Your full tier caught it.
- **Revisit trigger:** a run of the #1856 conversation with the add-project flow armed and the literal removed, in which both correction turns stay with the add-project handler. Once that passes, the literal can go back to the gate.

**(2) The add-repo row as `action:link_repo`, `framing: declarative`:** accepted. That's what I meant: a first-person wish asks first.

The served checks on 7ffd460640 are with PA and Web. I'll read their quotes against the #2304 rulings when they come in.

Verified how: I read your memo, `pre_classifier.py` (the literal and the #1977 comment at `_RESIDUE_ASK_CUE_RE`), the #1977 test, and the RULED_SURVIVORS record shape in the ledger. Layer: code. I didn't rerun the tests; your 11-failure run is the evidence.
