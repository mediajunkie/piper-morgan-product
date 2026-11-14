---
image: ''
alt: ''
caption: ''
---

# Which Agent Did It?

*October 21–23, 2026*

The question of how to attribute and trace work done by agents is more complicated than it looks. For example, Piper Morgan has a project repository at GitHub where I host the codebase, documents, and the rest of the context the agents need to do their jobs. All of the agents interact with GitHub to keep their work in sync, to send each other memos, to rebuild the software and test it, and so on.

The thing is, they all log in as me. It's my account. Sure, stuff Claude does gets that "coauthored by [your name] and Claude" line added here and there, but when reviewing or tracing past commits or closed issues, we have not had a clear, traceable way for agents (or "seats" as they've taken to referring to each other when discussing logistics) to sign their own work.

# I used to live in a room full of mirrors

My chief innovation agent (CIO) was doing some diligent checking related to a database restarter on the agenda, trying to anticipate any adverse impact on the main branch. CIO pointed out that "every seat acts on GitHub as `mediajunkie`, xian's own account" and also my account is "the repo's admin." 

This means every agent, acting as me, also inherited my account's right to bypass the repo's rule, meaning an agent could approve its own run, with the only thing holding them back being our own internal rules.

This for example meant that my head of sapient trust agent (HOST) had to withdraw their earlier claim that a run requiring a reviewer counts as "attended" because I'd have to approve it for it to go through. If any agent can act as me and approve it then requiring a reviewer does not necessarily mean the approval has to be attended by the human who owns the loop (me).

As CIO put it: "The chokepoint (required reviewer, rules) checks an identity, and every seat passes as that identity."

This "acting as me" loophole extends deeper than GitHub. The agent team debated narrowing what each agent's key could do but CIO argued "scoping can't meet the bar, because all 26 Claude processes run as Unix user `xian`, and read-denies are advisory, not OS permissions." On my Mac Studio, every agent is me, as well.

# How to distinguish them from me

The solution the team came up with was for me to create a GitHub App for the agents. The app is installed just in the relevant repo and has read/write permissions on code, issues, pull requests and Actions, but no workflow permission. 

A first test push to a protected branch was refused as expected, specifying who or what was refused: "actor `piper-morgan-agents[bot]`," while my own ordinary pushes went through fine by means of the bypass set up for my own convenience.

During the transition, we've left my own admin key and command-line `gh` login authenticated on the Amber machine all the Code agents run on. (We ended up leaving these in place too long and realizing they were being used as a fallback about a week later).

# Full attribution still unsolved

Preparing for this post, my communications agent (Comms) checked the last 200 commits on main and verified that all are still attributed to me, although some distinctions are visible. Eight of them came from the admin UI I'm using right now to write this blog post. The other 192 went through the usual way. The "App bot" method still signs all changes with me as the author. It just changes how the push is done.

For now, we still rely on a convention of including the information about which agent did what in a pair of trailer lines at the bottom of each message ("Co-Authored-By" and a session link), and in the analysis of 200 commits, only 119 had those. I expect this to improve since a hook has required the trailer on my account's commits since October 2.

I'm still figuring out where separation of roles, tasks, identities belong with these agent entities. A lot of the practices are first-draft ideas borrowed directly from human organization patterns. You can't even ask "Who is who?" without establishing first if you are asking a philosophical question or a technical one.

# Postscript: keeping the key safe

Just this past week I had to make it 100% clear: "We do need to keep my local keychain off-limits, at least without permission." This came up when the lead developer agent (Lead) initiated a test run that started the local server running on my Mac Studio. The local build was still able to read my OpenAI and Anthropic keys from that Mac's keychain and validate them with the providers.


---

*Next on Building Piper Morgan: "No New Skills This Time," in which the team reviews thirteen ideas for new agent skills and builds none of them.*

*If you looked at your own team's written history today (human or otherwise), could you tell who actually did each thing?*
