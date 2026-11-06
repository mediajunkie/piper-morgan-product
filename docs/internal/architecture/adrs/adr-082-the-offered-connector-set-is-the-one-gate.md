---
type: adr
number: 82
title: "The offered-connector set is the one gate: what a host offers decides what a user can connect, is told about, and has read"
status: "ACCEPTED"
valid_from: "2026-11-06"
last_updated: "2026-11-06"
---

# ADR-082: The offered-connector set is the one gate

**Status**: **ACCEPTED, 2026-11-06** (Arch-authored). This ADR records rulings already made and landed (decisions.log, 2026-10-30 to 2026-11-05) as one decision, so the next change to the offer set has a single place to read. It changes no code.
**Related issues**: #2236, #2237, #2245, #2238, #2284, #1481, #2262. Law it serves: ADR-080 (code decides permission), ADR-081 (whose token serves a request).

## Context

The beta (outside testers from 2026-10-31) offers two connectors, GitHub and Google Calendar. Slack and Notion exist in the code, with routes, stored credentials and readers, but they are not offered. Within one week, four separate defects showed the same gap: each surface kept its own idea of what was offered.
- **#2236:** the first capability reply listed connectors the beta doesn't offer.
- **#2237:** Integrations page connect routes accepted a Slack or Notion connection.
- **#2245:** chat suggested "connect my slack".
- **#2238:** hosted Notion read a global env key ahead of the user's own.
- **#2284:** a Slack token stored before the descope still fed chat answers.

A hand-kept list on each surface drifts, and each drift either offers something we don't support or reads a credential we said we wouldn't.

## Decision

### D1. One predicate, read at call time

`services/integrations/integration_status_service.py` holds it:
- `offered_connectors()` returns the host's offered set;
- `connector_offered(name)` is the yes/no.

The set is `BETA_OFFERED_CONNECTORS` (code-fixed, `{"github", "calendar"}` today), plus `STAGING_ONLY_OFFERED_CONNECTORS` when, and only when, `FLY_APP_NAME == "piper-morgan-staging"`.

Rules:
- The predicate is read at call time, never cached at import.
- An unknown name is not offered: the predicate fails closed.
- There is no env flag, Fly secret or user preference that widens it. A promotion runs staging's image on alpha and beta, and `FLY_APP_NAME` is set per app at runtime, so a staging-only offer can't travel (11-01 08:40).

### D2. Every surface reads that predicate, and none keeps a second list

| Surface | Reads it how |
|---|---|
| Connect, OAuth-start, OAuth-callback and credential-save routes (`web/api/routes/settings_integrations.py`, `web/api/routes/setup.py`) | `refuse_unless_offered(name)` as the route body's first statement: HTTP 409 with `NOT_OFFERED_MESSAGE`, before any redirect, validation or write (#2237, 10-30 20:50) |
| Integrations page (`templates/integrations.html`) | `window.__OFFERED_CONNECTORS__` from `web/api/routes/ui.py`. The page's `OAUTH_INTEGRATIONS` and `API_KEY_INTEGRATIONS` say only *how* a connector connects, and every use is behind `isOffered`. The page fails closed |
| Chat capability reply and floor identity context (`capability_answer.py`, `canonical_handlers.py`) | `offered_connectors()`, one key-based filter (#2245, 10-31 19:34; #2236, 10-30 19:05) |
| Chat connect pointers (`chat_pointers.py`) | `connector_offered`. A non-offered ask gets the pointer to what is offered (`NOT_OFFERED_ALTERNATIVE`) |
| Credential use-path reads (D3) | `connector_offered` |

A new surface that shows, guards or lists connectors reads the predicate. A surface that needs a connector's *kind* (OAuth or API key) may keep that as data, but never as a second offer list.

### D3. A non-offered connector's stored credential is not read for use

Stored credentials survive a descope, because accounts connected before it. The gate sits at the connector's one use-path read, not at each reader (#2284, 11-05 06:28; validated 10:41 on 865e06c3ba):
- **Slack:** `SlackConfigService.get_config(user_id)` returns the config with `bot_token` and `user_token` blank when Slack isn't offered. Readers then see "not connected" through the path they already handle (#2151). The socket-mode runner's start returns no runner on such a host.
- **Notion:** its stored-key reads check `connector_offered("notion")`.

Named exceptions, which may read a non-offered credential:
- **Disconnect** (`disconnect.py`) reads it to revoke and clear it. Disconnect routes never call `refuse_unless_offered`: a user may always clear a stale connection.
- **Status** (`integration_status_service`) checks existence only, so the card can say Piper still holds a connection.

A ratchet pins which modules may name the Slack keychain slots (`TestSlackSlotRatchet`).

### D4. Offering a connector is one code change, made with its checks

To offer a connector for real:
- move it into `BETA_OFFERED_CONNECTORS`;
- remove it from `STAGING_ONLY_OFFERED_CONNECTORS`;
- confirm its #1680 consequential-write sites are instrumented (#2262 did Notion's);
- confirm its use-path read takes the user's own credential under ADR-081's resolver shape (one resolver per connector, no global env key on hosted, #2238).

Which connectors are offered is product scope (PPM and xian); this ADR fixes only how an offer takes effect.

## Consequences

- **What a beta user sees and what Piper does now come from one fact.** A connector is offered everywhere or nowhere on a given host.
- **Staging can carry a test-only offer** (Notion's save-then-chat check) without any path to alpha or beta.
- **Residual: data written before a descope stays stored** until the user disconnects. It is unread for use (D3) and shown on the card (status exception). Purging it belongs to account deletion (#2158), not to this gate.
- **The rule's own risk** is a new reader that goes around the use-path read. The ratchet catches that for Slack's slots. Notion's reads are pinned by test (`TestNotionUserKeyGate`), not by a ratchet. A Notion ratchet is the next tightening if a second Notion reader appears.

## Evidence

- **Tests:**
  - `tests/unit/services/integrations/test_offer_gate_1481_2238.py`;
  - `tests/unit/services/integrations/test_offered_gate_credential_reads_2284.py`;
  - `tests/unit/services/integrations/test_notion_hosted_user_key_2238.py`.
- **Callers:** `git grep` for `connector_offered|offered_connectors|refuse_unless_offered` over `services/` and `web/` (2026-11-06) gives 8 `refuse_unless_offered` route sites and 10 other predicate calls, across 9 modules besides the definition.
- **decisions.log, Arch lines:** 10-30 19:05 and 20:50; 10-31 19:34; 11-01 08:38, 08:40 and 09:12; 11-05 06:28 and 10:41.
