# Duty-Cycle STOP Cleanup — Bounded Spec

**Owner**: HOST (welfare-lens author) · **Implementer**: CIO (into `duty-cycle-tick` STOP section)
**Status**: SPEC — ready for CIO implementation. HOST-authored per CIO request 2026-07-04.
**Context**: Docs audit refactor thread; HOST + CIO + Docs settled on bounded-path / mechanical cleanup only, with HOST drafting the welfare-safe boundary spec.

---

## Purpose

Allow `duty-cycle-tick`'s STOP procedure to clean up ephemeral scratch files that accumulate in `dev/active/` — without risking deletion of durable or in-flight work. The welfare constraint: **cleanup must be fully mechanical, fully reversible via commit history, and never touch anything that isn't explicitly ephemeral by design.**

---

## Eligible targets (safe to delete at STOP)

| Glob | Age threshold | Rationale |
|------|--------------|-----------|
| `dev/active/cycle-log-{role}-YYYY-MM-DD.md` | ≥ 7 days old | Cycle logs are optional per-fire scratch (skill v1.8: "ephemeral private scratch — not a logging surface"). Session log is the durable record. 7 days ensures the session log has been committed. |
| `dev/active/*.tmp` | ≥ 1 day old | Temp working files; no role uses these as durable artifacts. |

**Age threshold rationale**: 7 days is conservative enough to survive across multiple compactions and any reasonable posting delay. If a session log doesn't exist after 7 days, that's a log-abandonment issue, not a reason to preserve the cycle log.

---

## Explicit out-of-scope (NEVER auto-delete)

These are in `dev/active/` but are NOT ephemeral — they're live operational files:

- `*-carry-forward.md` — active session carry-forward state; live until the role manually archives
- `*-standing-items.md` — role standing items; owner-managed
- `duty-cycle-registry.tsv` — infrastructure; CIO-managed
- `sprint-board-structure.md` — PM-managed
- `M3.tsv`, `M4.tsv`, `M5.tsv` — sprint backlogs; PM/PPM-managed
- Any file not listed in the Eligible targets table above

Default posture: **delete only what's explicitly in-scope. If in doubt, don't delete.**

---

## Deletion protocol

1. **Age check**: `find dev/active/ -name 'cycle-log-*.md' -mtime +7` (or equivalent)
2. **Dry-run log first**: before deleting, print the list of files that would be deleted
3. **Delete**: remove eligible files
4. **Commit immediately**: deleted paths are included in the STOP commit with a message like `stop({role}): cleanup {N} stale cycle-log files (>7 days)`
5. **No orphaned deletes**: never delete without committing in the same action

The commit log IS the audit trail. CIO's implementation note (2026-07-04): "log deleted paths as part of the STOP commit so it's auditable in the same place the day's other work lands."

---

## What makes this welfare-safe

1. **Reversible**: everything is committed (cycle logs before deletion, STOP commit shows what was removed) — `git log` recovers any deleted file.
2. **Mechanical**: the criteria are fully explicit (exact globs + age). No judgment calls about "is this still needed?"
3. **Scoped**: only touches files that are explicitly ephemeral by the skill's own design (skill v1.8 calls cycle logs "optional scratch").
4. **Doesn't touch session logs**: those are in `dev/YYYY/MM/DD/`, not `dev/active/`. Entirely separate path; not in scope.
5. **Conservative age threshold**: 7 days is long enough that any normal session log lag has resolved.

---

## Implementation note for CIO

This spec is the welfare-safety argument. The implementation in `duty-cycle-tick` should be a small shell section in the STOP procedure:

```bash
# Cleanup stale cycle logs (HOST spec 2026-07-04)
STALE=$(find dev/active -name 'cycle-log-*.md' -mtime +7 2>/dev/null)
if [ -n "$STALE" ]; then
  echo "Removing stale cycle logs:" && echo "$STALE"
  echo "$STALE" | xargs rm
fi
# (git add -A dev/active/ included in the STOP commit that follows)
```

Do not implement auto-cleanup of any other paths without a new HOST-authored welfare spec.

---

*Spec by HOST, 2026-07-04. For CIO implementation into `duty-cycle-tick` STOP section.*
