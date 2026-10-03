# 2026-10-03 1625 — prog (Coding Agent) — #1595 Phase 3 six-GO-list deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `CONTEXTUAL_QUERY_PATTERNS` (13 literals),
`GET_DEFAULT_REPO_PATTERNS` (5), `INSIGHT_PULL_PATTERNS` (7), `LOCAL_GIT_STATUS_PATTERNS` (12),
`PRODUCTIVITY_QUERY_PATTERNS` (4), `SESSION_ACTIVITY_QUERY_PATTERNS` (6) in
`services/intent_service/pre_classifier.py` (read only — no literal edited/deleted). Touched only
the corpus builder, the fixture yaml, the pinned corpus-size test, the scope doc, and this session
log. NO LLM calls made anywhere. Did not touch git index (dispatcher instruction). Did not touch
`services/` or `tests/intent/`.

## Read first

- `dev/2026/10/03/2026-10-03-1605-prog-code-log-1595-phase3-deposits-repo-management.md` and
  `dev/2026/10/02/2026-10-02-1559-prog-code-log-1595-phase3-deposits-discovery-analysis-trust-memory.md`
  — the two most recent deposit-lane templates: row-shape convention, the two-step empirical
  verification (`pre_classify_with_pattern_list` for list identity + `_first_pattern_match` for
  literal identity), the "mathematically unreachable" shadow argument, the "don't generalize an
  old REVIEW anchor's disagreement without fresh evidence" discipline, the live/non-live
  determination via `workflow_entries.py` + `action_registry.py`.
- `services/intent_service/pre_classifier.py` — read all six lists' literal definitions
  (`CONTEXTUAL_QUERY_PATTERNS` 355-371, `LOCAL_GIT_STATUS_PATTERNS` 448-465,
  `PRODUCTIVITY_QUERY_PATTERNS` 468-473, `SESSION_ACTIVITY_QUERY_PATTERNS` 478-485,
  `INSIGHT_PULL_PATTERNS` 947-962, `SET_DEFAULT_REPO_PATTERNS`/`GET_DEFAULT_REPO_PATTERNS`
  1109-1145) and every claim branch in `pre_classify_with_pattern_list` (INSIGHT_PULL ~1335,
  GET_DEFAULT_REPO ~1364, CONTEXTUAL_QUERY ~1461 with its own inline if/any() action-split
  sub-check at 1465-1479, LOCAL_GIT_STATUS ~1587, SESSION_ACTIVITY ~1705, PRODUCTIVITY ~1716) and
  `_first_pattern_match`/`_matches_patterns` (1956-1974, confirmed: returns the FIRST pattern in
  list order that matches — the mechanism every shadow argument below depends on).
- `services/intent_service/action_registry.py` + `services/intent_service/workflow_entries.py` —
  grepped all six actions: `changes_query`/`attention_query`/`get_default_repo`/
  `local_git_status_query`/`productivity_query`/`session_activity_query` are all WORKFLOW
  disposition with a registered `WorkflowEntry` whose `flip_group` is `read_temporal` (changes_
  query_entry), `read_status` (get_default_repo_entry, local_git_status_query, session_activity_
  query, attention_query), or `read_referent` (productivity_query) — all inside the dispatched
  `--live` set. `pull_insights` is `ActionDisposition.FLOOR` (action_registry.py line 83) with
  ZERO `WorkflowEntry` hits in `workflow_entries.py` (grep-confirmed) — NON-LIVE, same shape as
  the 10-02 lane's four floor lists.
- `tests/fixtures/inversion_corpus_phase0.yaml` — grepped every target action for existing rows,
  their `category` field (confirmed QUERY for the five QUERY-category actions, MEMORY for
  pull_insights — matches `IntentCategory` production assigns), and their `notes`/`probe_verdict`
  fields (found three REVIEW anchors with a historical `DISAGREE` tag — LOCAL_GIT_STATUS,
  PRODUCTIVITY, SESSION_ACTIVITY — plus separately-ruled `action:` rows for changes_query and
  session_activity_query elsewhere in the corpus with explicit CXO/PPM live-router-agreement
  reasoning).

## What I did

1. Quoted the BEFORE gate command exactly as dispatched for each of the six lists. All six read
   "GO (deletable)" under `--list` (quoted below) — every existing claimed row is already a
   live-group MATCH or REVIEW-agrees, matching the dispatch's "the gate reads GO" framing.
