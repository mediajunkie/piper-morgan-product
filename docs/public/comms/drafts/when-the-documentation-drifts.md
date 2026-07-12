---
image: 'ai-tracks.png'
alt: 'Two trains on railroad tracks that begin together but slowly diverge into different directions, symbolizing documentation drifting away from code.'
caption: '"Headed my way?"'
---

# When the Documentation Drifts

*May 19–20, 2026*

The morning of May 20, an engineer on the project (Lead Developer, one of the role-named agents on the team) spent the first thirty-five minutes reverting work. A small skill that synced a manifest file across mailboxes had run during the previous day's session and done the job wrong. The skill's documentation said it would "append and reconcile." The code, when read carefully, was actually doing replace-with-overwrite, a much riskier maneuver if you make a mistake. Thirteen agent mailbox manifests had been wiped and would have to be restored from the last clean commit.

The error in the skill was an oversight. The docs were clear about the intent. The code was straightforward about what it actually did. The facts just didn't line up — and hadn't, for months.

This category of error was already tracked in the project's pattern catalog ("Documentation-Asserted Behavior Drift"), and it already had thirteen instances on file before this one.

# How the gap opens

How does this happen? We propose a skill, someone writes a memo describing what it'll do, and the language in the memo settles. The memo is read, reviewed, ratified, filed.

Sometime later, the engineer writing the code reads the memo, decides on an implementation strategy, and produces something intended to fit. The first pass usually adheres closely to the memo. The second pass, perhaps coming three weeks later, after a bug report, after a refactor for performance, after a related skill changes its expectations, might not.

The planning and the doing have no dynamic connection. Over months, they diverge. The divergence is silent because nobody reads the docs and the code side-by-side as a hobby. (Only a ruthless habit of scrubbing for stale information with every tracked decision even gets you close to keeping things aligned.)

Each source is consulted when its own purpose is in play. The docs get read when somebody's planning. The code gets run when somebody's working.

The drift surfaces when those two paths cross: when somebody working from the docs runs the code and gets a result the docs didn't predict.

# How asymmetry hides it

Traditionally, documentation was written and read by humans. Code is run by machines. Increasingly, machines are doing both.

It turns out that may not really matter or help much, due to the whole structure of the drift problem. Whoever is using the docs is doing planning work. They're forming a model of "what will happen" so they can decide whether and when to invoke the thing. When a machine runs the code, whatever happens happens. The model is gone. It's just execution now.

If the docs and the code agree, the planning produces a correct prediction of the execution. If they disagree, the planning produces an incorrect prediction. The incorrectness doesn't surface during planning — planning never touches the code. It surfaces at the moment of execution, which is also usually the moment when consequences land.

In our incident: somebody planned the work expecting the manifest sync to append. Somebody invoked the sync. The sync overwrote. Thirteen files lost. The planning surface had no signal that the model was wrong, because the planning surface only consults the docs. The execution surface had no signal that anyone was relying on the docs being right, because the execution surface only sees code.

That's the geometry of the problem.

# Why the cost is asymmetric too

Drift sneaks in cheaply. Every minor doc edit and every minor code edit risks introducing a tiny mismatch, and most of them never get noticed because nobody invokes the affected path under those specific conditions.

The cost piles up silently and then gets paid all at once when such a path is invoked. The cost is paid by the user of the moment, the person running the code with expectations based on the docs. They inherit the drift from whomever introduced it, perhaps weeks, months, or even years earlier, in a small unrelated change neither side noticed.

So the cost is asymmetric in time (paid much later than incurred) and asymmetric in person (paid by somebody other than the introducer). That asymmetry is why drift isn't caught at introduction: there's no immediate signal, and the introducer isn't there when the bill arrives.

# What the Piper Morgan pattern catalog does

Once we (when I say "we" I usually mean myself and this team of agent roles, in conversation) noticed this happening repeatedly, we named it. Pattern-073: Documentation-Asserted Behavior Drift. Naming something is a good place to start, but identifying a pattern alone doesn't prevent it from recurring. What naming does is help make the pattern recognizable, and helps make any accumulated wisdom about it findable.

