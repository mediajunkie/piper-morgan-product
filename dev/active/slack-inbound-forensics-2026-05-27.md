# Slack Inbound Forensics — 2026-05-27

**Investigator**: code-opus (forensic-research agent)
**Working dir**: `/Users/xian/Development/piper-morgan/piper-morgan-product` (read-only)
**Trigger**: PM smoke-test 2026-05-27 ~12:00 PM PDT — no response to DM, no response to `@mention` in `#piper-morgan`. Server up (port 8001, `/health` → 200), but `ngrok` not running AND not on PATH.

## TL;DR

**Q1 (Last verified working): NEVER.** I cannot find a single dated session log or commit message claiming end-to-end "I sent a message in Slack and Piper responded." The closest evidence is the **PM-074 commit (`6e6b02dde`, 2025-07-28)** asserting "live testing validated with 'Kind Systems' corporate workspace," but the *next-day* commit (`5710f6977`, 2025-07-29) **diagnosed the opposite**: webhook HTTP-200 reached, "background processing failing silently after webhook success." That gap was never closed in subsequent commits. **Confidence: high.**

**Q2 (What disentangled it): The wiring was REMOVED.** At PM-074 (Jul 28 2025), `main.py` contained `app.include_router(slack_router.get_router())` mounting `SlackWebhookRouter` directly. By the **CORE-GREAT-2D commit `aad66d9d1` (2025-10-01)**, that entire 1184-line main.py was reduced to a stub (`main.py` shrank to 421 lines per the diff stat) and Slack wiring vanished. The plugin system (`e12d62303` GREAT-3B, 2025-10-03) replaced it — but `services/integrations/slack/slack_plugin.py` only exposes `/api/v1/integrations/slack/status`, **NOT** the `/webhooks/events` routes from `SlackWebhookRouter`. The webhook router class still exists; it is simply never mounted. **Confidence: high** (verified by reading current `web/app.py`, `web/startup.py`, `main.py`, `slack_plugin.py`).

