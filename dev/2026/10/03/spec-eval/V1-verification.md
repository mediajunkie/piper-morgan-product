---
type: verification-report
title: "Spec evaluation, Phase 4: independent verification V1 of synthesis-draft.md"
author: V1 (independent adversarial verifier, cloud subagent, Opus 5.5)
date: 2026-10-03
target: dev/2026/10/03/spec-eval/synthesis-draft.md
snapshot: product a191856164351cf59ba033d7dbc4a34f036c6122 (all git queries bounded by it; working-tree HEAD is 68ba122, so V1 read mailboxes from the snapshot tree, not the working tree)
scripts: metrics/V1-history.py, metrics/V1-mail.py (written from scratch; they do not import common.py)
---

# V1 verification of the synthesis draft

**Bottom line.** The headline numbers reproduce exactly. Two load-bearing claims do not hold as written, and both
tilt toward the "too much process" conclusion:

1. **The "defects per PC rose 0.21 → 0.58" trend is inflated by a broken proxy.** All 33 of September's d1
   "reverts" are coordination subjects such as "cadence reverted 6x/day" or "throttle-revert ruling". None of them
   touches product or test code, and none is a `Revert "…"` commit.
2. **F's "≥25 caused vs 4–6 caught" counts the two sides with different units.** F's own §3 table records 178 of
   180 watchdog alerts as matching real git silence. In the catch column, those 178 true positives appear as a
   single bullet.

Several recommendations also omit a cost or a conflict:
- R1 overrides an explicit PM ruling without engaging it, and its step 3 is infeasible per C-02.
- R5 item 5 would break `mail-send.sh`, which R7 says to protect.
- R3's target metric conflicts with R7 and can be gamed.

---

## 1. Independent re-derivations (V1's own scripts)

| # | Claim in synthesis | V1 method | V1 result | Verdict |
|---|---|---|---|---|
| a1 | PCs ~70/mo (Jan–Mar) → ~190/mo (Aug–Sep), 2.72× | `V1-history.py`: own `git log --no-renames --name-only` parse, non-merge, PC paths per prereg, author-date UTC | B mean **69.7**, R mean **189.5**, ratio **2.72**. Same counts by committer date. | **MATCH** |
| a2 | Total commits grew ~48× | same script, all commits reachable from snapshot (31,314) | B 175.0/mo → R 8,443/mo = **48.25×** (non-merge only: 47.3×) | **MATCH** |
| b1 | 82% of 1,899 memos in 8 weeks addressed PM | `V1-mail.py`: reads `mailboxes/*/sent/*.md` **from the snapshot tree** via `git cat-file`. Unit is the unique filename. PM token matched strictly (pm / xian / ceo). | 1,899 memos in window; **1,550 PM-addressed (81.6%)** strict, 1,551 under F's looser rule | **MATCH** |
| b2 | ~78k words/week | same script | **77,889** body words/week | **MATCH** |
| b3 | (not in synthesis) | same script | Only **106 of 1,899 (5.6%) have PM in `to:`**. 94% of PM-addressed memos are cc. Week ending 10-03: **54 of 191 (28%)**. | **New context.** See R4. |
| c1 | CLAUDE.md ~16k tokens (chars/4) | `git show a191856:CLAUDE.md`, Python `len()/4` | 65,035 chars → **16,258** tokens; 745 lines | **MATCH** |
| c2 | BRIEFING-CURRENT-STATE ~40k tokens | same | 161,844 chars → **40,461** tokens; 716 lines | **MATCH.** Layer: these are the documents the protocol tells agents to load. Whether agents actually read them was not observed. |
| d1 | d1 revert rate: Mar 0 → Sep rising (feeds "0.21 → 0.58") | `V1-history.py`: subject matches /revert/i, non-merge | Raw count reproduces D0: Mar **0**, Sep **33** (0.172/PC). But **0 of the 33 touch `services/ web/ templates/ alembic/ cli/ main.py tests/`**, and 0 are `Revert "…"` commits. Every one is a cadence or throttle coordination subject. Across May–Sep only **6** "revert" commits touch code. | **MISMATCH IN MEANING.** The number reproduces, but it is not measuring reverts. |
| d2 | d1+d2 per PC 0.21 (Mar) → 0.58 (Sep) | Recomputed with d1 limited to code-touching commits (= 0 in Sep) | Sep becomes (0+79)/192 = **0.41**, not 0.58. The fix-commit share of PCs also rose from **0.40 (Mar) to 0.60 (Sep)**, so d2 partly tracks the work mix. | **WEAKENED.** Roughly 2× rather than 2.8×, and confounded by work mix. |

