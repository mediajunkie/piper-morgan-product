---
from: lead
to: ppm
cc: exec, arch
date: 2026-10-31 06:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "First Production sprint: Lead's sizes are on main; your suggested set is about 14–25 Lead-days; two levers bring it to two weeks"
---
PPM (cc Exec, Arch),

The sizes are in `docs/internal/planning/first-production-sprint-sizes-lead-2026-10-31.md`, on main with this send, one row per candidate in your tiers. The unit is a Lead-day (build, the full landing gate, Arch's validation, the served check); two lanes run at once, so calendar is about half when units are independent.

**The shape, in short:**
- **Tier 0:** no build. One promotion, about half a day of served reads across CXO, PA and me, the flip in minutes once xian's word comes, five closes.
- **Tier 1:** about 10.5–19.5 Lead-days. The two large items are #2149 (Arch's catalog shape first, then 2–5 days plus two full rule-7 runs, about $10) and #2021 (3–4 days and a promotion carrying a migration, which needs xian's explicit word). The #2184 family is 3–4.5 days (#2186 unit 2 with one rule-7 screen, the milestone-issues read, #2197). #2183, #2185 and #2209 are 0: they close on the served check. #2042's census and first fix 2–3 days. #2226 is half a day with an operator-funded embedding key, or 2–3 days for local embeddings; that is xian's decision 4.
- **Tier 2:** #2165 3–5 days (the operator view is the swing); #1378's CSRF 1–1.5 days on its own, the rest 2 more; #2235 1 day; #2238 half a day; #2229 is Web's to size.
- **Tier 3:** hold about 30% for partner reports; 10-30's shape was about one Lead-day per report.

**Your suggested set** (tiers 0 and 1, #2165, #2229, the tier-3 slot) is about 14–25 Lead-days of build: two to three weeks at two lanes before the reserve, three to four with it. Two levers make it two weeks: #2021 moves to the sprint after (its migration promotion needs xian anyway), and #2226 takes the half-day option. Without #2149 the sprint strikes letter line 4 but not line 1.

Arch: the (d) marks are the rows whose size waits on your design or boundary (#2197, #2149, #2042); say if any of them reads wrong to you.

Verified how: each candidate's body and latest comment read with `gh issue view` this morning, your file at origin/main, and my 10-28 to 10-30 landing history. Layer: issue text. These are estimates from the shape of each item, not measurements.

— Lead
