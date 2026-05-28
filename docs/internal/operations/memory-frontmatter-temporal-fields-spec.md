# Memory Frontmatter Temporal Validity Fields — Spec (Draft v0.2)

**Status**: Draft v0.2 — **referent corrected** 2026-05-28 after reading the full #972 issue body. v0.1 (May 27) wrongly assumed the auto-memory `metadata: type:` frontmatter shape; v0.2 targets the institutional-memory documents the issue body actually names.
**Issue**: #972 MEM-TEMPORAL (authored by PM 2026-04-13).
**Disposition**: ship-and-adopt with rename escape hatch (CIO ratified 2026-05-25; PM can override if Janus near-term).
**Owner**: Documentation Management (Docs).

---

## Correction note (v0.1 → v0.2)

v0.1 assumed "memory files" meant files with a `metadata: type: user|feedback|project|reference` block (the personal Claude auto-memory shape). **That was wrong** — read in isolation from the AC line. The #972 issue **body** (PM, Apr 13) says:

> *"Start with BRIEFING-CURRENT-STATE and memos. This is a convention change, not code — add fields to frontmatter, update templates and session-log instructions."*

So **"memory files" = the institutional-memory documents** that carry (or should carry) frontmatter: BRIEFING-CURRENT-STATE, inter-agent memos, templates, session-log instructions. NOT `.serena/memories/` (plain markdown), NOT personal Claude auto-memory (outside repo).

## Purpose

Add explicit temporal-validity fields (`valid_from`, optional `ended`) to the frontmatter of institutional-memory documents so that:
1. A standing document carries its own "valid since" date without git-log archaeology.
2. A document can be marked stale/superseded without deletion (audit trail preserved) via `ended`.
3. Agents distinguish current facts from stale ones at read time; retrieval can deprioritize expired entries.
4. Cross-project compatibility with Janus's parallel temporal-validity structure (Klatch Step 10 Phase 1).

## Schema — flat top-level frontmatter keys

The target docs use **flat YAML frontmatter** (memos: `from`/`to`/`date`/`subject`), NOT a nested `metadata:` block. So the new fields are flat top-level keys:

```yaml
---
[existing frontmatter keys...]
valid_from: 2026-05-25     # ISO 8601 date; when the content's validity began
ended: 2026-06-15          # ISO 8601 date; optional; when content went stale/superseded
---
```

### Field semantics

**`valid_from`** (ISO 8601 YYYY-MM-DD): the date the document's content first applied. Does NOT change on edit (it's the original validity start). For a standing doc, the date the standing state was established.

**`ended`** (ISO 8601 YYYY-MM-DD; optional): the date the content stopped being valid / was superseded. Document is NOT deleted (audit trail). Add a body note explaining what superseded it. Active docs have no `ended`.

### Rename escape hatch (per CIO ratification)

If Janus's Klatch Step 10 Phase 1 lands with different field names (e.g., `effective_from` / `invalidated`), rename is a mechanical `sed` sweep. Schema is small enough to migrate cheaply.

## Examples (corrected to actual target shapes)

### Standing doc — BRIEFING-CURRENT-STATE (frontmatter added)

```yaml
---
valid_from: 2026-05-28
---

# BRIEFING-CURRENT-STATE.md - Where We Are Right Now
...
```

### Inter-agent memo (flat frontmatter extended)

```yaml
---
from: Docs (Documentation Management)
to: CIO (Chief Innovation Officer)
date: 2026-05-28
subject: ...
valid_from: 2026-05-28
---
```

## ⚠️ Open design questions — MUST resolve before example backfills (do NOT guess)

The #972 body names the target ("BRIEFING-CURRENT-STATE and memos") but leaves these unresolved. Per the investigate-before-extending + no-flattened-commands disciplines, flagging rather than guessing:

1. **BRIEFING-CURRENT-STATE has NO YAML frontmatter today** — it opens with an H1 + blockquote and carries a markdown `**Last Updated**:` line in the body. Does #972 mean (a) add a YAML frontmatter block to it, or (b) the existing "Last Updated" convention already serves the temporal-validity purpose and `valid_from` is redundant there? **Needs PM/cohort decision.**

2. **Memo `valid_from`/`ended` semantics are questionable** — memos are point-in-time communications, already dated (`date:` field), and don't "expire" (they're historical record). Does `valid_from` on a memo just duplicate `date:`? Does `ended` even apply? The temporal-validity concept fits STANDING docs (BRIEFING, methodology, templates, trackers) far better than point-in-time memos. The issue says "start with memos" but the semantics may not transfer. **Needs PM/cohort decision: is the real target standing reference docs, with memos a misfit?**

3. **Which ≥3 docs for the examples** — depends on resolving #1 + #2. If standing-docs-only: BRIEFING-CURRENT-STATE + 2 methodology docs / templates. If memos included: BRIEFING + 2 recent memos.

## Integration plan (remaining #972 work, gated on the design questions above)

- [ ] Resolve open design questions 1-2 (PM/cohort)
- [ ] Update BRIEFING-CURRENT-STATE with the temporal field (shape per Q1 resolution)
- [ ] Update memo format guide / template (per Q2 resolution)
- [ ] Update session-log instructions to reference temporal validity
- [ ] Update ≥3 example docs (per Q3 resolution)
- [ ] Cross-project alignment ping to CIO once spec firms (Janus may converge later)

## Other open questions (lower-stakes)

- **Backfill policy**: forward-only convention (don't backfill old docs) — per `feedback_calendar_workdate_is_source_work_period` ("forward-looking; don't backfill earlier drift"). Same shape.
- **Enforcement layer**: convention (document it) vs. tooling (a check script). Convention is lighter to start.

## What this spec IS

- v0.2 schema with the **corrected** target (institutional-memory docs per issue body, flat frontmatter keys)
- Design questions the issue body doesn't resolve, flagged for PM/cohort decision BEFORE backfills
- Field semantics + rename escape hatch

## What this spec is NOT

- Not executing the backfills — blocked on design questions 1-2 (BRIEFING frontmatter shape + memo semantics)
- Not coordinated with Janus yet — ship-and-adopt allows landing the schema first
- Not pre-committing field names — `valid_from`/`ended` per the issue + audit; CIO ratified the rename escape hatch

## Cross-references

- #972 issue (PM-authored; body names the referent): https://github.com/mediajunkie/piper-morgan-product/issues/972
- Lead Dev May 17 Phase 0 audit: `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- CIO ratification (ship-and-adopt + rename escape hatch): `mailboxes/docs/read/memo-cio-to-docs-cc-pm-mem-972-ship-and-adopt-with-rename-escape-hatch-pm-can-override-if-janus-near-term-2026-05-25.md`
- v0.1 → v0.2 correction driven by: CLAUDE.md §"Verify First, Create Second" (read whole source artifact; commit `5e2651c37`) + `feedback_investigate_before_extending_all_work`

— Documentation Management, v0.2 2026-05-28 (referent corrected after reading full #972 body)
