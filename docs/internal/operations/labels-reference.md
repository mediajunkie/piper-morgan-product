# GitHub Labels Reference

**Status**: Canonical labels and conventions for the Piper Morgan repository.
**Last updated**: 2026-05-10
**Owner**: Lead Developer (ships); Architect (consults on structural decisions)

---

## Canonical labels

### `blocked` (flat, no prefix) — canonical 2026-05-10

**Decision**: PM disposition 2026-05-05 (#983 label-convention memo); Architect concurrence 2026-05-10 (bundled-response memo to Lead Dev).

**Semantics**: Issue is blocked on an external dependency or upstream decision — not actionable as currently scoped. Use sparingly; prefer a comment explaining what's blocking with cross-reference to the blocking issue.

**Why flat (no prefix)** rather than `status:blocked`:
- Our label vocabulary is currently minimal (~10-15 distinct labels)
- Flat is right *now*; namespaced becomes right *if* the vocabulary grows to ~30+ labels spanning multiple dimensions (priority, area, status, phase, etc.)
- The future-option is captured: when migration is needed, the canonical path is `blocked` → `status:blocked` with backward-compatible aliasing during transition

**Programmatic use**: `services/intent_service/context_assembler.py` (when #983 ships) will query for issues with this label to surface "blocked items" in floor context for PRIORITY queries.

**Not in scope (filed separately if needed)**: `needs-review`, `waiting-for`, `awaiting-input`. These are distinct concepts (review-pending, outbound-dependency, etc.) that warrant their own categories rather than additional rows in the blocked-bucket.

### Other canonical labels

Existing labels per `gh label list` should be considered canonical unless explicitly deprecated here. As of 2026-05-10, the priority labels (`priority: critical|high|medium|low`), category labels (`bug`, `enhancement`, `documentation`, `technical-debt`, `epic`, etc.), and sub-epic labels (`M2e`, `M2f`, `M2g`) form the working set.

---

## Migration path (future, if needed)

When the label vocabulary grows to require namespacing:

1. File a tracking issue for the migration sweep
2. Create namespaced label (e.g., `status:blocked`) and apply alongside the flat label on existing issues
3. Allow ~2 weeks for any automation to switch over
4. Remove the flat label
5. Update this doc with the new canonical

Don't rename the flat label in place; aliasing during transition preserves history and reduces coordination cost.

---

## Cross-references

- #983 CONTEXT-BLOCKED (the issue this convention unblocks): `https://github.com/mediajunkie/piper-morgan-product/issues/983`
- PM disposition memo (2026-05-05): `mailboxes/arch/inbox/memo-lead-to-arch-cc-ceo-pa-983-blocked-label-convention-2026-05-05.md`
- Architect concurrence (2026-05-10): `mailboxes/lead/inbox/memo-arch-to-lead-cc-ceo-pa-exec-bundled-response-935-936-983-1010-2026-05-10.md`
- M2f-E post-floor-coverage cohort: `docs/internal/planning/m2-structure.md` (when M2f-E walks)

— Lead Developer, 2026-05-10
