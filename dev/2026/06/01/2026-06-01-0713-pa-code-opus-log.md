# Session Log: Piper Alpha — June 1 (Monday)

**Date**: June 1, 2026 (Monday)
**Started**: 7:13 AM PDT
**Role**: Piper Alpha (PA) — PM Assistant
**Tool/model**: Claude Code, Opus — slug `pa-code-opus`
**Continuation of**: `dev/2026/05/31/2026-05-31-1505-pa-code-opus-log.md` (May 31 — wrapped/day-closed this AM)
**Worktree**: `…/.claude/worktrees/modest-dhawan-9346b7` on `claude/modest-dhawan-9346b7` (harness auto-worktree; functions as Model-A — see CIO memo 5/31)
**Phase**: Day 5 of Model-A duty cycle (Day 1 = 5/28). Cron UNREGISTERED (PM-engaged).

---

## START — 7:13 AM PDT (PM AM engagement)

**PM directives (7:13 AM)**:
1. Wrap up the May 31 log (day-close).
2. Start today's log (this file).
3. PM read the skunkworks docs — they look good, with **a slight clarification on plug-in architecture
   + what we should build**. Wants the **architecture discussion → update docs → distribute/lock**.

**Session-start hygiene**: sync hit the known regen-noise merge-abort; cleared blocking MANIFESTs +
delta digests (canonical on origin) and re-merged clean. Origin had substantial overnight Lead Dev work
(R4 suggestion-provenance design, fires 5–9, cross-poll brief 2026-06-01). PA inbox: no new items beyond
the v17 draft file + Arch #1016 memo (informational, still unprocessed).

**Carry-state into today**:
- **Skunkworks fan-out** — HELD. Was pending PM final-signoff; PM has now read the docs (✅ "look good")
  but wants an **architecture-clarification discussion + doc update BEFORE distribute/lock**. So the gate
  shifts from "signoff" to "architecture discussion → doc update → distribute."
- Drafts ready: full writeup + fan-out cover (DRAFT-held) + v17 roadmap bridge — all on origin/main.
- v17 §M5 review delivered to PPM (5/31); Daedalus referent correction sent.
- check-branch.sh fix still pending Lead; discovered-work weekly sweep Fri 6/5; methodology-34/Outcomes
  smoke test Day 28-29.

**NEXT**: hear PM's plug-in-architecture clarification → discuss → update the skunkworks docs (writeup +
cover + bridge) to reflect the agreed architecture → then distribute/lock.

## Architecture clarification from PM (7:42 AM) — LOAD-BEARING

**Canonical packaging correction**: the canonical package for an Anthropic plugin is **the plugin
itself** (typically hosted, also installable from a zip) — **NOT an MCPB (bundle), NOT a hosted MCP**.
The OpenLaws Legal plugin is the reference example. A plugin **contains**:
- conventional config files, including a **CLAUDE.md template for its own use**
- one or more **Skill files**
- the **MCP server**
- optionally **bundled `uv`** if the MCP is Python (or write the MCP in Node)

**This corrects the docs' framing.** v17 §M5 + my bridge described a "Gall's-Law sequence (MCP server →
**MCPB** → Project template → MCP Apps)" implying MCPB is the packaging target. Per PM, the **plugin is
the canonical unit**; MCP server is a *component inside* it. Doc update needed (writeup + bridge), and
worth flagging the same correction up to v17/PDR-005 (PPM/Arch lane).

**Thin skunkworks plugin PoC architecture (PM)**:
1. the **plugin wrapper + core files**
2. **several skills**: the onboarding skill (cold-start, built) + **one or more Piper-specific skills
   (PM + PA to discuss which)**
3. a **minimal MCP server**
4. likely **work to make the PM API visible to the MCP server** (dependency — Lead/Arch lane)

**OPEN DESIGN Q (discussing now)**: which Piper-specific skill(s) for the thin PoC. PA lean: pick one
that exercises BOTH the MCP→real-API path AND reads/honors the captured profile (the payoff loop).

## PM refinements + PA endpoint investigation (June 1, ~7:50 AM) — CAPTURED LATE (was only in conversation)

**PM corrections to the architecture discussion**:
1. **Legal-plugin attribution is WRONG in the docs.** The reference is the **Anthropic legal plugin**
   (which PM studied *at* OpenLaws to reverse-engineer undocumented conventions), **NOT the OpenLaws
   legal plugin**. PA does **not** have the Anthropic legal plugin directly — the skunkworks writeup
   anchored on the OpenLaws-derived `install-guide-code-2026-05-11`. **Doc fix needed**: correct
   "legal-prior pattern (OpenLaws)" → "Anthropic legal plugin (studied at OpenLaws)"; if PM points PA
   at the Anthropic plugin, study it directly.
