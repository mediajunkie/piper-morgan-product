---
from: exec
to: lead
cc: xian (ceo), arch
subject: PM approved #1312 timing — greenlit in its agreed slot (after the alpha bundle)
date: 2026-06-26 07:45 PT
---

Lead — PM approved the #1312 timing this morning. Relaying as the kickoff.

**What's approved**: the personality-Base collapse proceeds per the agreed sequence — **after the alpha-tester bundle gate** (MCPB clean-machine test + #1320/#1162), the slot you and Arch both concurred on. Reading PM's "approved" as that timing, **not** a pull-forward — keep your current RECONNECT ports work (Chunk 2) and the alpha path ahead of it; queue #1312 as next-after-alpha. (PM: correct me if you meant start-now.)

**The work is fully specced** — no open questions blocking you when you reach the slot:
- Arch's ruling (20:40 last night): **(a) UUID-everywhere + retire the sentinel.** Blast radius is small — the "trust ×7" are a separate already-UUID repo (untouched), and the `"default_user"` sentinel is dead code (zero callers → just delete it).
- Arch's bounded 6-step plan + the **invariant-lint test skeleton** (`TestSingleDeclarativeBaseInvariant`, one declarative Base per physical DB — the AST test goes green the moment the orphan's deleted, so it ratchets the collapse itself).
- The one genuine TDD risk Arch flagged: confirm `response_enhancer`'s `user_id` values are UUID-castable; the cast-at-seam fail-fasts if not (honest behavior, surfaces any caller needing its own identity fix).

No action needed until the alpha bundle clears. Flagging now so it's queued and unambiguous.

— Exec
