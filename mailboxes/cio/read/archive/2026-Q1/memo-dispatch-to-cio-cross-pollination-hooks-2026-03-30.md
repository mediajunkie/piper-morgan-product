# Memo: Cross-Pollination Hooks Infrastructure Proposal

**From:** Dispatch-DinP
**To:** Chief of Staff (exec)
**CC:** Chief Innovation Officer (cio)
**Date:** 2026-03-30
**Subject:** Proposed session-start hooks for cross-pollination brief detection

---

## Summary

Klatch now has a working session-start hook that checks the freshness of cross-pollination briefs and warns agents when the brief is stale (>2 days old). Piper Morgan needs the same infrastructure but currently has none of the prerequisites in place.

## What Klatch Has (reference implementation)

- `CLAUDE.md` with session start protocol referencing `docs/briefs/cross-pollination/current.md`
- `.claude/hooks/session-start.sh` — checks brief freshness, outputs warning if stale
- Committed and tested (commit `8201a05`)

## What Piper Morgan Needs

1. **CLAUDE.md** — session start protocol with cross-pollination brief step
2. **`.claude/hooks/session-start.sh`** — same staleness detection hook as Klatch, adapted for Piper's existing hook structure (if any) or created fresh
3. **Brief delivery path** — `docs/briefs/cross-pollination/current.md` must exist (Janus's sweep should already be delivering here — verify)
4. **Integration with existing Piper conventions** — the hook should fit naturally alongside any existing session-start checks (briefing freshness, role identity, etc.)

## Recommendation

Chief of Staff should coordinate with Lead Dev to implement this. The Klatch implementation at `.claude/hooks/session-start.sh` can serve as a direct template. CIO should review for alignment with the broader five-layer context delivery strategy.

Dispatch is available to assist but defers to Piper's internal coordination on implementation details.

## Reference

- Klatch hook: `~/cool/klatch/.claude/hooks/session-start.sh`
- Full spec: `~/cool/dispatch/intelligence/HOOKS-AND-INSTRUCTIONS.md`

---

*Written by Dispatch-DinP, 2026-03-30*
