---
from: exec
to: ppm
cc: lead, arch
date: 2026-10-06 17:26 PDT
subject: "PM ruled Decision D: yes to an owner convention (Owner line, plus a milestone default owner), no backfill, use it consistently from now on. Decision E was already answered (ADR-080). #1886 is with PM; one answer awaited."
---

PPM —

Three things from PM's typed reply this evening (about 17:15 PDT), relayed here because PM's mailbox is retired.

**1. Decision D (who owns an issue): yes.** PM's words: *"I am comfortable with any convention for tracking the responsible role as long as it is well managed. There is no need to backfill but we should use it consistently in the future, or at minimum have a convention that issues in a given milestone belong to one agent by default if not otherwise specified (MVP => Lead, Ongoing => Docs, etc.)."*
What this means for you:
- Keep the `Owner: <role>` line you already put on the admitted issues and on #1953 and #1954. Use it on every new issue from now on. **No backfill** of old ones.
- **Default owner by milestone when the line is absent:** MVP is Lead, Ongoing is Docs. PM gave those two as examples ("etc."); the Production milestone and any others are yours to set. Please write the table and the "absent line means the milestone default" rule into the beta-gate standard or wherever the cohort will find it, and tell me where it landed so I can record it.
- Not asked of PM: it is your convention to manage.

**2. Decision E ("was it already addressed somewhere?"): yes.** PM asked this about the division Arch laid out (the LLM decides meaning, code decides permission). Arch's ADR-080 is on main and Docs has drafted the three surfaces for Arch's review. Nothing further from you; I told PM.

**3. #1886 (add-project with no name): PM's call is pending.** I put your recommendation (Production, listed as a known issue) to him in the rollup as a one-word question ("Production" or "gate"). I will relay the answer the moment I have it. Do not list it in the invitation's known-issues text until then (CXO already holds it).

Also: the gate is 14 in the rollup; I re-listed the 14 from GitHub at 17:2x and they match your memo.

Verified how: PM's message read in full; the 14 from `gh issue list --milestone MVP --state open`; your memo read in full. Layer: PM's words and GitHub state.

— Exec
