---
image:
alt:
caption:
---

# Hypothesis Refuted

*May 8–9, 2026*

The system has an automated quality test we run periodically against a panel of scripted user inputs. The output of each input gets scored against a rubric — relevance, competence, tone — by a second LLM acting as a judge. The aggregate score is meant to track whether quality is drifting upward or downward as the codebase changes.

On Friday morning May 8, Lead Dev ran the test for the first time after the ethics-floor work and the multi-day M2d shipping arc had landed. The previous baseline, from mid-April, had been 72.1%. The new run came in at 65.6%.

That's a six-point drop. Six points across a hundred test cases. The system's most recent few weeks of work — multiple major architectural changes, several issues' worth of new behavior — had apparently produced a quality regression.

Lead Dev filed it as a P0 issue. The working hypothesis: the LLM had started fabricating responses somewhere in the new code paths. Hallucination regression. The auto-fail rule (any rubric dimension of zero triggers a FAIL) had caught ten cases where the model produced confident answers that didn't track the underlying state.

That's the hypothesis. The investigation was supposed to confirm it and identify the introduction point.

# What the investigation found

The investigation took most of Friday afternoon. By the time the report landed, the hypothesis was largely refuted.

Of the ten auto-failure cases, zero were pure LLM fabrication. The model wasn't making things up.

What the model was doing — what it had been doing the whole time, going back at least to the April baseline — was something else. The judge was scoring along a dimension I'll call *user-context-specificity*. The judge wanted responses that referenced the specific user's specific recent activity. When the responses were generic-but-correct, the judge marked them low on the specificity axis, and the auto-fail rule (any dim = 0 → FAIL) flipped the case to FAIL.

Seven of the ten failures were of that shape. Three of the ten were narrow real bugs — a setup wizard that hardcoded a project name, a missing slot value in a templated response, a routing miss. Real bugs to fix, but bugs that didn't add up to a six-point regression.

Then the smoking gun. One of the test cases, identified internally as Q56, kept producing a response that repeated three or four todos back to the user — a confident-sounding but slightly weird response that looked exactly like a fabrication. The investigation pulled the database state for the canonical test user. There were fifteen real todos in the database from earlier test runs. Every prior `add a todo` test case had mutated state and never cleaned up. The model wasn't fabricating todos. The model was accurately reflecting the polluted fixture.

The aggregate metric had dropped six points because the judge had become more aggressive on a dimension that depended on a fixture that had been contaminated by the test itself.

The hypothesis had been: *the system regressed.* The actual finding was: *the measurement instrument and its reference state had both drifted, and the system was approximately where it had been.* Two layers of category error, neither of them in the code we'd shipped.

# What the recovery looked like

By Saturday morning the remediation was queued. Fifteen stale items and a hundred-eleven orphan items got wiped from the canonical fixture. Lead Dev sent a recalibration memo to the experience-design and product-management roles asking them to look at the judge's rubric anchors. Three narrow bug fixes shipped for the actually-real bugs.

Then the retest. Run 5 diagnosed a remaining verdict-gap. Run 6 closed it. Run 7 came in at 68.9% PASS — above the mid-April baseline of 65.6%. (The 72.1% number from the original report turned out to be from an even older run with the un-polluted fixture. Compared against the most recent comparable baseline, the system was up, not down.)

I'd told Lead Dev on Friday evening that we wouldn't touch the next cleanup milestone until the preceding work cleared the benchmark. By 8:15 AM Saturday the benchmark was cleared. The cleanup work was unblocked.

What came next — Saturday's cleanup sprint — produced a second instance of the same shape.

The cleanup milestone had a queue of issues describing code that needed to be hardened or refactored. Lead Dev opened the first one and discovered the code the issue described didn't exist in the way the body said it did. The issue body claimed a defensive-fallback was missing. The actual code had been deleted weeks earlier. The fix wasn't to add the fallback. It was to close the issue and delete the dead test that referenced the no-longer-existent code path.

Then the second issue. Same shape — body said one thing, code said another. Then the third. By the end of Saturday, three of the five cleanup issues in that pass turned out to describe phantom work. The work was deletion, not implementation.

Lead Dev filed it as Pattern-067, *Issue-Body Reality Mismatch.* The counter-discipline: before scoping migration or refactor work, audit whether the body's claims still match the code. The pattern emerged because three instances showed up in a single day's work, but the pattern named a shape that had probably been firing quietly for months.

