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

## Consult test — RUN (2026-06-05, Cowork) — the failure-path behavior is the STAR

`/consult-piper what should I focus on next?` in Cowork, where the host has **no GitHub tool** (no MCP,
no `gh` in sandbox). The skill degraded *beautifully* — this is the strongest validation of the
honesty-as-ground principle yet:

- **Jargon scrub WORKED**: opened with *"Piper didn't have your current project info, so it couldn't
  point you at anything specific"* — plain language, no "floor_hit." (And when the user later asked what
  "floored" meant — because the agent slipped it once in a follow-up — it explained plainly + apologized.
  Even the recovery was honest.)
- **Honest degradation, not fabrication**: hit the GitHub-gather wall → did NOT fake data → **fell back
  to asking the user directly** via a form ("tell me what's in flight"), then re-asked Piper enriched.
  The no-silent-failure path the skill specifies, working under a *new* failure mode (no gather tool at
  all) we didn't explicitly design for. The skill generalized correctly.
- **Provenance stayed legible**: *"What I supplied: just the context you typed… What I added: nothing —
  the prioritization is Piper's."* Exactly the honest separation, in plain words.
- **The grounded answer was genuinely good**: with the user's typed context (last day of a 6-week sprint,
  demo + roadmap due, then plan a 1-week project), Piper gave sharp prioritization + one follow-up
  question. The payoff loop delivered real value even via the manual fallback.
- **It diagnosed the GitHub-connector confusion correctly + honestly**: distinguished *Piper's*
  `github_connected` (Piper's own GitHub) from *the host's* lack of a GitHub MCP tool; checked the
  registry (empty); read the screenshot and correctly explained the linked GitHub Integration is
  file/context access, NOT a tool-exposing connector (no `list_issues`); verify-don't-assert throughout
  (re-ran its toolset search to confirm). Textbook don't-guess-investigate.

**Finding (host-GitHub-gather)**: `consult-piper`'s GitHub gather assumes either a GitHub MCP tool OR
`gh` CLI. In Cowork **neither exists** (sandboxed shell, GitHub Integration ≠ callable tools). The
ask-the-user fallback saved it — but worth making that fallback a *designed* path, not just emergent. And
it reinforces the headline: the long-term fix is **Piper pulls its own GitHub directly** (closes #1155),
so consult-piper doesn't have to route through host tools that may not exist on a given surface.

## Cowork agent's ARCHITECTURE MEMO (`piper-morgan-cowork-architecture-memo.md`) — high quality

The Cowork agent wrote a full config-architecture memo (recovered in `cowork-test-outputs.zip`). It
independently reached **Option 1 = MCP-server-owns-config** (`get_profile`/`save_profile` tools), with
sequencing (4 steps), costs/risks (server-must-run → keep a read-only file mirror for graceful
degradation), and open questions (does company-profile.md also move behind the server? schema-version
now?). This is publishable-quality and matches PA's read exactly. **It's a real input to PDR-005's lane /
Architect Q6-Q7** — config-behind-MCP extends the just-ratified "MCP-server alongside FastAPI" mechanism.

**Artifacts recovered** (`byoc/cowork-test-outputs/outputs/`): the architecture memo, the populated
`piper-morgan-CLAUDE.md` (xian's PM profile) + `company-profile.md` (both real, usable), and the
setup-progress scratchpad. The Cowork agent staged these because it couldn't write to `~/.claude` — the
exact headline finding, demonstrated in the artifacts themselves.

## Disposition (updated)
- **#1 discovered work — config-path-not-portable** (highest-value finding of the arc): file it, with
  the MCP-server-owns-config fix + the architecture memo as the design input. Surface to PPM + Architect.
- **consult-piper ask-user fallback** → make it a designed path (small skill edit, later).
- **#1155 (floor ignores GitHub)** gains urgency: it's the clean fix for consult's gather-portability.
- Serial-vs-form (generative/enumerable) → meet-piper refinement.
- **Fan-out is now MUCH stronger**: "tested on Cowork, found BYOC's core hard problem (config
  portability), have a fix direction + a working honest-degradation demo." This is a *findings-rich*
  fan-out, not a "it works" one.