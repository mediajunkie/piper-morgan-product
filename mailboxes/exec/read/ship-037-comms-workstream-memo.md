# Ship #037 Workstream Memo: External Relations & Community
**From**: Communications Director
**Coverage**: Friday March 27 – Thursday April 3, 2026
**For**: Chief of Staff (Ship #037 synthesis), PM

---

## Published

Six pieces across two weeks, maintaining the weekend cadence plus midweek publications.

**Blog posts (Medium + LinkedIn)**:
- *Discovery Is the Bottleneck* — Sat Mar 29 (first blog-canonical publish: pipermorgan.ai → Medium → LinkedIn)
- *Wiring vs. Wizardry* — Sun Mar 29 (second blog-canonical publish)
- *Are We Doing It Backwards?* — Tue Mar 31 (third blog-canonical publish; Act 2 of six-part series)
- *The Floor That Wasn't* — Wed Apr 2 (fourth blog-canonical publish; Act 3 of six-part series)
- *Silent Failures* — Sat Apr 5 (insight post, outside this window but published from this week's planning work)

**Weekly Ship**:
- Ship #036 "Approaching the Gate" — Tue Apr 1 (LinkedIn + pipermorgan.ai Shipping News section)

**Note**: Silent Failures (Apr 5) and The Mismatch Category (planned Apr 6) were sequenced during the Apr 4 Comms session, which falls outside this coverage window.

## Blog-First Publishing Milestone

The biggest infrastructure development this week was the shift to **blog-first canonical publishing**. All four blog posts published during this window debuted on pipermorgan.ai before syndication to Medium and LinkedIn. This is a meaningful change — the project's own site is now the canonical home for new content, with Medium demoted from primary to syndication target.

The transition surfaced and resolved several infrastructure bugs: CSV parser field count mismatch (11→13 columns), date display off-by-one (UTC midnight → Pacific timezone shift), non-hex hashId breaking content rendering, and Medium link display logic. Each publish surfaced the next issue; Docs iterated the publish-to-blog skill from v0.3 to v0.5 across the window.

## Content Production

No new drafts this week — the pipeline from the Mar 26 production session (15 drafts) remained the active inventory. Focus shifted to sequencing and publishing from the existing queue.

**Six-act building narrative series** status:
1. Ten Roles, One Day (Act 1) — ✅ Published Mar 26
2. Are We Doing It Backwards? (Act 2) — ✅ Published Mar 31
3. The Floor That Wasn't (Act 3) — ✅ Published Apr 2
4. Fixing the Foundation (Act 4) — Scheduled Apr 8
5. Nine Voices (Act 5) — Scheduled Apr 10
6. The Closing Sprint (Act 6) — Scheduled Apr 15

**Weekend insight publications planned** (from Apr 4 Comms session):
- Apr 5-6: Silent Failures + The Mismatch Category ("things hiding in plain sight")
- Apr 11-12: The No-Anchoring Roundtable + Archaeological Debugging ("how you figure things out")
- Apr 18-19: Thirteen Mailboxes + Sibling Intelligence ("working together at scale")

## Pipeline State

The pipeline challenge remains sequencing, not generation. Inventory as of Apr 4:

- **Building narratives**: 3 acts remaining in six-part series (Acts 4-6, all scheduled)
- **Insight pieces**: 20 unscheduled (7 March, 3 February, 10 older Nov-Jan backlog)
- **Ship**: #037 covers this window; publishes next Wednesday

The three-weekend thematic pairing plan gives the insight backlog a sequencing framework it previously lacked. Each weekend pairs pieces that approach a similar theme from different periods of the project.

## Infrastructure

**Shipping News section**: Docs built a dedicated `/shipping-news` route on pipermorgan.ai with distinct visual identity (orange accent, ship badge). Ship #036 is the inaugural entry. Weekly Ships now have their own home alongside the blog.

**Blog-first pipeline**: Publish-to-blog skill at v0.5. Draft metadata convention established (comment blocks in markdown). The workflow is maturing — each publish is faster than the last.

**Editorial calendar**: CSV in project knowledge, updated through Apr 2. Known staleness issues remain but are narrowing — PM and Docs updated 15+ entries during this window.

## Conference Talk

IAC presentation ("Ethics as Information Architecture," Apr 17, Philadelphia) — now 9 days away. Draft deck (16 slides) and speaker notes exist from Mar 15. PM flagged as next collaborative priority on Mar 30. Not yet addressed in new project sessions. This is approaching urgency.

## M1 Gate UAT

Not a Comms deliverable, but relevant context for narrative purposes: the M1 gate UAT executed Apr 3 and **did not pass** (0/7 Gate 1, 0/1 Gate 2 tested). Floor LLM not reaching users was the blocking issue. This is significant story material — the gate design caught exactly what it was designed to catch, and Pattern-045 ("green tests, red user") was confirmed in production. Three fixes identified; re-test expected soon.

---

*Submitted: April 8, 2026*
