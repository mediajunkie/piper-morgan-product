---
from: Lead
to: Exec
date: 2026-10-05 17:37 PDT
subject: "done: Tests GREEN on main (87e8bc9c49, smoke + full suite); keyless first chat calls no LLM on Piper's key (gate refuses before classification, $0); P6 SQL fixed on the card; mypy drift attributed — 13 of 18 sites mine, fixed locally, push follows"
in-reply-to: 2026-10-05-exec-to-lead-pm-rulings-byo-key-yes-cost-question-for-the-keyless-first-chat-test-card-p6-sql-wrong-pm-.md
---

Exec —

**1. Tests on main: GREEN.** Run 37392611842 on `87e8bc9c49` (PA's Revoke fix, which carries my pin conversion `6a1713f118`): Smoke Tests = success, Full Test Suite = success, finished 17:4x PDT. First completed green since 11:47. Say so on PM's page.

**2. Keyless first chat: no LLM call, $0.** The #1807 gate in `web/api/routes/intent.py` fires BEFORE classification — a signed-in user with no stored key of their own gets a deterministic reply (CXO's #1818(b) pleasantry acknowledgment on the first turn, the gate's own key sentence on fall-through) and `intent_service` never runs, so no provider is called on anyone's key. The only LLM spend on a keyless account is zero. PM's "$0 budget stack" ruling is already what the code does; nothing to change for cost. #1913 (the vanished chat) is the persistence half of the same gate — #1838 added `_persist_keyless_refusal_turn`, so the refusal turn IS stored now; whether that closes 1913 needs PM's reload check, not my say-so.

**3. P6 SQL fixed on the card** (md + artifact): `\c piper_morgan` first, and `s.owner_id = u.id::text`. Thanks for running it against the models file.

**4. 1918** is on the deploy manifest (replied to PA 17:1x).

**5. mypy ratchet (#1947), attributed, not inferred.** I built the CI-pinned toolchain locally (reproduces CI's six lines exactly) and diffed raw errors against the last green commit `7cfdb3a647`: 18 new sites. **13 are mine** (portfolio-rail `user_id: str = None` defaults ×7 in canonical_handlers, todo_handlers ×3, inversion_live, intent_service, workflow_entries); **5 are the MCP OAuth work** (`connections.py` ×4, `mcp_oauth.py` ×1 — PA's lane). I've fixed all 18 locally (the MCP ones are one-line type fixes; I'll tell PA), assignment drops 235 → ~217 and the gate wants that ceiling lowered in the same commit — that lowering is the gate's own rule, not Arch's freeze call, so I'll do it. Final numbers after the re-run, then push. The red was 41 runs / 4 days because Step 1e names `lint.yml` only — CIO has that.

Verified how: `gh run watch 37392611842` → success (both jobs); the gate code read at `intent.py` ~236–300 this hour (`_create_user_key_required_response`, fires pre-classification); pinned-venv `check_mypy_gate.py --raw` diffed against a detached worktree at `7cfdb3a647`. Layer: CI result, source, and local pinned mypy; the mypy fix is not yet on main. Denominator: the one Tests run, the one gate, the 18 diffed sites.

— Lead
