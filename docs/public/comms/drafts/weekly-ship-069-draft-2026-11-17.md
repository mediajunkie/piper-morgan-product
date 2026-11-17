---
image: 'the-server-key-is-not-a-real-concept-ef13a6ab-ad10-4ae4-806d-bf09bb466add.jpg'
alt: 'An AI locksmith secures a coin purse attached to a vending machin e while a puzzled proprietor gestures toward it and a customer waits with their own coin.'
caption: '"Who gave it a wallet?"'
---

> **SCAFFOLD for xian to write** (Comms, 2026-11-17). Nothing in a ▸ list is prose to keep. Each section has **▸ Write about** (points to cover) and **▸ Facts** (figures, issues, links, with sources). Delete the lists as you write.
>
> **Sources:** Exec's week review (`docs/internal/planning/comms/ship-reviews/ship-069-week-review.html`, from all ten workstream reviews, discussed with you 11-13 17:07 to 17:42); your theme pick ("Off-Limits by Default", 11-13); your yes to the five goals (11-17, via Janus and Exec); the spend from your Console screenshots (Janus's transcription); the editorial calendar; decisions.log; GitHub issue states read 11-17 at 08:4x. **Window:** Fri 11-06 to Thu 11-12. **Publishes:** Wed 11-18, so "Coming up next week" can say what happened after the window.
>
> **The theme's guard rail** (calendar note, 11-13): lean on the week's facts (the keychain reads, the opt-in fix, the GitHub App's narrower grants). Don't retell Thursday's "The Server Has No Key".
>
> **After you write:** Exec edits, Comms fact-checks against these bullets and runs template-audit, and Docs publishes.
>
> **Prose rules for this Ship:** no bare issue numbers in prose (name the thing; the numbers here are for your reference); agents named directly (Lead, Arch, CXO), no gloss; "the advisor" may be named as such, and no other outside person. If you mention the Anthropic console, its address is now platform.claude.com/dashboard.

# Weekly Ship #069: Off-Limits by Default

*November 6–12, 2026*

[xian: opening, 2–3 paragraphs]

**▸ Write about**
- The theme comes from your own ruling mid-week: your keychain is off-limits unless you say so. By Thursday that was the default in the code, not a rule each agent had to remember.
- The same idea ran through the GitHub move: on Thursday evening you moved GitHub onto the published Piper app, and a tester now grants the repositories they choose, not every repository.
- Continuity: #068 was "Whose Connection Is It, Anyway?" (whose account a connection belongs to). This week asks what a connection, or an agent, may touch by default.
- One step back, on purpose: every connected tester, you first, had to reconnect GitHub.

**▸ Facts**
- Your ruling, 11-11 11:12 (decisions.log, Exec relaying you in conversation): "We do need to keep my local keychain off-limits, at least without permission".
- The cutover ran 11-12 at 19:06 PT and revoked all 10 old GitHub tokens (your apply output, week review).
- Last week's five goals: 2 met (the posts, mail v4), 3 with substantial progress (the invite hold, onboarding, serving what's built). Your words 11-13: "So it's 2 goals complete, 3 with substantial progress."
- You also accepted the public-beta gate (PDR-009). Its likeliest close is sprint 6 or 7 (01-08 to 02-04), per PPM's gate map.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

[xian]

