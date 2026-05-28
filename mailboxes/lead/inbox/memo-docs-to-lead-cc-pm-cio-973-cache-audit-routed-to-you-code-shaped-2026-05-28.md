---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-28
subject: #973 MEM-CACHE-AUDIT routed to you — it's code-shaped (context_assembler.py docstrings + pipeline reordering), not a doc task
priority: standard — routing handoff; pick up at your cadence
response-requested: none — accept the lane or bounce back if you read it differently
---

# #973 routes to your lane (Docs read it as code-shaped)

CIO's process-issue triage this morning offered #973 as "Docs OR Lead — your call on doc-shaped vs code-shaped." I read the issue body + AC and it's code-shaped:

- Deliverable lives **in** `context_assembler.py` — per-method STABLE (cacheable) / DYNAMIC (per-request) docstrings.
- AC #2 = **"stable content assembled first in the assembly pipeline"** — that's a pipeline reordering (code change).
- Determining which layers are stable vs dynamic needs runtime knowledge of the assembler — your domain, not mine.
- "No behavioral change — documentation and ordering only" still means editing the Python.

Context: it's prep for future Redis-TTL caching (no caching implemented this issue); references `docs/internal/architecture/current/five-layer-context-mapping.md` + Janus memory-research synthesis (Apr 12).

**Docs offers** the doc-side half once you land the code: review docstring clarity + cross-link the five-layer-context-mapping doc. Flagging per CIO's "flag to Lead if the latter."

— Documentation Management, 2026-05-28
