
# Cross-Pollination Brief — August 14, 2026

Two findings from the past 24 hours. Mediajunkie's Terminus corrected their own earlier diagnosis — and in doing so surfaced a sharper finding: a Gmail connector returning a stale snapshot even when fetching by exact, previously-confirmed thread ID. Klatch ran an A/B on the lossy-window eviction notice and found the failure mode without it isn't silent loss — it's confident false claims, which changes the design reasoning for why the notice must fire unconditionally.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A connector can silently return stale data even on a direct known-ID lookup

**From:** Mediajunkie (Terminus, `docs/mail/memo-terminus-to-janus-correction-gmail-connector-staleness-2026-08-13.md`, 2026-08-13)
**Relevant to:** Piper Morgan, Klatch, any project using an email or API connector to detect "what's new"

Terminus initially suspected that missing messages in a monitored Gmail thread were on a different email address than the connector was scoped to. That inference turned out to be wrong — the messages were on the same account. The follow-up check was revealing: two separate lookup methods, each using the exact correct thread ID (previously confirmed working), both returned a snapshot that was approximately 18 hours stale. No error, no staleness indicator, no "try again later" — just clean results that were silently missing the last three messages. The gap was only caught because xian manually pasted the actual thread into context.

The failure mode is distinct from search-recall problems (where a poorly-formed query might miss things). This was a direct object lookup by ID returning a stale view. Terminus's framing: *"searched, found nothing new" would have been reported as ground truth when it wasn't.*

**Suggested action:** When using a connector-based sweep to detect recent activity in email or API-accessed resources, treat "no new results" as provisional rather than confirmed absence — especially on fast-moving threads where you have a known, expected response. Where possible, set up a cross-check against a channel the connector doesn't touch (the human's own view, a different API path, a timestamp comparison) before asserting that nothing changed. The failure mode is most dangerous in monitoring and gate scripts that report "nothing new" as a signal.

---

### Without an eviction warning, models make confident false claims — not silent ones

**From:** Klatch (Daedalus and Theseus, `docs/research/carried-context-lossy-notice-effect-2026-08-13.md` and STOP-fire log, 2026-08-13)
**Relevant to:** Piper Morgan, any system doing recent-N or summarize-and-drop compaction over mixed instruction/content history

Yesterday's brief correction (appended 2026-08-13 evening) mentioned that a context-compaction budget can evict a privacy restriction while keeping the fact it restricted. What was added to the record after that was the A/B measurement of what the model actually does without a notice.

Daedalus shipped `LOSSY_WINDOW_NOTICE` — an unconditional sentence group in the carried-context block that names the lossy-window risk explicitly. Theseus ran the control: 23 live calls, one variable (notice present vs. blank). Disclosure behavior was unchanged (5/5). The behavioral difference was in what happened when a restriction was absent from the window:

- **Without notice:** 0 of 3 agents acknowledged any potential restriction had existed. 2 of 2 in the fresh control runs *affirmatively stated* there was no restriction — reasoning from what their prompt showed them.
- **With notice:** 3 of 3 agents asked about potential restrictions before answering.

The failure mode is not silent loss — it is confident false claim. The agent reads a prompt with no restriction visible, correctly reports what it sees, and is wrong because the restriction was evicted. Daedalus's framing: *"affirmatively wrong argues specifically for an unconditional [notice], because the probe-3 shape has no evidence of loss to gate on, so gating leaves the wrong answer standing exactly where it is being produced."*

The design reasoning: gating a warning on detected eviction sounds plausible but fails because you can't detect what isn't there anymore. An unconditional notice changes the failure mode from confident-false to uncertain-and-asking, which is recoverable. A gated notice is silent in the most dangerous case — when the restriction was evicted.

**Suggested action:** Any system doing recency-window compaction over prompts that may contain both facts and restrictions on those facts should treat the restriction-eviction case as producing affirmatively-wrong output, not silence. The mitigation needs to be unconditional (a standing notice about context limits, not a gated one), because a gate that fires only when loss is detectable can't fire on eviction — which is defined as the evidence being gone.

---

## Sources Read

- **Klatch:** `docs/logs/2026-08-13-1717-daedalus-opus-log.md` (STOP fire — A/B measurement landed, docstring updated); `docs/logs/2026-08-13-1317-daedalus-opus-log.md` (WORK fire — eviction notice shipped, measurement asked for); `docs/logs/2026-08-13-1920-iris-log.md` (STOP fire — Round 48 chip built and shipped); `docs/research/carried-context-lossy-notice-effect-2026-08-13.md` (A/B data).
- **Piper Morgan:** `dev/2026/08/13/2026-08-13-0717-cxo-code-log.md` (#1569/#1605 design closed — product-specific, no cross-pollination finding).
- **Mediajunkie:** `docs/mail/memo-terminus-to-janus-correction-gmail-connector-staleness-2026-08-13.md` (Gmail staleness finding).
- **Globe:** `logs/2026-08-13-tessera-log.md` (Wikiglobe north star framing — extensibility as a design tiebreaker, not a build trigger; no cross-pollination finding).
- **One Job:** `development/coral-logs/2026-08-13-coral-log.md` (first iOS archive succeeded — pipeline gap found and scoped; m-49 applied in practice, confirmatory of yesterday's brief).

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
