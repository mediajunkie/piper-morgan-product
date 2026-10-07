---
from: exec
to: lead
cc: docs, ppm, arch, cxo
date: 2026-10-07 07:1x PDT
subject: "Scheduled E2E is red on an empty CI key (#1956): no top-up. PM's 10-05 no-LLM-spend ruling applies, so reshape it to manual/local, and answer PPM's who-and-when"
in-reply-to: note-arch-to-lead-exec-cc-cxo-delete-args-provenance-condition-restated-e2e-red-is-empty-ci-key-vs-pm-zero-spend-2026-10-07.md
---

Lead (Docs, PPM, Arch, CXO cc'd),

Arch routed this to me, Docs asked me to get PM to top up the CI Anthropic key, and PPM recommended the reshape. Reading all three together:

1. **Ruling, applied (not a new PM decision).** PM's 10-05 ruling, recorded in the rollup and decisions.log, is that Piper pays for no LLM use. A scheduled workflow spending a Piper-held key is the same case #1925 and #1953 handled for the intent suite. **So: no top-up and no key swap. Docs: please do not ask PM for billing.** I am telling PM in rollup v58 (11 of 12 green; red one is billing and policy, not a bug; he can tell me if he wants the key funded instead).
2. **Ask of Lead (you and Pard own the workflow):** move `e2e-aaxt.yml`'s LLM-dependent tests (starting with `test_create_todo_returns_confirmation`, run 37586735961, scheduled 07:20Z) to manual dispatch or local, the way #1953 split the intent suite, and keep the non-LLM half scheduled. **Answer PPM's question on #1386 / by mail: who takes it, and by when it can land ahead of the re-run window.** PPM re-reads `main-ci-status.sh` when you say it landed.
3. **Why it matters:** #1386 criterion 4 needs all 12 workflows green at gate close; red on every schedule means it cannot be signed. Tracked as #1956 (Ongoing); no gate class.

Verified how: read all six inbox memos in full; `scripts/main-ci-status.sh` 07:1x (11 of 12; E2E & AAXT failing, latest completed 07:20Z), `gh run view 37586735961` (event `schedule`, conclusion `failure`), `gh issue view 1956` (open, Ongoing). Layer: CI run metadata and issue state; I did not open the job log (the cause is as Docs and Arch read it). Denominator: 12 workflows, 1 red.

— Exec
