# Cross-Pollination Brief — August 16, 2026

Two transferable findings from yesterday's window: a probe-design failure mode that showed up independently twice in one week in Klatch, and a platform scheduling discovery in Piper Morgan that separates one-shot and recurring cron behavior by two orders of magnitude.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Probes that match exact output wording go stale silently when the feature they're testing improves

**From:** Klatch (Theseus, `docs/research/round56-expand-address-live-2026-08-15.md`, 2026-08-15)
**Relevant to:** Piper Morgan, Design in Product, any project maintaining behavioral integration probes or regression tests against LLM output

Two separate probe failures occurred in the same week — independently, in different files — with the same mechanism: a probe was written to match a specific phrase in the model's output; the feature that phrase described was later improved; the new output no longer matched the old wording; the probe returned zero (a legal value), not an error. Both zero-results read as "the feature doesn't do this anymore" rather than "the probe stopped measuring."

From Theseus's writeup: "A probe keyed on a build's exact wording goes stale silently every time that wording is improved, and reports zero, and zero is a legal value." The Round 54 revert probe missed all Round 56 output because Round 56's edge-marker text changed. The Round 56 edge-marker probe then caught the same pattern in its own scanner: the phrase `"N that a different search of yours could reach"` — the Round 54 form — no longer matched any Round 56 output at all, and the scanner reported `edgeReachable = 0` on every run. A reader who didn't know to check would have concluded the Round 56 build had no edge-marker behavior at all.

Theseus's framing: "Two independent instances in one week is a pattern, not a coincidence."

**Suggested action:** When writing a behavioral probe or integration test against LLM output, avoid anchoring the pass criterion to the exact current wording of the output. Instead, match on structural or semantic markers that survive rephrasing — a tool call shape, a field name, a presence/absence of a distinct concept — rather than a prose phrase. Where prose matching is unavoidable, explicitly verify probe sensitivity: confirm the probe can fail (i.e., run it against a build where the behavior is absent and confirm it returns nonzero). A probe that has never been seen to fail may be measuring nothing.

---

### One-shot cron jobs fire within seconds; recurring cron jobs on the same platform show ~30-minute latency — they are different mechanisms, not the same mechanism with noise

**From:** Piper Morgan (CIO, `dev/active/cron-dispatch-latency-experiment-2026-08-15.md`, 2026-08-15)
**Relevant to:** Design in Product (trigger infrastructure), Klatch (scheduled intel sweeps), any project using the Claude Code on-web cron scheduler

The CIO duty cycle had been observing ~29–30 minute latency on its recurring `7 10,16,22` cron all week. Three one-shot cron jobs were scheduled at 22:47 / 22:52 / 22:57 PT as a controlled comparison. All three fired within 3–4 seconds of their scheduled minute (+3s, +3s, +4s). Spread across the three: 1 second.

The experiment did not set out to find a job-type difference — it set out to sample at shorter intervals to locate the source of the ~30-minute gap. What it found instead was that the gap doesn't exist for one-shot jobs at all. The two to three orders of magnitude difference between "single-digit seconds" and "~30 minutes" rules out a universal jitter floor: these are structurally different dispatch behaviors, not the same behavior at different noise levels.

What the experiment did NOT resolve: why the recurring cron specifically shows ~30-minute latency. The CIO's framing: "Something specific to recurring jobs, or to this particular cron's minute-of-hour, or to REPL-idle timing at the moment the recurring slot arrives, produces the ~30-min gap — not a universal dispatch-jitter property this experiment could have found by sampling faster."

**Suggested action:** For any cron-scheduled task where timing matters — monitoring sweeps, observability receipts, time-sensitive deliveries — prefer one-shot jobs over recurring cron when the platform is Claude Code on the web. If recurring jobs are necessary, budget for ~30-minute dispatch latency as a baseline, not as jitter to be optimized away. The experiment's design is replicable: three one-shot jobs at short intervals establishes a reference point for any platform whose recurring-job latency is unclear.

---

## Sources Read

- **Klatch** — `docs/research/round56-expand-address-live-2026-08-15.md` (Theseus, Round 56 probe); `docs/logs/2026-08-15-2130-calliope-sonnet-log.md` (rollup v45, coordination)
- **Piper Morgan** — `dev/2026/08/15/2026-08-15-1037-cio-code-log.md` (dispatch-latency experiment design and conclusion); `dev/active/cron-dispatch-latency-experiment-2026-08-15.md` (raw readings and conclusion)
- **Mediajunkie** — `logs/2026-08-16-pard-log.md` (swap plateau confirmation — three consecutive ~95% readings confirm stable state change, not transient; no new brief-worthy finding beyond Aug 15's local-model insight)
- **Globe** — delivery commits only (briefs from Aug 14–15); no new agent activity
- **One-job** — iOS build number bump (rc.31 TestFlight upload); log notes Aug 15 brief processed, no applicable cross-poll finding
- **Cookie-monster** — delivery commits only; no new agent activity

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
