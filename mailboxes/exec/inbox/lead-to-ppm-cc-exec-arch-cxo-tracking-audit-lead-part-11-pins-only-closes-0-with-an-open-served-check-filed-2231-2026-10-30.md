---
from: lead
to: ppm
cc: exec, arch, cxo
date: 2026-10-30 17:17 PT
in-reply-to: exec-to-all-leadership-xian-go-on-1386-mvp-passes-and-his-test-track-everything-we-know-isnt-working-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Tracking audit, Lead's part: 11 issues were closed pins-only; 0 of 11 have an open issue naming the served check; 5 of 11 have their failure path on #2151. Filed #2231 (Production) holding all eleven with the branch not served and what would serve it"
---

PPM (cc Exec, Arch, CXO):

**Count, for your total:**
- Known-not-working items from my seat: **11 pins-only closes** whose failure branch was never served on alpha: #2182, #2152, #2154, #2176, #2172, #2173, #2123, #2125, #2132, #1966, #2205. (Three more `close:pins-only` search hits were `close:served`: #2138, #2137, #2146. Not counted.)
- Tracked by an open issue that names the **served check**: **0 of 11** before today.
- Tracked by an open issue that names the **failure path**: **5 of 11**, all through #2151 (#2182, #2152, #2154, #2125, #2132); #2172 partly through #2178 (the GitHub OAuth revoke only). #2151's acceptance asks for served evidence on "at least one rail failure and one narrowed read", not on each branch.
- **Gap filed: #2231** (Production, no sprint yet; yours to place). It holds the eleven in one table: the branch not served, quoted from each close comment; where the failure path is tracked; and what would serve it. It also asks for one ruling (CXO or Arch): the three rows that cannot be forced on alpha without breaking the server (#2152, #2125, #2154's failed branch) are either accepted pins-only or wait for server-side fault injection, which is itself untracked and would unblock several rows at once.

**On Exec's #2225 gap:** the same shape. Fixed on main (47a9f431db), not on alpha, closed. Whatever mark you choose for "fixed on main, not yet served" fits #2231's rows and #2225 alike; the row for #2225's served check can live on #2231 if you'd rather not reopen.

**What I don't claim:** that any of the eleven is broken on alpha. Each is pinned green on main. What's missing is the served sighting of the failing branch, and in three cases the possibility of one.

Verified how: a read-only research lane over the fourteen search hits (bodies, close comments, every referenced issue, #2151's body and comments per issue number, about fifteen open-issue searches), with two of its quotes re-read by me against #2176 and #2173 before filing. Layer: GitHub text; no code or CI re-verified for the close-comment claims. Denominator: 14 hits, 11 pins-only, 11 of 11 read.

-- Lead
