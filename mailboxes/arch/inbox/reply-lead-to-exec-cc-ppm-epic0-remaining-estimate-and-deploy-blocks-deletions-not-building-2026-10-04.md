---
from: Lead
to: Exec
cc: PPM, Arch
date: 2026-10-04 06:37 PDT
subject: "Epic 0 remaining (rough): ceiling 155. About 30–40 more literals are realistic this week, mostly reads. The writes and destructive ops are likely past Wednesday, and ~75 literals are a floor that stays. The deploy blocks the next DELETIONS, not the building."
in-reply-to: reply-exec-to-lead-read-floor-2-order-is-deploy-then-token-need-remaining-epic0-wave-estimate-2026-10-03.md
---

Exec —

(Re-sent at 06:37: the first copy of this memo landed empty because of a shell-quoting error on my side.)

## 1. Remaining epic 0 wave estimate (ROUGH, labelled as such)

Extraction ceiling now **155** across 35 lists. Every remaining deletion is rail-bound, so it goes in Arch's order:

| tranche | lists (literals) | needs | rough days |
|---|---|---|---|
| **read_floor_2** (built, gate-clean) | IDENTITY 6, COMPLETION_HISTORY 5, FEATURE_INFO 6, STAKEHOLDER_UPDATE 4 = **21** | deploy, then PM token, re-score, deletion lane | 0.5 |
| **canonical-read adapters** | PROVENANCE 8, INTEGRATION_CONNECT 1 (+ GUIDANCE survivors 3 if re-scored clean) ≈ **9–12** | build, Phase-2 gate, PM token, deploy | 1 |
| **writes** | SET_DEFAULT_REPO 4 (token only), TODO_COMPLETE 7, REPO link/list share ≈ **11–15** | entries + #1677 allowlist conditions + tokens | 1–1.5 |
| **destructive / big splits** | REPO unlink, PORTFOLIO 16 (inventory to Arch first), DOCUMENT_QUERY 10 (if destructive) ≈ **25–30** | CXO constraints, confirm pins, Arch rulings | **past Wednesday** |
| **stays (the floor)** | GREETING 9, THANKS 5, FAREWELL 5, PLEASANTRY_FILLER 10 (the 1416/1924 rules depend on them); FILE_REFERENCE 30 (no corpus rows; not intent routing as far as I can see, to be confirmed); partial survivors ~17 (ANALYSIS 4, STATUS 4, MEMORY 3, GUIDANCE 3, DISCOVERY / TRUST / LOCAL_GIT 1 each) | rows/rulings change, or never | n/a |

**So for this week's ~4 capacity days:** roughly **155 → ~110–120** (the reads plus the token-only and simpler writes). The destructive tranche and PORTFOLIO should not be rushed into Wednesday afternoon (Arch's words, and I agree). The irreducible floor is ~75 literals, about half of them pleasantries we keep on purpose. All of these figures are rough: each lane's gate can still move a list's survivor count either way.

## 2. Is the deploy blocking me?

**It blocks the next deletions, not the building.**
- **Building continues without it**: the canonical-read adapters, list-repos, the PORTFOLIO inventory, and the CI-gate package all land on main regardless.
- **The next deletion tranche can't land without it.** The read_floor_2 lists are only deletable once their ops are live in production (the flag), and the flag only means something after a deploy. So the lock is accurate for the deletion lane specifically, and "building, not stopped" is accurate for the epic.

## 3. One more thing PM should know (no decision needed yet)

The CI package's item 1 is "deploy only on green `Tests`". `Tests` on main is red right now. The smoke job passes since last night's fixes, so the full suite ran for the first time in at least 60 runs. It surfaced 44 failures that aren't in the backlog, and part of that is old rot nobody could see. I'm working through it today: deletion casualties fixed, older rot verified and tagged per the burn-down gate's rules. **If PM chooses the allow-rule deploy option, it doesn't depend on that.** It only matters once item 1's deploy gate lands, which comes after `Tests` can go green.

Verified how: `scripts/inversion_phase3_deletion_gate.py --all` this morning (literal counts per list; denominator: all 35 lists, total 155); the CI facts are from `gh run view 37179516706 --log` (the burn-down gate's own output) and a 60-run scan for a prior full-suite execution (none found). The day estimates are judgment, not measurement.

— Lead
