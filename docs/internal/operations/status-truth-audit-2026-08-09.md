# Status-truth audit — the #1513 disease as a class (PM-directed, 2026-08-09)

**Method (m-43)**: static source analysis at a8d84c298; no live probes. **Denominators**: 20
status-reporting surfaces enumerated, 20/20 traced to terminal sources (chat 6, floor 3, web
routes 6, Slack 4, standup 1).

## Root cause — ONE mechanism behind 6 of 10 findings

`PluginRegistry.get_status_all()` → `plugin.is_configured()`, and **all four real plugins
hardcode `return False`** (github_plugin.py:63-72, slack_plugin.py:66-75,
calendar_plugin.py:66-75, notion_plugin.py:65-74 — same comment: "Without user context, we
can't determine configuration"). #784/#781 converted a crash into a permanent structural lie:
integration truth is user-scoped, the plugin interface has no user, so the registry is a status
source that CANNOT be right. The demo plugin reads DEMO_ENABLED env and loads at startup — so
registry-fed surfaces report real integrations never-connected and enumerate Demo beside them.
**The only integration that can ever appear connected is the fake one.**

## Findings (ranked by trust damage; full per-finding detail in session record 2026-08-09)

- **F1** `_format_integration_setup_guidance` (canonical_handlers.py:2169-2253, read at :2179) —
  registry-fed → all-four "Not connected" + Demo leak (#1534, PM-observed). Fix: thread user_id
  (in scope at :3825), read canonical service.
- **F2** The FLOOR is BLIND: `_gather_identity_context` (context_assembler.py:385-403) computes
  every integration "inactive" from the registry and the renderer omits the line entirely;
  `_gather_status_priority_context`'s github_connected (:813-824) is always-False AND never
  rendered (dead in _format_domain_context — comment-only at conversational_floor.py:782); all
  other categories receive NOTHING. PM's "no visibility" answer fully explained. Fix: per-user
  status block from the canonical service, rendered in BOTH directions ("GitHub connected;
  Notion isn't") — natural carrier for #1517's capability-manifest line.
- **F3** `_get_project_metadata` github gate constant-false (canonical_handlers.py:1451) — every
  project-status answer degrades + nudges CONNECTED users to connect (#1231 copy). Sibling
  `_get_priority_metadata` was fixed for this in #847; this one was missed.
- **F4** Chat/standup GitHub checks are OAuth-binding-BLIND: GitHubConfigService.is_configured
  is PAT-only; web /health checks binding-first (#1329). OAuth-bound-no-PAT user: web says
  healthy, chat degrades, standup/Radar work items silently []. (feed_factory.py:87;
  canonical_handlers.py:1536-1547.)
- **F5** Four public constant-false endpoints: `GET /api/v1/integrations/{name}/status` from
  each plugin's get_router() — `configured: false` forever, for everyone. No template consumes
  them; still live lying API surface. Fix: delete (preferred).
- **F6** Slack `/piper help` "I'm Connected To" (webhook_router.py:1370+, canonical_handlers.py
  :94-116) — filters registry to configured → empty or DEMO-ONLY.
- **F7** Slack /standup Blockers: "None" from `_get_blockers()` hardcoded `[]`
  (webhook_router.py:1685-1699) — m-44 false clear beside exemplary Yesterday/Today honesty.
  Fix: wire #983 blocked-items source or honest "not tracked from Slack yet".
- **F8** Agenda calendar offer conflates error with not-connected (`_get_calendar_context`
  returns None for both; :1311/:1351) + hardcoded calendar_connected=False at :1405. Fix:
  three-valued state.
- **F9** Demo-in-enumeration: registry conflates "loadable plugin" with "user-facing
  integration". Fix: user_facing flag in PluginMetadata + canonical-set filtering.
- **F10** StandupAssembler skips failing sources silently (assembler.py:86-92) — resilient but
  no "N of M sources" denominator; a GitHub outage reads as "no work items". Fix: skipped-source
  names on the summary + one degradation line.

**Verified TRUTHFUL (8 surfaces — the pattern to converge on)**: /api/v1/integrations/health
(#1513/#1337/#839/#1329 composition), /test/*, github/oauth-status, slack inbound/status (#1201
3-state incl. live socket), slack+calendar app-credentials/status, calendar settings routes,
setup status routes (fail-honest).

## The fix: ONE canonical status source

Extract `/health`'s already-correct internals into
`services/integrations/integration_status_service.py`:
`get_status(user_id, integration_id)` / `get_all(user_id)` →
`{configured, via: oauth_binding|keychain|user_secret_store|env, healthy, last_check}`.
Composition = `_github_oauth_bound` (binding-first) + `_get_integration_config_status`
(user-scoped store checks) + IntegrationHealthMonitor cache. Demo excluded structurally.
**Retire the lying source**: real plugins stop emitting `configured` (or emit None + note), and
a ratchet test asserts no non-test caller reads `get_status_all()[...]["configured"]`.

Migration table per surface + sequencing (F1+F2 = single-call-site swaps once the service
exists; F3/F4 change degrade copy → own retest pass; F5 deletable today): session record
2026-08-09. Relates: #1534, #1513, #1517, #1329, #847, #784 (root), #1231, m-44.
