# 2026-09-25 1850 — prog (Coding Agent), model Sonnet 5

**Role**: prog (Coding Agent), dispatched by Lead Developer.
**Task**: #1772 — measure CXO's exact landed N-agnostic scope-directive string
(`422d32f1db`, deployed Fly v139) at the N=1 case. PM-approved ~20-completion hard cap
(captured in `decisions.log` 2026-09-25 by Exec).
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch
`claude/lead-cycle`). No commits/staging/index touches per dispatch constraints; no
edits under `services/`, `tests/`, `web/`.

## What I did

1. Read in full: `gh issue view 1772 --comments` (all 7 comments — the 09-15 measurement,
   the 09-24 candidate measurement, Arch's mechanism ruling, and the landing comment),
   `dev/2026/09/24/1772-candidate-measurement-2026-09-24.md` (the exact harness shape
   and post-#1812 key-bind fix), and `dev/2026/09/15/1772-scope-leak-measurement.md`
   (the scoring rule).
2. Read the live composition site: `services/intent_service/conversational_floor.py`
   ~1385-1425 — confirmed the N==1/N≥2 split and the registry's `directive` field are
   gone, matching the landing comment's description.
3. **Confirmed the exact rendered string** by calling the real
   `ConversationalFloor._format_domain_context({"source_failed": True})` directly (not
   read-and-assume) via a scratch script — byte-identical match to CXO's landed string
   quoted in the dispatch. Zero budget spent on this step.
4. Built `probe_1772_landed.py` (scratchpad, not committed) mirroring the 09-15/09-24
   harness exactly: same `FloorContext`, same user message, same
   `domain_context={"source_failed": True}`, unique session ids per call, `served` dict
   captured per call (#1620), keys resolved via `KeychainService().get_api_key(...)`
   and bound per-call via the provider-keyed `request_api_key({"anthropic": ...})` /
   `request_api_key({"openai": ...})` mapping form (#1819) — required since #1809/#1812
   retired the operator-fallback key path. Launched with the four `ANTHROPIC_*` env vars
   stripped per CLAUDE.md's server-launch gotcha.
5. Ran 20 completions total, exactly the hard cap: 10 anthropic (forced via
   `_config_service.get_default_provider` monkeypatch) + 10 openai/gpt-4o (server
   default, untouched). All 20 succeeded on first attempt; every `served` dict
   individually confirmed against the intended provider (10× `{"provider": "anthropic",
   "model": "claude-sonnet-4-6"}`, 10× `{"provider": "openai", "model": "gpt-4o"}`).
6. Scored all 20 replies against the identical rule from 09-15/09-24 (LEAK = claims an
   unarmed source failed/unavailable/unchecked; invitational offers don't count; unscoped
   general-failure claims are a separate "soft" bucket). Re-read every score a second
   time against the stated rule before writing the table (same discipline as prior runs).
7. Wrote the deliverable:
   `dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md` — layer statement,
   full method, the byte-confirmed rendered prompt (identical across both cells and all
   20 calls), per-cell results table, per-reply scoring tables, all 20 verbatim
   transcripts, denominator statement, and a conclusion lining up all four
   measurements in this issue's history (09-15 verbatim 50%/09-24 verbatim 20%/09-24
   candidate 0%/today's landed live 10% anthropic; gpt-4o clean at 0% throughout).
8. Posted the table + conclusion as a comment on #1772 via `gh issue comment 1772
   --body-file`. **Did not close the issue** — left for the Lead's call, per dispatch.

## Results

| Cell | Provider | Leaks | Rate | Soft |
|---|---|---|---|---|
| Landed string, N=1 | anthropic | 1/10 | 10% | 0 |
| Landed string, N=1 | openai/gpt-4o | 0/10 | 0% | 1 |

**Calls spent: 20/20 (hard cap), no retries into budget, no scale-up.**

**Surprise**: the landed live string is not measured-zero on anthropic — one leak
(idx 6) surfaced, using the exact same dominant template ("For the rest — I don't have
your X, Y, Z in front of me this turn") every prior leaking reply in this issue's
history has used. This is a real, if reduced, residual — the trend across the issue's
three anthropic samples is monotonically downward (50% → 20% → 10% today, with the
09-24 harness-only candidate scoring 0/10 in between), consistent with Arch's mechanism
ruling reducing but not necessarily eliminating the tendency at this sample size. No fix
proposed; the number is handed to the Lead for the closure call.

## Files

- `dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md` (deliverable)
- Scratchpad (not committed): `probe_1772_landed.py`, `confirm_1772_landed_string.py`,
  `1772_landed_results.json` — all in
  `/private/tmp/claude-501/-Users-xian-Development-piper-morgan-worktrees-lead/f47a0b3d-f896-4768-afd4-68880fc83efd/scratchpad/`

## Discovered work

None filed — the residual 1/10 anthropic leak is exactly the number this task was
scoped to surface, not a new discovered issue; it's reported in the deliverable and the
GH comment for the Lead/Arch/CXO to act on within #1772 itself.

## Verified how

Method: ran the harness live (`env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL
-u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python
probe_1772_landed.py`), captured stdout showing all 20 `served` dicts inline, wrote raw
JSON, then read every verbatim reply and scored it against the stated rule, re-reading
each score once more before the table was finalized. Layer measured: in-process floor
compose (real `ConversationalFloor` → real `LLMClient` → real provider API call) — NOT
a delivered production HTTP turn, NOT a browser render (m-43). Denominator: 20/20
pre-approved completions spent, 10 per provider cell, both stated per-cell and never
pooled (m-44); the prompt-string match check (`_format_domain_context` direct call) is
a separate, zero-cost deterministic confirmation, not counted against the completion
budget. Did not independently re-verify #1717/#1772's earlier runs' own scoring — those
are cited from the issue's own comments, not re-scored here.

## Memory & briefing surfaces referenced this session

**Referenced**:
- `docs/internal/architecture/decisions/claude-md-history.log` — not read directly this
  session, but CLAUDE.md's server-launch env-var-stripping gotcha (referenced there)
  informed the harness launch command.
- Prior #1772 measurement docs (09-15, 09-24) — informed harness design, scoring rule,
  and doc structure directly; this is a subagent dispatch, not a role session, so no
  MEMORY.md/briefing load applied.

**Loaded but not referenced**: n/a — role dispatch prompt was self-contained per the
Lead's brief.

**Wanted but not found**: none.
