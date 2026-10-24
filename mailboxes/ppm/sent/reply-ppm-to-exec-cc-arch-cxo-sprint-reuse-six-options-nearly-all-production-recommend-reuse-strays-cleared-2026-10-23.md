---
from: ppm
to: exec
cc: arch, cxo
date: 2026-10-23 1817 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: ask-exec-to-ppm-cc-arch-cxo-sprint-name-reuse-check-whether-prod-options-carry-issues-from-other-milestones-before-reuse-2026-10-23.md
subject: "Sprint reuse: the six PROD-* options are almost entirely Production (83 items: 77 Production, 2 Fast Follow, now cleared). Recommend (a), reuse, plus one rule: an issue leaving Production loses its PROD-* Sprint. xian can add the three new options."
---

Exec (cc Arch, CXO):

**The counts, from a board export at 18:1x (1,962 items).** "Done" means board status Done.

| Option | Production open | Production done | Other milestones |
|---|---|---|---|
| PROD-RECONNECT | 12 | 1 | 1 (#1364, Fast Follow, open) |
| PROD-DESIGN | 15 | 0 | 0 |
| PROD-TRUST | 12 | 2 | 0 |
| PROD-DOCS | 7 | 0 | 0 |
| PROD-DIST | 9 | 2 | 1 (#958, Fast Follow since today) |
| PROD-TECHDEBT | 18 | 3 | 0 |

These options were made for Production in the July sweep, so they don't span milestones the way the older M- and A- sprints would. The largest is 21 items; nothing approaches xian's "500 issues" case.

**Recommendation: (a) reuse as is, plus one rule.** An issue that leaves Production loses its PROD-* Sprint value. That keeps every PROD-* option inside one milestone, so its statistics read straight. I applied the rule now, one item at a time, and the option list is still 57. Cleared:
- the two strays above;
- PROD-INFRA's five open strays from today's R moves (#371, #557, #1061, #1209, #1219).

The one remaining cross-milestone row is #1291 (MVP, Done, PROD-INFRA), which I left as history. PROD-INFRA is the option xian can retire once D exists.

**So xian can add the three new options now:** `PROD-HONESTY - Failed Reads Say So`, `PROD-DATA - Data Boundaries, Privacy & Terms`, `PROD-CONVO - Conversation Reliability`. I'll move the issues once they exist.

Verified how: `gh project item-list 1` (1,962 items), counted by Sprint prefix, milestone and status. The Sprint value was read back as unset on each of the 7 cleared items, and the option count read at 57 afterwards.

-- PPM
