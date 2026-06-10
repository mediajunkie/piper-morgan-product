# #1187 SUMMARIZE-FETCH-AUGMENTATION — wiring design (for the tandem session)

**Status:** fetch CORE built + tested (this commit); floor-injection wiring is the tandem work (it's output-quality / UAT-sensitive). Lead Dev, 2026-06-10.

## What's done (this commit)

`IntentService._fetch_summary_source_content(intent, workflow_id=None)` — the design-independent fetch dispatcher. For `source_type ∈ {github_issue, commit_range}` it reuses the (dormant) `_fetch_issue_content` / `_fetch_commit_content` helpers and returns `(content, metadata)`; `text` / `conversation` → `None` (floor-direct); `document` → `None` (deferred); fetch failure → `None` (graceful). 7 unit tests (helpers mocked — no LLM/network). No behavior change yet — it isn't called from the dispatch path.

## The remaining wiring (4 touches) — to do in tandem

The trace, confirmed:
- Summaries are category **SYNTHESIS**, which is **not** in `_should_route_to_floor`'s `_FLOOR_ROUTED_CATEGORIES`. So summarize floors via **`_handle_synthesis_intent` → `_handle_unknown_intent`** (NOT `_handle_floor_with_context`).
- `_handle_unknown_intent` builds a `FloorContext` **without** `domain_context` (the field exists; the #911 `_handle_floor_with_context` path populates it).
- `ConversationalFloor.respond()` **does** render `domain_context` into the prompt — but only via `_format_domain_context`, which renders **known keys only** (current_time, …). So an injected "source content" key needs a render branch.

Wiring touches:
1. **Detect + fetch** — in `_handle_synthesis_intent` (cleanest; summarize-specific, localized), before falling to the floor: if it's a summarize request with a fetchable `source_type`, call `_fetch_summary_source_content(intent, workflow_id)`.
2. **Inject** — pass `domain_context={"summary_source": {"content": ..., "meta": ...}}` into the floor (either via a summarize-aware floor call, or thread it through `_handle_unknown_intent`).
3. **Render** — add a `summary_source` branch to `ConversationalFloor._format_domain_context` so the fetched content lands in the LLM prompt ("Source to summarize: …").
4. **Prompt guidance** — ensure the floor knows to *summarize* the injected source (not just mention it); this is the **UAT-sensitive** part — summary quality/length/format needs eyeballing with real GitHub issues.

## Design choice to confirm in tandem

- **Option A (recommended): localize in the SYNTHESIS path.** Keep summarize-fetch logic in `_handle_synthesis_intent`; minimal blast radius; the general floor path is untouched.
- **Option B: add SYNTHESIS to `_FLOOR_ROUTED_CATEGORIES` + a ContextAssembler gatherer.** More "architecturally uniform" (uses the #911 context-assembly path) but changes routing for *all* synthesis intents + is a bigger change.
- **Option C: augment inside `_handle_unknown_intent` (gated on summarize).** Puts summarize-specific logic in the general floor path — least clean.

Recommend **A**. The open tandem questions: (1) confirm A vs B; (2) the floor prompt phrasing for "summarize this source" + length/format defaults; (3) the graceful-degradation copy when fetch returns None (keep today's "I couldn't pull that — want me to try again?"); (4) whether `document` source is in-scope for M3 or stays deferred (needs Notion/uploaded-file retrieval).

## Out of scope (per PPM #1158)
Persistent/exportable/structured summary artifacts. Reopen-trigger = a recurring use-case where the summary must persist/leave the conversation.
