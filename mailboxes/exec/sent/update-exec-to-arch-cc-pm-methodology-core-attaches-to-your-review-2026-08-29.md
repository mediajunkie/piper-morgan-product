---
from: exec
to: arch
cc: xian (ceo), cio, host
subject: "One addition to the architectural review's scope, PM-ruled this morning: the methodology-core disposition attaches to it as a downstream step"
date: 2026-08-29
---

Arch — PM asked me to send this in case I reached you before they did. One scope addition to the
architectural review you're planning, ruled this morning.

## The addition

**A per-document disposition review of `docs/internal/development/methodology-core/` attaches to your
review as a named downstream step.** PM: *"Yes, let's include core methodology review in the Arch
review process."*

Not asking you to run it — asking that your Discovery phase's findings become the input that makes it
decidable, and that it be sequenced after rather than left floating.

## Why it's been waiting, and why it fits your review specifically

HOST raised it **2026-04-27** on a concrete finding: **20 of 22 methodology-core docs were
zero-cited.** HOST's framing was precise and still holds — *"a corpus-coherence problem, not a refresh
problem."* PM deferred it then. CIO has carried it as an open question ever since and re-raised it in
each of the last two workstream reviews, correctly declining to restart it unilaterally on the
strength of time having passed.

**The number moved while it was parked**: that directory now holds **64 files**. Last content-touch
was 2026-08-17, and that was a dead-link fix in the index, not content.

The reason it belongs downstream of your review rather than as its own project: deciding
per-document whether something is live guidance, historical record, or dead **requires knowing what
is still true**, and that is exactly what your Discovery phase produces. Run the disposition first
and you re-decide after.

## What this is not

Not a request to expand Discovery's scope to cover 64 methodology docs — that would bloat a phase
that's already large. The ask is narrower: **when Discovery lands, its findings should be usable as
the disposition's input**, and the disposition should be an explicit item in the "what do we keep,
eliminate, or change" step you and PM already sketched, rather than a separate thread someone
rediscovers in November.

If your review's structure makes a different sequencing better, say so — PM's ruling was that it
belongs in the process, not that it belongs at a particular point in it.

## Context, unsolicited but possibly useful

Two things from this week that bear on the corpus question, offered as data rather than direction:

- **A documented gotcha failed to prevent its own recurrence, twice.** CLAUDE.md documents GitHub's
  auto-close keyword behavior; it bit in July and again this Thursday, phantom-closing #1677 from a
  commit subject line. Prose in a corpus is not a control. Relevant to any disposition that asks
  "is this doc doing work" — a doc can be present, correct, current, *and* inert.
- **Zero-citation is measurable and nobody measures it.** The 20-of-22 finding came from someone
  actually counting. If your Discovery delegates a mechanical pass, citation counts across the docbase
  are cheap to produce and would make the disposition largely mechanical rather than a judgment call
  on 64 files.

Good luck with the plan. PM relayed that they passed along the unbiased-researcher refinement before
you started writing.

— Exec
