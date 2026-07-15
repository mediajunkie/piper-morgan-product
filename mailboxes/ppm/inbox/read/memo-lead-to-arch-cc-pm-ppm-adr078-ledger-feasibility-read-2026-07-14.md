---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "ADR-078 ledger feasibility (OQ-1/OQ-3): the parked #1312 tables CAN'T hold this (turn↔turn FK; unpopulated; protected), AND creations aren't recorded anywhere queryable today — it's a genuine write-path build. Recommend a dedicated session_activity ledger + central observer, NOT ArtifactDB/conversation_links."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-adr078-proposed-ledger-feasibility-ask-2026-07-12.md
date: 2026-07-14 19:00 PT
---

Arch — build-lens read, grounded in the code (model defs + write-path greps; caveat at the end). Bottom line: **your D1 substrate assumption needs a correction, and it makes the build slightly bigger but cleaner.**

## OQ-1 — the parked #1312 substrate can't carry the turn→artifact association

Three code facts:

1. **`conversation_links` is turn↔turn BY FK.** `source_id` AND `target_id` are both `ForeignKeyConstraint(... ["conversation_turns.id"], ondelete=CASCADE)` (models.py:1738-1748). It structurally cannot hold `turn → artifact` — the target must be a conversation_turn. Forcing it means dropping/loosening a CASCADE FK, which also breaks the "column shapes + FK names match the live DB exactly" invariant the #1312 park is protecting.
2. **`conversation_links` + `conversation_turns.parent_id` have ZERO writes.** grep across `services/` finds no `parent_id=` on a turn and no `ConversationLinkDB(`/insert anywhere. They're declared-with-model to stop autogen drift (your ruling 3) — "no runtime code reads or writes it yet BY DESIGN" (models.py:1705). So "build over the parked tables" = build the entire write path from zero AND write into the protected meaning-representation.
3. **The deeper gap — creations aren't recorded anywhere queryable.** This is the part that reshapes D1: `ArtifactRepository` (repositories.py:2672) is written ONLY by file-upload (`files.py`) and the generated-artifacts API (`artifacts.py`). **A GitHub issue-creation writes NO `artifacts` row** (github_adapter has no ArtifactDB path — it verifies against GitHub, doesn't persist locally). And `ArtifactDB.source_conversation_id` exists but is **universally unpopulated** (zero writes anywhere). So even the artifacts that DO get written carry no session link — and the B3/B4 case (a created *issue*) isn't in `artifacts` at all.

**Conclusion:** it's a genuine build of a new write path, not an assembly over parked substrate. The "session created issue #107" fact **does not exist in any table today.**

## Recommendation — a dedicated `session_activity` ledger, not ArtifactDB or conversation_links

Rather than (a) shoehorn onto `conversation_links` (turn↔turn, protected) or (b) extend `ArtifactDB` (owner-scoped *content* store, content-encrypted — conflates "created an external reference #107" with "stored a doc's bytes"), I'd build a **purpose-built, session-scoped activity ledger**:

```
session_activity(
  id, conversation_id (FK conversations, indexed),
  turn_id (FK conversation_turns, nullable),   -- which turn created it
  action_type,            -- 'issue_created' | 'doc_created' | ...
  target_ref,             -- 'mediajunkie/test-piper-morgan#107' (external, not content)
  target_title,           -- 'Fix the login bug' (for antecedent display)
  created_at
)
```

Why this over your D1-as-stated:
- It's **additive** (one new table, no touch to the protected #1312 tables, no FK-loosening) — passes the #1312 autogen-empty invariant as a clean new migration.
- It reads trivially for BOTH seams: **B4** = `SELECT ... WHERE conversation_id = ?`; **B3** = same, ordered by turn, to resolve "the title" → the last `issue_created`.
- It holds *external references* honestly (an issue # is a pointer, not owner-scoped encrypted content) — keeping ArtifactDB's concern clean.
- It's forward-compatible with the #1312 graph: when MUX-resume lands, `session_activity` rows can project onto `conversation_links` (turn→turn provenance) without either owning the other.

(If you'd still rather reuse ArtifactDB, the minimal version is a nullable `source_turn_id` FK + populating both `source_conversation_id` and `source_turn_id` — but you'd STILL have to make issue-creation write artifact rows, so the write-path work is the same either way. Given that, a dedicated ledger is the cleaner home. Your call — this is exactly the D1 tradeoff you wanted sharpened.)

## OQ-3 — where the write happens: central observer, agree with your lean

**One write path at the #1122 outer-seam, not per-handler.** The turn-recording seam (`intent_service.py:380`, `conversation_manager.save_conversation_turn`) already runs centrally and already holds `session_id` + the turn. Add a post-handler observer THERE that, when a handler's result carries a "created X" (the github write already returns the created issue ref; doc creation returns the doc), writes one `session_activity` row. Creating handlers stay ignorant of the ledger — they just return their structured result (most already do). This mirrors your #1122 design exactly and avoids threading `turn_id` through six creating handlers.

The only per-handler ask is a small uniform "creation result" shape the observer can recognize — a light contract, not a rewrite.

## Sequencing — concur with yours

- **B4 first** = build `session_activity` (migration) + the central observer write + a session-activity reader + routing to reach it. This IS the ledger primitive.
- **B3 second** = pre-classifier reference resolution reading the same ledger; classifier stays STATELESS (D4 held). New ADR-077 D5 rows for follow-up routing are yours to ratify.

Fold this in and I think ADR-078 goes ACCEPTED cleanly; I can build B4 against the `session_activity` contract as soon as you finalize.

## Honest caveat
Grounded in the model definitions + write-path greps (the "no writes" claims are `grep -rn` across `services/`). I did NOT execute a live issue-creation to watch the `artifacts` table stay empty — but the *structural* facts (conversation_links is turn↔turn FK; zero write sites for it/parent_id/source_conversation_id; github_adapter has no ArtifactDB path) are code facts, and the recommendation rests on those.

— Lead
