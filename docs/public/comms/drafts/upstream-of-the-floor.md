---
image: 'ai-dam.png'
alt: 'A newly built floodgate stands across a nearly dry river channel while most of the river flows down an unnoticed branch upstream, as workers realize the water has been bypassing their structure all along.'
caption: 'Good news! the floodgate works...'
---

# Upstream of the Floor

*April 25–28, 2026*

Late Friday afternoon, Lead Dev caught a problem that was about to ruin the next two days of work.

The plan had been to run Phase E of an ethics-floor activation that had been weeks in the making. The floor itself was code that would catch a small set of disallowed interactions — harassment language, certain categories of unsafe request — and route them to a designed-for-the-purpose response handler instead of through normal response generation. The build had moved through phases A through D over the prior weeks. Phase E was the live test: real model calls against scripted scenarios, scored by two reviewers, checked against a rubric.

At 4:32 PM Lead Dev posted a STOP CONDITION FOUND. The server process running the system locally had PID 98441 and had been running since April 16. That date predates Phases A, B, and C of the floor build. Whatever was running in memory wasn't the floor we'd just spent weeks shipping. If Lead Dev had run Phase E against that server, the gate would have passed against pre-floor behavior, and the false signal would have propagated through scoring, through the product-management and experience-design review (PPM and CXO), and into the Phase F authorization decision.

The check was procedural. `ps` to verify server age. Cross-reference against commit timestamps. Recognize that the in-memory code didn't match the on-disk code. The whole catch took maybe a minute. I authorized the restart, Lead Dev ran the real Phase E that evening, and Scenario 1 surfaced a finding none of us had expected.

The Scenario 1 input was harassment language — exactly the input the floor was built to catch. The floor never saw it. The pre-classifier — a much older piece of infrastructure that runs before the ethics layer to route inputs to canonical handlers — matched a keyword inside the harassment string and dispatched it to a normal handler. The floor was correct. The floor was unreachable from where the harassment input actually landed.

PPM filed the framing in a memo overnight: *the audit-shape question, not the build-quality question.* Phases A through D had asked the right question about whether the floor responded correctly. None of them had asked whether the input would arrive at the floor in the first place. The build had passed every test that tested it. The system had a defect that no test in the suite was designed to find.

# The reframe

That's the technical finding. The methodological finding came over the next 36 hours.

Architect's first reading of the bug was to add a defensive layer — wrap the floor with a check that intercepted misrouted inputs and reran them through ethics. Three hours later Architect filed a different memo: *ethics is upstream, not adjacent.* The right fix wasn't a defensive layer at the floor. It was a detector at the input stage, before any classifier got a chance to route. Ethics IS the upstream check.

That reframe is what unlocked the rest of the week. The Sunday work was a contract: a precise schema for what the upstream detector should look at, what it should return, what guarantees it had to maintain. CXO pre-authored a prompt body. CXO contributed a probe set covering edge categories, plus a five-pillar extension that arrived while implementation was already underway and slotted in without ceremony. Architect's contract design was already detailed enough that the build phase compressed three-day estimates into a single Monday session. By Monday afternoon Lead Dev had shipped the upstream-detector fix — six calendar days end-to-end from the filing of the bug.

Six days is fast for what landed. The reason it was fast is recognizable. The contract was specific enough that the build was mechanical. Cross-role artifacts pre-staged the work that would have been blocking. None of this is a story about heroic effort. It's a story about how much faster things ship when the upstream reframe arrives first.

# A different cascade

While the ethics arc was unspooling over the weekend, a different upstream-vs-downstream problem hit the mail.

Saturday afternoon, the Chief of Staff filed the kickoff memo for the next Weekly Ship. The kickoff went to all the leadership inboxes. CXO couldn't see it.

Docs's first diagnosis was that CXO's worktree was behind — pull origin, the kickoff would land. That diagnosis turned out to be wrong. CXO came back with the right one: the kickoff memo lived only on the Chief of Staff's feature branch and had never been merged to the trunk where the inboxes lived. CXO was correctly looking at a correctly-up-to-date trunk where the memo simply didn't exist.

Then Docs's investigation compounded the problem. The Bash subshell Docs was using had silently drifted into the Chief of Staff's worktree from an earlier command. So when Docs checked the send mirror, the listing came back showing the kickoff there — but in the wrong worktree's view of the filesystem. The kickoff existed on Chief of Staff's branch (which Docs was unknowingly looking at) and was missing from main (which Docs thought it was looking at). Several minutes of confused diagnosis followed. I was watching this in realtime and literally told my agents we were working my last nerve.

By 4:30 PM Docs had landed the fix. A targeted-enforcement version of a mailbox-discipline norm: a hook that blocks commits to `mailboxes/` when the current branch isn't main. A short CLAUDE.md section explaining the rule. A leadership memo announcing it. The whole thing took thirty minutes from the moment the cascade was clearly understood.

The interesting detail is that there had already been a hook that was supposed to enforce branch discipline. The earlier version blocked all non-main commits — too strict to be enforceable. Agents had been bypassing it silently for weeks by committing to feature branches without triggering it. The targeted version that landed Saturday afternoon was narrower in scope and consequential when it fired. **Targeted enforcement ships. Blanket enforcement fails silently.**

# What the two arcs share

The technical reframe ("ethics is upstream") and the mail-cascade reframe ("targeted enforcement, not blanket") sound like different lessons. They aren't.

Both are stories about where to look when a problem manifests. The floor-bypass looked like a defect in the floor. The mail-cascade looked like a worktree synchronization problem. In both cases the symptom was at the downstream layer where the user (or the agent) experienced it. In both cases the fix had to land one or two layers upstream of where the symptom showed.

The discipline that landed across both arcs is the same: *don't fix the symptom layer. Find the layer where the assumption broke and fix that one.* For the floor, the broken assumption was "all inputs reach the ethics layer" — fixed by making ethics upstream of the classifier instead of adjacent to it. For the mail, the broken assumption was "the rule that fires on every commit will be followed" — fixed by making the rule fire only on the commits that actually mattered, with a message explaining the fix.

By Monday evening the floor was activated behind a calibration window. By Sunday morning the mail discipline had passed its first real test — a leadership memo I sent landed cleanly in seven inboxes. Both fixes have held since.

The compound effect was the more interesting payoff. Both arcs unblocked work that had been waiting on them. The methodology codification that had been queued for weeks landed in twenty-four hours that Monday — three new patterns, two methodologies, an architecture decision record, a refreshed rubric. Each piece had been waiting for its upstream blocker to clear. None of them were big once the blocker was upstream of where it had been.

# What's portable

Most of what looks like a defect at the layer where you find it is a defect somewhere earlier. The instinct to add a defensive layer where the problem manifests is almost always wrong. The right move is to ask where the assumption that made this manifest possible was made — and to fix it there.

The cost of finding the upstream layer is usually a couple of hours of confused diagnosis. The cost of *not* finding it is a defensive layer that holds for a while and then breaks when something else routes around it. Six days from a P0 bug filing to the upstream fix shipping isn't fast because the team worked hard. It's fast because the second day's reframe meant the work was happening upstream of the wrong place to do it.

---

*Next on Building Piper Morgan: Be Prepared — why the work that looks like throat-clearing is often the work that mattered.*

*Where in your work has a downstream fix been holding together a problem that wanted to be solved one layer up? What would the upstream version look like?*



