---
image:
alt:
caption:
---

# Stacked Silent Failures

*May 8–9, 2026*

A few weeks ago an automated quality test on my project's main system came back six points below its prior baseline. The system runs a hundred scripted user inputs against the production code, scores each response on a rubric (relevance, competence, tone), and produces an aggregate quality number. The number had been hovering around 72%. The new number was 65.6%.

The engineering role filed an investigation. The working hypothesis was the obvious one. *The model has started fabricating responses.* The last few weeks' worth of architectural changes — there had been a lot — had presumably introduced a regression somewhere in the response-generation pipeline. The auto-fail rule on the rubric (any single dimension scoring zero triggers a FAIL) had caught ten cases that looked like fabrications.

The investigation took an afternoon. By the time the report landed, the hypothesis was largely refuted, and the actual finding was more interesting than the hypothesis.

The six-point drop wasn't one regression. It was *three* silent failures, stacked, each of which would have looked like a non-problem in isolation.

The first failure was in the judge. The scoring rubric had drifted toward over-weighting a specific dimension — *user-context-specificity*, how closely the response referenced the specific user's specific recent activity. The drift had been gradual and the judge had been doing it for at least the prior several weeks. If you looked at the judge in isolation, nothing was broken. It was scoring along a slightly different axis than the team had thought it was scoring on.

The second failure was in the auto-fail rule. *Any dimension at zero produces a FAIL on the case.* The rule had been there for months. It was a critical guard — when responses are unambiguously bad on any axis, you want them flagged regardless of how good the other axes look. But in combination with the judge's drift toward user-context-specificity, the auto-fail rule started flipping borderline cases to FAIL whenever the response was generic-but-correct rather than user-specific-and-correct. The rule was correctly applied. The rule's interaction with the drifting judge was the problem.

The third failure was in the test fixture. The canonical test user had a database populated by prior runs of the test itself. Several test cases mutate state — *add a todo*, *create a project*, *log an entry* — and the test infrastructure had never cleaned up the mutations between runs. By May, the canonical user had fifteen real todos accumulated in the database. One of the failing test cases asked Piper to recap the user's recent activity. The response was a confident recap of the polluted state. From the outside it looked exactly like a fabrication. From the inside it was an accurate report of a contaminated reference.

Three failures, each silent in isolation. Together they produced one observed quality regression that none of them caused individually.

# Why this kept hiding

Each of the three failures had been latent for weeks. None of them screamed.

The judge's drift was silent because judges don't usually report what they're scoring along — they report a number. The number had a trendline. The trendline didn't show the drift, because the drift was in *what the number meant,* not in the number itself.

The auto-fail rule's amplification was silent because the rule was operating correctly per its own spec. *Any dim at zero → FAIL* doesn't have a wrong-answer state. It does what it says. The fact that it was now triggering on cases the team would not have called failures was a feature of the *composition* of the rule with the drifting judge, not of either piece alone.

The fixture pollution was silent because the database was working. Reads returned the data. Writes persisted. No error. No exception. The contamination only became legible when someone went looking for *why this test produced a confident-sounding wrong-shape answer.*

The hypothesis the team started with — *the LLM is fabricating* — wasn't wrong about the surface symptom. It was wrong about what kind of failure surface it was. *Fabrication* names a single cause. The actual failure surface had three causes stacked, none of which was fabrication.

# Why "find the root cause" is sometimes the wrong move

Most debugging discipline is built around finding *the* root cause. *Five Whys* digs from symptom to cause by asking why the layer above happened. *Fishbone diagrams* organize possible causes into categories so you can pick the most likely branch. Both techniques implicitly assume that there's *one* cause down at the bottom of the dig, and the discipline is to keep going until you find it.

That's right when there's one cause. It's exactly wrong when there are several, each contributing partly, none individually screaming.

The diagnostic move that worked on the quality-regression case wasn't *dig deeper.* It was *enumerate breadth.* Instead of pursuing the LLM-fabrication hypothesis to its limit, the engineering role catalogued all of the failed cases and asked, for each, *what could be contributing to this not just looking right.* The list of contributing factors converged to three. Each factor was a reasonable explanation for part of the failure surface. None alone explained it.

Once the team saw the stack, the fixes came in three pieces. Reset the fixture. Recalibrate the judge. Tighten the auto-fail rule. Each fix was small. The aggregate fix moved the quality number from 65.6% back to 68.9%, above the prior baseline. The system wasn't broken. The measurement infrastructure had drifted into a configuration that *produced* the appearance of breakage.

# Recognizing the shape

If you're debugging something and you've found *a* cause but the fix doesn't move the metric as much as the surface symptom suggested it should, the shape is probably stacked silent failures.

Other signals:
- The surface symptom is suspiciously dramatic but the diagnostic feels thin.
- You find a real bug, fix it, and the metric improves a little but not as much as you expected.
- Multiple plausible explanations are sitting in your investigation notes, and you've been treating them as alternatives rather than as possibly simultaneous.
- The system was working a few weeks ago and "nothing big changed."

When you see those signals, the right discipline isn't to dig further on the cause you've already found. It's to *enumerate everything that could be contributing*, set each against the failure surface, and ask which combination explains what you're seeing. If the answer is *all three,* fix all three.

The deeper observation is that complex systems fail more often by composition than by single-cause. The vocabulary of root cause has been useful and will keep being useful, but it tends to bias the diagnostic toward depth when sometimes the right axis is breadth. A second discipline — *find all the contributing latent failures, including the ones that have been silent for weeks* — is the one that catches the stacked case.

---

*Next on Building Piper Morgan: [TEASE PENDING — confirm next-scheduled-item at calendar update].*

*When have you found the "real" root cause of a problem and discovered the fix didn't move the metric? What else was contributing that you only noticed after?*

[FACT-CHECK NOTE for PM: Sources verified against May 8 + May 9 omnibus logs + Pattern-066 (Stacked Silent Failures) entry filed by CIO Pattern Sweep 2.0 May 9. Specific facts: May 8 retest Run-4 Quality 65.6% vs prior baseline; #1064 P0 floor-fabrication-investigation finds 0 of 10 auto-fails pure fabrication, 7 false flags from judge-calibration drift + auto-fail rule amplification + fixture pollution; Q56 smoking gun = 15 real todos in DB from prior runs. Recovery May 9: fixture reset + rubric recalibration + 3 narrow fixes → Run 7 Quality 68.9% PASS exceeds Apr 12 baseline. Pattern-066 (Stacked Silent Failures) filed Emerging by CIO May 9 per Pattern Sweep 2.0 (Apr 26 → May 9 cycle, first 4-phase invocation, 6 anti-pattern entries indexed + Pattern-066 + Pattern-024 status correction). The three-failure-stack framing matches the May 8 omnibus Core Themes #1 ("SYSTEMIC cause: judge over-weights user-context-specificity × auto-fail rule amplifies miscalibration + fixture pollution from prior runs").]

