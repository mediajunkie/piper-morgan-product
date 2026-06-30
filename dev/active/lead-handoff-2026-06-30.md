# Lead Dev — "if-needed" handoff (2026-06-30, ~08:35 PT)

**Purpose**: resume cleanly if this session hits the usage wall mid-stream (PM will log Lead Dev in on a backup account; expect a slight logistical discontinuity, not a context loss). **Nothing is half-done as of this writing** — every unit below is committed + pushed to `origin/main`. Read this + today's session log (`dev/2026/06/30/2026-06-30-0651-lead-code-log.md`) + `dev/active/lead-carry-forward.md`, then continue.

## State: all shipped + on origin/main, staging live
- **#1331** floor anti-confabulation (systemic prompt hardening) — **PM-verified live** (fresh chat: "add a milestone" → honest decline, no fake ✓).
- **get-default-repo** query handler — **live + PM-verified** ("what's my default repo?" → real answer).
- **#1330** disconnect now clears OAuth binding + #358 grant (not just PAT) — **CLOSED** with evidence (commit `4cb71d528`).
- **#1332** empty-message — instrumented (`intent_empty_message_payload_1332` WARNING live); awaiting next recurrence to capture the cause. Not yet root-caused.
- **Staging**: app `:8001` (health 200), `github-mcp-server` container `:8082`. Restart (from this worktree, env-stripped):
  ```
  env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
    POSTGRES_PORT=5433 GITHUB_MCP_SERVER_URL=http://localhost:8082/mcp \
    nohup /Users/xian/Development/piper-morgan/piper-morgan-product/venv/bin/python main.py > /tmp/piper-staging.log 2>&1 &
  ```
  (kill `:8001` LISTEN first: `lsof -nP -iTCP:8001 -sTCP:LISTEN -t | xargs kill`)

## Issues filed today (the "make it structural" thread — PM pushed twice on point-fix-vs-general)
- **#1333** — fabrication is a category problem: generalize the unwired-action honest-decline from a LIST (`unwired_writes.py`) to a CATEGORY rule (any action-classified intent w/ no handler → deterministic decline). Five-whys in the issue. **Clean next build** (generalizes existing code). ADR-worthy (Arch/HOST).
- **#1334** — connector-agnostic disconnect helper (recurrence-proof #1330) + **duplicate `/slack/disconnect` route** bug (lines 440 & 2146; live one may not revoke Slack-side).
- **#1335** — RECONNECT GATE: connector-refactor coverage matrix (8 considerations × connectors). **AUDITED this session** (results in #1335 comment): github ✅; calendar/slack/notion are keychain-model so binding-cells are N/A-until-migrated; binding model is github-only. **Gate done-when: #1337 + #1334 fixed + an Arch decision on whether to migrate the keychain connectors onto the binding model (or accept the two-model split).**
- **#1337** — (from the gate audit) Notion health was env-var-only → UI-configured Notion read "not configured." **FIXED + closed this session** (commit `818880596`; +2 tests; staging restarted). Note: notion uses `UserAPIKeyService` (#358 store), not the keychain slack/calendar use.
- **#1336** — [placeholder] expand/refactor canonical-query regression for connector states (bound/unbound/unreachable) + trust-property assertions. Triage later.

## What to do on resume (priority order, all unblocked unless noted)

> ⭐ **ACTIVE WORK (PM directive 2026-06-30, ~99% usage): execute the SLACK plan** → `dev/2026/06/30/slack-reconnect-plan-2026-06-30.md`. PM moved Slack up from "last" (team on slow cycles + the rest of the autonomous queue is drained). **First step: #1110** (thread `user_id` into `SlackClient.get_config` — `slack_client.py:57/77/89/116`; check #1085's masking; TDD). Then #1334 (slack-dup disconnect) → #1109 (Redis OAuth state) → #1201 (inbound onboarding, CXO-gated). Slack = keychain model (ADR-058), not the binding model.

1. **Field any PM testing findings first** (PM is testing async; their findings outrank backlog).
2. **#1333** deterministic fabrication category-rule — the highest-value structural build; clean. (Loop HOST/Arch on the trust-contract; ratification already in flight.)
3. **#1334** — connector-agnostic disconnect + fix the slack-dup route (slack-dup pairs with Slack work, which is LAST).
4. **#1335** — run the gate audit (fill the matrix; file follow-ups for gaps).
5. **RECONNECT backlog**: **inc.4** sim-transport removal — PACED for the Wed Jul-1 ~9pm usage-reset (big ~10-file dead-subsystem teardown; needs its own budget; plan on #1322 comment 4827173746 + carry-forward). **Slack** #1109/#1110/#1201 = LAST. **#1230** reconcile = PPM's lane. **#1327** later layers (explain-rules meta / M4 trust-gated infer-ask) = Arch/OQ-2.

## Guardrails (unchanged, critical)
- Push non-mail via `git push origin HEAD:main` from THIS worktree; mail via `scripts/mail-send.sh`. **Never** destructive git in PM's main checkout (`/Users/.../piper-morgan-product/` — PM has uncommitted drafts).
- Strip `ANTHROPIC_*` env vars when launching `main.py` / any Anthropic-SDK script.
- Delegated agents: forbid `git push` in their prompts + verify their branch/push claims (one stray-pushed to origin/claude today — caught + reconciled).
- RUN LEAN through Wed Jul-1 ~9pm.

## PM context
PM shifted to OpenLaws ~08:32 PT. Testing Piper async. The day's methodological theme (PM-driven): turn point-fixes into structural guarantees — that's why #1333/#1334/#1335 exist.
