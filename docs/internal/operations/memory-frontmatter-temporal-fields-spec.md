# Memory Frontmatter Temporal Validity Fields — Spec (v0.4)

**Status**: v0.4 — field-schema reconciled with CIO's ratified 4-field convention (PM ratified 2026-06-13 via `mem-972-temporal-validity-scoping-plan-cio-2026-06-12.md`). v0.3 (2026-05-30) used `valid_from`+`ended`; v0.4 adopts `valid_from`+`valid_until`+`superseded_by`+`last_verified` (CIO-ratified). `ended` dropped; `last_verified` added as expected field. Janus/Klatch alignment resolved via direct dinp read (CIO, 2026-06-15): `valid_from`+`last_verified` match exactly; `valid_until` vs Janus `ended`/`validUntil` is the one open question — PM bridge to Daedalus pending.
**Issue**: #972 MEM-TEMPORAL (authored by PM 2026-04-13).
**Disposition**: ship-and-adopt; `valid_until` name ratified by CIO (recommends keeping over `ended` for clarity); PM cross-project bridge to Daedalus may rename to match Janus.
**Owner**: Documentation Management (Docs); CIO co-owner (P1 shipped: `scripts/check-staleness.py`).

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

## Schema — flat top-level frontmatter keys (4-field, PM-ratified 2026-06-13)

The target docs use **flat YAML frontmatter**, NOT a nested `metadata:` block. Four fields:

```yaml
---
[existing frontmatter keys...]
valid_from: 2026-05-25       # expected on operating docs
last_verified: 2026-06-15    # expected on operating docs; when content was last confirmed current
valid_until: 2026-07-01      # optional; when content stops being valid / review horizon
superseded_by: path/to/new-doc.md  # optional; pointer to what replaces this
---
```

| Field | Required? | Meaning |
|---|---|---|
| `valid_from` | **expected** | when the fact/guidance became true; does NOT change on edit |
| `last_verified` | **expected** | when content was last *confirmed current* (distinct from `last_updated` = last *edited*); drives `check-staleness.py` — catches silent staleness |
| `valid_until` | optional | when content stops being valid / a review horizon; absent = "current until superseded" |
| `superseded_by` | optional | path or ID of the replacement doc; the load-bearing field — a stale doc that names its replacement is self-correcting |

### Detection mechanism — `scripts/check-staleness.py` (CIO-built, P1 shipped)

`check-staleness.py` (committed by CIO, 2026-06-15) warns on:
- Any doc past its `valid_until`
- Any doc whose `last_verified` is older than its staleness horizon
- Any doc with `superseded_by` set that is still being referenced

Freshness check uses `last_verified` first; falls back to `last_updated` if `last_verified` absent. **Severity**: warn + capture-as-tracked-task + fix-asap (PM-ratified 2026-06-13; stronger than warn-only).

### Open question — `valid_until` vs `ended` (PM decision pending)

Janus/Klatch alignment (CIO, 2026-06-15): `valid_from`+`last_verified` match exactly. The one divergence: this spec uses `valid_until`; Janus synthesis uses `ended` (with `validUntil` as a variant). CIO recommendation: **keep `valid_until`** (clearer symmetric pair with `valid_from`; Janus usage is inconsistent). PM cross-project bridge to Daedalus needed before finalizing — accept `ended` only if Daedalus has shipped it irreversibly.

## Examples (corrected to 4-field schema)

### Standing doc — BRIEFING-CURRENT-STATE

```yaml
---
type: briefing
title: "BRIEFING-CURRENT-STATE: Where We Are Right Now"
valid_from: 2026-05-28
last_updated: 2026-06-14
last_verified: 2026-06-15
---

# BRIEFING-CURRENT-STATE.md - Where We Are Right Now
...
```

*(Note: briefings from the May 28 pilot carry `valid_from`+`last_updated`; `last_verified` should be added as they are next touched.)*

### Essential briefing — active, no supersession

```yaml
---
type: briefing
title: "BRIEFING-ESSENTIAL-DOCS"
valid_from: 2026-04-26
last_verified: 2026-06-12
---
```

### Superseded doc — archived, names replacement

```yaml
---
type: briefing
title: "BRIEFING-CURRENT-STATE v2"
valid_from: 2026-03-01
valid_until: 2026-05-28
superseded_by: docs/briefing/BRIEFING-CURRENT-STATE.md
---
```

*(Memos are point-in-time documents — already dated via `date:` field; temporal-validity fields do NOT apply to memos. PM 2026-05-30: "I never asked for that.")*

## ✅ Design questions — RESOLVED 2026-05-30

PM dispositioned both open questions:

