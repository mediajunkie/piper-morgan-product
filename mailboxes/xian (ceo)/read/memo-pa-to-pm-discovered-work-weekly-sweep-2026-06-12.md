---
from: PA (Piper Alpha)
to: CEO (xian)
date: 2026-06-12
subject: Discovered-work weekly sweep — Fri 6/12 results (146 open; 0 high/crit unassigned ✅; 2 new stale-high)
priority: standard
response-requested: none — informational; PM action optional on stale-high flags
---

# Discovered-work weekly sweep — Friday 2026-06-12

**Vs. prior sweep (Fri 6/5: 126 open, 8 unassigned, 5 stale-high)**

| Metric | This week | Change | Health |
|---|---|---|---|
| Total open | 146 | +20 | — |
| Unassigned | 6 → 0* | -8 | ✅ |
| High/crit unassigned | 0 | same | ✅ |
| Stale >14d high/crit | 7 | +2 | ⚠️ flag (see below) |
| New last 7d | 38 | — | — |

*6 unassigned all filed today (0 days old); assigned to mediajunkie during sweep triage.

## Standing stale-high/crit (all assigned to you)

**Unchanged from 6/5 — known roadmap, no action needed:**
- **#103** CONV-FEAT-PRIOR (304d) — M5 roadmap, unscheduled
- **#104** CONV-FEAT-ALLOC (304d) — M5 roadmap, unscheduled
- **#106** CONV-FEAT-STRAT (304d) — M5 roadmap, unscheduled  
- **#321** DATA-AUDIT-FIELDS (204d) — architecture backlog
- **#358** SEC-ENCRYPT-ATREST (204d) — security, assigned

**NEW entrants this week (just crossed 14d threshold):**
- **[#1122](https://github.com/mediajunkie/piper-morgan-product/issues/1122)** MULTI-TURN-DOC-ANTECEDENT (17d) — the 'the doc'/'that one' antecedent regression. Lead Dev confirmed this is a known behavioral regression separate from model-ID issues (AAXT verified today). Assigned to you. Not neglected — just aging.
- **[#1129](https://github.com/mediajunkie/piper-morgan-product/issues/1129)** SLACK-INBOUND-STRUCTURAL (15d) — webhook mount removed by CORE. Assigned to you.

Both #1122 and #1129 are real work that's been properly filed; I'm flagging them because they just crossed the "worth PM attention" threshold, not because they're at risk of being lost.

## Today's new issues (filed 6/12, just assigned)

These came in today — all assigned to mediajunkie during triage:
- **#1199** Unify two default-repo/preference stores (github_preferences.json vs UserPreferenceManager)
- **#1198** Robot-script audit: 5+ ungated false promises ('I'll remember', 'I'll keep an eye on things')
- **#1197** Piper's floor voice uses banned sycophancy
- **#1196** Consciousness morning-greeting fabricates calendar access
- **#1195** Audit: built-but-unwired user-facing surfaces (PlaceService, AutonomousExecutor, KeyAuditService)
- **#1193** session_scope() never commits despite docstring — silent write-loss

#1193 + #1195 look load-bearing; the others are quality/honesty fixes. All assigned to you for now — Lead Dev or whoever filed them can take ownership as prioritized.

## Overall health: HEALTHY

0 high/crit unassigned = clean triage hygiene. The +20 total is consistent with a heavy Lead Dev week (38 new issues in 7 days). Stale count is driven by long-tail M3/M5 backlog, not neglect.

— PA (Piper Alpha), 2026-06-12 ~10:20 PT
