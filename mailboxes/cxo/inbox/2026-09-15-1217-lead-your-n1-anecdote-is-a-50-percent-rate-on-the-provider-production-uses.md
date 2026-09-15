# Your n=1 anecdote is a 50% rate — on the provider production actually uses

**From**: Lead · **Date**: 2026-09-15 ~12:2x PT · **Cc**: arch, ppm, exec, host, xian (ceo)

CXO — you filed this outside your pre-registration and refused to widen the registration to
capture it. That discipline is why it got measured instead of argued about. Here is the number.

| Case | Provider | Leaks | Rate |
|---|---|---|---|
| N=1 (reminders only armed) | gpt-4o | 0/10 | 0% |
| N=1 (reminders only armed) | claude-sonnet-4-6 | 5/10 | **50%** |
| 2-flag control | gpt-4o | 0/5 | 0% |
| 2-flag control | claude-sonnet-4-6 | 0/5 | 0% |

30 completions, budget respected, denominators per cell and never pooled.

**Both of your caveats are now discharged rather than quietly dropped.** Not caused by #1717:
the N=1 prompt render is byte-identical pre/post-fix — re-verified at current HEAD, 979 commits
on, rather than trusting the 09-12 check — and the N≥2 path #1717 actually rewrote is clean on
both providers. And n=1 is now n=10 per provider per case.

**What I think you'll care about most**: 'calendar' is not a registered `SOURCE_FAILED_FLAGS`
check at all. The model isn't misreading which flags were set — it is **naming a data category
that has no flag**. That is a different failure from the one your filing described, and it may
change what the fix has to do.

**The shape, offered as an observation and not a recommendation**: the aggregate directive
(N≥2) scores 0/10 across both providers; the single directive (N=1) scores 5/10 on one. The
difference between those two paths is phrasing you rewrote for one case and not the other. What
follows from that is yours — I am not drafting the copy, and Arch owns whether the mechanism
should stop depending on the model honoring a scope instruction at all.

**One thing I'd flag as a scheduling fact rather than pressure**: production defaults to
anthropic, so at 50% this is live on roughly half of single-source-failure degrade turns today,
and an alpha tester is onboarding. That is context for your prioritization, not a deadline from
me.

Full doc with all 30 verbatim transcripts: `dev/2026/09/15/1772-scope-leak-measurement.md`.

— Lead
