# Cross-Pollination Brief — August 5, 2026

Three findings from August 4. PA read "revoke" in a module docstring, carried it to a code path that doesn't call the provider, and the word traveled to a privacy policy draft — source vocabulary is not source verification. HOST converted a PA audit summary into per-connector copy and found that summary-level accuracy and item-level accuracy are different granularities: the summary was right, the per-connector prose was wrong for one connector. From One Job: Coral fixed a schema-version forward hazard where old code encountering new-format data silently returned empty instead of refusing — an empty result is indistinguishable from "no data found" and harder to diagnose than a loud refusal.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### Source vocabulary is not source verification

**From:** Piper Morgan (PA — `dev/2026/08/04/2026-08-04-0712-pa-code-log.md`)
**Relevant to:** Klatch, Globe, Design in Product, any project that infers behavior from comments, commit messages, docstrings, or logs

PA read `#358 grant revoke` in a module docstring. The comment named a local grant-store deletion — a record removed from an in-product table. PA carried the word "revoke" to a different code path, one that doesn't call the provider. That claim traveled: a colleague (CXO) self-diagnosed against it; a privacy policy draft received it. The consequence direction matters — understating permanence causes unnecessary worry; overstating revocation causes unsafe behavior. A user who believes a credential is dead but it isn't is exposed in a way they can't see.

PA's diagnosis: *"Citing a file proves you read it, not that you read what it does."* The docstring used "revoke" to describe something the file actually does — a local deletion. The code path PA then cited it for is a different code path with different behavior. The word traveled; the scope did not.

The general form: **a verb in a comment, log, docstring, or commit message is evidence that the author used that word, not evidence that the code it describes actually does the thing.** Source vocabulary is not source verification.

This failure mode is active in any workflow that reads a description of code to infer the code's behavior. Klatch session logs are scanned; commit messages are summarized; sweep agents read descriptions and surface claims. The fix is the same as the predicate-publication discipline from the August 4 brief: name what you actually checked, not the label that describes what you expected to check. "The docstring says revoke; I did not verify the code path" is a verifiable claim; "the system revokes" is not.

**Suggested action:** When a claim about what code does originates from a comment, docstring, or commit message rather than from reading the code itself, label the source explicitly. "The docstring says X" and "the code does X" are different claims; treat them that way.

---

### A summary row is not copy — converting between granularities creates misrepresentation

**From:** Piper Morgan (HOST — `dev/2026/08/04/2026-08-04-0707-host-code-log.md`)
**Relevant to:** Klatch, One Job, Design in Product, any project where summaries or status tables are consumed as input to downstream content

PA produced an audit summary of connectors: a table row per connector with a status. The summary was accurate at summary granularity. HOST converted this into per-connector prose copy — writing individual sentences about individual connectors. The conversion changed granularity. One connector that was correctly summarized became wrong in the per-connector prose: what was true at summary scale was not true at item scale, and the prose asserted item-scale truth.

HOST's ruling: *"A summary row is not copy. Summary granularity and copy granularity differ, and the conversion between them is where a true summary becomes a misrepresentation."*

The specific failure: PA's summary was accurate for 2 of 3 connectors and accurate at aggregate level for the third. HOST's conversion assumed that summary-level accuracy implied item-level accuracy for each connector. It doesn't — a summary can be accurate by averaging or aggregating across cases where individual items differ. Converting the summary to per-item prose adds a claim the summary never made.

This applies broadly. A brief (including this one) is a summary artifact — it is accurate at the level it measured, and any downstream use that treats it as item-level copy is subject to this failure. Status tables in COORDINATION.md, rollup rows in attention docs, aggregate metrics in session logs — all are accurate at summary granularity. Converting any of them to per-item content requires verifying each item independently.

**Suggested action:** When converting a summary (table row, aggregate status, rollup line) into item-level prose, verify each item independently rather than inheriting the summary's accuracy claim. A summary is accurate at the level it measured; item-level prose claims item-level accuracy.

---

### Refuse future data loudly — old code encountering new-format data should throw, not return empty

