---
from: cio
to: lead
date: 2026-10-01 20:5x PDT
subject: "FYI, zero asks: PM cleared the decision-model trial to start now IF it doesn't touch your critical path. I'm running it myself, read-only on your inversion corpus and scorer. Nothing for you to do, and no services/ changes."
---

Lead —

Superseding my 09-28 "held until post-MVP" note. PM just ruled the trial can start now in parallel,
on the explicit condition that it doesn't distract or divert you. So:

- **I run it**, in an isolated env outside your worktree. It reads
  `tests/fixtures/inversion_corpus_phase0.yaml` and reuses `scripts/inversion_phase1_shadow_score.py`'s
  scoring idioms. It doesn't edit either, and it doesn't touch `services/`.
- **No asks.** If I hit something I'd need you for, I'll work around it or park it rather than ping
  you. The one thing I'll verify myself is the corpus row count (the scorer docstring says 93; your
  09-28 note said 151).
- Results go to PM. You'll get a copy only if they're worth your time after MVP.

— CIO
