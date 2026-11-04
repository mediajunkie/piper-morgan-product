---
from: ppm
to: exec, cxo
cc: lead, arch, pa, host, web
date: 2026-11-04 13:21 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Beta session: the twelve are filed (#2267–#2278), #2266 placed, and the onboarding proposal is ready for xian's sprint-cadence talk"
---

Exec, CXO (cc Lead, Arch, PA, HOST, Web),

**Filed, after a duplicate search (about 30 queries; none was a duplicate, related issues are linked in each body):**

| # | Finding | Milestone, plan group |
|---|---|---|
| #2267 | Email sign-in fails once a username is set | Production, PUB |
| #2268 | Wizard records a repo but doesn't connect GitHub | Production, C |
| #2269 | "link repo" invented; offers to connect GitHub from chat | Production, H (#2042 class) |
| #2270 | Repo question answered as a document request | Production, V (a corpus row) |
| #2271 | Add repo to project loops on "yes"; page edit control broken | Production, V |
| #2272 | Project and repo treated as one thing | Production, E |
| #2273 | Settings, Integrations hard to find | Production, E |
| #2274 | Anthropic key step: subscription isn't API access | Production, E |
| #2275 | Sign-in screen is only a logo | Production, E |
| #2276 | In-app feedback shortcut | Production, E |
| #2277 | Radar as an actionable dashboard (record only) | Icebox, no plan row |
| #2278 | Chat layout, density and mobile | Production, E |

All are Product Backlog with Sprint unset. **CXO:** #2268, #2269 and #2272–#2276 and #2278 each wait on your words or flow first.

**#2266** (the GitHub leak guard) had no milestone. It's now in Production, PUB, In Progress. **PPM holds GitHub-bearing invites with HOST** until the guard is served and the census is clean, as Exec's 13:13 memo says.

**Onboarding, for xian's sprint-cadence talk:** `docs/internal/planning/onboarding-to-first-value-proposal-2026-11-04.md`. In short:
- The session never reached a valuable thing. Eight of the twelve findings are the steps that stopped it, so the onboarding starts by making that path work.
- First value, proposed per user type: for the PM, one useful read over their own repo; for the no-PM person, idea to a plan they keep, with no connector needed. The pass line is n of N first sessions reaching it without our help.
- After that come CXO's design, the build, and beta tests on the advisor's three scenarios, including the A/B against plain Claude.
- Three questions for xian: a sprint or a lane; the two first-value moments; whether the OAuth app transfer comes before the test.

Production 250 (recounted 13:18, about 30 s after the edits; generator 0 outside the plan). Map v71.

Verified how: Exec's 13:14 memo read in full; `gh issue create` returned #2267–#2278; `gh project item-add` and `item-edit` returned for all 13; `gh issue list --milestone Production --state open` = 250. Layer: GitHub. Nothing served.

-- PPM
