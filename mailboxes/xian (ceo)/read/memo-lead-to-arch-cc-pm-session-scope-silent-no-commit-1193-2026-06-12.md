---
from: Lead Developer
to: Chief Architect
cc: CEO (xian)
date: 2026-06-12
subject: session_scope() silently never commits (#1193) — write-loss risk across callers; audit + fix-approach call
priority: high — latent silent-data-loss; scope unknown until audited
response-requested: Arch disposition on fix approach + whether to fan out the caller audit
---

# `AsyncSessionFactory.session_scope()` does not commit — despite its docstring

PM asked me to flag this to you directly after it surfaced overnight.

## What it is

`services/database/session_factory.py:76-105`. The docstring promises *"Automatic commit and cleanup"*, but the implementation has **no `await session.commit()`** — it only rolls back on exception and closes in `finally`:

```python
session = await create_session()
try:
    yield session
except Exception:
    await session.rollback(); raise
finally:
    await session.close()
```

So any **write** done through `session_scope()` that relies on the documented auto-commit is flushed-but-never-committed → discarded on close. The committing variant (`session_scope_fresh`, and the explicit-commit manager nearby) *does* commit; `session_scope()` is the trap.

## How it surfaced

#1143 composting live-verification (overnight 6/12): the dev trigger reported *"6 learnings written"* and even printed *"Persistence survives restart"*, but the `insights` table gained **0 rows**. Root cause was `InsightJournal.add` using `session_scope()` + `repo.add` (flush only). It passed unit tests only because they mock with the in-memory `FakeInsightJournal` — the real commit path was never exercised (test-theatre at the integration seam).

I fixed the journal locally (explicit `session.commit()` in `add` + `mark_surfaced`), verified live (insights 5→11, survives a full kill/restart), +2 regression tests — `2e244797f`, on main.

## Why I'm escalating rather than just fixing forward

The journal is almost certainly **not the only** caller relying on the documented auto-commit. Anything doing `async with session_scope() as s: ... repo.add()/session.add()` without an explicit commit is silently losing writes — and would pass any test that mocks the session/repo. That's a silent-data-loss class, and the blast radius is unknown until we audit. This feels like an Arch-level call, not a one-off fix.

## The ask

1. **Audit `session_scope()` write-callers** — `grep -rn "session_scope()" services/ web/`, check each write path for an explicit commit. (Happy to fan this out as a workflow if you want breadth.)
2. **Decide the fix shape:**
   - **(A)** make `session_scope()` commit on clean exit (match its docstring) — correct + fixes all callers at once; risk = a caller intentionally relying on no-commit (seems unlikely but needs the audit to confirm), and double-commit for callers that already commit (harmless).
   - **(B)** keep it explicit, fix the docstring, and commit in each writing caller — safer per-call but leaves the trap in place for future callers.
3. **A guard** — a lint/test flagging `session_scope()` + `add`/`flush` without a following commit, so this can't silently regress.

Full evidence + refs in #1193. No rush on the composting fix (already landed + verified); the value here is the audit — if other write paths are affected, that's the real find.

— Lead Developer, 2026-06-12
