# BYOC hosted-alpha readiness checklist

**Filed**: 2026-09-15 (PA). Phase A deliverable named in
`dev/active/byoc-parallel-work-plan-2026-09-15.md`. **Not a new requirements list** — #1462 (the
ratified hosted-MCP epic) already has the complete requirements/AC/sequencing structure; this
document is a live-status pass against it, plus the ownership mapping the parallel-work plan needs
(who does each open item, without touching Lead's queue) and a single ordered start-here sequence.
Re-verify against #1462 directly before treating any row here as current — this is a snapshot, not
the source of truth.

## Status against #1462, checked 2026-09-15

| Item | #1462 status | Actual status (verified) | Owner (per parallel-work plan) |
|---|---|---|---|
| `mcp.pipermorgan.ai` deployed (DNS/TLS) | unchecked | **Not started.** No DNS, no TLS. | Phase B — Arch or prog |
| Auth (OAuth preferred, API-key fallback) | unchecked | **Not started.** Design ratified (ADR-070 D3), not built. | Phase C — prog |
| Caller-identity resolution, fail-closed | unchecked | **Not started.** This is #1458 — open, and confirmed absent from the current MVP epic order (checked again this fire). | Phase C — prog |
| Tool catalog derived from registry, situation-named | unchecked | **Not started.** Naming-test (situation vs. object-shaped) also not run — shares a rig with the recomposition probe, neither built yet. | Phase A (test design) now; Phase C (build) — prog |
| Colleague-model resources-for-reads/tools-for-writes split | unchecked | **Not started** — no server exists yet to split. | Phase C — prog |
| Claude plugin package assembled | unchecked | **Design substantially done, not activated.** `dev/2026/08/30/plugin-manifest-draft-2026-08-05.md`: `name` is the only required field, remote MCP (`http`/`sse`/`ws`) confirmed supported, license resolved (Apache-2.0). Deliberately not placed at the live `.claude-plugin/plugin.json` path — that would make this repo itself a discoverable plugin, a decision nobody's made yet. | Phase A/B — activation is a small, low-risk decision once Phase B's server exists |
| ChatGPT path (remote MCP + skills) | unchecked | **Not started**, and gated on the deployment existing at all. | Phase C — prog |
| Recomposition rubric branch (#1463) | unchecked in #1462 | **Design-level answer landed, T-axis still open.** Rubric is v0.7 — PA's member-not-metadata mechanism passes cleanly in both vendors on the one shape tested. `#1462`'s checkbox is stale; the honest state is "informs design, cannot issue a formal pass" — not simply unchecked. | PA — ongoing, no build dependency |
| Fail-closed identity, verified by test | unchecked | **Not started** — depends on the identity layer existing. | Phase C — prog |
| First-contact / cold-start demonstration | unchecked, "the only criterion that fails today" per PDR-006 | **Currently fails**, confirmed. This is the single load-bearing product claim across both PDR-006 and #1386. | Cross-cutting — not a BYOC-only fix |
| ChatGPT honest-decline ("equivalent core capabilities") | flagged false-as-written | **CORRECTED this fire — better than represented.** A failure-shaped payload framing already tests at 6/6 (100%, matching Claude) — PA's own N=6/cell probe, 2026-08-02, whose result was in #1462's body but never made it back into PDR-006 (fixed this fire). Real remaining gap: provider-API-direct evidence, not tested against a deployed host — a deployed-host retest is owed, not an open capability question. | PA (design) done; retest owed once Phase B exists |

## What this changes about "ready to test"

Two items that read as open capability gaps are actually **closed at the design level, pending
verification once infrastructure exists**: the recomposition mitigation (member-not-metadata) and
the honest-decline mitigation (failure-shaped payloads). Neither needs more design work. Both need a
deployed `mcp.pipermorgan.ai` to retest against. This means Phase B (the DNS/TLS stand-up) is more
load-bearing than it looks — it's not just infrastructure, it's the precondition for closing out two
of the harder-sounding open questions with a retest rather than new design work.

## Start-here sequence, given all of the above

1. **Phase B first**: stand up `mcp.pipermorgan.ai` (DNS/TLS only, no app logic, near-zero MVP risk).
   Unlocks retesting both the recomposition and honest-decline mitigations against the real host.
2. **In parallel with 1, Phase A**: finalize the tool-catalog naming-test design (shares a rig with
   the recomposition probe — build both instruments together).
3. **Once 1 lands**: hand #1458 (identity isolation, fail-closed) to prog — this is the actual
   pre-user gate, and per the architect conditions in #1462, foundational, not a hardening pass done
   later.
4. **Once 3 lands**: tool catalog build (derived from registry) + first connector implementations,
   also prog.
5. **Plugin package activation** (moving the manifest to its live path) is a small, late, low-risk
   step — sequence it whenever the server is far enough along to be worth pointing a plugin at, not
   earlier.

## What this checklist does not resolve

The plugin-activation decision (making this repo a discoverable Claude Code plugin) and the
milestone/timeline question for #1462 itself (currently milestone-unset, PM-gated) are both
decisions for someone else to make, named here so they don't get assumed by omission.
