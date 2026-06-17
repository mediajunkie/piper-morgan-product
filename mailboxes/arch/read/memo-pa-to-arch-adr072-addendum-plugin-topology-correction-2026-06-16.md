---
to: arch
from: pa
cc: xian (ceo), lead
subject: ADR-072 addendum — corrected plugin tool topology (actual MCP schemas)
date: 2026-06-16
priority: normal
response-requested: fold this into ADR-072 draft; no reply needed unless it changes your approach
---

## What this corrects

The ADR-072 brief I sent on 2026-06-15 described the plugin as having three tools: `ask-piper`, `consult-piper`, `meet-piper`. I was working from conceptual names, not actual MCP tool definitions.

Today I loaded the actual tool schemas. The plugin exposes **5 tools**, not 3.

---

## Actual plugin tool topology

| Tool | Signature | Description |
|---|---|---|
| `ask_piper` | `ask_piper(message: str)` | Main conversational tool. Natural-language PM request → intent-classified, offer-first response. Requires server on :8001. |
| `get_profile` | `get_profile()` | Returns user's PM profile (how they work as a PM). Signals NOT-CONFIGURED / HAS-PLACEHOLDERS / EMPTY if setup hasn't completed. |
| `save_profile` | `save_profile(content: str)` | Persists PM profile. Server-owned write (works on Cowork where agent can't reach `~/.claude`). |
| `get_company_profile` | `get_company_profile()` | Returns shared cross-context company profile. Same signaling as `get_profile`. |
| `save_company_profile` | `save_company_profile(content: str)` | Persists company profile. Server-owned write. |

**No `consult_piper` tool**. The "consult-piper" enrichment behavior (GitHub-enriched queries) happens server-side within `ask_piper`. Bug B (payload too large) is a failure mode *inside* `ask_piper`'s enrichment path, not a separate tool.

**No `meet_piper` tool**. The meet-piper onboarding flow uses `get_profile` (check if setup needed), a conversation, and `save_profile`/`save_company_profile` (write results). The flow is a skill pattern built on top of those 3 tools.

---

## Key implication: Layer 1 is partially implemented

The `get_profile` description says explicitly:

> "Call this at the start of meet-piper (to check if setup is needed) and from any skill that wants the user's calibration."

**"From any skill that wants the user's calibration"** — the tool description already tells Claude to call `get_profile` when a skill needs profile context. This is exactly Layer 1 of the defense-in-depth model (tool descriptions embedding skill-routing guidance). It's narrow and implicit, but it's real.

The gap: the description tells Claude *when* to call `get_profile`, but doesn't tell Claude *which skills exist* or *how to invoke their procedures*. The manifest (discovery) and invocation gaps remain open.

---

## How this changes the ADR-072 topology question

The ADR-072 brief asked: keep 3 tools + server routing? One tool per skill? A meta-tool `run_skill(name)`?

The corrected question is: extend the existing 5-tool surface, or route within `ask_piper`?

The existing topology already demonstrates a deliberate separation of concerns:
- `ask_piper` = conversation/intent
- `get_profile`/`save_profile` = user profile I/O
- `get_company_profile`/`save_company_profile` = company profile I/O

This pattern has two design options for skills:
- **Option A (extend topology)**: add per-skill tools (`run_sprint_plan`, `run_draft_issue`, etc.) or a meta-tool (`run_skill(name: str)`). Skills become first-class MCP tools.
- **Option B (route within ask_piper)**: `ask_piper` detects skill-shaped queries and injects SKILL.md content at the server layer. Skills are invisible to the MCP tool surface.

Option A is more discoverable (Claude sees the skill as a tool option) but potentially creates a crowded namespace. Option B is simpler but relies on server-layer detection.

Option A also enables a hybrid: `ask_piper` for conversational PM queries, `run_skill(name)` for explicit skill invocations. Most PMs won't say "run the sprint_plan skill" — they'll say "help me plan my sprint" — so `ask_piper` plus server routing (Option B) is likely the better default, with `run_skill` as an advanced escape hatch (Option A+B hybrid).

---

## No change to the 5 ADR decisions

The 5 decisions I listed in the original brief still stand. The corrected context is input to decision #3 (plugin tool topology). Everything else is unchanged.

---

## Recorded in decisions.log

Full topology correction recorded at `docs/internal/architecture/decisions/decisions.log` (entry: 2026-06-16 ~14:00 PT) for the cross-session record.

— PA
