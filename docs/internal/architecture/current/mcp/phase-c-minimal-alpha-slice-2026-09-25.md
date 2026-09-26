# MCP Phase C — minimal alpha-testable slice

**Author**: Arch · **Date**: 2026-09-25 · **Trigger**: sprint plan Fri 09-25 → Thu 10-01, PM theme
"getting to beta and getting the mcp to alpha testing" — "Arch defines the minimal alpha-testable
slice; Lead deploys. Target: an endpoint an alpha tester can actually connect to this sprint."
**Scope of this doc**: what ships THIS sprint, not the full #1462 epic. #1462 and PDR-006 remain the
governing documents for everything deferred here.

## Two "Phase" numberings exist for the same rollout — naming this so it stops colliding

- **Exec's Phase A/B/C** (decisions.log 2026-09-23) is the *infra rollout* framing: A/B were DNS/TLS
  assignment on Fly (PA/Pard, done — "Phase B done" per this morning's kickoff). **C is "application-
  code concerns"** — building the actual server.
- **#1462's own Phase 0/1/2/3** (PDR-006 implementation epic) is the *build sequencing* inside that
  application code: 0 = build-independent probes, 1 = identity boundary + auth, 2 = tool catalog +
  connectors, 3 = plugin package + ChatGPT path.

**Exec's "Phase C" = #1462's Phases 0-3, in total.** This doc scopes a slice *inside* #1462's own
Phase 1, not a fourth numbering. Use #1462's numbers when talking about build sequencing; use Exec's
letters only for the infra-vs-app-code distinction.

## Current state, verified this fire, not assumed from the epic's age

- `services/mcp/` holds `consumer/` and `protocol/` — **no `server/` directory exists**. This is a
  from-scratch build, confirmed today via `ls`, not carried from the epic's 09-01 finding.
- **#1458 (cross-caller state isolation) — still OPEN**, verified via `gh issue view` this fire.
- ⚠️ **CORRECTED 2026-09-25 evening (CXO) — this bullet cited a stale version.** As of v0.8.2
  (this morning), the rubric's T-axis **split into T-own-surface and T-MCP-surface.**
  **T-own-surface** now has real, pre-registered results across four closed rounds: a known
  fixture (shared-head-noun coverage claims) fails on both vendors; a tested mitigation fixes it on
  Claude but never on GPT-4o (0/8 across every design tried) — a specific finding, not a pass.
  **T-MCP-surface remains genuinely `UNMEASURED — blocked on increment-1 MCP infra`** — and that
  binding condition is *this Phase C build*. Once this resources-only slice ships, T-MCP-surface
  stops being permanently blocked for the first time — the first real tester's client actually
  recomposing one of these resources is the first live opportunity to move it off `UNMEASURED`.
  **The risk framing below is unchanged by this correction** — CXO confirmed it directly: "accepted
  for one named tester this sprint; not resolved" is exactly the rubric's binding condition, and
  T-MCP-surface may never be silently treated as a pass. Only the version/status text was stale.

## The scope decision: ONE named tester, READ-ONLY resources, ZERO tools, THIS sprint

**Ship #1462 Phase 1 (identity boundary + auth) for real, at full rigor — not scoped down.**
Condition 1 (fail-closed caller identity) is not a multi-tenant hardening pass to defer; it's the
property that makes a single real tester's real data safe to serve at all. "No identity, no read;
never default to anonymous" holds whether there's one caller or a thousand. **Nothing about a small
alpha earns a shortcut here** — build it to the PDR's own standard, verified by the PDR's own
acceptance criterion (an unresolvable-identity call reads nothing; caller A cannot reach caller B's
state, even if there is no live caller B yet to test against).

**Defer #1462 Phase 2's tools and full registry-derived catalog. Ship resources only, and a small,
explicitly-named handful of them** (user profile, colleague model summary, one connector's read —
whichever connector the named tester already has authorized). Reasoning:

1. **Resources are app-controlled reads; tools are model-controlled mutations** (condition 3,
   already ratified). A read-only slice is categorically lower-risk than anything that can act on a
   user's behalf, and it's enough to demonstrate real value.
2. **The epic's own first-contact criterion — "the user's own data appears in the first exchange,
   unprompted" — is satisfiable with resources alone.** It does not require a single tool. This is
   the exact criterion the epic flagged as the one thing the current AC set can't fail on; a
   resources-only slice can actually be judged against it honestly, this sprint.
3. **The "consequential refusals as failure-shaped payloads" AC (PA's 6/6-vs-1/6 finding) is a
   TOOL-response problem** — it's about what a *tool call* returns when it refuses. Zero tools means
   this AC doesn't apply yet, honestly, not by omission. Don't claim it passed; state it's out of
   scope for this slice.
4. **The tool-naming A/B test (situation-shaped vs. object-shaped) has nothing to name yet.** Also
   correctly out of scope, not a gap.
5. **#1458's cross-caller risk is real only once there's a caller B.** Scoping to exactly one named,
   identified tester for this sprint doesn't relax condition 1 (still built and verified in full),
   but it does mean #1458's own remaining untraced surfaces (Redis, floor/context state,
   rate-limiting *under anonymous callers*) aren't yet live risk for a slice with a real, resolved
   identity and no second caller. **Naming this explicitly, not assuming it silently**: #1458 stays
   OPEN and un-discharged; this slice does not close it, and adding a second tester before #1458
   closes would be the wrong move without re-checking this reasoning.
6. **The recomposition rubric's `T-MCP-surface` axis — `UNMEASURED, blocked on increment-1 MCP
   infra` — is the one real accepted risk in this scope, and this build is the thing it's blocked
   on** (corrected 09-25 evening, CXO — was previously mis-cited from a stale v0.4 as
   `PENDING-PROBE`; `T-own-surface`, the sibling axis, has real closed results this rubric doesn't
   need re-litigated here). A resources-only slice still recomposes through someone else's chat
   client, so the honesty-under-recomposition question is live even without tools. **Flagging this
   as a known, accepted gap for a single named tester, with a forward-looking hook**: once this
   slice ships, `T-MCP-surface` stops being permanently blocked — the first tester's client actually
   recomposing a resource is the first live chance to move it off `UNMEASURED`, not just a risk to
   carry. Rather than silently
   treating a resources-only slice as automatically safe from the concern it was raised for.

**Auth**: OAuth preferred per ADR-070 D3; for a single named tester this sprint, an API-key fallback
is acceptable **only if the identity it resolves to is the same real, fail-closed identity condition
1 requires** — the fallback lowers assurance of *how* the key was obtained, not the fail-closed
property of what happens once it's resolved. Don't let "just use an API key for the alpha" become an
identity-boundary shortcut; it's a transport convenience, not an exemption.

**Connector reads**: resolve via logical keys per ADR-070 Amendment A (bindings, not literal URLs) —
this is already the standing pattern, not a new decision for this slice.

## What this sprint does NOT ship, named so nobody infers otherwise

- Any tool (mutating or not) — zero tools this sprint, by design, not by running out of time.
- The full registry-derived tool catalog (condition 2) — nothing to derive a catalog *of* yet.
- The plugin package or ChatGPT path (#1462 Phase 3).
- #1458's closure — cross-caller isolation remains an open, tracked gate; this slice's safety rests
  on there being exactly one real caller, not on #1458 being resolved.
- A passing recomposition-honesty verification — the risk is accepted and named for a single tester,
  not resolved.

## Acceptance for THIS slice (not #1462's full AC list)

- [ ] `mcp.pipermorgan.ai` serves an MCP `initialize` handshake and exposes resources only (no
      tools in the capability set).
- [ ] Fail-closed identity, verified by test: an unresolvable-identity call reads nothing; there is
      no code path to a default/anonymous owner.
- [ ] The one named alpha tester's real profile/colleague-model/one-connector data appears via a
      resource read, in the client they're actually using (Claude or ChatGPT, whichever they pick).
- [ ] This doc's named-gap list (#1458 open, rubric T-axis pending) is stated to the tester or to
      whoever manages tester communication — not silently accepted on their behalf.

## Escalation trigger back to Arch

If reaching this slice turns out to need a mutation (a tool) for any reason — including something
as small as "let the tester correct a wrong profile field" — that's a scope change past what this
doc rules, and it re-opens conditions 2/3's full weight (tool catalog shape, consequential-refusal
payload shape) rather than sliding in unreviewed. Flag it; don't build around it quietly.

**Verified how**: `services/mcp/` directory contents checked live via `ls` this fire (not assumed
from the epic's age); `#1458` state checked via `gh issue view` this fire. **Correction, 09-25
evening**: the rubric's T-axis status originally cited (`PENDING-PROBE`, from CXO's 09-02 memo) was
itself stale by 09-25 morning (v0.8.2 split it into T-own-surface/T-MCP-surface) — CXO caught this
directly against the rubric's own current file, not against my citation. Layer: live repo state +
issue state + prior memo (original) / live rubric file (correction), all verified before writing.
Denominator: this doc scopes one sprint's slice of #1462's Phase 1; it does not re-verify or
re-scope Phases 2/3, #1458's fix, or the rubric's own probe design.
