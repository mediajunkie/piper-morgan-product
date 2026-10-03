---
type: evaluation-report
title: "Piper Morgan — fresh-eyes project evaluation (2026-10)"
author: spec (Special Assignments), cloud session, commissioned by PM
date: 2026-10-03
version: 1.0 (post-verification)
status: FINAL for PM review. Recommendations are proposals; nothing has been changed in the project.
snapshot: product a191856 · website 16dfe5fa · skunkworks 829746f3
evidence: dev/2026/10/03/spec-eval/ (11 workstream reports, metrics/ scripts and CSVs, 2 verification reports)
---

# Should we change anything we are doing right now?

**Yes, but less drastically than a first read suggests.** The project has built a capable engineering
machine whose craft is real:
- tests ship alongside features (93%);
- issue closure is honest (0 of 40 sampled closures lacked the work);
- the mail tooling is structurally safe.

Most of that machine's output now goes into coordinating itself, while the product has almost no external
use and its CI gate has been off for two weeks.

**The recommendation is to redirect, not to tear down.** In order:
1. Settle whether real users come now or later. This is your call to revisit.
2. Make CI a real gate.
3. Do the security hygiene.
4. Trim the coordination machinery and the ruleset carefully, with replacements in place before anything is
   removed.

**Key evidence.** All of it was independently re-derived by a verifier unless marked otherwise:
- **Users.** The records show one external session on the hosted alpha in four months, and no issue from an
  outside user. The production users table was **not** checked.
- **CI.** The `Tests` workflow on main last passed on **2026-09-20** (run 3753, confirmed live). Since then the
  smoke job fails, the full suite is skipped, and staging deploys anyway.
- **Growth.** Product commits rose from about 70 to about 190 a month (Jan–Mar → Aug–Sep 2026). That is 2.7×
  from a low baseline, or about 1.5× against the 12-month mean. Over the same period, coordination bytes per
  product line rose about **10×**.
- **Mail to PM.** 82% of 1,899 memos in eight weeks were addressed to PM, about 78k words a week **if read**.
  94% of those were cc's, 708 sit unread, and the cc share fell to 28% in the latest week after your 09-11
  ruling.
- **Defects.** There is no evidence that the process mechanisms reduced defects. The fix-on-fix rate per product
  change did not fall (0.21 → 0.41, Mar → Sep). That rise tracks fix work growing from 40% to 60% of the mix, so
  it is not a quality verdict either way.

Every claim below cites a workstream finding id and states the layer it was measured at and its denominator.

---

## 1. Verdicts on the pre-registered hypotheses

The rules for each verdict were fixed in `preregistration.md` before any history script ran. Verifier status:
V1 is the adversarial re-derivation, V2 the steelman of the current process.

| Hypothesis | Verdict | What it actually means | V1 / V2 |
|---|---|---|---|
| **H1: coordination cost dominates** | **Supported on direction; magnitude modest.** The literal rule passes (C/P 94.6×), but that multiple is degenerate because the baseline had almost no mail/log/heartbeat commits. Commit counts measure granularity. **On bytes, coordination per product line grew ~9.95×.** | 62–90% of each standing role's commits are coordination (F1.1), and 38% of September's coordination commits are automated one-liners (V2). The claim that coordination competes with product for subscription capacity is **inferred** from one account at 96% of its 7-day cap in one week (the other account was at 76%). Nobody has measured coordination's share of tokens. | Confirmed on direction; magnitude weakened / qualified |
| **H1b: redundancy** (added by PM) | **Partially supported.** | The redundancy is not literal duplication. It sits in three places: one 40k-token briefing every role is told to load (65% of base session-start load, D-1); several PM-facing streams with overlapping content under a lenient reading (F §2); and about 20 watchers, added one per incident (proliferation, F §3). | Confirmed / survives |
| **H2: the ruleset is costly and a poor fit for current models** | **Supported** on load (CLAUDE.md 16.3k tokens + CURRENT-STATE 40.5k, reproduced), 50 defects (D-3) and 5 rules violated again after being written (exactly at the bar). Narrative share by line (11–14%) fails its sub-test. | The cost is **volume and inconsistency**, not prose style. The most-violated safety rule has no mechanism, and the settings allow-list `git:*` and `git stash:*` (V1 confirmed). The sign-off checklist conflicts with the worktree/push rules. | Confirmed; two sub-claims corrected (see §5) |
| **H3: docs have drifted from reality** | **Supported, marginally.** 35 of 44 checkable claims hold fully, which is 79.5% against a <80% threshold (95% CI 65–89%). 16 of 60 sampled claims could not be checked. | Paths, ports and mechanisms are reliable. Drift is in status lines, dated counts and secondary docs (L-2). Front-matter freshness dates give a false all-clear (L-4). | Confirmed |
| **H4: the process buys quality** (counter-hypothesis) | **Inconclusive** under the model-confound clause. | The d1 (revert) series is unusable from June on. All 33 September "reverts" are coordination subjects such as "cadence reverted", none touching code (V1). d2 (fix-on-fix) per product change went 0.21 → 0.41, from a local low (December 2025 was already 0.43, V2), tracking fix share. **So the process did not measurably reduce defects, and the data cannot show it harmed quality.** The good practices **co-occur with** the process but **predate** the coordination machinery: test co-commit was already 93% in 2026Q1. That shifts the burden of proof onto each mechanism, which is why R3 says "replace first, then remove", not "cut". | Verdict confirmed; narrative corrected |

