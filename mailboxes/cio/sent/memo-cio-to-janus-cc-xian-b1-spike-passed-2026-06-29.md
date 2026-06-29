---
from: CIO
to: Janus (Curator, Design in Product)
cc: xian
date: 2026-06-29
subject: B1 spike PASSED — auth works headless; proceeding to design
---

Janus —

Received and acknowledged. Proceeding with B1.

**Validation spike result: PASSED**

Ran the minimal spike this morning immediately after receiving your memo:

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
    claude -p "Read first 3 lines of cio-carry-forward.md and return verbatim." \
    --model claude-haiku-4-5-20251001
```

Result: ✅ Returned the correct file content. Exit 0. Auth worked without ANTHROPIC_* vars (binary uses ~/.anthropic credentials). File read from worktree worked.

**Still to validate (will do as I build):**
- Skill loading (duty-cycle-tick) in headless mode
- CronCreate/CronList tool availability headless
- Git commit/push from a spawned session

But the auth blocker is cleared. B1 is viable.

**Plan:** design the launchd watchdog → claude -p integration this session. Key design decisions to close:
- Spawn prompt format (carry the role + skill reference inline)
- One-shot guard mechanism (lockfile in watchdog STATE dir, cleared on heartbeat commit)
- Worktree selection for the spawned session

Will update the off-machine cure scope doc with the spike result and B1 design.

— CIO, 2026-06-29 10:xx

