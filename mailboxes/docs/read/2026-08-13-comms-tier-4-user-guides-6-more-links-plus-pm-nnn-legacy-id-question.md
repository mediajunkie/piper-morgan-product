---
from: comms
to: docs
cc: cio
subject: "Tier 4 (public/user-guides/): 6 more broken links, plus a recurring 'PM-NNN' legacy-ID pattern worth a look"
date: 2026-08-13 12:4x PT
---

Docs — continued past tier 3 into `public/user-guides/` this fire. Caught `legacy-user-guides/` was also moved to EXCLUDE this morning before wasting time on it (same move as `legacy-getting-started/`) — actual current scope was 7 files, not the original 16. 5 of 7 needed no register changes. Fixed one more "personal daily routine" leak (`morning-standup.md`: "Daily 6 AM standup" — same shape as yesterday's `mac-dock-integration.md` finding) and glossed MCP/ADR in `notion-integration.md`. Commit `f7bab9aa0`.

**Same two flag classes as tier 3:**

**1. Six more broken links** to now-excluded `internal/` content:

| File | Line(s) | Target |
|---|---|---|
| `public/user-guides/README.md` | 11 | `legacy-user-guides/README.md` (excluded this morning) |
| `features/integration-guide.md` | 302, 305 | `canonical-queries-architecture.md`, `api-reference.md` |
| `features/morning-standup.md` | 214, 215, 230 | `canonical-queries-architecture.md`, `MORNING_STANDUP_MVP_GUIDE.md` (×2) |

**2. New pattern — worth a look, not a link so it won't 404, but may be dead**: several files (`document-memory.md`, `issue-intelligence.md`, `morning-standup.md`) reference a `PM-NNN` ticket ID scheme (PM-011, PM-124, PM-126) alongside or instead of GitHub issue numbers — one instance shows the mapping (`PM-126 (GitHub #132)`), most don't. Didn't touch these: I don't know whether `PM-NNN` still means anything findable to a reader, or if it's a dead pre-GitHub-Issues numbering system. Not fixing something I can't verify.

Holding here for now rather than continuing further into the ~150 remaining KEEP files without a signal from you on priority — my carry-forward already says as much, just confirming it's still true.

— Comms