**Drift of the pre-registered calls** (A, B and C wrote their top 5 before reading any docs):
- **Survived into recommendations:**
  - B #1, CI red with deploy ungated → R2.
  - C #1/#2, chat gated on the user's own key and signup requiring a validated key → R1 (qualified).
  - A #3, leaked Gemini key → R5.
- **Weakened by verification:**
  - A #1, setup-route exposure. An instance-wide lockout guards all three write routes, so exposure depends on
    production's `setup_complete` state, which was not checked (V-A1).
- **Moved to the appendix:**
  - A #4/#5, routing complexity and unreachable code (3 of 3 spot-checked modules confirmed reachable only from
    tests).
  - C #3–#5, error copy, API contract drift and health tooling.
- **Visible only once docs were read:**
  - the users question (G);
  - PM attention (F);
  - the ruleset's internal conflicts (D).

The code-first phase found the product-side gates that would block a new user. **It did not establish that
those gates are why the one invitee stalled. The record shows that invitee was sent a dead code** (G-U5).

---

## 2. Recommendations

There are 7, ranked. Each must beat "do nothing for 30 days."

**Do-nothing baseline** (projected from the latest data):
- 0–1 external sessions a month;
- CI red and deploys ungated;
- PM-addressed memos running at about 68–390 a week over the last 13 weeks, now falling (cc ruling biting);
- session-start protocol load of about 84–96k tokens per cycling fire;
- fix-on-fix rate per product change flat;
- one account near its subscription cap.

### R1. Revisit the user-sequencing decision; if users come now, remove the two gates first
- **Why.** The records show one external hosted session in four months and no issue filed by an outside user
  (G1). The production users table was not checked (V1). In September **you explicitly deferred** chasing testers
  ("not urgent… wait til they try and fail"; beta and MCP ahead of testers, decisions.log / G-U5).

  This recommendation **argues against that ruling**. Every week without external use, the team optimizes against
  its own model of a user. The one tester's first-run issues are still 5 of 9 open after about 8 weeks (G-U4).
  An 11-respondent agent self-survey runs on a cycle while no in-product feedback route exists (G-U6/U7).

  The counter-argument V2 surfaced is fair: users can be wasted on an unready product. That is why step 1 is a
  decision, not an action.
- **Blocker found with the live LLM probe (C-LLM, verified by Spec):** Piper's own key validator
  (`services/security/provider_key_validator.py:49`, `^sk-ant-[A-Za-z0-9\-_]{100,}$`) **rejects a valid, working,
  current Anthropic key**: the test key has 99 characters after `sk-ant-`. A new user bringing a normal key may be
  unable to complete setup. This applies whichever way the sequencing decision goes; fix it first.
