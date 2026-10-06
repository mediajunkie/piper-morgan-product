# Arch's (a): router-extracted targets for complete_todo and the clear family — plan of record (Lead, 2026-10-06)

**Ruling (Arch, 2026-10-05):** "LLM decides meaning, code decides permission." complete_todo and the clear family consume
router-extracted targets (ordinals, ranges, names, exception sets, and the clear-verb answer). Deterministic code stays at
**resolution against real data** and **the mutation boundary** (the #1190 confirm, which must ENUMERATE what will be touched
and what won't). Gate = the Phase 3 discipline: corpus rows WITH EXPECTED TARGET SETS → shadow score on the served model →
a LIVE probe that asserts the SERVED ANSWER → then delete the floor-internal binders (the new ratchet goes down).

**Why (PM, 2026-10-05, live):** "Mark the first three complete and leave the fourth one pending" completed ONE; a verb answer
carrying the list fell to `complete_todo('it')`. Both were regex interpretation of what the user said (surface 4).

## 1. The args schema (what the router emits; strings only, per the prompt's "simple key/value" rule)

For target-bearing todo/reminder ops (`complete_todo` first; `delete_todo` and the clear family follow):

| key | shape | meaning |
|---|---|---|
| `targets` | list of strings, user order | which items the verb applies to |
| `exclude` | list of strings | items explicitly carved out ("except", "but not", "leave X") |
| `scope` | `"due"` \| `"all"` | which list the positions index: the due-reminder list the floor just rendered (default when the turn follows a reminder flag) or the whole active list |

Target string mini-grammar (the router copies the user's meaning, not their words):
`"1"` ordinal (1-based) · `"1-3"` inclusive range · `"last"` · `"name:<text>"` a quoted/named item · `"all"`.
Examples: "mark the first three complete and leave the fourth" → `targets:["1-3"], exclude:["4"]`;
"clear 'check the test card again' and 'review the pr'" → `targets:["name:check the test card again","name:review the pr"]`;
"clear my reminders except for 'revise the pr'" → `targets:["all"], exclude:["name:revise the pr"]`.

**Where the router learns it:** the rail entry description (the grammar reads a rail entry's description once an op has one —
memory `project_router_grammar_prefers_rail_entry_description`), amended with one sentence naming the keys and the
mini-grammar. Scored with the ×4 same-session control on the old text, like every description change.

## 2. The gate, in order

1. **Corpus rows with `expected_args`** (new optional field; rows without it score as today). PM's own phrasings first,
   then the shapes the binders cover today (ordinal, last, `#N`, quoted name, "the overdue one", exception clause,
   verb-answer-with-list). Source prefix `phase3-args/complete_todo`.
2. **Scorer**: `router_matches` stays the action verdict; a new `args_match(expected_args, decision.args)` adds an
   `ARGS_MISMATCH` verdict (action right, targets wrong) — reported separately so the two failure classes stay visible.
   Normalization: trim, lowercase names, `#1`→`1`, `1–3`→`1-3`.
3. **Shadow score** the new rows on the served model (`--source-prefix phase3-args/`), Haiku + Sonnet legs if the Phase-2
   gate's two-leg rule applies; **≥ the Phase 3 threshold on both action and args** before the handler reads anything.
4. **Handler consumption** (behind the live flag's existing group — no new token): `handle_complete_todo` reads
   `context["inversion_args"]`; resolves `targets`/`exclude` against the real candidate list (`_due_reminder_todos` or active
   todos per `scope`); **one resolved item → complete as today**; **two or more, or any `exclude` → arm the #1190 confirm**
   with the enumeration *"Complete A, B, C? Leaving D. (yes/no)"* (a `build_todo_batch_complete_confirmation` beside the
   delete one; same carrier). Unresolvable name → the honest ask, naming the candidates. CXO rules the batch copy (her D).
5. **Live probe** (llm-marked e2e, real app + Postgres 5433): PM's phrasings → assert the SERVED ANSWER (the enumeration,
   then the completion summary), not `route=inversion`.
6. **Delete** `_ORDINAL_SHAPE_RE`-path binding in `handle_complete_todo` and the clear family's regex binders as each
   carrier flips; lower `todo-floor-binding` / `reminder-clear-binding` ceilings in the same commits. The #1631 prose floor
   retires per carrier at the same point (Arch (b)).

## 3. Pacing (Exec 10-05: weekly usage 59%, no stop line, self-pace)

Deterministic first (schema text, scorer, rows), ONE scored run of the new rows (≈20 rows × 2 legs), then the handler.
No subagent fan-out for this unit. The live probe runs once per phrasing set, not per edit.

## 4. Open questions for Arch (sent with this doc)

- Is the string mini-grammar acceptable, or do you want structured objects (`{"kind":"range","from":1,"to":3}`) despite
  the prompt's "simple strings" rule?
- `scope` default: "the list the floor just rendered" is state the router does not see — should the HANDLER infer scope
  (due list when the previous assistant turn flagged reminders; else active todos) rather than the router emitting it?
