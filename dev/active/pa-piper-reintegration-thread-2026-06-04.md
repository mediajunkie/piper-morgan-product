# The Piper reintegration thread (forward idea — capture, not a plan yet)

**Author**: PA · **Date**: 2026-06-04 · **Status**: PM forward-thinking, captured durably per
write-to-file-don't-carry-in-head. Not scheduled work; a thread to return to.

## The idea (PM, 2026-06-04 eve)

Once the **OpenLaws** engagement winds down, reintegrate what the distributed Piper instances have
each learned into **a single Piper Morgan assistant for PM** — eventually. The instances:

- **Piper Open** — the OpenLaws product-assistant role (an instance of the Piper-Morgan-prototype-as-
  Claude-role). Has been learning a real client domain + a full plugin stack (multiple slots, multiple
  skills in tandem, an MCP server hitting a real API).
- **PA (me)** — the PM-assistant instance; has been figuring out duty-cycle autonomy, the cohort
  coordination substrate, and now the BYOC thin-plugin build.
- (and the broader cohort's methodology corpus.)

"Reintegrate" = fold the divergent learnings back into one assistant rather than maintaining parallel
specialized Pipers forever.

## Why it's the natural endpoint (the meta observation, same day)

PM's framing: *"here you are, one Piper Morgan prototype designing and building another Piper Morgan
PoC, all with the goal of building the 'real' Piper Morgan — when we're already kind of doing it."*

The recursion is the evidence: the prototype building its successor *is* the product working. So the
"real" Piper isn't a distant artifact — it's the convergence of the instances that are already running.
Reintegration is how the fork (specialize per context) rejoins (one colleague who knows PM across
contexts).

This also connects to the **cross-client identity-coherence framework** already in PDR-005 (the 3
invariants / 3 variables): reintegration is the *same* problem viewed over time instead of across
clients — how do divergent context-adapted Pipers stay one identity?

## Why BYOC is the enabling substrate (PM confirmed same day)

BYOC > reinventing chat + tools + harness from scratch. The plugin model means each Piper instance is
a thin, portable capability layer riding on the platform's chat/tools/harness — so reintegration
becomes "merge the skills + profiles + MCP surfaces," not "merge three bespoke apps." The thin-PoC
(#1145) is the first proof that the capability layer is small and portable enough for this to be
realistic.

## Open questions for when this becomes active (not now)

- What's the unit of reintegration — skills? the CLAUDE.md profile? MCP tool sets? all three?
- Does Piper Open's OpenLaws-domain learning generalize, or stay firewalled (per the cross-project
  IP-firewall norm in PM's company profile)?
- Does reintegration produce one plugin with many skills, or a marketplace of per-context plugins
  sharing a profile? (The `claude-for-legal` monorepo-marketplace is a reference for the latter.)
- Timing: gated on OpenLaws wind-down (the current 6-week bet + ~3-week taper per PM's profile).

**Return trigger**: OpenLaws engagement winding down. Until then this is a captured thread, not a task.