2. Computed the exact unexercised-literal set per list via the gate's own `unexercised_literals()`
   (imported `inversion_phase3_deletion_gate` directly, not hand-counted): CONTEXTUAL_QUERY 11/13,
   GET_DEFAULT_REPO 4/5, INSIGHT_PULL 6/7, LOCAL_GIT_STATUS 11/12, PRODUCTIVITY_QUERY 3/4,
   SESSION_ACTIVITY_QUERY 5/6 — **40 unexercised literals total**, matching the dispatch's
   13/2, 5/2, 7/2, 12/1, 4/1, 6/1 framing exactly.
3. Read each claim branch directly. Five of six lists are single-action (no per-literal
   branching): GET_DEFAULT_REPO → `get_default_repo`, INSIGHT_PULL → `pull_insights` (category
   MEMORY), LOCAL_GIT_STATUS → `local_git_status_query`, PRODUCTIVITY_QUERY →
   `productivity_query`, SESSION_ACTIVITY_QUERY → `session_activity_query`. CONTEXTUAL_QUERY
   is a two-way split resolved by the SAME explicit `any()` sub-check the claim site itself runs
   (lines 1465-1479): the first 7 literals (the "changes" block) route `changes_query`, the
   remaining 6 (the "attention" block) route `attention_query` by elimination — read the exact
   sub-check regex list (identical to the list's own first 7 literals) rather than guessing which
   block a literal belonged to.
4. Determined live/non-live for each action by reading `action_registry.py` +
   `workflow_entries.py` directly (not inferred): `changes_query` (flip_group `read_temporal`),
   `attention_query`/`get_default_repo`/`local_git_status_query`/`session_activity_query`
   (flip_group `read_status`), `productivity_query` (flip_group `read_referent`) — all five LIVE
   rail ops, all five flip_groups inside the dispatched `--live` set. `pull_insights` — FLOOR,
   zero `WorkflowEntry` registrations — the one NON-LIVE op this unit.
5. Checked each existing REVIEW anchor's historical `DISAGREE` tag against its CURRENT gate-run
   verdict (same "don't generalize without fresh evidence" discipline the REPO_MANAGEMENT lane
   established): LOCAL_GIT_STATUS's "what branch are we on?", PRODUCTIVITY's "what's my
   productivity?", and SESSION_ACTIVITY's "what did we create this session?" all show
   REVIEW-agrees at router confidence 1.0 in the CURRENT gate run (quoted below) — the historical
   DISAGREE tag is stale. Cross-checked against separately-ruled `action:` rows elsewhere in the
   corpus for changes_query/session_activity_query (CXO/PPM "beyond Arch's four named buckets"
   rulings, explicit live-router-agreement reasoning) — confirms the generalization. Concluded:
   no REVIEW rows needed for any of the 40 literals; all use the list's own confident action.
6. Drafted one natural phrase per unexercised literal, reasoning through same-list earlier-sibling
   shadow risk by hand (reading each list's full literal set and matching order) BEFORE drafting,
   then verified every candidate empirically in one combined script against the REAL production
   matcher: `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name + action assertion)
   and `PreClassifier._first_pattern_match(cleaned, PreClassifier.<LIST>)` (literal-identity
   assertion, using the exact `clean_for_matching` production transform). **39 of 40 passed on the
   first attempt.**
7. The one failure was diagnosed, not discarded: GET_DEFAULT_REPO_PATTERNS'
   `\bwhat\s+default\s+repo(?:sitory)?\b` was claimed by its earlier sibling
   `\bwhat(?:'s|\s+is)?\s+(?:my\s+)?default\s+repo(?:sitory)?\b` instead. Proved this is
   STRUCTURAL, not phrasing-dependent: the earlier literal's `'s`/`is`/`my` groups are all
   optional, so any string satisfying the later literal (bare "what" + whitespace + "default" +
   whitespace + "repo[sitory]") already satisfies the earlier one — a strict subset relationship
   for every possible input. Confirmed with three more independent phrasings ("what default repo
   should i use", "what default repository is configured", "what default repo" bare) — all four
   claimed by the earlier sibling, never this literal. Same shape as the 10-02 lane's MEMORY_
   PATTERNS self-shadow. No row deposited for this literal.
8. Also found (while drafting, not from a failure) that SESSION_ACTIVITY_QUERY_PATTERNS'
   `\bwhat did (?:we|i) create this session\b` is PARTIALLY shadowed: its "we" branch ("what did
   we create this session") is always claimed first by the earlier sibling `\bwhat did we
   create\b` (a strict prefix match — confirmed empirically), but its "i" branch ("what did I
   create this session") has no such earlier-sibling prefix and reaches the literal cleanly. Used
   the "i" phrasing — reachable, not shadowed, same "one reachable shape" pattern as the
   REPO_MANAGEMENT lane's "which repo connected" row.
9. Checked all 39 drafted phrases against the existing corpus via `grep -qF` — zero duplicates.
10. Deposited a single HAND_ROWS block (39 rows) in `scripts/build_inversion_corpus_phase0.py`,
    after the existing REPO_MANAGEMENT_PATTERNS block, before the closing `]`. `source` cites
    `phase3-conversion/<LIST> literal r"<literal>"` per row, matching convention. `category: QUERY`
    for the five QUERY-category lists, `category: MEMORY` for INSIGHT_PULL rows (matching
    production's `IntentCategory` assignment, confirmed against existing corpus rows for the same
    actions). `notes` on rows carrying a specific finding (the GET_DEFAULT_REPO shadow literal's
    own comment explains why NO row was deposited for it; the LOCAL_GIT_STATUS local/git-status
    pair notes the within-list ordering; the SESSION_ACTIVITY "i"-variant row notes the partial
    shadow; the six INSIGHT_PULL rows each note the NON-LIVE disposition).
11. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 457 → 496
    rows (+39). `git diff --numstat` on the yaml + builder: 320/0 and 165/0 — purely additive, zero
    deletions. QUERY category denominator: 123 → 162 (39 new QUERY rows — the INSIGHT_PULL rows
    are category MEMORY, not QUERY).
12. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
    `test_claimed_plus_unclaimed_equals_corpus_size` 457 → 496 (claimed 75 → 114, unclaimed
    unchanged at 382 — confirmed by direct `gate.build_census(cats=None)` call using the test's
    own exact computation). Searched for other pinned `\b457\b` constants: `git grep -n "\b457\b"
    -- tests scripts` — only the just-fixed hit plus unrelated matches (an SVG path string, a
    migration-script comment, a large-text fixture line).
13. Re-ran the gate for all six lists: all now read "GO (partial)" (not "GO (deletable)" anymore,
    since every new row is UNSCORED/[FAIL] under the partial-verdict logic — same mechanics the
    REPO_MANAGEMENT lane's AFTER report showed). Directly confirmed via `unexercised_literals()`
    that exactly 1 of 40 literals remains unexercised (the proven GET_DEFAULT_REPO shadow) and the
    other 39 are now claimed.
14. Ran both dry-run validations — no LLM calls (each script self-reports this):
    - `inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls" self-reported (same
      pre-existing, unrelated TEMPORAL regression note every prior lane since has also seen — not
      touched by this unit, no TEMPORAL literal involved).
    - `inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made" self-reported.
15. `ruff format` + `ruff check` on both touched `.py` files: `ruff check` was already clean;
    `ruff format --check` flagged the builder for reformatting, ran `ruff format` to fix,
    re-confirmed clean. `git diff --numstat` reconfirmed purely additive (320/0, same as before
    the reformat) after; regenerated the corpus yaml once more to confirm it's unaffected
    (identical row count and structure).
16. Tests (run together this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` +
      `tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
      `tests/unit/test_inversion_phase1_shadow_score_1595.py` +
      `tests/test_architecture_enforcement.py` — **143 passed, 1 xfailed**, 0 failed.
    - Extraction ceiling re-confirmed **201** (unchanged) via direct
      `pattern_literal_counts.total_literal_count()` call — no `pre_classifier.py` literal
      edited/deleted in this unit.
17. Added a dated progress-log entry to
    `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.
18. Verified scope compliance via `git status --short` at session end: only
    `scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`, and
    `tests/unit/test_inversion_phase3_deletion_1595.py` show as modified. Git index not touched
    (nothing staged, per dispatcher instruction).

## Table: literal → phrase → expected → verified-claiming-literal (per list)

### CONTEXTUAL_QUERY_PATTERNS (11 of 11 unexercised literals — 100% reachable)

| literal | phrase | expected |
|---|---|---|
| `\bwhat'?s changed since\b` | "what's changed since last week" | `action:changes_query` |
| `\bshow.*changes since\b` | "show me the changes since last monday" | `action:changes_query` |
| `\bshow me.*changed\b` | "show me everything that's changed" | `action:changes_query` |
| `\bchanges since\b` | "any changes since the last deploy" | `action:changes_query` |
| `\bactivity since\b` | "give me the activity since yesterday's standup" | `action:changes_query` |
| `\bupdates since\b` | "any updates since this morning" | `action:changes_query` |
| `\bwhat needs attention\b` | "what needs attention right now" | `action:attention_query` |
| `\bneeds my attention\b` | "this project needs my attention today" | `action:attention_query` |
| `\bshow.*needs.*attention\b` | "show me what needs the most attention" | `action:attention_query` |
| `\bitems.*need.*attention\b` | "the items that need attention haven't been touched" | `action:attention_query` |
| `\battention items\b` | "please list the attention items for review" | `action:attention_query` |

### GET_DEFAULT_REPO_PATTERNS (3 of 4 unexercised literals reachable — 1 unreachable)

| literal | phrase | expected |
|---|---|---|
| `\bwhich\s+(?:repo(?:sitory)?\s+)?is\s+(?:my\s+)?default(?:\s+repo(?:sitory)?)?\b` | "which repository is my default" | `action:get_default_repo` |
| `\b(?:show\|see\|tell\s+me\|get)\s+(?:my\s+)?default\s+repo(?:sitory)?\b` | "please show my default repository" | `action:get_default_repo` |
| `^(?:my\s+)?default\s+repo(?:sitory)?\??$` | "my default repository" | `action:get_default_repo` |

**Unreachable**: `\bwhat\s+default\s+repo(?:sitory)?\b` — mathematically shadowed by its earlier
sibling `\bwhat(?:'s|\s+is)?\s+(?:my\s+)?default\s+repo(?:sitory)?\b` (optional `'s`/`is`/`my`
groups make the earlier pattern a strict superset). Confirmed empirically with four phrasings, all
claimed by the earlier sibling. No row deposited.

### INSIGHT_PULL_PATTERNS (6 of 6 unexercised literals — 100% reachable; NON-LIVE op)

| literal | phrase | expected |
|---|---|---|
| `\bwhat do you know about (me\|my \|our \|the )` | "what do you know about my work habits" | `action:pull_insights` |
| `\btell me what you('ve\| have) learned\b` | "tell me what you've learned about my habits" | `action:pull_insights` |
| `\bwhat insights do you have\b` | "what insights do you have about my productivity" | `action:pull_insights` |
| `\bshow me what you('ve\| have) learned\b` | "show me what you've learned about my preferences" | `action:pull_insights` |
| `\bwhat patterns have you (noticed\|observed\|found\|seen)\b` | "what patterns have you noticed in my work" | `action:pull_insights` |
| `\bwhat have you noticed about (me\|my \|our \|the )` | "what have you noticed about my habits lately" | `action:pull_insights` |

### LOCAL_GIT_STATUS_PATTERNS (11 of 11 unexercised literals — 100% reachable)

| literal | phrase | expected |
|---|---|---|
| `\bwhat branch am i on\b` | "what branch am i on right now" | `action:local_git_status_query` |
| `\bwhich branch are we on\b` | "which branch are we on at the moment" | `action:local_git_status_query` |
| `\bcurrent branch\b` | "can you tell me the current branch" | `action:local_git_status_query` |
| `\bworking tree (?:clean\|dirty\|status)\b` | "what's the working tree status" | `action:local_git_status_query` |
| `\buncommitted changes?\b` | "are there any uncommitted changes" | `action:local_git_status_query` |
| `\bdirty (?:working )?tree\b` | "do we have a dirty working tree" | `action:local_git_status_query` |
| `\bahead of (?:main\|origin\|upstream\|master)\b` | "are we ahead of origin right now" | `action:local_git_status_query` |
| `\bbehind (?:main\|origin\|upstream\|master)\b` | "are we behind upstream at all" | `action:local_git_status_query` |
| `\bunpushed commits?\b` | "do we have any unpushed commits" | `action:local_git_status_query` |
| `\blocal git status\b` | "can you show the local git status" | `action:local_git_status_query` |
| `\bgit status\b` | "please run git status for me" | `action:local_git_status_query` |

(The last two are siblings where "local git status" is a substring of itself containing "git
status" — since the "local git status" literal is earlier in the list, `_first_pattern_match`
claims it first; the "git status" row's phrase deliberately omits "local" so it reaches its own
literal.)

### PRODUCTIVITY_QUERY_PATTERNS (3 of 3 unexercised literals — 100% reachable)

| literal | phrase | expected |
|---|---|---|
| `\bshow.*productivity\b` | "show me my productivity report" | `action:productivity_query` |
| `\bproductivity metrics\b` | "can you share my productivity metrics" | `action:productivity_query` |
| `\bmy productivity\b` | "i'd like to check my productivity this week" | `action:productivity_query` |

### SESSION_ACTIVITY_QUERY_PATTERNS (5 of 5 unexercised literals — 100% reachable)

| literal | phrase | expected |
|---|---|---|
| `\bwhat have we created\b` | "what have we created so far" | `action:session_activity_query` |
| `\bwhat did we make\b` | "what did we make earlier" | `action:session_activity_query` |
| `\bwhat did (?:we\|i) create this session\b` | "what did i create this session" | `action:session_activity_query` |
| `\bwhat did we do this session\b` | "what did we do this session" | `action:session_activity_query` |
| `\bwhat (?:issues\|items) did we (?:create\|make\|open)\b` | "what issues did we open during the call" | `action:session_activity_query` |

(The third row's "we" phrasing is shadowed by the earlier sibling `\bwhat did we create\b` — the
"i" phrasing is the only reachable shape for this literal, confirmed empirically.)

**39/40 reachable, verified via the real production matcher, zero rewords needed for any deposited
phrase, zero duplicate phrases.**

## Live/non-live per action (for the Lead's surface-2-probe planning)

| action | list | disposition | flip_group | live under dispatched `--live` set? |
|---|---|---|---|---|
| `changes_query` | CONTEXTUAL_QUERY (changes block) | WORKFLOW | `read_temporal` | **LIVE** |
| `attention_query` | CONTEXTUAL_QUERY (attention block) | WORKFLOW | `read_status` | **LIVE** |
| `get_default_repo` | GET_DEFAULT_REPO | WORKFLOW | `read_status` | **LIVE** |
| `local_git_status_query` | LOCAL_GIT_STATUS | WORKFLOW | `read_status` | **LIVE** |
| `productivity_query` | PRODUCTIVITY_QUERY | WORKFLOW | `read_referent` | **LIVE** |
| `session_activity_query` | SESSION_ACTIVITY_QUERY | WORKFLOW | `read_status` | **LIVE** |
| `pull_insights` | INSIGHT_PULL | FLOOR | none (no WorkflowEntry) | **NON-LIVE** |

Five of six actions are LIVE rail ops — the inverse of the REPO_MANAGEMENT lane (where the single
action was non-live despite being CANONICAL disposition) and the DISCOVERY/ANALYSIS/TRUST/MEMORY
lane (all four floor/non-live). `pull_insights` is the one op in this unit that will need a
surface-2 probe when scored; the other five won't, since the live consult already dispatches their
rail keys directly.

## Findings

**One structurally-unreachable literal** (GET_DEFAULT_REPO_PATTERNS): see item 7 above and the
table note. Mathematical shadow, not phrasing-dependent — proved via the optional-group
superset argument and confirmed with four independent phrasings.

**One partially-unreachable literal** (SESSION_ACTIVITY_QUERY_PATTERNS): see item 8 above. Only
the "we" branch is shadowed; the "i" branch is independently reachable and was used for the
deposited row.

**Three historical REVIEW/DISAGREE anchors do not generalize to the new rows.** LOCAL_GIT_STATUS,
PRODUCTIVITY, and SESSION_ACTIVITY each carry a corpus row whose `probe_verdict: DISAGREE` tag
dates to an earlier probe, but the CURRENT gate run (quoted below) shows REVIEW-agrees at router
confidence 1.0 for all three. Cross-checked against already-ruled `action:` rows elsewhere in the
corpus for the same action family (changes_query, session_activity_query) with explicit CXO/PPM
live-agreement reasoning. No REVIEW rows deposited for any of the 39 new rows — same discipline the
REPO_MANAGEMENT lane established for its own REVIEW anchor.

**No destructive-confirm or other write-without-guard findings this unit.** All six lists/actions
are pure READS (confirmed by reading each handler's `effect=EffectClass.READ` declaration in
`workflow_entries.py`, or FLOOR disposition for pull_insights) — no destructive verb, no mutation,
nothing analogous to the REPO_MANAGEMENT lane's unlink-without-confirm finding.

## Gate output — BEFORE (all six lists)

```
=== CONTEXTUAL_QUERY_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## CONTEXTUAL_QUERY_PATTERNS
literals: 13  |  rows claimed: 2/457
verdict: GO (deletable) — deleting removes 13 literals: ceiling 201 -> 188
rows claimed:
  [OK] "what needs my attention?" -> claim=attention_query expected=action:attention_query router=attention_query@0.95 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what changed since yesterday?" -> claim=changes_query expected=action:changes_query router=changes_query@1.0 verdict=MATCH :: MATCH (expected action live via group)
pattern->corpus conversion needed (11 literal(s) unexercised): [11 literals listed]

=== GET_DEFAULT_REPO_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## GET_DEFAULT_REPO_PATTERNS
literals: 5  |  rows claimed: 2/457
verdict: GO (deletable) — deleting removes 5 literals: ceiling 201 -> 196
rows claimed:
  [OK] "what is my default repo?" -> claim=get_default_repo expected=action:get_default_repo router=get_default_repo@1.0 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what's my default repo?" -> claim=get_default_repo expected=REVIEW router=get_default_repo@1.0 verdict=REVIEW :: REVIEW-agrees (route=get_default_repo == claim=get_default_repo; live via group)
pattern->corpus conversion needed (4 literal(s) unexercised): [4 literals listed]

=== INSIGHT_PULL_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## INSIGHT_PULL_PATTERNS
literals: 7  |  rows claimed: 2/457
verdict: GO (deletable) — deleting removes 7 literals: ceiling 201 -> 194
rows claimed:
  [OK] "what have you learned about my workstyle?" -> claim=pull_insights expected=action:pull_insights router=pull_insights@0.95 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what have you learned about my work style?" -> claim=pull_insights expected=REVIEW router=pull_insights@1.0 verdict=REVIEW :: REVIEW-agrees (route=pull_insights == claim=pull_insights; live via group)
pattern->corpus conversion needed (6 literal(s) unexercised): [6 literals listed]

=== LOCAL_GIT_STATUS_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## LOCAL_GIT_STATUS_PATTERNS
literals: 12  |  rows claimed: 1/457
verdict: GO (deletable) — deleting removes 12 literals: ceiling 201 -> 189
rows claimed:
  [OK] "what branch are we on?" -> claim=local_git_status_query expected=REVIEW router=local_git_status_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=local_git_status_query == claim=local_git_status_query; live via group)
pattern->corpus conversion needed (11 literal(s) unexercised): [11 literals listed]

=== PRODUCTIVITY_QUERY_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## PRODUCTIVITY_QUERY_PATTERNS
literals: 4  |  rows claimed: 1/457
verdict: GO (deletable) — deleting removes 4 literals: ceiling 201 -> 197
rows claimed:
  [OK] "what's my productivity?" -> claim=productivity_query expected=REVIEW router=productivity@1.0 verdict=REVIEW :: REVIEW-agrees (route=productivity == claim=productivity_query; live via group)
pattern->corpus conversion needed (3 literal(s) unexercised): [3 literals listed]

=== SESSION_ACTIVITY_QUERY_PATTERNS ===
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed
## SESSION_ACTIVITY_QUERY_PATTERNS
literals: 6  |  rows claimed: 1/457
verdict: GO (deletable) — deleting removes 6 literals: ceiling 201 -> 195
rows claimed:
  [OK] "what did we create this session?" -> claim=session_activity_query expected=REVIEW router=session_activity_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=session_activity_query == claim=session_activity_query; live via group)
pattern->corpus conversion needed (5 literal(s) unexercised): [5 literals listed]
```

(Command, each list: `scripts/inversion_phase3_deletion_gate.py --list <LIST> --live
create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,
read_synthesis,read_temporal`)

## Gate output — AFTER (all six lists)

```
=== CONTEXTUAL_QUERY_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 13  |  rows claimed: 13/496
verdict: GO (partial) — 11 load-bearing literal(s) SURVIVE, deleting the other 2: ceiling 201 -> 199
  (the 2 already-scored OK rows don't need survivor status; all 11 new UNSCORED rows do)
rows claimed: 2 [OK] (unchanged) + 11 [FAIL] UNSCORED (no router call made)

=== GET_DEFAULT_REPO_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 5  |  rows claimed: 5/496
verdict: GO (partial) — 3 load-bearing literal(s) SURVIVE, deleting the other 2: ceiling 201 -> 199
rows claimed: 2 [OK] (unchanged) + 3 [FAIL] UNSCORED

=== INSIGHT_PULL_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 7  |  rows claimed: 8/496
verdict: GO (partial) — 6 load-bearing literal(s) SURVIVE, deleting the other 1: ceiling 201 -> 200
rows claimed: 2 [OK] (unchanged) + 6 [FAIL] UNSCORED

=== LOCAL_GIT_STATUS_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 12  |  rows claimed: 12/496
verdict: GO (partial) — 11 load-bearing literal(s) SURVIVE, deleting the other 1: ceiling 201 -> 200
rows claimed: 1 [OK] (unchanged) + 11 [FAIL] UNSCORED

=== PRODUCTIVITY_QUERY_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 4  |  rows claimed: 4/496
verdict: GO (partial) — 3 load-bearing literal(s) SURVIVE, deleting the other 1: ceiling 201 -> 200
rows claimed: 1 [OK] (unchanged) + 3 [FAIL] UNSCORED

=== SESSION_ACTIVITY_QUERY_PATTERNS ===
corpus denominator: 496 rows total = 114 claimed + 382 unclaimed
literals: 6  |  rows claimed: 6/496
verdict: GO (partial) — 5 load-bearing literal(s) SURVIVE, deleting the other 1: ceiling 201 -> 200
rows claimed: 1 [OK] (unchanged) + 5 [FAIL] UNSCORED
```

All six "GO (partial)" with 0 deletable this unit — correct and expected: every new row reads
UNSCORED (no router call made, no LLM calls anywhere in this unit), same 2026-10-01 gate tightening
every prior lane since has found. Direct `unexercised_literals()` call confirms exactly 1 of the 40
originally-unexercised literals remains unexercised (the proven GET_DEFAULT_REPO shadow); the other
39 are now claimed. The Lead's budgeted scoring run resolves MATCH/REVIEW/MISMATCH per row.

## New corpus total

457 → **496** rows (+39). Per-category denominators after rebuild: QUERY 162 (was 123), TEMPORAL
69, STATUS 54, PRIORITY 44, PORTFOLIO 27, GUIDANCE 26, EXECUTION 26, DISCOVERY 25, **MEMORY 23**
(was 17), ANALYSIS 15, TRUST 11, CONVERSATION 5, SYNTHESIS 4, IDENTITY 3, PROVENANCE 2.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 496 rows (54 REVIEW), exit 0.
- `git diff --numstat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `165 0` and `320 0` respectively — purely additive, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported.
- Per-list gate re-runs (all six, quoted above) → exit 0, corpus denominator 496 rows = 114
  claimed + 382 unclaimed; all six GO (partial), all 39 new rows UNSCORED.
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py
  tests/unit/test_inversion_phase3_surface2_floor_1595.py
  tests/unit/test_inversion_phase1_shadow_score_1595.py tests/test_architecture_enforcement.py
  -q -p no:cacheprovider` → **143 passed, 1 xfailed**, exit 0.
- `venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import pattern_literal_counts as
  plc; print(plc.total_literal_count())"` → **201**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted; task's "no deletion in this unit" condition met).
- `venv/bin/ruff format` on `scripts/build_inversion_corpus_phase0.py` → 1 file reformatted;
  `ruff format --check` + `ruff check` on both touched `.py` files → clean after; `git diff
  --numstat` reconfirmed 0 deletions after the reformat, and the regenerated corpus yaml is
  unaffected (identical 496-row output).

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +39 rows in one comment-headed block,
  after the REPO_MANAGEMENT_PATTERNS block, before the closing `]`)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 457→496 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 457→496, with
  updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (dated progress-log entry added)
