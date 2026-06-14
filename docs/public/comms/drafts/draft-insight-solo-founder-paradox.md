---
image:
alt:
caption:
---

# The Solo Founder Paradox

*February 15, 2026*

I was home with the flu. Day six. The project was going fine. Agents had been running sessions, closing issues, pushing code. My Chief of Staff had synthesized the week's progress. The architecture was holding. The cathedral was being built without me shouting through a bullhorn every day.

So I had some time to think.

You know, I hadn't had a flu, not this type of two-week crud anyhow, since before Covid. I forgot what it was like to be sidelined physically and cognitively. It kind of forced a full-system reboot.

What else? I had a podcast interview coming up. [Cindy Chastain's show](https://creators.spotify.com/pod/profile/this-moment-were-in/episodes/Building-Piper-Morgan-A-Product-Management-Experiment-in-Agentic-AI--Christian-Crumlish-e3h6f9r/a-acigfee), where I'd need to explain what I was building and why. My communication chief agent (Comms) and I worked through the narrative arc, and somewhere in that conversation, five strategic themes surfaced, and the first one really stuck:

**Solo founder paradox**: When agents handle execution, the human is the necessary bottleneck for matters of judgment and relationships. 

# The bottleneck shifted

Before (gestures vaguely) all of this, the bottleneck was execution. Like a lot of product and UX folk, I had ideas, designs, architectural opinions galore, but rarely anyone interested in helping me implement them. Suddenly agentic AI offered to solve all that. Over time I accumulated a Lead Developer, a Chief Architect, a Chief of Staff, a Documentation specialist, and so on, now up to something like 11 active agents. (Seven leadership roles, and four "task oriented" roles.) They write code, review architecture, draft blog posts, synthesize workstreams. You name it.

The execution capacity of my "team" now exceeds anything a solo founder could traditionally access. On busy days all 11 agent roles are active, along with subagents and the occasional singleton specialist.

But the bottleneck didn't disappear. It moved.

I'm still the only one who can have coffee with Ted Nadeau and understand what he's really saying about the architecture. I'm still the only one who can read the room if Michelle logs in as an alpha tester and something doesn't work. I'm still the only one who can decide that the floor inversion diagnosis is right, that the principal product manager (PPM) agent's synthesis accurately captures the chief architect (Arch)'s intent, that the chief experience officer (CXO)'s voice guidance is faithful to how I want Piper to sound.

Judgment. Taste. Relationships. Things you can't really delegate.

# What scales and what doesn't

The agent team scales beautifully for structured work. Give the Lead Developer an issue with clear acceptance criteria and they'll audit, implement, test, and document it — often in a single session. Give the Communications Director omnibus logs and they'll produce narrative drafts that need your editing pass but not your research time.

What doesn't scale is anything that requires sensing the context that isn't in the documents. Alpha testers have feelings that don't appear in bug reports. Advisors have opinions they share over dinner that never become memos. Your own instinct about whether a feature *feels* right can't be extracted into acceptance criteria — or at least, I haven't figured out how.

The Agent 360 questionnaire my head of sapient trust (HOST - a sort of HR lead for my agents and human relationships with alpha testers, advisors, future staff potentially) circulates every few months recently surfaced this same concept from the point of view of the agent experience. Agents cited "PM-as-mailbot latency" as a friction point. (I'm "the PM" for most of them, since my initial role on this project was "PM looking for AI engineer".) 

They were waiting for me to route messages, relay context, make judgment calls. My attention was the throughput limiter, not their capability.

Recently, the automated duty cycle has made me less of a "dumb bottleneck," enabling multi-agent conversations, debates, decisions, and proposals to move forward without me slowing them down.

# The uncomfortable math

I can and do run ten or more agent sessions in a day. Each session produces real work — code, documents, decisions. We make progress on the roadmap. MVP and the beta release come ever closer. The agents are never tired, never distracted, never in a bad mood. (Well, hardly ever.)

But each session also consumes my attention. Reading the output. Making the judgment calls. Ratifying the decisions. Deciding what's right and what needs revision. Ten sessions means ten context switches, ten sets of decisions, ten moments where the work pauses until I weigh in.

My own cognitive bottleneck is no longer wasted on rubberstamping mechanical processes, but it still gets full. There's a ceiling. Not on what the agents can produce, but on what I can absorb, evaluate, and direct. And that ceiling is lower than the agents' capacity.

The next frontier is relying on my chief of staff to coordinate the team and my assistant (Piper Alpha) to organize my work.

As usual, none of this is new. All of this resembles the human dynamics it was trained on. Traditional management and delegation grapples with the "span of control" problem: how many direct reports can a manager effectively handle? 

Is the AI version different because agents don't need motivation and career development, or is it the same because the judgment bottleneck is the same?

# What I'm trying instead

Four partial solutions (and counting), none complete:

**The mailbox system.** Instead of being the real-time router for every inter-agent message, I built structured mailboxes, initially requiring a lot of manual delivery on my part but now with delivery automation, which required migrating all of my leadership roles from Claude Chat to Claude Code (where up to then only the "doers" had been operating). Agents write memos with explicit recipients. The system handles routing. I handle exceptions. This doesn't eliminate the judgment bottleneck — I still approve the important decisions — but it removes me from the mechanical relay work.

**The cross-pollination process.** Instead of manually carrying insights between Piper, Klatch, and my other projects, I built an automated intelligence sweep. An agent who functions as the majordomo for my [Design in Product](https://designinproduct.com) operation (Janus) reads a set of project repos daily and publishes a [cross-pollination briefing](https://designinproduct.com/internal/) identifying any innovative work other agents might be able to learn from and apply to their own projects. My judgment is encoded in the system design — what counts as relevant, what format the briefs should take — rather than exercised on every individual insight.

**The contextual architecture.** Instead of orienting each new agent session personally as I used to have to do, I've evolved a system (or "harness" I guess I am supposed to call it) of briefing documents, handoff memos, and current-state references. The goal: any agent should be able to start a session and know what's happening without my narrating it.

**The duty cycle.** My chief innovation officer (CIO) and I have implemented, and continue to iterate on, an automated daily START > WORK > STOP cycle that ensure they maintain their session logs, check for new messages, and work on unblocked tasks whenever possible, saving up anything they are blocked on, want to discuss, or otherwise need to bring to my attention. My Chief of Staff agent (Exec) rolls up all the attention queues into a single html "dashboard" for my attention so I can get a quick briefing on anything I need to decide on, or otherwise unblock, when I have the time.

Each of these constructs converts one-time judgment into reusable infrastructure. None of them eliminates the need for judgment entirely. The paradox doesn't ever resolve (paradoxes don't do that, they just sit there, pulsing), but things do get more efficient, and it becomes more clear to me where and when I want to spend my scarce attention and what my own limits are.

# The underlying issue

The solo founder paradox isn't really about AI. It's about what happens when your execution capacity exceeds your judgment capacity. Traditional founders hit this when they hire faster than they can manage. AI-augmented founders hit it when their agents produce faster than they can evaluate.

The answer, in both cases, is probably the same: you have to learn to delegate judgment, not just execution. That's harder. It requires trusting systems — human or AI — with decisions you'd rather make yourself.

I'm not there yet. But the architecture is pointing in that direction.

---

_Next on Building Piper Morgan: First Subagent in Production — when the first production subagent ran, the methodology held at every layer it was supposed to. The deployment surfaced the layer that wasn't._

_If your tools could do ten times as much work, would you be ten times as productive — or would you just hit a different ceiling? What would that ceiling be?_
