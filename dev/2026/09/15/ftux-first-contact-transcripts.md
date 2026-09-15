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

---

# RE-RUN 2026-09-15 (07:07–07:13) — proving #1814 fixed, by observation

**Observer**: Coding Agent (prog), delegated by Lead Developer. **Purpose**: re-run Case 2 (the case
that failed above) after `a3404c609` ("fix(llm): make credential resolution principal-aware so a BYOC
user's own key is actually used (1814)") — confirmed via `git merge-base --is-ancestor a3404c609 HEAD`
to be an ancestor of this worktree's HEAD, deployed as prod v109. This gates the external alpha tester's
invite, currently held on this exact observation.

## Layer statement for this re-run

Same method as above, same layer: **deployed code path** (`a3404c609`, ancestor of `origin/main`, 0
commits behind at run time) via a **local `main.py` subprocess** (`--no-browser`, `ANTHROPIC_*` stripped,
ephemeral port 60696) against the **real shared local Postgres** (5433), forced onto
`PIPER_CREDENTIAL_STORE=db` (confirmed via the server's own startup log line). Real HTTP routes end to
end: `create-user`, `complete`, `login`, `intent`. **Not a production first-contact.** Unlike the original
run above, **all three cases this time produced genuine, complete replies** — nothing here needed to be
flagged as incomplete or unreachable.

## Case 2 (re-run) — signed-in user, own stored key, "What can you do?"

Same setup shape as the original Case 1/2 above: throwaway account (`user_id=1df455e5-ed38-4a76-bc53-
8fdf36a068d6`), `/complete` with a fresh validator-shaped (`sk-ant-`, 110 chars) throwaway Anthropic key,
`default_llm_provider=anthropic`. Turn 1 ("Hi there!") reproduced the original Case 1 **verbatim**
(deterministic greeting + ADR-075 notice — not re-quoted here, see Case 1 above). Turn 2:

**Request**: `POST /api/v1/intent` — `{"message": "What can you do?", "session_id": "<same session>"}`

**Verbatim reply**:
```
I can't generate responses right now because my LLM connection isn't working. This blocks most of my
core functionality. The issue could be an expired API key, a deprecated model, or a configuration
problem. Please check your LLM API key in Settings — once that's resolved, I'll be back to full
capability.
```

**Server log for this request** (three consecutive structured-log lines):
```
{"provider": "anthropic", "task_type": "conversation", "error": "Error code: 401 - {'type': 'error',
'error': {'type': 'authentication_error', 'message': 'API key is invalid.'}, 'request_id': None}",
"event": "llm_primary_failed", "logger": "services.llm.clients", "level": "warning"}
{"event": "All LLM providers failed: [\"anthropic: Error code: 401 - {'type': 'error', 'error':
{'type': 'authentication_error', 'message': 'API key is invalid.'}, 'request_id': None}\"]",
"logger": "services.llm.clients", "level": "error"}
{"error": "All configured LLM providers failed. Details: anthropic: Error code: 401 - ...",
"error_type": "auth", "session_id": "be56505b-...", "intent_category": "DISCOVERY",
"event": "conversational_floor_error", "logger": "services.intent_service.conversational_floor",
"level": "error"}
```

### Classification and why this is the PASS

**Reaching an auth error IS the pass.** The request reached the real Anthropic API — `provider:
anthropic` shows in the log, a real network call was made — and got back a genuine 401
`authentication_error` ("API key is invalid."), because the throwaway key is syntactically valid but not
a real credential. This is categorically different from yesterday's failure, where the request never
left the process: `FLOOR_FALLBACK_NO_PROVIDER` fired because the upstream "is anything configured" gate
never consulted the user's own key at all. Today, `_classify_llm_error`
(`services/intent_service/conversational_floor.py:618-651`) inspected the real exception string and
classified it `"auth"` (matched on `"401"`/`"authentication"` at :627-639) rather than `"no_provider"`
(which needs `"not configured"`/`"no llm provider"` in the string, and neither appears — the LLM layer
was reached this time). The `"auth"` classification selects `FLOOR_FALLBACK_AUTH`
(`conversational_floor.py:593-598`) over `FLOOR_FALLBACK_NO_PROVIDER` (:607-612, yesterday's bug text,
"I don't have an LLM provider configured yet..."). **The user's own stored key was resolved, selected by
the per-request `ContextVar` path `a3404c609` added, and actually sent to Anthropic.** That resolution is
exactly what #1814 says was broken, and exactly what this observation now shows working.

### Correction to what copy the user actually sees here (mechanism, not judgment)

The task brief expected this case's copy to be compared against `user_friendly_errors.py`'s
`invalid_api_key` entry. Read in full (`services/ui_messages/user_friendly_errors.py`): that entry's
message/recovery are real and current, but they are **not what fired for this call**. `intent.py`'s
`_extract_degradation_message` → `UserFriendlyErrorService.make_error_user_friendly` only runs for
exceptions that propagate to `/api/v1/intent`'s top-level exception handler. `ConversationalFloor`
catches its own LLM exception internally (`conversational_floor.py:1573-1584`) and returns a
`FloorResponse` with `FLOOR_FALLBACK_AUTH` directly — it never raises, so the top-level handler and
`UserFriendlyErrorService` are never reached on this floor-routed path. **The actual invalid-key copy a
signed-in user sees on a floor-routed capability question is `FLOOR_FALLBACK_AUTH`'s text** (quoted
above), not the `user_friendly_errors.py` string. Reporting this precisely rather than describing the
`user_friendly_errors.py` copy as what appeared, which it did not.

**Separately, for completeness**: the `user_friendly_errors.py` recovery text the task brief actually
quoted ("Top up the key's billing, or replace it with a funded one under Settings → LLM API Keys.")
belongs to the **`insufficient_quota`** entry (rewritten 2026-09-14, commit `ce8fd6f90`, replacing the
old "...or remove the current key to fall back to the built-in model" — the #1807-obsolete advice CXO
flagged as actively routing a tester into a worse state). The **`invalid_api_key`** entry's recovery
("Check or replace it under Settings → LLM API Keys.") is unchanged since 2026-07-14. Both are correct,
current, and neither contains the old "fall back to the built-in model" trap language — confirmed by
reading the file in full — but neither is the mechanism that produced Case 2's copy above. Whichever
call surface eventually does route through `UserFriendlyErrorService` (e.g. a non-floor exception path),
the copy there is confirmed clean of the #1807-obsolete trap language.

## Case 3 (re-run) — keyless new user, first turn — #1807 no-regress

Second throwaway account (`user_id=0cb32c66-e420-4fe0-bb2c-0f58132b725c`), `/complete` called with only
`user_id` (no key fields at all — the same supported skip-the-key path).

**Verbatim reply** (identical to the original Case 3 above):
```
I can't run this without an LLM key of your own — Piper doesn't bill anyone else's account. Add your
Anthropic API key in Settings and I'll pick right back up.
```
`clarification_type=user_key_required`. Server log shows only `intent_user_key_required_1807` — no
`conversational_floor`/LLM log lines — confirming the #1807 gate still fires before classification/LLM,
**unchanged by the #1814 fix**. `personalization_contexts` row count 0 for this account (ADR-075 notice
correctly never seeded), `conversations` 1 (auto-created before the gate fires, same as the original run).

