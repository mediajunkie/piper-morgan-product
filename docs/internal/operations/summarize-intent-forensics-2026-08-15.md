# Summarize-Intent Forensics — what got lost, unwired, or regressed (2026-08-15)

**Commissioned by**: PM (xian), 2026-08-15, verbatim: *"summarizing was one of the very first
intents we supported with Piper. This requires forensic research and not rhetorical questions.
What got lost, unwired, or regressed that this is even a question, more than a year later in
the build?"*
**Context**: Inversion Phase-1 shadow score (`docs/internal/architecture/current/inversion-phase1-shadow-score-2026-08-14b.md`)
routes "summarize the document" to CLARIFY because the 62-operation registry-derived grammar has
no summarize operation; the corpus row expects `category:SYNTHESIS`.
**Method**: git archaeology (`-S` pickaxe over `services/`), live measurement (pre-classifier +
grammar derivation + registry disposition run in-process, env-stripped, POSTGRES_PORT=5433),
and end-to-end code trace of the current chat path. Every sha below verified `commit` via
`git cat-file -t`. Read-only investigation; this report is the only artifact.

---

## Headline finding

**PM's memory is exact — and the capability was never lost in one place. It was never fully
wired in the first place, and the pieces that DID work were split across four surfaces that
each subsequently went dark, moved, or were deliberately re-routed.** Specifically:

1. **Summarize-as-intent existed from the literal first commit** (2025-06-01) as the SYNTHESIS
   category's defining example — but for the first five months the chat path answered it with
   **acknowledgment theater** ("I'll help you create that."), never an actual summary.
2. **Real document-summarize code shipped twice and both times missed the chat path**: the
   #290 handlers (Nov 2025) were wired to REST only — their chat dispatch existed *only in a
   guidance doc* — and the file-reference resolver (June 2025) lost its only live caller when
   `main.py` was gutted (Oct 2025) and was never re-wired into the web chat path.
