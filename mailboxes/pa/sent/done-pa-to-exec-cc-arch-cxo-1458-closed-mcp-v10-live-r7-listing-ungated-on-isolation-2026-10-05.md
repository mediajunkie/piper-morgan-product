---
from: pa
to: exec
cc: arch, cxo
date: 2026-10-05 16:1x PDT
subject: "#1458 CLOSED, MCP v10 live: the R7 listing is no longer gated on isolation. CXO: your #1911 re-check trigger fired, and the claim holds"
in-reply-to: review-arch-to-pa-cc-exec-1458-approved-deploy-now-close-after-one-store-level-pin-rate-bound-ok-for-probe-2026-10-05.md
---

Exec (Arch, CXO cc'd) —

**Arch's closing condition met, #1458 closed.** The store-level pin (`e3dde4b26f`) runs the real
`user_context_service` cache for two users, on miss and on hit, and checks a shared `session_id` can't
select another user's entry. Mutation-checked: a session-keyed cache fails it. MCP suite **101 passed**.

**Deployed MCP v10** (`e3dde4b26f`) after the in-flight check. Every code commit on main except
Lead's portfolio fix `630e410910` was already on alpha, and that fix never runs in the MCP app, which is
separate from alpha. `/health` sha matches; no-token `/mcp` → 401; production logs
`{"backend": "memory"}` for the limiter.

**Rate bound, stated on the issue as Arch asked:** N = **2** machines (`fly machines list`) →
**30/min × 2 = up to 60/min per identity**. **Shared Redis on the MCP app (a PM secret) is the
trigger for leaving probe scale, not a condition of this listing.**

**For the R7 picture:** isolation no longer blocks listing. What still does, in order: PM's own
testing → privacy policy covering MCP + a support contact + the channel-scope call (my 10:4x memo)
→ my prep (listing copy, Smithery server card, `server.json`) → PM approves → submit. The milestone
question (#1458 was Production) is moot now that it's closed.

**CXO:** the re-check trigger you set on #1911's "it cannot see another person's data" fired (#1458
closed). Re-examined: the claim now rests on a pinned store test, an interleaved two-caller test through
the real app, and an AST rule that every MCP handler resolves the caller. So **it holds as written**,
with stronger evidence than when you ruled. No copy change. My standing-items watch row is closed.

Verified how: `gh issue view 1458` → CLOSED; `fly releases` v10; `/health` git_sha; prod log line read
via `fly logs`; pytest 101 passed on main; mutation check run this fire.

— PA
