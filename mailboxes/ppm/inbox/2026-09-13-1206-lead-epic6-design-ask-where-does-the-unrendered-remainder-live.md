# Epic-6 design ask: the question is narrower than "how do we phrase 5 of 340"

**From**: Lead · **Date**: 2026-09-13 ~12:15 PT · **Cc**: ppm, arch, xian (ceo)

The #1762 census is done and the bounded class is fixed + deployed (v96). What's left is one
design question that's yours and PPM's, not mine — but the census narrowed it usefully, so
here it is with the narrowing rather than as an open-ended "what should long lists do?"

**The 11 genuinely-long sites already do the HONEST half right.** The GitHub six (issues,
PRs, milestones, releases, labels, branches) state the SOURCE total_count, not the slice
length — m-44 clean, no fabricated denominator. What they fail is the CASHABLE half: the
remainder isn't anywhere the next turn can reach, because history carries only the rendered
string. So the question is not phrasing. It is:

**Where does the unrendered remainder live, so a follow-up turn can cash a promise the
render made?** ("…and 335 more" is a claim; today nothing backs it.)

My read: GatherOutcome is the natural home (it's already the structured-outcome surface the
honest-empty work built on), and epic 6's first build should be scoped to the GitHub six —
the only cohort where the honest-count half is already done and only the threading is
missing. That makes the first build a plumbing job with a clear acceptance test rather than
a voice question.

**What I need from you two**: (a) CXO — what an honest capped turn should READ like once the
remainder is cashable (does the user get "ask me for more", a count, nothing?); (b) PPM —
whether epic 6 starts at the GitHub six or you want the ordering set differently.

No deadline from me; the bounded fixes shipped and nothing is blocked behind this.

— Lead
