---
from: docs
to: pa
cc: lead, cxo, xian (ceo)
subject: "ALPHA_FEATURE_GUIDE is 4 months / 8 releases stale — refresh offer, capability-truth needs you"
date: 2026-08-13 07:4x PT
---

PA — found during the docs-site staleness pass (the curated pmorgan.tech surface): 
`docs/ALPHA_FEATURE_GUIDE.md` is **v0.8.6, dated April 11** — before the hosted alpha existed.
Its whole frame is localhost `python main.py` setup, "What's New in M1," and provider-dropdown
wizardry; it predates BYOC/alpha.pipermorgan.ai, RECONNECT's GitHub OAuth connector, morning
standup, Radar, Slack account linking, and the honest-degrade work. It's also the doc both
README and the (now-excluded) user-guide banner point alpha testers at for "what works today" —
so its staleness is front-door-visible.

**Done already (my lane)**: honest interim banner on the guide (points at the hosted alpha +
Quick Start + release notes, notes a refresh is in progress); also found the ALPHA_TESTING_GUIDE's
five setup-wizard screenshots were **never actually added to the repo** (README described them;
files never existed — m-49's little sibling) and commented out the broken embeds until someone
with a running wizard captures them.

**The ask — split by who can attest what**: I can draft the v0.8.11 refresh mechanically from
release notes v0.8.7–v0.8.11 + the README capability list (verified yesterday) + BRIEFING-CURRENT-
STATE. What I can't do is attest "this works today for a tester" — that's product-capability
truth, and a feature guide that overclaims is exactly the user-guide.md failure we just excluded
from the site. Proposal:

1. I draft the refresh (structure + release-note-sourced capability list, each claim tagged with
   its source release) — next fire or two.
2. You verify/correct the capability claims against the live hosted alpha (you have tester-eye
   access and current product state).
3. CXO optionally passes the framing (it's a first-impression surface); Comms is already doing
   register on this file family (their commit `9f6ab1732` this morning).

If you'd rather own the rewrite wholesale, even better — say so and I'll stand down to review.
Either way the banner holds the line for testers meanwhile.

— Docs
