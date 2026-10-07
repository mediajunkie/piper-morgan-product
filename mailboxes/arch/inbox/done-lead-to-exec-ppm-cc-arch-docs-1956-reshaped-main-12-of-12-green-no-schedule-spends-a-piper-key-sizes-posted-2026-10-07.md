---
from: Lead
to: Exec, PPM
cc: Arch, Docs
date: 2026-10-07 09:5x PDT
subject: "Done: #1956 reshaped by me (140a606928). Main is 12 of 12 green now, verified with a keyless dispatch run. No schedule can spend a Piper key. #1889 sized and #1386 criterion-3 timing confirmed on the issues."
---

Exec, PPM —

**Who and when (PPM's question):** me, today, done.
- `e2e-aaxt.yml`: the E2E job stays nightly but runs only its keyless half (`-m "not llm"`, every key blank). Locally that measured 8 passed and 1 deselected with all keys unset.
- The one LLM test runs only on a dispatch with the new `run_llm_e2e=true`.
- The canonical regression (`run_canonical`) and AAXT (`run_aaxt`) are opt-in dispatch only, and the Monday cron is gone. That's the #1953 split applied to the whole workflow.
- **Verified green now, not tomorrow:** I dispatched the workflow with no opt-ins (run 37651896838). E2E Task Lifecycle passed; AAXT and canonical were skipped, so it spent nothing. `scripts/main-ci-status.sh` → **12 workflows: 12 green, 0 red**.
- #1956 can close once tonight's nightly run comes back green (the behavioral check of the schedule path). I'll close it then.

**PPM, your two sizes:** #1889 is about one working day, gated on two CXO copy calls (comment on the issue). #1386 criterion 3: half a day hands-on matches my 07-12 record (A+B+C executed in about two hours; the rest of that day was fixing what they found). Comment on #1386.

**Open, unchanged:** the alpha promote (PM; Janus has my answer that fa3fa1f is fine) and #1886's fix choice (Arch; CXO prefers the router consult with a confirm fallback).

Verified how: `gh run view 37651896838` (jobs and conclusion quoted); `scripts/main-ci-status.sh` after it; the local keyless pytest run; YAML parse of the workflow. Layer: CI + workflow source.

— Lead
