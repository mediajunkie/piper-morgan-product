# D0 — git-history metrics (Spec evaluation)

Snapshot: piper-morgan-product `a191856164351cf59ba033d7dbc4a34f036c6122` (all queries bounded by it). Scripts and CSVs: `metrics/` (`common.py`, `m1_monthly.py`, `m2_bytes.py`, `m3_memos.py`, `m4_snapshots.py`, `m5_models.py`, `m6_roles.py`, `h4_defects.py`). Re-run order: m1, m2, m3, m4, h4, m5, m6 (h4 reads m4 CSVs). Month = author date, UTC. Layer for everything: **git-history**. Denominator: all 31,314 commits reachable from the snapshot (non-merge unless stated). `preregistration.md` was not edited.

## 1. H1 — coordination cost (M1.1, M1.2, ratio)
| month | pc | pc_lines | tc | mail | log | hb | hb-last-invoked | stop | heartbeat | merge | coord_total | C_over_P |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-06 | 53 | 17249 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 0.113 |
| 2025-07 | 52 | 37951 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| 2025-08 | 33 | 43787 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 5 | 0.152 |
| 2025-09 | 22 | 11655 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 |
| 2025-10 | 80 | 48362 | 17 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 2 | 0.025 |
| 2025-11 | 205 | 42165 | 78 | 0 | 3 | 0 | 0 | 0 | 0 | 21 | 24 | 0.117 |
| 2025-12 | 37 | 11846 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 10 | 0.27 |
| 2026-01 | 97 | 68284 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 0.031 |
| 2026-02 | 45 | 10918 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0.022 |
| 2026-03 | 67 | 9110 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 62 | 62 | 0.925 |
| 2026-04 | 52 | 8842 | 7 | 165 | 12 | 0 | 0 | 0 | 0 | 72 | 249 | 4.788 |
| 2026-05 | 127 | 25697 | 25 | 439 | 405 | 0 | 0 | 2 | 0 | 220 | 1066 | 8.394 |
| 2026-06 | 257 | 31451 | 39 | 961 | 865 | 0 | 0 | 3 | 0 | 920 | 2749 | 10.696 |
| 2026-07 | 130 | 19734 | 74 | 995 | 706 | 6 | 0 | 93 | 1 | 372 | 2173 | 16.715 |
| 2026-08 | 187 | 51688 | 32 | 1541 | 968 | 628 | 0 | 193 | 3 | 1077 | 4410 | 23.583 |
| 2026-09 | 192 | 41110 | 57 | 1755 | 1416 | 724 | 1909 | 183 | 0 | 1331 | 7318 | 38.115 |
| 2026-10 | 29 | 3484 | 32 | 213 | 226 | 77 | 125 | 23 | 0 | 158 | 822 | 28.345 |

Class counts are non-merge commits whose subject starts with that token (`mail`, `log`, `hb`, `hb-last-invoked`, `stop`, `heartbeat`; followed by `(`, `:`, space or end). `coord_total` = six classes + merge commits. PC = non-merge commit touching `services/ web/ templates/ alembic/ cli/ main.py`; TC = non-merge commit touching `tests/` but no PC path. `pc_lines` = added+deleted in PC paths only.

### Bytes (M1.2 bytes, M1.3 token proxy)
| month | mailboxes_bytes | dev_bytes | docs_briefing_bytes | token_proxy | token_proxy_excl_airlift |
|---|---|---|---|---|---|
| 2025-06 | 0 | 0 | 0 | 0 | 0 |
| 2025-07 | 0 | 0 | 0 | 0 | 0 |
| 2025-08 | 0 | 0 | 0 | 0 | 0 |
| 2025-09 | 0 | 2868514 | 69264 | 734444 | 734444 |
| 2025-10 | 0 | 20758908 | 55857 | 5203691 | 5203691 |
| 2025-11 | 0 | 10193451 | 11677 | 2551282 | 2551282 |
| 2025-12 | 0 | 3187981 | 0 | 796995 | 796995 |
| 2026-01 | 663053 | 3091126 | 43401 | 949395 | 949395 |
| 2026-02 | 132369 | 0 | 4590 | 34239 | 34239 |
| 2026-03 | 222920 | 38717043 | 97257 | 9759305 | 451838 |
| 2026-04 | 8068599 | 3497076 | 98460 | 2916033 | 2916033 |
| 2026-05 | 18316881 | 4741957 | 108836 | 5791918 | 5791918 |
| 2026-06 | 9640796 | 6837763 | 203625 | 4170546 | 4170181 |
| 2026-07 | 14158939 | 7569302 | 258986 | 5496806 | 5496806 |
| 2026-08 | 22662375 | 7376458 | 172184 | 7552754 | 7552754 |
| 2026-09 | 18596480 | 11003165 | 227656 | 7456825 | 7456825 |
| 2026-10 | 1543329 | 1323313 | 11703 | 719586 | 719586 |