- This session log (new)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/canonical_handlers.py` (read only), `services/intent_service/
action_registry.py` (read only), `services/intent_service/workflow_entries.py` (read only),
`tests/intent/` (not touched this unit), `web/` (not relevant), any flag/env var,
`scripts/inversion_phase3_deleted_patterns.json` (no deletion performed), the gate script, the
ledger, GitHub.

## Verified how

- **Method**: computed the exact unexercised-literal set per list by importing and calling the
  gate's own `unexercised_literals()` against `build_census()`'s claimed rows (not hand-counted).
  Read each list's full literal set and the `pre_classify_with_pattern_list` if-chain ordering
  directly (not inferred) before drafting any phrase, including CONTEXTUAL_QUERY's own inline
  action-split sub-check. Drafted 40 phrases designed from the regex structure and the identified
  shadow risks; verified all 40 in one combined script run against the REAL production functions
  — `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name AND `intent.action` read
  directly) and `PreClassifier._first_pattern_match(cleaned, PreClassifier.<LIST>)`
  (literal-identity assertion, using production's own `clean_for_matching` transform) — with 39/40
  passing on the first attempt. The 1 failure was independently re-verified with 3 more
  phrasings to confirm the shadow is structural (optional-group superset argument), not an
  accident of the first phrasing choice. Checked all 39 deposited phrases against the existing
  corpus via `grep -qF` before depositing — zero duplicates. Gate re-runs, pytest, ruff, and
  ceiling invocations were all run this turn via Bash and their output is quoted/counted above, not
  recalled from memory. `git diff --numstat` run and quoted directly to confirm purely-additive
  changes, re-confirmed after the ruff reformat and after a second corpus regen. `git status
  --short` run at session end to confirm scope compliance.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit —
  the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in this
  session, confirmed by each script's own self-report and the absence of any LLM-client invocation
  in the commands run). The WORKFLOW/FLOOR disposition and flip_group membership were verified by
  reading `action_registry.py` and `workflow_entries.py` directly, not inferred from behavior. The
  three REVIEW-anchor re-checks were read from the gate's own current-run output, not assumed from
  the corpus's historical `probe_verdict` field.
