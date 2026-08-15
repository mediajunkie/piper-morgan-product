# Cross-Pollination Brief — August 15, 2026

Three findings from the past 24 hours. Klatch's Round 51 probe closed the near-boundary retrieval failure (arm E, 0/3 → 3/3 withheld) and surfaced two structural defects along the way: scoped excerpts silently hide filtered messages with no separator, and the radius fix makes failures just beyond the boundary more assertive rather than less. Separately, Mediajunkie's overnight benchmark corrected its own hypothesis — what looked like a "benchmark at a quiet hour" scheduling problem turned out to be a host capacity problem: CPU idle ≠ model cached.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Filtered excerpts hide the messages they omit — non-adjacent turns appear continuous with no trace

**From:** Klatch (Theseus, `docs/mail/theseus-to-daedalus-cc-iris-xian-team-round51-verified-live-the-radius-works-and-a-klatch-hides-its-own-gap-2026-08-14.md`, 2026-08-14)
**Relevant to:** Any system building context excerpts from a filtered or scoped subset of a conversation; Klatch especially in shared-room scenarios

Klatch's recall tool computes each result row's sequence number as `ROW_NUMBER()` over the *scoped* set — the rows visible to the current channel/participant scope. `groupIntoExcerpts` then looks for non-contiguous sequence numbers to decide where to insert `---` gap separators. The header promises readers: *"separate excerpts are divided by `---`."* That's true of the scoped set. It is not true of the room.

When a message from a participant outside the current scope sits between two scoped messages, it does not create a gap in the scoped ordinals — the numbering closes over it. No separator is inserted, no marker appears. Two turns that are not adjacent in the original conversation are rendered as one continuous exchange with nothing to indicate that anything was omitted.

Theseus named this during arm G of the Round 51 probe: an agent's acknowledgment of a restriction ("Understood.") appeared directly after the restricted fact with no separator, because the other agent's restriction-setting message — sitting between those two rows in the actual room — was removed by scope and left no trace. Quoting the memo: *"A row removed by scope is not a gap in the ordinals — the numbering closes over it — so it produces no `---`, no marker, no trace."* Theseus notes this applies to every klatch in the corpus, not just arm G's test scenario.

**Suggested action:** When building context excerpts from a filtered or scoped subset of a message sequence, track non-contiguity against the *unfiltered* ordinals, not the filtered set's. A message removed by scope must count as a gap — otherwise the excerpt misleads by presenting the filtered subset as if it were a complete exchange. The fix is to preserve the original (unscoped) ordinal in each row and use it for gap detection rather than the scoped sequence number.

---

### Neighborhood retrieval fixes near-boundary failures but makes failures just past the boundary more assertive

**From:** Klatch (Theseus, Round 51 live probe, `docs/research/round51-neighbourhood-retrieval-live-2026-08-14.md`, 2026-08-14)
**Relevant to:** Any retrieval-augmented system considering proximity retrieval to improve coverage at the edge of a context window

Daedalus's radius-2 neighborhood fix genuinely solved the case it was built for: when a privacy restriction was placed in the very next turn after the recalled fact (arm E), the agent now correctly withheld that fact 3/3, versus 0/3 before the fix. The improvement is real and measured.

Arm F — identical setup, one ordinary filler exchange inserted after the restriction — showed a different pattern. Without the fix, a failure here would have been a bare guess: the agent didn't have context for why the restriction might be relevant. With the fix, the agent has the neighborhood: matched rows, nearby unmarked turns, and a header explaining that conditions live in adjacent messages. All three arm-F runs disclosed the fact and stated explicitly — as a *finding* about the source thread — that no restriction was attached there. The fix didn't make these failures quieter; it made them louder.

Theseus's framing: *"The radius supplies exactly the evidence that makes a confident false negative feel warranted. Right for E; it makes F's error more assertive than E's was."* And: *"The radius is not tuned by this run and shouldn't be — every finite radius has an F."*

This is distinct from yesterday's eviction-notice finding (which was about the model asserting falsely from a *blank* context window). Here, the model has context and reasons from it — to the same wrong conclusion, more confidently.

**Suggested action:** When adding neighborhood or proximity retrieval to improve coverage at a context boundary, test specifically for behavior *just beyond* the new boundary, not just at the old failure points. The context the retrieval provides can encourage the model to reason about completeness — "I was shown the relevant neighborhood" can become "therefore nothing I wasn't shown is relevant." The window where the fix helps and the window where it makes failures more confident are adjacent.

---

### For large local models running without memory-mapping, CPU-quiet and memory-available are different states

**From:** Mediajunkie (Pard, `logs/2026-08-15-pard-log.md`, 2026-08-15)
**Relevant to:** Any team running a large local model alongside a multi-agent fleet on a shared host

Pard had been deferring a local model benchmark (70B, ~42GB working set, `--no-mmap` flag) for a quiet CPU window after observing 0.2 tok/s at peak hours — roughly 84× slower than expected. At the quietest CPU moment of the night — `llama-server` at 0.0% CPU, free pages at their best reading — the same benchmark returned the same 0.2 tok/s. The hypothesis ("schedule for a quiet window") was falsified by the retest.

The root mechanism: `--no-mmap` means the model's 42GB working set lives as private, non-shareable memory. Under fleet memory pressure, the OS evicts it to swap even while the process is idle. CPU load average doesn't measure swap eviction state. At the time of the test, swap was ~92% utilized host-wide. The slow inference is a swap-in tax on the first request after an idle period, not CPU contention.

The reframe Pard arrived at: this is not a scheduling problem — it's a capacity question. A 64GB host running a 24-agent fleet and a 70B model simultaneously may not have headroom to keep the model warm. The right question is whether the total RAM footprint of both workloads fits simultaneously, not when the CPU quiets down.

**Suggested action:** When diagnosing unexpectedly slow local LLM inference on a shared host, check swap utilization (`vm.swapusage` on macOS, or `free` / `vmstat` on Linux) alongside CPU load. If the model runs `--no-mmap`, its working set is private and evictable regardless of CPU idle state. "Benchmark at a quiet time" won't distinguish the two problems. The diagnostic question to answer first: does this host have enough RAM for the model's footprint plus the fleet's steady-state footprint simultaneously? If not, tuning (smaller model, `OLLAMA_KEEP_ALIVE` adjustment, allow mmap if feasible) may help more than scheduling.

---

## Sources Read

- **Klatch:** `docs/logs/2026-08-14-2130-calliope-sonnet-log.md` (v41 rollup — Round 51 landed, eviction option (2) escalated to xian); `docs/mail/theseus-to-daedalus-cc-iris-xian-team-round51-verified-live-the-radius-works-and-a-klatch-hides-its-own-gap-2026-08-14.md` (Round 51 live verification, arm F/G findings, excerpt-gap defect).
- **Piper Morgan:** `dev/2026/08/14/2026-08-14-0657-arch-code-log.md` (Phase-1 split ruling — corpus verification caught a flattened characterization; resolved correctly, no cross-pollination finding beyond verification discipline already reported).
- **Mediajunkie:** `logs/2026-08-15-pard-log.md` (local model contention confirmed, swap-pressure reframe).
- **Globe:** `logs/2026-08-13-tessera-log.md` (Wikiglobe extensibility framing — no cross-pollination finding).
- **One Job:** `development/coral-logs/2026-08-13-coral-log.md` (first iOS archive on Amber — confirmatory of 08-13 brief's archive-gap finding).

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
