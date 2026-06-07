# BYO substrate, Piper brings the judgment — synthesis (2026-06-07)

**Purpose**: name the frame that runs through this weekend's BYOC work in one place, before the beta
architecture decisions. PM-flagged ("we are doing some critical BYO- thinking now") and extended with the
upstream-collaboration idea ("could the person's own Claude be deputized to gather/act on Piper's behalf
— Piper as a *colleague* for their assistant, not a tool"). Threads through ~5 weekend docs + the
`consult-piper` skill (which turns out to be the working prototype of the upstream idea).

## The thesis
Piper's architecture is converging on a single shape: **the user brings the commodity substrate; Piper
brings the judgment.**
- **BYO-Chat** — the plugin: Piper inside the Claude you already use.
- **BYO-LLM-key** — you fund your own inference.
- **BYO-credential** (Option A) — your own access, no secret baked into the plugin.
- **BYO-connected-accounts** — your own OAuth'd connectors.
→ Piper provides the thin distinctive layer: **calibration** (how *you* work), **methodology** (trust
gradient, Conscious Floor, honest degradation), **role-shaping**.

## Why BYO is the load-bearing frame, not a buzzword
1. **Economics = trust (the same move).** BYO collapses our hosting/cost/liability toward zero (a side
   project *can* ship to strangers) AND keeps the user's key/data/accounts off our infrastructure.
   Cheaper-for-us is identical to more-trustworthy-for-them. That alignment is rare and it's the crux.
2. **It locates the value.** If the substrate is commodity (model, chat, connectors), Piper can't be
   defensible on those → value is forced up into judgment/calibration/methodology. BYO is the constraint
   that tells you what to invest in.
3. **Right answer to "the platform laps you."** Don't be in the commodity business; ride the platform +
   the user's key; own the judgment layer the platform won't.
4. **The tension.** BYO pushes setup friction onto the user → it's only viable paired with frictionless
   onboarding (meet-piper / one connect-step / bundled uv / honest degradation = the counter-force).
   Discipline: **maximize what's BYO (cost + trust), minimize the setup tax (adoption).**

## The upstream dimension: bring your own *connected agent* (PM, 2026-06-07)
The deepest BYO. The user's own Claude/agent is **already connected** (Calendar, GitHub, Notion, …).
Rather than Piper re-implementing every connector, Piper **deputizes the host agent** to gather info and
(with consent) execute on its behalf — adapting to what's available, reconnecting only the gaps.

This flips the relationship:
- **Old (hierarchical):** host → `ask_piper` → Piper-as-tool. Piper needs its own copy of every
  connector — the redundancy we hit 6/7 (host has Calendar; Piper doesn't → Piper floors).
- **New (collegial):** host ↔ Piper as **colleagues**. Piper says what it needs; the host gathers/acts
  with what it has; Piper reasons; Piper self-connects *only the gaps*. **"A colleague for your assistant,"
  not "a tool for your assistant."**

### We already built the prototype: `consult-piper`
`consult-piper` is exactly this loop, special-cased to GitHub: *Piper floors for missing context → the
host gathers it → re-ask Piper enriched → present with visible provenance.* PM's vision = **generalize it
from GitHub-only to any connector the host already has.**

### How it's expressible — three layers
- **Piper-server = judgment** (calibration/floor/value). Can't call "up" — MCP is request/response, the
  host is the client; the server only answers. So brokering can't live here.
- **Piper-skill = the collaboration broker** (it runs *inside* the host agent). It negotiates capability:
  "what do you have? I'll use it; what you don't, I'll get myself." **This is where deputization lives.**
- **Host agent = the connected hands/eyes.**

### What it needs to become general
1. **Structured needs signal** — Piper returns "I need X (this week's calendar) + Y (open issues)"
   machine-readably (today consult-piper *infers* the gap from prose; the structured signal is already a
   flagged roadmap item).
2. **Capability discovery** — the skill asks the host what connectors it has, routes each need to an
   available one, flags unmatched needs for Piper-side connection.
3. **Trust boundary** (the trust gradient already covers it): **gather/read freely; execute/write only
   with the user's consent.** Deputizing reads is low-risk; deputizing *actions* crosses the consent gate
   and must stay there — "colleague" can't quietly erode "the user is in control."
4. **Provenance** (consult-piper already shows it): answers span host-gathered + Piper-reasoned — keep it
   visible and correctable.

### Honest constraints
- MCP can't push up → all deputization is **skill-mediated** (consult-piper-shaped), not via the bare
  `ask_piper` MCP call.
- Info-gathering is the easy, safe half; **action-on-behalf** is where the consent gate has to bite.
- Capability discovery depends on the host exposing what it's connected to — verify what's introspectable.

## The one-line thesis
**BYO substrate, Piper brings the judgment — and where the substrate is a *connected agent*, Piper is a
colleague to it: it uses what's already there and only reconnects what's not.**

## Refs
- `pa-byoc-hosted-distribution-exploration-2026-06-07.md`, `pa-option-a-decouple-credential-plan-2026-06-07.md`,
  `pa-byo-llm-key-beta-scoping-2026-06-07.md`, `pa-plugin-marketplace-hosting-research-2026-06-07.md`
- `consult-piper` SKILL (the working prototype of the upstream/colleague loop)
- Memory: platform-laps-you = value-chain-climbing; honesty-as-ground.