- **Denominator**: 6 target lists (CONTEXTUAL_QUERY/GET_DEFAULT_REPO/INSIGHT_PULL/LOCAL_GIT_STATUS/
  PRODUCTIVITY_QUERY/SESSION_ACTIVITY_QUERY) — 39 of 40 previously-unexercised literals (across all
  six lists combined) now have a corpus row; 1 of 40 confirmed structurally unreachable (proven via
  the optional-group superset argument, not just empirically probed, and reconfirmed with 3
  additional phrasings). Test denominator: 143/143 passed (plus 1 pre-existing xfail) across all
  four specified test files run together in one invocation, not separately. Ceiling denominator:
  201/201 unchanged, confirmed by direct call. `git status` run at session end to confirm scope
  compliance (3 tracked files touched, matching the dispatch's allowed scope).

## Memory & briefing surfaces referenced this session

- **Referenced**: `dev/2026/10/03/2026-10-03-1605-prog-code-log-1595-phase3-deposits-repo-management.md`
  and `dev/2026/10/02/2026-10-02-1559-prog-code-log-1595-phase3-deposits-discovery-analysis-trust-memory.md`
  (row-shape convention, two-step empirical verification method, the mathematical-unreachability
  argument shape, the live/non-live determination method, the "don't generalize an old REVIEW
  anchor without fresh evidence" discipline — all directly informed this unit's structure and
  findings); `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress
  log, appended to).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope — git index not touched at all).
- **Wanted but not found**: none — the dispatch prompt's cited templates and the live code
  (pre_classifier.py, action_registry.py, workflow_entries.py, canonical_handlers.py) were
  sufficient for every claim made in this unit.

## Discovered work

None filed as a separate GitHub issue (matching the established convention of prior deposit lanes
— reporting inline rather than filing, since these are measurement/evidence findings for the
Lead's own ruling, not independently actionable bugs). No destructive-write-without-guard findings
this unit (all six actions are pure reads or FLOOR). Two structural findings reported inline above:
the GET_DEFAULT_REPO self-shadow (no row deposited, proof given) and the SESSION_ACTIVITY partial
self-shadow (the "we" branch shadowed, the "i" branch used instead).
