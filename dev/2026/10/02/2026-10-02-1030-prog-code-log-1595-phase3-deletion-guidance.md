# 2026-10-02 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 seventh deletion (GUIDANCE_PATTERNS)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`. Task: seventh Phase 3 deletion ratchet unit — tombstone `GUIDANCE_PATTERNS` (21 literals) in `services/intent_service/pre_classifier.py`.

## Outcome: STOPPED — disagreeing reabsorption found at the AFTER check

Did not commit, did not leave the tombstone in place. Reverted `pre_classifier.py` to its pre-session state (confirmed via `git diff --stat` — empty).

## BEFORE gate (quoted)

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list GUIDANCE_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo
```

```
corpus denominator: 385 rows total = 125 claimed + 260 unclaimed

## GUIDANCE_PATTERNS
literals: 21  |  rows claimed: 21/385
verdict: GO (deletable) — deleting removes 21 literals: ceiling 329 -> 308
```

21/21 rows `[OK]`, 0 `[FAIL]`, 0 "needs a corpus row" literals (gate's own line: "pattern->corpus conversion: every literal in this list is exercised by >=1 corpus row"). Proceeded per the dispatch's ordering rule.

Four rows pass under Arch's 2026-10-02 condition (d) — router MISMATCH/declined, but a frozen N=5 surface-2 probe shows the LLM classifier landing the phrase in GUIDANCE on every sample:
- "I could use some guidance on this" — anthropic:claude-sonnet-4-6 5/5, openai:gpt-4o 5/5 (both land `provide_guidance`/GUIDANCE)
- "do you have a recommendation" — anthropic 5/5, gpt-4o 5/5 (`provide_guidance`/`provide_recommendation`, both GUIDANCE)
- "what's your advice here" — anthropic 5/5, gpt-4o 5/5 (`provide_guidance`, GUIDANCE)
- "ok that's merged, what now?" — anthropic 5/5, gpt-4o 5/5 (`provide_guidance`/`provide_next_steps`/`prioritize`, all GUIDANCE category)

Source reports: `docs/internal/architecture/current/inversion-phase3-surface2-floor-probe-2026-10-02-n5-anthropic.md`, `...-n5.md` (gpt-4o leg).

Measured `total_literal_count()` (manual sum over all `*_PATTERNS` class attributes) = 329, matching `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` = 329 (pre-deletion baseline confirmed correct).

## Tombstone applied (temporarily, to run the AFTER probe) then reverted

Applied the standard seventh-deletion tombstone (`GUIDANCE_PATTERNS = []  # type: List[str]` + comment block, claim-branch dead-code comment, mirroring the sixth deletion's template exactly) to run the empirical AFTER reabsorption check against the live `PreClassifier`. Then **reverted both edits** once the STOP condition below was confirmed — `git diff --stat services/intent_service/pre_classifier.py` is empty.

## AFTER check: reabsorption scan (all 21 claimed phrases, `pre_classify_with_pattern_list`)

17 of 21 phrases came back `UNCLAIMED` post-tombstone (clean — ready for the LLM/floor to reach by category). **4 phrases were reabsorbed, and all 4 DISAGREE with the ruled destination:**

| phrase | ruled/expected | reabsorbed by | reabsorbed action | agrees? |
|---|---|---|---|---|
| "I need to setup my projects" | `action:get_contextual_guidance` | `STATUS_PATTERNS` (literal `\bmy projects\b`) | `get_project_status` | **NO** |
| "how do I configure my projects" | `action:get_contextual_guidance` | `STATUS_PATTERNS` (literal `\bmy projects\b`) | `get_project_status` | **NO** |
| "I want to set up my projects" | `action:get_contextual_guidance` | `STATUS_PATTERNS` (literal `\bmy projects\b`) | `get_project_status` | **NO** |
| "I'd like to set up my portfolio" | `action:get_contextual_guidance` | `STATUS_PATTERNS` (literal `\bmy portfolio\b`) | `get_project_status` | **NO** |

Confirmed the claiming literal directly (regex scan of `STATUS_PATTERNS` against each phrase, pre-tombstone list, no LLM involved):
```
I need to setup my projects -> \bmy projects\b
how do I configure my projects -> \bmy projects\b
I want to set up my projects -> \bmy projects\b
I'd like to set up my portfolio -> \bmy portfolio\b
```

Confirmed the ruled/expected destination for all 4 in `tests/fixtures/inversion_corpus_phase0.yaml` (lines 724-761): `category: GUIDANCE`, `expected: action:get_contextual_guidance`, sourced from GUIDANCE_PATTERNS literals `\bsetup.*projects?\b`, `\bconfigure.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b` respectively.

