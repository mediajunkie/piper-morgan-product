# #1812 steps 5–6 — pre-registered execution plan (Phase A, 2026-09-20)

**Author**: Lead. **Status**: PLAN COMMITTED BEFORE CODE — per the pre-register discipline
(#1810/#1814's lesson: paired halves land together or the gap is named at ship time; this
seam's own history is why this doc exists before the diff does). Phase B executes against
this checklist, next wake or fresh context.

**Unblocked by**: PM's normal-account ruling (decisions.log 09-19 17:1x). **Enumeration
source**: Arch's six-consumer memo (09-19, in read/) — verified against a fresh census
this fire; matches, plus the test surface Arch flagged unverified, now counted (below).

## The one open decision, posed to PM this fire

**Who sponsors shared/CLI-ingest KG embeddings after the seam dies?** The straight-line
application of PM's two standing rulings (#1812 "every call is the user's call" +
"my account = normal account") is: **the ACTING USER's stored key** — a CLI ingest run by
PM embeds on PM's stored OpenAI key, resolved like any request. No new concepts. Awaiting
PM's confirm; Phase B's ingestion change assumes it unless PM says otherwise.

## Phase B checklist — production code (order matters)

1. **`services/llm/request_key.py`** — retire gate 1 + the explicit-operator binding:
   - Delete `OPERATOR_SERVER_KEY_ENV` (:125) + `_operator_env_on()` (:152) + gate-1
     re-checks (:294, :370) + the explicit `request_api_key(None)`-means-operator path
     (:319-326). **`None`/unbound becomes unconditionally a refusal** — Arch's preferred
     disposition ("a gate that can never open is dead code that reads as policy").
   - `request_api_key(None)` itself becomes either an error at bind time or a no-op
     unbind — DECIDE AT DIFF TIME by reading its callers (Slack binds only when a key
     exists; conftest changes below); prefer: `None` binding raises immediately (loud).
2. **`web/utils/llm_key.py`** — delete `is_designated_operator` (:43) entirely; the two
   ladder injections (:119, :191) lose their third rung (pass nothing / remove the
   param from `resolve_request_api_key`'s signature if no other injector remains).
   Docstrings: the "None only for the designated operator" contracts all rewrite —
   `expand_llm_key_binding`'s None-means-operator contract (#1822's Slack comment)
   becomes None-means-nothing-bound.
3. **`web/api/routes/intent.py`** (:51 import, :569 injection) — same removal.
4. **`services/knowledge_graph/ingestion.py`** — delete the operator fallback branch in
   `RequestKeyedOpenAIEmbeddingFunction.__call__` (keychain/env read): unbound → refuse,
   full stop. **Find the CLI ingest entry point and make it resolve+bind the invoking
   user's stored OpenAI key** (the PM-confirm above); if no such CLI path is live, note
   that and delete its authorization comment.
5. **Step 6 — `services/llm/clients.py` import-time singleton** (:675/:734 region): the
   module-level `LLMClient()` singleton that made a keyless-owner key seem necessary.
   Verify current line numbers at diff time (they've drifted all month); convert to
   lazy/per-use construction; check `SERVING_MODEL_RECORD` and any import-time
   dependents survive.

## Phase B checklist — tests (~48 refs, 6 files, censused this fire)

- `test_operator_server_key_1807.py` (15 tests, wholly seam): RETIRE the operator-grant
  tests; KEEP-AND-INVERT the refusal tests (unbound refuses stays true, now
  unconditionally — they get simpler). File likely renames to the refusal contract.
- `test_provider_request_key_1819.py` (13 refs) + `test_unbound_key_refusal_1809.py`
  (10) + `test_clients_gemini.py` (3) + `test_request_key_1162.py` (1): convert
  operator-binding fixtures to explicit key-mapping bindings.
- `test_embedding_request_key_1819.py` (4 refs): operator branch → refusal assertions.
- **`tests/conftest.py` `_operator_spend_binding_for_live_llm_1819`**: the live-LLM tier
  currently authorizes via the seam. Replace with explicit mapping binding:
  `request_api_key({"anthropic": env_key, "openai": env_key})` from the env keys that
  un-skipped the tests — same spend, no operator concept.
- **Spend-free ratchet note**: `SPEND_FREE` membership should be UNCHANGED (the seam is
  authorization, not routing) — run it as a canary; any membership change is a defect in
  this lane, not a promotion.

## Verification (pre-registered, the full bar)

Guard rails (`-k "1807 or 1320 or 1814 or 1815 or 1816 or 1809 or 1819 or 1822"`) green
after conversion · full llm+config+intent_service+integrations sweep · ratchets + mypy
gate at ceiling · smoke · the spend-free ratchet 14/14 with membership identical · grep
census returns ZERO hits for `OPERATOR_SERVER_KEY|is_designated_operator` outside
docs/history · deploy is a SEPARATE decision (this changes spend authorization; it rides
the next cut, not a same-day push, unless PM says otherwise).

## What this dissolves when it lands (recorded so nobody re-derives)

- My #1823 trace §2 caveat (selection-wider-than-binding on the transitional seam) —
  update the trace record in the same push (Arch's 09-19 flag).
- The `None`-means-operator honest-empty hazard (Arch's "load-bearing one").
- The last code artifact of the server-key concept. #1812 itself can then close.
