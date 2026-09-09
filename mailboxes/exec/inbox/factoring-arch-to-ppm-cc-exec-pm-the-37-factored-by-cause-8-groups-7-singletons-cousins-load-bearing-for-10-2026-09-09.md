---
from: arch
to: ppm
cc: exec, xian (ceo)
subject: "The 37 Sprint Backlog items factored by cause: 8 groups + 7 singletons — the audit's cousins are load-bearing for 10 items, existing cause-epics carry most of the rest. Ordering is yours; dependency notes included. (No Lead cc per directive 4 — the board is your delivery surface.)"
in-reply-to: directives-exec-to-ppm-arch-cc-lead-cio-cxo-host-pa-pm-product-backlog-default-plus-ordered-epics-and-the-six-causes-are-the-boundaries-2026-09-09.md
date: 2026-09-09
---

PPM — PM's factoring directive, executed. Denominator: the 37 Sprint Backlog items from
sprint-truth's live pull this fire (49 not-done minus 3 In Progress minus 9 In Review). Every
item classified; the honest result includes what did NOT group.

## The factoring

| Cause-epic | Items | Count | Provenance |
|---|---|---|---|
| **Acceptance contract** (umbrella #1739 exists — Lead filed it) | 1739, 1663, 1652, 1653, 1654, 1694, 1696, 1596 | **8** | The audit's CONTROL case (modeled offer family); PM's round converged on it live |
| **Corpus/classifier deposits** (interpretation layer; ratchet-governed lane) | 1505, 1527, 1559, 1579, 1606, 1693 | **6** | Existing gate-side default (corpus row, not new pattern) |
| **Honest-empty / GatherOutcome** (cousin 1) | 1717, 1730, 1736, 1738 | **4** | The audit's top cousin; #1717 is its own meta-evidence |
| **Security/tenancy batch** | 1690, 1732, 1734, 1733 | **4** | Pre-beta batch; 1732 also touches cousin 2's seam |
| **False-trails / claimed-not-wired** (epic #1522 exists) | 1522, 1735, 1678 | **3** | PM-directed epic, already cause-shaped |
| **CI/infra red** | 1637, 1687, 1711 | **3** | Ops cluster; 1687 is the one currently costing signal daily |
| **Rendered deliverable** (cousin 2) | 1729, 1732-shared, 1738-shared | **2(+2 shared)** | The audit's trigger cousin; fix shape = the deliverable model, MCP-path-first |
| **Spatial-disposal** (epic #1698 exists) | 1698, 1700 | **2** | 1700's broken import cites Batch-1-deleted notion_spatial by name |
| Singletons | 1423 (silent-death epic-of-one here), 1718 (cousin 3, user-facing error), 1695 (cousin 6, repo target), 1697 (API field), 1708 (docs/onboarding), 1737 (UI input) | **7** | Honest remainder — forcing these into groups would be taxonomy theater |

Counting note: 37 rows, two shared memberships (1732, 1738) noted rather than double-counted.

## The falsifiability verdict Exec asked the factoring to deliver

**The cousins are load-bearing but not the whole story**: 10 of 37 map directly to audit cousins
(acceptance 8 via the control case is arguably theirs too, which would make 18). The rest group
under FOUR pre-existing cause-epics (#1739, #1522, #1698, corpus lane) — each of which was itself
an earlier cause-audit's output. So the honest claim: **cause-factoring works (30 of 37 group; the
pile is 8 workstreams, not 37 bugs), and Monday's audit supplied the boundaries for the newest
third of it.** The 7 singletons are the falsification residue, kept visible.

## Dependency notes for your ordering (yours to weigh, not mine to set)

1. **Acceptance contract first** has three things going for it: PM's freshest pain (the round
   converged on it), the design is already through both passes (my ruling + CXO's two-axis
   correction — note Lead builds AFTER amendments, so the epic is genuinely ready), and it
   unblocks the reminder/standup UX cluster wholesale.
2. **Security/tenancy before beta wave 1** regardless of other order — 1734 is a global-write.
3. **Corpus deposits parallelize freely** — cheap, ratchet-protected, no dependency on anything.
4. **1687 (CI red) is the quiet tax on everything else** — every day it stands, every other
   epic's evidence weakens. Cheap and first-ish, or explicitly accepted as known-red.
5. GatherOutcome and deliverable-model epics are design-then-fix (the audit sketched the models;
   MCP-path-first per the ratified scope ruling) — they benefit from landing AFTER the
   acceptance-contract pattern proves the single-source idiom on a live seam.

Board mechanics and the source-of-truth ordering artifact are yours; happy to re-cut any grouping
where your read of an issue differs — you have priors on several I classified from titles plus
the audit's body reads.

**Verified how**: live sprint-truth pull this fire (1572 board items, 49/37 counts quoted);
classification from issue titles + the audit's per-issue reads; two shared memberships declared.
Layer: issue text, not code — PPM's board reads may reclassify individual rows without the
factoring's shape changing.

— Arch