Bytes = UTF-8 bytes of added diff lines (renames detected, so pure moves add 0). `token_proxy` = (mailboxes+dev+docs/briefing)/4. **Outlier:** 2026-03 (37.2 MB) and some of 2025-10/-11 `dev/` bytes are bulk "Airlift dev/ working docs" archival imports, not agent output (commit subjects e.g. `f0abb152f6`, `170fb00493`, `b49c12457a`); the `excl_airlift` column removes commits whose subject contains "Airlift". Only March 2026 is affected by that filter; the 2025-10 spike (20.8 MB) is not tagged Airlift and is unexplained here (unverified: likely another bulk import).

### H1 pre-registered computation (B = 2026-01..03, R = 2026-08..09)
| quantity | B mean/month | R mean/month | R÷B |
|---|---|---|---|
| PC count | 69.7 | 189.5 | 2.72 |
| PC lines (add+del) | 29,437 | 46,399 | 1.58 |
| M1.2 coordination commits | 22.0 | 5,864 | 266.5 |
| C/P, mean of monthly ratios | 0.326 | 30.85 | 94.6 |
| C/P, pooled (sum÷sum) | 0.316 | 30.94 | 98 |
| coord bytes (excl. Airlift) ÷ PC lines | 65.0 | 647.0 | 9.95 |
| coord bytes/month (excl. Airlift) | 1.91 MB | 30.0 MB | 15.7 |

**H1 verdict line: criteria (a) mean C/P R ≥ 2× B: met (94.6×). Criterion (b) PC growth (2.72×) < half of coordination growth (266.5× → half = 133×): met. Refutation conditions (C/P R ≤ 1.25× B; PC growth ≥ coordination growth): not met. Per the pre-registered rule: SUPPORTED.** Model-timeline confound: not assessable as an alternative explanation of the C/P ratio itself (model change would not obviously create mail/log commits); see section 4 for dates. Plain-number caveat: B contains almost no coordination commits by this subject definition because the mail/log/hb conventions did not yet exist in B (first `mail(` commit in the series is 2026-04), so the B denominator is near zero and the multiple is large by construction.

### M1.4 memos delivered to `mailboxes/xian (ceo)/inbox/` (new `.md` files added, excluding MANIFEST)
| month | ceo_inbox_new_memos |
|---|---|
| 2025-06 | 0 |
| 2025-07 | 0 |
| 2025-08 | 0 |
| 2025-09 | 0 |
| 2025-10 | 0 |
| 2025-11 | 0 |
| 2025-12 | 0 |
| 2026-01 | 0 |
| 2026-02 | 0 |
| 2026-03 | 3 |
| 2026-04 | 15 |
| 2026-05 | 614 |
| 2026-06 | 458 |
| 2026-07 | 643 |
| 2026-08 | 852 |
| 2026-09 | 1002 |
| 2026-10 | 39 |

Last 13 weeks (7-day buckets ending at snapshot 2026-10-03 17:41Z):

| week_ending | ceo_inbox_new_memos |
|---|---|
| 2026-07-11 | 147 |
| 2026-07-18 | 87 |
| 2026-07-25 | 68 |
| 2026-08-01 | 310 |
| 2026-08-08 | 343 |
| 2026-08-15 | 179 |
| 2026-08-22 | 91 |
| 2026-08-29 | 94 |
| 2026-09-05 | 247 |
| 2026-09-12 | 247 |
| 2026-09-19 | 189 |
| 2026-09-26 | 390 |
| 2026-10-03 | 91 |
Attention rollups: item counts not computed (not in D0 scope; would need parsing rollup artifacts). Unobserved here.