**Why this is worse than the sixth deletion's "pattern not load-bearing" shapes, not just a routine reabsorption**: the BEFORE gate's own row output shows all 4 of these phrases scoring `MATCH` against the frozen router (`get_contextual_guidance@0.85` / `@0.95`) — i.e. if GUIDANCE_PATTERNS is removed and the phrase reaches the LLM classifier (surface 2), it lands correctly. But `STATUS_PATTERNS`' pre-existing `\bmy projects\b`/`\bmy portfolio\b` literals claim these phrases *deterministically, before surface 2 ever runs* — `pre_classify` checks STATUS_PATTERNS ahead of GUIDANCE_PATTERNS in its if-chain (both are unconditional substring/regex checks, no blocker guard). So deleting GUIDANCE_PATTERNS would not fall through to a correct LLM landing for these 4 rows — it would produce a confident, deterministic, WRONG route (`get_project_status` instead of `get_contextual_guidance`) that previously could not happen (GUIDANCE_PATTERNS claimed first and won). This is a genuine regression the dispatch's STOP condition ("a reabsorption DISAGREES") exists to catch.

## Per the dispatch's explicit STOP condition

> STOP and report instead of guessing if: ... a reabsorption DISAGREES.

Stopping here. Did not proceed to steps 5-8 (the `--all` gate split, ceiling lower, test conversions, doc append) since the deletion itself is not currently safe to make.

## What I did NOT do (scope discipline)
- Did not touch `scripts/inversion_phase3_deletion_gate.py` (per instructions).
- Did not modify `scripts/inversion_phase3_deleted_patterns.json`, any test file, `tests/test_architecture_enforcement.py`, or the routing-stack doc — no partial/half-applied ledger or ceiling change left behind.
- Did not call any LLM — the four condition-(d) probe facts were read from the two existing frozen probe-report files, not re-derived.
- Did not `git add` or `git commit` anything (no changes remain in the working tree for this file — confirmed clean).

## Open question for Lead/Arch

Does this block the GUIDANCE_PATTERNS deletion outright, or is there a narrower fix (e.g., the two STATUS_PATTERNS literals `\bmy projects\b`/`\bmy portfolio\b` could be scoped tighter, or these 4 phrases could be excluded from the deletion's claimed-row set with a documented carve-out, or the STATUS/GUIDANCE if-chain order could matter)? Flagging rather than picking — this is a cross-list design call, not a mechanical ratchet step.

## Verified how
- **Method**: ran `scripts/inversion_phase3_deletion_gate.py --list GUIDANCE_PATTERNS --live ...` (BEFORE); applied the tombstone edit; ran `PreClassifier.pre_classify_with_pattern_list(phrase)` for all 21 claimed phrases (AFTER, empirical, no LLM); regex-scanned `STATUS_PATTERNS` directly against the 4 reabsorbed phrases to name the exact claiming literal; grepped `tests/fixtures/inversion_corpus_phase0.yaml` to confirm the ruled destination; reverted the edit and confirmed `git diff --stat` is empty.
- **Layer**: deterministic/unit only (real corpus fixture, real `PreClassifier` code, real frozen router-probe report files read as data) — no LLM calls this session, consistent with the dispatch's "No LLM calls anywhere" constraint.
- **Denominator**: all 21/21 claimed rows checked at BEFORE; all 21/21 claimed phrases checked at the AFTER reabsorption scan (not a sample) — 4/21 reabsorbed, 4/4 of those disagreeing.

## Memory & briefing surfaces referenced this session
- **Referenced**: CLAUDE.md worktree/sign-off/subagent-dispatch rules (session conduct); sixth-deletion commits (`d1e954f08b`, `02c73d6dc1`) as the structural template for the tombstone comment, ledger shape, and test-conversion idiom; `tests/unit/test_inversion_phase3_deletion_1595.py` docstrings for the ledger field shapes (`shadowed_literals`, `misserved_at_deletion`, `surface2_verified_at_deletion`); the two surface-2 floor-probe reports for the condition-(d) evidence.
- **Loaded but not referenced**: most of the skill listing (duty-cycle, mail, blog-drafting skills — not applicable to this coding task).
- **Wanted but not found**: no existing doc cross-referencing STATUS_PATTERNS' `\bmy projects\b`/`\bmy portfolio\b` against GUIDANCE's setup-phrase literals as a known collision — this appears to be a new finding, not a previously-flagged gap.