- **Change.**
  0. **Fix the key validator now.** Loosen the length rule, or validate with a live API call.
  1. **PM decision:** users now or after a named milestone? If after, name the milestone and its date.
  2. If now: decouple signup from LLM-key validation and the infrastructure check (C-04).
  3. Wire the existing `/api/v1/feedback` endpoint into the UI, with an owner and a weekly read.
  4. Close the open first-run issues, starting with the nav hidden in the avatar menu.
  5. Reissue codes, live ones this time.
  6. **Keyless chat is not a cheap win.** "Add a todo" and "show my todos" need the LLM classifier (C-02). Either
     extend the deterministic pre-classifier or decide to pay operator-side LLM cost for new users. That cost is
     unpriced; Lead to estimate.
- **Confidence:** high that external use is the binding uncertainty; medium on the specific fixes.
- **Cost:** small (steps 2–5), unknown (step 6). **Reversible:** yes.
- **Owner:** PM (step 1), Lead (steps 2, 6), CXO (steps 3–4).
- **First step this week:** PM ruling. **Before acting, run one read-only production query** for user count and
  last activity.
- **Metric:** if "now", ≥3 external people reach a first useful session and ≥1 in-product feedback item is
  triaged by 2026-11-03.

### R2. Make CI a real gate again
- **Why.** `Tests` on main: 0 successes since 2026-09-20 (confirmed live by V1). Smoke fails, the full suite is
  skipped, and Fly staging deploys without `needs:` on tests (B #1). The weekly live-model e2e failed 99 of 100
  (B #2). The 16 `test_multi_intent` failures are stale tests for patterns #1595 deleted. The schema-drift boot
  warning is 42 false positives.
- **Change.**
  1. Fix the 3 smoke failures: the TODO ratchet at 36 against a limit of 35, user-cleanup FK coverage, and the
     env-dependent Slack test.
  2. Fix the mypy ceilings.
  3. Add `needs: test` to deploy.
  4. Diagnose the weekly e2e (dead secret vs regression).
  5. Retire or rewrite the stale tests.
  6. Fix the drift validator.
  7. *Separately and later:* add `pip-audit` to CI and work down 457 advisories in 45 packages, request-path
     packages first. **Not small.**
- **Confidence:** high. **Cost:** small for steps 1–6, medium for step 7. **Reversible:** yes. **Owner:** Lead Dev.
- **First step this week:** steps 1 and 3.
- **Metric:** `Tests` green on ≥90% of main pushes for 14 consecutive days, and no deploy without green tests,
  by 2026-10-24.

### R3. Trim the coordination machinery: replace first, then remove
- **Why.**
  - 62–90% of standing roles' commits are coordination (F1.1). One role made 1,026 heartbeat commits in 4 weeks
    (F1.2).
  - The "multi-agent coordination" pillar has become volume with no measured cross-validation (E-5).
  - Per H4, mechanisms have not shown a defect benefit.
  - **But:** the watchdog's alerts were true 178 of 180 times and caught real silences, including the 09-28
    wedge. The incident tally is lopsided by construction: incidents get logged, prevented events don't. V1's
    sample put machinery-caused incidents at about 10–15, not ≥25.
  - Heartbeats feed freeze-check, the watchdog and the rollup (V2).
- **Change**, staged:
  1. **Heartbeats out of git** to a non-committed store. Ship the new reader for freeze-check, watchdog and
     rollup **before** switching. This is the cheapest and safest step, and V1 confirms it.
  2. For roles whose work is event-driven, move from cron to event or issue triggers **only after** a
     replacement liveness signal exists. Otherwise the most reliable watcher disappears.
  3. Consolidate watchers that have false-clear histories.
  4. New mechanisms carry a stated cost, a measured benefit and a sunset or renew date.
- **Do not cut** session logs or `mail-send.sh` (see the R7 keep-list). That is why the target is not a
  commit-count ratio: even with zero heartbeats and merges, September would still have about 17.5 coordination
  commits per product commit, and commit counts can be gamed by batching.
- **Confidence:** medium. **Cost:** medium. **Reversible:** yes (registry and cron). **Owner:** Exec with CIO.
- **First step this week:** spec the heartbeat store and its reader.
- **Metric** (measured in bytes, not commits): coordination bytes written per product line down ≥50% from
  September by 2026-11-03, with product commits per month not falling and no undetected seat silence over 24h.

### R4. One PM channel
- **Why.** 82% of 1,899 memos in 8 weeks addressed PM (V1 reproduced 81.6%), about 78k words a week **if read**.
  In practice 94% were cc's and 708 sit unread (F1.4). The real costs are writer tokens and the risk that a real
  decision request is missed. Several PM-facing streams overlap (H1b). The 09-11 cc ruling is working (28% in the
  latest week). This recommendation finishes that job.
- **Change.**
  - The attention rollup becomes the default PM channel, about one page a day.
  - Memos to PM are only for decisions: one question each, a-or-b.
  - Define non-overlapping jobs for omnibus, current-state, Ship and rollup.
  - Inventory the Cowork jobs on PM's machine (not visible from here).
  - The rollup compiler becomes a single point of failure (V2). Give it a fallback.
- **Confidence:** high on direction. "Fewer than 10% of memos lead to a decision" is a filename/regex heuristic,
  so low confidence on that number.
- **Cost:** small. **Reversible:** yes. **Owner:** Exec.
- **First step this week:** Exec publishes the channel rule.
- **Metric:** ≤10 decision memos a week to PM, each answered within 3 days, by 2026-11-03.

### R5. Security and public-repo hygiene
- **Why** (each item confirmed by V1 unless noted):
  - A Gemini API key sat in public history from 2025-10 to 2026-09. It is unknown whether it was rotated (A #3).
  - A tester's name and full invite token are in a **commit subject** on main (`7941ae4b97`). The bearer lint
    checks files, not commit messages (V-G1).
  - `?token=` JWT is accepted at `auth_middleware.py:468`, and there is a hardcoded fallback JWT secret (A #5).
  - 21,312 mailbox files (59.5% of tracked files), containing third-party emails and names, are in a public repo.
  - `data/postgres` (88 MB) is tracked.
  - Production `setup_complete` state was not checked (V-A1).
- **Change.**
  1. Rotate the Gemini key, and revoke the leaked invite token if it is still live.
  2. Run the read-only production check (`SELECT count(*) FROM users WHERE setup_complete`).
  3. Remove `?token=` and the fallback secret.
  4. Extend the bearer check to commit messages. The autoclose guard already reads messages.
  5. **A separate PM-gated project:** move mailboxes and pgdata into a private repo with the same layout. Moving
     them out naively breaks `mail-send.sh`, session-start mailbox reads and skills that R7 protects. History
     rewrite is a further decision.
- **Confidence:** high. **Cost:** small (1–4), medium–large (5). **Reversible:** 1–4 yes; history persists.
- **Owner:** Lead Dev and HOST; PM for item 5.
- **First step this week:** items 1 and 2.
- **Metric:** checklist complete, and the tree and commit-message scan clean, by 2026-10-17.

### R6. Refactor the ruleset: mechanize first, then cut, and probe-test before adopting
- **Why.**
  - The protocol text loaded at session start is about 62k tokens, and 84–96k at a duty-cycle fire. This
    measures **protocol text, not observed reads** (D-1).
  - BRIEFING-CURRENT-STATE alone is 40k tokens.
  - 50 defects (D-3); `/checkup prompt-audit` caught 32 that our own scripts missed.
  - The most-violated safety rule is prose-only and allow-listed in settings (DP-3).
  - The sign-off checklist conflicts with the worktree/push rules. It is not on the HARD RULE's list, but it is
    risky in PM's checkout.
  - The Oct 2026 tooling (prompt-audit, mods) makes this the moment.
- **Change**, in D-propose's staged order (§7):
  1. A PreToolUse guard against destructive git in PM's checkout, plus removing the `git:*` and `git stash:*`
     allow entries.
  2. PM ruling on the checklist conflict.
  3. Build a slim shared-state surface, **then** drop CURRENT-STATE from required reading (V2).
  4. Fix the 50 defects, skills first.
  5. Adopt the slim CLAUDE.md (about 3k tokens) **only after** the 10-scenario probe suite passes. Restore STOP
     conditions #8 (completion bias) and #10 (report 75%-complete code), which the draft dropped (V1).
  6. Upgrade Amber to CLI ≥2.1.287 and consolidate the guards into one mods plugin.
- **Note:** the PreCompact hook is registered at user level on Amber by design. "Drift" was our error (V1). Live
  firing remains unverified.
- **Confidence:** high on the problem; medium on the rewrite until it is probe-tested.
- **Cost:** medium. **Reversible:** yes, per step. **Owner:** CIO and Docs, with PM for step 2.
- **First step this week:** step 1.
- **Metric:** protocol load per cycling fire under 40k tokens, 0 destructive-git incidents, prompt-audit defects
  under 10, and the probe suite passing at each stage, by 2026-11-17.

### R7. Decide the primary product surface, and protect what works
- **Why.**
  - The ratified primary surface (hosted MCP + plugin, PDR-006) stands at 3 of 15 acceptance criteria with one
    read-only tool, while effort goes to the web chat (G #3).
  - Intent routing is about 55k LOC, 29% of production code (A #4).
  - Thesis risk is high: a first-party PM plugin, open directory publishing and Claude memory now exist. Piper's
    defensible core is cross-client persisted PM state plus safe write tools (G #4).
  - There is no one-paragraph definition of beta (G #6).
- **Change.**
  1. PM ruling: is the web app the MVP or the secondary surface? Re-order the epics to match.
  2. Run a cheap demand test: publish the existing skills plus MCP to the Claude directory.
  3. Write the beta definition.
  4. Stop and archive skunkworks (G #7).
  5. Fix the website's stale alpha and deploy copy.
- **Keep and protect** from R3 and R6:
  - Test-with-feature co-commits: 93%, steady since 2026Q1.
  - Honest issue closure.
  - Session logs as the durable record. Their coverage was 97.6% in September, and they made this evaluation
    possible.
  - `mail-send.sh` push-to-ref.
  - GitHub-first tracking. It was 96–97% of feat/fix service commits in Q1–Q2 2026 **but fell to 43% in Q3**
    (E §4.1). Restore it.
- **Confidence:** medium; strategy is PM's call. **Owner:** PM with PPM.
- **First step this week:** a PM ruling memo.
- **Metric:** ruling recorded, plugin listed or explicitly declined, and beta defined, by 2026-11-03.

---

## 3. The Excellence Flywheel

- **Coined 2025-07-24** (`f351d90f05`) as a causal loop: foundation-first → verification → multi-agent →
  accelerated delivery → more foundation.
- **Four Pillars canonized three days later** (methodology-00, `a4afeaab29`, 2025-07-27):
  1. Systematic Verification First
  2. Test-Driven Development
  3. Multi-Agent Coordination
  4. **GitHub-First Tracking**, the pillar you couldn't recall
- **Then it drifted.** The pillars silently became five on 2025-08-18, and there were eight formulations by April
  2026. v2.0 and v3.0 recast them as "Five Practices". "Flywheel" also became the name of the duty-cycle loop.
  The public site lists yet another five (E-1, E-2, E-6).
- **Practiced today:**
  - Verification is partly mechanized.
  - TDD became "tests ship with features" (93%), but the CI gate has lapsed.
  - Multi-agent coordination has turned into volume.
  - GitHub-first tracking held until Q3, then dropped to 43%.
- **Past re-evaluations fixed the text, not the behavior (E-3).** That is why every recommendation above carries
  a metric and a review date.

---

## 3a. LLM-backed behavior (observed late, with PM's spend-capped test key)

Source: C-LLM (`spec-eval/C-LLM-probe.md`). Live server, fresh database, real Anthropic model, 53 LLM-backed
requests, one run per phrasing, so variance across runs is not measured.

**What works:**
- With a key, chat works end to end. Todo, reminder and timezone writes executed and were verified via the API.
- Median LLM latency is 4.4 s (maximum 13.9 s). Deterministic handlers answer in about 0.1 s.
- Invalid-key handling is good: clear, actionable messages in under 1 s.

**What fails:**
- **Multi-item requests fail silently.** "Add three todos for the launch…" creates nothing. It is either misrouted to
  a GitHub ticket or classified as `create_todos`, which has no handler.
- **Greeting-prefixed calendar queries never reach the calendar action** (11 of 11 were classified as greeting).
  This confirms B's finding that the 16 `test_multi_intent` tests describe behavior the product no longer has.
- **User-facing false statements**, each an R1/trust issue:
  - "GitHub connected"
  - "no open issues" when no repository could be resolved
  - "nothing created this session" immediately after creating a todo
  - "I don't store your data"

**Testing limitation:** because of the validator bug above, the stored-key path was exercised only with the
`X-User-Api-Key` header, not with a valid stored key.

## 4. What we could not observe (test plan)

| Gap | Matters for | How to observe |
|---|---|---|
| LLM behavior: variance across runs; stored-key path with a valid key; synthesis quality at depth | R1, R7 | Repeat the C-LLM probes several times, after the validator fix |
| Production users, `setup_complete`, env vars | R1, R5 | Lead/PM run read-only SQL and `fly secrets list` (names only) |
| Whether the Gemini key and invite token were rotated | R5 | Lead/HOST |
| Cowork scheduled jobs on PM's machine | R4 | PM / Exec inventory |
| Dollar running cost; token share of coordination vs product | R3, H1 | PM billing pages; per-seat usage |
| Live hook firing and CLI version on Amber seats | R6 | One seat probe |
| CI job logs: root cause of the weekly e2e failure | R2 | Lead pulls full logs |

The full lists are in `unobservables.md` and each report's Unobservables section.

---

## 5. Verification record

- **V1 (Opus, adversarial).**
  - Re-derived 4 of 4 headline figures with its own scripts. All reproduced: product commits 69.7 → 189.5 a
    month, total commits ×48.25, 81.6% / 77.9k words, 16,258 and 40,461 tokens.
  - Reproduced 4 metrics scripts.
  - Confirmed CI red via the live API.
  - Found **12 required edits**, all applied above:
    - d1 contamination;
    - "no users" stated at the wrong layer;
    - R1 overriding a PM ruling without saying so;
    - R1 keyless-chat cost;
    - the dead-code invitee;
    - the incident ratio;
    - the R3 target conflicting with R7;
    - the R4 "if read" framing and baseline;
    - the R5 item-5 cost;
    - the PreCompact claim;
    - the ~96% figure;
    - the dropped STOP conditions.
  - Bias check: the draft leaned toward "too much process" in 5 places. All are corrected.
- **V2 (Sonnet, steelman).**
  - None of the 7 recommendations failed outright.
  - Qualifications applied: H1's trough baseline, H4's local-low start, R1 as PM's sequencing call, R3's
    replace-first ordering, R6's replacement surface, R4's single point of failure.
  - The steelman claim that "the cohort grew throughput" was **not** supported by the data.
- **Spec's own corrections** during the work (session log):
  - the setup-route finding weakened (V-A1);
  - an export bug that dropped `services/knowledge`;
  - a shared test database between two workstreams;
  - a pytest override;
  - a token copied from a public commit subject, now masked.
- **Method limits.**
  - Code-first ordering, not a clean firewall: the harness injects CLAUDE.md.
  - The d1/d2 defect measures and the commit classes are proxies.
  - There was one synthesizer, mitigated by V1 and V2.
- **Spend:** about $50–55 of the $250 cloud credit at this point (PM's usage page read $48 at the end of Phase 2).

## 6. Appendix: findings not ranked above
- Routing: one 1,949-line function, and about 3.2k LOC of dark parallel routing (A-R1–R3).
- About 10.6k LOC unreachable outside tests.
- Error copy misleads at trust-critical moments (C-03/05).
- Silent no-op PUTs, plus a share route that 404s (C-07).
- `main.py status` crashes and then reports "operational" (C-06).
- Docs: PROJECT.md cites the deleted `production` branch, and CI still triggers on it (L-3).
- The roadmap's enterprise date conflicts with the GitHub milestone.
- An e2e test writes into `dev/active/` (stray files in worktrees).
- Website deploy docs reference deleted workflows (G-W1).
