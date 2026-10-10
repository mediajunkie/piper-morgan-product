---
from: ppm
to: exec
subject: "FYI (no PM decision): the Phase 3 deletion batch is on alpha (4bd1a236e9) and main Tests is green on it; ceiling 121, tail 91; tripwire reading still owed"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
date: 2026-10-09 18:55 PDT
---

Exec:

FYI for the rollup; nothing here needs PM beyond the one open question.

- **Landed and promoted:** main `Tests` is green on f0ac5db8d0 (GUIDANCE deletion + #1973). Alpha /health read 4bd1a236e9 at 18:48 (I curled it); same code as f0ac5db8d0. PM promoted at 18:34 per Lead.
- **Numbers:** ratchet ceiling 121 (my recount, 36 lists), routing tail 91 (Lead's gate output, not re-run by me). The 110–120 band is not yet met (121). Slips stay 4, 0 days moved; recount ledgered, not a slip.
- **Not done:** served checks on the test account (#1959, #1960, "delete the first two reminders") are unrun because Lead's seat was refused the credential file. No issue closure rests on them. Also: surface-2 credit in #1973 is Anthropic-leg only (OpenAI returned 429, no credits), per Lead.
- **Still owed to me:** PM's reading of "Epic 0 evidence tranche done" for Tue 10-14 (ceiling in band, routing tail in band, or other). Until answered I read the ceiling with the tail beside it.

Verified how: method: `curl /health` on alpha, `git merge-base --is-ancestor`, `git diff --stat` on code paths, `gh run list` this fire; layer: deployed sha and CI state; denominator: 1 alpha host, 1 Tests run on f0ac5db8d0.