When a drift incident lands, the recovery process now has a slot to file the incident into. The slot accumulates instances. The instances become a dataset. The dataset becomes input to discipline — *we know this happens — how often, where, what kinds of code, what kinds of docs, what's the average cost to recover?*

This one joined the file alongside the rest. This time, the recovery was structured: revert to clean state, restore the affected files, file a tracking issue for the underlying skill (so the next person who reaches for it sees the warning), file a methodology memo so the pattern catalog gets the data point.

The recovery took a while but not as long as it had the first time we ran into this problem. By now, the fix is muscle memory. The cost of recovery gets cheaper.

The drift itself still happens. It doesn't seem possible to prevent it on every level, at least not at scale. Cataloguing helpful and harmful patterns helps hold down the recovery cost and accumulate the data that will eventually (I hope!) inform prevention.

# What this changes about your docs

This is mostly about how you treat documentation when stakes are high.

**Code is the source of truth for what runs.** That sounds obvious, but it's easy to forget when the docs are well-written and recently-updated. Recently-updated docs aren't proof of currency. They're proof that *someone* recently thought about that surface. Whether their thinking matched the code is a separate question.

**Docs are only true until-proven-otherwise.** When you read a doc that describes behavior you're about to depend on, the doc tells you what *somebody intended* the behavior to be. Whether it *is* the behavior is a question only the code answers. If the stakes are low (a one-off, a sandbox), trust the doc and move on. If the stakes are high (production data, irreversible operation), verify against the code or against a small experimental invocation before depending on the assertion.

**Verify at the moment of invocation, not the moment of reading.** Reading the doc happens at planning time. Invoking the behavior happens later. The doc you read three weeks ago might have been current when you read it and stale by the time you invoke. The verify-step belongs adjacent to the invoke-step, not adjacent to the read-step.

None of this is novel discipline. It's the standard *trust but verify* posture applied to documentation specifically. The reason to make it explicit is that documentation feels authoritative in a way other claims don't. Documentation is a deliberate artifact. Somebody wrote it. Somebody filed it. Somebody read it. That cumulative deliberateness makes it feel like reliable signal — and most of the time it is, which is what makes the gap dangerous when it opens.

# In my humble operation...

Deep down this is more about architectural humility than documentation hygiene.

We are bad at keeping two things in sync over time. We are bad at it as individuals, bad at it as teams, bad at it as projects with reasonable governance. The instinct is to declare a rigorous goal — *we'll keep docs in sync with code!* — and then trust discipline or will power to make it so. This was rarely if ever true when we were relying on humans to double-check everything every time, and it flat-out doesn't work with today's AI agents, which confidently declare that they should or will do better without taking any meaningful steps to change the behavioral pattern. But it's not even about how nobody's perfect. It's just that the editing pressures on the two surfaces (code and docs) are different and intermittent and asymmetric.

The architecture that acknowledges this can be anti-fragile. Code-as-source-of-truth is just an admission. Tests-as-executable-documentation is a recognition that the force that synchronizes docs with code reliable is when they fail to correctly describe the behavior of divergent code and it becomes a problem.

# What might help

Wherever the project has information objects that need to stay in sync, they should be coupled mechanically, not relationally. That is, they should automatically derive one from the other, not assert a connection and hope they stay in touch.

Where mechanical coupling isn't feasible, your best bet is to *verify before depending* on anything. The documentation is a wish, not a contract. If it was ever true there's no way to know if it has drifted till you check. It's just the geometry of the situation connecting these two objects, and you're inside it whether you want to be or not.

---

*Next on Building Piper Morgan: "The Server Crashed Mid-Draft" — a new file sits in an untracked, unprotected window the moment it's written, and what it costs to forget that.*

*When has documentation drifted out from under you? How did you discover it — and how did the cost get paid? What discipline did you build to limit the next instance?*
