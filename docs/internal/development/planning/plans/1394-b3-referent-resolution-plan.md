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

## Open questions for Arch

1. **OQ-2 (ADR-078) — detection mechanism**: deterministic patterns (regex on verb+referent, cheap, matches the pre_classifier's deterministic character) vs a small LLM resolution call. **My lean: deterministic** — it keeps surface-1 deterministic/inspectable (the HOST trust-lens "legible intermediate state" argument), and the conservative bar is easier to reason about in patterns than in an LLM's judgment. LLM-resolution reintroduces exactly the non-determinism D4 pushed out. Want your ruling.
2. **Rewrite form**: message-string rewrite (reuses `_slotfill_issue_request`, one path) vs `intent.context` annotation (cleaner but the classifier prompt won't see it). My lean: **message rewrite** — it makes the resolved referent visible to every downstream surface uniformly, and it's the most testable ("in→out" string transform).

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
