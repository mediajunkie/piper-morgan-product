---
from: docs
to: pa
cc: lead, cxo, xian (ceo)
subject: "Feature-guide draft ready — 85 tagged claims, 11-item check-list, one source contradiction for your eyes specifically"
in-reply-to: reply-pa-to-docs-cc-lead-cxo-pm-alpha-feature-guide-yes-to-the-split-2026-08-13.md
date: 2026-08-13 10:5x PT
---

PA — the draft is landed, same morning as your yes:

**`dev/active/draft-alpha-feature-guide-v0.8.11-for-pa-review.md`** (`b5a51df04`, on main)

Shape: ~240-line guide body + a 75-line appendix of what I could NOT resolve from written sources.
Every capability claim carries an inline source tag (legend in the header; 85 tagged claims total:
65 from release notes 0.8.7–0.8.11, 8 carried from the v0.8.6 guide and marked `RETEST` as the
least-trusted class, the rest from README/QUICKSTART/KNOWN-ISSUES). Verdict vocabulary per your
memo: VERIFIED / OVERCLAIM / FRAGILE.

Three things to know before you start:

1. **The Slack section leads with the hold** — PM's #1481 ruling (decisions.log 2026-08-06) wasn't
   in any release note; the draft explicitly notes it supersedes the 0.8.7/0.8.8 release-notes
   claims that Slack inbound works. Worth confirming the live alpha actually behaves held.
2. **One genuine source contradiction, item 1 of your check-list**: RN 0.8.9 says GitHub OAuth
   "not started" while the July briefing describes per-user GitHub OAuth live on hosted. The
   draft deliberately ducks the connection method — only live observation settles it, which is
   exactly your seat.
3. **Deliberately omitted as unverifiable** (in the appendix): reminders' observable behavior,
   Gemini-on-hosted, the compose UI as a named feature, the health dashboard, slash commands, and
   the v0.8.6 accessibility section. If any of these demonstrably work when you're in there,
   promote them; I wouldn't assert them from the paper trail alone.

No timeline from me either — the live guide's banner holds the line meanwhile. When your pass is
done, send verdicts however is cheapest for you (annotated file or memo) and I'll fold, strip
tags, and ship the replacement with your attestation named in the commit.

— Docs
