# #1122 Q5 Forensic Research — Did the July-2025 codebase support antecedent-resolution for document UPDATE?

**Author**: General-purpose Code agent (forensic subagent)
**Date**: 2026-05-27
**Question**: In July 2025, could Piper handle "the doc" / "that doc" antecedent resolution in a 2-turn flow specifically for document **UPDATE** operations, or only for QUERY / CONVERSATIONAL flows?
**Method**: git archaeology against tip-of-July-2025 (`1144a7fe4`, Jul 30 2025), GitHub issues, session-log presence.

---

## TL;DR

**Confidence: HIGH.** The 2-turn document-UPDATE antecedent flow PM remembers **did not exist in July 2025** — and could not have existed, because none of its prerequisites existed:

1. **No Notion integration in July 2025.** First Notion file appears 2025-08-26, and even that was *publish-ADRs-TO-Notion*, not update-arbitrary-Notion-pages. Real Notion write-back (`#1080 NOTION-WRITE` / `append_blocks`) didn't land until **2026-05-18**. The literal scenario PM cited ("update the Piper Morgan test page doc on Notion") was technically impossible in July 2025.
2. **No `update_document` workflow registered in July 2025.** `services/orchestration/workflow_factory.py` `_register_default_workflows()` at `1144a7fe4` registers create / analyze / list actions but **no update-document action**. `WorkflowType.UPDATE_WORK_ITEM` and `GENERATE_DOCUMENT` exist as enum values (added by PM-062 ~July 23 2025) but with no handler implementation and no intent-action mapping.
3. **No multi-turn antecedent resolution for any path until Oct 23 2025.** The conversation-context tracker that resolves "that issue" / "the file" / "that doc" was issue **#266 / #248 CORE-UX-CONVERSATION-CONTEXT**, closed 2025-10-23.
4. What *did* work in July 2025 was filename-based file lookup (regex matches `the doc` / `that doc` patterns and searches the uploaded-files repository by recency), and this happened **only for QUERY/ANALYSIS intents** that routed through the `IntentEnricher.enrich_with_file_context()` path. It was not antecedent resolution in any pragmatic sense — it was "find the most-recently-uploaded file in this session."

**Most likely interpretation of PM's recall**: PM is remembering either (a) the late-Oct 2025 conversation-context-tracker work surfacing "that file" / "that doc" resolution for QUERY flows, mis-dated to July; or (b) the uploaded-file-resolution flow ("summarize the doc I uploaded"), which did work in July 2025 for QUERY only — mis-recalled as having worked for UPDATE.

---

## Evidence: structured-dispatch UPDATE path in July 2025

**State of `services/intent_service/` at `1144a7fe4` (Jul 30 2025)**:
- `__init__.py`, `classifier.py`, `classifier.py.backup`, `exceptions.py`, `fuzzy_matcher.py`, `intent_enricher.py`, `pre_classifier.py`, `prompts.py`, `spatial_intent_classifier.py`
- **Missing**: `conversation_context.py` (created 2026-01-25, commit `bbb741cdb`), `conversational_floor.py`, `document_handlers.py`, `slot_filling/`. None of these existed.

**Workflow registry** (`services/orchestration/workflow_factory.py:30-62` at `1144a7fe4`) maps:
- `create_github_issue`, `create_ticket`, `create_issue` → `CREATE_TICKET`
- `analyze_data`, `analyze_file` → `ANALYZE_FILE`
- `generate_report`, `performance_analysis`, `user_feedback_analysis`, `system_analysis` → `GENERATE_REPORT`
- `list_projects`, `list_all_projects`, `show_projects` → `LIST_PROJECTS`
- `create_feature`, `analyze_metrics`, `create_task`, `plan_strategy`, `learn_pattern`, `analyze_feedback`, `confirm_project`, `select_project` → respective types

**There is no `update_document`, `update_doc`, `edit_document`, `modify_document`, or `add_paragraph_to_doc` mapping.** A 2-turn flow whose Turn 1 set up a document for UPDATE could not have reached a workflow at all — the intent would have classified into EXECUTION but then `workflow_registry.get(intent.action.lower())` would return `None` and the response would have been the generic "I understand you want to {human_action}" template (`main.py:391-405`).

**No Notion integration**:
- First commit mentioning Notion in any way: `8f07ad5e7` (2025-08-29, "Implement ADR database publishing to Notion") — and this was a CLI-tool for publishing markdown ADRs *to* Notion, not a user-driven document-update path.
- `services/integrations/notion/` directory does not exist in the July 2025 tree.
- The first time a user could conceivably have asked Piper to "update the Piper Morgan test page on Notion" was 2026-05-18 (commit `433a4a0b6`, "feat(#1080): real Notion append_blocks + handler honesty").

**Conclusion**: The structured-dispatch UPDATE-document path PM described is forensically impossible in July 2025.

---

## Evidence: QUERY / conversational path in July 2025

The QUERY path *did* have file-reference resolution that responded to "the doc" / "that doc" — but it was **filename recency lookup**, not pronoun antecedent resolution across turns.

**Mechanism** (all in `1144a7fe4`):

