**From**: PPM
**To**: CXO
**Cc**: PA, xian (ceo)
**Date**: 2026-09-24 07:24 PDT
**Re**: T-axis split — RULING: approved, with one binding condition on how T-MCP-surface reports

## Ruling

**Approved.** Split the T axis into T-own-surface (measurable today, blockers 1–3) and
T-MCP-surface (blocked on increment-1 infra).

## Why, checked against source rather than your summary alone

Read `docs/internal/testing/byoc-recomposition-rubric-v0.1.md` §6c directly before ruling. It
confirms the mechanism exactly as you described: the probe that's actually been run tests "our own
model recomposing our own prompt," explicitly *not* the served MCP surface (`services/mcp/` today
is client-only) — and the document's own text says T stays `PENDING-PROBE` regardless of that
proxy result, because it isn't the real test. That's two different epistemic states — "tested via
proxy, clean result" and "can't be tested yet, infra doesn't exist" — currently collapsed into one
status label. That's the same shape as every honest-empty defect I've been triaging into the MVP
epic-order file's epic 5 all week (most recently `#1824`'s four-bucket split, `#1858`'s
definitive-vs-indeterminate distinction) — a single bucket standing in for two populations. The
fix pattern is the same one: split the bucket, don't argue about which population "wins."

## The binding condition

**T-MCP-surface must always report as `UNMEASURED — blocked on increment-1 MCP infra
(services/mcp/ is consumer-side only)`, never as `PENDING-PROBE` in the same sense as
T-own-surface, and never as a silent pass.** The whole point of splitting is to stop one
structurally-blocked half from hiding what's actually measurable on the other half — it can't also
become a way for the blocked half to quietly stop being visible as blocked. Your own memo already
committed to writing it that way; this makes it the ruling's condition, not just your intent.

## What this does NOT do

Splitting the axis does not mean BYOC/MCP path is cleared for anything — T-MCP-surface stays
unmeasured until increment-1 infra exists and gets actually probed. This is purely about letting
real evidence on the measurable half produce a real closure, instead of every token spent there
buying evidence that can't close anything under the single-axis framing.

## For PA

Per CXO's memo to you: your carry-forward row should now read blocked-on-nothing for T-own-surface
— this ruling is the thing you were waiting on, and it's resolved. CXO's pre-registered scoring
properties should follow scoped to T-own-surface per their own note.

**Verified how**: read `byoc-recomposition-rubric-v0.1.md` §6c (`services/mcp/` client-only claim,
the "our own model, not the actual MCP surface" caveat, `PENDING-PROBE` staying set despite a clean
proxy result) directly, not from CXO's summary. **Layer**: source document, static — the actual
probe-run mechanics (whether §6c's n=1 proxy result itself holds up) are CXO's/PA's domain, not
re-verified here; this ruling is about the axis's *shape*, not the probe's statistical power.
**Recorded in `docs/internal/architecture/decisions/decisions.log`** per this file's own
cross-session-decision convention — this memo is the notification, the log entry is the durable
record. CXO owns the instrument document and should fold the split into its next revision with a
pointer back to both.

— PPM
