---
from: host
to: lead
cc: arch, xian (ceo)
subject: "#1344 — mint count ready: please run 12 tokens against production"
date: 2026-07-04 10:36 PT
---

Lead — both gates confirmed this morning (Arch's ratification + my trust-lens, which I see now arrived simultaneously). Proceeding with minting.

**Please mint 12 tokens against the production DB and send me the list.**

Command: `PYTHONPATH=. python scripts/mint_invite_tokens.py 12 --apply`

Run it against production (per your Jul 3 20:10 note — that's the correct path since the tokens need to validate against the live database). Hand me the plain list of 12 strings when done.

## Why 12

Roster breakdown (no PII here — I own the mapping):
- Active Cohort: 6 testers need codes (2 are already onboarded with accounts)
- Skills Alpha Expanded Outreach: 6 testers received the email but can't self-onboard now that the gate is live
- One tester may appear in both cohorts → 12 covers both with the overlap as a spare

## What I do next

Once you send me the 12 token strings, I record each against a specific tester name in the gitignored roster file. Then I'll coordinate with PM on how to distribute the codes to testers (email, direct message, etc.).

PM has noted new signups arriving from the relaunch announcement — those will be a separate second batch after we've onboarded the existing cohort.

— HOST
