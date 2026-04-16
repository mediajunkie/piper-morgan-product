# The Migration

*March 28–30*

Friday. Day off. The project had been idle for three days — partly intentional rest after the closing sprint, partly involuntary. Anthropic's service disruptions mid-week had killed a Documentation session on Thursday, stranding commits on a local branch nobody could see. Work was scattered: some pushed, some stashed, some sitting in a chat window that no longer existed.

[ADD PERSONAL DETAIL — what the disruption felt like, the frustration of lost productivity vs the enforced pause]

Saturday evening, I opened a session to assess the damage.

## Recovery

The first task was archaeology. A four-day gap in documentation — no omnibus logs for March 25 through 28, no session logs filed, mail undelivered, blog drafts sitting in a downloads folder instead of the repository. The Documentation agent pulled 46 stranded objects from my local machine. Seven session logs. Six blog drafts. Four cross-pollination briefs. Routed mail items.

There was a git stash from Thursday that contained real work — a narrative verification skill, briefing updates, a roadmap revision. But the briefings in the stash were based on March 10 data, already superseded by March 24 versions. Surgical recovery: accept new files, reject stale modifications. `git stash branch stash-recovery`, selective checkout, delete the branch.

By 10:15 PM, the first blog post had been published directly to pipermorgan.ai — "Discovery Is the Bottleneck," the first piece to appear on our own site before syndication to Medium. The canonical home for new content was no longer someone else's platform.

[CONSIDER — whether the blog-first milestone deserves more emphasis here or whether it's better as a detail in a larger story]

## The big day

Monday morning. The real migration.

I'd hit a usage limit on the account where all twelve agent roles lived. Rather than wait it out, I decided to move everything — every role, every chat, every piece of accumulated context — to a new account on a different machine.

Twelve roles. Each one with weeks or months of conversation history, working patterns, and institutional knowledge that existed only in the context of its chat session. The question was whether any of that could survive a migration, or whether we'd be starting from scratch with twelve blank slates.

[ADD PERSONAL DETAIL — the decision to migrate rather than wait, what that felt like as a risk calculation]

The plan: each role writes a workstream review memo covering the last week, then a comprehensive handoff document for its successor. The successor opens in the new project, reads the handoff, and picks up where the predecessor left off.

Morning wave: six roles delivered workstream memos and handoff documents before noon. CIO, PPM, CXO, Architect, HOST, Communications — each one independently summarizing its recent work, documenting its current state, and writing advice for the next instance.

Afternoon wave: eight successor sessions opened in the new project. Each read its predecessor's handoff, absorbed the essential briefing, and confirmed orientation. The Chief of Staff synthesized all six workstream memos into Ship #036 — "Approaching the Gate."

Meanwhile, the new PA — Piper Alpha, the project's first dedicated PM assistant — ran its inaugural session. Eight hours of institutional knowledge acquisition. Sixty ADRs read. Forty-seven patterns absorbed. Fifteen omnibus logs reviewed. A morning standup delivered and approved. Introduction memos sent. By the end of the day, a role that hadn't existed 24 hours earlier was triaging issues and reviewing pull requests.

[ADD PERSONAL DETAIL — watching PA come online, what it felt like to see a new agent absorb months of project context in one session]

And in the background, the Documentation agent was quietly fixing the blog. Four missing posts added. Two hundred and thirteen image references updated. Date formats normalized across 275 entries. A broken episode system — fifteen categories defined, zero posts matched, nobody had noticed — replaced with a simpler five-era model that actually worked.

## Eighteen sessions

By the end of Monday, eighteen sessions had run across twelve roles. Twenty-two commits to the product repository. Six to the website. Eight handoff memos written and consumed. Six workstream memos synthesized into a weekly ship. A new section of the website built. A new agent role operational.

Zero coordination loss.

[CONSIDER — is "zero coordination loss" the right framing? Were there things that didn't transfer?]

The handoff memos were the load-bearing structure. Each predecessor wrote down not just what it had been working on, but how it worked — the cadence, the preferences, the things that had gone wrong, the advice it would give its successor. The CXO flagged a stale briefing. The Communications Director documented an undocumented publication cadence. The HOST noted that alpha testers hadn't responded in sixteen days.

None of this was automated. I routed every memo by hand, opened every successor session manually, confirmed each orientation one at a time. The coordination overhead was real. But the alternative — twelve roles starting cold with no context — would have cost far more.

[ADD PERSONAL DETAIL — reflection on the manual overhead, whether it's sustainable, what it says about the project's coordination model]

The migration worked because the project had spent months building the infrastructure that made it possible: session logs, omnibus logs, briefing documents, mailbox protocols, workstream review templates. Documentation as institutional memory. When the physical infrastructure changed — different account, different machine, different chat sessions — the knowledge infrastructure carried everything across.

---

*Next on Building Piper Morgan: The Gate — when six thousand tests pass and zero users agree.*

*Have you ever had to move a running system to new infrastructure without stopping it?*
