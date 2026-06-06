# Skunkworks BYOC plugin — Cowork/Desktop test findings (2026-06-05)

**Source**: PM ran the v0.2 plugin in Claude Desktop / Cowork, 6/5 PM. Two tests: `meet-piper` (full
interview) + a `consult` run (pending paste). **Tracking**: #1145.
**Status**: findings captured live (write-to-file; too valuable for the transcript only). Feeds the
fan-out memo + discovered work.

## HEADLINE FINDING — the config-path is a CLI-first assumption that breaks in Cowork (structural)

`meet-piper` writes the profile to `~/.claude/plugins/config/dinp/piper-morgan/CLAUDE.md`. In **Claude
Code** the agent owns the home filesystem → trivial. In **Cowork** the agent's file tools are scoped to
connected folders + a session scratchpad, and its shell is a separate Linux sandbox that doesn't mount
real `$HOME` at all. So a skill whose whole job is "write to `~/.claude`" hits a wall — specifically:
- **Catch-22 observed**: Write refused (path exists, must Read first) + Read refused (path outside
  connected scope). Neither tool can touch `~/.claude/...` from Cowork.
- **Agent's workaround (good)**: staged both fully-populated files in its outputs folder + gave a
  one-line `cp` install command. No data lost, surfaced honestly.

**This is the SAME CLASS of finding as the 5/31 rung-1 runtime/filesystem mismatch** (Cowork shell ≠
host). The plugin keeps making CLI-first filesystem assumptions that Cowork (a key BYOC target surface!)
violates. The "run anywhere" thesis demands surviving non-Code runtimes.

## THE FIX (agent's #1, and I concur it's the right direction): MCP-server-owns-config

Instead of `meet-piper` writing a file, it ends by calling a **`save_profile` / `get_profile` tool on
the local Piper MCP server**. The server becomes the single source of truth — reachable identically from
Claude Code, Cowork, or anywhere the MCP is connected. **No agent-filesystem dependency at all.** Bonus:
config becomes *queryable* (a tool), not a file someone has to parse.

**Why this is strategically big — three connections:**
1. **It's the honest fix for the whole surface-portability problem.** The config-path breakage on Cowork
   (and any non-Code host) disappears if config lives behind the MCP, which is the one thing guaranteed
   reachable wherever the plugin runs.
2. **It deepens PDR-005's mechanism set.** PDR-005 already commits to "MCP-server packaging alongside
   FastAPI" — this says the MCP server should *also* own user-config read/write, not just intent. A
   natural extension of the just-ratified canonical mechanism.
3. **It's a concrete step toward the reintegration thread.** "One Piper across surfaces" needs one
   source of truth for who-you-are; server-owned config IS that. Config-behind-MCP is how Piper Open +
   PA + future instances could share a profile.

Alternatives the agent named (kept for the record): (2) config in a user-chosen connected folder
(Cowork-native but fragments the canonical-path assumption); (3) a Cowork-sanctioned config dir (platform
change, not plugin-doable today). **#1 (server-owns-config) is best-first.**

## SECOND FINDING — serial-vs-form: the real axis is GENERATIVE vs. ENUMERABLE

PM (as tester): "some of this would have been ok as a form." The agent articulated it well: strict
one-question-at-a-time is elegant in a terminal and **earns its keep for generative voice/posture
questions** (the interview demonstrates the serial cadence it's collecting — self-proving). But
**enumerable/list-shaped inputs** (the integrations list, the per-project pace table) are *better as a
form / multiple-choice* — serial is over-applied there. The agent baked this distinction into the
captured profile's serial-questions rule. Good finding; matches the Cowork-form-affordance point from
the 5/31 test.

## THIRD — connector visibility quirk
GitHub showed NOT wired in the Cowork session despite being a live connector elsewhere → PM will try
reconnecting before the next test. (Affects `consult-piper`'s GitHub gather; the skill's gh-CLI fallback
may not exist in Cowork's sandbox either — watch the consult result.)

## Disposition
- File discovered-work: **config-path-not-portable** (the headline) — likely the highest-value issue
  from this whole skunkworks arc, since it gates BYOC's multi-surface promise.
- The MCP-server-owns-config architecture = a real design proposal for PDR-005's lane / Architect Q6-Q7;
  surface to PPM + Architect (the Cowork agent is drafting an architecture memo on it too — that's a
  separate artifact; this is the skunkworks-side record).
- Both findings strengthen the fan-out: "we tested on a second surface and learned exactly what BYOC's
  hard problem is (config portability), and have a fix direction." Far stronger than "PoC works."
- Serial-vs-form (generative/enumerable) → a `meet-piper` refinement for a later rung.

## Consult test — PENDING (PM pasting next)