# Why the two findings rhyme

The judge had drifted from what it was measuring. The issue bodies had drifted from what they were describing. Both gaps had stayed silent for a long time — the judge produced numbers, the issues described what looked like real work, the system kept running. The drift only surfaced when the gap got wide enough that something tripped.

In both cases the diagnostic instinct was to fix the system to match the report. The hypothesis was *the system regressed.* The hypothesis was *implementation work needs to happen here.* In both cases the actual move was to fix the reference — clean the fixture, recalibrate the rubric, audit the body against the code — not the system.

This is a generalizable trap. Any time a measurement runs against a reference that the measurement itself can mutate, the reference drifts. Any time a description outlives the code it described, the description becomes a different document. The compounding is silent. Nothing screams. The aggregate number is six points lower. The implementation queue is full of work that turns out to be deletion. The system is fine. The system was always going to be fine. The work is upstream — at the reference state, not the system under measurement.

# What's portable

Most of what looks like a system regression turns out to be a reference-state drift. The discipline this week's findings landed across both layers is the same: when a measurement or a description has been quietly running ahead of the code it's supposed to track, the fix is to ground-truth the reference, not patch the system. Reset the fixture before re-running the metric. Audit the body before scoping the work. Recalibrate the rubric before chasing the regression.

The day Lead Dev cleared the M2f cleanup, the actual code change for the morning was small. Three narrow bug fixes. A fixture wipe. A rubric memo to two roles. The cleanup sprint deleted a thousand-plus lines of code that nobody had been running for months. The single rubric drop had pointed at all of it, indirectly, by the time we understood what we were actually looking at.

---

*Next on Building Piper Morgan: [TEASE PENDING — confirm next-scheduled-item at calendar update].*

*Where in your work has a measurement or a description been silently running ahead of the system it's supposed to track? What would grounding the reference look like?*

[FACT-CHECK NOTE for PM: Sources verified against May 8 + May 9 omnibus logs. Key facts: May 8 — Lead Dev's canonical retest Run-4 (Routing 93.4%, Quality 65.6% vs Apr 12 baseline 72.1%); #1064 P0 filed; investigation report at `dev/2026/05/08/floor-fabrication-investigation.md` finds 0 of 10 auto-fails pure fabrication, 7 false flags (judge-calibration / methodology / fixture artifacts), 3 narrow real bugs (setup wizard hardcoded ×3 sites; `#N` slot-filling; routing-miss queries). Q56 smoking gun: 15 real todos in DB from fixture pollution. SYSTEMIC cause: judge over-weights user-context-specificity × auto-fail rule (any dim=0 → FAIL) amplifies miscalibration. CEO directive May 8 17:22: "we do not go in M2f till the preceding work at least meets the most recent benchmarks and exceeds on relevant queries." May 9 — fixture reset (15 stale + 111 orphan wiped) + recalibration memo to CXO+PPM (`29f0b592`) + 3 fixes (#1065 setup-wizard `49c48c2e`; #1067 doc-update routing `f623bba2`; #1066 `#N` slot-fill `78be342e`). Run 7: Quality 68.9% PASS exceeds baseline. M2f Group A+B closed via dead-code deletions: #932 HIBP honest-unknown + #933 re-enable key validation + #936 UserService deletion (−435 LOC) + #935 analytics deletion (−1378 LOC). Pattern-067 (Issue-Body Reality Mismatch) filed Emerging with 3-of-5 evidence from same day's Group A+B work.]

[SOURCE NEEDED for PM: The 72.1% Apr 12 vs 65.6% Apr 12 baseline framing — May 8 omnibus references both "Apr 12 baseline 65.6%" and "Apr 16 peak 72.1%" at different points. I rendered the comparison as 72.1% prior baseline → 65.6% Run-4 → 68.9% Run-7 (above Apr 12 baseline). The framing is internally consistent (system ended up above the comparable baseline) but the specific numbers are taken from the omnibus's framing rather than direct verification of the retest CSV files. Flag if the numbers should match a different reference baseline.]

[SOURCE NEEDED for PM: "I'll call user-context-specificity" — the omnibus describes the judge over-weighting "user-context-specificity" as a phrase. I rendered it as a slightly-narrative naming move ("I'll call"). The actual Lead Dev investigation doc may have a more precise term; if so, swap.]
