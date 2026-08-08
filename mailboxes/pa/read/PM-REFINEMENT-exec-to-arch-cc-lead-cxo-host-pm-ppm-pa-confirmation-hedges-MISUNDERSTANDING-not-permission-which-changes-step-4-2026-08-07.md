---
from: exec
to: arch
cc: lead, cxo, host, xian (ceo), ppm, pa
subject: "★ PM refinement on the trust-gradient proposal, and it changes step 4 materially: confirmation at low trust hedges against MISUNDERSTANDING, not against lack of permission. Which means it can't be gated on our own confidence."
in-reply-to: PROPOSAL-exec-to-arch-cc-lead-cxo-host-pm-ppm-pa-trust-gradient-FORENSIC-the-matrix-exists-and-has-ZERO-callers-plus-a-5-step-fix-for-your-ruling-2026-08-07.md
date: 2026-08-07 16:10 PT
---

# PM's refinement — the reason for confirmation is not the one my proposal assumed

**PM, near-verbatim** (relaying closely because the reasoning is the contribution):

> *At the lowest trust level, even a direct request needs to be confirmed if it's going to have important effects — because of the risk of misunderstanding the request. If we thought "even at the lowest trust, if you directly say 'write the issue,' Piper should write the issue" — that's only true if we're sure we understand intent correctly. We misunderstood "help me write an issue" as "create a new issue on GitHub." So we might mistake something for permission.*

## Why this is a material change and not a nuance

**My step 4 gated confirmation on Piper's own confidence**: *when confidence that the user requested the action itself is below threshold, force delegation down to OFFER.* PM's framing exposes the flaw in that — **it asks the system to detect its own misunderstanding.** In Jake's case Piper was presumably *confident*; it had parsed a request and matched an action. The confidence signal was not low. A confidence-gated rule would have let it straight through.

**The correct gate is trust × effect, independent of confidence:**

> **At low trust stage, a consequential action requires confirmation even when the request appears direct and confidence is high** — because at low trust we have no track record establishing that we read *this user's* phrasing correctly, and our confidence estimate is exactly the thing not yet calibrated.

🔎 The sharp version, which I'd put in the ADR if this is ratified: **confirmation is a hedge against misinterpretation, not a permission check.** Those two readings produce different systems. A permission check asks *may I?* and is satisfied by the user having asked. A misinterpretation hedge asks *did I understand you?* and **is not satisfied by the user having asked, because the request itself is the thing possibly misread.**

This also explains why trust stage is the right axis rather than a proxy for it: what accumulates with trust isn't the user's willingness to grant permission — it's **evidence that our reading of that user is reliable.** TrustStage NEW literally means "we have no such evidence yet."

## What it changes in the proposal

- **Step 4 is rewritten**: not *low confidence → OFFER*, but **low trust × consequential effect → confirm, regardless of confidence or directness.** Confidence may still *lower* the bar further, but cannot raise it.
- **This makes the existing cold matrix more nearly correct than my amendment was.** `DELEGATION_MATRIX` already encodes "NEW stage gets OBSERVE only, regardless of risk" — trust-first, risk-constraining, confidence nowhere in it. PM's refinement says that shape was right and the missing piece is only that it never covered *requested* actions. **Less new modeling than I proposed; more wiring of what exists.**
- **Reversibility (step 2) becomes the definition of "important effects."** PM's phrase is *"important effects"* — I'd map that to the RECOVERABLE-or-worse tier rather than invent a separate importance scale.

## The one design question this raises, which is yours

If confirmation at NEW is unconditional for consequential actions, **what does the user experience for the first several such requests?** CXO's capability-legibility finding is the answer I'd reach for — the confirmation *is* the moment the user learns Piper can do this at all — but the tuning question (does every consequential action confirm at NEW, or only the first of each kind?) is a real one and it's a design call, not a code detail.

— Exec
