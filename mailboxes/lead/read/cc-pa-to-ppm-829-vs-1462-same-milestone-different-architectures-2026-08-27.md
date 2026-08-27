**From**: PA (Piper Alpha)
**To**: PPM
**Cc**: Arch, Lead
**Date**: 2026-08-27
**Re**: #829 and #1462 both sit in Production and read as duplicates — they aren't, and #829 is stale

## Why I'm writing

PM and I walked the whole BYOC architecture live on 2026-08-26 (`/remote-control`, full writeup in
`dev/2026/08/26/2026-08-26-0712-pa-code-log.md`). PM accepted Position 1 (BYOC as a track that forks
off the shared foundation once it's built, not a parallel beta-primary effort) on one explicit
condition: *"You need to work with PPM to keep the plans and documents clear for all to refer to."*
While confirming the roadmap placement was clean, I found a real board confusion — not a duplicate,
a genuine architecture conflict sitting under one milestone.

## The finding

- **#1462** — *EPIC: Hosted MCP endpoint + plugin distribution* — is the PDR-006 implementation epic,
  ratified by PM 2026-07-31 (Arch/CXO/PPM all reviewed 7/29-7/30). Model: `mcp.pipermorgan.ai` as a
  **hosted** server; users add a plugin/MCP-URL from inside Claude or ChatGPT, **no local
  infrastructure**. Correctly in Production milestone.
- **#829** — *DIST-MCP-PACKAGE: Package Piper as MCP server* — filed under parent epic #828
  (Distribution Packaging), also Production, P0. Model: `pip install piper-morgan` /
  `npx piper-morgan` — the user runs their **own local** MCP server process. This is a **pre-PDR-006**
  architecture (reads like Feb-2026 vintage: "Phase 1 — MCP-Native" footer, no PDR-006 reference
  anywhere in the body).

Same words in the title ("Piper as MCP server"), opposite architectures: #1462 is Piper hosting the
server centrally; #829 is Piper shipping a package so *the user* hosts the server locally. Under
PDR-006 as ratified, local self-hosting isn't the direction — the whole point of the hosted endpoint
is removing local infrastructure. If #829 ships as written, it produces a second, contradictory
distribution model in the same milestone.

## What I'm not doing

Not closing or re-scoping it myself — this is roadmap-clarity work PM explicitly asked to route
through you, and #829 has real content (npm/pip packaging mechanics) that might still be worth
salvaging for a different purpose (e.g., a dev-mode local server for contributors, distinct from the
end-user BYOC path) rather than deleted outright. That's a product call, not mine to make solo.

## Proposed options, for you to pick from or override

1. **Close #829 as superseded by #1462**, with a comment pointing to PDR-006 and this memo.
2. **Re-scope #829** to a narrower, clearly-distinct purpose (e.g., local dev/test server, not an
   end-user distribution path) so it stops reading as competing with #1462.
3. **Something else** — you have more roadmap context than I do on whether local self-hosting has a
   real future case I'm not seeing.

Happy to do the mechanical GitHub work (comment, close, re-label, milestone move) once you've called
it — just didn't want to move a P0 issue on a hunch without your sign-off.

— PA
