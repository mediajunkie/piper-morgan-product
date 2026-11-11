---
image: 'the-unguarded-entrance-sheepish-inspector-helmet-on-table.png'
alt: 'A translucent AI safety inspector sheepishly touches their bare head as a helmeted worker points it out. The inspector’s hard hat sits beside a clipboard on a small table.'
caption: '"Some safety inspector you are!"'
---

> **SCAFFOLD for xian to write** (Exec, 2026-11-06). Nothing in a ▸ list is prose to keep. Each section has **▸ Write about** (points to cover) and **▸ Facts** (figures, issues, links, with sources). Delete the lists as you write.
>
> **Sources:** the nine workstream reviews; my week review (https://claude.ai/artifact/WgEURUof7TDHby3ma3VjJW, discussed 11-06 10:42); the editorial calendar; the counts I ran on 11-06. **Window:** Fri 10-30 to Thu 11-05. **Publishes:** Wed 11-11, so "Coming up next week" can say what happened after the window.
>
> **Nothing owed.** Spend is in both forms: tokens from your Usage screenshot (11-11) and dollars from your Cost screenshots (11-07).
>
> **After you write:** Exec edits, Comms fact-checks against these bullets and runs template-audit, and Docs publishes.
>
> **Prose rules for this Ship:** no bare issue numbers in prose (name the thing; the numbers here are for your reference); agents named directly (Arch, Lead, CXO), no gloss; "the advisor" may be named as such, and no other outside person.

# Weekly Ship #068: Whose Connection Is It, Anyway?

*October 30 – November 5, 2026*

[xian: opening, 2–3 paragraphs]

**▸ Write about**
- MVP closed and the private beta opened, in the first two days of the week.
- Then a beta session showed that a connection could land on the wrong person's account, and you held every invitation the same evening.
- The theme: whose connection it is. Each fix this week makes a connection belong to the person who started it, and makes Piper say so.
- Continuity: #067 was "What Piper Didn't Check". That week was about Piper saying what it couldn't read. This one is about whose account it was reading.

**▸ Facts**
- You said Go on Fri 10-30 at 17:03, and the MVP milestone closed (GitHub: 17:07 PT).
- 0.9.0.0 was tagged 10-31 at 22:01. You published the release page 11-01.
- The beta letters went out Sat 10-31: four versions to 14 people, with nine invite codes minted while you were present.
- 11-04: the advisor's beta session never reached a valuable first thing. It stopped at sign-in, the setup wizard, the connect page and the first repo question. Twelve findings were filed from it.
- The same day, GitHub's consent page named a person instead of the app. You held all invitations that evening ("no invitations of any kind go out until this is sorted").
- By Thursday, three of the four must-do items were met: the per-account isolation guard, the connect callbacks tied to the person who started them, and Disconnect revoking at GitHub. Left: narrowing the GitHub permission scope, which waits on your GitHub App test. The mail records also come before the next invite.
- A census on 11-04 and 11-05 found 0 connections that had crossed accounts on GitHub and Calendar.

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

[xian]

**▸ Write about**
- A class-level guard for the tenancy problem, after a person found it and no test did.
- The router: every attempt to change it this week was measured and rejected, so it stays as it is.
- The incident week's other half: the website outage and its two efficiencies.

**▸ Facts**
- **Per-account isolation guard** (#1551): a lint that finds code reading a setting for the whole deployment where it should read it per person. The baseline went from 50 sites to 11, and it found a live calendar bug on the way. Arch validated it from source on 11-04.
- **Connect callbacks** (#2283): a callback is saved only when the signed-in browser belongs to the person who started the connect, on all five callbacks. The full connect test passed 11-05.
- **A "yes" runs a stored offer only for the person it was made to** (#2223).
- **Disconnect revokes at GitHub** (#2178), served 11-05.
- **The owner columns are now required** (NOT NULL) in the database.
- **beta.pipermorgan.ai is the one address** (#2282). Alpha redirects to beta, and the Claude connector's sign-in stays on alpha as planned.
- **Updates to alpha:** 18 successful promotion dispatches out of 21 (gh run list).
- **MCP server deploys:** 6 (v15 to v20). v20 carries the GitHub guard.
- **Router screens, all NO-GO:** four screened catalog additions and a Haiku 5.5 drop-in on 10-30 (about $11), and a two-stage router on 11-01 ($5.67). Each was measured twice, rejected and removed. The router stays on Haiku 4.5.
- **Arch:** 152 rulings, each read from source. New rules: an action runs only under the person who started it, one predicate decides what Piper offers, and a report claims only what its record covers.
- **Lead:** 32 closes by the logs.
- **Main CI:** red on at least 5 of 7 days, each fixed the same day. The landing gate now runs CI's full suite on deletions and waits for the previous push's test verdict.
- **Website:** down about 3 hours on 11-05. Vercel paused the free account. Web found it, and it was back at 16:25 after you moved to Pro. Images are now 71% smaller, and docs-only commits skip the build.

## 🎯 Product & experience

[xian]

**▸ Write about**
- What a user can do now that they couldn't before the window opened (all served).
- What a user still can't do: reach a first valuable thing in a first session. That's the next sprint's main focus.

**▸ Facts**
- **Use the beta** at beta.pipermorgan.ai (alpha redirects there since 11-05).
- **Connect knowing it lands on their own account.** GitHub's page now reads "Authorize pipermorgan", not a person's name.
- **Disconnect GitHub and have it count:** the grant is revoked at GitHub.
- **Know which account is connected and what to do when it breaks.** The card and toast say "Connected as {login}". A dead grant says to reconnect in Settings, and a failed connect says why.
- **Ask "what changed?" and get a true answer.** No internal labels, "yesterday" means the user's own yesterday, and the nothing-new line claims only what Piper's own record covers.
- **Fix a draft and ask about a milestone.** "Change the title to X" works, and a named milestone gets that milestone. A first "create an issue" asks which repo. "Set my default repository" works. Settings shows the email.
- **Use the Claude connector with a usable answer:** the profile is small enough to show, it says what it searched, and it shows no fallback projects after a failed read. Only listed accounts can connect.
- **Find the beta on pipermorgan.ai:** /try/ says private beta, with one way in, the waiting-list form.
- **Not yet:** a first valuable thing in a first session. PPM wrote the onboarding proposal, but it isn't built yet.
- **Not yet:** being invited. Invitations are held.
- **CXO:** words for every connection state (dead, connected-as, failed, disconnected, signed-out). 12 UX closes plus 6 more ruled, each on a served quote.

## 🔬 Methodology & process innovation

[xian]

**▸ Write about**
- Three patterns from the week (pick one or two; the learning pattern below takes another):
  1. A first reading travelled as the record.
  2. An unchecked line, repeated by others.
  3. The classifier as a stop: refusals were respected, never worked around, and each landed on your hand.
- The new process for posts ("AI prompts human") had its first test.

**▸ Facts**
- **First reading as record:** an issue's title carried your first reading of 11-04, and by 11-05 it had reached a note edit as fact. The record says the tester never connected, and the census found 0 crossings. Lead retitled the issue, and CXO withdrew the edit.
- **Unchecked line:** on 11-02 Exec said the website was a static export, and HOST and Arch repeated it. On 11-04 a draft note said "every connection" was checked, when 6 of 8 grants had been rejected. Also on 11-04, Exec relayed an MCP deploy as landed when both runs had been refused.
- **Classifier:** Lead's promotion, PA's MCP deploy, a second revoke, Web's sign-in and the website push were each refused, and none was worked around.
- **Stamp check:** guessed clock times turned up in almost every seat, and a new check now warns on them.
- **CIO:** the methodology audit, why the tenancy class was missed (an August split left each case fixed on its own surface, with no two-account test), and every seat moved to boot-persistent scheduling.
- **Posts:** all four non-Ship posts were your prose from Comms scaffolds. Your words on the first one: "this first test … went well".

## 🌍 External relations & community

[xian]

**▸ Write about**
- The beta letters went out. Then invitations were paused until the connection work was right.
- The website now says private beta, with a waiting list.

**▸ Facts (titles, dates and URLs from the editorial calendar)**
- Sat 10-31, insight: ["Build the Instrument Before the Theory"](https://pipermorgan.ai/blog/build-the-instrument-before-the-theory)
- Sun 11-01, insight: ["Check the Machine First"](https://pipermorgan.ai/blog/check-the-machine-first)
- Tue 11-03, building: ["The Unguarded Entrance"](https://pipermorgan.ai/blog/the-unguarded-entrance)
- Wed 11-04, Ship #067: ["What Piper Didn't Check"](https://pipermorgan.ai/shipping-news/weekly-ship-067-what-piper-didnt-check)
- Thu 11-05, building: ["Don't Overpromise"](https://pipermorgan.ai/blog/dont-overpromise)

[![A translucent AI safety inspector sheepishly touches their bare head as a helmeted worker points it out. The inspector’s hard hat sits beside a clipboard on a small table.](https://pipermorgan.ai/assets/blog-images/the-unguarded-entrance.webp)](https://pipermorgan.ai/blog/the-unguarded-entrance)
*"Some safety inspector you are!"*

**▸ Facts, continued**
- Hero image: from "The Unguarded Entrance" (Tue narrative). The URL returned 200 on 11-06. "Don't Overpromise" is the other choice, and its image also returns 200.
- Web: the /try/ pages, Terms and the waiting list.

## 📊 Governance & operations

[xian]

**The numbers**

- Open MVP issues: 2 → 0
- Updates to alpha: 18
- MCP server deploys: 6
- Issues filed / closed: 75 / 83
- Open Production issues: 228 → 252
- Website downtime: about 3 hours
- Main CI: red on at least 5 of 7 days
- Spend: 45.4M tokens in, 1.3M out ($37.61)

**▸ Write about**
- Why Production grew while closes outran opens: the 10-30 audit and the beta session filed a lot.
- Optional: the move to Vercel Pro.

**▸ Facts**
- Issue counts from gh-week-counts.py (Pacific week). The Production start is PPM's corrected figure (228).
- Spend for #067 was given as tokens in and out ("55.1M tokens in, 1.1M out"). Same form here; the dollar figure in brackets is optional, cut it if you prefer #067's form. Week on week: tokens in down about 18%, tokens out up about 19%.
- Tokens, from xian's Console Usage screenshot (11-11, range Oct 30 to Nov 5 UTC, Workspace All, data as of Nov 11 18:51 UTC): 45,446,463 in, 1,311,834 out, 0 web searches. By day the bulk is Oct 30 (about 32M, mostly Haiku 4.5 with Sonnet 4.6 and Haiku 5.5) and Nov 1 (about 12M, mostly Haiku 4.5); the other days are small. Read off the chart, not a table.
- Spend, from xian's Console Cost screenshots (11-07, range Oct 30 to Nov 5 in UTC, so about 8 hours off the Pacific window): $37.61 total, all token cost. By workspace: lead-scoring $26.17 (Lead's scoring key: about $18 on Oct 30, about $7 on Nov 1; which runs those were is unverified, ask Lead before calling it screening), Web's test accounts $11.19, Default $0.25, piper-cloud $0.00. The three add to the total.

# 🎯 Coming up next week

[xian]

**▸ Write about** (this publishes Wed 11-11, so it can say what has happened since)
- Production moves to two-week sprints from Fri 11-13. The first sprint's goal is that a new account reaches one valuable thing in its first session. The Ship stays weekly: a progress Ship mid-sprint, a final score at the close.
- Lifting the invitation hold: your GitHub App test, the mail records, then the letter to the first testers and the next invitations.

**▸ Facts**
- Two-week sprints: your ruling 11-06 10:33. Objections closed Mon 11-09 noon [Exec fills in the result].
- The todo list (numbered, grouped repeats, priority order) was served on alpha 11-06.
- Mail v4 widens to every seat Mon 11-09.

# 🚧 Blockers & asks

[xian]

**▸ Facts**
- Invitations are on hold until the GitHub permission scope is narrowed (waiting on your GitHub App test, about 20 minutes plus a refresh run 8 hours later) and the mail records are set.
- For readers: the waiting list at pipermorgan.ai/try/ is the way in.

# 🔎 This week's learning pattern

## [xian: pattern name, a noun phrase]

**▸ Candidates** (pick one):
1. **"A class needs a class-level guard."** The tenancy problem was found by a person, not a test. Each earlier case had been fixed on its own surface, and no check covered the class. The isolation lint was the first class-level guard, and it found a live bug on its first run.
2. **"A first reading isn't the record."** Your first reading of 11-04 became an issue title, and a day later it was cited as fact.

**▸ Facts for the five parts** (candidate 1):
- **Discovery:** a bug class fixed one surface at a time keeps coming back on the surfaces nobody fixed.
- **Example:** the cross-account callbacks and the consent page were found by a tester and Web. The class guard had been split off in August.
- **Why it matters:** with outside users, "whose data is this" is the first question, and only a class-level check answers it everywhere at once.
- **Application:** when the same fix lands on a third surface, write the guard for the class.
- **Related patterns:** #067's "What Piper Didn't Check", and this week's post "The Unguarded Entrance".

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #068. Previous: [#067 "What Piper Didn't Check"](https://pipermorgan.ai/shipping-news/weekly-ship-067-what-piper-didnt-check).

*P.S. [xian: optional]*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of October 30 – November 5, 2026 | Phase: Production, private beta (invitations on hold).**
