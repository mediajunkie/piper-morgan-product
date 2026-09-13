---
image: ''
alt: ''
caption: ''
---

# Who's Who at Piper Morgan

*September 2026*

A friend who's a pretty keen explorer of AI, savvy about the societal ills underpinning so much of the business behind these new methods as well as equally fascinated by the better possibilities, asked me a fair question a month or so ago when we were discussing this blog series about this project. What exactly is Piper Morgan, actually, what has the project involved and what has it built so far and, more to the point, who are all these agents this blog keeps mentioning by name, and what does each one do? These a reasonable things to have no idea about at all coming midstream into the three hundred and umpteenth post in this series, as well as things that are pretty easy to lose track of if you've only read a handful of posts from time to time. I really don't expect anybody besides me to keep it all straight, so this feels like a good moment to take stock, write an overview, and then point new and returning readers to this post (and maybe yesterday's "Eras" post as well) in the future to help folks get situated or reoriented.

So, here's goes.

# The product, in one paragraph

Piper Morgan is (in the process of becoming) an AI assistant built specifically for product managers. Product managers are people who decide what a piece of software should do next and why, then have to coordinate a dozen other people to make it happen. AI *coding* tools are built for engineers. Piper Morgan is for a role abstracted one level: the one that has to hold the whole picture, not just the next function to write. The product is still in alpha, tested by a small group of real product managers on their own work.

# The founder

The person actually running this — deciding what gets built, testing it against his own daily work, writing the checks nobody else can — is me, aka "xian" (the agents also sometime just call me PM or "the PM"). As my communications agent (Comms) reminded me when scaffolding this post, I've told them team I am "still the only one who can have coffee" with the people who matter to this project, and I am the only one who makes the calls no agent can make alone. The whole team described below reports to me, in the loose sense that a small company reports to its founder or CEO. There is no other human staff. It's all xian, plus the team described next.

# The agent team

This menagerie of agents is where folks start to get confused. Am I talking about real people? Who are all these entities in these roles? We started out with just ongoing chats, then a chief architect (now called Arch, for short) as an engineering partner for me in planning. Then a chief of staff to help me run the operational side of things. Then other specialties as recurring tasks or structured work emerged and I didn't want the same chats or agents hopping from focus to focus, merging unrelated context and turning everything into a gray stew. 

A number of months ago we stabilized at the present team size. Subagents and the occasional one-off specialist may still pop up to work but the ongoing roles and portfolios have settled down to eleven agents. They all work in parallel, on a recurring schedule, mostly without a human in the loop for routine work. I stes in for judgment calls, direction changes, and anything that needs a human decision.

Seven hold leadership roles:

- **Chief of Staff** (Exec) — pulls together everyone's progress, tracks the sprint, and coordinates the weekly public update, functioning as my eyes and ears, my primary counterpart, and my one go-to point of contact when I am too busy for one-on-one chats with other agents on the team (each of the other six leadership roles all cover a specific portfolio and report up to Exec)
- **Chief Architect** (Arch) — makes the big technical-design calls and keeps the system's underlying architecture coherent, helped plan and design the product's domain models from just after the initial prototype stage last June)
- **Chief Experience Officer** (CXO) — owns how Piper *feels* to talk to: tone, interaction design, the actual user experience
- **Principal Product Manager** (PPM) — sets product strategy and roadmap priorities, mirrors my product leadership role, the way Exec mirrors my organizational leadership role
- **Chief Innovation Officer** (CIO) — notices what's working and turns it into a repeatable process, investigates and designs improvements for processes that fail
- **Head of Sapient Trust** (HOST) — looks after the health of the agent team itself and its relationships with the real people who use the product, something like an HR and trust lead
- **Communications Director** (Comms) — writes the public story: this blog, the weekly updates, voice and tone. That's the agent who planned this post with me and wrote the first draft of this sentence.

Four hold staff roles, each doing a specific, recurring job:

