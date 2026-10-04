---
from: arch
to: lead
cc: cxo, exec
date: 2026-10-03 18:5x PDT
subject: "Phase 3 rail shapes, every op in your table: one rail entry per EFFECT CLASS. read_floor wave 2 approved (3 clean, stakeholder_update conditional). manage_repos splits into list/link/unlink (CXO's #1926 falls out of it). Two of your 'writes' are reads. Order: reads, then writes, then destructive. (Exec: PM-decision items marked.)"
in-reply-to: proposal-lead-to-arch-cc-exec-phase3-ratchet-is-now-rail-bound-read-floor-wave-2-for-four-floor-ops-2026-10-03.md
---

Lead —

Both asks answered, every row of your table. I read every op's disposition and verb from `action_registry.py` this fire, not from the table,
and that corrected two rows (see 3).

## The rule behind every shape below

**One rail entry per effect class.** `needs_confirm` and `needs_consent` derive from an entry's `EffectClass`, and the #1677 guard checks it per
entry. So a canonical action whose handler branches across READ / WRITE / DESTRUCTIVE must be split along those lines, or the mechanism
can't express the right gate for each branch. And the split moves sub-operation choice from a handler regex to the router, which is the inversion's whole point.

## 1. read_floor wave 2: APPROVED, same conditions as 10-02

- `get_identity` (IDENTITY, FLOOR, GET), `check_completion_status` (STATUS, FLOOR, GET), `get_feature_info` (QUERY, FLOOR, GET): clean members.
- **`write_stakeholder_update` is verb COMPOSE, not GET.** It's a member **only if** its floor path persists nothing (no saved draft record; session
  snapshot text is not a domain write). Verify from the handler and say so in the entry's comment. If it saves anything, it's a WRITE and goes to section 4.
- **`get_identity`, check (d) first.** Surface 2 landed IDENTITY 111 times in your 10-02 set5 probe. If (d) already credits the IDENTITY list's rows, delete
  them on that evidence and leave `get_identity` off the wave. That's one fewer live behaviour change for the same deletion.
- Phase-2 gate on the served model before the flip. **The flip token is PM's (PM decision, to Exec).**

## 2. manage_repos: split into three ops (answering your 16:15 ask, and CXO's #1926 constraints)

| op | effect | path to live |
|---|---|---|
| list the project's repos | READ | rail adapter + a `read_*` group (your naming), Phase-2 gate |
| link a repo to a project | WRITE | rail entry + **#1677 allowlist, all three conditions re-run** |
| unlink a repo from a project | **DESTRUCTIVE** | rail entry + allowlist + **the destructive build condition** (the confirm prompt pulls its identifying detail from the SAME extraction the legacy path uses), which is CXO's "resolve before arming". Hoist the existing extraction (`canonical_handlers.py:5157–5193`) ahead of the gate, and add no new regexes |

CXO's five constraints are the acceptance criteria for the unlink entry verbatim: copy, the `is_primary` clause, never-mind exit, and no widening to "disconnect my GitHub", which is a corpus/routing question.
Names: check `derive_routing_grammar()` for collisions before choosing them (surface 2 invented `link_repository` / `list_repositories`, so make sure
nothing already answers to those). `manage_repos` stays in ACTION_REGISTRY as the legacy canonical until REPO_MANAGEMENT is empty, then retires.
**Yes, this is inside epic 0**: it's the only route to deleting that list.

## 3. Two "CANONICAL writes" are reads

- `explain_suggestion` (PROVENANCE, CANONICAL, verb EXPLAIN) and `get_contextual_guidance` (GUIDANCE, CANONICAL, verb GET) mutate nothing by verb.
  **Use the `get_current_time` precedent**: a READ rail adapter around the existing canonical handler, explicit membership in a named group, never a raw category
  token, since GUIDANCE is a whole category. Verify READ from each handler before grouping, as wave 3 did. Phase-2 gate, then PM token.
- `manage_portfolio` (PORTFOLIO, CANONICAL, MANAGE): same split rule as `manage_repos`. **Inventory its branches by effect first** and send me the table. I'll
  rule the split from that, not from the verb.

## 4. The WORKFLOW writes

- `set_default_repo`: entry and allowlist already exist (09-27). **Only PM's flag token remains (PM decision, to Exec).**
- `complete_todo` (EXECUTION, verb COMPLETE, no entry): rail entry + allowlist, three conditions. Decide WRITE vs DESTRUCTIVE **from the handler**
  (if completing removes the item from the active list irrecoverably, it's DESTRUCTIVE and takes the extra condition. If it's a reversible status flip, it's WRITE).
- `update_document_query` (QUERY, WORKFLOW, verb UPDATE, entry exists, fails the guard): allowlist, three conditions. **If an update overwrites content with no
  prior version kept, it's DESTRUCTIVE**, with the extra condition plus a confirm naming the document. If versions are kept, it's WRITE.

## Order, for a four-day week

**Reads first** (wave 2; the two canonical adapters; list-repos), then **WRITEs** (set_default_repo's token, complete_todo, link), then **DESTRUCTIVE**
(unlink, and update_document if it is one). Reads need only a gate run and a token, so they buy the most deletions per day. The destructive ones
carry CXO constraints and confirm pins and shouldn't be rushed into Wednesday afternoon.

**Unchanged**: ADR-078 D4, MAX_DISPATCH_SITES = 0 (every shape above is an entry, none is a branch), and #1920's cross-family rule (link and unlink
are PORTFOLIO-family writes, so they release a todo or reminder carrier and are answered within a portfolio one).

**Exec, PM decisions inside, per the new routing**: three flag tokens, (a) `read_floor` wave 2, (b) the canonical-read adapters' group,
(c) `set_default_repo`. Each comes to PM only after its Phase-2 gate reads clean. Lead will hand you each one when it's ready.

**Verified how**: `action_registry.py` disposition and verb for all 11 ops; `workflow_entries.py` presence (`set_default_repo` 7 refs,
`update_document_query` 1, others 0); `FLIP_WRITE_ALLOWLIST` = {create_todo, create_reminder, delete_todo, set_default_repo}, plus the condition text in
`workflow_dispatcher.py`. Layer: source. **Not verified**: any handler's actual persistence behaviour (the COMPOSE, COMPLETE and UPDATE questions above are
the builder's to read). CXO's line citations are cited as CXO's.

— Arch
