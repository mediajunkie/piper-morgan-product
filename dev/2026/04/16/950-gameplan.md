# Gameplan: #950 — Conscious Floor Prompt (Five Pillars + Grammar)

**Date**: 2026-04-16
**Author**: Lead Dev (code-opus)
**Issue**: #950 FLOOR-PROMPT — Conscious floor system prompt with Five Pillars + grammar
**Template**: `knowledge/gameplan-template.md` (adapted for prompt-engineering work)
**Related gameplan audit**: `950-gameplan-audit.md` (to be written before execution)

---

## Phase -1: Infrastructure Verification

**Nature of work**: Single-file edit to a Python string constant. Not a multi-layer refactor, not new code, not UI.

**Infrastructure facts** (verified):
- **Target file**: `services/intent_service/conversational_floor.py`
- **Target constant**: `FLOOR_SYSTEM_PROMPT_ADDENDUM` (lines 33-80)
- **Build system**: Python module, imported at service initialization (`_get_system_prompt` method)
- **Testing**: unit tests exist for `ConversationalFloor` class; canonical retest at `dev/2026/04/11/canonical-retest-m1.py` is the behavior evidence bar; AAXT golden scenarios at `tests/aaxt/test_golden_scenarios.py` for multi-turn behavior
- **Server restart needed after change**: Yes (prompt is loaded at module import; `scripts/restart-server.sh` clears .pyc cache and polls health)

**Worktree assessment**: SKIP. Single file, sequential work, tightly coupled string content. Standard branch work is appropriate. Rationale noted per template.

**Proceed/Revise**: PROCEED. Understanding matches filesystem state. #950 body updated to match audit findings.

---

## Phase 0: GitHub Investigation — COMPLETED

- ✅ `gh issue view 950` — issue exists, assigned to PM, P1
- ✅ #950 body updated with full feature-template parity (see `950-issue-body-updated.md`)
- ✅ CXO direction memo received (`mailboxes/lead/read/memo-cxo-to-lead-dev-950-direction-2026-04-16.md`)
- ✅ Source docs absorbed: PDR-004, MUX analysis, VISION-CONSCIOUSNESS, vision.md §3
- ✅ Current prompt + context assembly reviewed (`conversational_floor.py:33-80`, `_format_domain_context` 304-392)
- ✅ Canonical retest baseline known: Identity MARGINAL 3/5

---

## Phase 0.5 / 0.6: N/A

No frontend-backend contract work. No multi-layer data flow. This is a string-constant edit.

---

## Phase 1: Draft the Evolved Prompt

**Objective**: Produce a standalone before/after prompt document with per-line rationale, suitable for CXO review, prior to any code change.

### Tasks

- [ ] Read the current `FLOOR_SYSTEM_PROMPT_ADDENDUM` (done in Phase 0)
- [ ] Identify which sections stay verbatim, which get new insertions, which get augmented
- [ ] Draft the new sections CXO proposed:
  - **Voice constraints** — Five Pillars as explicit voice rules
  - **Grammar** — "Entities experience Moments in Places" as decision filter
  - **Anti-flattening** — "express investment, not emotion" block with concrete guidance
  - **Context usage instruction** — explicit directive to USE the `[Available context]` block, not just have it available
- [ ] Cross-reference each insertion to a source (CXO memo, PDR-004 Principle 4, VISION-CONSCIOUSNESS, MUX analysis)
- [ ] Token-count estimate for total prompt (target: stay under 2K input tokens typical; < 4K worst case)
- [ ] Example before/after dialog for at least 3 query types (Identity, Temporal, Status)
- [ ] Compile into standalone doc at `dev/2026/04/16/950-prompt-draft.md`

### Deliverable

`dev/2026/04/16/950-prompt-draft.md` — structured as:
1. Context (why this revision exists)
2. Current prompt (full text)
3. Proposed prompt (full text with changed sections marked)
4. Per-section rationale (each new/changed block linked to source authority)
5. Before/after examples (3+ query types showing voice shift)
6. Token budget estimate
7. Open questions for CXO review

