# BYOC parallel-work plan — proceeding alongside MVP, not through it

**Filed**: 2026-09-15 (PA), following PM's direct ruling in conversation, 2026-09-15.
**Owner**: PA (planning/design lane), with build phases routed to prog rather than Lead.
**Status**: ACTIVE — approved by PM in-conversation, pending this write-up as the reference doc.

## PM's ruling — the actual constraint, quoted so it can't drift

> "I think that parallel work is okay if it doesn't distract from lead developer and if we don't
> merge anything that causes any problems with the MVP. In other words MVP is still the top priority
> and we're on a convergence path with it. We could possibly do alpha testing of BYOC at the same
> time but the ultimate test should be that we're not derailing the MVP milestone. If you can put
> together a plan that doesn't step on the toes of the lead dev and the current work underway, then
> I'm comfortable with having things proceed in parallel."

Two hard conditions, one soft permission:
1. **Must not distract Lead Dev** from MVP.
2. **Must not merge anything that risks the MVP milestone.**
3. **Permitted, not required**: real BYOC alpha testing may run concurrently with MVP, *if* the
   above two hold.

MVP remains the top priority and the convergence path is not to be perturbed. This plan exists to
satisfy those conditions structurally, not by good intentions per-PR.

## What's actually true right now (checked, not assumed — 2026-09-12/15)

- `mcp.pipermorgan.ai` is **not deployed**. No DNS, no TLS, nothing live.
- **#1458** (cross-caller state isolation, hosted MCP endpoint) is **OPEN, unstarted**, and — checked
  again 2026-09-15 — **does not appear anywhere in the current MVP epic order**
  (`dev/active/mvp-epic-order-2026-09-09.md`). It is not folded into the reopened security/tenancy
  epic (epic 2). It is genuinely unclaimed BYOC-only work.
- The cold-start demonstration criterion (PDR-006's single load-bearing product claim) currently
  fails.
- ChatGPT's honest-decline capability sits at ~50% vs. 100% on Claude (PA's N=6 probe, still current).
- The recomposition-rubric instrument (#1463) is closed with a design-level answer (v0.7, PA's
  member-not-metadata mechanism) but its T-axis remains `PENDING-PROBE` — informs design, can't issue
  a pass.
- There **is** a coding-agent capacity distinct from Lead already in active, regular use: `prog`
  session logs exist most days (four separate instances on 2026-09-15 alone), doing scoped side-work
  (e.g. #1816) outside Lead's main epic queue. This is the mechanism that makes condition 1 satisfiable
  without inventing anything new.

## The plan — three phases, split by who it costs

### Phase A — design/planning, zero engineering cost, PA-driven, running now

Touches no codebase. Cannot distract Lead or risk any merge, by construction.

- Hosted-alpha readiness checklist (the concrete list of what must be true before a real tester
  touches `mcp.pipermorgan.ai` — deployment, #1458 closed, catalog built and naming-tested, cold-start
  demonstration passing).
- Tool-catalog naming-test design (situation-shaped vs. object-shaped tool names — PPM's open
  question in PDR-006, sharing a rig with the recomposition probe).
- Keep PDR-006 and the recomposition rubric current as real work lands (already doing this — caught
  and fixed a stale PDR-006 citation 2026-09-12).

### Phase B — infrastructure-only, low blast radius, not necessarily Lead's

`mcp.pipermorgan.ai` DNS/TLS stand-up. Arch already flagged this as upstream of everything else on
this path and it is pure deployment configuration — it does not touch application code, so it
carries near-zero risk to the MVP codebase even if it lands before MVP closes. Candidate owner: Arch
or a prog instance, not Lead.

### Phase C — real build (the #1458 fix, first MCP tool implementations)

This is where condition 1 actually bites — genuine coding-agent capacity that would otherwise
compete with MVP. **Proposal: route this to a prog instance, not Lead's queue.** The mechanism
already exists and is already used for exactly this shape of scoped-off work. Lead stays fully on
MVP; BYOC gets real engineering progress without ever touching Lead's plate.

## Merge discipline (satisfies condition 2, mechanically)

Nothing from Phase B or C merges to `main` without an explicit check, stated in the PR itself, that
it does not touch any file/path referenced by the current MVP epic order or any in-flight MVP issue.
A one-line "checked against `mvp-epic-order-2026-09-09.md`: no overlap" statement, verified before
merge, not assumed. If a future BYOC PR *does* need to touch shared code, that's the trigger to stop
and ask, not to proceed on the theory that it's probably fine.

## What "alpha testing concurrently" would require, if PM wants it

PM's ruling permits, but doesn't require, real testers touching BYOC while MVP is still converging.
That would need at minimum: Phase B done (server actually reachable), #1458 closed (safe under
multiple simultaneous testers), and the cold-start demonstration passing. None of that exists yet —
naming it here so it's not silently assumed to be closer than it is.

## Next concrete step

Build the Phase A readiness checklist first (no dependency on anyone else's time) — that's what
actually unblocks handing Phase C to a prog instance with a real spec to build against, rather than
a prog instance re-deriving the same PDR-006/ESSENCE reading PA already did.
