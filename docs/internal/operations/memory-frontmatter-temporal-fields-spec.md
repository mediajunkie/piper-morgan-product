# Memory Frontmatter Temporal Validity Fields — Spec (Draft v0.1)

**Status**: Draft v0.1, partial-progress per v0.6.3 IDLE-advances-low-priority-work rule applied during Docs Fire 6 (2026-05-27 ~18:35 PT).
**Issue**: #972 MEM-TEMPORAL
**Disposition**: ship-and-adopt with rename escape hatch (CIO ratified 2026-05-25; PM can override if Janus near-term).
**Owner**: Documentation Management (Docs).

---

## Purpose

Add explicit temporal-validity fields to memory file frontmatter so that:
1. Memory files carry their own "valid since" timestamp without requiring git log archaeology.
2. Memory files can be marked invalid without deletion (preserving audit trail) via an optional `ended` field.
3. Tooling can filter active vs. retired memories programmatically.
4. Cross-project compatibility with Janus's parallel temporal-validity structure (per Lead Dev May 17 Phase 0 audit Q4).

## Schema

Memory file frontmatter gains two new optional fields under `metadata`:

```yaml
---
name: kebab-slug
description: one-line summary
metadata:
  type: user|feedback|project|reference
  valid_from: 2026-05-25     # ISO 8601 date; required for new memories from spec-adoption forward
  ended: 2026-06-15          # ISO 8601 date; optional; populate when memory becomes invalid
---
```

### Field semantics

**`valid_from`** (required for new memories from spec-adoption forward; backfill optional for existing):
- ISO 8601 date (YYYY-MM-DD).
- The date the memory's content first applied / was first banked.
- For memories pinned from a specific PM directive: the date of the directive.
- For long-running observations: the date the pattern was first noticed.
- Does NOT change when the memory is edited (it's the *original* validity start).

**`ended`** (optional; populate at retirement):
- ISO 8601 date (YYYY-MM-DD).
- The date the memory's content stopped being valid / the memory was retired.
- Memory file is NOT deleted — preserved for audit trail.
- Add a brief note in the body explaining what superseded it.
- Active memories have NO `ended` field (or empty value).

### Rename escape hatch (per CIO ratification)

If Janus's Klatch Step 10 Phase 1 lands with different field names (e.g., `effective_from` / `invalidated`), rename is mechanical (`sed` across `~/.claude/projects/.../memory/*.md`). Schema is small enough to migrate cheaply.

## Examples

### New memory (active)

```yaml
---
name: docs-merge-keeper-sweep-cadence
description: Docs runs merge-keeper sweep daily to catch stranded session logs.
metadata:
  type: reference
  valid_from: 2026-05-27
---
```

### Retired memory

```yaml
---
name: claude-desktop-as-primary-surface
description: Claude Desktop is the primary surface for substantive role work.
metadata:
  type: reference
  valid_from: 2026-03-15
  ended: 2026-04-26
---

[Body content...]

**Retirement note** (2026-04-26): superseded by leadership migration to Claude Code. All seven leadership roles + Lead Dev + Docs on Code by 2026-04-26. See `docs/briefing/ROSTER.md` for current surface assignments.
```

## Integration plan (remaining work)

This spec is the schema. Full #972 deliverable adds these integration points:

- [ ] Update `BRIEFING-CURRENT-STATE.md` template to include `valid_from` field
- [ ] Update memo format guide (or wherever the template lives — TBD)
- [ ] Update session log instructions to reference temporal validity
- [ ] Update ≥3 existing memory files as examples (backfill `valid_from` where confidently knowable; leave blank where date is fuzzy)
- [ ] Cross-project alignment ping to CIO once spec firms (per "ship-and-adopt" disposition; Janus may converge later)

## Open questions

1. **Backfill policy for existing memories**: forward-only convention (don't backfill old memories) — per the `feedback_calendar_workdate_is_source_work_period` pattern, which adopted "forward-looking convention; don't backfill earlier drift." Same shape.
2. **Whose date for backfill**: when backfilling is voluntary, use the memory file's git first-commit date as default proxy for `valid_from`. Mechanical via `git log --diff-filter=A --format=%ai`.
3. **Where to enforce the field**: tooling layer or convention layer? Convention layer is lighter (just document); tooling layer would be a script that checks new memory files for `valid_from` presence.
4. **Janus alignment ping cadence**: ping CIO after spec lands; CIO reaches out to Janus if their parallel work has firmed.

## What this spec IS

- v0.1 schema definition for the two new frontmatter fields
- Examples + integration-plan checklist for remaining #972 work
- Partial-progress (#972 is ~3-5 hr full work; this spec is ~30 min)

## What this spec is NOT

- Not the final integration into other surfaces (BRIEFING / memo guide / session log instructions / example backfills) — that's the next ~2-4 hr of work
- Not coordinated yet with Janus — ship-and-adopt disposition allows landing this first
- Not pre-committing to specific field names — `valid_from` + `ended` per Lead Dev May 17 audit guess; CIO ratified the rename escape hatch

## Cross-references

- Lead Dev May 17 Phase 0 audit: `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- CIO ratification (ship-and-adopt with rename escape hatch): `mailboxes/docs/read/memo-cio-to-docs-cc-pm-mem-972-ship-and-adopt-with-rename-escape-hatch-pm-can-override-if-janus-near-term-2026-05-25.md`
- Docs lane-acceptance: `mailboxes/docs/sent/memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md`
- #972 issue: https://github.com/mediajunkie/piper-morgan-product/issues/972

— Documentation Management, 2026-05-27 ~18:40 PT (partial-progress per v0.6.3 IDLE-advances-low-priority-work; Docs Fire 6)