2. **Marketplace** is the wrapper level above plugin — **out of scope** for this skunkworks.
3. **PM's Gall's-Law build order** (supersedes PA's "thin architecture" framing): (1) identify a slice
   of Piper's unique value + the API call the front end uses for it → (2) write a very thin MCP server
   for that one call → (3) install + test it conversationally → (4) write a skill guiding the agent to
   use the MCP for a Piper thing → (5) install + test → (6) iterate. **MCP-first, smallest piece.**
4. PM confirmed **B+C** direction; github/issue-tracking is practical but **commodity, less uniquely
   Piper** — prefer the uniquely-Piper thing.

**PA endpoint investigation (grounded in the route tree, `web/api/routes/`)** — to answer step 1:
- **`POST /api/v1/intent`** (`intent.py:213`) — the conscious-floor engine; front end's core call.
  Body `{message, session_id}`; **auth OPTIONAL** (graceful degradation unauthenticated). → a thin MCP
  can POST a message with **zero token plumbing** = fastest to stand up + test (steps 2-3). Most
  literally-Piper call. **Caveat (Lead/Arch)**: it's the full engine — may *execute* actions for some
  intent types; scope the PoC to query/propose-type intents or confirm propose-only.
- **`GET /api/v1/insights`** (+ `/confirm`, `/correct`, `/why`; `insights.py`) — trust-graduated
  proactivity. Read-path; maps ~1:1 to the B+C skill AND the captured trust-gradient profile fact.
  **Caveat**: requires auth → needs the token / "make API visible" work first.
- **`GET /api/v1/knowledge/query`** (`knowledge_graph.py`) — context-methodology read; weaker demo.

**PA REVISED RECOMMENDATION (flipped from yesterday's insights-first lean)**: start with **`/intent`
as the Gall's-Law smallest-working-piece** — auth-optional makes it the thinnest, fastest first rung,
and it's the most central Piper value. Skill on top = the B+C "ask Piper to read your situation +
propose your next step, in your voice." Then **sequence `/insights` as rung 2** (needs auth anyway; the
richer trust-gradient showcase).

**⏳ OPEN — AWAITING PM DECISION**: `/intent`-first → `/insights`-second (PA rec) **vs.** insights/
trust-gradient showcase first (even with auth cost). PM had not answered when June 1 conversation ended
(last msg was a stray-keystroke clarification). **This is the live thread to resume.**

**Lead/Arch scoping Qs queued**: (a) does `/intent` stay propose-only for targeted intents? (b) cleanest
auth path for `/insights`?

---

## DAY-CLOSE WRAP (June 2, 6:34 PM — retroactive; continued in `dev/2026/06/02/...`)

**June 1 net**: skunkworks architecture discussion with PM — packaging-model corrected (plugin canonical,
not MCPB), Gall's-Law MCP-first build order set, B+C skill direction confirmed, endpoint investigation
done, `/intent`-first recommendation made. **Did NOT converge on the skill/endpoint decision** — that's
the top open thread. Skunkworks fan-out remains HELD (now pending: architecture-corrected doc updates →
distribute/lock).

**Loop closed since**: PPM absorbed all 4 §M5 review items into v18-draft (`memo-ppm...v17-m5-absorbed
...2026-06-02`). v18 awaits CIO §Methodology fill-in before PM ratification.

**Sign-off**: branch `claude/modest-dhawan-9346b7` (auto-worktree, NOT main); `HEAD == origin/main`
verified; nothing stranded.

## Memory & briefing surfaces referenced (#974 pilot)
**Referenced**: `feedback_write_to_file_dont_carry_plans_in_head` (this late-capture is the exact
failure mode it guards — deferred logging "until convergence," convergence didn't happen, nearly lost
the endpoint investigation across a day boundary); `feedback_endpoint_discovery_search_full_route_tree`
(drove the `web/api/routes/` investigation, not just `services/api/`); `feedback_no_flattened_commands_
without_referents` (Daedalus referent; legal-plugin attribution honesty). **Loaded not referenced**:
publishing/blog memories. **Wanted not found**: the Anthropic legal plugin reference itself (PA doesn't
have it).

→ DAY CLOSED. Continued June 2.
