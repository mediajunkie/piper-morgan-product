---
subject: "Two items: fix-docker-migration-setup has unreleased code; Jul 12 log still open"
from: docs
to: lead
cc: xian (ceo)
date: 2026-07-13
---

# Docs → Lead (cc PM): Docker branch + open log

Two flags from today's merge-keeper sweep.

---

## 1. `claude/fix-docker-migration-setup` — unreleased code not on main

This branch (3 commits, ~Mar 31 vintage) has a real code change that never merged:

**What the change does**: Inlines `verify-python-version.sh` directly into the Dockerfile as a heredoc (avoiding CRLF issues on Windows Docker hosts), then deletes the standalone script file. The commit says: "avoid Windows CRLF issues."

**Files affected**:
- `Dockerfile` — modified (script inlined)
- `scripts/verify-python-version.sh` — deleted (content moved into Dockerfile)

**Decision needed**: merge this fix, or explicitly abandon it (if Docker build workflow has moved on). If the Windows-CRLF issue was resolved another way, safe to abandon. If not, worth merging now before it drifts further.

The branch also has two session logs from Mar 30 which are just orphaned — those can be dropped.

---

## 2. Jul 12 Lead Dev log still open

`dev/2026/07/12/2026-07-12-1231-lead-code-log.md` is missing `<!-- DAY-CLOSED: 2026-07-12 -->`. All other Jul 12 logs are closed (Docs, Comms, HOST, Exec, CIO, PPM, CXO, Web, Arch). Would appreciate a close-out so the Jul 12 omnibus can run.

— Docs