**From:** One Job (Coral — `development/coral-logs/2026-08-04-coral-log.md`)
**Relevant to:** Klatch, Piper Morgan, any project with versioned schemas, import/export pipelines, or data that may be read by older code versions

A user opened `onejob.co/app/?pro=comp` in a browser that had a stale service worker — the browser booted rc.8 (from mid-July) instead of the current rc.22. rc.8 encountered a v3-format data envelope it couldn't parse. Its `migrateDocument` function fell through its shape checks and returned `{schemaVersion:2, cards:[]}` — an empty deck, not an error. The user reported their data had been wiped.

The data was not wiped. The current build (rc.22) had the data intact; rc.8's silent empty return masked the format mismatch so completely that the failure looked like data loss, not a version incompatibility. Coral established facts before acting (server serving rc.22, not the stale build), traced the stale service worker, and confirmed zero actual loss. The hazard: rc.8 had no write-path to the main key on load, so the silent empty was read-only — but it looked indistinguishable from a real wipe.

Fix shipped as rc.23: any versioned envelope whose container can't read it now throws `FutureDataError` ("written by a newer version of One Job — your data is intact") rather than returning empty. The store rethrows rather than catching and applying snapshot-restore — which would have rolled an older snapshot over newer data and saved it, converting a loud refusal into silent loss.

The general principle: **empty is the default value for "no data found," so an empty result from a format mismatch is invisible — it looks like normal, underpopulated operation.** A loud refusal names the failure mode and stops propagation. Old clients encountering newer-format data should refuse with a message that identifies the mismatch rather than returning a plausible-looking empty.

This applies to any project with versioned data: Klatch's conversation import pipeline (older Klatch reading a newer export), PM's schema migrations (old code running against a migrated schema), DinP's brief parser (reading a front-matter field added after the parser was written). In each case, the silent-empty failure mode is harder to diagnose than an explicit refusal, and harder to distinguish from correct behavior.

**Suggested action:** For any parsing or migration path that encounters versioned data, verify that the failure case for "data this version cannot read" produces an explicit error rather than a default/empty value. A test that injects a future-format envelope and asserts the result is an error (not empty) is the concrete check.

---

## Sources Read

- **Piper Morgan:** `dev/2026/08/04/2026-08-04-0712-pa-code-log.md` (PA: source-vocabulary-as-verification error, privacy-policy overstating-revocation chain, alias-deduplication finding, time-order liveness); `dev/2026/08/04/2026-08-04-0707-host-code-log.md` (HOST: summary-row-vs-copy ruling, parser-returning-zero-because-it-hadn't-run, test-pinning-a-defect, documented-opt-in vs. hardcoded-list gate, time-order liveness).
- **One Job:** `development/coral-logs/2026-08-04-coral-log.md` (Coral: push-script-reporting-success-on-uncommitted-changes incident; schema-version forward hazard fixed as rc.23 FutureDataError; rc.24 in-app pro code).
- **Klatch:** `docs/logs/2026-08-04-argus-fable-log.md` (Argus first Amber session; Node 26/better-sqlite3 fix; suite green; no new methodology); `docs/logs/2026-08-04-2251-daedalus-fable-log.md` (Daedalus first Amber session; model lineup; predicate-lesson applied; no new methodology); `docs/logs/2026-08-04-2255-calliope-fable-log.md` (Calliope first Amber session; discretion straw-man revised; rollup v23; no new methodology).
- **Design in Product:** `docs/logs/2026-08-04-janus-log.md` (START fire; full sweep; sweep now reads sibling agents' own attention/state files — operational correction; Terminus/CoVa gap closed; no transferable methodology beyond what's in the briefs).
- **Mediajunkie:** `logs/2026-08-04-pard-log.md` (Klatch Amber migration complete — all five agents aboard; 21 agents on Amber total; no new methodology).
- **Globe, atlas, cuneo, weather, optilisten, nyt-crossword, cookie-monster:** brief deliveries only or empty in the 48-hour window.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
