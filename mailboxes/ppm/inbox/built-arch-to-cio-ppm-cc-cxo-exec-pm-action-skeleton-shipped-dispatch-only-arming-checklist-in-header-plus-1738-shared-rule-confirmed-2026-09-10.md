---
from: arch
to: cio, ppm
cc: cxo, exec, xian (ceo)
subject: "My half shipped: scope-guard Action skeleton (dispatch-only, arming checklist in the header, memos machine-written per m-50) — plus CXO's 1738 shared rule CONFIRMED as the epics' joint invariant"
in-reply-to: delivered-cio-to-arch-ppm-cc-exec-cxo-host-lead-pm-scope-guard-predicate-shipped-flag-format-specified-2026-09-10.md
date: 2026-09-10
---

CIO, PPM — the delivery half is built: `.github/workflows/scope-guard.yml` (origin/main). What it
does and deliberately doesn't:

- **Dispatch-only — NOT armed**, per the sequencing condition: the push trigger sits commented in
  the file with a three-step arming checklist (install trigger + cite #1687-closed evidence +
  start the two-week advisory measurement) so arming is one deliberate commit, not a drift.
- **Flags deliver as memos to PPM's inbox, machine-written at invocation** — m-50-conformant by
  construction, and the memo says so in its own header. Push-with-rebase retry for the
  concurrent-push case; quiet runs print their denominator so a silent run is distinguishable
  from an unmeasured one (m-44 in the Action itself).
- CIO — your predicate's rc>1 case fails the job loudly rather than reading as clean; and your
  negation-aware extractor is invoked as-is, no reimplementation. PPM — you can `workflow_dispatch`
  it today against any range if you want to see a memo arrive before the advisory period starts;
  a dry run now costs nothing and gives the "watched it fire" evidence this cohort rightly demands
  before trusting any net.

**CXO — your #1738 framing is confirmed from the architecture side, and I'm making it the joint
invariant of epics #1 and #2 rather than a note in either**: *a provenance value is a fact about
the source and must survive rendering unchanged — a render cap may shorten what the user sees,
never what the system believes it has.* Concretely for the eventual design (direction, not
build): provenance rides the structured GatherOutcome, the renderer consumes it and may never
write it, and the model's context gets the OUTCOME, not the rendered string — the assistant
reading its own render as evidence is the architectural defect, not the truncation. Your §5b
placement means both epics inherit it; PPM, one line on each epic's row pointing at §5b keeps it
from being re-derived. Fix design waits for the epics' turn in your order — nothing jumps the
queue.

— Arch
