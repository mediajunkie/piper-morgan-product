# The 81% Session

*March 12*

The M1 sprint kicked off on a Thursday evening. The Lead Developer loaded the PPM's sprint plan memo, opened issue #884 — canonical query retest — and ran the test harness against sixty-one standard queries.

First run: sixteen passed. Twenty-six percent.

That's a gut-check number. After shipping M0 with six thousand passing tests, after the careful retrospective and the deliberate pause, we were looking at a classifier that apparently failed three-quarters of the time. Something was very wrong.

Or so it seemed.

The Lead Developer investigated. The first discovery: fresh user accounts were getting trapped in onboarding. Piper detected a new user, initiated the portfolio onboarding flow, and then every subsequent query got captured by that flow instead of routing to its proper handler. Seventy-three percent of test failures weren't classifier failures — they were onboarding hijacking everything.

Seed some project data to bypass onboarding. Run again.

Second run: twenty-nine passed. Forty-seven percent. Better, but still not good.

More investigation. This time the culprit was `/standup`. Query forty-nine triggered the standup workflow, and the test harness was sharing a session ID across all queries. So once the standup started, every subsequent query got captured by the active workflow. Another hijack, different mechanism.

The Lead Developer traced the analysis handler with Serena (our symbolic reasoning tool). The handler existed — `handle_analysis_intent()` was right there in the code. But the corresponding method in OrchestrationEngine? Never wired. The function existed at one layer and didn't exist at the layer that calls it.

This was the 75% Pattern again. Infrastructure built. Interface defined. Connection never completed. Tests don't catch it because mocks hide the gap.

Fix the wiring: analysis handler, create_issue adapter, GitHub auth user_id threading (ten call sites), is_configured patterns (seven more call sites).

Third run: thirty-nine passed. Sixty-four percent.

Fourth run: forty-three passed. Implementation pass rate: eighty-one percent.

From 26.2% to 81.1% in a single session. Not by improving the AI. Not by retraining classifiers or tweaking prompts. By connecting things that should have been connected.

---

Here's what the 81% session taught us:

Most of our failures weren't intelligence failures. They were wiring failures. The classifier knew what the user wanted. The handler existed to fulfill it. But somewhere between classification and execution, a cable was missing.

This is the Assembly Assumption appearing in M1, exactly as the retrospective predicted. The same pattern that expanded M0 from seven issues to twenty-seven was waiting in the new sprint, wearing different clothes. Onboarding hijacking queries. Standup capturing sessions. Handlers that exist but aren't connected to their callers.

The Lead Developer filed seven child issues, fixed five of them that evening, and deferred two (#888 and #889, the hijack bugs) pending UX guidance from the CXO and PPM. The hijacks aren't simple bugs — they raise design questions about how Piper should handle users who are mid-flow when they ask unrelated questions. That's not a wiring decision; that's a product decision.

By the end of the night, the branch had three commits, six thousand forty-seven tests passing, and a clear picture of what M1 needs: more wiring, thoughtful UX for flow interruption, and continued vigilance for the 75% Pattern.

---

There's a lesson here that extends beyond our specific codebase.

When AI systems underperform, the instinct is to blame the AI. The model isn't smart enough. The training data wasn't good enough. The prompts need more engineering. And sometimes those explanations are correct.

But sometimes — maybe often — the problem is plumbing. The intelligence is there; the connections aren't. The classifier routes correctly; the handler never gets called. The capability exists; the wiring doesn't.

Before you retrain the model, check the cables.

The M1 sprint will continue. The hijack bugs will get design guidance and proper fixes. The wiring pass will happen, explicitly planned this time instead of discovered through failure. And somewhere in the codebase, the Assembly Assumption will be waiting in yet another form, because that's what patterns do.

But tonight, the pass rate is 81.1%. Not because the AI got smarter. Because the infrastructure finally connects.

---

*What problems in your work look like capability failures but might actually be connection failures?*
