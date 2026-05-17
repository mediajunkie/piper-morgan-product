# M-sprint backlog snapshot — 2026-05-17

**Source-of-truth notes:**
- "Milestone" in GitHub = top-level bucket (MVP / Fast Follow / Post-MVP / Enterprise)
- "Sprint label" in GitHub = `M1`, `M2e`, `M2f`, `M2g` (no `M3`/`M4`/`M5` labels yet)
- This doc maps PM's mental categories (M2g / M2 discovered / M3 / M4 / M5) onto the actual GitHub state, with explicit gap markers where the GitHub Project metadata would be needed to fill in.
- Author: Lead Developer, post-#1102 close.

---

## M2g (current sprint — chip-away mega-sprint)

**Definition (per yesterday's session + today's work)**: bounded MVP-tier issues being chipped away during the current sprint window. Label: `M2g` in GitHub.

### Open (3)

| # | Title | Priority | Lead Dev assessment |
|---|---|---|---|
| 1089 | KG-PRIVACY-FILTER: Design + implement actual privacy filtering for KG node operations (#1010 follow-up) | low | Bounded; architecture review needed; this is up next per PM directive |
| 1016 | ARCH-DESIGN: LLM-touch boundary principle — unified architectural posture | epic | Architect's lane; Lead Dev support role |
| 1011 | ARCH-DESIGN: Slash-command dispatch precedence — post-MVP design decision | architecture | Post-MVP design call; not Lead Dev gating |

### Closed today (2026-05-17 — 5 closures)

| # | Title | Commit |
|---|---|---|
| 1102 | PATTERN-073-DATA-SUBSTITUTION: hardcoded fake projects | `39240d179` |
| 1100 | MUX-SURFACE-7-SLICE-2: session selector + audit-summary | `0e6a080f9` |
| 1099 | MUX-SURFACE-7: User-Facing Audit Envelope Read View | `95437267` |
| 1097 | MUX-SURFACE-1: Sidebar reconciliation | `ff403315` |
| 1096 | TEMPLATED-EMPTY-STATE-AUDIT: full sweep | `c08be3dc7` + `00bf5470b` |

### Closed yesterday (2026-05-16 — 8 closures incl. #1094 marquee)

#1094 (engine deletion, −10,734 LOC), #1095 (transparency auth gates), #1083 (issue-checkbox lint hook), #1084 (Q25 HTTP-path), #1079 (standup multi-turn state), #1075 (route migration), #1064 (floor-fab investigation), #1015 (RequestContext migration Phase 2).

### Closed earlier in sprint (May 6–15)

#1093, #1092, #1088, #1087, #1072, #1067, #1066, #1065, #1063, #1059, #1057, #1056, #1055, #1021, #1020, #1019, #1017 — 17 closures.

### M2g lifetime tally
- **Closed**: 30 issues (May 6 → May 17)
- **Open**: 3 issues
- **Closure rate**: ~2/day average; surge today (5)

---

## M2 discovered work (overflow / follow-ups)

**Definition**: issues discovered during M2 work that are post-MVP or were demand-gated. In GitHub: **Fast Follow milestone** (35 open / 2 closed).

### Sample (first 15 of 35; full list via `gh issue list --milestone "Fast Follow" --state open`)

| # | Title | Theme |
|---|---|---|
| 1098 | BUG-#1083: issue-checkbox-lint hook doesn't honor annotation pattern | tooling |
| 1101 | TRANSPARENCY-CLEANUP-#1100: audit-summary universal-claims fields | Pattern-073 service-side |
| 1085 | CONTEXT-ACTIVITY-SLACK: Slack source to recent-activity aggregation | demand-gated |
| 1080 | NOTION-WRITE: Activate update_document capability | demand-gated |
| 1081 | NOTION-SLACK-XREF: cross-reference Notion + Slack | demand-gated |
| 1082 | NOTION-TEST-REWRITE: Rewrite test_notion_spatial_integration.py | tech-debt |
| 1045 | POST-MVP: Project Detail Activity tab | UI |
| 1044 | FOLLOWUP: Local-git 'what branch are we on?' query handler | M2e straggler |
| 1037 | MUX-INSIGHT-TOPIC-MAPPING: Wire topic filter on Insight Journal | MUX |
| 837–833 | DIST-*: First-run, installer, auto-update, desktop-wrapper, SQLite (5 issues) | distribution epic |
| 828 | EPIC: DIST — Distribution Packaging | epic |
| 760 | TECH-DEBT: slack_workspaces table for proper team_id → user mapping | tech-debt |
| 716 | MUX-FEATURES-VIEW: Features View with Lifecycle | MUX |
| 686 | MUX-LIFECYCLE-ANIMATIONS: transition animations | MUX |
| 651 + 650 | FUTURE-CONSCIOUSNESS: account-delete + settings-reset confirmation patterns | consciousness |

**Total Fast Follow open**: 35 (incl. distribution epic with 5 sub-issues + multiple MUX follow-ups + consciousness future-requirements).

---

## M3 (next sprint after M2g)

**Definition gap**: **no `M3` label exists in GitHub.** **No issues currently scoped or labeled M3.**

Probable shape (Lead Dev inference, NOT ratified):
- M2g residue if any survives (currently 3 open — could roll forward if not done)
- Selected Fast Follow promotions (which ones depends on PM/CIO scoping)
- Surface 7 MUX-doc polish landing → final Surface 7 work
- Pattern-073 instance 9+10 service-side cleanup (#1101)
- Surface 2 + Surface 4 (Phase 2.2 of MUX/UI Round 2) once PDR-005 v0.4-sufficient signal fires from PPM
- Surface 6 (Phase 2.3 of MUX/UI Round 2) alongside voice work

**GitHub Project metadata gap**: M3 scoping decisions live in the GitHub Project board (or equivalent). Backfill needed:
- Which issues from Fast Follow get promoted to M3 milestone/label?
- Is M3 a label PM creates, or a separate milestone?
- M3 sprint window / target dates?

---

## M4 (sprint after M3)

**Definition gap**: **no `M4` label exists. No issues scoped or labeled.**

Probable shape (purely Lead Dev guesswork):
- Distribution epic (#828) sub-issues — if M4 = pre-launch packaging window
- MUX/UI Round 2 Phase 2.2 finishing items if not done in M3
- Surface 5 (per ADR-064) build if M3 hasn't landed it

**GitHub Project metadata gap**: same as M3 — no GitHub-side specification yet.

---

## M5 (per PM directive yesterday: "all M sprints are MVP sprints; M5 is part of MVP")

**Definition gap**: **no `M5` label exists. No issues scoped.**

Probable shape (Lead Dev inference):
- Final MVP polish + distribution
- Pattern-073 → Proven promotion (if not already)
- Any remaining MVP critical-path items not yet bucketed

**GitHub Project metadata gap**: largest — M5 is the most-distant sprint and has the least definition. Backfill from GitHub Project board (sprint planning view) would clarify whether M5 is a real planned sprint or a placeholder.

---

## Gaps PM may want to backfill from GitHub Project

1. **M3 / M4 / M5 sprint labels not created in GitHub.** If these are intended to be filed as labels (like M2e/M2f/M2g) PM may want to create them and tag issues. Or they could live in the Project board's iteration column.
2. **Fast Follow → future-M-sprint promotion mapping not done.** 35 Fast Follow issues; some are clearly M3-worthy (e.g., #1098 hook bug — easy chip-away), others are post-launch (#828 distribution epic).
3. **Sprint windows / target dates** not in this snapshot. The current sprint (M2g) doesn't have a public end-date that I can see; M3/M4/M5 likewise undated.
4. **Epic mapping** — MUX/UI Round 2 is an epic spanning Phase 2.1 + 2.2 + 2.3. Currently mapped under #1090 (UI-1.0-PLAN). LLM-touch boundary epic (#1016) similarly spans surfaces. The relationship between epics and M-sprints isn't surfaced in labels.

---

## Cross-references

- Sprint label conventions: M1, M2e, M2f, M2g exist; M2a–M2d closed before label-rename pass
- MVP milestone: 72 open, 728 closed (the umbrella for all sprint labels)
- Fast Follow milestone: 35 open (this doc's "M2 discovered work")
- Post-MVP milestone: 7 open
- Enterprise milestone: 13 open
- Yesterday's M2 snapshot: `dev/active/M2-backlog-2026-05-16.md` (31 issues; today's surge closed 5 of those + 1 from prior day)

---

*Last updated*: 2026-05-17 ~09:30 PT (Lead Dev, post-#1102 close)