1. **BRIEFING-CURRENT-STATE frontmatter shape**: **RESOLVED — add a YAML block.** Already shipped via the May 28 briefing YAML-upgrade pilot (commit `b40876b87`): BRIEFING-CURRENT-STATE now opens with `--- type: briefing / title: ... / valid_from: "2025-09-30" / last_updated: "2026-05-28" ---`. The `valid_from` carries the temporal-validity field per this spec; the `**Last Updated**:` line in the body remains as a human-readable freshness marker (no conflict).

2. **Memo `valid_from`/`ended` semantics**: **RESOLVED — DROP memos from scope.** PM 2026-05-30: *"let's drop them— i never asked for that."* Memos are point-in-time documents (already dated via the `date:` frontmatter field, never "expire," exist as historical record); the temporal-validity concept doesn't apply. The targets of #972 are **standing reference documents only**: briefings, methodology docs, templates, trackers, session-log instructions — NOT memos.

3. **≥3 example docs (the AC threshold)**: **substantially complete via the May 28 pilot.** All 17 briefing docs received YAML frontmatter with `valid_from` (commit `b40876b87`), well exceeding the ≥3 examples AC.

## Integration plan (remaining #972 work)

- [x] Resolve design questions 1-2 (PM 2026-05-30)
- [x] Update BRIEFING-CURRENT-STATE with the temporal field (May 28 pilot `b40876b87`)
- [x] ≥3 example docs (17 briefings via pilot)
- [x] 4-field schema ratified (CIO scoping plan, PM 2026-06-13)
- [x] Janus/Klatch alignment investigation (CIO, 2026-06-15 — `valid_from`+`last_verified` match; `valid_until`/`ended` pending PM bridge)
- [x] `check-staleness.py` lint shipped (CIO, P1 — warn+capture-task+fix-asap behavior)
- [x] Field-name reconciliation — Docs spec updated to v0.4 (this commit)
- [ ] **Session-log instructions** — recommend DROP by same point-in-time logic as memos (session logs are dated, ephemeral, never "expire"). Flagging for PM ratification rather than guessing.
- [ ] **Briefings `last_verified` stamp** — 17 briefings have `valid_from`+`last_updated` from May 28 pilot; add `last_verified` as touched (not a bulk-stamp — `last_verified=today` everywhere would lie about re-verification)
- [ ] **Other standing-doc classes** — ADRs (69), Patterns (80), Methodology (52): add `valid_from`+`last_verified` opportunistically; no bulk-stamp
- [ ] **`valid_until` vs `ended` PM decision** — PM cross-project bridge to Daedalus/Janus needed; hold until that bridge exists
- [ ] Close #972 once session-log-instructions disposition lands + PM confirms `valid_until` name

## Other open questions (lower-stakes)

- **Backfill policy**: forward-only convention (don't backfill old docs) — per `feedback_calendar_workdate_is_source_work_period` ("forward-looking; don't backfill earlier drift"). Same shape.
- **Enforcement layer**: convention (document it) vs. tooling (a check script). Convention is lighter to start.

## What this spec IS

- v0.4 4-field schema, PM-ratified 2026-06-13: `valid_from`+`last_verified` (expected) + `valid_until`+`superseded_by` (optional)
- Aligned with CIO's ratified scoping plan (supersedes v0.3 `valid_from`+`ended` shape)
- Janus/Klatch alignment resolved: `valid_from`+`last_verified` exact match; `valid_until` pending PM bridge
- ≥3-examples AC satisfied via May 28 briefing YAML pilot (17 docs)
- Scope: **standing reference docs only** (briefings, methodology, ADRs, patterns, templates, session-log instructions) — NOT memos (point-in-time, already dated)

## What this spec is NOT

- Not finalizing `valid_until` vs `ended` — pending PM cross-project bridge to Daedalus
- Not authorizing bulk `last_verified` stamps — `last_verified=today` everywhere would lie; stamp only when actually re-verifying
- Not applying to memos (dropped PM 2026-05-30) or session logs (recommend same point-in-time drop — flagged for PM)

## Cross-references

- #972 issue (PM-authored; body names the referent): https://github.com/mediajunkie/piper-morgan-product/issues/972
- Lead Dev May 17 Phase 0 audit: `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- CIO ratification (ship-and-adopt + rename escape hatch): `mailboxes/docs/read/memo-cio-to-docs-cc-pm-mem-972-ship-and-adopt-with-rename-escape-hatch-pm-can-override-if-janus-near-term-2026-05-25.md`
- v0.1 → v0.2 correction driven by: CLAUDE.md §"Verify First, Create Second" (read whole source artifact; commit `5e2651c37`) + `feedback_investigate_before_extending_all_work`

— Documentation Management, v0.3 2026-05-30 (referent + design questions resolved); v0.4 2026-06-15 (field-schema reconciled with CIO ratified 4-field plan; Janus alignment incorporated)
