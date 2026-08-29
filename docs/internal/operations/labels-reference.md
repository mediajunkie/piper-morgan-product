# GitHub Labels Reference

**Status**: Canonical labels and conventions for the Piper Morgan repository.
**Last updated**: 2026-05-11 (corrected — supersedes May 10 draft)
**Owner**: Lead Developer (ships); Architect (consults on structural decisions)

---

## Convention: namespaced labels with space delimiter

The project's existing label vocabulary is **already namespaced** using the `{category}: {value}` pattern with a literal space:

- `priority: critical | high | medium | low`
- `component: database | workflow | integration | ui | api | knowledge | ai`
- `status: blocked | needs-implementation | needs-improvement`
- `size: small | medium | large`
- `type: research`

New labels in this vocabulary should follow the same `{category}: {value}` shape. Cross-references in docs or code that name these labels should match exactly (with the space).

---

## Canonical labels

### `status: blocked` — canonical 2026-05-11

**Decision**: PM disposition 2026-05-05 (#983 label-convention memo); Architect concurrence + correction 2026-05-10/11 (the May 10 bundled-response had recommended flat `blocked` in error; corrected May 10 memo `memo-arch-to-lead-cc-ceo-pa-exec-1075-filed-plus-983-label-correction` recognized the existing namespaced convention and updated the recommendation to `status: blocked` with the space).

**Semantics**: Issue is blocked on an external dependency or upstream decision — not actionable as currently scoped. Use sparingly; prefer a comment explaining what's blocking with cross-reference to the blocking issue.

**Programmatic use**: `services/intent_service/context_assembler.py` (when #983 ships) will query for issues with this label to surface "blocked items" in floor context for PRIORITY queries.

**Not in scope (filed separately if needed)**: `status: needs-review`, `status: waiting-for`, `status: awaiting-input`. These are distinct concepts that warrant their own values rather than additional rows in the `status: blocked` bucket. If filed, they should follow the existing namespace.

### Existing labels (canonical by use)

Labels in the `priority:` / `component:` / `status:` / `size:` / `type:` namespaces (listed above) are canonical. Single-word labels like `bug`, `enhancement`, `documentation`, `technical-debt`, `epic`, `architecture`, sub-epic labels (`M2e`, `M2f`, `M2g`), and helper labels (`good first issue`, `help wanted`) are also canonical and predate the namespaced convention.

A few legacy labels (`P1`, `priority-medium`, `milestone`, `piper-morgan`, `learning`, etc.) appear in `gh label list` without descriptions — these are legacy from earlier sprint structures and should not be propagated; new issues should use the namespaced versions where applicable.

---

## Pattern-063 / Methodology-24 note

The flat-vs-namespaced choice was the subject of a small parallel-authoring-drift instance May 10 (Architect's bundled response recommended flat `blocked` without verifying the existing namespace). Self-caught on May 10 PM by Architect during #1075 filing; revised recommendation routed via this doc. The correction is the methodology working as designed — Branch-or-Anchor diagnostic surfaced the drift on re-read; no harm done.

---

## Cross-references

- #983 CONTEXT-BLOCKED (the issue this convention serves): `https://github.com/mediajunkie/piper-morgan-product/issues/983`
- PM disposition memo (2026-05-05): `mailboxes/arch/inbox/memo-lead-to-arch-cc-ceo-pa-983-blocked-label-convention-2026-05-05.md`
- Architect bundled-response (2026-05-10): `mailboxes/lead/read/memo-arch-to-lead-cc-ceo-pa-exec-bundled-response-935-936-983-1010-2026-05-10.md` (recommended flat `blocked` — superseded)
- Architect correction (2026-05-10 follow-up, received 2026-05-11): `mailboxes/lead/inbox/memo-arch-to-lead-cc-ceo-pa-exec-1075-filed-plus-983-label-correction-2026-05-10.md` (corrected to `status: blocked`)
- Pattern-063 Parallel-Authoring Drift: `docs/internal/architecture/patterns/pattern-063-parallel-authoring-drift.md`
- Methodology-24 Branch-or-Anchor: methodology corpus

— Lead Developer, 2026-05-11 (initial: 2026-05-10; corrected: 2026-05-11)
