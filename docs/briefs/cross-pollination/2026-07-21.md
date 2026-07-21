# Cross-Pollination Brief — July 21, 2026

Three technique findings today: a two-pass gate protocol that catches what green tests miss (Klatch); a victim-side cure for shared-pool test contamination (PM); and a diagnosis that LLM warm-up latency is 2× slower than steady-state and will false-trigger timeout-based fallbacks (Mediajunkie).

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Tests prove "what we built works" — a capability checklist proves "what we built achieves the use case"

**From:** Klatch, Argus + Calliope + Iris (`docs/operations/pre-gate-protocol.md`, filed 2026-07-19)

**Relevant to:** Any project that gates releases on test suites

The composition gesture shipped green tests, green AAXT coverage, and an Iris review pass. The gate was declared clear. The first time someone tried to run the canonical use case — the weekly leadership review with agents carrying their week's context — it couldn't be done. The test suite proved "what we built works"; it said nothing about whether what was built achieved the intended purpose.

The filed protocol formalizes two passes before any "gate clear" declaration:

**Pass 1 — Capability Inventory:** Walk through each capability required for the canonical use case as yes/no. Every row must be ✅ before the gate clears. "Mostly done" or "close" is ☐. This is a human + real-system check — no automated test can do it; it asks "does this exist and can it run?" not "does it behave correctly."

**Pass 2 — Scope Reconciliation:** Before declaring any feature "complete," list every item in xian's stated scope and get explicit calls on anything not built. "Not now" said in passing is not an approved deferral — only a recorded decision in a memo, COORDINATION.md, or ROADMAP.md counts.

The composition continuity gap would have been caught by Pass 1 at the gate; the missing Paths B/C would have been caught by Pass 2.

**Suggested action:** Before the next gate declaration in any project, run a manual capability inventory anchored to the stated canonical use case. If you can't state one canonical use case, that's the first gap to surface.

---

### Shared-pool test contamination is an accumulation effect — cure the victims, not the poisoners

**From:** Piper Morgan, Lead Developer (session log `dev/2026/07/20/2026-07-20-1202-lead-code-log.md`, issue #1452)

**Relevant to:** Any project with integration tests sharing a database connection pool

A class of `asyncpg InterfaceError: another operation is in progress` failures appeared under full integration test load but not in isolated runs. Root cause: abandoned mid-operation connections accumulating in the shared pool from earlier tests. No single poisoning test caused this — it was an accumulation effect, meaning every subdirectory run clean in isolation but the load of the full suite surfaced it.

Hunting individual poisoner tests was a dead end. The cure: convert affected tests to fresh-per-test database engines (the "B15 house pattern") rather than sharing the pool. The poisoned tests began passing as soon as they stopped consuming from the shared pool. 22 backlog entries cleared; the fix was verified in-sweep under the same full-integration load that previously killed them.

The principle: when tests interfere through shared infrastructure, isolate victims to their own resource rather than diagnosing which test left the resource in a bad state. Accumulation-effect contamination has no single culprit; the systemic cure is victim-side isolation.

**Suggested action:** If your integration test suite has occasional failures that appear under full-suite load but not in isolation, try fresh-per-test engines before investing in contamination bisection. Bisection of accumulation effects rarely converges.

---

### First-after-idle LLM inference runs 2× slower than steady-state — calibrate timeouts separately

**From:** Mediajunkie, Pard (task #12 closure, `docs/backlog.md`, 2026-07-20)

**Relevant to:** Any project running LLM inference with timeout-based fallbacks or health checks

Benchmarking on eight production-shaped prompts revealed: steady-state throughput was 31–33 tok/s, but first-after-idle inference ran at 20.6 tok/s, taking 44.4 seconds. A 40-second timeout calibrated to steady-state was tripping the fallback handler on the first request after an idle period — making the system appear to be failing when it was warming up.

The fix was a timeout raise to 60 seconds. The insight is that a single timeout constant conflates two distinct operating regimes. If your fallback mechanism doesn't distinguish warm-up from actual failure, you'll see false positive fallback triggers on first requests after quiet periods.

**Suggested action:** When calibrating LLM inference timeouts, benchmark cold-start (first-after-idle) separately from steady-state. Set the timeout to the cold-start ceiling, not the steady-state median. Add a note in your fallback handler that first-request latency is inherently higher.

---

## Sources Read

- **Klatch**: `docs/operations/pre-gate-protocol.md`, `docs/logs/2026-07-19-iris-log.md`, `docs/mail/` (Daedalus→Calliope transcript-model reframe, Argus pre-gate reply, 2026-07-19)
- **Piper Morgan**: `dev/2026/07/20/2026-07-20-1202-lead-code-log.md` (Lead Dev day-close, issue #1452 harness + burn-down arc)
- **Mediajunkie**: git log (task #12 closure commit, `docs/backlog.md` patch)
- **Globe, One Job, Weather, Cookie Monster**: brief deliveries only (cross-pollination re-posts) — no new source activity
- **Atlas, Cuneo, Optilisten**: no activity in window
- **NYT Crossword**: automated status prints only — no narration

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

