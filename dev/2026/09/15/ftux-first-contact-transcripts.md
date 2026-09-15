# FTUX first-contact transcripts — brand-new user's first chat turn

**Date**: 2026-09-15
**Observer**: Coding Agent (prog), delegated by Lead Developer
**Purpose**: close CXO's oldest unobserved claim — what a brand-new user actually sees on their first
chat turn, verbatim. Observation only; not a judgment of whether the copy is good.

## Layer statement (read this before the transcripts)

This observes the **deployed code path on `origin/main`** (this worktree was at `d93934216`, `git
fetch` confirmed 0 commits behind `origin/main` at run time) via a **local `main.py` subprocess**
(`--no-browser`, `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/
`ANTHROPIC_CUSTOM_HEADERS` stripped, ephemeral port 59901) against the **real shared local Postgres**
(port 5433, the same dev database used by unit-pin tests), forced onto `PIPER_CREDENTIAL_STORE=db`
(`EncryptedDBCredentialStore` — matches the credential-store backend layer prod resolves to, confirmed
by the server's own startup log line). Real HTTP routes end to end: `/api/v1/setup/create-user`,
`/api/v1/setup/complete`, `/api/v1/auth/login`, `/api/v1/intent`. **This is NOT a production
first-contact** — it does not exercise fly.dev, prod's actual OS-keyring auto-detection, or any
production data. It is the same *code*, run for real, on a local *server* and a local *database*, using
throwaway invite tokens minted directly via `docker exec piper-postgres psql` (there is no HTTP mint
endpoint) and throwaway accounts, all deleted afterward and verified by count.

Two of the three cases below are **fully genuine, complete replies** (the greeting is a deterministic
handler; the keyless refusal is a deterministic pre-LLM gate — neither needed a working Anthropic key).
The third (capability question, keyed case) **could not produce genuine LLM-generated content**: I have
no billing-capable Anthropic key to mint, and did not pursue macOS Keychain access to a possibly-real
local key (it hung on an interactive GUI prompt rather than returning a value; touching PM's personal
keychain for an observation task was out of scope). Per this task's own instructions, I attempted the
call anyway with the same validator-shaped throwaway key setup already used, and I'm reporting exactly
what came back — clearly flagged as a **provider-availability-gate failure**, not genuine capability
copy, not an "invalid key" auth error either (see the root-cause trace at the end; filed as
[#1814](https://github.com/mediajunkie/piper-morgan-product/issues/1814)).

---

## Case 1 — Keyed new user, turn 1: plain greeting

Setup: throwaway account created via invite token, `/complete` called with a validator-shaped
(format-valid, high-entropy, non-billable) Anthropic key and `default_llm_provider=anthropic`. Logged
in via `/api/v1/auth/login`. First-ever message on a brand-new session.

**Request**: `POST /api/v1/intent` — `{"message": "Hi there!", "session_id": "<fresh uuid>"}`

**Verbatim reply**:
```
I'm here and ready. Hello!

What's on your mind?

(Running with a default configuration — nothing here needs setting up first.)
```

**What rode along**: the ADR-075 one-time personalization notice — the parenthetical last line. Nothing
else. The `intent` block: `category=conversation`, `action=greeting`, `confidence=1.0`.

**What did NOT ride along, and why (both confirmed by reading source, not just observing absence)**:
- No FTUX empty-state interview opening ("I don't have anything of yours in front of me yet...") —
  gated behind `PIPER_FTUX_INTERVIEW`, default OFF per a PPM 2026-09-03 HOLD ruling; left unset for this
  run, matching what a real deploy of `main` carries today.
- No first-contact data demonstration block ("Here's what I'm already keeping track of in...") — this
  throwaway account has zero configured connectors (no GitHub), and that block only renders for a
  configured connector with real data. A cold account with nothing connected gets nothing here, by
  design (the code is "structurally incapable" of naming an entity it didn't read this turn).

## Case 2 — Same keyed user, turn 2: "what can you do"

Same session, same account, immediately after Case 1.

**Request**: `POST /api/v1/intent` — `{"message": "What can you do?", "session_id": "<same session>"}`

**Verbatim reply**:
```
I don't have an LLM provider configured yet, so I can't generate conversational responses. You can add an OpenAI or Anthropic API key in Settings to enable this. In the meantime, I can help with todos, GitHub issues, and other structured tasks.
```

**What rode along**: nothing — no ADR-075 notice this time (correctly: it already fired once for this
account in Case 1 and the code tracks "seen" per-account in the database, not per-process or
per-message). `intent.category=DISCOVERY`, `action=get_capabilities`, `floor_hit=true` (this category
floor-routes to an LLM-generated response, unlike Case 1's deterministic greeting).

**Honesty flag on this one**: this account DOES have a stored, format-valid Anthropic key, and
`/api/v1/intent`'s own signed-in-key gate (#1807) had already let the request through on that basis —
it was NOT refused with the "add your key" message. The "no LLM provider configured" text above is a
**different, deeper fallback** (`FLOOR_FALLBACK_NO_PROVIDER`) that fires for an unrelated reason: the
component that decides "is any provider available" for this call never looks at a user's own stored
key at all — only a legacy global keychain slot that #1810 (merged this week) correctly stopped
populating. Root-cause trace and a new tracking issue are at the bottom of this file. **This is not
what a working capability answer looks like, and is not what a genuinely invalid/expired key would
produce either** (a real auth failure classifies to a different fallback, `FLOOR_FALLBACK_AUTH`, whose
copy is about checking the key in Settings for auth reasons, not "not configured yet").

## Case 3 — Keyless new user, first turn (the invite's actual near-term scenario)

Setup: a second throwaway account, `/complete` called with **no `openai_key`, no `anthropic_key`, no
`default_llm_provider`** — the real, supported "skip the key step" path (both fields are `Optional` in
the request schema). This is the state the alpha invite creates until the tester adds their own key —
and exactly what Janne gets if he opens the chat before finishing that step.

**Request**: `POST /api/v1/intent` — `{"message": "Hi there!", "session_id": "<fresh uuid>"}`

**Verbatim reply**:
```
I can't run this without an LLM key of your own — Piper doesn't bill anyone else's account. Add your Anthropic API key in Settings and I'll pick right back up.
```

**What rode along**: nothing — no greeting, no ADR-075 notice, no capability copy. `intent.action=clarify`,
`requires_clarification=true`, `clarification_type=user_key_required`, `suggestions=["Add your
Anthropic API key in Settings"]`.

**Notable, confirmed both by reading the route code and by the server log**: this is the **#1807
honest-refusal path**, and it fires **before classification, before the LLM, before the greeting
handler ever runs** — the key-resolution check in `/api/v1/intent` happens unconditionally, ahead of
`intent_service.process_intent`. That means a keyless signed-in user gets this exact same refusal
**no matter what they type first** — a bare "hi" gets the identical "add your key" copy a substantive
question would get. The server log for this request shows only `intent_user_key_required_1807`; no
`conversational_floor` or LLM-client log lines at all, confirming no LLM call was attempted.

---

## ADR-075 once-per-account notice — summary

- Appears **exactly once per account**, appended after a successful (non-refused, non-degraded)
  reply — confirmed here on Case 1's greeting.
- Does **not** repeat on the same account's next turn (confirmed: absent from Case 2's reply).
- Does **not** appear on the keyless refusal (Case 3) — the code path that would append it
  (`intent_service.process_intent`'s post-processing) never runs when the #1807 gate refuses first.
- Tracking is DB-row-based (`personalization_contexts.has_seen_personalization_notice`), not
  per-process or per-session — genuinely once-per-account, matching its name.

## Root cause of Case 2's fallback (traced, filed as new work — not fixed here)

`services/llm/clients.py::_complete_raw` resolves the active provider via
`LLMConfigService.get_default_provider(user_id)`, which depends on `get_configured_providers(user_id)`
→ `get_api_key(provider)` — and `get_api_key` (`services/config/llm_config_service.py:213-234`) checks
**only** the legacy global/bare keychain slot plus an env-var fallback, never the per-user stored key.
Since #1810 (this week) correctly deleted the only code that used to populate that global slot, this
check now returns empty for **any** user whose only key is their own — real or fake, doesn't matter,
the check never looks at it. `get_default_provider` raises, `_complete_raw`'s fallback checks the
server-level singleton clients (also empty, no global key), and raises `RuntimeError("No LLM providers
configured...")` — **before ever reaching** `_anthropic_complete`, where the correct per-request BYOC
key threading (`anthropic_client_for_request`, wired for #1162/#1807) actually lives and would have
worked. Filed as **[#1814](https://github.com/mediajunkie/piper-morgan-product/issues/1814)** — this
will hit the real alpha tester on his very first non-greeting question, immediately after doing exactly
what the invite asks (configuring his own key first).

## Cleanup verification

Both throwaway accounts and every row they created (`users`, `user_api_keys`, `secure_credentials`
per-user entries, `personalization_contexts`, `conversations`/`conversation_turns`, `audit_logs`,
`learned_patterns`, `invite_tokens`) were deleted and re-verified at 0 for each account's UUID. Global
counts returned to baseline: `users` 2117 (unchanged), `users WHERE setup_complete=true` 0 (unchanged),
`secure_credentials` 0 (unchanged — no global/bare key ever created, consistent with the #1810 fix).
The ephemeral harness server (PID 73905, port 59901) was killed; the pre-existing dev server (PID
30735, port 8001) was confirmed untouched throughout and still listening afterward. No production
system, no the alpha tester's own minted invite token, and no real Anthropic spend were touched at any
point.
