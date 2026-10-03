---
type: evaluation-report
title: "Piper Morgan, fresh-eyes evaluation: synthesis (DRAFT, pre-verification)"
author: spec (Special Assignments), cloud session
date: 2026-10-03
status: DRAFT. Phase 4 independent verification has not run yet. The numbers here are working results.
snapshot: product a191856 · website 16dfe5fa · skunkworks 829746f3
---

# Should we change anything we are doing right now?

**Yes.** The project has built a capable machine for building software. It points that machine mostly at
itself, and very little at users.

The core evidence:
- One external person has used the hosted product in four months.
- CI on main has not been green since 2026-09-20.
- The PM receives about 78k words of agent mail a week, and fewer than 10% of it leads to a decision.
- Total commits grew about 48 times (coordination commits about 266 times) while product commits grew about 2.7 times.
- Defects per product change rose rather than fell as the process mechanisms were added.

The craft inside the code and process is real: features ship with tests 93% of the time, issue closure is
honest, and the mail tooling is structurally safe. **The recommendation is to redirect, not to tear down.**
Put users and a working CI gate first. Then cut the coordination machinery and the ruleset down to what
demonstrably earns its cost.

Every claim below cites a workstream report in `dev/2026/10/03/spec-eval/` by finding id, along with the
layer it was measured at and its denominator.

---

## 1. Verdicts on the pre-registered hypotheses

The rules for each verdict were fixed in `preregistration.md` before any history script ran.

| Hypothesis | Literal pre-registered verdict | What it actually means | Confidence |
|---|---|---|---|
| **H1: coordination cost dominates** | **Supported.** C/P rose 94.6× from B to R. Product changes grew 2.72× while coordination commits grew 266×. (D0 §1) | Criterion (a) is degenerate: the baseline window has almost no mail/log/heartbeat commits, because those conventions didn't exist yet. So **the 94.6× is real but proves less than it looks.** Independent measures agree on direction: 62–90% of each standing role's commits are coordination (F1.1); the PM-addressed reading load is ~5.2 h/week (F2.1); the cohort ran at 96% of its 7-day subscription cap (F §6), so coordination competes with product work for capacity. Product output did grow (PCs ~70/month in Jan–Mar → ~190/month in Aug–Sep; lines ~1.6×), so this is overhead, not stagnation. | Medium–high on direction; low on the magnitude |
| **H1b: redundancy** (PM-added) | **Partially supported.** Shared reading is 94% of session-start load (D-2). Overlapping PM-facing outputs: yes under a lenient reading, no under a strict one (F §2). Duplicate watchers: no. | The redundancy isn't literal duplication. It shows up in three places: (1) **one 40k-token briefing that every role is told to load** (65% of base load, D-1); (2) **several PM-facing streams covering the same ground**, so the PM's real channel has become the rollup while 708 memos sit unread (F1.4); (3) **~20 watchers, one added per incident** (proliferation, F §3). | Medium |
| **H2: the ruleset is costly and a poor fit for current models** | **Supported** on M2.1 (~62k tokens, rising to 84–96k at a fire), M2.2 (50 defects), M2.4 (5 re-violated rules, exactly at the bar). M2.3 fails by line count (11–14% narrative). | The cost is **load volume and contradictions**, not narrative style. CLAUDE.md contradicts its own HARD RULE in two places (DP-4). The most-violated rule has no mechanism, and the settings even allow-list the commands it forbids (DP-3). | High |
| **H3: docs have drifted from reality** | **Supported, marginally:** 35/44 = 79.5% hold fully (threshold <80%; 95% CI 65–89%) (L-1). | Paths, ports and mechanisms are reliable. Status lines, dated counts and secondary docs drift (L-2). Front-matter freshness dates give a false all-clear (L-4). This is a hygiene problem, not a crisis. | Medium (one claim either way flips it) |
| **H4: the process buys quality** (counter-hypothesis) | **Inconclusive** under the model-confound clause. The literal rule passes on 3 windows, all from one Feb–Apr 2026 episode. (D0 §3) | **No evidence that the added mechanisms reduced defects.** Defects per PC (d1+d2 proxies) **rose from 0.21 (Mar) to 0.58 (Sep)**, and 15 of 23 mechanism windows show a rise. These are proxies, and the trend is confounded by model changes and volume. So the claim is not "the process causes defects." It is: **the burden of proof for keeping a mechanism now sits with the mechanism.** Things the process does demonstrably buy: test co-commit 93% (E-4), honest issue closure (0/40 closed-not-done, G-B5), 97.6% session-log coverage (D-5), and structurally safe mail (`mail-send.sh`). | Medium |

**Drift from the pre-registered calls.** A, B and C each committed their own top 5 before reading any docs.
Here is what happened to those calls once the docs were read:
- **Survived into recommendations:**
  - B #1 (CI red, deploy ungated) → R2.
  - C #1 and #2 (chat gated on the user's key; no signup without a validated key) → R1.
  - A #3 (leaked Gemini key) → R5.
