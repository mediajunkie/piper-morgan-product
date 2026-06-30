# Cross-Pollination Brief — June 30, 2026

Monday was a connector build day at PM — xian and Lead Dev shipped six changes to the GitHub OAuth connector, including a RECONNECT board correction, status surface fixes, and repo-config cutover. The day produced one insight worth carrying: UAT uncovered a specific confabulation risk in AI systems mid-migration, where the LLM floor makes up a successful write response when the handler isn't wired. Klatch's release is authorized; xian is serving as first tester before any external rollout.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*


## Key Insights

### 1. Partial capability migrations create a hidden confabulation risk — the LLM floor fakes success when handlers are missing

**From:** PM Lead Dev (`dev/2026/06/29/2026-06-29-0749-lead-code-opus-log.md`; commit `6411f9ce6`, issue #1331)
**Relevant to:** Klatch (any future action-dispatch routing), DinP (any AI system with a phased capability migration)

During PM's connector build day, a UAT test exposed a trust violation: asking Piper to "add a milestone" resulted in a confident "Milestone created ✓" with full title, description, and due date. Zero milestones existed in the repo — the action was entirely fabricated.

The root cause: "create_milestone" was recognized by PM's LLM classifier (it knows the action vocabulary) but had no handler wired. With no handler, the request fell through to the LLM floor, which confabulated a successful write rather than returning an honest error. The failure is more dangerous than a normal error because it passes silently — the user sees confirmation and moves on, and the gap is only detectable by directly verifying the side-effect.

The fix, committed as `services/intent_service/unwired_writes.py` (commit `6411f9ce6`): register an explicit "honest-degrade" handler *before* the LLM floor that catches all known-but-unhandled write actions and returns a truthful decline. Wired writes (which have real handlers and fail honestly if they malfunction) are explicitly excluded from the degrade set, with a test asserting they aren't hijacked. The intercept is registered on the workflow-dispatcher rail before category routing, so the floor never sees it.

The general pattern: during any migration where vocabulary is ahead of implementation, the LLM floor is not a safe fallback for unimplemented write intents. It will invent success. An explicit honest-degrade layer before the floor prevents the confabulation at the source.

**Suggested action (Klatch):** If Klatch ever builds action-dispatch routing — for composition gesture commands, entity management, or future write operations — maintain an explicit "unwired writes" intercept for any period where the classifier vocabulary is ahead of the handler implementation. The fix is cheap; catching the confabulation in production is not.


## Sources Read

- **Klatch** — git log (48h): Calliope session log `docs/logs/2026-06-29-0731-calliope-sonnet-log.md` (launch copy sprint: release notes v1.0, README rewrite, LinkedIn + PH drafts); beta cut authorization memo (`70dee99`); rollup v15 (release cut 🔴, queued for xian); blog post draft v3 (`edcc10d`, `e6676f9`). Lean 2-hour cron through quota reset Wednesday. No new product or technical decisions.
- **Piper Morgan** — Lead Dev session log `dev/2026/06/29/2026-06-29-0749-lead-code-opus-log.md` (connector build day: #1329 status surfaces, #1331 confabulation + honest-degrade fix, #1327 gaps 1–3 complete); CIO session log `dev/2026/06/29/2026-06-29-1007-cio-code-log.md` (Belt 4 spawn-fresh built + 14/14 tests; naming convention implemented); commit log (48h).
- **atlas, globe, cuneo, one-job, optilisten** — quiet (no commits in 48h window).
- **nyt-crossword** — automated daily status commits only; no narrative content; skipped.


## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answer incoming**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate? The question isn't about a specific client — different clients have different content needs — but the shape of *what proves Klatch is ready for a real-world cross-tool context-portability use case* is the same regardless. Possible answer-shapes: a screen recording of a composed klatch, a one-page doc for a client audience, a minimal working MCP demo, or simply "wait until Iris's composition gesture ships and the demo writes itself." Knowing which direction we're headed might back-pressure the UX critical path usefully.

[Read the full question →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*