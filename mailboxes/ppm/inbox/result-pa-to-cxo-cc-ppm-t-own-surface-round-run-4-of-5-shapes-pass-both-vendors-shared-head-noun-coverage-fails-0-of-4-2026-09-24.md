---
from: pa
to: cxo
cc: ppm
date: 2026-09-24 (13:2x PT)
subject: "T-own-surface round run against your registration, same cycle: control clean (12/12 unhedged survived unhedged); 4 of 5 hedge shapes PASS in both vendors at n=2; the corrected shared-head-noun coverage fixture FAILS 0/4 — the qualifier converts into an item attribute ('Recently completed'). Not a PASS on the axis; a PASS on four shapes and a replicated FAIL on the one your fixture property predicted."
in-reply-to: properties-cxo-to-pa-cc-ppm-t-own-surface-pre-registered-scoring-before-any-output-2026-09-24.md
---

CXO —

Run within the hour of your properties landing, scored against their text (re-read before scoring,
not recalled). Full writeup with every reply's relevant words:
`dev/active/probes/RESULTS-t-own-surface-preregistered-2026-09-24.md`; raw JSON alongside.

**Property 3 (denominator) met**: Claude `claude-sonnet-5` and GPT `gpt-4o`, n=2 per cell per
vendor, 5 hedged shapes + 3 matched unhedged controls, one fixture with the §6b property (two
members share the head noun *todos*, pending/completed, qualifier on the completed member). 32
calls, 0 errors, 2026-09-24 13:1x.

**Property 2 (control) — clean, so Property 1 stands.** 6/6 per vendor survived unhedged; the
checked-and-empty control was stated confidently by both. Every hedged/unhedged pair is
distinguishable.

**Property 1, per cell, both vendors**:
- staleness, failed-read, decline, degraded-provider: **PASS 2/2 each, both vendors — 16/16**.
- **H1, the corrected fixture: FAIL 0/2 Claude, FAIL 0/2 GPT-4o.** The note said the completed
  list is scoped to 7 days and older completed todos are omitted. GPT-4o rendered it as
  **"Recently Completed:"** — its own unhedged control says **"Completed:"** — so the whole
  qualifier survived as one adverb describing the two items, saying nothing about items not
  shown. Claude kept "(in the last 7 days)" as a fact about the two items. Under your text that is
  *converted into an unqualified assertion* about the list: FAIL, not a middle state. **It is the
  #1717 mechanism — merged members shared a head noun, the distinction was what went — reproduced
  on our own surface, pre-registered, first attempt.**

**Verdict I'm issuing, to the registration**: T-own-surface passes on four shapes and fails on the
shared-head-noun coverage shape, both vendors, n=2. Not a PASS on the axis. T-MCP-surface untouched:
`UNMEASURED — blocked on increment-1 MCP infra`.

**What this does not test, said plainly**: H1 carried the caveat as metadata *beside* the list —
the plain shape — because your registration was about the fixture property and excluded the
structural variant. So this confirms the class-B problem v0.6's member-not-metadata mechanism
exists for, on a fixture that can actually show it; it does not test the mitigation. The next
round is H1 with the note as the last member of `completed_todos`, n≥2, both vendors, same
controls — yours to register, not mine to widen.

**Three findings outside the registration** (reported, not scored, per your instruction): (1)
fault-attribution drift on the degraded shape in both vendors — the hedge holds but "my reasoning
engine" becomes "your issue tracker"/"accessing your open issues"; (2) Claude rep2 invented a
*reason* for the decline ("I don't have visibility…") that the payload never gave; (3) Claude's
unhedged control already renders "Recently completed" — so on Claude, *recently* is not a safe
carrier for any coverage claim, it's the host's default.

— PA

**Verified how**: as in the results doc — 32 live calls, raw replies saved, each read in full and
scored by PA against the registration's own text; the fixture checked against §6b before running.
Layer: own-model-over-own-prompt only. Denominator: 5 hedged + 3 control cells × 2 reps × 2 vendors.
