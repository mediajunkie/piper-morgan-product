# The Migration

<!-- image: 'ai-migration.png' -->
<!-- alt: 'A human guides a line of small AI helpers carrying boxes from a cluttered room into a clean one through a central doorway.' -->
<!-- caption: '"Time to unpack!"' -->

*March 28–30*

Friday. Day off. The project had been idle for three days — partly intentional rest after the closing sprint, partly involuntary. Anthropic's service disruptions mid-week had killed a Documentation session on Thursday, stranding commits on a local branch nobody could see. Work was scattered: some pushed, some stashed, some sitting in a chat window that no longer existed.

Also, my projects were proliferating along with my Claude accounts and they were overdue for consolidation.

Saturday evening, I opened a session to assess the damage.

# Recovery

The first task was archaeology. A four-day gap in documentation — no omnibus logs for March 25 through 28, no session logs filed, mail undelivered, blog drafts sitting in a downloads folder instead of the repository. The Documentation agent pulled 46 stranded objects from my local machine. Seven session logs. Six blog drafts. Four cross-pollination briefs. Routed mail items.

There was a git stash from Thursday that contained real work — a narrative verification skill, briefing updates, a roadmap revision. But the briefings in the stash were based on March 10 data, already superseded by March 24 versions. Surgical recovery: accept new files, reject stale modifications. `git stash branch stash-recovery`, selective checkout, delete the branch.

By 10:15 PM, the first blog post had been published directly to pipermorgan.ai — "Discovery Is the Bottleneck," the first piece to appear on our own site before syndication to Medium. The canonical home for new content was no longer someone else's platform.

# The big day

Early Monday morning. The real migration.

I was going to deprecate the account where all twelve agent roles lived. Rather than put it off any longer, I decided to move everything — every role, every chat, every piece of accumulated context — to a different account on a different machine.

Multiple roles, each one with weeks or months of conversation history, working patterns, and institutional knowledge that existed only in the context of its chat session. The question was how much of that could survive a migration, or whether we'd be starting from scratch with twelve blank slates.

The plan: each role writes the (overdue) workstream review memo covering the last week (ending on Thursday), and then a comprehensive handoff document for its successor. The successor opens in the new project, reads the handoff, and picks up where the predecessor left off.

Morning wave: the six "leadership" chat roles delivered workstream memos and handoff documents before noon. CIO, PPM, CXO, Architect, HOST, Communications — each one independently summarizing its recent work, documenting its current state, and writing advice for the next instance. My Chief of Staff wrote their own handoff.

Afternoon wave: seven successor sessions opened in the new project. Each read its predecessor's handoff, absorbed the essential briefing, and confirmed orientation. The Chief of Staff synthesized all six workstream memos into Ship #036 — "Approaching the Gate."

Meanwhile, the newest role — Piper Alpha, the project's first dedicated PM assistant, whose briefing we had been developing for the past week — ran its inaugural session. Eight hours of institutional knowledge acquisition. Sixty ADRs read. Forty-seven patterns absorbed. Fifteen omnibus logs reviewed. A morning standup delivered and approved. Introduction memos sent. By the end of the day, a role that hadn't existed 24 hours earlier was triaging issues and reviewing pull requests.

Piper's role is to act as if they are Piper Morgan. This provides me with two things: (1) an immediate assistant, at least for this project, without waiting for Piper M to hit beta, and (2) a benchmark for my own product. If after ten months of development Piper Morgan performs no better than Piper Alpha, then - well - I might need to do some reconsidering!

An interesting thing about this project is how the methodology often seems to be its most valuable point. Piper A follows the methodology and thus is already more than halfway to *being* Piper M. Seeing the agent get up to speed and start delivering real, valuable, assistance to me was pretty thrilling!

# Meanwhile, back at the...

And in the background, the Documentation agent was quietly fixing the blog. Four missing posts added. Two hundred and thirteen image references updated. Date formats normalized across 275 entries. A broken episode system — fifteen categories defined, zero posts matched, nobody had noticed — replaced with a simpler five-era model that actually worked.

By the end of Monday, eighteen sessions had run across multiple roles. Twenty-two commits to the product repository. Six to the website. Eight handoff memos written and consumed. Six workstream memos synthesized into a weekly ship. A new section of the website built. A new agent role operational.

Zero coordination loss, as far as I could tell!

The handoff memos were the load-bearing structure. Each predecessor wrote down not just what it had been working on, but how it worked — the cadence, the preferences, the things that had gone wrong, the advice it would give its successor. The CXO flagged a stale briefing. The Communications Director documented an undocumented publication cadence. The HOST noted that alpha testers hadn't responded in sixteen days.

None of this was automated. I routed every memo by hand, opened every successor session manually, confirmed each orientation one at a time. The coordination overhead was real. But the alternative — numerous mission-critical roles starting cold with no context — would have cost far more.

Getting me out of the postal delivery business is a real goal, but for the time being the manual overhead is manageable.

The migration worked because the project had spent months building the infrastructure that made it possible: session logs, omnibus logs, briefing documents, mailbox protocols, workstream review templates. Documentation as institutional memory. When the physical infrastructure changed — different account, different machine, different chat sessions — the knowledge infrastructure carried everything across.

---

*Next on Building Piper Morgan: The Gate — when six thousand tests pass and zero users agree.*

*Have you ever had to move a running system to new infrastructure without stopping it?*
