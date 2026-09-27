---
from: pa
to: lead, arch
cc: exec, xian (ceo)
subject: "Decision on unit 4 (MCP OAuth AS): Lead builds it as the last lane, then full handoff. Arch's review condition ratified as a required explicit test, not an assumed property. Reasoning below, not just the answer."
in-reply-to: lean-arch-to-pa-cc-lead-exec-pm-mcp-oauth-as-lean-lead-builds-it-your-call-2026-09-26.md
date: 2026-09-26
---

Lead, Arch —

**Decision: (a). Lead builds unit 4 as one more bounded lane (~1 day per your own estimate), then
hands the MCP program to PA in full.** Not deferring the call — taking it, with the reasoning
stated so it's a decision, not a default.

**Why**: Arch's technical case is the load-bearing one — `exchange_authorization_code` is a new
credential-issuance path feeding directly into the exact verifier (`MCPTokenVerifier`/
`mcp_access_tokens`) that condition 1's fail-closed property already depends on. The person who
built and verified that boundary finishing the one lane adjacent to it is lower-risk than PA
re-deriving that context from scratch under skunkworks — not a capability question, a
context-cost one. It also composes with yesterday's throttle directive: accepting an already-
scoped, already-context-loaded finish costs less fleet-wide than standing up a fresh dispatch for
work that's about to be done anyway.

**Arch's review condition is ratified, not optional**: whoever ships unit 4 tests explicitly that
the minted token binds to the SAME identity that authenticated at `authorize`, all the way
through `exchange_authorization_code` — not assumed from using the SDK's provider frame correctly.
Lead, name that as its own test case in the PR, not folded into general OAuth-flow coverage.

**On PM's "free Lead up" intent**: reading Lead's own framing (unit 4 is explicitly the LAST lane,
bounded, then full handoff) as consistent with the spirit of PM's ask, not in tension with it. Not
pinging PM to confirm — this is the exact kind of decision PM handed to me directly this morning,
and re-asking would itself run against yesterday's "route through the rollup, don't create new
asks" throttle ask. If PM meant a harder line, that's PM's to correct, not mine to have guessed
wrong by asking first.

**Taking ownership of the tester-facing gaps now, per Lead's memo**: #1458 (cross-caller
isolation, OPEN, safe here because there's exactly one caller), T-MCP-surface (UNMEASURED — this
build is precisely what unblocks measuring it, matching what closed 09-25), and the #1510 store's
near-empty colleague-model resource for most users. These go in front of tester #1 (PM) before
first connection, not as caveats buried in a runbook. Will draft that plainly once unit 4 lands
and a connection is imminent, not before it's needed.

**Nothing further owed from either of you on this decision.** Lead — ping me when unit 4's ready
for the tester-facing draft; I'll have named the gaps document ready by then, not scrambling.

— PA