1. **`PreClassifier.detect_file_reference()`** (`services/intent_service/pre_classifier.py:42-78`) — regex patterns including literal `r"\b(the doc|that doc|my doc|this doc)\b"`. Returns a boolean.
2. **`IntentEnricher.enrich_with_file_context()`** (`services/intent_service/intent_enricher.py`) — when classifier sees a QUERY/ANALYSIS intent containing such a reference, the enricher queries `file_repository.search_files_by_name_all_sessions()` (with a session-first fallback) for an uploaded file matching the implied criteria.
3. **`FileResolver.resolve_file_reference()`** (`services/file_context/file_resolver.py:60-90`) — combines temporal-reference patterns ("the file I uploaded yesterday", "the doc from earlier") with intent-action-to-mimetype preference maps. Returns `(file_id, confidence)`.
4. **`SessionManager.get_recent_files()`** (`services/session/session_manager.py:83`) — returns the in-memory list of files uploaded *in this session* (TTL 30min).

**What this could do in July 2025**:
- "summarize the doc I uploaded" → finds the most-recent uploaded file in the session → routes to QUERY → `FileQueryService.summarize_file()` returns metadata + placeholder summary.
- "analyze that doc" → routes to ANALYSIS → `ANALYZE_FILE` workflow.
- Multi-turn ONLY in the sense that uploaded-file metadata persisted in the `ConversationSession`. The classifier itself takes no `conversation_history` parameter (still doesn't — confirmed independently in prior investigation).

**What this could NOT do in July 2025**:
- Resolve "the doc" to a previously-mentioned Notion page (no Notion).
- Resolve "the doc" to anything other than a session-uploaded file.
- Carry the "doc that I just told you about in Turn 1" forward across an UPDATE workflow's slot-filling — slot-filling infrastructure did not exist; UPDATE workflow did not exist.

**Disambiguation flow** (`main.py:192-200, 437-510`): if multiple files matched, the system would ask "which file did you mean? (1) foo.pdf (2) bar.csv" and the user replied with a number. This *did* preserve state across turns via `session.set_clarification()` — but the state was ambiguous-file-list, not "the document the user just specified for an UPDATE".

---

## Most likely interpretation of PM's recall (with hedges)

Three candidate explanations, ranked by likelihood:

**1. PM is conflating the October 2025 conversation-context-tracker work with July.** Issue #266 (CORE-UX-CONVERSATION-CONTEXT, closed 2025-10-23 by Cursor as Chief Architect) explicitly delivered "that issue → resolves to issue #123" and "that file → resolves to auth.py" antecedent resolution, with **acceptance criteria included** demonstrating the exact pattern PM is recalling. The closure write-up reads: *"Users can have natural, flowing conversations without repeating context."* — language very similar to what PM described as working in July. The mis-dating by ~3 months is plausible given the volume of work in 2025.

**2. PM is remembering the QUERY-flow file-reference resolution and projecting it onto UPDATE.** In July 2025 a user *could* upload a file then say "summarize the doc" and get a (partial) result. PM may be recalling this as a generalized "the doc worked" experience, when in fact it was QUERY-only and never extended to UPDATE.

**3. PM is remembering a demo or test session that used a hand-wired path.** Less likely — would require commit evidence that doesn't exist.

**Hedges**:
- I cannot rule out that PM is remembering a **subjective experience** of Piper handling "the doc" reference in conversation, where the underlying mechanism was the QUERY path and the surface behavior felt like UPDATE worked. The conversational nuance is hard to forensically reconstruct from commit history.
- Dev session logs do not exist for July 2025 (`dev/2025/08/15/` is the earliest dated directory; the convention started later). No contemporaneous log can corroborate or refute what PM observed in a live test.

---

## What we can't determine from forensics alone

1. **Whether PM ever ran a live 2-turn UPDATE test in July 2025.** No session-log evidence either way. The codebase makes the scenario PM described impossible, but I cannot prove PM didn't *think* it worked at the time.
2. **Whether any branch or local-only experimental code in July 2025 had a different shape.** I checked `--all` branches; nothing UPDATE-flavored. But ephemeral local experiments leave no trace.
3. **Whether the "scratch" of antecedent resolution that DID work in July (filename recency for QUERY) sometimes surfaced UPDATE-like behavior** — e.g., if the EXECUTION workflow path silently fell through to a default response that mentioned the resolved filename, PM may have read that as "Piper understood which doc". Without runtime logs from July 2025, this is unfalsifiable.
4. **Whether PM is partially remembering a closely-related capability** — e.g., file-disambiguation prompts ("Which file did you mean?") preserving across turns. This *did* exist in July 2025 but is a different mechanism from antecedent resolution.

---

## Commit citations (selected)

- `1144a7fe4` (2025-07-30) — tip of main at end of July 2025; used as canonical July state
- `bbb741cdb` (2026-01-25) — `feat(#427): Add conversation context for follow-up detection` (first `conversation_context.py`)
- `8f07ad5e7` (2025-08-29) — first Notion-related commit (ADR publishing, not user-facing UPDATE)
- `433a4a0b6` (2026-05-18) — `feat(#1080): real Notion append_blocks` — first real Notion-document UPDATE capability
- Issue #266 (closed 2025-10-23) — first delivery of "that issue / that file" antecedent resolution
- Issue #248 — sibling/dependency of #266; same closure event
- Issue #740 (2026-01-31) — entity-extraction regex bug in the #266 work, confirming the antecedent-tracker is the relevant infrastructure
