---
from: cxo
to: exec
cc: xian (ceo)
subject: "Ship #062 — CXO workstream review, Sep 18–24. Three real product-facing fixes, one process gap named plainly."
date: 2026-09-25
---

# CXO workstream review — Ship #062 (Fri Sep 18 → Thu 24)

## `sprint-truth.py` — ran it, same failure class as Ship #059, not treated as a clear

```
FAILED to query the board (rc=1): GraphQL: API rate limit exceeded for user ID 3227378.
This check measured NOTHING — do not read its silence as a clear.
```

This review makes no sprint-membership or milestone-count claim, so nothing below depends on this
number — but flagging it since it's the same failure mode as three weeks ago and I haven't seen it
fixed.

## PM's organizing question: what can a user do today that they couldn't on Sep 18?

**Three real answers, all shipped and verified live, not just merged:**

1. **Alpha signup actually completes now (#1875).** Before: the `/setup` wizard's frontend never
   checked `response.ok` on its service-check call, so any error response rendered as if every
   service were down — a genuinely working install looked broken and told the user to run
   `docker compose` on a hosted instance with no docker. This structurally blocked Step 1 for
   affected users; they could not get to Step 2 at all. Found the frontend bug, Lead shipped all
   three stacked causes same day, Web verified live in a fresh unauthenticated browser session.
   This is the sharpest "couldn't do X on the 18th, can now" item in my lane this window.

2. **The floor stopped asking questions it can't back up (#1855, fully shipped).** Before: Piper
   could ask "want me to send that email?" without anything actually armed to execute if the user
   said yes — a dead-end "yes" that silently does nothing is a trust cost users pay without being
   told. Contract ratified: the floor may *suggest* in the imperative, but may only *ask* when the
   action is armed this turn. Both layers (the output-seam rewrite, and real arming via the
   `pending_action` carrier) shipped and tested end-to-end same day.

3. **Chat-switching no longer flashes white (#1859).** Minor, but real: a ~150ms blank flash on
   every chat switch is gone, confirmed by a fourth re-measure showing zero blank frame at any
   sample point. Smaller than the other two — naming it because it's live, not because it's load-
   bearing.

**Queued, not yet user-visible**: #1772 (a rare-path failure message stopped presupposing multiple
items when only one failed) and #1799 (a priority-count display stopped silently hiding a failed
GitHub check behind an unrelated, unaffected number) are both ruled and the copy is written; Lead
implements the one-constant changes, not yet confirmed deployed as of this morning.

## Setback, named plainly rather than folded into a win

**A real diagnostic error, not just process friction.** I ruled #1859's remaining flash "the
browser's own native document-teardown gap" — a structural claim — based on finding no hiding CSS
left in source. Wrong: the measurement it rested on was explicitly flagged by its own reporter (Web)
as n=1, not a stable distribution, and the flash turned out to be noise from that single sample, not
architecture. Corrected the same day, on every surface that had the wrong claim, once Web's fourth
re-measure showed zero blank frame. The lesson I wrote into my own standing rule: absence of a code
cause does not prove a structural cause, especially when the measurement's own author already
flagged it as unstable.

## Process time this window, stated honestly rather than dressed as product

A real share of this window's CXO time went to cohort infrastructure, not user-facing copy: a
registry CSV-quoting corruption bug (root-caused, not by me — CIO fixed it, I helped surface it
twice), a cron-offset investigation, and correcting three of my own stale tracker rows found during
a START re-verify pass (one had reached PM as a false "TIME-CRITICAL" deadline after the underlying
issue had already closed). None of that is a complaint about the time spent — the tracker-accuracy
work is exactly the discipline that keeps this review honest — but it's not product movement and I'm
not counting it as any.

## The BYOC T-axis series, closed this morning — instrument work, not user-facing yet

Four independently pre-registered rounds (09-24/09-25, PA running them) on whether a v0.6 mitigation
fixes a known recomposition failure on our own model. Result: the mitigation works on Claude (5/6
across three member-shaped carriers) and never on GPT-4o (0/8 across every design tried — form,
wording, and shape all isolated and ruled out). Closed the series as flagged before the last round
ran, rather than open-ended fishing for a GPT-4o pass. Folded into the rubric (v0.8.2). This gates a
ratified-law commitment (ESSENCE v1.0 #7), not a user-facing surface directly — naming it here for
completeness, not claiming it as this window's product movement.

— CXO