## 2. Mechanism introduction dates and ruleset growth
- First commit touching `mailboxes/`: `2979642a6e` 2026-01-14 "chore: Reorganize dev files, add mailbox system, docs cleanup".
- First commit touching `.claude/skills/duty-cycle-tick`: `ce42e05c68` 2026-06-06 "skill(cio): duty-cycle-tick v1.0 ...".
- `.claude/hooks` files, first-add date (`metrics/m4_hooks_first_add.csv`): session-start.sh 2026-02-25; check-branch.sh 2026-03-31; log-maintenance-reminder.sh 2026-04-19; precompact-signoff-warning.sh 2026-05-08 (+ `.disabled` copy 2026-05-17); pre-commit-broad-staging-warn.sh and context-usage-reminder.sh 2026-05-15; issue-checkbox-lint.sh 2026-05-16; pre-commit-reconcile-drafts.sh 2026-06-15; memory-index-overlimit-warn.sh 2026-07-31; PROBE-userpromptsubmit.sh 2026-08-05; post-commit.sh 2026-09-21; autoclose-guard.sh 2026-09-24; pre-commit-ruff-warn.sh 2026-10-01. (13 files present at snapshot; `.disabled` and PROBE files are not real mechanisms but are kept in the pre-registered list as found.)
- Skills: `.claude/skills/*` dirs with SKILL.md: 0 until 2025-12, 5 at 2026-01, 11 at 2026-03, 31 at 2026-06, 35 at 2026-08 onward (table below). Earlier skills may have lived at other paths (unverified).

### Month-end snapshots: ruleset vs product (deliverables 4 and 8)
| month | claude_md_bytes | claude_md_lines | claude_md_mom_growth | gt25pct | skills_count | skills_bytes | hooks_files | docs_briefing_bytes | services_web_py_loc |
|---|---|---|---|---|---|---|---|---|---|
| 2025-06 | 0 | 0 |  |  | 0 | 0 | 0 | 0 | 7622 |
| 2025-07 | 18065 | 500 |  |  | 0 | 0 | 0 | 0 | 32496 |
| 2025-08 | 7857 | 226 | -0.565 | 0 | 0 | 0 | 0 | 0 | 64758 |
| 2025-09 | 4916 | 153 | -0.374 | 0 | 0 | 0 | 0 | 64579 | 71251 |
| 2025-10 | 7883 | 227 | 0.604 | 1 | 0 | 0 | 0 | 87936 | 100503 |
| 2025-11 | 32671 | 958 | 3.144 | 1 | 0 | 0 | 0 | 60048 | 115292 |
| 2025-12 | 35104 | 1023 | 0.074 | 0 | 0 | 0 | 0 | 60048 | 123291 |
| 2026-01 | 7685 | 243 | -0.781 | 0 | 5 | 37570 | 0 | 61664 | 166158 |
| 2026-02 | 9749 | 280 | 0.269 | 1 | 5 | 39503 | 1 | 61005 | 172244 |
| 2026-03 | 11159 | 306 | 0.145 | 0 | 11 | 77643 | 1 | 122566 | 177234 |
| 2026-04 | 23568 | 486 | 1.112 | 1 | 12 | 99891 | 3 | 197322 | 175009 |
| 2026-05 | 30785 | 556 | 0.306 | 1 | 15 | 182250 | 7 | 272864 | 178943 |
| 2026-06 | 43831 | 623 | 0.424 | 1 | 31 | 383997 | 8 | 404722 | 187369 |
| 2026-07 | 57197 | 658 | 0.305 | 1 | 34 | 462825 | 9 | 447659 | 183667 |
| 2026-08 | 70168 | 756 | 0.227 | 0 | 35 | 528078 | 10 | 514583 | 185703 |
| 2026-09 | 65534 | 745 | -0.066 | 0 | 35 | 592281 | 12 | 554465 | 188257 |
| 2026-10 | 65534 | 745 | 0.0 | 0 | 35 | 594619 | 13 | 555620 | 190130 |