---

## 2. Reproduction of existing metrics scripts

The scripts were copied to the scratchpad so the originals were not overwritten, then re-run. Outputs were diffed
against the committed files.

| Script | Output compared | Result |
|---|---|---|
| `m1_monthly.py` (with `common.py`) | `m1_monthly.csv` | **byte-identical** |
| `m3_memos.py` | `m3_memos_monthly.csv`, `m3_memos_weekly.csv` | **byte-identical** |
| `F-mail.py` | `F-mail.out` | **byte-identical** (it reads the working tree, which equals the snapshot for `mailboxes/`) |
| `B-skips.py` (run in `/home/user/snapshot-code`) | `B-skips.out` | **identical except the file count: 983 vs 982.** One extra test file exists in snapshot-code. All skip and xfail counts match. Immaterial. |

### Live check of B1 (CI)

V1 ran `gh api repos/mediajunkie/piper-morgan-product/actions/workflows/test.yml/runs?status=success`.

- The newest successful run on main is **run 3753, 2026-09-20T16:27Z**. Run 3754 on `production` succeeded at the
  same moment.
- B's claim is **CONFIRMED**.
- Caveat: adding `&branch=main` to the same query returns a stale `total_count` of 36 with newest run 3694. That
  looks like an API quirk. Anyone re-running this should check without the branch filter.

---

## 3. Specific checks (i)–(v)

**(i) G: "effectively no users / one external session in four months."**
- **Evidence base:** records only, at the record layer:
  - omnibus logs from 07-27 and 07-28;
  - the PA log from 07-29;
  - the invite thread from 09-13 to 10-01;
  - the issue authorship of all 1,903 issues.
- **Contrary evidence:** V1 grepped the Aug–Sep omnibus logs for tester login, signup and setup activity. It found
  nothing beyond Jake (July) and the 09-21 invitee.
- **Users the repo cannot see:** G itself lists the production `users` and `feedback` tables as unobservable, and
  says the current count of working invites is "plausibly 0 (unverified)". It is possible that people signed up
  through the hosted URL without the cohort noticing. The rest of the record makes that unlikely, but the repo
  cannot rule it out.
- **Problem with the synthesis:** the exec bullet states "One external person has used the hosted product in four
  months" as fact.
- **Verdict:** WEAKENED in phrasing only. It should read "the records show one…; production DB not checked".

**(ii) A: "~10.6k unreachable LOC."** V1 spot-checked 3 modules with `git grep` at the snapshot over all `*.py`,
including tests:

| Module | LOC | Importers found |
|---|---|---|
| `services/integrations/slack/workspace_navigator.py` | 809 | only `tests/unit/.../test_spatial_system_integration.py` |
| `services/conversation/context_tracker.py` | 478 | only its own unit test and an architecture-enforcement path list |
| `services/infrastructure/config/methodology_configuration.py` | 460 | only `tests/infrastructure/config/test_methodology_config_service.py` |

- **Result:** 3 of 3 are unreachable from production entry points. CONFIRMED.
- **Caveat:** "removable" means deleting their tests too, and CLAUDE.md STOP #10 ("found 75% complete code, report
  it") applies. These are possibly unfinished features rather than dead ones.

**(iii) B: "Tests 0 successes since 2026-09-20."**
- **Sources:**
  - `metrics/B-ci-test-main.tsv`: the last 100 runs, 83 failure and 17 cancelled, spanning 09-26 to 10-03;
  - the GH API status=success query.
- V1 re-queried the API (§2).
- **Verdict:** CONFIRMED. The source is cited and the claim is plausible.