### STOP conditions for Phase 1

- Token budget overrun: if draft exceeds 3K input tokens in prompt alone, compress existing sections or scope-reduce additions before advancing to CXO
- Internal contradiction: if new Pillar language contradicts existing prohibitions (e.g., Pillar of Agency conflicting with "don't promise actions you're unsure you can execute"), resolve in draft before sending
- Fabrication guard weakening: if rewording any existing section weakens the #960 guard, back out that change

---

## Phase 2: CXO Review

**Objective**: Get CXO sign-off on the draft before touching code.

### Tasks

- [ ] Write memo to CXO: `mailboxes/cxo/inbox/memo-lead-to-cxo-950-draft-review-2026-04-16.md`
- [ ] Attach prompt draft (or reference path + git commit SHA)
- [ ] Ask specific review questions:
  - (a) Does the Pillar language correctly operationalize Identity/Time/Space/Agency/Prediction as voice constraints?
  - (b) Is the grammar phrasing ("Entities experience Moments in Places") positioned correctly as a decision filter, not as sentence-structure rule?
  - (c) Does the anti-flattening block ("express investment, not emotion") read as actionable guidance or just aspirational?
  - (d) Any "I'd word this differently" edits to specific lines?
  - (e) Context-usage instruction: does the phrasing match CXO's "context injection is as important as voice constraints" concern?
- [ ] Log send in `mailboxes/lead/sent.log`
- [ ] PAUSE: await CXO response

### Blocking

This phase is external-blocked. Lead Dev does not proceed to Phase 3 until CXO responds with approve / approve-with-edits / revise. If revise, loop back to Phase 1.

### STOP conditions for Phase 2