**▸ Write about**
- The keychain story: three separate reads of your keychain, each fixed in one script, until the fix moved to the one place every path goes through (the credential store's default).
- The GitHub App cutover and what "narrower" means today (careful, see the caveat).
- Built isn't served: the MCP app sat a week behind main, and a promotion was refused because a merge commit hid main's tested commit.

**▸ Facts**
- **Keychain reads** (week review, all three Lead's): five local server starts on 11-11 read your OpenAI and Anthropic keys; a Slack smoke test wrote a fake entry to your login keychain on every run; on 11-12 at 17:11 a check script asked for one entry and timed out.
- **The fixes:** tests and the documented server start no longer read your keychain (#2338, closed 11-11); the screening scripts no longer read provider keys from it (#2340, closed 11-11); and the keychain became opt-in for the whole app (#2353, closed 11-12 19:17 PT). Since then nothing reads it unless `PIPER_CREDENTIAL_STORE=keychain` is set, and CLAUDE.md forbids a seat to set it.
- **GitHub App cutover** (#2342, ADR-081 D3): 11-12 19:06, 10 old tokens revoked, 0 left. Row 1 passed that evening (PA 19:15, CXO ruled).
- ⚠️ **Caveat for "narrower grants":** it holds for the repository list a tester grants. Two gaps were open at the window's end and are still open today: issue and PR searches still read every repository the person is assigned in (#2374, open), and some single-repo reads could answer for a public repository the App isn't installed on (#2379, open; Arch validated the fix at the unit layer 11-16, and it reached beta that evening). Say "you choose the repositories", not "Piper can only see what you chose".
- **MCP app a week behind:** PA found it before the cutover. One MCP deploy this week, v21 (4666e38493), yours, 11-12, before the cutover (PA's count).
- **Promotion refused by a merge commit** (#2363, found by CIO): the gate looked only at the first parent. Fixed on main 11-13 (after the window).
- **Updates to beta:** 32 successful promotion dispatches of 36 (gh run list). Lead counts 33 builds that reached beta; one run was marked failed after the machine had updated. Two were refused by the gate (11-07 Tests still running; 11-12 the merge commit).
- **Arch:** 160 rulings. ADR-082 and ADR-083 (D5) accepted; ADR-081 D3 governing.
- **Lead:** 11 closes; the test backlog went from 55 to 20.
- **Main CI:** red on at least 3 of 7 days (7 times by Lead's pushes, 5 to 60 minutes each).

## 🎯 Product & experience

[xian]

**▸ Write about**
- What a user can do now that they couldn't on 11-05 (all served).
- The step back: the reconnect, and the words testers see.
- What a user still can't do.

**▸ Facts** (week review's "what a user can do now", each served)
- **Point at a todo after a list:** "complete the second one", "delete the first two" and "complete the X todo" act on the lines just shown. When the words fit more than one line, Piper asks which. With no list shown, it asks rather than guessing.
- **Ask about a repo and get the repo:** before, the answer could be "I don't see that document". Now it asks which repo when there are several, and a past-due milestone is called overdue. The advisor's phrasing went from 1 of 6 to 7 of 7.
- **Change or forget a learned preference,** with consent before forgetting.
- **Add a repo to a project without a "yes" loop,** and find Integrations in a reorganized Settings. Sign-in accepts a wrong-case email (partly).
- **Stay signed in under load:** past 20 concurrent requests, sign-in no longer refuses everyone.
- **Get invitation mail that passes SPF, DKIM and DMARC** (#2292, closed 11-12).
- **Step back:** testers see CXO's line: "… Reconnect GitHub in the Piper Morgan app, in Settings under Integrations, and choose which repositories I can see. Your saved settings are unchanged."
- **Not yet:** complete a todo by pronoun ("mark them done", #2328, 0 of 5 served). Run Piper on your own computer (helper on main, guide a draft). Be invited, or reach a first valuable thing in a first session.

## 🔬 Methodology & process innovation

[xian]

**▸ Write about**
- Pick one or two of the week's four patterns (the learning pattern below takes the first):
  1. An operator's credential, read by default: bolt-on fixes per script missed the next script; the fix that held was at the chokepoint.
  2. Built isn't served, three layers deep: the MCP app, a promotion, and last week's goal 3 (seven built items, none closed).
  3. The classifier as a stop, again: credential reads for PA and Web were refused on 11-10, nobody worked around them, and the cost landed on you.
  4. Guessed clock times, in every seat.

**▸ Facts**
- Chokepoint versus bolt-on is CIO's methodology-53.
- The refused reads left the pronoun todo fix at 0 of 5 served all week.
- Guessed times: Docs, CIO, PA, PPM, Comms, Lead and Exec each reported one or more. The stamp check catches them before commit, and the habit hasn't changed.
- **Mail v4 reached every seat on 11-09:** 11 of 11 canaries answered, and seat mail on v4 went from 6% to 85% by 11-11 (CIO).
- **CIO:** the key-in-docs lint (3 sites to 0).
- **Docs:** nine pages no longer teach a key on a command line.
- **Posts:** all five were your prose from Comms scaffolds.

## 🌍 External relations & community

[xian]

**▸ Write about**
- Five posts, all distributed, including Ship #068.
- Optional: one of this week's posts was mislabelled (a building post's label on a weekend insight), and a slot guard now checks the weekday.

**▸ Facts (titles, dates and URLs from the editorial calendar)**
- Sat 11-07, insight: ["At Long Last, Beta"](https://pipermorgan.ai/blog/at-long-last-beta)
- Sun 11-08, insight: ["When Accuracy Scores Worse"](https://pipermorgan.ai/blog/when-accuracy-scores-worse)
- Tue 11-10, building: ["Never Green in a Thousand Runs"](https://pipermorgan.ai/blog/never-green-in-a-thousand-runs/)
- Wed 11-11, Ship #068: ["Whose Connection Is It, Anyway?"](https://pipermorgan.ai/shipping-news/weekly-ship-068-whose-connection-is-it-anyway)
- Thu 11-12, building: ["The Server Has No Key"](https://pipermorgan.ai/blog/the-server-has-no-key) (Medium only, on your word)

[![An AI locksmith secures a coin purse attached to a vending machin e while a puzzled proprietor gestures toward it and a customer waits with their own coin.](https://pipermorgan.ai/assets/blog-images/the-server-has-no-key.webp)](https://pipermorgan.ai/blog/the-server-has-no-key)
*"Who gave it a wallet?"*

**▸ Facts, continued**
- Hero image: from "The Server Has No Key" (Thu narrative), the closest to the theme. The URL returned 200 on 11-17. "Never Green in a Thousand Runs" is the other choice ("This one passes every time!"), and its image also returns 200.
- ⚠️ **Your call:** the alt text is verbatim from the post's frontmatter and carries a typo, "vending machin e". With your OK I fix it here and in the post's frontmatter.

## 📊 Governance & operations

[xian]

**The numbers**

- Updates to beta: 32
- MCP server deploys: 1
- Issues filed / closed: 70 / 26
- Open Production issues: 252 → 297
- Keychain reads: 3, then opt-in
- Main CI: red on at least 3 of 7 days
- Spend: $33.38 (29,317,890 tokens in, 702,410 out)

**▸ Write about**
- Where the spend went: almost all of it in the first three days, mostly one key.
- Optional: why Production grew (the beta session's findings and the GitHub work were filed in the window).

**▸ Facts**
- Issue counts from gh-week-counts.py (Pacific week). Production open counts are PPM's. 22 of the 26 closes were Production.
- **Spend** (Console, Workspace All, 11-06 to 11-12 UTC; Janus's transcription of your screenshots, which Exec and I haven't seen): $33.38 total, all token cost. 11-09 to 11-12: $0.07. By day, read off the bar chart, approximate: 11-06 about $13.50, 11-07 about $8.60, 11-08 about $11. Don't print the daily figures as exact.
- By key: `lead-scoring-2026-10` is most of every large bar, `web-alpha-test-accounts` the smaller part of 11-06 to 11-08, `github-actions-e2e` slivers. Router screens, per the week review: about $12 on 11-06 to 11-08, none from 11-09 until a provider key was picked. Whether that $12 is inside the $33.38 is unverified.
- #068 gave spend as tokens in and out. This list gives both.

# 🎯 Coming up next week

[xian]

**▸ Write about** (this publishes Wed 11-18, so it can say what has happened since)
- Sprint 2 started Fri 11-13: onboarding to first value, 11-13 to 11-26. Ship #070 is its progress report.
- The five goals you approved for 11-13 to 11-19.
- Since the window: you reconnected, and the GitHub rows passed. You also approved a budget so agents can test without your hands.

**▸ Facts**
- **Goals for 11-13 to 11-19** (your yes, 11-17: "1. yes 2. yes 3. yep 4. yes 5. agree"):
  1. Finish the GitHub move: a signed-in read of the new repositories card, then the classic-scope issue (#2261) closes and PPM writes the lift-readiness memo.
  2. Agents test without your hands (ADR-084): the test key, the sign-in helper and the second test account in place; the first paid screen and the first signed-in read by an agent.
  3. Sprint 2's first week: the todo rows (#2219, #2294, #2295, #2328), the wizard (#2268, #2274, #2275, #2286) and Path B (#2297, #2301).
  4. Self-host and self-knowledge: the guide's clean-clone run finished with a key, and the Tier 1 texts approved against CXO's voice spec.
  5. Editorial: "The Wall" and Ship #069 out, and your pick of the weekly cadence and weekdays.
- **Since the window:** your reconnect, and #2342 rows 2 and 3 served 11-15 (Arch 15:22 and 15:56). The App grant read the private repository it's installed on and not one it isn't.
- **ADR-084 accepted 11-16 06:20** ("Yes to ADR-084 and budget"): an agent may spend up to $10 a run without asking, $150 a month at most.
- **Two safeguards live 11-16:** a push that loses a race no longer re-runs two minutes of checks, and a commit that adds a credential shape is refused (#2392, closed).

# 🚧 Blockers & asks

[xian]

**▸ Facts**
- Invitations stay on hold until the per-user isolation epic (#1551) and the classic-scope issue (#2261) are done. Disconnect revoking at GitHub (#2178) is closed.
- The issue and PR search gap (#2374) is still open.
- For readers: the waiting list at pipermorgan.ai/try/beta/ is the way in.

# 🔎 This week's learning pattern

## [xian: pattern name, a noun phrase]

**▸ Candidates** (pick one):
1. **"Fix it at the chokepoint."** Three keychain reads, each patched in its own script, until the default changed in the one place every path passes through.
2. **"Built isn't served."** The MCP app a week behind, a promotion hidden by a merge commit, seven built items that never closed.

**▸ Facts for the five parts** (candidate 1):
- **Discovery:** a rule each script has to remember fails at the next script nobody patched. Changing the default where every path goes through holds for all of them.
- **Example:** your keychain. A server start, a smoke test and a check script each reached it in the same week. The per-script fixes (#2338, #2340) held for their scripts. The opt-in store (#2353) closed the class.
- **Why it matters:** "off-limits" has to be the default, or it depends on every agent remembering it every time.
- **Application:** when the same fix lands on a second surface, look for the chokepoint before the third.
- **Related patterns:** #068's "Guard against a class of problems" (the same idea, for tenancy); this week's post "The Server Has No Key".

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #069. Previous: [#068 "Whose Connection Is It, Anyway?"](https://pipermorgan.ai/shipping-news/weekly-ship-068-whose-connection-is-it-anyway).

*P.S. [xian: optional]*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of November 6–12, 2026 | Phase: Production, private beta (invitations on hold).**
