---
from: PA (Piper Alpha)
to: CEO (xian)
cc: Lead Developer
date: 2026-05-23
subject: M2 sprint convergence read — issue-count is close to closure; quality verification + M3-M5 are the load-bearing gates between here and beta
priority: standard — planning input, not action-required; consume at reunion-break cadence
response-requested: at your cadence; corrections to my read welcome; CC Lead Dev so they can flag-back if synthesis is off
---

# M2 sprint convergence read

## TL;DR

**Issue-count convergence**: M2 has 3 open issues across all sub-epics. 1 of those (#1089) is in active piecemeal-increment build (Lead started Increment 1 of 5 this morning, ~2-2.5 hr remaining at stated pace). 1 (#1016) is an architecture epic that may serve as a tracker rather than a closeable issue. 1 (#1011) is explicitly post-MVP per the briefing. **Plausible structural M2 close: Tue-Wed May 26-27.**

**Quality-gate convergence**: Latest canonical retest Run 9 (May 13) sat at **69.8% PASS** against the **≥75% PASS** north star. **No retest has run since May 13**, despite 15+ M2g closures in the May 15-17 window + #1085 slice 3 today. The quality gap could already have closed; we don't know. **Run 10 is the missing data point.**

**Year-anniversary beta (May 27/28)**: Not plausible. M3-M5 work hasn't started (M3/M5 placements landed May 5 but no shipping); the Phase A Gemma simulation harness (alpha-catch-22 reframe) isn't visibly in flight in the briefing or recent logs.

**Realistic beta vector**: Structural M2 close ~next week. Then a Run 10 canonical retest closes (or surfaces gaps in) the quality north star. Then M3-M5 work (PM-framed "much less onerous") plus Phase A simulation harness. **Weeks, not months — but not days.** Anchoring on a specific date is premature without a Run 10 data point and a Phase A status check.

## What I can attest from logs + GitHub + briefing

### M2 sub-epic state (cross-referencing m2-structure.md + briefing May 18 + GitHub state today)

| Sub-epic | Status | Source of truth |
|---|---|---|
| M2a Foundation Cleanup | ✅ DONE (10/10) Apr 11-14 | m2-structure.md + briefing |
| M2b Test Infrastructure | ✅ DONE (5/5) Apr 14-15 | m2-structure.md + briefing |
| M2c Conversational Depth | ✅ DONE (6/6) Apr 16 — Quality jumped to 72.1% post-#950 | m2-structure.md + briefing |
| M2d MUX Lifecycle | ✅ DONE (audit-cascade restructure May 2 + 9-issue ship May 6) | briefing (m2-structure.md is stale on this) |
| M2e Integrations | ✅ DONE | briefing |
| M2f Security + Infra | ✅ STRUCTURALLY COMPLETE EOD May 12 (Groups A+B+C+E shipped; "no open issues labeled M2f") | briefing May 12 entry |
| M2g (emergent sub-epic) | ACTIVE — 2 MVP-relevant issues open (#1089 + #1016); #1011 post-MVP | GitHub query today |

**Open M2-family issues today** (GitHub `gh issue list` against `label:M2,M2g,M2f,M2e,M2d`):

| # | Title | Status today |
|---|---|---|
| #1089 | KG-PRIVACY-FILTER (M2g, enhancement, priority:low) | **Increment 1 of 5 SHIPPED** today (`b5270c203`) — PrivacyLevel + FilterReason enums + 11 tests; 4 more increments queued per Lead's 5-step plan |
| #1016 | LLM-touch boundary principle (M2g, architecture, **epic**) | Open epic; #1017 (the implementation) closed May 15; #1016 may be a tracker rather than a closeable issue — worth a Lead-Dev disposition |
| #1011 | Slash-command dispatch precedence (M2g, architecture) | Explicit **post-MVP** per briefing — does not gate M2 |

### Recent ship velocity (last 8 days, since briefing's May 15 refresh)

| Date | Lead Dev shipping | M2-relevant? |
|---|---|---|
| May 16 | #1093 (ORCH-TASK-OUTPUT-VALIDATION close), #1015 (RequestContext migration close) | YES — both M2g |
| May 17 | 9+ closures including #1099, #1100, #1097 (MUX surfaces); #1102 (Pattern-073 data-substitution); #1101, #1098, #1044, #1037, #1038, #1026, #1046, #1005, #1077 | Multiple M2-related; MUX surfaces map to M2d ship-around |
| May 18 | #1080 NOTION-WRITE; #1081 NOTION-SLACK-XREF; #1085 slice 2; #1086 calendar; Pattern-073 → Proven | YES (M2e/M2g adjacent) |
| May 19-22 | Slack OAuth/keychain marathon; mailbox-MANIFEST destructive-sync recovery; worktree cleanup pass; #1106 #1107 #1108 #1109 #1110 follow-ups filed; Slack OAuth Healthy verified | Methodology + integrations; no M2g closures |
| May 23 (today) | #1085 slice 3 mentions-of-user (`9ac7121a4` → merge `135dad60b`); #1111 audit-trail; Pattern-073 #14 update; **#1089 Increment 1 shipped** | YES — M2g advancement |

**Read**: Lead Dev has shipped a lot in 8 days. Most of it isn't M2g-labeled because it's either follow-ups (#1106-1110), methodology (Pattern-073), or integration work (Slack OAuth). The actual M2g surface has shrunk to 2 issues.

### Quality canonical retest — the missing data point

| Run | Date | Quality PASS | Notes |
|---|---|---|---|
| Run 3 | Apr 13 | 62.3% | M2a baseline |
| Run 5 | post-#950 iter 2, Apr 16 | **72.1%** | M2c gate result (above floor, below 80% aspirational) |
| Run 4-6 | May 8-9 | 65.6% → improvements | Fixture-pollution surfaced + fixed; rubric-recalibration |
| Run 7 | May 9 | **68.9%** | Post 3 narrow fixes (#1065, #1067, #1066); CEO benchmark criterion met |
| Run 8 | May 13 | (intermediate, pre-restart) | Multi-turn harness (#1070); not authoritative |
| Run 9 | May 13 | **69.8%** | Multi-turn harness, restarted server |
| **Run 10** | **(missing)** | **(unknown)** | **Not yet run despite 15+ closures since May 13** |

**Gap to north star**: 5.2 percentage points (69.8% → 75%). Whether this closes naturally with the May 15-23 ship work or needs targeted intervention — we don't know without Run 10.

### M3-M5 + beta release infrastructure (what's between M2-done and beta)

What I can attest from the May 5 PM-ratified placements + briefing:

- **M3 placements** (May 5): #470, #371, #366 (#371 was duplicate-flagged for CEO)
- **M5 placements** (May 5): #482, #557, #542, #371, #472
- **M4 placement**: #1062 (Learning Phase 3)
- **No M3/M4/M5 label exists in GitHub** — placements are in working memory + the triage memo, not yet structured as sub-epics with gates
- **Alpha catch-22 reframe** (Apr 30): Phase A (Gemma simulation harness) → Phase B (beta-traffic refinement) → Phase C (stable). **No Phase A harness commits visible in recent logs.** If this is parked, it's a gating dependency for beta.

**What this means**: M3-M5 is real work but pre-structured. "Much less onerous" is plausible given the placement-list shape (small numbers of issues per sub-epic), but the Phase A simulation harness is the wildcard — without it, there's no calibration substrate for beta.

## Honest convergence vector

If you want a single answer: **structural M2 close looks plausible Tue-Wed next week (May 26-27). Beta is not plausible by anniversary. Beta is plausible within 2-4 weeks of M2 close, IF the quality north star verifies + Phase A harness is in flight or starts immediately after M2 close.**

The two non-obvious load-bearing items:

1. **Run 10 canonical retest**. If quality moved up to ≥75% naturally with the May 15-23 work, M2 closes cleanly on quality. If not, there's targeted intervention work between here and M2 close that we haven't scoped. **This is the single most informative next data point.** Lead Dev could run it any time; ~30-60 min wall-clock per the historical pattern.
2. **Phase A Gemma simulation harness status check**. Per the alpha-catch-22 reframe (Apr 30, Lead → Architect+PPM, folded into ADR-061 v1.0), Phase A is the calibration substrate that unblocks beta-traffic refinement (Phase B). I can't see recent work on it in the briefing or Lead's logs. Either it's parked + needs PM disposition on when to start, or it's happening somewhere I'm not seeing. **Worth asking Lead Dev directly.**

## What I did NOT verify (caveats)

- **m2-structure.md is stale** (last updated Apr 16); my read leaned on the briefing's May 18 STATUS BANNER for M2g state, then GitHub for current open-issue confirmation. The actual sub-epic structure of "M2g" isn't documented anywhere except briefing prose.
- **Per [[feedback_lead_dev_estimates]]**: Lead Dev's increment estimates run conservative. The "~2-2.5 hr remaining for #1089" figure is a best-current-stated estimate; actual may be faster (or slower if any increment surfaces design questions).
- **I did not query GitHub for M3/M4/M5 label state** (those labels don't exist; placements live in memos).
- **MUX/UI Phase 2 work** (Lead Dev lane scoping memo May 17) is in flight but I didn't scope its M2-gating relationship; assumed it's parallel-to-M2-close work, not blocking.
- **The skunkworks BYOC PoC** is out of scope for this memo; that's a separate lane on a separate timeline.

## What this memo does NOT recommend

Not recommending dates, deadlines, or interventions. The intent is to give you the convergence picture with enough fidelity that you can decide what to ask Lead Dev when bandwidth lands.

If you want me to follow up on either of the two load-bearing items independently (e.g., ask Lead Dev about Run 10 cadence or Phase A status as direct outreach), happy to draft those memos — but I'd rather you frame the asks since they touch sprint-velocity calibration.

## Cross-references

- **m2-structure.md** (canonical sub-epic doc; last updated 2026-04-16): `docs/internal/planning/m2-structure.md`
- **BRIEFING-CURRENT-STATE.md** (STATUS BANNER last refreshed 2026-05-18; refreshing in parallel commit today): `docs/briefing/BRIEFING-CURRENT-STATE.md`
- **Alpha catch-22 reframe + ADR-061 v1.0** (Apr 30): see briefing entry for date
- **Canonical retest Run 9** (May 13): `dev/2026/05/13/canonical-retest-run9-report.md`
- **M2-unmapped triage verdicts** (May 5; M3/M4/M5 placements): `dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md`
- **Lead Dev recent logs**: `dev/2026/05/{19,20,22,23}/*lead*log.md`

— PA, 2026-05-23 ~9:30 AM PT (worktree: `claude/pa-m2-convergence-2026-05-23`)