3. **What summarize became on the live path is a deliberate June-2026 product ruling**
   (SUMMARIZE-TAXONOMY #1158, PPM 2026-06-08): summaries are ALWAYS floor-rendered; the floor
   gets fetch-augmentation for sources it can't reach. GitHub-issue summarize genuinely works
   end-to-end since 2026-06-11. **The `document` branch of that same design was explicitly
   deferred in #1187, #1187 was closed with the deferral inside it, and no successor issue
   tracks it.**
4. **A quiet August-2026 regression narrowed even the *taxonomy***: the #1432 orphan-delete +
   Phase-4 re-land restored the classifier's verb prompt from a pre-#1158 snapshot, silently
   dropping `document` (and `conversation`) from the `source_type` vocabulary the live
   classifier is taught.
5. **The Inversion grammar is honest about all of this**: it derives from rail + ACTION_REGISTRY,
   and summarize has **zero rows in either** (measured: `[]`) — floor-routing was implemented as
   *absence* (unknown → FLOOR default), and absence is invisible to a registry-derived grammar.
   The router therefore cannot name a summarize operation; CLARIFY is what a catalog-hole looks
   like from the router's seat.

So the answer to "what got lost?": **not one thing — a capability that was always
75%-complete had its remaining 25% deferred (by ruling), stranded (by refactor), and
narrowed (by re-land), while the one slice that was finished (GitHub issues) works today.**

---

## Timeline — every state change, sha + date

| Date | Sha | Event | State of "summarize the document" after |
|---|---|---|---|
| 2025-06-01 | `41a553bd0` | Initial bootstrap. `IntentCategory.SYNTHESIS = "synthesis"  # Generate docs, summarize` — summarize is in the day-1 enum comment. | Category exists; no handler. |
| 2025-06-03 | `1616f95d2` | First classifier. LLM prompt: "SYNTHESIS: Generating documents, summaries, or reports"; keyword fallback `"summarize" → SYNTHESIS/generate_content`. | Classifies correctly; downstream is scaffold. |
| 2025-06-04 | `7e39fd09e` | Document upload + knowledge domains added. | Docs can be uploaded; summarize-of-them not wired. |
| 2025-06-06 | `a03bcc9aa` | First comprehensive docs. Claims: "**ANALYZE_DOCUMENT**: Document analysis and summarization", backlog story PM-012 "upload documents and get analysis and summaries automatically", example utterance "Review the requirements document and summarize key points". **The claim history PM remembers is real and this early.** | Documented as a capability; engine's `TaskType.CREATE_SUMMARY` is `_placeholder_handler` (verified at `f062aaf61:services/orchestration/engine.py:53`). |
| 2025-06-23 | `f062aaf61` | File-resolution system (PM-011): `FileResolver` + `IntentEnricher` wired into `main.py`'s chat handler — resolves "the document" → `file_id`, with disambiguation UX. | Best-ever state of the *reference-resolution* half. But SYNTHESIS execution is still `"I'll help you create that."` (`f062aaf61:main.py:319`) — acknowledgment, not a summary. |
| **2025-10-01** | **`aad66d9d1`** | **BREAK 1.** Commit labeled `docs: Complete CORE-GREAT-2D documentation suite` guts `main.py` 1184→109 lines — deletes the entire inline chat handler **including the only live `IntentEnricher` call**. Chat moves to the `web/app.py` + `IntentService` path, which never had file enrichment. | "The document" can no longer be resolved to an uploaded file on the chat path. Never re-wired since (verified: zero non-test callers of `IntentEnricher`/`enrich_with_file_context` today). |
| 2025-10-11 | `45c3a3b03` | GAP-1: all 10 category handlers incl. SYNTHESIS in `IntentService`. | SYNTHESIS routes to a real handler; summarize-of-document still has no content path. |
| **2025-11-01** | **`2452ba9ae`** | **BREAK 2 (shipped dark, #1522 family).** #290 ships all 6 document workflows incl. `handle_summarize_document` (real `DocumentAnalyzer` call) + REST `POST /api/v1/documents/{file_id}/summarize` + classifier normalization `"summarize" → "summarize_document"` + `IntentType.SUMMARIZE_DOCUMENT`. **The chat dispatch (`elif intent_type == "summarize_document"`) exists ONLY in `dev/active/code-architectural-guidance-290.md` inside this commit — it was never implemented in `intent_service.py`** (pickaxe: no revision of `services/intent/intent_service.py` ever contained the string). | A working summarizer exists — reachable only by raw REST with a `file_id` the chat can't supply. Chat path: classifier emits `summarize_document`, nothing consumes it, falls through. |
| 2025-11-03/05 | `8fc3a65ea` / `3193c9949` | ActionMapper adds then removes (#294, EXECUTION-only cleanup) the `"summarize" → "summarize"` mappings. Removal was correct — nothing consumed them. | Unchanged. |
| 2025-11-22 | `c33e4cfd9` | #308 injects `IntentEnricher` into `OrchestrationEngine` — the orchestration island, which archaeology later confirms was never the live chat path. | Enricher "wired" — into dead code. |
| 2026-05-15 | `92617bab1` | #1094 deletes `OrchestrationEngine` → enricher fully orphaned (no callers at all). | Unchanged for users; the orphan is now visible. |
| 2026-06-06→08 | `e7fd12ee0`, `3c65c7017`, `fba6452f0` | #1124 Phase 2/4: canonical `Verb.SUMMARIZE` + verb→legacy-action shim; classifier prompt flip (on `llm_classifier.py` — later found to be the orphan, #1432). Flip prompt's source_type vocab: `github_issue, commit_range, text` (3-set). | Transitional. |
| **2026-06-08/09** | **`30c27dcb7`** | **THE DELIBERATE RE-ROUTE (not a break).** #1158 SUMMARIZE-TAXONOMY, PPM product ruling 2026-06-08: a summary's output is ALWAYS conversational (floor-rendered); `(SUMMARIZE, *)` deliberately unmapped in the shim → summaries floor by default. Widens source_type vocab to the PPM 5-set `{text, conversation, github_issue, commit_range, document}` — **on `llm_classifier.py`, the file later deleted as an orphan.** Canonical fixtures assert floor for summaries (`tests/e2e/test_canonical_conversations.py:120,139` — rows 38, 47). | Summaries route to the floor by design. Floor has no source content yet. |
| 2026-06-09 | `2d8ccc5ac` | #1124 deletes the dead `summarize`/`create_summary` SYNTHESIS elif; `_handle_summarize` retained DORMANT as fetch-helper seed (its docstring: "'document' retrieval is part of the deferred fetch-augmentation work" — `services/intent/intent_service.py:10499-10521`). | Unchanged; the old structured renderer is now formally off-path. |
| **2026-06-10/11** | **`b6519a200`, `22715910b`, `062cb59d4`** | #1187 fetch-augmentation: `_fetch_summary_source_content` + floor `summary_source` injection (`conversational_floor.py:746`). **"summarize-issue now works end-to-end"** — the first time chat summarize of an unreachable source ACTUALLY works. **The `document` branch is written as an explicit no-op**: "document → deferred (Notion/uploaded-file retrieval); not yet wired" (`services/intent/intent_service.py:10694-10695`). #1187 CLOSED 2026-06-12 with the deferral inside; **no successor issue exists** (GH search verified 2026-08-15). | GitHub-issue + commit-range summarize: WORKS. Document summarize: deferred, untracked. |
| **2026-08-02** | **`5fba0f1be` + `7e866d87b`** | **BREAK 3 (the quiet regression).** #1432 deletes the orphan `llm_classifier.py` — which was the ONLY file carrying the #1158 5-set vocab — and re-lands the Phase-4 flip on live `classifier.py` **from the pre-#1158 reference impl (`fba6452f0`)**. The live prompt's source_type vocab is now the 3-set: `"github_issue, commit_range, text"` (`services/intent_service/prompts.py:222`). `document` and `conversation` silently dropped; `_handle_summarize`'s docstring still claims the 5-set (now stale). | The live classifier is no longer even *taught* that `source_type=document` exists. |
| 2026-08-14 | `dc9f20d03` | #1595 Inversion Phase 1: grammar derived from rail + ACTION_REGISTRY. Measured live 2026-08-15: **62 operations, zero containing "summar"**; ACTION_REGISTRY has **zero summarize rows**; `get_disposition("synthesis", "summarize")` → FLOOR only via the *unknown-action default*. | Router-layer: "summarize the document" → CLARIFY @0.4 (both runs). Production chain unchanged (classifies SYNTHESIS, floors without content). |

---

## Current live behavior, layer by layer (m-43: each line names what was measured/read)

Utterance: **"summarize the document"** (user has uploaded a file this session).

| # | Layer | What happens | Evidence type |
|---|---|---|---|
| 1 | Pre-classifier (`pre_classifier.py`) | **Declines** (returns None) — for this and "analyze the file I uploaded", "summarize github issue #1124", "summarize this". | **Measured** in-process 2026-08-15. |
| 2 | LLM classifier (`classifier.py`) | Emits SYNTHESIS. The phrase is literally a few-shot example in the live prompt: `"summarize the document" → {"category": "synthesis", "action": "generate_summary"}` (`prompts.py:254`) — **the corpus row is the prompt's own teaching example**, which is why Phase-0 full-chain MATCHed it. source_type vocab offered to the model: `github_issue, commit_range, text` — `document` absent (`prompts.py:222`). File context = filenames only (`classifier.py:513`), no file_id slot in the emitted JSON. | Code trace (prompt text + parse path `classifier.py:1147-1182`). |
| 3 | Verb shim (`action_registry.py:529-538`) | `(SUMMARIZE, *)` deliberately unmapped → action keeps free form (`generate_summary`). The `"summarize"→"summarize_document"` normalization at `classifier.py:552` fires only on the exact action `summarize` — and `summarize_document` has no consumer anywhere on the chat path anyway. | Code trace. |
| 4 | Action rail (`workflow_entries.py`) | No summarize key (rail keys enumerated; `analyze_document`/`analyze_file` exist but are the **Notion** analyze handler, `workflow_entries.py:1311-1322`). Falls through to category routing. | Code read + grammar derivation (rail is grammar source 1). |
| 5 | SYNTHESIS category handler (`intent_service.py:9173`) | `_handle_synthesis_intent` → `_fetch_summary_source_content` → `source_type` is None/`text` (never `document`, per layer 2) — and even if it were `document`: **"document → deferred … not yet wired; return None"** (`intent_service.py:10693-10696`). Returns None → floor with **no** `summary_source`. | Code trace. |
| 6 | Conversational floor (`conversational_floor.py:746`) | `summary_source` injection exists and works (proven for GitHub issues) but receives nothing here. The context assembler has **no document/uploaded-file gatherer** (all `_gather_*` methods enumerated: identity, memory, temporal, calendar, todos, projects, GitHub… no files). Floor answers from conversation only — honest degrade if the content isn't already in the transcript. | Code read (assembler method census). |
| 7 | REST surface (NOT chat) | `POST /api/v1/documents/{file_id}/summarize` → `handle_summarize_document` → `DocumentAnalyzer` — **live and mounted** (`web/app.py:261`, `web/api/routes/documents.py:171-198`). Requires a `file_id` the chat path cannot supply. | Code read (router mount + handler). |
| 8 | Inversion router (shadow) | Grammar = rail + registry = **62 ops, no summarize** (measured). Router's only honest vocabulary for this row: an operation name, NONE, or CLARIFY. It says CLARIFY @0.4. Under the #1158 design the *production-equivalent* answer would arguably be NONE (floor). The corpus expectation `category:SYNTHESIS` is a Phase-0 full-chain shape the router layer cannot express at all. | Measured (grammar derivation) + shadow-score doc. |

**Adjacent family status** (task item 4):
- **"analyze the file I uploaded"** — same shape: pre-classifier declines (measured); corpus expects `analyze_data`; the rail's `analyze_document` is the **Notion** document analyzer, not uploads; the upload-analyze handler (`handle_analyze_document`, #290) is REST-only. Shadow: CLARIFY (Family-4 honest abstention, context-free run).
- **Notion document family** — wired on the rail: `search_documents`/`find_documents`/`search_notion`, `analyze_document`/`analyze_file` (READ), `update_document`/`edit_document`/`update_document_query` (WRITE, effect-classed) (`workflow_entries.py:1059-1061, 1193-1199, 1311-1322`). These appear in the 62-op grammar. Wired, not dark.
- **Uploaded-file family** (#290 handlers + `FileResolver`/`IntentEnricher`) — code alive, tests exist, REST mounted; **chat-unreachable since 2025-10-01**; enricher orphaned since `92617bab1` (2026-05-15) at the latest, stranded since `aad66d9d1` in practice.
- **Vestiges confirming the intended UX**: `ui_messages/templates.py:33` `("synthesis", "summarize_document"): "Here's my summary of {filename}:"` and `personality_bridge.py:42` — templates for a chat flow that never fired.

---

## The precise break points (ranked by causal weight)

1. **#290's chat dispatch was never implemented** (`2452ba9ae`, 2025-11-01). The
   handlers/REST/enum/normalization all shipped; the dispatch block lived only in the
   guidance doc committed alongside. #1522 shipping-dark family, textbook. This is the single
   biggest reason "summarize the document" never worked in chat.
2. **`aad66d9d1` (2025-10-01) stranded the file-reference resolver.** A 1075-line deletion of
   `main.py`'s chat handler under a `docs:` commit label removed the only live
   `IntentEnricher` call; the successor chat path (`web/app.py` → `IntentService`) never got
   one. Without it, no chat turn can bind "the document" to a `file_id`, so even a wired
   handler would have nothing to act on.
3. **#1187 closed with its `document` branch deferred and untracked** (2026-06-12). The
   design (PPM's fetch-augment-then-floor) explicitly includes document retrieval; only
   `github_issue` + `commit_range` were built. Closing the issue buried the deferral — this is
   the deferred-work-without-a-tracking-issue antipattern, found live.
4. **The 08-02 re-land regressed the taxonomy** (`5fba0f1be` + `7e866d87b`). Deleting the
   orphan classifier deleted the only implementation of #1158's 5-set source_type vocabulary;
   the re-land used the pre-#1158 snapshot (`fba6452f0`) as reference, so the live classifier
   today is not told `document` (or `conversation`) is a valid source_type. Nobody chose to
   drop it; it fell out of a correct deletion done from a stale reference point.
5. **Floor-by-absence is invisible to the Inversion grammar** (`dc9f20d03`, 2026-08-14).
   #1158 implemented "summaries floor" as *the absence of any registry row* (unknown →
   FLOOR default, measured). A grammar derived from "what is registered" structurally cannot
   see a capability that exists only as an unregistered default. Not a bug in the derivation —
   a representational gap in the registry itself.

---

## What still EXISTS (rewireable) vs what is genuinely GONE

**Exists, live, working today**
- Chat summarize of GitHub issues + commit ranges (#1187/#1192a, since 2026-06-11): fetch → floor `summary_source` injection → real summary.
- Chat summarize of text already in the conversation (floor-direct, by construction).
- REST document summarize: `POST /api/v1/documents/{file_id}/summarize` (mounted, `web/app.py:261`).
- `SYNTHESIS` category, `Verb.SUMMARIZE`, the classifier's correct SYNTHESIS classification of the phrase.

**Exists, dark, rewireable (no rebuild needed)**
- `handle_summarize_document` + `DocumentAnalyzer` (real summarizer, #290, integration-tested).
- `FileResolver` (`services/file_context/file_resolver.py`) + `IntentEnricher`
  (`services/intent_service/intent_enricher.py`) — reference resolution + disambiguation UX, orphaned but intact.
- `_fetch_summary_source_content`'s dispatcher shape — the `document` branch is a marked TODO slot, not missing architecture.
- Floor `summary_source` injection — source-agnostic, proven with GitHub issues.
- `_handle_summarize` (dormant) — kept deliberately as the fetch-helper seed.

**Genuinely gone (git-history only)**
- The #1158 5-set source_type prompt vocabulary (lived only in deleted `llm_classifier.py`; recoverable at `30c27dcb7`).
- `main.py`'s enricher-wired chat handler (recoverable at `f062aaf61`, but the architecture has moved on).
- Nothing else. **No summarize capability was ever deleted; every deletion in this history (`2d8ccc5ac`, `92617bab1`, `5fba0f1be`) removed dead or orphaned code, correctly.**

---

## Repair options (options, not a decision — PM decides)

**Option A — Corpus honesty (hours).** Re-express the Phase-0 row for the router layer:
under the ratified #1158 design, the production-equivalent router answer for "summarize the
document" is NONE (floor), not `category:SYNTHESIS` (a full-chain shape the router can't emit).
Same for "analyze the file I uploaded" (Family-4/Phase-2 context question). The shadow-score
doc itself flags this as "a Phase-0 corpus question, recorded rather than tuned around."
Honest, cheap, changes nothing user-facing: document summarize remains absent from chat.

**Option B — Represent the floor route in the registry (hours→1 day).** Add explicit
ACTION_REGISTRY rows (e.g. `("synthesis", "summarize")` → FLOOR, with description + example
per the #1595 Family-1 enrichment pattern). The grammar derivation picks them up automatically
(registry-only canonicals are source 2), the router gains a `summarize` operation, and the
CLARIFY hole closes without touching production routing (registry rows with FLOOR disposition
don't change dispatch — dispositions already default there). Converts floor-by-absence into
floor-by-declaration, which is also what the Inversion Phase-2 executor will need anyway.
Guard: `validate_verb_coverage` + the routing-vocabulary lint already enforce the metadata.

**Option C — Finish the deferred #1187 document branch (1–3 days).** The actual user-facing
repair; makes "summarize the document" work in chat for uploaded files — for the first time
ever, per this archaeology. Concretely: (1) restore `document` (+`conversation`) to the live
prompt's source_type vocabulary (`prompts.py:222`, one line + table-driven tests — undoes
Break 4); (2) implement the `document` branch of `_fetch_summary_source_content` using
`FileResolver` (resolve "the document" → file_id, reusing the orphaned enricher logic) +
`DocumentService.get_document` for content (both alive); (3) thread session_id/user_id
(already available at the synthesis handler seam); (4) floor injection is already done.
Risks: user-isolation on file access (the #290 handlers already enforce it — reuse, don't
re-implement); disambiguation UX for multiple uploads (the June-2025 enricher had this;
decide whether v1 just takes most-recent). Pairs naturally with B.

**Option D — Also chat-wire the uploaded-file *analyze* sibling (add ~1 day to C).** Same
mechanism, same orphaned pieces, fixes "analyze the file I uploaded" (the other shadow-score
CLARIFY). Could be a follow-on issue rather than scope creep on C.

A and B are compatible and cheap; C is the one PM's question is really about; D is the same
repair applied to the sibling. Recommended framing for PPM: #1158's ruling ("output always
floor, sources branch") is sound and none of these options reverse it — C/D complete it.

## Discovered work (per Discovered Work Discipline — reported to Lead, no issues filed from this read-only session)

1. **#1187's deferred `document` branch has no tracking issue** (deferral is buried in a closed
   issue + a code comment). Needs an issue whichever option PM picks.
2. **Stale docstring**: `_handle_summarize` (`intent_service.py:10514-10521`) claims the
   classifier's source_type vocabulary is the 5-set; the live prompt teaches the 3-set.
3. **`IntentEnricher` + `FileResolver` are orphaned live code** (zero non-test callers) — either
   Option C consumes them or they're #1432-family fix-or-delete candidates.
4. **Dead vestige pair**: `ui_messages/templates.py:33` + `personality_bridge.py:42` reference
   the never-fired `summarize_document` chat action.
5. **`aad66d9d1` precedent**: a 1075-line functional deletion under a `docs:` label is why Break 2
   was hard to find; worth a line in the commit-hygiene guidance.

---
*Forensics by Coding Agent (prog), 2026-08-15, for Lead Dev / PM. All shas verified
`git cat-file -t` = commit. Live measurements: pre-classifier decline (4 phrases), grammar
derivation (62 ops, no summarize), registry disposition (unknown → FLOOR), zero summarize
registry rows.*