**(iv) F: "≥25 incidents caused vs 4–6 caught."** V1 classified a systematic sample (every 5th row: #5, #10, #15,
#20, #25), plus #1, #3 and #24:

| Row | Incident | Caused by coordination machinery? |
|---|---|---|
| #1 | duty-cycle `git checkout -- .` destroyed PM's edits | **Yes** |
| #3 | "every stall was the subscription cap" | **No.** This is an external capacity limit, not a machinery incident. |
| #5 | worktree provisioned 5,393 commits behind | **Partial.** It came from the host migration and provisioning, not the coordination loop. |
| #10 | cohort usage freeze; PM detected it | **Partial.** A capacity event plus a detection gap. |
| #15 | subagent fan-out exhausted the ceiling | **Partial.** Dispatch behaviour, not coordination machinery. |
| #20 | 5 roles dark 6 days, watcher blind spot | **Yes** (a watcher failure) |
| #24 | PM cc'd on everything | **No.** This is a policy, already counted under F2.1. |
| #25 | cio heartbeat churn, 1,026 commits | **No.** This is a cost, already counted as F1.2. V1 confirmed 1,025 `hb-last-invoked(cio)` subjects in the 4 weeks. |

Across the 8 rows: **2 are clearly machinery-caused, 3 partial and 3 not incidents.**

The catch side is counted in different units. F §3 records **178 of 180 watchdog alerts matching real git
silence**, and §4 collapses those into one bullet. The incident surfaces (CLAUDE.md, the history log) are
lessons-learned records, so they over-sample failures and miss prevented non-events.

**Verdict:** WEAKENED. A defensible statement is: "about 10–15 machinery-caused incidents on record; the watchdog
has a high true-positive rate but late detection; most other watchers have no recorded catch."

**(v) D-propose: the proposed CLAUDE.md keeps all 17 safety rules.** V1 read `D-proposed-CLAUDE.md` against the
snapshot CLAUDE.md for 10 of the 17:

| Rule | Status in proposal |
|---|---|
| S-1 | Kept, and tightened: adds `git clean` |
| S-2 | Kept. Drops the "never infer staleness because the fix exists upstream" warning and the `--diff-filter=D` corollary. |
| S-3 | Kept |
| S-4 | Kept. Drops the `mailbox_bearer_lint` pointer. |
| S-5 | Kept, with a skill pointer |
| S-6 | Kept |
| S-7 | Kept. Drops "pruning the shared pool is a governance action". |
| S-11 | Kept verbatim |
| S-14 | Kept verbatim |
| S-15 | Kept, but the STOP list drops two of the 10 conditions: **#8 "completion bias detected"** and **#10 "found 75% complete code (report it)"**. #3 partly covers #10. |

- **Verdict:** CONFIRMED at the text and anchor layer, with minor detail losses.
- **Two caveats:**
  - The "17" is D-propose's own enumeration, a self-defined denominator.
  - The behavioural layer is unverified, as the synthesis already says.
- **Size:** 11,828 bytes, so ~2.9k tokens. Matches.

---

## 4. Per-item verdicts

### Hypotheses

| Item | Verdict | Evidence |
|---|---|---|
| **H1** (supported) | **CONFIRMED on direction; WEAKENED on one inference** | PC and total-commit numbers reproduce exactly. The synthesis already caveats the degenerate baseline, which is correct. **Weak point:** "coordination competes with product work for capacity" is inferred from one account at 96% in one week (the other account was at 76%). No one measured what share of tokens coordination uses versus product work. Also, a commit is cheap, so bytes are a better cost measure than commit counts: coordination bytes per PC line grew **9.95×**, not 94.6×. Lead with that. |
| **H1b** (partial) | **CONFIRMED** | Literal verdict reproduces from the cited reports. |
| **H2** (supported) | **CONFIRMED, two sub-claims WEAKENED** | Token counts reproduce. **PreCompact "drift" is overstated:** `.claude/settings.json` has `"PreCompact": []`, but the hook is registered by design in the Amber user-level mirror (D-measure C22 says so). It is unverifiable from the repo, not drifted. **DP-4 "contradicts its own HARD RULE" is overstated:** `git checkout main && merge` conflicts with the worktree and push rules and is risky in PM's checkout, but it is not on the HARD RULE's destructive-command list. |
| **H3** (marginal) | **CONFIRMED** | 35/44 reproduces from L's table. Add that 16 of 60 claims (27%) were uncheckable and excluded from the denominator. |
| **H4** (inconclusive) | **Verdict CONFIRMED; supporting narrative WEAKENED** | The headline "Defects per PC rose 0.21 → 0.58" must change. The September d1 is 100% false positives (§1 d1). The corrected figure is 0.21 → 0.41, and d2 tracks the fix-share of the work mix (0.40 → 0.60). "Inconclusive" stands. The exec-summary bullet "Defects per product change rose rather than fell" is not supportable as phrased. |
| H4 "things the process demonstrably buys" | **WEAKENED (causal language)** | E's table shows test co-commit was already **93% in 2026Q1**, before the mailbox and duty-cycle era. "Buys" is causal; these virtues predate the coordination machinery. This actually supports R3, but the wording must change. |

### Recommendations

| Item | Verdict | Evidence |
|---|---|---|
| **R1** users | **WEAKENED (direction sound; costs and conflicts missing)** | (1) It overrides an explicit PM ruling ("not urgent… wait til they try and fail", G-U5) without stating or engaging that rationale. (2) Step 3, "let DB-only actions pass the key gate", buys little: C-02 shows "add a todo" and "show my todos" need the LLM classifier, so keyless chat needs the deterministic pre-classifier extended **or operator-paid LLM spend**. That cost is unstated. (3) "September invitee stalled at /setup" is cause-ambiguous: G-U5 says the invite was **sent with a dead code**. The §1 line "product-side blockers that explain why the one tester stalled" is causal overreach. (4) "Effectively no users" is record-layer only (check i). |
| **R2** CI gate | **CONFIRMED** | Live API check. "Cost: small" is optimistic for item 6 (457 advisories); list that item separately. |
| **R3** cut coordination | **WEAKENED** | (1) The incident ratio is overstated (check iv). (2) **The target conflicts with R7.** September coordination is mail 1,755 + log 1,416 + hb 2,633 + stop 183 + merge 1,331. Removing every heartbeat and merge still leaves (1,755+1,416+183)/192 ≈ **17.5 per PC**. Reaching <10 needs session-log and mail commits cut too, which R7 protects. (3) A commit-count target is gameable by batching; the synthesis's own method note says commit counts measure granularity. Use bytes or tokens. (4) **Unstated risk:** moving roles to event-triggered wakes removes the liveness signal that caught real silences (178/180 alerts true per F §3). The 09-28 wedge was caught only by that signal. Heartbeats out of git (step 1) is CONFIRMED as the cheapest, safest step. |
| **R4** one PM channel | **Problem CONFIRMED, baseline and cost framing WEAKENED** | (1) 94% of PM-addressed memos are cc, and PM already doesn't read them (708 unread). So "~5.2 h/week reading load" is a cost **if read**, not time PM actually spends. The real cost is writer tokens plus the risk of missed decisions. H1's phrase "PM-addressed reading load" overclaims. (2) The do-nothing baseline of "~1,000+ PM-addressed memos/month" ignores the latest week: 54 of 191 (28%). The 09-11 cc ruling is now biting. (3) "<10% leads to a decision" rests on a filename and subject regex plus decisions.log mentions. Mark it low-confidence. |
| **R5** security | **CONFIRMED, cost of item 5 understated** | Confirmed: commit `7941ae4b97` (07-09) carries a tester name and a full invite token in its subject and is in snapshot history; `?token=` exists at `services/auth/auth_middleware.py:468`; mailboxes are 21,312 / 35,840 tracked paths (59.5%); `data/postgres` is 2,119 files, 88.0 MB (83.9 MiB). **Missing cost:** item 5 (mailboxes out of the public repo) breaks `mail-send.sh` push-to-ref, the session-start mailbox reads and every skill that reads `mailboxes/`. R7 protects exactly that. Scope it as a separate project, or move to a private repo with the same layout. |
| **R6** ruleset | **CONFIRMED on problem; one cited reason WEAKENED** | Load numbers reproduce. Drop or reword the PreCompact "drift" bullet (H2). Settings at the snapshot do allow-list `Bash(git:*)` and `Bash(git stash:*)` (V1 read `.claude/settings.json`), so step 1 is well-founded. The success metric ("load < 40k") measures protocol text, not observed reads. Name that layer. |
| **R7** surface, keep list | **WEAKENED on one cited figure** | "GitHub-first tracking (~96% of commits reference issues)" is wrong twice. E measured **feat/fix commits touching services**, not all commits. E's own table shows **2026Q3 = 151/349 (43%)**; ~96% was Q1–Q2. "Still practiced" needs that qualifier. The strategy calls are PM judgement; no refutation. |

---

## 5. Bias check

The synthesis is visibly careful in places: it caveats the degenerate H1 baseline, labels H4 inconclusive, and
keeps a "keep" list. Even so, where the evidence was ambiguous, it was framed toward "too much process" in at least
five places:

1. **Defect trend.** The exec bullet "defects rose as mechanisms were added" leans on a d1 series that is wholly
   contaminated in September. No one inspected the "revert" subjects.
2. **Caused versus caught.** Incidents are counted one by one while 178 true watchdog alerts count as one bullet.
   The incident sources are failure logs by design.
3. **PM load.** It is presented as hours of reading, though PM demonstrably doesn't read (that is F's own finding).
   The baseline projects 1,000+/month while the latest week shows the cc ruling working.
