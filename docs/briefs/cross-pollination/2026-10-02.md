# Cross-Pollination Brief — October 2, 2026

Two findings this window. Klatch's probe system surfaced a structural trap in absence controls: a corpus scanner that finds *owners* of a label will find the probe file itself if that file contains the label as a query argument. Piper Morgan's freeze-check found that `grep -q` under `set -uo pipefail` turns a successful match into a script failure through SIGPIPE — the quiet-flag optimization is the hazard.

## Key Insights

### 1. A corpus absence-control must exclude the probe file from both the hits search and the owner lookup — Klatch, Theseus, Round 313

**From:** Klatch (Theseus) · 2026-10-01 log
**Relevant to:** any project with a corpus scanner that tests for the absence of a label, symbol, or reference by querying who "owns" or defines it

Theseus was writing a probe to verify that a label (`Q9`) had no owners — an absence check. The probe file contained `ownersOf('Q9')` as the test call. The corpus scanner reads any quoted label as a definition, so the probe file itself became the owner of `Q9`. The owner lookup returned a non-empty result not because the production code was broken, but because the test file was included in the scan.

The probe file was already excluded from the *hits population* (the search for where Q9 appeared in production code). But the *owner lookup* — the separate query asking which file defines Q9 — ran against the full corpus including the probe file. Both sides of the check need the same exclusion.

Theseus's framing: the self-exclusion that protects one half of a corpus query does not automatically extend to the other. A control that asserts "no file owns X" will find the test file owning X as soon as the test file queries for X.

A second observation from the same round: when a repair inserts a citation between two tokens to break a problematic pairing, the insertion makes a known positive invisible by disrupting the nearest-preceding binding. If the known positive fires on the token *pair*, separating them removes it for the wrong reason — the probe was testing the pair, not the individual tokens. The structural fix is to keep the pair and repair the binding rule, not to separate the tokens.

**Suggested action:** In any corpus-level absence check ("no one should own X," "no file references Y"), identify every query the probe makes — not just the primary population search — and apply the same self-exclusion to each. Test the control with a known positive that deliberately adds the queried label to a third file (not the probe file), to confirm the exclusion only removes the probe's own presence, not genuine owners.

---

### 2. `grep -q` under `set -uo pipefail` turns a successful match into a script failure via SIGPIPE — Piper Morgan, Pard, commit `7f4d65054`

**From:** Piper Morgan (Pard) · freeze-check v0.17 NO-DAY-CLOSE detector
**Relevant to:** any shell script using `grep -q` (or any other early-exit consumer) in a pipeline under `set -uo pipefail`

`grep -q` exits immediately after finding the first match, without reading the rest of stdin. This sends SIGPIPE to the producer process — the command feeding the pipe — which then terminates with a non-zero status. Under `set -uo pipefail`, a pipe where any stage exits non-zero fails the entire script. The result: a match is found, the script "succeeds" at its query, and then fails anyway because the producer was killed.

Pard found this while shipping a streak detector that scanned role logs for the absence of a `DAY-CLOSED` marker across K consecutive days. The detector used `grep -q` to test for the marker. Under `pipefail`, false failures appeared on roles that *did* have the marker — the very population it was supposed to pass cleanly.

Fix: remove `-q` and use full-read grep. If suppressing output, redirect to `/dev/null`:

```bash
some_command | grep 'pattern' > /dev/null
```

This reads all stdin before exiting, so no SIGPIPE reaches the producer. Alternatively, guard with `|| true` if a non-match should not fail the script.

The subtlety: `grep -q` is routinely recommended as the "efficient" form for boolean checks. Under `set -uo pipefail` it is the dangerous form. The optimization that makes it fast — early exit — is exactly what makes it unreliable in a strict pipeline.

**Suggested action:** Audit shell scripts that use `grep -q` (or `head -1`, `tail -1`, or any other early-exit consumer) inside pipelines guarded by `set -uo pipefail`. Replace `grep -q` with `grep … > /dev/null` or add `|| true` guards where a non-match is an acceptable outcome. Add a known-negative test case (a grep that provably should not match) to confirm the pipeline exits cleanly when the pattern is absent.

## Sources Read

- **Klatch:** `docs/logs/2026-10-01-1047-theseus-opus-log.md` (Round 313 — self-scanning corpus self-reference trap; probe excludes itself from hits but not from owner lookup); commits in window
- **Piper Morgan:** commit `7f4d65054` (freeze-check v0.17 NO-DAY-CLOSE detector; `grep -q` SIGPIPE under `pipefail`); commits in window
- **Mediajunkie:** commits in window — mail-sweep script refactor (detect-vs-enumerate pattern, already covered in 10/01 brief); not separately reported
- **Globe** (commits: fire logs, brief deliveries): not brief-worthy
- **Weather** (commits: UTC timestamp fix, KPAO station switch logged and confirmed): operational fixes, not cross-pollination-worthy
- **One Job, nyt-crossword:** brief deliveries and automated prints; not brief-worthy
- **Atlas, Cuneo, Optilisten:** no commits in window

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
