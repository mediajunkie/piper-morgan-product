# #1122 MULTI-TURN-DOC-ANTECEDENT — Investigation (2026-05-27)

**Investigator**: Lead Developer subagent
**Mode**: Diagnosis only (no code changes)
**Status**: Root cause identified, fix shape proposed for PM disposition

---

## TL;DR

The `_handle_update_document_notion` handler (services/intent/intent_service.py, grep "Issue #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING") calls `extract_slots(message=original_message, template=DOCUMENT_UPDATE_TEMPLATE, llm_service=...)` with **only the current turn's text**. `original_message` resolves to the literal current message ("Please add a new paragraph to the doc..."). When the user says "the doc," there is no antecedent in that string, the LLM returns `{}` for `doc_name`, and the handler emits the canned "I need to know which document to update" clarification (grep "I need to know which document to update").

The fix is not narrowly inside #1121; it is **architectural**. `extract_slots()` accepts no `conversation_history` parameter (grep "async def extract_slots"). The slot-extractor prompt template (grep "User message:") refers only to the current message. Conversation context EXISTS as a sliding 10-turn window (services/intent_service/conversation_context.py, grep "max_turns: int = 10") but is consulted only by the regex follow-up detector and the LLM follow-up decoder in the classifier path — never by the dispatch handlers.

PM's "this worked in July 2025" memory is **almost certainly mistaken about the date** — `services/intent_service/conversation_context.py` did not exist until 2026-01-27 (commit bbb741cdb, "feat(#427): Add conversation context for follow-up detection"); `services/intent_service/document_handlers.py` was created 2025-11-01 (commit 2452ba9ae, Issue #290). There was no per-session entity memory in July 2025. The "worked then" behavior was more likely "the conversation was QUERY-shaped and the LLM had recent turns in the prompt directly," not "the dispatch handler resolved antecedents." That doesn't change the validity of the user-facing bug — but it does mean we are **building entity-antecedent resolution for the dispatch path for the first time**, not restoring something that decayed.

---

## Architecture: How conversation context flows turn-to-turn

**Where context lives** (services/intent_service/conversation_context.py):

- Module-level `_conversation_contexts: dict[str, ConversationContext]` is a process-local in-memory store keyed by `f"{user_id or 'anonymous'}:{session_id}"` (grep "_context_key").
- `ConversationContext` holds `turns: list[ConversationTurn]` (max 10, max 30 min) plus a `lens_stack` and a one-turn `last_offer` field.
- `ConversationTurn` records: `message`, `response`, `intent`, `temporal_reference`, `entity_references` (list[str]), `topic`, `lens`.
- The `entity_references` field carries a load-bearing comment: **"stored, not yet consumed (audit #827)"** (grep "stored, not yet consumed"). This is the dead-code symptom: entities are saved but no read path consumes them.

**Where context is consulted** — classifier path only (services/intent_service/classifier.py):

- grep "get_or_create_context(session_id)" → loads conv_context into the classification context.
- grep "detect_follow_up" → regex-based detection of follow-up shapes ("how about today?", "yes", "that one").
- grep "decode_follow_up_with_llm" → LLM decode when a conversational lens is active.
- grep "conv_context.add_turn" → records the new turn AFTER classification, with `temporal_reference` and `topic` extracted but `entity_references` left empty (grep "extract_topic(message, intent)" — no equivalent `extract_entity_references`).

**Where context is NOT consulted** — dispatch handlers in intent_service.py:

- `_handle_update_document_notion` (grep "Processing document update via Notion") only reads `intent.context.get("original_message", "")` — the current turn's message text.
- The LLM classifier (`services/intent_service/llm_classifier.py`) builds the classification prompt without conversation history (zero matches for "conversation_history\|conv_context\|history" in that file).
- The slot extractor (`services/slot_filling/slot_extractor.py`) builds its prompt with only `User message: "{message}"` (grep "User message:") and existing slot values from THIS turn's state.

**Net result**: The conversation_context module is a sophisticated infrastructure-layer module that is consulted ONLY for follow-up phrase detection (regex + lens-decoded LLM) at the classifier level. Once the classifier returns an `Intent`, the dispatch handler runs against a single-turn string. Entity antecedent resolution has no read path.

---

## Slot-extractor capability assessment

