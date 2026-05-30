# Memory Frontmatter Temporal Validity Fields — Spec (Draft v0.3)

**Status**: Draft v0.3 — **design questions resolved** 2026-05-30 PM directives: Q1 confirmed (add YAML frontmatter block to BRIEFING-CURRENT-STATE; already shipped via May 28 briefing pilot `b40876b87`); **Q2 RESOLVED — drop memos from scope** ("I never asked for that"). The temporal-validity work targets **standing reference documents only**, not point-in-time documents. v0.2 (May 28) corrected the referent after reading the full #972 issue body. v0.1 (May 27) wrongly assumed the auto-memory `metadata: type:` frontmatter shape.
**Issue**: #972 MEM-TEMPORAL (authored by PM 2026-04-13).
**Disposition**: ship-and-adopt with rename escape hatch (CIO ratified 2026-05-25; PM can override if Janus near-term). Standing-doc scope only per 2026-05-30 PM directive.
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

## ✅ Design questions — RESOLVED 2026-05-30

PM dispositioned both open questions:

1. **BRIEFING-CURRENT-STATE frontmatter shape**: **RESOLVED — add a YAML block.** Already shipped via the May 28 briefing YAML-upgrade pilot (commit `b40876b87`): BRIEFING-CURRENT-STATE now opens with `--- type: briefing / title: ... / valid_from: "2025-09-30" / last_updated: "2026-05-28" ---`. The `valid_from` carries the temporal-validity field per this spec; the `**Last Updated**:` line in the body remains as a human-readable freshness marker (no conflict).

2. **Memo `valid_from`/`ended` semantics**: **RESOLVED — DROP memos from scope.** PM 2026-05-30: *"let's drop them— i never asked for that."* Memos are point-in-time documents (already dated via the `date:` frontmatter field, never "expire," exist as historical record); the temporal-validity concept doesn't apply. The targets of #972 are **standing reference documents only**: briefings, methodology docs, templates, trackers, session-log instructions — NOT memos.

3. **≥3 example docs (the AC threshold)**: **substantially complete via the May 28 pilot.** All 17 briefing docs received YAML frontmatter with `valid_from` (commit `b40876b87`), well exceeding the ≥3 examples AC.

## Integration plan (remaining #972 work)

- [x] Resolve design questions 1-2 (PM 2026-05-30)
- [x] Update BRIEFING-CURRENT-STATE with the temporal field (May 28 pilot `b40876b87`)
- [x] ≥3 example docs (17 briefings via pilot)
- [ ] Session-log instructions — decide whether to add `valid_from` convention (session logs are also point-in-time like memos; recommend dropping by the same logic — flagging for PM ratification rather than guessing)
- [ ] Continue the broader YAML-frontmatter upgrade to other standing-doc classes already queued in standing-items (ADRs 69, Patterns 80, Methodology 52, .serena/memories 29)
- [ ] Cross-project alignment ping to CIO once the spec firms (Janus may converge later)
- [ ] Close #972 once session-log-instructions disposition lands

## Other open questions (lower-stakes)

- **Backfill policy**: forward-only convention (don't backfill old docs) — per `feedback_calendar_workdate_is_source_work_period` ("forward-looking; don't backfill earlier drift"). Same shape.
- **Enforcement layer**: convention (document it) vs. tooling (a check script). Convention is lighter to start.

## What this spec IS

- v0.3 schema with the resolved target (**standing reference docs only** — memos dropped per PM 2026-05-30)
- Field semantics + rename escape hatch
- ≥3-examples AC satisfied via the May 28 briefing YAML pilot

## What this spec is NOT

- Not coordinated with Janus yet — ship-and-adopt allows landing the schema first
- Not pre-committing field names — `valid_from`/`ended` per the issue + audit; CIO ratified the rename escape hatch
- Not applying to point-in-time docs — memos dropped (2026-05-30); session-log instructions flagged for the same disposition

## Cross-references

- #972 issue (PM-authored; body names the referent): https://github.com/mediajunkie/piper-morgan-product/issues/972
- Lead Dev May 17 Phase 0 audit: `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- CIO ratification (ship-and-adopt + rename escape hatch): `mailboxes/docs/read/memo-cio-to-docs-cc-pm-mem-972-ship-and-adopt-with-rename-escape-hatch-pm-can-override-if-janus-near-term-2026-05-25.md`
- v0.1 → v0.2 correction driven by: CLAUDE.md §"Verify First, Create Second" (read whole source artifact; commit `5e2651c37`) + `feedback_investigate_before_extending_all_work`

— Documentation Management, v0.2 2026-05-28 (referent corrected after reading full #972 body)
