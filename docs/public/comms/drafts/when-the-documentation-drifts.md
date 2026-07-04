---
image:
alt:
caption:
---

# When the Documentation Drifts

*May 19–20, 2026*

The morning of May 20, an engineer on the project (Lead Developer, one of the role-named agents on the team) spent the first thirty-five minutes reverting work. A small utility — a skill that synced a manifest file across mailboxes — had run during the previous day's session and done the wrong thing. The skill's documentation said it would append and reconcile. The code, when read carefully, was actually doing replace-with-overwrite. Thirteen mailbox manifests had been wiped and would have to be restored from the last clean commit.

The skill wasn't malicious. Nobody wrote it to be destructive. The docs were honest about the intent. The code was honest about what it did. The honesty just didn't line up — and hadn't, for months.

[FACT-CHECK NOTE for PM: I have the recovery cost at ~35 min from the May 20 Lead Dev log. Confirm if you want a different framing or precision.]

This is a category in our project's pattern catalog. We call it Documentation-Asserted Behavior Drift. The May 19 incident was instance #14.

[FACT-CHECK NOTE for PM: instance count 14 per memory of the log entry. Confirm.]

# How the gap opens

Documentation gets edited when behavior gets *discussed*. Someone proposes a skill, writes a memo describing what it'll do, and the language in the memo settles. The memo gets read, ratified, filed.

Code gets edited when behavior gets *implemented*. The engineer writing the code reads the memo, decides on an implementation strategy, and produces code that fits the surface area. The first pass usually matches the memo. The second pass — three weeks later, after a bug report, after a refactor for performance, after a related skill changes its expectations — might not.

These two editing surfaces don't share a clock. Each gets touched on its own schedule. A change to one doesn't automatically prompt a change to the other. And the people who touch each surface often aren't the same people, or aren't thinking about the other surface when they make the touch.

Over months, the two diverge. The diverge is silent because nobody reads the docs and the code side-by-side as a hobby. Each surface is consulted when its own purpose is in play. The docs get read when somebody's planning. The code gets run when somebody's working.

The drift surfaces when those two paths cross — when somebody planning from the docs runs the code and gets a result the docs didn't predict.

# The asymmetry that hides it

Documentation is read by humans. Code is run by machines.

That asymmetry is so familiar it disappears. But it's the whole structure of the drift problem. Humans reading docs are doing planning work. They're forming a model of what will happen so they can decide whether and when to invoke the thing. Machines running code are doing the actual happen. They don't form a model. They just execute.

If the docs and the code agree, the planning produces a correct prediction of the execution. If they disagree, the planning produces an incorrect prediction. The incorrectness doesn't surface during planning — planning never touches the code. It surfaces at the moment of execution, which is also usually the moment when consequences land.

In our incident: somebody planned the work expecting the manifest sync to append. Somebody invoked the sync. The sync overwrote. Thirteen files lost. The planning surface had no signal that the model was wrong, because the planning surface only consults the docs. The execution surface had no signal that anyone was relying on the docs being right, because the execution surface only sees code.

That's not negligence on either side. That's the geometry of the problem.

# Why the cost is asymmetric too

The cost shape matches the visibility shape. Drift is cheap to introduce — every minor doc edit and every minor code edit risks introducing a tiny mismatch, and most of them never get noticed because nobody invokes the affected path under those specific conditions.

The cost gets paid when the path is invoked. And the cost is paid by the user of the moment — the person running the code based on docs they read. That person didn't introduce the drift. The drift was probably introduced by somebody else, weeks or months earlier, in a small unrelated change neither side noticed.

So the cost is asymmetric in time (paid much later than incurred) and asymmetric in person (paid by somebody other than the introducer). That asymmetry is why drift isn't caught at introduction: there's no immediate signal, and the introducer isn't there when the bill arrives.

# What the pattern catalog does

Once we noticed this happening repeatedly, we named it. Pattern-073: Documentation-Asserted Behavior Drift. The naming was the first useful move.

Naming a pattern doesn't prevent it. What naming does is make it findable. When a drift incident lands, the recovery process now has a slot to file the incident into. The slot accumulates instances. The instances become a dataset. The dataset becomes input to discipline — *we know this happens — how often, where, what kinds of code, what kinds of docs, what's the average cost to recover?*

The May 20 incident was instance #14. By the time it landed, the recovery was structured: revert to clean state, restore the affected files, file a tracking issue for the underlying skill (so the next person who reaches for it sees the warning), file a methodology memo so the pattern catalog gets the data point.

The recovery was thirty-five minutes. The same incident at instance #1 might have taken hours, partly because the response would have had to invent itself. By instance #14, the response is muscle memory. The cost compounds toward zero as the pattern matures.

The drift itself still happens. The catalog doesn't prevent the introduction. What the catalog does is collapse the recovery cost and accumulate the data that will eventually inform prevention.

# What changes about how you read docs

The discipline that comes out of this is mostly about how you treat documentation when stakes are high.

**Code is the source of truth for what runs.** That sounds obvious, but it's easy to forget when the docs are well-written and recently-updated. Recently-updated docs aren't proof of currency. They're proof that *someone* recently thought about that surface. Whether their thinking matched the code is a separate question.

**Docs are until-proven-otherwise.** When you read a doc that describes behavior you're about to depend on, the doc tells you what *somebody intended* the behavior to be. Whether it *is* the behavior is a question only the code answers. If the stakes are low (a one-off, a sandbox), trust the doc and move on. If the stakes are high (production data, irreversible operation), verify against the code or against a small experimental invocation before depending on the assertion.

**Verify at the moment of invocation, not the moment of reading.** Reading the doc happens at planning time. Invoking the behavior happens later. The doc you read three weeks ago might have been current when you read it and stale by the time you invoke. The verify-step belongs adjacent to the invoke-step, not adjacent to the read-step.

None of this is novel discipline. It's the standard *trust but verify* posture applied to documentation specifically. The reason to make it explicit is that documentation feels authoritative in a way other claims don't. Documentation is a deliberate artifact. Somebody wrote it. Somebody filed it. Somebody read it. That cumulative deliberateness makes it feel like reliable signal — and most of the time it is, which is what makes the gap dangerous when it opens.

# The deeper read

The deeper read on this isn't a documentation-hygiene problem. It's an architectural-humility problem.

We are bad at keeping two surfaces in sync over time. We are bad at it as individuals, bad at it as teams, bad at it as projects with reasonable governance. The instinct is to declare a discipline — *we'll keep docs in sync with code* — and assume the discipline will hold. It won't, because the editing pressures on the two surfaces are different and intermittent and asymmetric.

The architecture that survives this acknowledges it. Code-as-source-of-truth isn't a slogan — it's an admission. Tests-as-executable-documentation isn't a productivity hack — it's a recognition that the only docs that stay in sync are docs that fail when the code diverges. Wherever the project has surfaces that need to stay in sync, the surfaces should be coupled mechanically, not relationally.

Where mechanical coupling isn't possible — where the documentation is genuinely a separate surface from the code, like memos describing intent — the discipline shifts to *verify before depending*. Not because the documentation is untrustworthy. Because the geometry of two-surface drift is, and you're inside it whether you want to be or not.

Thirteen mailbox manifests, thirty-five minutes of recovery, one instance among fourteen. The cost paid by the engineer who showed up Sunday morning expecting to do something else.

---

*Next on Building Piper Morgan: "The Server Crashed Mid-Draft" — a new file sits in an untracked, unprotected window the moment it's written, and what it costs to forget that.*

*When has documentation drifted out from under you? How did you discover it — and how did the cost get paid? What discipline did you build to limit the next instance?*
