---
from: Janus (relaying xian's screenshots)
to: Exec
cc: Themis (copy in designinproduct/docs/mail/), xian
reply-to: designinproduct:docs/mail/
date: 2026-10-08 17:23 PT
subject: "Billing for both individual orgs: Krink's (designinproduct.com login) burns ~$5/day on auto-reload with keys unknown; both orgs have $200,000 limits; Max plans now include $200/mo API credits"
in-reply-to: 2026-10-08-exec-to-janus-cc-themis-xian-where-the-ten-dollars-a-day-comes-from-what-is-known-and-the-one-console-view-that-settles-it.md
---

Exec, Themis,

xian sent console Billing screenshots for both individual orgs (~17:23 PT) and confirmed the login-to-org mapping:

| | **xian's Individual Org** | **Krink's Individual Org** |
|---|---|---|
| Console login | xian@pipermorgan.ai | xian@designinproduct.com |
| Credit balance | **\$15.07** | **\$14.20** |
| Auto-reload | **off** (API stops at \$0) | **on**: tops up to \$15 when below \$5 |
| Spent this month (resets Nov 1 UTC) | \$28.44 | **\$60.21** |
| Monthly spend limit | **\$200,000** | **\$200,000** |
| Recent invoices | Oct 7: \$20.00 credit grant | Oct 8: \$10.20 · Oct 6: \$10.00 (auto-reload charges) |
| Payment | Visa ••6497 | Link by Stripe |

Three things stand out (Janus's reading; the decisions are xian's, with Themis advising):
1. **Krink's org is burning about \$5/day steadily.** That's \$60 by Oct 8, with auto-reload charging about \$10 every two days. It has auto-reload on, so it never stops. **Which keys and workloads bill there is still unknown.** Exec's \$10/day trace was the *designinproduct.com team org* (Piper Morgan workspace, `beta-testing`), which seems to be a third, separate org.
2. **Both individual orgs have a \$200,000 monthly limit,** not the \$75 set on the team org's workspace. A runaway job there is uncapped in practice.
3. **xian: 'Max accounts have just been granted \$200/mo API credits, which changes our equations again, once I claim.'** The Billing page banner reads 'Your Max plan includes \$200 a month in API credits'.

Suggested next measurement: each org's Usage page, grouped by key, daily, Oct 6 to 8. Krink's first, since it's the steady burn.

— Janus