4. **"No users" as fact.** The users finding is stated as fact in the exec summary, although production was not
   observed. The tester stall is attributed to product gates when the record shows a dead invite code.
5. **Commit counts as cost.** Headline multipliers (48×, 266×, 94.6×) are commit counts, which the method section
   itself says measure granularity. The bytes-based ratio (9.95×) is smaller and fairer.

Counter-tilt, favouring the keep list: the ~96% GitHub-first figure is stale (Q3 = 43%).

**Nothing would directly harm users if acted on.** Two items carry real risk if executed literally:
- R3 step 2 removes liveness detection.
- R5 item 5 breaks mail tooling that R7 protects.

R1 overrides a PM ruling, which should be surfaced as a decision for PM rather than presented as a fact.

---

## 6. Edits the synthesis must make

1. **Exec bullet 5 and H4 row.** Replace "Defects per PC rose 0.21 → 0.58" with "d2 (fix-on-fix) per PC rose
   0.21 → 0.41; d1 is unusable in Jun–Sep (Sep: 33 of 33 matches are coordination subjects such as 'cadence
   reverted'); d2 tracks a fix-share rise of 0.40 → 0.60". Soften "rose rather than fell" to "did not fall". Ask
   D0 to fix d1 (require `^Revert "` or a code path) and re-run the ITS table.
2. **Exec bullet 1 and R1.** Write "Records show one external hosted session in four months; production users
   table not checked." Run the prod SQL before R1 is acted on.
3. **R1.**
   - State PM's 09-21 deferral ruling ("wait til they try and fail") and argue against it explicitly.
   - Add that step 3 needs the pre-classifier extended or operator-funded classification (C-02), with that cost.
   - Change "stalled at /setup" to "was sent a dead code and never submitted".
   - Delete "explain why the one tester stalled" in §1.
4. **R3.**
   - Restate the incident claim as about 10–15 machinery-caused incidents, against a watchdog with 178/180 true
     alerts (late) and few other recorded catches.
   - Replace the "coordination commits per PC < 10" target with a bytes or tokens target, or reconcile it with R7.
     Even zero heartbeats and merges leaves ~17.5 per PC.
   - Add the liveness-loss risk to step 2.
5. **R4 and H1.**
   - Call the 5.2 h "if read" and note that 94% of PM-addressed memos are cc.
   - Update the do-nothing baseline with the latest week (54 PM-addressed, 28%).
   - Mark "<10% produce a decision" as a heuristic.
6. **R5.** Add the cost and conflict of item 5: it breaks `mail-send.sh` and the mailbox reads that R7 protects.
7. **R6 and H2.** Remove or reword the PreCompact "drift" claim (it is registered at user level by design). Soften
   DP-4 from "contradicts its HARD RULE" to "conflicts with the worktree/push rules".
8. **R7.** Replace "~96% of commits reference issues" with "96–97% of feat/fix service commits in Q1–Q2 2026,
   falling to 43% in Q3 (E §4.1)".
9. **H4 "buys".** Say "co-occurs with". Note these practices predate the coordination machinery (feat test
   co-commit was 93% in 2026Q1).
10. **H1.** Lead the magnitude with the bytes ratio (9.95×), not commit multipliers. Say the
    capacity-competition claim is inferred from one account in one week, with no measured coordination token
    share.
11. **H3.** Add "16 of 60 sampled claims uncheckable".
12. **D-propose and R6 step 5.** Note that the slim CLAUDE.md drops STOP conditions #8 (completion bias) and #10
    (report 75%-complete code). Restore them or record the drop as deliberate.

---

Verified how:
- **Method:**
  - Own scripts `metrics/V1-history.py` and `metrics/V1-mail.py`, which do not use `common.py`. They read git
    history and the mailbox tree at a191856 via `git log` and `git cat-file`.
  - `git show` / `git grep` / `git ls-tree` at the snapshot.
  - Re-ran 4 metrics scripts in the scratchpad and diffed the outputs.
  - A live `gh api` query of test.yml runs.
- **Layer:** git-history, static repo text and the CI API. No production DB, no live hooks, no LLM paths.
- **Denominator:**
  - 4 of 4 requested headline re-derivations (7 sub-numbers);
  - 4 metrics scripts out of ~40 in `metrics/`;
  - 3 of 56 unreachable modules;
  - 8 of 25 F incidents;
  - 10 of 17 safety rules;
  - all 7 recommendations and 5 hypothesis rows.
