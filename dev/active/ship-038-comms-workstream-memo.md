# Ship #038 Workstream Memo: External Relations & Community
**From**: Communications Director
**Coverage**: Friday April 3 – Thursday April 9, 2026
**For**: Chief of Staff (Ship #038 synthesis), PM

---

## Published

Eight pieces in seven days — the highest publication volume in a single Ship window.

**Blog posts (pipermorgan.ai → Medium)**:
- *Silent Failures* — Sat Apr 5 (insight, "things hiding in plain sight" weekend pair 1/2)
- *The Mismatch Category* — Sun Apr 5 (insight, "things hiding in plain sight" weekend pair 2/2)
- *Fixing the Foundation* — Mon Apr 7 (building narrative, Act 4 of six-part series)
- *Nine Voices* — Wed Apr 9 (building narrative, Act 5 of six-part series)

**Weekly Ship**:
- Ship #037 "New Ground" — Wed Apr 8 (Shipping News + LinkedIn)

**Cross-posted to LinkedIn**: Silent Failures, The Mismatch Category.

**Note**: Fixing the Foundation also appeared in the Apr 8 omnibus as published that day; the editorial calendar shows pubDate Apr 7. Both dates may be correct (blog publish vs Medium syndication).

## Publication Cadence

The Docs agent corrected the publication schedule during this window: **Tue/Thu for building narratives, Sat/Sun for insight pairs, Wed for Ship**. This cadence is now explicit in the editorial calendar rather than existing only as undocumented practice.

All blog posts this week were blog-first canonical publishes to pipermorgan.ai, continuing the pattern established Mar 28. The publishing workflow is visibly maturing — Docs advanced the publish-to-blog skill to v0.5 and the pipeline is getting smoother with each post.

## Six-Act Series Status

The inversion arc (Mar 13-22) is nearing completion:

| Act | Title | Status |
|-----|-------|--------|
| 1 | Ten Roles, One Day | ✅ Published Mar 26 |
| 2 | Are We Doing It Backwards? | ✅ Published Mar 31 |
| 3 | The Floor That Wasn't | ✅ Published Apr 2 |
| 4 | Fixing the Foundation | ✅ Published Apr 7 |
| 5 | Nine Voices | ✅ Published Apr 9 |
| 6 | The Closing Sprint | Scheduled Apr 14 |

After Act 6 publishes, the building narrative queue runs out. New narrative material is needed — the M1 gate UAT story (Apr 3-9) is the obvious next arc. See "Narrative Planning" section below.

## Content Production

No new drafts were produced during this window. The focus was publishing from the deep pipeline built in the Mar 26 session (15 drafts) and the Apr 4 sequencing work (three-weekend thematic plan for insights).

**Weekend insight plan status**:
- Apr 5-6: ✅ Silent Failures + The Mismatch Category ("things hiding in plain sight")
- Apr 11-12: The No-Anchoring Roundtable + Archaeological Debugging ("how you figure things out") — the calendar shows No-Anchoring Roundtable scheduled for Apr 11
- Apr 18-19: Thirteen Mailboxes + Sibling Intelligence ("working together at scale") — Sibling Intelligence scheduled for Apr 19

## Pipeline State

The pipeline remains deep on insights (17 unscheduled after this weekend's publications) but the building narrative queue is running dry. The six-act series finishes Apr 14 with one remaining act. After that, we need new narrative material.

**Insight backlog**: 17 unscheduled pieces (4 March, 3 February, 10 older Nov-Jan). Two weekends of thematic pairs are planned (Apr 11-12, Apr 18-19). Beyond that, the backlog sustains many more weeks.

**Building narrative gap**: After The Closing Sprint (Apr 14), the next natural narrative arc is the M1 gate UAT story — a compelling three-act structure is sitting right there in the omnibus logs (see below).

## Conference Talk

IAC presentation ("Ethics as Information Architecture," Apr 17, Philadelphia) — **7 days away**. PA reviewed the talk during the Apr 8 session and noted it is approximately 90% ready, flagging that the 80.3% proof point needs verification. Draft deck (16 slides) and speaker notes exist from Mar 15. This remains the highest-priority Comms item. PM and Comms have not yet done the collaborative refinement session that was flagged as next priority on Mar 30.

## M1 Gate UAT — Story Material

The M1 gate UAT story from this week is significant narrative material. The arc:

**Round 1 (Apr 3)**: 0/9 passed. The gate design works — it catches exactly what 6,300 green tests cannot. Pattern-045 ("green tests, red user") confirmed in production.

**Round 2 (Apr 7)**: 0/9 again. The fix didn't fix it. The API key wasn't the real problem. The team has to go deeper.

**Round 3 (Apr 8)**: 5/9 passed. Lead Dev's Five Whys traces the real root cause — a deprecated OpenAI model ID silently returning 404, caught by error handling, never surfacing to user or logs. The floor comes alive for the first time in user testing. The stakeholder presentation query — the origin story of the floor inversion — scores 8/9.

This is strong material for at least two pieces: a building narrative ("The Gate Meets Reality" or similar) and an insight piece about the Five Whys investigation pattern applied to debugging silent failures across system boundaries.

---

*Submitted: April 10, 2026*
