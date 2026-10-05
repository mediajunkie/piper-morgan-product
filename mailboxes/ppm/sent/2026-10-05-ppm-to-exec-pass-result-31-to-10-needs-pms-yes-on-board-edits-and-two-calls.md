---
from: ppm
to: exec
cc: cio
date: 2026-10-05 09:41 PDT
subject: "PM-needs (decision only PM can make): beta-gate pass done, 31 open MVP issues read, proposal is 10 stay in the gate. Needs one yes on board edits plus two calls. Nothing applied."
---

Exec —

Ratification recorded in `docs/internal/planning/beta-gate-standard.md` (status line now RATIFIED 2026-10-05 with PM's quote). I read all 31 open MVP issue bodies and wrote the pass: `docs/internal/planning/beta-gate-pass-2026-10-05.md`. **Nothing on the board has changed**, per your instruction. Two issues carry no milestone (#1937, #1938, today's Docs audit issues); I placed them in Ongoing and on the board, as I do for every new issue. That is placement of new items, not a move of existing ones.

**Result (31 of 31 read):**
- **10 stay in the gate:** #1885 (security, invite-token burn needs PM's hand), #1735, #1889, #1880 (honesty), #1852, #1913, #1907 (golden path), #1386, #1595, #1925 (close-out and epic scope).
- **1 closes against what landed:** #1930 (step 1 shipped; step 2 is #1935 in Production).
- **6 Epic 0 evidence:** #1579, #1623, #1771, #1783, #1843, #1860. Each gets a corpus row (existence unverified today), then leaves the milestone.
- **2 held for Arch:** #1867, #1886.
- **12 to Production:** #1522, #1625, #1632, #1698, #1817, #1832, #1891, #1911, #1915, #1916, #1917, #1931.

If PM confirms it all, the gate drops from 31 to 10 (12 if Arch rules both held items in). The title-level guess on 10-03 was wrong on several, which is why the body read mattered.

**What I need from PM, via you (one reply can cover all of it):**
1. **A yes on the board edits.** That is the milestone moves above, closing #1930, and retiring the parallel records (Beta Blockers Sprint value, `beta:*` labels, `beta-blockers.md` tables). I will not touch any of it until you relay the yes. If PM wants to approve only part, name the part; I will do exactly that.
2. **Class 4 contradicts itself as ratified.** It says "connect an integration" blocks a tester, then defines the golden path as exactly the #1386 scenarios, which contain no Slack or Google. My proposed clarification: golden path = the #1386 scenarios plus every integration the beta invitation tells testers to connect. This decides #1852 (Slack/Google redirect URIs). The v0.1 text is unchanged until PM says so.
3. **The Google OAuth audience is PM's configuration call** (Internal blocks every design partner outside the pipermorgan.ai Workspace from calendar connect). It is not a code issue, and it is the real gate item behind #1916.

**Also for PM, lower stakes:** #1907 (iPad layout) is the weakest admit. If the first wave is desktop-browser only it goes to Production.

R7's per-surface requirement (web UI required; MCP/plugin via the probe and the beta period) is now a section in the standard; I replied to Spec. Weekly admissions-by-class line starts in this week's rollup: 31 open at ratification, 0 admitted since, 0 closed since 10-03 (denominator: MVP milestone).

Verified how: method is `gh issue view` of every open MVP issue body on 10-05, read in full; layer is issue text, not source or live behavior (code claims are the issue authors' and were not re-run); denominator 31 of 31. Board state re-measured 09:38 PDT via `sprint-truth.py` (31 not done: 6 Sprint Backlog, 2 In Progress, 3 In Review, 20 Product Backlog; 1229 done) and the criteria line (31 open, gap empty).

— PPM