CLAUDE.md months with >25% month-over-month byte growth (vs previous month-end snapshot): 2025-10, 2025-11, 2026-02, 2026-04, 2026-05, 2026-06, 2026-07. CLAUDE.md shrank/restructured twice (2025-08, 2026-01: -57%/-78%), so growth percentages are partly rebounds. Snapshot CLAUDE.md = 65,534 B / 745 lines (matches prereg's 745 lines). Ruleset bytes (CLAUDE.md + skills + docs/briefing) at 2026-09: 65.5k + 592k + 554k = 1.21 MB vs 188k Python LOC in services+web; at 2026-01: 7.7k + 37.6k + 61.7k = 107k vs 166k LOC. Python LOC grew 1.13× (166,158 → 188,257) while ruleset bytes grew about 11×.

## 3. H4 — interrupted time series
Monthly defect signals (normalized per PC). d1 = non-merge commit, subject starts with "Revert" or contains "revert" (case-insens.). d2 = non-merge `fix` commit touching a product-path or tests file that a feat/fix commit touched in the prior 72h.
| month | pc | d1_reverts | d2_fix_on_fix | d12_per_pc |
|---|---|---|---|---|
| 2025-06 | 53 | 0 | 5 | 0.094 |
| 2025-07 | 52 | 0 | 3 | 0.058 |
| 2025-08 | 33 | 3 | 7 | 0.303 |
| 2025-09 | 22 | 0 | 1 | 0.045 |
| 2025-10 | 80 | 0 | 11 | 0.138 |
| 2025-11 | 205 | 2 | 68 | 0.341 |
| 2025-12 | 37 | 0 | 16 | 0.432 |
| 2026-01 | 97 | 0 | 26 | 0.268 |
| 2026-02 | 45 | 0 | 12 | 0.267 |
| 2026-03 | 67 | 0 | 14 | 0.209 |
| 2026-04 | 52 | 0 | 11 | 0.212 |
| 2026-05 | 127 | 3 | 14 | 0.134 |
| 2026-06 | 257 | 9 | 52 | 0.237 |
| 2026-07 | 130 | 14 | 45 | 0.454 |
| 2026-08 | 187 | 8 | 58 | 0.353 |
| 2026-09 | 192 | 33 | 79 | 0.583 |
| 2026-10 | 29 | 0 | 1 | 0.034 |

60 days before vs after each mechanism date (defect rate = (d1+d2)/PC; windows [t-60d,t) and [t,t+60d); "complete"=after-window ends before snapshot):
| mechanism | date | after_window_complete | pc_before | pc_after | d12_rate_before | d12_rate_after | rate_drop_frac | pc_change_frac |
|---|---|---|---|---|---|---|---|---|
| first mailbox commit | 2026-01-14 | True | 250 | 117 | 0.364 | 0.282 | 0.225 | -0.532 |
| duty-cycle-tick skill | 2026-06-06 | True | 190 | 390 | 0.163 | 0.31 | -0.902 | 1.053 |
| hook session-start.sh | 2026-02-25 | True | 134 | 122 | 0.261 | 0.23 | 0.121 | -0.09 |
| hook check-branch.sh | 2026-03-31 | True | 114 | 177 | 0.228 | 0.153 | 0.331 | 0.553 |
| hook log-maintenance-reminder.sh | 2026-04-19 | True | 126 | 282 | 0.246 | 0.188 | 0.236 | 1.238 |
| hook precompact-signoff-warning.sh | 2026-05-08 | True | 137 | 381 | 0.153 | 0.228 | -0.49 | 1.781 |
| hook pre-commit-broad-staging-warn.sh | 2026-05-15 | True | 135 | 405 | 0.133 | 0.249 | -0.87 | 2.0 |
| hook context-usage-reminder.sh | 2026-05-15 | True | 135 | 405 | 0.133 | 0.249 | -0.87 | 2.0 |
| hook issue-checkbox-lint.sh | 2026-05-16 | True | 132 | 395 | 0.114 | 0.258 | -1.272 | 1.992 |
| hook precompact-signoff-warning.sh.disabled | 2026-05-17 | True | 136 | 394 | 0.11 | 0.259 | -1.347 | 1.897 |
| hook pre-commit-reconcile-drafts.sh | 2026-06-15 | True | 237 | 397 | 0.169 | 0.353 | -1.089 | 0.675 |
| hook memory-index-overlimit-warn.sh | 2026-07-31 | True | 387 | 377 | 0.31 | 0.451 | -0.454 | -0.026 |
| hook PROBE-userpromptsubmit.sh | 2026-08-05 | False | 390 | 388 | 0.31 | 0.451 | -0.454 | -0.005 |
| hook post-commit.sh | 2026-09-21 | False | 267 | 146 | 0.393 | 0.555 | -0.411 | -0.453 |
| hook autoclose-guard.sh | 2026-09-24 | False | 298 | 110 | 0.383 | 0.618 | -0.616 | -0.631 |
| hook pre-commit-ruff-warn.sh | 2026-10-01 | False | 379 | 29 | 0.464 | 0.034 | 0.926 | -0.923 |
| CLAUDE.md >25% month 2025-10 | 2025-10-01 | True | 54 | 282 | 0.204 | 0.287 | -0.41 | 4.222 |
| CLAUDE.md >25% month 2025-11 | 2025-11-01 | True | 102 | 241 | 0.118 | 0.357 | -2.033 | 1.363 |
| CLAUDE.md >25% month 2026-02 | 2026-02-01 | True | 128 | 113 | 0.312 | 0.23 | 0.264 | -0.117 |
| CLAUDE.md >25% month 2026-04 | 2026-04-01 | True | 114 | 179 | 0.228 | 0.156 | 0.314 | 0.57 |
| CLAUDE.md >25% month 2026-05 | 2026-05-01 | True | 115 | 366 | 0.209 | 0.189 | 0.097 | 2.183 |
| CLAUDE.md >25% month 2026-06 | 2026-06-01 | True | 178 | 387 | 0.157 | 0.31 | -0.971 | 1.174 |
| CLAUDE.md >25% month 2026-07 | 2026-07-01 | True | 384 | 288 | 0.203 | 0.424 | -1.085 | -0.25 |

Mechanism dates for CLAUDE.md spurts = first day of the spurt month. Windows overlap heavily across mechanisms (the 23 tests are not independent).

**Rule application.** Mechanisms meeting "after rate ≥25% lower AND PC not down >25% AND window complete": **3 of 23** (check-branch.sh 2026-03-31: -33%, PC +55%; CLAUDE.md spurt 2026-02: -26%, PC -12%; CLAUDE.md spurt 2026-04: -31%, PC +57%). Mailbox (-22.5%, PC -53%), duty-cycle-tick (rate +90%) and the first hook (-12%) do not meet it. 15 of 23 show a rising rate; 7 show a ≥10% drop.
**H4 verdict line, literal rule: "supported" criterion technically met (≥2 mechanisms), refutation criterion (no mechanism ≥10% drop, or rates rise) not met. But:** the 3 passes come from 23 overlapping windows in Feb-Apr 2026 (all three sit inside the same 2026-02..04 stretch, i.e. one episode counted three times); every later mechanism (May-Oct 2026) shows a higher d1+d2 rate per PC after; monthly d1+d2 per PC rose from 0.21 (2026-03) to 0.58 (2026-09); and every one of the 23 mechanism dates falls within 30 days of a model first-mention (section 4). I therefore report **H4: literal rule = supported on one early episode; effectively INCONCLUSIVE per the pre-registered model-confound clause, with defect-signal trend upward since 2026-05.** d1/d2 are commit-message/file-overlap proxies, not defect measurements: fix-on-fix also counts iterative multi-commit fixes within one change.

## 4. Model-timeline confound
Vendor release dates are **unsourced** in the repo (no file states them), so none are asserted. Sourced alternative: first commit in `dev/ docs/ .claude/ CLAUDE.md` that mentions each model string (`metrics/m5_models_first_mention.csv`). These are first mentions in repo, a lagging proxy for adoption, not release dates:
Opus 4.1 2025-08-08 (`0e7494921a`); Sonnet 4.5 2025-10-02 (`a7db0796c7`); Haiku 4.5 2025-10-25 (`3e8aab7c70`); Opus 4.5 2025-11-29 (`b8fbad55fb`); Opus 4.6 2026-02-11 (`c75ebcab3d`); Sonnet 4.6 2026-03-24 (`a0d5c2ada2`); Opus 4.7 2026-04-20 (`5989e55bf3`); Opus 4.8 2026-06-01 (`176fb253c4`); Sonnet 5 2026-07-01 (`6fad484358`); Opus 5 2026-07-25 (`99c4c48329`); Opus 5.5 2026-09-22 (`789b33e45e`); Sonnet 5.5 2026-10-02 (`355cc06770`).
Mechanism dates within 30 days of a first-mention: first mailbox (Opus 4.6, -28d); duty-cycle-tick (Opus 4.8 +5d); session-start hook (Opus 4.6 +14d, Sonnet 4.6 -27d); check-branch (Sonnet 4.6 +7d); log-maintenance (Opus 4.7 -1d); all May 2026 hooks (Opus 4.7/4.8 within 15-27d); pre-commit-reconcile (Opus 4.8 +14d); memory-index/PROBE (Opus 5 +6d/+11d); post-commit/autoclose/ruff (Opus 5.5 / Sonnet 5.5 within 11d). All 23 listed mechanism dates have at least one model first-mention within 30 days (full per-mechanism list reproducible from the CSVs). The model timeline therefore cannot be separated from mechanism timing.

## 5. Per-role activity
Files: `metrics/m6_roles_commits.csv` (monthly, by subject-prefix role slug) and `m6_roles_sessionlogs.csv` (new session-log files per month by filename role). Totals over all history, subject-prefix commits: cio 2248, lead 1826, host 1338, exec 1278, docs 1260, comms 1207, pa 1088, arch 1051, cxo 965, ppm 956, web 886, watchdog 168. New session-log files by filename role: lead 496, prog 490, docs 378, arch 296, exec 279, cxo 209, comms 206, ppm 181, cio 171, pa 163, host 139, web 119 (plus long tail: prog-cursor 96, spec 33, ...). Note the two measures rank roles differently (cio is top by commits but near-bottom by log files). Slug normalization is by first token in parentheses; variants like `pard-`, `janus-` are left as separate rows.

## Deviations
1. d2 "a file" restricted to product-path + tests files (spec says any file; would produce spurious overlaps with dev/mail files). Fix commit = subject matching `^fix\b` (case-insens.); feat/fix prior-touch lookback uses last 5 touches per file.
2. d1 counts non-merge commits only (merge commits are in the coordination series).
3. Bytes = added diff-line bytes, not blob sizes; renames suppressed. Airlift bulk imports reported separately (added column; original total retained).
4. "Mechanism" list = every hook file first-add + spurt months + mailbox + duty-cycle-tick, i.e. 23 tests, not a pre-chosen small set; windows overlap. CLAUDE.md spurt date set to the first day of the month.
5. Months use author date; rebases/cherry-picks could shift a few commits across month boundaries.
6. M1.4 counts file adds, not unique memos (a file re-added after a move counts again; --no-renames used).

## Unobservables
- **d3 (reopened issues) and d4 (bug-labelled issues opened):** `gh` unavailable; the GitHub MCP `search_issues` is semantic search with no label filter or total counts, so not cheaply obtainable. Observable via GitHub REST (`/issues?labels=bug&since=`, issue timelines) with a token.
- **Vendor model release dates:** not in repo; need vendor release notes.
- **Attention-rollup item counts (M1.4 second half), read costs (M1.3 read side):** out of D0 scope / need D-measure.
- **Cowork/PM-machine jobs, runtime token spend:** not in git.
- **Whether defects are real:** d1/d2 are message/file-overlap proxies; true defect rates need issue/CI data.
- **Skills before 2026-01 at other paths, 2025-10 20.8 MB dev/ spike cause:** unverified.
