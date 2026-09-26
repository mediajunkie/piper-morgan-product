# Session Log — 2026-09-26 — prog (Coding Agent) — #1595 unit 4 build

**Role**: Coding Agent (prog)
**Model**: Opus 5 (1M context) — `claude-opus-5[1m]`, observed at start; dispatched by Lead Developer
at Opus tier (stated deliberately; epic 0's most delicate unit)
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Issue**: #1595 unit 4 — multi-intent under the inversion consult, Arch's shape (ii)
**Constraints**: no commits/staging/index touches; no LLM calls (deterministic router stubs only);
no flag/env/Fly changes. All honored — `git status` shows 4 modified + 2 new files, index untouched.

---

## Reads (in the dispatched order)

- `docs/internal/architecture/current/intent-routing-stack.md` — full (1004 lines): the four
  surfaces, #1595 flip-1 consult seam, #1667 flip groups, #1677/#1559/#1606 write allowlist,
  #1763 sibling partition, #1896 stand-down.
- `dev/2026/09/25/2026-09-25-1900-prog-code-log-1595-unit4.md` — the design probe (why option (a)
  is unbuildable; the ratchet-clean span recipe, reused here).
- Arch: `correct-…-unit4-ruled-shape-ii-2026-09-25.md` and
  `mailboxes/lead/inbox/rule-arch-…-unit4-sequencing-approved-…-2026-09-26.md` (the inbox copy —
  the `read/` copy in the opening git-status snapshot no longer exists on disk).
- Lead: `mailboxes/lead/sent/2026-09-26-0650-lead-to-arch-…-sequencing-proposal-….md`.
- Code: `_process_intent_internal` (consult seam, multi-intent partition, rail block),
  `inversion_live.py`, `pre_classifier.detect_multiple_intents`, `orchestrator.py`,
  `destructive_confirm.build_todo_delete_confirmation`, the three named test files.

## Design (written before coding)

- **The loop** lives in `IntentService._maybe_dispatch_multi_intent_inversion`, called from
  `_process_intent_internal` immediately after the existing consult seam and only when
  `peek_live_route_provenance().reason == "multi_intent_split_stand_down"` — that peek is what
  couples the #1896 lift to the stand-down instead of re-probing every flagged turn.
- **Rail reuse**: the rail block (old lines 2911–3151) was extracted VERBATIM into
  `IntentService._dispatch_action_rail` returning `_RailOutcome`. Two callers, one body. No new
  `elif intent.action`, no second rail-membership dispatch decision.
- **Pause ends the turn** via `_RailOutcome.armed` (the #1190/#1509 gate returns) OR a #846 store
  peek across each dispatch (a handler that armed its own carrier). Remaining siblings are named
  by `_compose_deferred_sibling_line`.

## Work log

- **10:40** — session log created; mandatory reads.
- **10:45** — four read-only probes (no LLM): surface-1 split behavior on 25 candidate turns,
  rail membership + effect per emitted action, segment derivation, named-target resolution.
  **Finding that changed the test plan**: surface 1 cannot emit a WRITE/DESTRUCTIVE sibling at
  all, so the dispatch's named test turns (3)(4)(5) don't split. Rebuilt them so the destructive
  sibling comes from the CONSULT, on turns that really do split.
- **10:50** — implementation: `spans` on `MultiIntentResult` + `_first_pattern_match`;
  `sibling_segments` / `peek`+`publish` provenance / `multi_intent_sibling` in `inversion_live`;
  `_RailOutcome` + `_dispatch_action_rail` + `_maybe_dispatch_multi_intent_inversion` +
  `_compose_deferred_sibling_line` in `intent_service`.
- **11:00** — tests (24) green after three fixes: the stand-down now publishes its provenance
  (it returned early without one, so the seam never fired); pending-action intent is an object
  not a dict; the "one dispatch site" assertion rewritten to count `dispatch_workflow` call sites
  honestly (3, unchanged) instead of a substring that also matched a comment.
- **11:05** — docs: `intent-routing-stack.md` consult-seam paragraph + a full unit-4 block;
  `inversion_live.py` module docstring.
- **11:06** — gates: all green (below).

## Gates

| Gate | Result | Exit |
|---|---|---|
| `ruff format` / `ruff check --fix` (4 files) | 4 already formatted / All checks passed | 0 |
| `pytest tests/unit/services/intent_service/ tests/unit/services/intent/` | 4875 passed, 16 warnings, 133.58s | 0 |
| `pytest tests/test_architecture_enforcement.py` | 63 passed, 1 xfailed, 10.17s | 0 |
| `scripts/run-sweep.sh ratchets` | 73 passed, 1 xfailed; mypy: all 24 ratcheted codes at ceiling (total=1121) | 0 |

`MAX_DISPATCH_SITES = 0` before and after. `TestExtractionPatternRatchet` `pre-classifier`
ceiling 567 before and after (no new pattern literal — `_matches_patterns` is a byte-identical
delegator over the same single `re.search` pass).

## Discovered work filed

None filed as new issues — two findings belong to open issues and are reported to Lead:
1. **Residual #1896 face**: "what are my todos and delete my hydrate reminder" returns ONE
   intent from surface 1, so the split guard never fires and the whole-message consult can still
   answer the delete half and drop the read half. Needs option (b) (router-returned plan).
2. **#1606 still blocked twice over**: its turn doesn't split at surface 1, and `set_default_repo`
   is an unallowlisted WRITE. Lead's call whether either earns its own row.

## Memory & briefing surfaces referenced this session
- **Referenced** — `CLAUDE.md` (STOP conditions, evidence + "Verified how", m-43/m-44, session-log
  discipline, no-new-elif rule); `intent-routing-stack.md` (load-bearing for the whole design);
  Arch's two rulings; Lead's sequencing proposal; the 09-25 unit-4 design probe (its span recipe
  was reused verbatim in spirit).
- **Loaded but not referenced** — the Pard authorship incident memo; ROSTER.md.
- **Wanted but not found** — a single place stating which actions surface 1's multi-intent
  splitter can emit and their rail effects. I had to measure it; the measurement is now pinned as
  a test (`test_surface_one_emits_no_write_or_destructive_sibling`) and stated in the doc's
  unit-4 block, so the next agent doesn't re-derive it.