`async def extract_slots(message, template, llm_service, existing_values=None)` (grep "async def extract_slots") has no parameter for conversation history. The prompt builder `_build_extraction_prompt` (grep "def _build_extraction_prompt") interpolates only:
- The template's slot definitions and extraction hints
- Optionally `existing_values` (already-filled slots THIS extraction is updating)
- `User message: "{message}"` — the single current turn

To support antecedent resolution, the function signature would need a new param (e.g., `conversation_history: Optional[list[dict]] = None`), the prompt builder would need to interpolate recent turns, and the prompt instructions would need to direct the LLM to resolve pronouns/antecedents against that history (grep "Extract ONLY values explicitly stated").

**Cost**: small library-level change (~30 lines including type hints and a docstring). The riskier part is the prompt-engineering: the LLM must be told to resolve antecedents WITHOUT hallucinating across unrelated entities (e.g., if turn 1 mentioned "the README" and turn 5 mentions "the doc" after intervening unrelated turns, which one is "the doc"?). The `meeting` workflow already proves that LLM-based slot extraction over conversational state is workable (the slot_filling_manager session model exists for this) — but that mechanism is invoked only when a workflow is ACTIVE, not for ad-hoc one-shot intent dispatches.

---

## Bisect findings

The bisect frame "worked in July 2025, broken now" doesn't survive the file-creation timeline:

- `services/intent_service/conversation_context.py` — **created 2026-01-27**, commit bbb741cdb, "feat(#427): Add conversation context for follow-up detection." Before this date, there was no per-session conversation memory module.
- `services/intent_service/document_handlers.py` — **created 2025-11-01**, commit 2452ba9ae, "feat: Complete Issue #290 - All 6 document processing workflows." Pre-November, there were no document-specific handler functions at all.
- `services/intent/intent_service.py::_handle_update_document_notion` — added much later (Notion integration arrived in late 2025 per `433a4a0b6 feat(#1080): real Notion append_blocks`).
- `services/slot_filling/slot_extractor.py` — created with Issue #765 GLUE-SLOTFILL, also recent.

**The "regression" PM remembers from July 2025 is not the same code path.** In July, the system was running on the pre-handler-decomposition architecture (intent_service.py was a monolith hitting LLM-driven response generation more directly). PM's anecdotal recall of "mentioning a doc by antecedent worked" most plausibly corresponds to a LLM-conversation flow where recent turns were always in the prompt to the LLM response generator. That conversational mode still works (see AAXT discrepancy below) for QUERY-shaped messages — what does NOT work is the post-Nov 2025 architectural choice to route document UPDATE to a structured slot-extraction path that bypasses history.

**Recommendation**: drop the bisect frame. This is not a regression of working code; it is a **gap introduced by the late-2025/early-2026 decomposition into structured dispatch handlers**. The same gap will exist for every other slot-filled action (todo updates, calendar event edits, issue edits — wherever a handler uses `extract_slots(message=original_message, ...)` with no history).

---

## AAXT discrepancy explanation

`tests/aaxt/test_golden_scenarios.py::TestContextRetention::test_pronoun_resolution_across_turns` (grep "test_pronoun_resolution_across_turns") sends:

- Turn 1: "I need to plan a stakeholder presentation for next week"
- Turn 2: "Can you help me structure that?"

Turn 1 classifies as something CONVERSATION/QUERY-shaped, NOT a structured-action intent like `update_document`. Turn 2 classifies similarly. **Neither turn enters the dispatch-handler path**; both flow through the LLM-driven response generation (conversational floor or QUERY handler) where recent turns ARE passed to the LLM as context (e.g., grep "conversation_history=history" — there are 6 hits in intent_service.py, all in floor/QUERY/error-recovery paths, none in the slot-filling handler path).

Additionally, the judge's pass criterion is loose: "Did the response help structure a presentation, not ask what 'that' is?" The judge passes if the LLM produces ANY structuring-help response, which the LLM does because it sees the full conversation in its prompt. The test does not verify entity-binding semantics.

PM's scenario differs because:
1. Turn 1 ("Hi Piper! Please update the Piper Morgan test page doc...") classifies as `update_document` → routes to `_handle_update_document_notion` → handler succeeds because doc_name is extractable.
2. Turn 2 ("Please add a new paragraph to the doc...") also classifies as `update_document` (it contains "update" verbs and "doc") → routes to same handler → handler tries `extract_slots(message=this_single_message, ...)` → LLM cannot find a doc_name in that string → handler emits clarification.

