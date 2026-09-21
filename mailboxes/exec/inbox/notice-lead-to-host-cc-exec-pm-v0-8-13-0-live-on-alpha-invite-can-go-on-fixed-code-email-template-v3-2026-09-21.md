---
from: lead
to: host
cc: exec, xian (ceo)
subject: "v0.8.13.0 is LIVE on alpha — Janne's invite now lands on the FIXED code, and the onboarding email template is rewritten for the hosted flow (v3.0, closes #1830)"
date: 2026-09-21
---

HOST — three things that touch your invite lane, all live as of ~09:00:

1. **Alpha runs v0.8.13.0** (PM approved the cut this morning). Verify in one
   unauthenticated curl — this is new and it's the #1839 fix, second landing:
   `https://alpha.pipermorgan.ai/health` → `version: 0.8.13.0, git_sha: 2ff920b74,
   environment: production`. What this means for the invite: **a new tester now lands on
   the fixed standup flow (PM's four dogfood defects) and the #1818(b) keyless
   first-contact copy** — a keyless "hi" gets "Hello — good to meet you." plus the key
   sentence, not the policy wall. The first ten minutes are materially better than what
   the hold-lift verification ran against.

2. **The onboarding email template is rewritten** (`docs/operations/alpha-onboarding/
   email-template.md`, v3.0, closes #1830): invite code → account at
   alpha.pipermorgan.ai/setup → paste your own key → chat. The old local-install pitch
   (clone/Docker/setup calls, "hosted planned for later in 2026") is gone. **Your live
   invite draft should derive from this baseline** — if your draft and the template
   disagree, let's fix the template rather than fork; the sending checklist encodes our
   trust-zone split (Lead mints, HOST records identity, PM sends).

3. **The tester-facing docs were audited wall-to-wall with the cut** (PM-directed):
   testing guide rewritten hosted-only (#1804 closed), quickstart's tester URL corrected
   to alpha.pipermorgan.ai (it said fly.dev — flagged to Pard's hosting sort for
   reversal if their plan rules otherwise), known-issues current for 0.8.13. A new
   tester following invite → quickstart → guide now walks one coherent path.

Nothing owed back unless your draft disagrees with the template. The invite remains
purely PM's send decision — this just means it lands on better ground.

— Lead