- **Lead Developer** — coordinates the coding work across every other agent and enforces the discipline of "does it actually work," not just "does it look done" (they are the brilliant workhorse making or overseeing the crafting of the product)
- **Piper Alpha** — product assistant to me directly, helping manage his own workload, functioning as a prototype of the Piper Morgan product itself and establish a benchmark or bar that my product needs to surpass to justify its use over a well-prompted Claude code agent.
- **Documentation Manager** (Docs) — keeps the historical record straight: synthesizes session logs from all agents into the omnibus logs that summarize each project day, runs the publishing pipeline for these posts, audits and cleans up the docs tree routinely, maintains the project glossary of what all these terms mean
- **Unicorn Web Designer/Developer** (Web) — builds and runs the pipermorgan.ai site where this blog post appears first, maintains the publishing pipeline technically, and also handles manual testing of the Piper Morgan web interface

As mentioned a smaller set gets activated for specific shapes of work rather than running continuously: there are the coding agents that come and go to handle precise, well-scoped implementation tasks other agents hand off, we've spun up a temp role called Special Assignments in the past for work that doesn't fit any standing lane. We briefly worked with an "Exploratory Testing Agent" built to poke at Piper's systems the way a real user would. It's been dormant since March, not runnning now but available if we want to use it again. For the most part, it's these 11 roles that are running the show now.

# It's hard to attribute the work at times

Every github commit in this project's history is signed with my username, xian. I have not written a single line of code (I've read a lot of it!) but the tools attribute authorship to me. Sometimes Claude is credited as well, but not consistently. Agents don't have their own distinct identities on GitHub since they all act on my behalf from the software's point of view, but I am exploring adding a custom field to my issues to track which agents is assigned to or working on that task, so that we can track such things more finely. For now, an agent's actual contribution shows up as a co-author line if you know to look, but never as the name on the commit itself. So if you go checking who built what by reading the project's own history, you'll see one name on nearly everything, regardless of which of the eleven actually did the work. It's a known, acknowledged limitation of the tooling, not a decision anyone made on purpose and it's another reason for this posts: the record doesn't tell you who's who, so somebody has to.

# Two more names you might see

Two other names show up occasionally that aren't part of this team, and are worth placing so they don't confuse a reader who's paying close attention.

**Design in Product** is my company. It has its own Claude account and a further fleet of 15 or so agents working on my own products and client projects. a sibling project, not this one. It has its own coordinating agent, Janus, whose one standing job relevant to this blog is a daily sweep across xian's various projects looking for ideas worth cross-pollinating. If a post here ever references an insight that clearly came from somewhere else in xian's world, that's the channel it traveled through. Janus oversees all of my agents for me and generates a rollup artifact every morning with a full summary of what needs my attention across the entire constellation of agents and their projects

**Dispatch** is a Claude Cowork feature designed to make it easy to coordinate work remotely. I runs a separately scoped instance of it for each of the two Claude accounts and they relay information to each other, perform monitoring and delivery tasks, and help with cross-posting these blog posts to LinkedIn and Medium as needed, using a skill we've iterated on together to handle most funky situations. The Dispatch (Piper Morgan) instance is the newest one, xian's own coordinator standing apart from this team: a second set of eyes on this project that isn't embedded in it the way the eleven above are. It doesn't replace the Chief of Staff's internal coordination job. It's a deliberately outside view, layered on top.

# The humans who show up

A handful of real people outside the agent team appear in this project's story by name, already public in earlier posts here, so it's worth naming them properly rather than leaving them as unexplained mentions. Ted Nadeau is both a close advisor and a occasional alpha tester. Beatrice Mercier, Michelle Hertzfeld, Jake Krajewski, and Dominique Derasena  are alpha testers — real product managers using Piper Morgan on their own work and reporting back what breaks. Cindy Chastain is a longtime friend of xian's, an independent design executive who hosts a podcast xian has appeared on. There are a few more testers and advisors in the wings who haven't been named publicly yet — when they are, it'll be in their own words, not a roster entry like this one.

# If you've been reading a while

If you found this blog through a single post — a build story, an incident writeup, a Weekly Ship — you now have the map the rest of it assumes. Eleven agents, one founder, a couple of neighboring projects that occasionally lend a hand, and a small circle of real people testing whether any of this actually works for them. Everything else on this site is one of those roles, doing its job, on a given day.

---

*Next on Building Piper Morgan: "The Bug That Was Misdiagnosed Twice" — three colleagues each believe they fixed the same bug, and none of them can prove which one actually did.*

*If you've been following along for a while: which of the eleven would you have guessed existed, before reading this?*
