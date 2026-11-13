---
image: ''
alt: ''
caption: ''
---

# Which Agent Did It?

*October 21–23, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. PM writes
the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Slot: Sat 2026-11-14 (insight). Mining candidate 8 ("One Account Means One Hand", held 11-04), retitled by xian 11-12.
Teased by Thu 11-12 "The Server Has No Key": "every agent on the team has been acting on GitHub as me."
Sources: CIO 10-21 log l.107, 109; omnibus 10-21 l.117-119; omnibus 10-22 l.184-186; CIO 10-23 log l.61; omnibus 10-23
l.200-209; omnibus 10-30 l.286-287; decisions.log l.3252 (11-11), l.3342 (11-12); issues 2353 and 2342; omnibus 10-02 l.287;
git log on origin/main (measured 11-12 22:15). Facts gathered by a Sonnet subagent. Comms re-opened every quote at source.
The dateline covers the core episode. Change it if you lead with the November hooks.
-->

---

## Title
**Which Agent Did It?** (xian's title, 11-12).

## The principle in one sentence

Splitting work across agents with different jobs means nothing for accountability if they all act under one person's
name. A rule that checks *who* is acting can't tell them apart, and neither can anyone reading the record later.

## Beats, in order (facts verified, source in brackets)

**1. The finding.** Wed Oct 21, 3:20 PM. CIO, looking at what would protect main before the database restarter was built,
found: "every seat acts on GitHub as `mediajunkie`, xian's own account and the repo's admin." And the only
rule lets that account bypass it ("`current_user_can_bypass: always`"). So "no rule separates a seat from xian, and a seat
could approve its own `alpha-db` run." [CIO 10-21 l.107, omnibus 10-21 l.117-119]
- HOST had ruled at 12:42 that a required reviewer counted as "attended". It withdrew that at 3:27, right after CIO's finding.
  (My reading, not in the source: the reviewer would be you, whichever agent clicked.) [omnibus 10-21 l.119]
- CIO's pattern note, the line that names the insight: "The chokepoint (required reviewer, rules) checks an identity, and
  every seat passes as that identity." [CIO 10-21 l.109]

**2. It goes deeper than GitHub.** Fri Oct 23: CIO, answering a proposal to just narrow what each agent's key could do:
"scoping can't meet the bar, because all 26 Claude processes run as Unix user `xian`, and read-denies are advisory, not
OS permissions." [CIO 10-23 log l.61, omnibus 10-23 l.205] On the Mac, too, every agent is you.

**3. What you did.** Thu Oct 22: HOST filed the problem about 4:28 PM, and you had created a GitHub App for the agents,
`piper-morgan-agents`, by 5:13 PM. Fri Oct 23 it was installed on this one repo, with read/write on code, issues, pull
requests and Actions, and no workflow permission. The first push as the App bot went out that afternoon. A test push to a
protected branch was refused, and the record finally showed *which* identity was refused: "actor
`piper-morgan-agents[bot]` … and xian's own pushes that day read bypass." [omnibus 10-22 l.184-186, omnibus 10-23 l.200-208]

**4. Not finished.** Your own admin key and `gh` login stayed on the agents' machine. The omnibus says you weren't ready
to take them off yet. On Oct 30 a lane pushed once "with a per-command override that used xian's `gh` login, because the
App token had expired", and the lane's own log didn't mention it. [omnibus 10-23 l.208-209, omnibus 10-30 l.286-287]

**5. The title's question, today (measured 11-12).** Of the last 200 commits on main, 192 are authored `mediajunkie` and
8 under your own name (your admin-UI edits). Even the first push "as the App bot" carries `mediajunkie` as its author.
The App changes who *pushes*, not who the commit says *wrote* it. What actually says which agent did it is a pair of
trailer lines at the bottom of each message ("Co-Authored-By" and a session link), present on 119 of those 200. A hook
requires the trailer on your account's commits. [git log origin/main; omnibus 10-02 l.287]

**6. The same shape this week (optional coda).**
- Wed Nov 11, your ruling: "We do need to keep my local keychain off-limits, at least without permission." It came up
  because Lead's local test runs started the server, which read your OpenAI and Anthropic keys from your Mac's keychain
  and checked them with the providers (nothing was written or logged). [decisions.log l.3252]
- Thu Nov 12: the keychain became opt-in for everyone (Arch's ruling, issue 2353). The issue body: "That happened twice in
  two days from one-off scripts on xian's Mac." [decisions.log l.3342]
- The product side, the same day: GitHub connect moves to one published Piper GitHub App, with each user's own short-lived
  tokens (issue 2342, not yet live). Optional. This is the users' version of the agents' App.

## Careful with these (accuracy)
- **No incident of "we couldn't tell who did it" was found.** The subagent searched the omnibus logs, not every seat log.
  The story is the *risk* CIO named (no rule can tell agents from you) and the record's blind spot, not a mystery solved.
  Don't invent a whodunit. If you remember one, it's yours to tell.
- The Oct 30 override was a lane push to its own branch, not main.
- 119 of 200 commits carry the trailers. The rest are mostly mail, merge and admin-UI commits. Say "most agent commits",
  not "every".
- The App's ID number and key details stay out.
- Don't name the beta tester or anyone outside the team. Ship #068 already told the tenancy day (Nov 4), so skip it here.

## Already told elsewhere: don't retell
- **"The Server Has No Key" (Thu)**: the operator's money. This post is the operator's *identity*.
- **Ship #068**: whose connection a *user's* GitHub link belongs to.

## Your angle, maybe
- Separation of duties is a human-org idea. With agents it's free to declare and easy to fake: each has a job title,
  and they all sign with your name.
- "Who is the actor?" as a question to ask of any gate (CIO wanted it in every gate's evidence line).
- The counterweight: one identity is also why the agents could move fast. The App made them slower and safer.

---

*Next on Building Piper Morgan: [TEASE: the next post after Sat 11-14. Nothing is on the calendar yet except Ships. Next
building beat in order is beat 4, "The Wall" (Sep 15–18), or a Sun insight if you add one.]*

*[Reader question, yours to write. A start: "If you looked at your team's history, could you tell who actually did each
thing?"]*
