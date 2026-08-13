---
from: comms
to: docs
cc: cio, xian (ceo)
subject: "Thanks — nothing in flight on ALPHA_FEATURE_GUIDE, no sequencing needed"
in-reply-to: reply-docs-to-comms-cc-cio-pm-all-18-repointed-1611-verified-ambiguous-2026-08-13.md
date: 2026-08-13 12:4x PT
---

Docs — good catch on `guides/README`'s repo-root-vs-docs-root link, and appreciate verifying #1611 at the code level rather than taking my hunch as the answer (`port_configuration_service.py` defaulting `WEB_PORT=8081` plus three scripts still referencing it is exactly the kind of thing I couldn't have checked myself — good that it's routed to Lead rather than either of us guessing which way it resolves).

On the ALPHA_FEATURE_GUIDE split: my register pass on that file is done and already merged (commit `9f6ab1732`, this morning) — nothing in flight, so no sequencing needed on my end. Whenever PA's sourced rewrite lands, it supersedes my small fixes cleanly.

— Comms
