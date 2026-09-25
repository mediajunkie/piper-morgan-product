# #1735 — the personalization learning loop: re-census at HEAD, what was fixed, and the one decision left

**Date**: 2026-09-24
**Author**: Coding Agent (prog, Opus — dispatched by Lead)
**Issue**: [#1735](https://github.com/mediajunkie/piper-morgan-product/issues/1735)
**HEAD censused**: `29c64a86d3` (worktree `claude/lead-cycle`)
**Supersedes for factual purposes**: the 2026-09-08 trace in the issue body — the ground moved under
three of its four findings (#1574, #1791, #1876, and CXO's copy call all landed in between).

**Verified how** — method: every row below is a grep or a run test quoted in the same pass, not a
recollection of the 09-08 trace; layer (m-43): the store, not the return value — the auto-apply pins
read back through a *fresh* `UserPreferenceManager` against the real local Postgres, because "the
loop is connected" can only be true at the store layer; denominator: **joint 3 of 4 fixed**, joints 1,
2 and 4 censused-and-left (they are the reserved design decision), plus the three named residual
readers pinned, plus the notice copy re-checked.

---

## Part 1 — the four joints, 2026-09-08 vs NOW

| # | Joint | 09-08 finding | **NOW at `29c64a86d3`** | Evidence |
|---|---|---|---|---|
| 1 | `PersonalizationContext` — read live into classifier + floor prompts | `upsert` has **zero** content-writing callers | **UNCHANGED.** Still writer-less for real content. | `services/configuration/personalization_repository.py:57` (`upsert`). Probe: `grep -rn "\.upsert(" services/ web/ cli/ main.py` → 3 hits, and only one is this repo's: `personalization_repository.py:104`, inside `get_or_seed_default`, which passes `is_seeded_default=True` and `NEUTRAL_DEFAULT_CONTEXT`. The other two are `ConnectorConfigRepository` / `ConnectorBindingRepository`. Nothing can write tuned content. |
| 2 | `UserPreferenceManager` — where the post-#1613 learning writes | in-memory per-instance; nothing reads `personality_*` | **HALF-FIXED, and the half that remains is the important one.** *Storage*: **no longer in-memory for user scope** — #1574 made user scope read-through/write-through to `users.preferences["upm"]`. *Readers*: **still zero.** Nothing anywhere reads a `personality_*` key. | Storage: `services/domain/user_preference_manager.py:241-255` (the #1574 block), `:272` `_ensure_user_loaded`, `:304` `_persist_user_prefs`, `:374-376` (user-scope set → persist). Global and session scope are **still in-memory, on purpose** (`:226-230`, `:249` "Session scope stays in-memory ON PURPOSE"). Readers: `grep -rn 'personality_{' services/ web/ cli/` → 3 hits, **all writers or docstrings** (`preference_handler.py:225` and `:445` write; `preference_detection.py:146` documents). Zero `get_preference("personality_…")` anywhere. |
| 3 | `apply_auto_preferences` | **silent total no-op** — pattern dict missing the `confidence` / `pattern_data` keys its own gate requires | **WAS STILL TRUE AT HEAD — now FIXED.** Proven both directions by test, see below. | Gate: `services/domain/user_preference_manager.py:1213-1233` (`confidence` absent → `0.0 < 0.7` → `return False`; then `pattern_data` must carry `preference_key`/`preference_value`). Caller (pre-fix, cited by text not line since the file has since changed): in `apply_auto_preferences`, `await self.preference_manager.apply_preference_pattern(pattern={"dimension": …, "new_value": …, "hint_id": …, "source": "auto_apply"}, …)` — **none of the gate's keys** — followed immediately by `applied.append({…})` **without reading the return value**, then `logger.info(f"Auto-applied preference for {user_id}: …")`. |
| 4 | `users.preferences` JSONB — read live by `PersonalityProfile.load_with_preferences` | written only by onboarding-hardcode / declared-mode / login-tz; no learning writer | **UNCHANGED for the keys that are read.** `load_with_preferences` reads exactly five questionnaire keys and nothing else; their only writer is still an onboarding hardcode. | Reader: `services/personality/personality_profile.py:193` → `:240` `_create_from_preferences`, which reads `communication_style`, `work_style`, `decision_making`, `learning_style`, `feedback_level` (`:252-289`). Probe: `grep -rn "communication_style\|work_style\|decision_making\|learning_style\|feedback_level" services/ web/` (minus the profile module and tests) → one production writer, `services/intent/intent_service.py:4525`, and it is `prefs.get("communication_style", "detailed")` — a default-if-absent hardcode that **never overwrites and never learns**. The other JSONB writers use different keys and do not feed this reader: `collaboration_gate.py:273` (#1510 working-mode key), `user_timezone.py:115` (`timezone`, #1572), `user_preference_manager.py:324` (the `"upm"` namespace, #1574). |

### The notice copy (ADR-075 OQ-3)

**Rendered at**: `services/configuration/personalization_service.py:81` —
`FIRST_RESPONSE_PERSONALIZATION_NOTICE`, appended once by
`maybe_consume_first_response_notice` (`:182`) and spliced by
`services/intent/intent_service.py` at the seam
`result.message = f"{result.message}\n\n{notice}"`.

**Current copy**: `"(Running with a default configuration — nothing here needs setting up first.)"`

**The false clause is GONE.** CXO's 2026-09-08 copy call ("cut, don't rewrite") landed the same day;
the rationale is recorded in the module at `:70-80`.

**The xfail pin is NOT still in place — and that is correct, not a lapse.** The two composed-turn pins
in `tests/unit/services/intent_service/test_ftux_interview_1688.py`
(`TestPromiseClassPin::test_real_cold_turn_flag_on_is_promise_free` and `…_flag_off_…`) were
`xfail(strict)` while the copy decision was pending; they XPASSed when the cut landed and were
**promoted to plain green per their own instruction** (`:687-695`, `:737-746`). A third pin,
`test_notice_verbatim_cxo_copy_call_2026_09_08`, literally pins the landed string. So the copy claim
is now guarded by a green pin rather than a pending xfail — stronger, not weaker.

⚠️ **One thing to be clear about**: cutting the clause removed the *false promise*. It did not connect
the loop. Joints 1, 2-readers and 4 are all still open, which is why #1735 stays open.

---

## Part 2 — what I fixed

### (a) `apply_auto_preferences` — the silent no-op

`services/intent_service/preference_handler.py:168` (`apply_auto_preferences`).

**Red first.** `tests/unit/services/intent_service/test_auto_apply_preferences_1735.py`, driven with a
real `PreferenceHint` that passes `is_ready_for_auto_apply()` (confidence 0.95, `EXPLICIT_FEEDBACK`)
against a real per-run DB user. Baseline at `29c64a86d3`: **5 failed, 1 passed**. The load-bearing
failure was

```
tests/.../test_auto_apply_preferences_1735.py:116: in test_auto_apply_lands_in_the_upm_store_a_fresh_manager_can_read
    assert (
E   AssertionError: assert None == 'DETAILED'
```

…and note what did **not** fail in that same run: the assertions above it,
`result["success"] is True` and `result["errors"] == []`. The handler reported a clean success while
the store was empty. That is the defect, measured.

**Three changes**, all inside `apply_auto_preferences`:

1. **The pattern now has the gate's shape** — `confidence` from the hint's own `confidence_score`, and
   a real `pattern_data` whose `preference_key` is `personality_{dimension}`: the **same key**
   `confirm_preference` writes on the user-accepted path (`:445`), so the two halves of one loop stop
   disagreeing about where a learned preference lives.
2. **USER scope, and `session_id` is deliberately not forwarded.** `set_preference` routes on the
   *presence* of `session_id` **before** it reads `scope` (`user_preference_manager.py:367-379`), so
   the old `scope="session" if session_id else "user"` meant every auto-apply from the live hook —
   which always has a session (`intent_hooks.py:124-128`) — would have gone to the in-memory session
   map and evaporated even after the key bug was fixed. User scope is the DB-backed one.
3. **Failure is LOUD.** The return value of `apply_preference_pattern` is now read. A rejected write
   logs at WARNING naming the key and the confidence, and produces an `errors` entry with a `reason`
   — never a fabricated `applied` row. A hint that cannot supply `preference_value` is reported the
   same way with the missing field names. A hint below the auto-apply bar is still a **silent skip**,
   deliberately: reporting a correct skip as an error turns the loud channel into noise nobody reads.

**Green**: 9/9 in that file (the 6 auto-apply pins + 3 below). The pre-existing
`test_apply_auto_preferences_high_confidence`
(`tests/unit/services/personality/test_preference_detection.py:527`) stays green and becomes
*meaningful* — it asserted `applied` had a row, which before the fix was true precisely because the
code fabricated the row.

### (b) The three named "silently resets on restart" readers — **already fixed by #1574; now pinned**

#1735 named `calendar_setup_offered`, `slack_default_channel` and `notion_database` as readers that
treat a per-instance dict as persistent. **They do not, at HEAD.** All three are typed accessors over
`get_preference(key, user_id=…)` — `user_preference_manager.py:985`, `:1097`, `:1128` — which routes
through `_ensure_user_loaded` (`:272`) to `users.preferences["upm"]`. #1574 fixed the mechanism under
all three at once. **No residual code fix was needed.**

What *was* missing was evidence: #1574's own pins
(`tests/unit/services/domain/test_preference_persistence_1574.py`) exercise the **generic**
`set_preference`/`get_preference` with the key `"timezone"`. Nothing pinned these three **by name**,
so "already fixed" was a code-reading claim rather than a measured one. Added
`TestNamedResidualReadersAreDbBacked` — three pins, each driving the **typed accessor** across a
fresh-manager boundary (= a restart) against the real DB. All green. A future refactor of any one
accessor now cannot silently re-strand it.

### What I did **not** touch

**Which store is canonical.** #1735 reserves that for Arch/PM and I left it reserved. The fix above
makes `apply_auto_preferences` stop lying about the store *it already targeted*; it does not promote
that store, does not add a reader, and does not write to `PersonalizationContext`.

---

## The one question that remains

> **`personality_*` has two writers and zero readers. Which store should the learned personality
> actually flow into — and is the answer allowed to be "none, delete the writers"?**

Both halves of the learning loop now write `personality_{dimension}` into
`users.preferences["upm"]` durably (auto-apply as of this change; `confirm_preference` since #1574).
**Nothing reads those keys.** The live prompt-shaping path reads a *different* set of keys in the
*same column*: `load_with_preferences` reads the five flat #1422 questionnaire dims. So the learning
writes to `users.preferences["upm"]["personality_warmth_level"]` while the prompt reads
`users.preferences["communication_style"]` — same column, two rooms, no door.

The joint is therefore one **mapping function** wide, not an architecture. Three options:

| Option | What it is | Cost | Risk |
|---|---|---|---|
| **A — bridge (recommended)** | Teach `_create_from_preferences` to overlay the `upm` `personality_*` keys **on top of** the questionnaire defaults it already computes: learned value wins, questionnaire is the base, hardcoded default is the floor. | **Small — one function, ~30 lines + pins.** No migration, no new store, no new write path. The dimension→attribute mapping already exists in both directions (`PreferenceDimension` ↔ the four profile attributes). | **Low, but real**: this is the first change that lets conversation *silently* alter Piper's voice. Needs a user-visible surface ("why did it change?") or the trust property #1735 is really about is only half-closed. |
| **B — promote `PersonalizationContext`** | Make joint 1's store canonical and give `upsert` a real writer. | **Large.** A second store, a migration, and a reader swap in the classifier + floor prompt path. | Highest blast radius — it sits in the live prompt path for every turn. |
| **C — delete the writers** | Decide learned personality is not a product commitment yet; remove both `personality_*` writers and the auto-apply branch. | **Smallest.** | Honest, and cheap to reverse. But it discards a working detection stack (`ConversationAnalyzer`) rather than connecting it. |

**Recommendation: A**, *conditional on* a CXO call on the visibility question. The mechanism cost is
genuinely small and it is the only option that makes the detection stack earn its keep. But note the
shape: #1735 exists because a *copy* promise outran a *mechanism*. Shipping A without a
"here's what I learned about you, and you can undo it" surface would be the same mistake with the
arrow reversed — a mechanism that outruns the user's awareness of it. **The cheapest honest first cut
of A is: bridge the read, and have the auto-apply path surface what it changed in the turn where it
changed it** (the `applied` list this fix now populates truthfully is exactly the payload that needs).

⚠️ **Whichever way it goes, do not leave it as it is.** Two writers and zero readers is the
false-liveness class #1735 was filed under — and it is now *more* misleading than it was on 09-08,
because the write genuinely persists. A durable write nobody reads looks like a working feature from
every angle except the one that matters.

---

## Discovered while censusing (report-only — not fixed, not filed)

1. ⚠️ **Two timezone homes, and the chat action writes the one the todo path does not read.**
   `users.preferences["timezone"]` (flat, #1572) is written by the login capture
   (`services/utils/user_timezone.py:115`) and read by `get_user_timezone` (`:53`), which
   `services/intent_service/todo_handlers.py` calls at `:584`, `:786`, `:1342`, `:1740` to interpret
   due dates. `users.preferences["upm"]["standup_reminder_timezone"]` (#1876) is what the
   conversational "set my timezone to …" action and `PUT /api/v1/preferences/timezone` write
   (`workflow_entries.py:1636-1637`, `web/api/routes/preferences.py:298`). **A user who states their
   timezone in chat does not change how their todo due-dates are interpreted.** I did not run this
   end-to-end — layer checked is the read/write key path by grep, not a live turn — so treat it as a
   strong lead, not a confirmed user-visible bug. The two keys may be *intended* to be distinct
   (reminder-schedule tz vs. display tz); if so, the naming is the hazard.
2. **`PreferenceConfirmation` is constructed and discarded** in `apply_auto_preferences`
   (`preference_handler.py`, the `confirmation = …` block). I kept it — it documents the audit shape
   the confirmation path uses and its `new_value` is what gets written — but nothing persists it, so
   there is no audit trail for an auto-applied preference. Relevant to option A's visibility question.
3. **`_SESSION_HINTS` is a module-level dict** (`preference_handler.py:37`) with a 30-minute TTL and
   no eviction except on read. A suggestion offered and never confirmed is never collected. Small
   leak, not urgent; noted because it is the same "per-process dict treated as a store" family #1574
   was cleaning up.
</content>
