---
from: cxo
to: lead
cc: xian (ceo)
subject: "Setup UX copy review — #1318 unblocked; one substantive fix + one tracked debt"
date: 2026-06-25
---

Hey Lead — setup UX copy review is done now that #1318 is closed.

Overall: the flow is structurally sound. One substantive suggestion on the intro panel; one lower-priority copy debt tracked for post-alpha.

## Substantive: Piper intro panel — middle paragraph

**Current**:
> "I can help with tracking tasks, managing GitHub issues, prepping for standups, and keeping your calendar in view."

**Proposed**:
> "I've got a view across your GitHub issues, your calendar, and what's coming up in your standups — I'll help you stay on top of it all."

**Why**: The current copy is a capability list. Through the Colleague Test lens, a new colleague doesn't recite their qualifications — they show they understand your world. The proposed version shifts from "here are my features" to "I see what you're working with." Same information, collegial register. This is the alpha tester's first impression of Piper's voice.

The change is `templates/setup.html` around line 348, in the `.piper-description` paragraph.

This is a recommendation before the alpha tester wave goes out — not a blocker, but the intro panel is our highest-visibility first-impression moment.

## Tracked: Step 1 error state — developer command exposed

**Current** (setup.js line ~129):
> "Required services are offline. Run: docker compose up -d"

For alpha testers on the Droplet, this will never appear (#1318 fixed, services healthy). For local installers, it's appropriate but the bare docker command could confuse a PM.

**Proposed** (low-priority copy debt):
> "Some background services aren't running. If you're setting up locally, try: `docker compose up -d`"

Not urgent for the alpha wave — filing it as copy debt so it doesn't get lost.

## Everything else: passes

- "Let me help you get set up. I'll need to check a few things and connect to your tools." → natural ✓
- "Connect Your AI" / provider selection → fine for technical alpha audience ✓
- "Tell Piper about the projects you're working on." → collegial ✓
- "You're all set. Piper is ready to help." → solid ✓

The intro panel copy change is the one thing worth doing before invitations go out, if bandwidth allows.

— CXO
