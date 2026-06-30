# #1110 Design Plan — thread user_id through SlackClient → get_config

## Core decision: LAZY per-operation client construction in the router

`SlackIntegrationRouter` is a startup SINGLETON (slack_plugin.py #784: "no user context at
startup"). user_id is per-operation everywhere. So:
- Router `__init__` does NOT take user_id (unchanged signature).
- Router stops EAGERLY building SlackClient in `__init__`. Instead a private
  `_get_client(user_id)` lazily builds (and caches per-user) the SlackClient for the operation,
  preserving the spatial-vs-legacy selection logic.
- Every router operation method gains a `user_id: str` param, threaded to `_get_client`.

## SlackClient changes (core of the issue)
- `__init__(self, config_service, user_id)` — user_id REQUIRED. Raise ValueError if falsy
  (guardrail: a client that can't call get_config is useless; never accept None).
- store `self.user_id`.
- `_ensure_session`, `_check_rate_limit`, `_make_request` → `get_config(self.user_id)`.

## Live-path scoping note
`socket_mode_runner` (live connector) uses its own AsyncWebClient, NOT SlackClient — out of
scope. The bug lives in the webhook/router/legacy seam.

## Caller fixes + user_id source
| Caller | Source |
|---|---|
| settings_integrations.get_slack_channels:499 `SlackClient()` | `current_user.sub` + add SlackConfigService() |
| settings_integrations.get_slack_settings:2076 `SlackIntegrationRouter()` | system status check — uses test_auth; connector user via SLACK_CONNECTOR_USER_ID; flag if absent |
| response_handler.py:160 `SlackClient(config_service)` default | uses SlackConfigService(); needs user_id — see handler send path |
| response_handler send paths (`_send_slack_response`, `_send_consolidated_response`) | `slack_context["user_id"]` → router.send_message(..., user_id=) |
| simple_response_handler send path | `slack_context["user_id"]` |
| reminder_job._send_reminder:254 | per-reminder `user_id` → router.send_message(..., user_id=user_id) |
| context_assembler._fetch_slack_activity_items:1666 | `user_id` method param → router.list_im_channels(user_id=)/get_conversation_history(user_id=) |
| response_flow_integration._send_response_to_slack:188 | `response_target.user_id` |
| webhook_router (passes router as slack_client to handler) | `_get_connector_user_id()` = SLACK_CONNECTOR_USER_ID |
| test_mrkdwn_1227.py:109 | dummy "u1" |

## TDD test plan (tests/unit/services/integrations/slack/test_slack_client_user_id_1110.py)
1. `SlackClient(config_service=mock, user_id="u1")`; call `_ensure_session` → assert
   `get_config` called with "u1".
2. same; call `_check_rate_limit` → assert get_config("u1").
3. same; call `_make_request` (patch session) → assert get_config("u1").
4. `SlackClient(config_service=mock)` with no user_id → raises ValueError/TypeError.
5. `SlackClient(config_service=mock, user_id="")` → raises ValueError.
6. Router: `router.send_message(channel, text, user_id="u1")` builds client whose
   config_service.get_config is called with "u1" (lazy construction).