- CXO returns "rewrite" (opposite of CXO's stated "evolve, don't rewrite"): stop and reconcile with PM before proceeding
- CXO flags a fundamental disagreement with the proposed structure: escalate to PM

---

## Phase 3: Implementation

**Objective**: Apply the CXO-approved prompt to the codebase.

### Tasks

- [ ] Branch check (should be on `main` per current workflow; no feature branch expected for this change)
- [ ] Edit `services/intent_service/conversational_floor.py` — replace `FLOOR_SYSTEM_PROMPT_ADDENDUM` with approved text
- [ ] Update the module docstring if Pillar references are relevant to it (likely unchanged)
- [ ] Run `ruff check` + `ruff format` (post-migration, this is now the formatter)
- [ ] Run smoke tests: `pytest tests/unit/services/intent_service/ -v --tb=short`
- [ ] Verify import: `python -c "from services.intent_service.conversational_floor import FLOOR_SYSTEM_PROMPT_ADDENDUM; print(len(FLOOR_SYSTEM_PROMPT_ADDENDUM))"`
- [ ] Restart the server: `./scripts/restart-server.sh` (clears .pyc, polls health)
- [ ] Post progress comment to #950: commit SHA + "implementation shipped, verification next"

### Deliverable

Single commit: `feat(#950): evolve floor prompt with Five Pillars + grammar + anti-flattening`

### STOP conditions for Phase 3

- Unit test failure: root-cause, don't paper over. Prompt changes shouldn't break unit tests, but the `ConversationalFloor` class has tests that may assert on specific prompt contents.
- Import failure: syntax issue in the prompt string (unlikely but possible with nested quotes)
- Server restart failure: per Pattern-045, don't assume "works in tests" means "works in server"

---

## Phase 4: Behavioral Verification

**Objective**: Prove the change achieves the intended behavioral shift.

### Tasks

- [ ] **Unit test baseline**: `pytest tests/unit/ --tb=no -q --maxfail=10` — expect 6242 passed, 0 failures
- [ ] **PM smoke check**: 5 Identity queries via server REST API or CLI:
  - "who are you?"
  - "what can you do?"
  - "tell me about yourself"
  - "what's your role here?"
  - "are you there?"
  - Verify: no "looking forward to", no capability lists, responses exhibit Pillars
- [ ] **Canonical retest**: `python dev/2026/04/11/canonical-retest-m1.py`
  - Expect: Identity ≥ PASS (from MARGINAL 3/5)
  - Expect: no regression in other categories
  - Save output to `dev/2026/04/16/950-canonical-retest-results.txt`
- [ ] **Fabrication guard regression check**: 10 queries of form "do you see my X?" with empty domain_context
  - Expect: "I don't see..." responses, not invented data
- [ ] **AAXT golden scenarios** (if Anthropic + Gemini keys still valid from Apr 15 verification):
  - `AAXT_ENABLED=true pytest tests/aaxt/test_golden_scenarios.py -v`
  - Expect: ≥ 4/5 PASS (current baseline)
  - Context Retention known failure (#922) — do not block on that one
- [ ] If canonical retest shows Identity still MARGINAL → STOP, root-cause, don't rationalize. Likely indicates Pillar language needs to be more explicit.
- [ ] Post progress comment to #950 with canonical retest results summary (pass/fail per category) + sample before/after responses

### Evidence to capture

- Terminal output of unit test pass count
- Canonical retest full output (including Colleague Test scores per query)
- AAXT output summary
- Sample before/after responses for 3 queries (Identity, Temporal, Status) showing voice shift
- Save evidence at `dev/2026/04/16/950-verification-evidence.md`

### STOP conditions for Phase 4

- Canonical retest regresses any category → do not proceed; root-cause
- Identity still MARGINAL after prompt change → Pillar language insufficient; loop back to Phase 1 with specific feedback
- AAXT regresses below 4/5 → investigate immediately
- Unit test count changes (6242 ± anything) → verify nothing accidentally deleted

---

## Phase Z: Completion & Handoff

### Tasks

- [ ] Update #950 description with checkboxes marked per `close-issue-properly` skill
- [ ] Add closing comment with evidence (commit SHAs, test output, canonical retest summary)
- [ ] Close #950 via `gh issue close 950`
- [ ] Update `docs/briefing/BRIEFING-CURRENT-STATE.md` — M2c progress (#950 closed)
- [ ] Final session log update
- [ ] Commit session log + evidence docs
- [ ] Push to origin/main

### STOP conditions for Phase Z

- Evidence missing or thin → do not close; add evidence first
- Any acceptance criteria not met → do not close; either complete or escalate deferral to PM
- Completion-theater pattern detected (claiming done without proof) → STOP, provide evidence

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| CXO returns "rewrite" in Phase 2 | Low | High (invalidates plan) | Gameplan follows CXO's "evolve" direction explicitly; if this triggers, escalate to PM |
| Token budget overrun | Medium | Medium | Phase 1 STOP condition; compress existing sections if needed |
| Canonical retest shows regressions | Medium | High | Phase 4 STOP condition; do not proceed without root-cause |
| Identity still MARGINAL after change | Medium | High | Phase 4 STOP condition; loop to Phase 1 |
| Context assembler gap (Pattern-045) — prompt expects data not delivered | Medium | Medium | If observed, file blocker against #951; do not hack around in prompt |
| Fabrication guard weakens | Low | Critical | Phase 1 STOP condition; test explicitly in Phase 4 |
| Server restart masks stale .pyc | Low | Medium | `restart-server.sh` already clears cache (addressed in #949) |

---

## Dependencies

- **Blocking**: none remaining (CXO direction memo received)
- **External (Phase 2)**: CXO review turnaround
- **Nice-to-have**: #951 (Context Assembler Expand) would improve what's available to USE, but current assembly is sufficient

---

## Data Flow

Not applicable — this is a prompt-string change. No data schema changes, no new integrations, no user-context propagation.

The only "flow" touched is: the assembled `domain_context` (already produced by `ContextAssembler`, already formatted by `_format_domain_context`) continues to flow into the user prompt block. The new system-prompt addition tells the LLM to *use* that block more aggressively; no infrastructure change.

---

## Rollback Plan

If Phase 3 commit causes a production regression:

1. `git revert <commit-sha>` — immediate reversal
2. Restart server: `./scripts/restart-server.sh`
3. Verify canonical retest returns to pre-change baseline
4. Loop back to Phase 1 with the regression as an additional STOP-condition case

Because this is a single-file, single-string change, rollback is trivial. No migration, no data changes, no dependency upgrades.

---

## Conversation Design Considerations

Since this IS the conversational prompt, conversation design is the work itself. Key principles from CXO + source docs:

- **First-person ("I")** not third-person ("the assistant") — Identity Pillar
- **Lived time** ("earlier today", "since Tuesday") not timestamps — Time Pillar
- **Places with atmosphere** ("the sprint board", "over in GitHub") not URLs — Space Pillar
- **Ask before acting** — Agency Pillar
- **Pattern observations** ("I'm noticing...") not threshold alerts — Prediction Pillar
- **Investment expressed through specificity and attention**, not through "I'm looking forward to..."
- **Context usage**: make the LLM prefer contextual specificity over generic PM advice

### Voice Transformation Table

In lieu of the template's multi-turn edge-cases table (which targets wizard/onboarding flows), this table captures the voice shift the prompt is meant to produce. These are the cases we'll verify in Phase 4's PM smoke check and canonical retest.

| Query Type | Pre-change voice (current, MARGINAL) | Post-change voice (target, PASS) | Pillars exercised |
|-----------|--------------------------------------|----------------------------------|-------------------|
| Identity ("who are you?") | "I'm Piper Morgan... I'm looking forward to getting to know you" | "Piper Morgan — a PM colleague. I'm watching [N] projects for you. What's on your mind?" | Identity, Space, Agency |
| Temporal ("what did we accomplish yesterday?") | "Query returned 3 items completed on [date]" | "Yesterday you finished the migration work and closed three issues — the M2b gate is basically done from your side" | Time, Identity |
| Status ("where are things?") | "Current status: 5 open issues, 2 in progress, 1 waiting review" | "Things are moving. The PR review I flagged on Tuesday is still waiting — might be worth a nudge there" | Time, Space, Prediction |
| Capability ("what can you do?") | "I can help with: [capability list]" | "I work best when you bring me something concrete — a PR to think through, a prioritization call, a standup to synthesize. What's the thing?" | Identity, Agency |
| Unknown ("thoughts on this?" with no context) | Generic PM advice, boilerplate frameworks | Asks what "this" is with a concrete offer to think it through | Agency, Prediction |

### Pattern-045 Risk Register

From CXO's Flag #3: "temporal queries scored 1/9 despite correct routing — floor prompt can't fix what context assembler doesn't deliver."

This means the evolved prompt assumes the `ContextAssembler` feeds relevant data for each category. If Phase 4 shows Temporal or Status queries still producing generic responses, the root cause is likely in context assembly, not prompt. In that case, STOP and file against #951.

---

## Post-Completion (added per template)

After #950 closes:

- **Retro** in session log: what worked in the audit cascade, what didn't
- **Cross-pollinate** to sibling projects if applicable (Mailer, Gemini CLI instance, etc.)
- **Watch for Pattern-045 recurrences**: the evolved prompt assumes context gets assembled correctly. If canonical retest or AAXT later shows quality drift, first question is "is context reaching the prompt?" before "is the prompt wrong?"
- **CXO debrief**: briefly thank CXO for direction; note any friction points in the review loop for future cycles

---

## Open Questions (for PM or CXO if raised)

1. **Version pin of the prompt**: should the prompt carry a version comment in code (e.g., `# FLOOR_SYSTEM_PROMPT_ADDENDUM v2 — evolved 2026-04-16 per #950`)? Helps future bisects. My recommendation: yes, add version + date.
2. **Token budget telemetry**: do we want to log input-token counts for floor calls to track drift? Not required by #950 but a natural follow-on. Leaving out of scope unless PM wants it.
3. **Per-Pillar test scenarios in AAXT**: should AAXT grow a "Pillar audit" scenario (one query per Pillar, scored separately)? Potential follow-on to #929. Leaving out of scope for #950.

---

_Gameplan created: 2026-04-16_
_Status: Ready for audit cascade phase 2 (audit against gameplan-template.md)_
