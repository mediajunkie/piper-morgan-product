# B3 Plan — Pre-Classifier Referent Resolution (#1394, ADR-078 D2)

**Author**: Lead Dev · **Date**: 2026-07-15 · **Status**: PLAN (for Arch review → D5 rows)
**Depends on**: B4 (the `session_activity` ledger — DONE + ratified 2026-07-15). **Reads** that ledger.
**Arch constraint folded in**: the over-resolution guard (memo 2026-07-15 12:45) is the load-bearing design driver, not a bolt-on.

---

## The build-lens correction to "surface 1" (the feasibility finding)

ADR-078 D2 says B3 resolves the referent "at the pre-classifier (surface 1)." Taken literally that means `PreClassifier.pre_classify(message)` — but that method is **static, synchronous, and message-only**: no `user_id`, no `session_id`, and sync (can't `await` the owner-scoped ledger read). B3 cannot live there as-is.

**Where it actually belongs**: `IntentClassifier.classify()` (`classifier.py:147`) is **async** and already has `user_id` + `session_id` in scope; it calls `pre_classify(message)` at line 219. B3's resolution is a **new async step in `classify()`, immediately before `pre_classify`**, that rewrites the message, then hands the rewritten message to the existing `pre_classify`.

This still honors ADR-078's intent exactly:
- **Still surface-1 / pre-classification** — it runs before the LLM classifier; it's an explicit upstream transform.
- **D4 held** — the classifier stays stateless; we do NOT inject history into the classification prompt. The referent is resolved and made explicit *before* classification, so the classifier sees `"change the title of issue owner/repo#107"`, not conversation state.
- **Owner-scoped** — `classify()` has the resolved principal, so the ledger read uses B4's `list_for_session(owner_id, conversation_id)` (D1a preserved end-to-end).

("surface 1" was the right altitude; "the sync `pre_classify` function" was the wrong specific home — same shape as B4's D1 substrate correction.)

## The resolution step (design)

`_resolve_referent(message, user_id, session_id) -> str` (async, in `classify()`):

1. **Detect** a follow-up referent — CONSERVATIVE (see guards). Trigger requires BOTH:
   - an **update/modify verb** (`change`, `update`, `rename`, `edit`, `set`, `add … to`, `close`, `reopen`, `label`), AND
   - a **referent with no explicit target**: a definite-article artifact noun (`the title`, `the issue`, `the body`, `the label`) OR a bare pronoun (`it`, `that`) — AND the message carries **no explicit issue number / repo already** (if it does, there's nothing to resolve).
2. **Read the ledger** — `list_for_session(owner_id, session_id)`, newest-first (already the reader's order). Take the most recent creation whose `action_type` plausibly matches the referent (an issue verb → most recent `issue_created`).
3. **Rewrite** — inject the explicit reference so the DOWNSTREAM machinery resolves it with zero new parsing: rewrite to include `issue <owner/repo>#<n>` (or annotate `intent.context` with `repository` + `issue_number`). The existing `_slotfill_issue_request` already extracts `owner/repo#N`, so a message-level rewrite reuses it — no new slot-fill.
4. **Return** the rewritten message (or the original untouched — see guards).

## The two guards (Arch's load-bearing constraint — non-negotiable)

- **N1 — no-referent → no rewrite.** Empty ledger (nothing created this session) → return the message UNCHANGED. B3 must not fabricate a target; downstream honest-degrade ("which issue?") handles it. (The B4 handler already degrades honestly on empty.)
- **N2 — fresh-topic → no hijack.** A new unrelated request that merely contains a definite article after a creation ("the roadmap needs restructuring" following an issue-create) must NOT be rewritten as a follow-up. This is the D4 concern at surface 1: a false hit silently misroutes — the exact class we're KILLING. Mechanisms: (a) require the update-verb+referent co-occurrence (step 1), not just a definite article; (b) require the referent noun to plausibly match the last creation's artifact type; (c) **conservative-when-uncertain — resolve only a high-confidence referent, else leave untouched.** A miss (real follow-up left unresolved) is recoverable via honest-degrade; a false hit is not.

## turn_id (deferred from B4, lands here)

B4 left `session_activity.turn_id` null. B3 doesn't strictly need it (it resolves "latest" via `created_at` order), but B3 is the natural time to populate it — requires `save_conversation_turn` to return the persisted turn id so the observer can stamp it. In scope for the B3 build; not a blocker for resolution.

## Capability finding (answers Arch's §4 — a title-update handler DOES exist)

Arch's ratification flagged "no title-update handler → B3 must route to honest-decline, never create_issue (duplicate)." **Build-lens correction, grounded:** the handler exists and works.

- **`_handle_update_issue`** (`intent_service.py:7130`, docstring "FULLY IMPLEMENTED") extracts `title`/`body`/`state`/`labels`/`assignees` (via the same `_slotfill_issue_request`, including the `#1386-B3'` "change the title … to X" to-form), requires ≥1 field, and calls **`github_router.update_issue(title=title, …)`** — which forwards `title` (`github_integration_router.py:367`), a real title change. Tested (`test_execution_analysis_handlers.py`, `test_action_mapper.py`).
- **Dispatch**: the elif chain `intent_service.py:6515` (`mapped_action in ["update_issue","update_ticket"] → _handle_update_issue`), with `action_mapper` aliasing `modify_issue`/`update_github_issue`/`update_ticket` → `update_issue`. This is **surface-4 (elif) dispatch, not the rail** — which is why a rail-based grounding misses it (the "fourth vocabulary" the routing-stack doc warns about).
- **So both cases land honestly, no new decline handler needed**: "change the title of #107 **to 'Foo'**" → real update; "change the title of #107" (no new value) → the handler's own validation returns "no fields to update / which title?" honest clarification (`:7230`). Neither is Notion; neither is `create_issue`.

**This corrects P1's expected destination**: the update-issue EXECUTION lane (`update_issue`), NOT a REVIEW/decline lane.

**The REAL risk (replaces "no handler")** — reachability: `update_issue` is **NOT in ACTION_REGISTRY, not rail-registered, not prompt-suggested** (elif-only). `pre_classify` returns None for update phrasings → routing depends on the **LLM classifier** emitting `update_issue`/`modify_issue`/etc. So Arch's `create_issue`-duplicate fear is real *as a classification-misfire risk*, not a missing-handler one — the probe must confirm "change the title of issue owner/repo#107" classifies to `update_issue` (not `create_issue`, not floor).

**Design option (closes the mode-4 gap deterministically)**: since B3 *deterministically* detects update-verb + referent + resolves #107, B3 can **emit the intent directly** (`action=update_issue` + context) rather than rewrite-and-hope-the-LLM-routes-right — B3 becomes effectively a pre-classifier rule for resolved update-requests. Fully deterministic on B3's cases (more D4-clean than leaving the resolved message to the LLM), and it removes the create_issue-duplicate risk *by construction* for exactly the cases B3 handles. This is MORE than "pure message rewrite," so it's Arch's call (OQ-3 below).

**Separate hardening (not blocking B3)**: `update_issue` being registry/rail-invisible is a mode-4 fragility for ALL update requests, not just B3's. Worth adding to ACTION_REGISTRY + rail — a small separate fix; will file.

## Open questions for Arch

1. **OQ-2 (ADR-078) — detection mechanism**: deterministic patterns vs a small LLM call. **My lean: deterministic.** *(RULED by Arch 2026-07-15: deterministic.)*
2. **Rewrite form**: message-string rewrite vs `intent.context` annotation. My lean: **message rewrite.** *(RULED by Arch: message-rewrite; preserve raw `Intent.original_message` per #1332 — store both raw + resolved.)*
3. **(NEW, from the capability finding) Pure-rewrite vs deterministic-emit**: given B3 already deterministically knows "this is `update_issue` for #107", should B3 (a) rewrite the message and let the LLM classify (mode-4 reachability risk — could misfire to `create_issue`, the duplicate hazard §4 flagged), or (b) **emit the resolved intent directly** (`action=update_issue` + context), closing that hazard by construction for B3's cases? **My lean: (b)** — the honest completion of "deterministic detection," removes the create_issue-duplicate risk rather than relying on the probe to confirm the LLM behaves. More than a string-rewrite, so your call.

## D5 corpus rows (maps to your P1/P2/N1/N2 preview)

| Row | Utterance (after context) | Expected route | What it proves |
|---|---|---|---|
| **P1** | "change the title" after `issue_created #107` | issue-update (NOT Notion) | the core fix — resolution works |
| **P2** | "add a label to it" after a creation | issue-update | pronoun resolution |
| **N1** | "change the title" with empty ledger | unchanged → honest degrade ("which issue?") | no fabrication |
| **N2** | fresh definite-article topic after a creation | NOT hijacked (routes as its own new intent) | over-resolution guard |

N1/N2 make it safe; P1/P2 make it useful. Send the exact expected-destinations and I'll build the resolution + guards against them TDD, same as B4.

## Test plan (mirrors B4's rigor)

- Unit: `_resolve_referent` in→out string transforms — P1/P2 rewrite correctly; **N1/N2 return the message UNCHANGED** (the guard tests are the load-bearing ones, like D1a was for B4).
- Owner-scoping: resolution reads only the acting principal's ledger (D1a end-to-end) — a second user's creation never resolves another user's "the title".
- Routing: post-rewrite, P1/P2 pre_classify/route to issue-update; N1/N2 route as before. #1283 ratchet stays green.
- D5 behavioral rows (Arch-authored) run in the out-of-CI corpus.
