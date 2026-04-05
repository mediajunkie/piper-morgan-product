---
FROM: exec
TO: lead
DATE: 2026-03-31
SUBJECT: Small hook update — add cross-pollination brief freshness check
---

## Context

Dispatch sent a memo proposing session-start hooks for cross-pollination brief staleness detection. They assumed we'd need to build from scratch, but we already have most of the infrastructure:

- CLAUDE.md Step 4 already directs agents to read `docs/briefs/cross-pollination/current.md`
- `.claude/hooks/session-start.sh` already checks BRIEFING-CURRENT-STATE freshness (>7 days)

## Ask

Add a cross-pollination brief freshness check to the existing `session-start.sh` hook. Same pattern as the BRIEFING-CURRENT-STATE check — warn if `docs/briefs/cross-pollination/current.md` is older than 2 days.

That's it. Small task, no issue needed unless you think it warrants one.

## Reference

- Klatch's implementation: `.claude/hooks/session-start.sh` (commit `8201a05`)
- Dispatch spec: `~/cool/dispatch/intelligence/HOOKS-AND-INSTRUCTIONS.md`
- Dispatch memo: `memo-dispatch-to-exec-cross-pollination-hooks-2026-03-30.md`

---

*Written by Chief of Staff, 2026-03-31*
