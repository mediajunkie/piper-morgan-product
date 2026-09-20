---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
cc: exec
date: 2026-09-20
subject: "Walkthrough-ready — re-checked the open items live just now; 3 of them no longer need your verdict"
---

Exec said you're making time for both walkthroughs today, so I re-verified the open obs-pass items
against the live site rather than handing you a three-week-old artifact. **Short version: three
fewer things to decide.**

# No longer need a verdict — resolved since the 08-31 pass

| # | item | now |
|---|---|---|
| **#6** | Privacy policy dated "September 2025", visibly stale | **reads "May 2026"** — fixed |
| **#27** | No featured/hero post on the blog index | **resolved** — 544×544 hero at the top of `/blog`, the `FeaturedPost` work I shipped 08-29 |
| **#5** | Theme toggle — "not sure if it has a discoverable affordance" | **it does**: `aria-label="Switch to dark mode"`. Answerable without a design call, unless you want a *visual* affordance beyond the label |

# Confirmed still open — these are real and yours

| # | item | verified live |
|---|---|---|
| **#17** | `/what-weve-learned` has 60KB+ of content but no nav presence | nav is `/`, `/try/`, `/get-involved/`, `/about/` — **not there** |
| **#8** | Footer "Journey" → `/blog/`, while the nav "Journey" dropdown has 3 children | footer href confirmed `/blog/` |
| **#1** | Two pages both cover "how we work" | `/methodology` **200**, `/what-weve-learned` **200** — both live, so the IA question stands |

The remaining open items are copy/judgment calls that don't change under re-checking (#10 caps
headline, #12/#13/#14 copy, #15/#16 methodology depth, #19–#21, #22/#23, #25/#26, #28).

# Two honest notes about the prep itself

**The artifact's screenshots are from 08-31 and are three weeks stale** — the *findings* above are
re-verified live, but the images aren't. Say the word and I'll re-shoot all 15 pages before you sit
down; I didn't do it unprompted because the findings are what drive verdicts, not the images.

⚠️ **My first pass on #27 said "not resolved" and was wrong.** It searched for the words
"featured"/"latest", which aren't rendered as visible copy — so it couldn't distinguish "no featured
post" from "a featured post that doesn't say the word." I only caught it because I knew I'd shipped
that component myself. Re-checked structurally. Flagging because it's the same class of error as the
workDate one I just corrected, caught this time before it reached you.

**Verified how**: headless browser against the live site this fire — privacy page text, nav/footer
hrefs enumerated from the DOM, theme-toggle `aria-label` read directly, `/blog` first-block geometry
measured (544×544 hero at y=104 vs 355×224 grid cards at y=1128), and HTTP status on both
how-we-work pages. **Not verified**: the copy/judgment items, which have no mechanical check — they
need your read, which is the point of the session.

— Web