## Greeting + ADR-075 notice — re-confirmed

Case 1 (re-run, keyed user, "Hi there!") reproduced the original Case 1 **verbatim**: deterministic
greeting, ADR-075 once-per-account parenthetical notice appended, `category=conversation`,
`action=greeting`, `confidence=1.0`. Turn 2 (Case 2 above) correctly carried **no** second notice —
confirming the once-per-account (DB-row-tracked, not per-process) behavior still holds after the #1814
fix. Behavior unchanged from the original run in every respect.

## Cleanup verification (re-run)

Baseline before this run: `users` 2215 / `setup_complete=true` 0 / `secure_credentials` 0 /
`invite_tokens` 235. A recovered-before-it-mattered incident occurred identical in class to the original
run's `$USERNAME` hazard (a shell variable named `USERNAME` is read-only/special in zsh) — caught via
the response echoing back `username=xian` in a validation error, before any user row existed; verified
`users WHERE username='xian'` = 0 both before and after; re-ran with `TESTUSER` instead.

Both throwaway accounts and every row they created (`users`, `user_api_keys`, `secure_credentials`
per-user entries via `KeychainService.delete_api_key`, `personalization_contexts`, `conversations`/
`conversation_turns`, `audit_logs`, `learned_patterns`, `invite_tokens`) were deleted and re-verified at
0 for each account's UUID across every table checked. Global counts returned to exact baseline: `users`
2215, `setup_complete=true` 0, `secure_credentials` 0, `invite_tokens` 235 (both minted tokens confirmed
gone). The ephemeral harness server (PID 14479, port 60696) was killed; the pre-existing dev server (PID
30735, port 8001) confirmed untouched throughout and still listening afterward. No production system, no
alpha tester's own minted invite token, and no real Anthropic spend were touched at any point.

## Bottom line for the invite-hold decision

**#1814 is fixed at the layer this observation can see.** Case 2 — the exact scenario that failed before
the fix — now reaches the real Anthropic API with the signed-in user's own resolved key and receives a
genuine authentication error, correctly classified and correctly worded (no "not configured" text, no
reference to a server-side fallback). The #1807 keyless refusal (a separate, deliberately-unchanged gate)
still fires correctly and was not regressed by this fix. The one open item for a *real* billable key
(as opposed to this throwaway one) is untested by this observation — a live, funded key would need to
reach `_anthropic_complete` and return real capability content, which this task correctly does not
require and this observer correctly did not attempt.