The AAXT test would only catch this if it specifically targeted the structured-dispatch path with an antecedent across turns AND asserted on the response shape ("does NOT contain 'I need to know which document'"), not the LLM judge's fuzzy "did it help" verdict.

---

## Recommended fix shape

Three options, ordered by scope:

**(A) Narrow fix — handler resolves antecedent from conversation_context** (~50-100 lines, scoped to update_document):
- In `_handle_update_document_notion` (grep "Processing document update via Notion"), before calling `extract_slots`, check `get_or_create_context(session_id, user_id)`.
- If `doc_name` slot comes back empty AND the previous turn's intent was also `update_document` (or referenced a doc), reuse the previously-resolved doc_name (which would need to be persisted in turn.entity_references or a new field).
- Pros: localized, testable, ships fast. Cons: doesn't generalize; every slot-filled handler needs its own version of this; doubles down on the bespoke-handler pattern that #1124 PRE-FLOOR-HANDLER-AUDIT is trying to retire.

**(B) Medium fix — extend extract_slots to accept conversation_history** (~30 lines in slot_extractor + ~5 lines per call site):
- Add `conversation_history: Optional[list[dict]] = None` to `extract_slots()`.
- Update the prompt builder to interpolate recent turns when present, with explicit instructions about pronoun resolution.
- Update `_handle_update_document_notion` (and future slot-filled handlers) to pass `conversation_history` derived from `get_or_create_context(session_id, user_id).turns`.
- Pros: generalizes to every workflow that uses extract_slots; makes slot-filling the conversation-aware primitive. Cons: prompt-engineering risk (hallucination across unrelated antecedents); needs golden test coverage.

**(C) Broad fix — entity-antecedent resolution as a classifier-stage primitive** (~200+ lines, infrastructure):
- Add an entity-resolution pass in the classifier between pre-classification and LLM classification, modeled on the existing `detect_follow_up` step.
- When the message contains a known antecedent phrase ("the doc", "that issue", "the one I mentioned"), look up the most recent matching entity from `conversation_context.turns` and substitute or attach the resolved entity to `intent.context.resolved_entities`.
- Have dispatch handlers consult `intent.context.resolved_entities` as a first-class slot source.
- Pros: solves the general problem PM frames in the issue ("any antecedent reference"); aligns with #1124 PRE-FLOOR-HANDLER-AUDIT direction; finally consumes the `entity_references` field that's currently dead (audit #827). Cons: bigger change; touches the classifier; needs extensive testing across categories.

**My recommendation**: **(B)** for the immediate fix on #1080's path (1-2 day scope), with **(C)** scoped as a follow-on for general antecedent resolution (3-5 day scope, post-M2). (A) is tempting but ships exactly the bespoke per-handler logic that #1124 was filed to retire — every shortcut in this direction makes #1124 harder.

---

## Open questions for PM

1. **Bisect frame disposition**: PM ranked #1122 "as important as M2 pieces" partly on the premise this is a recovered-regression bug. If the architectural diagnosis above is correct (no regression — gap introduced by structured-dispatch decomposition), does that change the priority calculus? Or does the user-facing "Piper feels robotic" framing carry priority regardless?
2. **Scope at fix-time**: Solve only for `update_document` (option A or narrow B), or do the wider work for all slot-filled actions now (option B fully) and post-MVP for the general classifier-stage primitive (option C)?
3. **AAXT coverage**: Should we add a new AAXT scenario specifically targeting structured-dispatch antecedent resolution (Turn 1: "Update doc X", Turn 2: "Add Y to that doc"), with an assertion that the response does NOT contain "I need to know which document"? This would catch the regression class even if the LLM judge is loose.
4. **`entity_references` dead-field**: The `ConversationTurn.entity_references` field has been "stored, not yet consumed" since the audit #827 noted it. Should #1122 fix include actually populating + consuming it, or do we leave that for the entity-resolution primitive in option C?
5. **PM's July 2025 memory**: Confirming the bisect finding — to PM's recollection, was the July 2025 working flow specifically a "structured doc-UPDATE handler honored 'the doc'" path, or was it more conversational ("ask Piper about a doc, then ask follow-up questions that resolved 'the doc'"). The latter still works today via the QUERY path; the former is the new capability we're being asked to build.

---

**Word count**: ~1450
**File**: `/Users/xian/Development/piper-morgan/piper-morgan-product/dev/active/1122-investigation-2026-05-27.md`
