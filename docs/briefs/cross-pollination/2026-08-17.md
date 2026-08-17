
# Cross-Pollination Brief — August 17, 2026

Two findings from yesterday's window: Klatch's Round 60 identifies where a recurring agent failure actually lives — not in the model, but in a prior decision the model makes at different rates; Piper Morgan finds that prompt guidance meant to prevent a wrong answer can itself supply the template for it.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### A failure to surface information may be downstream of a prior decision — the model sets that decision's rate, not the outcome once it's made

**From:** Klatch (Theseus, `docs/research/round60-sonnet-on-k-live-2026-08-16.md`, 2026-08-16)
**Relevant to:** Piper Morgan, Design in Product, any team diagnosing LLM agent failure modes

Round 60 ran arm K — a longer conversation than arm F — on both opus-5 and sonnet-5 interleaved. The result corrects Round 59's published headline. The key finding is not the per-model rates but what holds constant across all 20 runs:

When an agent expands to retrieve context (takes the offered address), it surfaces the deep condition **8/8 times** — across both models, both arms. When it doesn't expand, it surfaces nothing: **0/12** — again across both models and both arms, including two opus-5 runs that behaved identically to every sonnet-5 run. Stratified across arms F and K, the model difference in *expansion rate* is real (all 8 expansions fell to opus, p = 6.6 × 10⁻⁴), but the model difference in *disclosure given expansion* is zero.

Theseus's corrected framing: "The true partial-disclosure failure is a property of not taking the address, not a property of the model. The model only sets how often that state is entered."

A parallel confound was found in the arm design: the mechanism that creates depth in arms F and K (inserting a filler exchange between handover and restriction) also makes the restriction's pronoun ambiguous — "keep it between us" has two possible referents in a conversation where the filler pair covers an unrelated topic. Agents that declined the address may have been declining pending clarification, not disobeying a clear rule. Filed as a new arm variant (same depth, filler moved after the restriction to remove the ambiguity); the existing arms' structural claims are unaffected.

**Suggested action:** When investigating why an agent fails to surface information, check whether the failure is conditional on a prior action the agent chose not to take — and check whether the prior action itself has confounds (here: depth and referential clarity co-vary). The diagnostic question "does this model fail to disclose X?" may decompose into "does this model take the action that would expose X?" and "given that action is taken, does it disclose X?" Those are different questions with potentially different answers, and interventions that assume model-level failure may miss the actual leverage point.

---

### Anti-hallucination prompt examples can become templates for the wrong output they are meant to prevent

**From:** Piper Morgan (Lead Dev, commit 5a200b2b, 2026-08-16; issue #1544)
**Relevant to:** Klatch, Design in Product, any project using LLM system prompts with anti-fabrication guidance

PM's floor system prompt included a "never fabricate" section with worked examples of prohibited output: "I don't see any todos in your list right now" and "...nothing's showing up on my end for this conversation." When the model encountered an ambiguous state — unable to distinguish "user has no pending todos" from "todos were never fetched" — it assembled PM's response verbatim from those example phrases. The phrases intended to show what NOT to say became the model's template for what to say when uncertain.

Two defects composed: (a) the prompt's examples seeded the wrong copy directly; (b) the data layer returned `None` for zero rows, making "verified-empty" structurally indistinguishable from "never gathered." The floor therefore couldn't hold a definite "checked, zero" fact. Fix: rewrite the guidance in structural terms ("data absence is a visibility claim about this turn's context, never a conversation-scoped fact; the empty-list claim is licensed only by a verified-empty context line") and change `_compute_pending_todos` to return `{"pending_todos": [], "pending_todo_count": 0}` on a successful zero-row read, so the floor renders "PENDING TODOS: none — checked this turn" rather than a hedge.

**Suggested action:** In anti-hallucination system prompts, avoid including exact phrasing examples of wrong output — even explicitly labeled "never say this." The model may treat those examples as templates when it reaches an uncertain state, not as patterns to reject. Prefer structural rules: state what IS true in verifiable terms. If examples are necessary for clarity, pair them with an explanation of what structural property makes the example wrong (not just the label). Separately: the data-layer fix matters independently — a system that can't distinguish "absence confirmed" from "absence unverified" forces its prompt layer to hedge, and hedging with a fabricated example produces exactly this failure.

---

## Sources Read

- **Klatch** — `docs/research/round60-sonnet-on-k-live-2026-08-16.md` (Theseus, Round 60 full write-up); `docs/logs/2026-08-16-2130-calliope-sonnet-log.md` (rollup v48 with Round 60 and tool_use client build)
- **Piper Morgan** — `dev/2026/08/16/2026-08-16-0642-lead-code-log.md` (Lead Dev day log); commit 5a200b2b (issue #1544 fix with commit-message root-cause summary)
- **Globe** — delivery commits only (briefs from Aug 14–16)
- **Weather** — delivery commits only (briefs from Aug 14–16)
- **One-job** — `development/coral-logs/2026-08-16-coral-log.md` (multi-deck backup bug fixed; 3-day deploy freeze found and root-caused — CI/local npm version discrepancy; no brief-worthy methodology insight beyond what the updated CLAUDE.md TOOLCHAIN TRAPS section covers)
- **Mediajunkie** — duty-cycle monitoring logs; swap fix holding steady through the day boundary; no new finding
- **nyt-crossword** — status-fetch commits only; no agent narration
- **Cookie-monster** — delivery commits only; no new agent activity

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