**Q3 (Architecture drift): Yes — significant Pattern-072 + Pattern-073 instance.** `services/integrations/slack/ngrok_service.py` (262 lines) is referenced ONLY by tests — zero production consumers (no startup script, no main.py, no web/ code calls `NgrokService.start_tunnel`). Socket Mode is documented in README as an option but `enable_socket_mode: false` default + no implementation. README still advertises "Phase 3 Complete ✅" and tells users to set `SLACK_BOT_TOKEN` — the OAuth wiring works (#1085 work proves outbound API calls succeed), but the inbound webhook path has been silently disconnected from app startup for ~8 months. **Confidence: high.**

---

## Q1: Last verified Slack-inbound working

### Strongest claim, never substantiated

**Commit `6e6b02dde`** (2025-07-28, "Complete PM-074 Slack Spatial Intelligence System implementation"):
> "Live testing validated with 'Kind Systems' corporate workspace / Real-time webhook event processing confirmed operational / Spatial event mapping and attention attractor system functional"

No accompanying session log captures a verbatim "Piper posted X in response to my @mention" sequence — the claim is in the commit message only.

### Next-day reality check (the same person, 24 hours later)

**Commit `5710f6977`** (2025-07-29, "Complete Slack webhook infrastructure with background processing diagnosis"):
> "✅ INFRASTRUCTURE COMPLETE: webhook delivery working via ngrok metrics... ✅ ROOT CAUSE IDENTIFIED: Webhook infrastructure fully functional (instant HTTP 200 responses) / Background processing failing silently after webhook success / Issue located between async task creation and Slack API posting / Ready for Chief Architect deep dive on background processing chain"

Translation: Slack → ngrok → FastAPI returned HTTP 200, **but Piper's response never reached Slack**. The "Chief Architect deep dive" was never logged as completed.

### Subsequent Slack work (Q4 2025 → May 2026) was OUTBOUND or scaffolding only

- **#161 Slack reminder integration** (Oct 2025): outbound message posting, not inbound webhook handling
- **PM-074 spatial / #194 service unification** (Sep–Oct 2025): refactoring, not smoke tests
- **#1081 NOTION-SLACK-XREF** (May 2026): the `[ ]` AC explicitly reads *"Smoke: Slack message with Notion URL renders Notion context — deferred to manual PM UAT — agent cannot drive live Slack→Notion smoke"* — REOPENED on May 24 under PM's deferred-AC self-justification correction (#1081 is currently OPEN). This is direct evidence that *no live smoke has ever been documented* for inbound Slack URL unfurl.
- **#1085 CONTEXT-ACTIVITY-SLACK** (May 18–23 2026): "mentions-of-user" was an **outbound** read of Slack via API (the recent-activity aggregator pulling DMs), NOT inbound webhook handling. The May 19–22 OAuth marathon arc was **about `search:read` scope for the search.messages outbound API call** — `dev/2026/05/19/...`, `dev/2026/05/20/...`, `dev/2026/05/22/...` logs do not contain `@piper` or "inbound smoke" anywhere.
- **#1107 DinP re-registration** (May 21 2026): OPEN; planned migration of the Slack app from Kind to Design in Product workspace; explicitly deferred.

### Search confirmation

```bash
grep -i -rn "piper.*responded\|piper.*posted" dev/2025 dev/2026 --include="*.md" | grep -i "slack"
# Only hit: dev/2026/01/21/620-slack-integration-grammar-audit.md:217:
#   '5. **Experience Test**: "Piper responded in the Slack channel" not "Response sent to channel"'
# (Grammar/UX audit copy, not a smoke-test record.)
```

**Conclusion**: I find no dated, verifiable record of "I @-mentioned Piper in Slack and Piper replied" since the codebase has been on GitHub. The July 29 2025 diagnosis is the high-water mark and it explicitly says the loop wasn't closing.

---

## Q2: What disentangled it (the load-bearing finding)

### The smoking gun: main.py at PM-074 vs. main.py today

`git show 6e6b02dde:main.py | grep slack` (2025-07-28):

```python
28:from services.integrations.slack.webhook_router import SlackWebhookRouter
154:slack_router = SlackWebhookRouter()
155:app.include_router(slack_router.get_router())
```

`git show a5cd9fd3e:main.py` (Phase 2 recovery, Sep 2025): same wiring via `SlackDomainService.get_webhook_router()` — main.py still 1184 lines, slack still mounted.

`grep -n "slack\|webhook" main.py` (current `main.py`, 421 lines):
```
(no matches)
```

### When the wiring vanished

**Commit `aad66d9d1`** (2025-10-01, "docs: Complete CORE-GREAT-2D documentation suite and coordination") shows `main.py | 1184 +------------------` in the stat — i.e., gutted to a stub. Slack mounting went with it.

**Commit `e12d62303`** (2025-10-03, "feat(plugins): Add dynamic discovery and config-based loading (GREAT-3B)") wired in the plugin registry as the replacement. But `services/integrations/slack/slack_plugin.py::get_router()` only returns:

```python
self._api_router = APIRouter(prefix="/api/v1/integrations/slack", tags=["slack"])
@self._api_router.get("/status")  # <— THIS IS THE ONLY ROUTE
```

The `SlackWebhookRouter` class (with `/webhooks/events`, `/webhooks/interactive`, `/webhooks/commands`) is **never instantiated** by the plugin path. Verified by:

```bash
grep -rn "SlackWebhookRouter\|from services.integrations.slack.webhook_router" --include="*.py" | grep -v test | grep -v __pycache__
# Only non-test consumers:
#   services/domain/slack_domain_service.py (constructs it, but nothing mounts the result)
#   services/debugging/slack_inspector.py (imports handler for diagnostic purposes)
```

`SlackDomainService` is itself consumed only by `services/integrations/mcp/skills/standup_workflow_skill.py` (the standup MCP skill, an outbound surface), so the webhook router never reaches FastAPI startup.

### This is Pattern-073 (Documentation-Asserted-Behavior Drift)

`services/integrations/slack/README.md` still proclaims **"Phase 3 Complete ✅ (October 18, 2025)"** with `webhook_endpoints: /slack/webhooks/events` listed in the architecture. The code says otherwise.

---

## Q3: Architecture drift assessment

### Current intent (per README + config)

- ngrok-based local-dev tunneling (`ngrok_service.py`, README example commands)
- Optional Socket Mode flag (`enable_socket_mode: false` default, no implementation found)
- Webhook router exposes `/webhooks/events` for production deployment

### Current state (per actual code)

1. **Webhook router exists but is unmounted** — `services/integrations/slack/webhook_router.py` is a 1400+ line class never registered with FastAPI app
2. **ngrok service is test-only** — `NgrokService` referenced only by `tests/unit/services/integrations/slack/test_ngrok_webhook_flow.py` + `test_spatial_system_integration.py`. Zero production callers
3. **No startup script knows about ngrok** — `grep -i ngrok scripts/*.sh scripts/*.py` returns nothing in `start-piper.sh`, `start.sh`, `restart-server.sh`
4. **No ADR for Slack inbound tunneling strategy** — `docs/internal/architecture/current/adrs/` has no Slack-or-tunneling-specific ADR; closest is ADR-038 spatial intelligence (architectural pattern, not deployment)
5. **OAuth + outbound API works** — May 19–23 work proves the outbound side (search.messages, DM aggregation, OAuth token persistence) functions
6. **Open #1107** (DinP Slack app re-registration) explicitly contemplates a fresh `A0…` app registration with manifest including redirect URIs for "local + production environments" — but the local-dev tunneling mechanism is not specified

### What this means

The May 19–22 "Slack OAuth marathon" arc verified **outbound** (Piper reading Slack via API). It did not touch the **inbound** webhook path because the inbound path is not wired into `main.py` / `web/app.py` at all. PM's 2026-05-27 smoke test fails for a **structural** reason (no route is listening for the webhook), not an OAuth/config reason.

The ngrok-on-PATH assumption is moot — even if ngrok were running, Slack's HTTP POST to `localhost:8001/slack/webhooks/events` would 404.

---

## Recommended path forward

### Option A — Restore (small): wire the existing webhook router back into the app

**Effort**: ~30 min code + ~1 hr smoke validation

1. Add to `web/app.py` (alongside other `RouterInitializer.mount_router(...)` calls):
   ```python
   from services.integrations.slack.webhook_router import SlackWebhookRouter
   _slack_webhook = SlackWebhookRouter()
   app.include_router(_slack_webhook.get_router())
   ```
2. Install ngrok on PATH (`brew install ngrok` or use the alternative tunnel of choice)
3. Configure `https://<ngrok-url>/slack/webhooks/events` in `api.slack.com/apps/A097QATL1D1` Event Subscriptions
4. Smoke: DM the bot, confirm webhook reaches `_handle_events_webhook`, confirm response posts back

**Risk**: The 2025-07-29 "background processing failing silently" diagnosis was never resolved. Likely we wire the route + still find Piper doesn't respond because of the downstream async chain. Budget another 2–4 hrs for that debugging.

### Option B — Restore-then-modernize: Option A + replace ngrok with Cloudflare Tunnel or Socket Mode

**Effort**: A + ~2 hrs (Socket Mode requires `slack_sdk.socket_mode` integration; not currently in the codebase)

Socket Mode is the long-term path for local dev — no public URL needed, no tunneling daemon to babysit. The config flag exists (`enable_socket_mode`); the implementation does not.

### Option C — Rebuild post-#1107: ride the Design in Product re-registration

**Effort**: ~4–6 hrs combined

#1107 is the natural moment to revisit *all* the inbound assumptions:
- Fresh app manifest in DinP can specify Socket Mode from day one
- Fresh redirect URIs avoid the Kind workspace's stale OAuth tokens
- Clean test: brand-new app, brand-new wiring, brand-new smoke test, all captured in one session log

This is my recommended path **if PM has the bandwidth**. The current state is "scaffolding asserted but never live"; #1107 is a natural inflection point to make it actually live and document the smoke.

### Documentation cleanup (regardless of restore vs. rebuild)

1. `services/integrations/slack/README.md` — strike "Phase 3 Complete ✅" until inbound is verifiably running
2. File a Pattern-073 instance for the asserted-but-disconnected webhook router (Patterns catalog)
3. Consider whether `ngrok_service.py` should be deleted (Pattern-072 alive-scaffolding) or kept as a future tunneling helper

---

## Evidence inventory

**Commits referenced**:
- `6e6b02dde` (2025-07-28) PM-074 spatial impl — first webhook mount
- `5710f6977` (2025-07-29) PM-078 background-processing-fails diagnosis
- `a5cd9fd3e` (2025-09-?) Phase 2 recovery — moved mount to SlackDomainService
- `aad66d9d1` (2025-10-01) CORE-GREAT-2D — main.py gutted, Slack mount lost
- `e12d62303` (2025-10-03) GREAT-3B plugin system — SlackPlugin replaced wiring, but only `/status` route

**Logs referenced**:
- `dev/2025/09/26/2025-09-26-1527-prog-code-log.md` (PM-074 attribution)
- `dev/2026/05/19/2026-05-19-0655-lead-code-opus-log.md` (OAuth marathon — outbound)
- `dev/2026/05/20/2026-05-20-0604-lead-code-opus-log.md` (search.messages scope investigation)
- `dev/2026/05/23/2026-05-23-0840-lead-code-opus-log.md` (#1085 slice 3 ship — outbound)
- `dev/2026/05/24/2026-05-24-0931-lead-code-opus-log.md` (#1081 reopened for missing live smoke)

**Issues referenced**:
- #1081 NOTION-SLACK-XREF — OPEN; live smoke never run
- #1085 CONTEXT-ACTIVITY-SLACK — CLOSED; outbound only
- #1107 DinP re-registration — OPEN; planned but deferred
- #472 EPIC: Slack Integration TDD Gaps — CLOSED 2026-05-24
- #692 WIRE-SLACK — CLOSED 2026-05-24 as Pattern-073 cleanup

**Files verified**:
- `/Users/xian/Development/piper-morgan/piper-morgan-product/main.py` (no slack/webhook)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/web/app.py` (no SlackWebhookRouter mount)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/web/startup.py` (plugin registry mounts, but only `slack_plugin.get_router()`)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/services/integrations/slack/slack_plugin.py` (only `/status` route)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/services/integrations/slack/webhook_router.py` (exists, has routes, never mounted)
- `/Users/xian/Development/piper-morgan/piper-morgan-product/services/integrations/slack/ngrok_service.py` (exists, only tests consume)
