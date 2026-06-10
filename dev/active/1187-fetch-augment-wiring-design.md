# #1187 SUMMARIZE-FETCH-AUGMENTATION — wiring design (for the tandem session)

**Status (updated 2026-06-10, post-tandem):** Mechanism COMPLETE + unit-tested (fetch core + floor-injection wiring + **Gap-1 issue-number extraction**). **BLOCKED for end-to-end UAT on #1192** (integrations last-mile). #1187 the issue stays OPEN — PM directive: "wait till we can test it without hacks." Lead Dev.

## Tandem outcome (2026-06-10)

Live UAT of `summarize github issue #1124` fell to the floor. Root cause was NOT the floor-injection wiring — it was two upstream gaps the mocked unit tests hid:

1. **Gap 1 (FIXED this commit):** the classifier tags `source_type=github_issue` but never slots the issue number. `_fetch_issue_content` rewritten to the proven live `github_router` path (Issue #1042): parse `#N` from the raw message → init router → `is_configured` gate → `get_issue(n)` with the router resolving the repo internally. 8 new tests mock the *router* (not the helper) so the real extraction is exercised. 43 pass (only pre-existing #1188 fails).

2. **Gap 2 (→ #1192, NOT #1187):** there is no product-native way to connect GitHub + designate a repo. Repo resolution's only currently-functional path is the `PIPER_DEFAULT_REPO` dev env-hatch (process-wide — wrong by design). The native paths (user `default_repo`, project↔repo link) exist in backend but the user-facing last mile is broken/missing: no API to SET default_repo (#869), project never threaded onto chat requests, GitHub-connect UI fails with a working PAT (#541). Filed as **#1192** (M3).

**#1187 resumes** when #1192 lands a real repo-resolution path; then: restart server, UAT a real `summarize issue #N`, tune `_format_domain_context` summary wording on real output, merge + close. The mechanism is **inert until then** (fetch returns None → floor degrades exactly as today).

---
**Original (pre-tandem) notes below:**

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
