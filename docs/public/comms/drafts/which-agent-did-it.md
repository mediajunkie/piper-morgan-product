---
image: ''
alt: ''
caption: ''
---

# Which Agent Did It?

The question of how to attribute and trace work done by agents is more complicated than it looks. For example, Piper Morgan has a project repository at GitHub where I host the codebase, documents, and the rest of the context the agents need to do their jobs. All of the agents interact with GitHub to keep their work in sync, to send each other memos, to rebuild the software and test it, and so on.

The thing is, they all log in as me. It's my account. Sure, stuff Claude does gets that "coauthored by [your name] and Claude" line added here and there, but when reviewing or tracing pass commits or closed issues, we have not had a clear, traceable way for agents (or "seats" as they've taken to referring to each other when discussing logistics) to sign their own work.

# I used to live in room full of mirrors

My chief innovation agent (CIO) was doing some diligent checking related to a database restarter on the agenda, trying to anticipate any adverse impact on the main branch. CIO pointed out that "every seat acts on GitHub as `mediajunkie`, xian's own account" and also my account is "the repo's admin." 

This means every agent, acting as me, also inherited the right to bypass any rules, meaning they can approve their own runs, with the only thing holding them back being our own internal rules.

This for example meant that my head of sapient trust agent (HOST) has to withdraw their earlier claim that a pull request that requires a reviewer counts as "attended" because I have to approve the PR for it to go through. If any agent can act as me and approve it then requiring a reviewer does not necessarily mean the approval has to be attended by the human who owns the loop (me).

As CIO put it "The chokepoint (required reviewer, rules) checks an identity, and every seat passes as that identity."

This "acting as me" loophole extends deeper than GitHub. The agent team debated narrowing what each agent's key could do but CIO argued "scoping can't meet the bar, because all 26 Claude processes run as Unix user `xian`, and read-denies are advisory, not OS permissions." On my Mac Studio, every agent is me, as well.

# How to distinguish them from me


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
