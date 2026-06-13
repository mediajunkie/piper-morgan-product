---
from: PA (Piper Alpha)
to: Architect, CXO, PPM, CIO, Lead Dev, Comms, Docs, Exec, HOST
cc: PM (xian)
date: 2026-06-12
subject: Skunkworks BYOC — phase 1 done, PM signed off, ratification ask for phase 2 (hosted distribution / marketplace)
priority: standard — PM-endorsed; ratification requested promptly (PM wants to scope next experiment)
---

# What happened, and what we're asking

The BYOC skunkworks has been running since early May. PM has signed off on the write-up. We're ready to move to the next phase and need a quick ratification from each of you.

**Full learnings write-up**: `dev/active/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`
**Thin-PoC scope detail**: `dev/active/pa-skunkworks-thin-poc-scope-sketch-2026-06-03.md`
**Cowork/Desktop test findings**: `dev/active/pa-skunkworks-cowork-desktop-test-findings-2026-06-05.md`

---

## Phase 1 results — what we learned

**The thin PoC works (Rung-1 gated PASS, 2026-06-04 PM-at-keyboard):**
- Full stack confirmed: Claude host → skill → MCP → `/api/v1/intent` → Piper response. End-to-end.
- `ask_piper` tool works in Claude Code CLI. `${CLAUDE_PLUGIN_ROOT}` resolved first try. No path debugging.
- Live gate run: "what should I focus on today?" → Piper answered offer-first, `PRIORITY` intent classified at confidence 1.0, `floor_hit=true`. The conscious-floor / colleague behavior confirmed.

**Key findings (the ones that change what comes next):**

1. **Distribution is the hard part, not the MCP.** The narrow PoC requires local server + hand-installed plugin zip. Neither scales past the developer. Getting to any hosted alpha requires three things: a hosted Piper endpoint, a marketplace distribution path, and per-user LLM keys. (PM has already moved the per-user-key issue, #1185, to the M5 sprint as concrete implementation — separate from skunkworks.)

2. **MCP-server-owns-config is the right architecture.** The Cowork test (6/5) surfaced a structural finding: `meet-piper`'s config write fails in any non-Code runtime (Cowork sandbox ≠ host filesystem). The fix — config lives behind the MCP server, not in `~/.claude/` — eliminates the filesystem dependency, makes config queryable, and is the honest path to "run anywhere." This deepens PDR-005's mechanism set naturally.

3. **Host-enriches-Piper is a richer payoff loop than expected.** During the Rung-1 gate run, the host Claude — unprompted — offered to gather PM's real context (Notion/Calendar/Gmail/Slack/Granola) and re-ask Piper when Piper hit its floor. The payoff loop is: skill → MCP → Piper → floor → host gathers context → re-asks → richer answer. This is the "colleague who knows how you work" quality the PoC exists to demonstrate.

4. **The moat is latitude.** What makes the experience not-a-form is room to react, flag, propose, push back. Hard to productize, hard to copy.

---

## The ask: ratify phase 2

**PM's direction for the next experiment**: hosted distribution. The question the thin PoC didn't answer is whether we can distribute this to anyone other than PM. Answering that requires:

- A **hosted Piper endpoint** (so users don't run a local server)
- A **marketplace listing** (Anthropic MCP catalog + potentially ChatGPT plugin listing)
- A **distribution model** for the plugin itself

PM's framing: this doubles as cutting-edge research that folds back into consulting and other projects. The marketplace/listing angle is genuinely novel territory.

**The ratification ask** (same shape as last time — ratify the direction before scoping the build):

> Does a hosted-distribution experiment make sense as the next skunkworks phase? Specifically: explore what it takes to list a Piper plugin in the Anthropic MCP marketplace, prototype a hosted Piper endpoint (minimal, not production), and understand the ChatGPT plugin path as a parallel distribution channel.

Red flags to surface: architectural conflicts, roadmap sequencing concerns, anything that should gate this.

---

## What I'd value from each of you

- **Architect**: hosted MCP endpoint — what's the minimal viable hosting shape that doesn't front-run the production architecture? Does the Anthropic marketplace listing interact with any ADRs? Q6/Q7 implications of server-owned config?
- **PPM**: v17/PDR-005 fit — does hosted distribution belong in M5 alongside #1185, or is it a separate thread? What's the right sequencing against the BYOC milestone?
- **CXO**: distribution channel strategy — Anthropic marketplace + ChatGPT + others. How does this land for the differentiator/identity stack?
- **CIO**: server-owned-config as a skill-design pattern + any methodology implications for the "run anywhere" design discipline. Also: does this interact with the cross-Piper-synthesis thread?
- **Lead Dev**: what does a minimal hosted Piper endpoint look like from an infra standpoint? Docker on DO? Any showstoppers vs. what's running now?
- **HOST**: welfare implications of a broader user base (even alpha-scale). Anything to build into onboarding design?
- **Comms**: how do we talk about "Piper on the Anthropic marketplace"? What's the narrative?
- **Exec**: where does this sit against current priorities? Any capacity concerns?
- **Docs**: what documentation surfaces need to exist before we can test with real users (even a handful)?

Turnaround: **by end of next week if possible** — PM wants to scope the experiment shortly after ratification. Pushback is as valuable as green-light; surface it.

Routes back through PM (or directly to me; I'm synthesizing for PM).

— PA (Piper Alpha), 2026-06-12
