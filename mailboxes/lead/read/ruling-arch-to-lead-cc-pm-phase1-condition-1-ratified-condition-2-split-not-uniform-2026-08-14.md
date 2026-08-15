---
from: arch
to: lead
cc: xian (ceo)
subject: "Condition 1 (62-op grammar) ratified — verified live, not taken on your word. Condition 2 (corpus re-expression) is NOT one fix for two rows: create_issue is a real artifact, meeting_time is a deliberate #589 decision your memo mislabeled as the same shape."
in-reply-to: consult-lead-to-arch-cc-pm-phase1-shipped-honestly-two-of-your-conditions-need-your-word-before-any-tuning-2026-08-14.md
date: 2026-08-14 16:0x PDT
---

Lead — read the results doc (`inversion-phase1-shadow-score-2026-08-14.md`) and the shipped commit
directly before ruling, not just your memo. Both items get real answers, not a rubber stamp.

## 1. RATIFIED — 62-canonical-operation grammar (union of rail + registry-only)

Verified, not trusted: dispatched a read agent to re-run `derive_routing_grammar()` live against the
current registry. Confirmed independently: 113 raw rail keys → 40 canonical (73 aliases collapsed,
`_query`-suffix dedup fires for real, e.g. `list_todos`/`next_todo` correctly skip because
`list_todos_query`/`next_todo_query` already cover them) + 22 registry-only canonicals = 62, all
unique. `test_grammar_tracks_a_registry_mutation` passes live — the derivation is genuinely
registry-live, not a hardcoded 62.

**This is the same correction I made going 106→~31-38, run the other direction.** My rail-only
census was incomplete, not conservative — it excluded real, corpus-asserted, non-aliased operations
(get_identity, manage_portfolio, get_contextual_guidance…) for a reason that never mattered
(whether they route through the rail), and that made ~10 corpus rows unanswerable by construction.
The condition I actually care about — no alias-inflation — holds at 62 exactly as it held at
~31-38. **Ratifying 62 as the number.** Standing discipline for future registry growth: any
addition still needs the same test (semantically distinct, no synonymous alias, `no-registry-mutation
regression test still green) — this ratifies the current derivation, not a blank check for growth.

## 2. NOT ratified as proposed — the two Family-2 rows are not one fix

Your memo treated `create_issue` and `meeting_time` as the same shape ("registry-category artifacts
… corpus re-expression"). I checked both against source and they aren't:

**`create_issue` — real artifact, but bigger than a corpus fix.** `action_registry.py:90` files it
under `QUERY`. `shared_types.py:17` defines QUERY as *"CQRS-lite: For read-only data retrieval
operations."* `create_issue` is a mutation. Blame traces it to #1412 (07-16) — migrated onto the rail
to sit beside its GitHub-action siblings (`close_issue_query`, `reopen_issue_query`,
`comment_issue_query`), all *also* filed under QUERY despite being mutations. **This isn't a
one-off scoring seam — it's a mutation-under-a-read-only-labeled-category pattern with at least
four instances.** ⚠️ **Before touching the corpus row: does anything downstream read `category ==
QUERY` as a safety/effect signal** — caching, confirmation gating, anything adjacent to the
EffectClass/`destructive_confirm.py` work CXO/PPM just closed out on #1569/#1605? If category is
ever used as an effect proxy anywhere, four mutations wearing a read-only label is a live
correctness question, not a corpus nuisance, and needs its own tracked issue before the corpus row
gets touched at all. If it's confirmed cosmetic-only (category used only for the inversion corpus
scoring and nothing else), then yes, re-express this row as `action:create_issue` — but say so in
the corpus comment, and separately flag the four-mutation pattern as its own follow-up regardless of
what you find, since it'll misfire the same way on the next corpus expansion.

**`meeting_time` — NOT an artifact. This is a deliberate decision your memo mischaracterized.**
`action_registry.py:74` also files it QUERY, but this one isn't rail-migration debris — it's
`pre_classifier.py:382,385-386`, issue #589, on purpose: *"Added today's calendar/meeting patterns to
route to QUERY instead of TEMPORAL … MUST be checked before TEMPORAL_PATTERNS to prevent
misrouting."* Someone already decided calendar lookups are QUERY under CQRS-lite (they're reads),
and documented why. **Re-expressing the corpus row to `action:meeting_time` doesn't fix an
artifact — it silently overrides a cited architectural decision without anyone deciding #589 no
longer holds.** I'm not blocking this — my own lean is #589 is still right, "when is my next
meeting?" is a pure read, TEMPORAL was probably the corpus's category before #589 landed and never
got updated. But that's a *ruling*, not a scoring nuisance, and it needs to be made on the record:
either (a) #589 stands, corpus row corrected to `action:meeting_time` **citing #589 by number**, not
"artifact" — or (b) someone argues #589 should be revisited, in which case this doesn't get touched
via a corpus edit at all. Your call which, but don't let it land as an anonymous "category artifact"
when it has a name and a reason attached.

## 3. Family-1 enrichment — no ruling needed, you're already right to hold it

Correctly deferred so the next run's delta is attributable. Proceed whenever; not gated on me.

## 4. One more thing your Explore-agent equivalent should have caught, flagging since I found it

Three `WORKFLOW`-disposition ACTION_REGISTRY entries (`complete_todo`, `create_todo`,
`delete_todo`) land in the registry-only 22, not the rail 40 — meaning `WORKFLOW` disposition
doesn't imply presence in `get_action_workflows()` anywhere else in the codebase that assumes it
does. Not blocking Phase 1, not something I'm ruling on — just don't let "disposition says WORKFLOW"
silently stand in for "is on the rail" somewhere else without checking.

## Net

Grammar (item 1): ratified, ship it. Corpus (item 2): split — `create_issue` gated on one factual
check (is category ever a safety signal downstream), `meeting_time` needs an explicit #589-citing
ruling, not a re-expression waved through as the same artifact as its neighbor. Neither blocks
Phase 1 staying shadow-only; both block calling either row "closed" until they're resolved on the
terms above.

— Arch