- **Weakened by Spec's own verification:** A #1, setup-route exposure. All three write routes carry the #1504
  instance-wide lockout, so exposure depends on whether production has any user with `setup_complete`.
  Production is unverified (V-A1).
- **Demoted to the appendix:** A #4/#5 (routing complexity, dead code) and C #3–#5 (error copy, API drift,
  health tooling). Each is real, but none ranks above "nobody is using it."
- **What only the context-aware phase could see:** the absence of users (G), the PM-attention load (F), and the
  ruleset's own contradictions (D). Code alone could not have surfaced the top recommendation. The code-first
  phase did surface the product-side blockers that explain *why* the one tester stalled.

---

## 2. Recommendations (7; ranked; each must beat "do nothing for 30 days")

**Do-nothing baseline.** Projected from the R-window trend:
- 0–1 external user sessions a month
- CI red, with deploys continuing ungated
- ~1,000+ PM-addressed memos a month
- session-start load ~84–96k tokens per fire
- d1+d2 per PC flat-to-rising
- the cohort pinned at its subscription ceiling

### R1. Put real users in front of the product within 30 days
- **Why:** One external hosted session in four months (G1). The September invitee stalled at `/setup` (G-U3).
  Chat refuses everything, including deterministic actions, without the user's own LLM key (C #1). An invitee
  cannot sign up without a validated key and a full infrastructure check (C #2). There is no feedback button,
  although `/api/v1/feedback` exists (G-U6). 5 of 9 issues from the one tester's first run are still open (G-U4).
- **Change:**
  1. Reissue invite codes now.
  2. Decouple signup from LLM-key validation and from the infrastructure check.
  3. Let DB-only actions (todos, lists, projects) pass the key gate.
  4. Wire the existing feedback endpoint into the UI, with a named owner and a weekly read.
  5. Close the remaining first-run issues (nav hidden in the avatar menu first).
- **Evidence layer:** live server run plus records. **Confidence:** high that this is the binding constraint;
  medium that these specific fixes are sufficient.
- **Cost:** small to medium; mostly existing code paths. **Reversible:** yes.
- **Owner:** PM (invites), Lead Dev (gates), CXO (FTUX).
- **First step this week:** PM reissues codes to 3–5 people; Lead removes the signup key gate.
- **Success metric:** ≥3 external people reach a first useful session, and ≥1 piece of in-product feedback is
  received and triaged. **Review:** 2026-11-03.

### R2. Make CI a real gate again
- **Why:** `Tests` on main has 0 successes since 2026-09-20 (83 failed and 17 cancelled of the last 100). Smoke
  fails, so the full suite is skipped, and Fly staging deploys regardless (B #1). The weekly live-model e2e
  failed 99/100 (B #2). 457 advisories across 45 packages, with no vulnerability scan in CI (B #3).
- **Change:**
  1. Fix the 3 smoke failures: the TODO ratchet (36>35), user-cleanup FK coverage, and the env-dependent Slack test.
  2. Fix the mypy ceilings.
  3. Make deploy jobs `needs:` the test job.
  4. Find out why the weekly e2e fails (dead secret or real regression).
  5. Retire the 16 stale `test_multi_intent` tests (#1595).
  6. Add `pip-audit` to CI, then bump request-path packages.
  7. Fix the schema-drift validator, which produces 42 false positives.
- **Confidence:** high. **Cost:** small. **Reversible:** yes. **Owner:** Lead Dev.
- **First step this week:** the 3 smoke fixes plus `needs:` on deploy.
- **Success metric:** `Tests` green on ≥90% of main pushes for 14 consecutive days; no deploy without green tests.
  **Review:** 2026-10-24.

### R3. Cut the coordination machinery to what earns its keep
- **Why:**
  - 62–90% of standing roles' commits are coordination (F1.1). One role wrote 1,026 heartbeat commits in 4 weeks (F1.2).
  - ≥25 recorded incidents were caused by the machinery, against ~4–6 recorded catches (F §4).
  - The cohort is at its subscription ceiling (F §6).
  - The "multi-agent coordination" pillar has turned into volume with no measured cross-validation (E-5).
  - The burden-of-proof framing (H4) applies.
- **Change**, staged and in this order:
  1. Take heartbeats out of git: write to a non-committed store, or one overwritten file.
  2. Move most standing roles from cron duty cycles to event- or issue-triggered wakes. Keep cron only where a
     role has demonstrably time-driven work.
  3. Retire watchers that have false-clear histories, or consolidate them.
  4. Make every new mechanism carry a stated cost, a measured benefit and a review date. The default is
     sunset unless it is renewed.

  Do **not** remove `mail-send.sh`, session logs, or issue-closure discipline (see R7).
- **Confidence:** medium. It is a lever on capacity and PM attention; quality effects are unproven either way.
- **Cost:** medium (coordination redesign). **Reversible:** yes, through the registry and cron entries.
- **Owner:** Exec, with CIO.
- **First step this week:** move heartbeats out of git for every seat.
- **Success metric:**
  - coordination commits per PC fall from ~38 to <10 within 30 days;
  - d1+d2 per PC does not rise;
  - PCs per month do not fall.

  **Review:** 2026-11-03.

### R4. One PM channel, and the PM's reading time capped
- **Why:**
  - 82% of 1,899 memos in 8 weeks addressed the PM: ~78k words/week, about 5.2 h (F2.1).
  - Fewer than 10% produce a decision.
  - 708 memos have been unread since 09-11 (F1.4).
  - The 09-11 cc ruling took about 3 weeks to take effect.
  - Several PM-facing streams cover the same ground (H1b).
- **Change:** the attention rollup becomes the **only** default PM channel, capped at one page a day.
  - Memos to the PM are reserved for decisions, written as one item per question with an a-or-b choice.
  - Consolidate the omnibus, current-state, Ship and rollup into a defined set with non-overlapping jobs.
  - Inventory the Cowork jobs on the PM's machine (unobservable here) and fold them in or stop them.
- **Confidence:** high on the problem; medium on the exact remedy. **Cost:** small. **Reversible:** yes.
- **Owner:** Exec.
- **First step this week:** Exec publishes the channel rule and the consolidated list.
- **Success metric:** PM-addressed words below 10k/week; time from decision request to PM ruling falls (baseline to
  be measured by Exec). **Review:** 2026-11-03.

### R5. Security and public-repo hygiene, now
- **Why:**
  - A Gemini API key sat in public history from 2025-10 to 2026-09 (A #3).
  - A tester's full invite token is in a **commit subject** on main (`7941ae4b97`; V-G1). The bearer lint only
    checks files, so it can't catch this.
  - JWTs are accepted through a `?token=` query parameter, and a hardcoded fallback JWT secret is refused
    only when env is literally "production" (A #5).
  - There are 21,312 mailbox files (59% of tracked files) in a public repo, holding 17 non-noreply email
    addresses and names (F6).
  - An 85 MB Postgres data directory is tracked (A).
  - Production `setup_complete` state is unverified (V-A1).
- **Change:**
  1. Rotate the Gemini key and revoke the leaked invite token if they are still live.
  2. Run the one-line production check (`SELECT count(*) FROM users WHERE setup_complete`).
  3. Remove the `?token=` path and the fallback secret.
  4. Extend the bearer check to commit messages; the autoclose guard already reads messages.
  5. Move mailboxes (and the tracked pgdata) out of the public repo into private storage. History rewrite is a
     separate, PM-gated decision.
- **Confidence:** high. **Cost:** small (items 1–4); medium (item 5). **Reversible:** items 1–4 yes; item 5
  partly (history persists).
- **Owner:** Lead Dev and HOST; PM for item 5.
- **First step this week:** items 1–2.
- **Success metric:** checklist done; secret scan of tree and messages clean. **Review:** 2026-10-17.

### R6. Refactor the ruleset: mechanize first, then cut, and test before adopting
- **Why:**
  - ~62k tokens are written into every session start; 84–96k at a fire (D-1).
  - BRIEFING-CURRENT-STATE alone is 40k tokens, 65% of the base load.
  - 50 defects (D-3).
  - The most-violated safety rule is prose-only and allow-listed in settings (DP-3/M-1).
  - Two self-contradictions need a PM ruling (DP-4).
  - Hook registration has drifted: the PreCompact hook CLAUDE.md calls "confirmed firing" has no registration in
    repo settings (D-6, F).
  - The Oct 2026 tooling (`/checkup prompt-audit`, mods) makes this the right moment.
- **Change**, in D-propose's staged order (D-propose §7):
  1. A PreToolUse guard against destructive git in the PM's checkout, plus removing the `git stash:*` and
     `git:*` allow-list entries. No mods are needed for this.
  2. PM rulings on the two contradictions.
  3. Drop BRIEFING-CURRENT-STATE from required session-start reading; slim it to a short current block.
  4. Fix the 50 defects, skills first.
  5. Adopt the slim CLAUDE.md (~3k tokens, all 17 safety rules kept) **only after the 10-scenario probe suite
     passes**.
  6. Upgrade the Amber CLI to ≥2.1.287 and consolidate the guards into one mods plugin.
- **Confidence:** high on the problem; medium on the rewrite until it is probe-tested.
- **Cost:** medium. **Reversible:** yes (git revert per step).
- **Owner:** CIO and Docs, with a PM ruling on step 2.
- **First step this week:** step 1, plus the PM ruling.
- **Success metric:**
  - session-start load per cycling fire below 40k tokens;
  - 0 destructive-git incidents;
  - prompt-audit defects below 10;
  - the probe suite passes after each stage.

  **Review:** 2026-11-17.

### R7. Decide the product's primary surface. Keep what works.
- **Why:**
  - The ratified primary surface (hosted MCP plus plugin, PDR-006) is at 3/15 acceptance criteria with 1
    read-only tool, while effort goes to the web chat and its routing (G #3).
  - Intent routing is ~55k LOC, 29% of production code (A #4).
  - Thesis risk is high: a first-party PM plugin, open directory publishing and Claude memory already cover
    much of the persona and methodology (G #4).
  - Piper's defensible core is cross-client persisted PM state plus safe write tools.
  - No single document says what "beta" is (G #6).
- **Change:**
  1. PM ruling: is the web app the MVP or the thin secondary surface? Re-order the epics to match.
  2. Run a cheap demand test: publish the existing skills plus the MCP server to the Claude directory.
  3. Write a one-paragraph beta definition.
  4. Stop and archive skunkworks (G #7).
  5. Fix the website's stale alpha and deploy copy.
- **Keep, explicitly, and protect from the cuts in R3 and R6:**
  - test-with-feature co-commits (93%)
  - honest issue closure
  - session logs as the single durable record
  - `mail-send.sh` push-to-ref
  - GitHub-first tracking (~96% of commits reference issues). This is the forgotten fourth pillar, and it is
    still practiced.
- **Confidence:** medium (strategy calls rest with the PM). **Cost:** small to decide, variable to execute.
  **Reversible:** yes.
- **Owner:** PM with PPM.
- **First step this week:** the PM ruling memo.
- **Success metric:** the ruling is recorded; the plugin is listed or explicitly declined; the beta definition
  exists. **Review:** 2026-11-03.

---

## 3. The Excellence Flywheel (PM asked for its history)

- **Origin:** the name was coined 2025-07-24 (`f351d90f05`) as a causal loop: foundation-first → verification →
  multi-agent → accelerated delivery → more foundation.
- **The original four pillars**, canonized three days later (methodology-00, `a4afeaab29`, 2025-07-27), were:
  1. Systematic Verification First
  2. Test-Driven Development
  3. Multi-Agent Coordination
  4. **GitHub-First Tracking** (the one PM couldn't recall)
- **Drift:** it silently became five pillars on 2025-08-18, and there were eight formulations by April 2026.
  v2.0 and v3.0 replaced the pillars with "Five Practices." "Flywheel" now also names the duty-cycle loop.
- **The public methodology page** lists a different set of five and hasn't been updated since (E-1, E-2, E-6).
- **Stated versus practiced:**
  - Verification is practiced in prose and partly mechanized.
  - TDD became "tests ship with features" (93%), but CI enforcement has lapsed.
  - Multi-agent coordination has turned into coordination volume.
  - GitHub tracking is practiced.
- **Re-evaluations so far fixed the text, not the behavior (E-3).** This evaluation's recommendations carry
  success metrics and review dates for that reason.

---

## 4. What we could not observe (test plan)

The full list is in `unobservables.md` plus each report's Unobservables section. The ones that matter most:

| Gap | Why it matters | How to observe |
|---|---|---|
| LLM-backed chat, classification and synthesis | It is the main product surface | Re-run C's chat probes with `PIPER_TEST_ANTHROPIC_API_KEY`: a fresh cloud session, see the handoff |
| Production state: users, `setup_complete`, env vars | Gates R1 and R5 | Lead/PM run read-only SQL and `fly secrets list` (names only) |
| Cowork scheduled jobs on the PM's machine | H1b / R4 | The PM or Exec lists them |
| Dollar running cost (LLM, Fly, Amber) | R3 sizing | PM billing pages |
| Live hook firing on Amber seats; CLI version | R6 steps 1 and 6 | One seat runs a probe commit and `claude --version` |
| CI job logs (root cause of the weekly e2e) | R2 | Lead pulls full logs |

---

## 5. Method notes and limits

- **Order:** code first, then docs, with pre-registration. The harness injects CLAUDE.md into subagents, so
  the "cold" phase was code-first ordering, not a clean firewall.
- **Proxies:** commit-subject classes and d1/d2 are proxies. Commit counts measure granularity, not work.
- **One synthesizer.** Mitigated by Phase 4 (two independent verifiers re-deriving numbers with their own scripts).
- **Spec's own process errors, all caught and corrected** (session log):
  - pytest addopts override
  - `pkill` matching itself
  - a shared database between B and C
  - a tar exclude that dropped `services/knowledge`
  - a lint hit on a token copied from a public commit subject
- **Spend at the end of Phase 2:** $48 of $250 credit (PM's usage page).
