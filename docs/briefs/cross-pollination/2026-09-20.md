# Cross-Pollination Brief — September 20, 2026

Two insights this window. Klatch built a pair of environment-variable levers that retired six source-patching test probes, fixing a class of measurement fragility along the way. One Job's audit for write-deletion orphans discovered that the instrument itself carried the defect it was looking for — and in doing so surfaced a cross-language contract that no single-language tool can see.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. A test probe that patches shipped source to set a constant loses the ability to detect stale guards — an env-var lever built at the right seam retires the whole pattern — Klatch Rounds 235/237/238

**From:** Klatch  
**Relevant to:** Piper Morgan, One Job, any project with behavioral test probes

Four probes in Klatch's test suite were rewriting the same constant in shipped source (`FINGERPRINT_LINE_CAP` in `session-scanner.ts`) to make endpoint-level measurements that would otherwise have had no seam. This approach has three compounding weaknesses: the patch guard degrades to a skip if the spelling changes (Round 234 found arms lost silently when a constant was reformatted from `50000` to `50_000`), a crash between patch and restore leaves the repo modified, and a guarded skip makes "feature not built" and "probe arm stale" look identical in output. Klatch Rounds 235 and 237 built two env-var levers — `KLATCH_EXPORT_ROOT` and `KLATCH_FINGERPRINT_LINE_CAP` — that gave the probes a proper seam without touching source.

The design discipline applied to both levers: read per call rather than cached at module load (so probes that set the variable after server startup still get it, rather than finding the import-time snapshot); invalid values throw rather than silently falling back to the default (a silent fallback would report the probe's setpoint while measuring the default, confounding exactly the measurement the lever exists to serve); and an explicit function argument still wins over the variable (probes measuring specific values aren't polluted by the environment). Round 238 verified the conversion by re-measuring endpoint deltas on the same corpus used to derive the original patch numbers, not by checking exit codes — because exit codes can only report pass/fail, not confirm which value was actually applied.

**Suggested action:** When a test probe rewrites shipped source to create a seam, ask which function parameter or environment variable at the correct architectural boundary would make the probe unnecessary. Build the lever once; it will retire multiple probes, and each one's skip guard will stop masking stale arms.

---

### 2. An audit instrument that searches by literal string carries the defect it is auditing for — One Job (2026-09-19)

**From:** One Job (Coral)  
**Relevant to:** any project with cross-language or cross-module storage contracts

Coral ran an audit for write-deletion orphans (storage slots where a writer exists but the reader was never updated, or vice versa). The first pass returned zero exposures — not because there were none, but because the grep searched for literal string values while the code accesses storage keys via constants. The audit instrument had the same structural defect as what it was auditing: a dependency on the literal spelling of the key. The same change that would orphan a reader would also make the audit's search string a no-match.

Re-running by constant surfaced one real exposure: a Swift/TypeScript cross-language contract where `AddCardIntent.swift` writes `"CapacitorStorage.oneJobPendingCards"` directly into UserDefaults (the Capacitor plugin adds the `CapacitorStorage.` prefix when writing), and `shortcutsInbox.ts` reads `"oneJobPendingCards"` (the plugin strips the prefix when reading). No single-language grep, typecheck, import-sweep, or analyzer can see both sides of this contract simultaneously; rename either side and intent cards queue silently forever while every analysis tool reports green. Coral pinned the contract with a test that reads both source files and asserts the keys resolve to the same value, then mutation-tested the pin by renaming the Swift key — confirming the test goes red on a real mismatch.

**Suggested action:** Before treating a zero result from a contract audit as "all clear," check whether the audit instrument reads constants to their values or matches their spellings. Cross-language storage contracts in particular are invisible to any single-language analysis and need a bi-source test. Mutation-test any such pin: a test that doesn't go red when you break the contract isn't a pin.

## Sources Read

- **Klatch** — `docs/COORDINATION.md`, `docs/logs/2026-09-19-1717-daedalus-opus-log.md` (Round 237 lever design), commit messages for Rounds 234–238
- **Piper Morgan** — commit log for 48-hour window; no brief-worthy innovations (session fires, issue triage, T1 synthesis endorsed)
- **One Job** — `development/coral-logs/2026-09-19-coral-log.md`

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
