---
from: Lead Developer (lead)
to: Piper Alpha (pa)
cc: PM (xian) — informed in-session
date: 2026-06-19
subject: "Heads-up: the MCP standup-skill is on the hollow path — migrate to the honest engine sooner rather than later (#1289)"
---

# Heads-up: the MCP standup-skill needs migrating to the honest standup engine (#1289)

PA — a heads-up on one of the MCP skills you've been assembling, flagged directly by PM (2026-06-19) so it's on your radar early.

## What
The **MCP standup-skill** — `services/integrations/mcp/skills/standup_workflow_skill.py` — still calls the **hollow `MorningStandupWorkflow`** (`services/features/morning_standup.py`), the legacy standup path that fabricated "time saved / efficiency" vanity metrics.

## Why it matters now
#1269 shipped the **honest standup engine** — `build_user_standup_summary(user_id)` / `StandupAssembler` (`services/standup/assembler.py`). It *derives* the standup from the live Radar EntitySources (no fabrication; conversations dropped; "Watch" not "Blockers"; capped top-N). It's now live on three surfaces:
- the **chat** standup (`IntentService._handle_standup_query`),
- the **/standup page** (`GET /api/v1/standup/today`),
- the **Slack-chat** path (via `process_intent` → the honest engine).

The MCP standup-skill is **the one surface still on the hollow path.** PM tested the Slack-chat standup today and it's honest ✓ — but anyone hitting the MCP-skill surface would still get the old fabricating output. Since it's a *fabricating* path, that's a real honesty gap, not just a stale format.

## The ask (PM: sooner rather than later)
Migrate the skill to call the honest engine instead of `MorningStandupWorkflow`:
- `build_user_standup_summary(user_id)` → `.to_prose()` (narrative) / `.to_dict()` (structured) — the same shape your `_format_for_slack` already consumes.
- #1289 tracks retiring the hollow `MorningStandupWorkflow` entirely.

Not hard-blocking, but flagging now so it doesn't linger. Ping me for wiring details — I'm happy to hand you a dict-shape adapter for the existing `_format_for_slack` consumer, or pair on the swap.

— Lead Dev, 2026-06-19
