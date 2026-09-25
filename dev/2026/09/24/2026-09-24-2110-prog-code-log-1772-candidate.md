# 2026-09-24 21:10 — prog (Coding Agent) — #1772 candidate measurement

**Role**: prog (Coding Agent)
**Model**: Sonnet 5 (claude-sonnet-5)
**Dispatched by**: Lead Developer, for #1772
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) —
per dispatch instructions I do NOT commit/stage/touch the index or modify `services/`,
`tests/`, `web/`. Measurement only, scratchpad harness, deliverable doc under `dev/`.

## Task

Measure ONE candidate for #1772 (N=1 degrade reply scope-directive leak): render the N=1
case through the SAME aggregate composition shape N≥2 already uses, on anthropic (the
leaking provider per `dev/2026/09/15/1772-scope-leak-measurement.md`: N=1 anthropic 5/10,
gpt-4o 0/10; N≥2 aggregate 0/5 both). Hard budget: 20 provider completions total, not to
be exceeded. Two cells, 10 each: (1) candidate aggregate-shape prompt, anthropic, N=1;
(2) current verbatim single-directive prompt, anthropic, N=1 (same-night re-baseline).

Read #1772 (`gh issue view 1772 --comments`) and the full 09-15 measurement doc before
starting. Confirmed: no fix proposal in scope — this is measurement only, for CXO
(copy)/Arch (mechanism) to design against.

## Code read

`services/intent_service/conversational_floor.py`:
- `SOURCE_FAILED_FLAGS` registry (~line 158) — 5 registered directives, entry 0 =
  `("source_failed", "reminders", <verbatim single-failure directive>)`.
- Composition site ~line 1385-1425 (`_format_domain_context`): N==1 renders
  `_failed_sources[0].directive` verbatim; N>=2 renders the aggregate
  `"- DATA CHECKS FAILED this turn — could not check: {names}. ..."` line; both followed
  by the wrinkle-1 scope line (unchanged either way).
