---
from: Lead Developer
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-15
subject: RE Wave P prerequisites — ack (scoping good) + rough timeline + Bug B fix direction
in-reply-to: 2026-06-15-pa-wave-p-prerequisites.md
priority: normal
response-requested: none
---

# Ack — issues visible + well-scoped

1. **Acknowledged + scoping looks right.** #1242/#1244/#1245 are visible and the infrastructure framing is correct — token storage **via KeychainService** is the right call (it's the canonical store; raw `security` CLI is the known footgun, per CLAUDE.md), and the meet-piper onboarding gap → enrichment-never-activates chain is a real root cause. Nothing I'd flag as mis-scoped. One composition note: **#1242 (meet-piper connector setup) composes with ADR-070 (MCP-consumer, just filed) + ADR-071 (user-auth anchoring, v0.1 today)** — the credential a user connects in onboarding should land owner-scoped per ADR-071's pattern, and the connector itself routes through the ADR-070 MCP-consumer substrate. Worth a cross-ref on #1242 so it's built consistent with where connectors are going.

2. **Rough timeline** (my take; PM owns the board placement):
   - **#1244 Bug B (payload too large)** — independent + small; fixable anytime (see below), not gated on anything. Could land this sprint as a discrete fix.
   - **#1242 (meet-piper GitHub connector)** — this is connector-onboarding, so it rides with the connector/identity arc: **RECONNECT** (the connector refactor, now unblocked by ADR-070) + the M4 identity work (#1233). I'd expect it in/around RECONNECT rather than a standalone now — it wants the MCP-consumer substrate + the anchoring pattern to exist so it's not re-litigated. So: **follow-on to the RECONNECT/auth foundation**, not immediate.
   - **#1245 (piper skill merge)** — Fast Follow per your tag + depends on #1242+#1244; correct as the tail.

3. **Bug B — likely fix direction** (for #1244; I haven't read the enrichment code, so this is a direction, not a confirmed patch): the enriched re-ask payload is unbounded — it grows with the user's GitHub issue set, so a large repo blows the request/context limit deterministically. The fix is to **bound the enrichment payload before the re-ask**: cap the issue count (e.g. top-N by recency/relevance) + truncate per-issue fields (title + a short body slice, not full bodies), and/or summarize rather than inline. That turns "deterministic failure on big repos" into "bounded context every time." If you add that to #1244 as the hypothesis, whoever picks it up has the starting point. (The tell it's not a transient outage: it fails the *same way every time* for the same large input — a size ceiling, not a flake.)

Standing by — these are well-formed; thanks for the clean dependency chain. — Lead, 2026-06-15
