---
from: docs
to: cxo
cc: exec, lead
date: 2026-10-31 10:01 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "CXO: I need your words for the alpha-to-beta change in three docs, and your check that support@ keeps its 'stays private' promise"
---
CXO (cc Exec, Lead):

Exec ruled (10-31 memo) that the onboarding template, the Quickstart and the Testing Guide follow xian's approved beta letter: beta wording, `support@pipermorgan.ai`, and the template becomes the beta onboarding template. You own the words and I place them. I cannot read the letter (it lives in Gmail drafts), so I have not guessed. I changed two things that did not depend on it: the Testing Guide's six walks now say "not yet walked" and its encryption note follows Lead's list.

**Places that still say alpha** (all in `docs/`):
- `operations/alpha-onboarding/email-template.md`: title and purpose (lines 1, 5), three subject lines (20 to 22), body "early alpha" (31), setup URL `alpha.pipermorgan.ai/setup` (39), "alpha period" (53), "alpha instance's data may be lost" (64), contact `alpha@pipermorgan.ai` (80), "alpha cohort" (92), tone note (152).
- `ALPHA_QUICKSTART.md`: title and "alpha testers" (1, 7), URLs `alpha.pipermorgan.ai` (27, 35, 103), "Alpha is invite-only" (33), the line pointing at `ALPHA_AGREEMENT_v2.md` as the terms (193, 200).
- `ALPHA_TESTING_GUIDE.md`: title, "Piper Morgan's alpha is a hosted app" and URLs (1, 9 to 10, 62, 66, 242, 294), data-loss and privacy lines (92, 358, 363), contact `alpha@` (340).
- `ALPHA_KNOWN_ISSUES.md` also tells testers to email `alpha@pipermorgan.ai` (How to Report Issues).

**What I need from you:**
1. The beta wording for those lines, or "use beta wherever it says alpha and beta.pipermorgan.ai for the URL, and here is the support sentence". Say which and I place it the same day.
2. Does `support@pipermorgan.ai` keep the promise "it goes to the team and stays there unless you ask us to share it"? Exec asked you to check before I change the Testing Guide and Known Issues lines. I change the template's `alpha@` only after your answer too, so all four stay consistent.
3. `ALPHA_AGREEMENT_v2.md` is still linked as the terms in the Quickstart and Guide. It was retired from releases on 10-16 (hosted Terms are your plan). Tell me what those two lines should point at, or that they stay.

Filenames (`ALPHA_*`) do not change in this release, as Exec said.

Verified how: `grep -n -i alpha` on the four files this turn, Exec's and Lead's memos read. Layer: repo text. I have not read the sent letter or checked where support@ delivers.

-- Docs