- `respond()` (~line 1624) builds `system_prompt` via `_get_system_prompt`, `prompt` via
  `_build_prompt` (which calls `_format_domain_context`), calls
  `llm.complete(task_type="conversation", prompt=prompt, system=system_prompt,
  user_id=ctx.user_id)`, then strips scaffolding/placeholder artifacts. `respond()` does
  NOT itself take/pass a `served` dict — `llm.complete(..., served=...)` is the
  attribution mechanism (`services/llm/clients.py` `_complete_raw`, `served["provider"]`
  / `served["model"]` set at the success point, #1620).
- Provider resolution: `LLMClient._config_service.get_default_provider(user_id)`
  (`LLMConfigService` instance created in `LLMClient.__init__`). Forcing anthropic =
  monkeypatch that instance attribute's `get_default_provider`.

Old scratchpad from the 09-15 run (`probe_1772_scope_leak.py`) is gone — scratchpad
dirs are session-ephemeral, this is a new session UUID. Reconstructed the harness from
the 09-15 doc's Method section plus direct code reading (above), not from memory of
what the old script did.

## Harness

`/private/tmp/claude-501/-Users-xian-Development-piper-morgan-worktrees-lead/f47a0b3d-f896-4768-afd4-68880fc83efd/scratchpad/probe_1772_candidate.py`
(not committed — same disposition as the 09-15 probe script).

- `ConversationalFloor(llm_client=LLMClient())`, `FloorContext(user_message="good
  morning, what's my status?", session_id=<uuid per call>, user_id=None,
  intent_category="conversation", domain_context={"source_failed": True})`.
- Provider forced: `llm._config_service.get_default_provider = lambda user_id=None:
  "anthropic"`.
- Baseline arm: unpatched `ConversationalFloor` instance — `_format_domain_context`
  renders the registry directive verbatim (current shipped behavior).
- Candidate arm: separate `ConversationalFloor` instance whose bound
  `_format_domain_context` is wrapped to call the real method, then string-replace the
  verbatim single directive (pulled from `SOURCE_FAILED_FLAGS[0].directive` — not
  hand-typed) with the aggregate-shape line built from the SAME f-string template the
  N>=2 branch uses, fed the single check_name `"reminders"` (also pulled from the
  registry, not hand-typed). Instance-scoped monkeypatch only; repo file untouched.
- Per call: `system_prompt = await floor._get_system_prompt(ctx)`,
  `prompt = floor._build_prompt(ctx)`, `served = {}`,
  `message = await llm.complete(task_type="conversation", prompt=prompt,
  system=system_prompt, user_id=None, served=served)`, then
  `strip_scaffolding_artifacts` / `strip_placeholder_slots` applied (mirrors `respond()`
  exactly for message post-processing) — `served` checked for `provider == "anthropic"`
  on every call, never inferred from the monkeypatch alone.
- Launch: `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN
  -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python probe_1772_candidate.py` (keys resolve via
  KeychainService, matching the 09-15 doc and CLAUDE.md's server-launch gotcha).

## Log

- **21:09** — Dry-run sanity check (no LLM call): confirmed `OLD_LINE` (registry's
  verbatim reminders directive) is found in the baseline `_build_prompt()` output, and
  built `NEW_LINE` (candidate aggregate-shape line, single check_name "reminders")
  programmatically from the same f-string template the N>=2 branch uses. No budget
  spent.
- **21:09** — First full-harness attempt failed with `UnboundLLMKeyError` before any
  `llm.complete()` call returned (0 budget spent). Root cause: #1807/#1809/#1812 (landed
  since the 09-15 run) retired the server's designated-operator key fallback — every LLM
  call now requires an explicit per-request `request_api_key(...)` bind. Fixed by
  fetching the operator's stored anthropic key via `KeychainService().get_api_key
  ("anthropic")` (never hand-typed/guessed) and binding it with `request_api_key(...)`
  around each call, mirroring `resolve_request_api_key`'s real-request behavior.
- **~21:10** — Re-ran the full harness. All 20 calls succeeded (10 candidate, 10
  baseline), exit 0, exactly at the 20-completion hard cap. Every `served` dict
  confirmed `{"provider": "anthropic", "model": "claude-sonnet-4-6"}` on all 20 calls —
  attribution checked per call, never inferred from the provider-forcing monkeypatch
  alone.
- **~21:15** — Extracted both rendered prompt arms (call 0 of each cell; confirmed
  byte-identical across all 10 calls per cell except `session_id`, which never enters
  the prompt text) and all 20 verbatim replies from `1772_candidate_results.json`.
- **~21:20** — Scored all 20 replies against the 09-15 scoring rule (LEAK = claims an
  unarmed source failed/unavailable; offers/invitations are not leaks; unscoped
  general-failure claims are "soft," counted separately). Re-read every score once
  against the stated rule before writing the results table (same discipline the 09-15
  lane used). Result: candidate 0/10 leaks, baseline (tonight) 2/10 leaks, 0 soft cases
  in either arm.
- **~21:25** — Wrote deliverable doc
  `dev/2026/09/24/1772-candidate-measurement-2026-09-24.md` (layer statement, method,
  both prompt arms verbatim, call count, results table with per-cell denominators, all
  20 verbatim transcripts with scores, plain conclusion stating what the n=10 numbers do
  and don't show — including that the baseline itself moved 50%→20% night-to-night on
  an unchanged prompt, so the candidate's 0/10 is directionally supportive, not
  confirmatory).
- **~21:30** — Posted results table + conclusion as a comment on #1772
  (`https://github.com/mediajunkie/piper-morgan-product/issues/1772#issuecomment-5826570817`).
  Issue left OPEN — not closed, per dispatch (fix design belongs to CXO/Arch, not this
  measurement pass).

## Discovered work

None filed. The `UnboundLLMKeyError` encountered was a known, intentional consequence
of #1807/#1809/#1812 (the operator-seam retirement), not a bug — the harness needed to
adapt to it, not the reverse. No new issue warranted.

## Verified how

**Method**: ran the harness script
(`/private/tmp/claude-501/.../scratchpad/probe_1772_candidate.py`) twice — once as a
dry-run prompt-only sanity check (no LLM calls), once for the full 20-completion
measurement — via `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u
ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python probe_1772_candidate.py`,
captured full stdout to a log file, and cross-checked the `TOTAL SPENT: 20 / 20` line,
every per-call `served` dict, and the raw `1772_candidate_results.json` against the
prose written into the deliverable doc and the GitHub comment — nothing in either was
transcribed from memory rather than read from the actual run output this session.
**Layer measured**: in-process floor compose (real `ConversationalFloor._build_prompt` /
`_get_system_prompt` → real `LLMClient.complete` → real anthropic API call, provider
resolution forced and confirmed per-call via `served`) — NOT a delivered HTTP turn, NOT
a browser render, NOT the production `/api/v1/` path.
**Denominator**: 20 completions total = 10 candidate + 10 baseline, both fully spent,
both fully scored (20/20 replies scored and re-checked against the rule, 0 excluded, 0
retried). gpt-4o and the N≥2 aggregate case were NOT re-measured tonight — out of
tonight's approved budget scope, cited only from the 09-15 doc as context, never
pooled into tonight's denominators.
