---
type: plan
title: "Fresh-eyes project evaluation: plan"
author: spec (Special Assignments), cloud session
date: 2026-10-03
version: v0.4 (v0.3 + H1b redundancy, PM 10-03; PM answers to open items recorded) (v0.1 audited by an independent Opus subagent, all 10 findings addressed in §9; v0.3 adds the Oct 2026 Claude Code update, §7a)
status: DRAFT for PM review. Nothing in §4 runs until PM approves.
---

# Fresh-eyes project evaluation: plan v0.4

Rendered for review: https://claude.ai/artifact/REnJcehYvTBtkzJW26YdYH

## 1. The question and what counts as an answer

**Guiding question (PM):** *Should we change anything we are doing right now, and if so why and how?*

The deliverable is a decision set, not a survey:
- **At most 7 ranked recommendations.** Each one carries:
  - what to change, and why
  - evidence (with the layer it was measured at and the denominator)
  - confidence
  - cost
  - reversibility
  - owning role
  - the **first step a named role could take this week**
  - a **falsifiable success metric** and a **review date**
- **A "do nothing for 30 days" baseline.** Every recommendation has to beat it explicitly.
- Everything else goes in an appendix of findings, not into the recommendations.
- "Keep X" counts as a valid recommendation. Nothing is exempt from scrutiny, and effort already spent on something is not a reason to keep it.

## 2. Preliminary sweep (measured; auditor re-derived the starred rows)

| Signal | Value | How measured |
|---|---|---|
| ★ Product repo history | 31,307 commits since 2025-06-01. Roughly 450/month until Apr 2026, then 2.2k (May), 4.9k (Jun), 3.8k (Jul), 6.9k (Aug), 10.1k (Sep) | `git log origin/main`, unshallowed |
| ★ Last 90 days by subject prefix (21,154 commits) | mail 4,367 · log ~3.2k · hb-last-invoked 2,034 · hb 1,435 · docs 1,906 · **merges ~2.86k** · stop 492 · feat/fix/refactor/test/perf 876 | Leading word of the subject. **This is a measure of granularity, not of work:** 495 non-merge commits touched services/web in that window. Not used as evidence on its own (§3.3). |
| Code churn, services/web/tests | +169k/−102k in the last 90 days, versus +82k/−48k in the prior 90 | `--numstat` |
| ★ Tracked files | 35.8k total: **mailboxes 21.3k**, dev 7.3k, docs 2.5k, data 2.1k, tests 1.2k, services 477, web 121 | `git ls-files` |
| Code size | services+web ≈ 190k Python LOC; ≈ 469k including tests; 1,009 test files | `wc -l` |
| ★ Ruleset | CLAUDE.md 745 lines / 65 KB (≈16k tokens). 31 briefings, 37 skills, 13 hooks, 25 CI workflows (2 are `.backup`) | `wc`, `ls` |
| Authorship | 17.5k of the last 90 days' commits are authored by `mediajunkie`. **Git author can't tell agents apart**; roles show up only in subject prefixes and log filenames | auditor |
| Product state (docs' claim, **unverified**) | Alpha on Fly (`piper-morgan` v151), v0.8.14.0 | BRIEFING-CURRENT-STATE |
| "Excellence Flywheel" | First appears 2025-07-24/25, rooted in "Systematic Verification First" (`bf869bbcca`). The four pillars have not been recovered yet | `git log -S` |
| Container | docker/psql/python3.11/playwright binaries are present. **But the docker daemon is down, there's no venv, and no LLM key** | auditor: `docker info`, env |

## 3. Method

### 3.1 Code-first ordering (not a "firewall")
In this setup the subagent harness injects the repo's CLAUDE.md, so a clean "cold" read isn't possible and the report won't claim one. What we can do honestly:
- **A, B and C (code/product) work from a `git archive` export with no `.git`, `docs/`, `dev/`, `mailboxes/`, `knowledge/` or `rag/`,** and are told in writing to set aside any injected instructions.
- **Pre-registration.** Before Phase 2 starts, A, B and C each commit a "top 5 things that matter" list. The synthesis then reports how far the warm phase moved those calls. Measuring that drift is what the firewall was meant to protect, and it still gets protected this way.
- **D0 (history instrumentation) is scripts only,** and its outputs are numbers. It inevitably sees commit subjects, so it is classed as instrumentation, not as cold analysis.

### 3.2 One snapshot
Everything is pinned to the three repos' `origin/main` SHAs recorded at kickoff.

### 3.3 Hypotheses with pre-registered tests
Metrics and decision thresholds are written into `spec-eval/preregistration.md` **before D0 runs** and are not changed afterward. Any later change is logged with its reason.

- **H1: coordination cost dominates.** Cost is measured in **tokens/$, PM-minutes and wall-clock time per merged product change** (merged product change = a non-merge commit touching services/web/templates/alembic, or an issue closed with a code diff), not in commit counts. *Supported if* that ratio has risen materially since April 2026. The threshold is set in the pre-registration.
  - **H1b: redundancy** (added at PM's request, 10-03). Several agents read the same documents, several jobs produce overlapping updates for PM, and several mechanisms watch the same thing. Measured by:
    - overlap in what each role loads at session start (documents loaded by N roles × their token size)
    - duplicate or overlapping recurring outputs addressed to PM (rollups, digests, current-state refreshes, the Weekly Ship, plus any Cowork scheduled jobs)
    - more than one watcher on the same signal (freeze watchdog, heartbeats, merge-keeper, CI liveness)
    - how often a PM-facing item is read or acted on, where that can be observed

    Cowork scheduled jobs stored on PM's machine **can't be seen from the repo**. They go on the unobservables list, and Exec or PM supplies an inventory.

- **H2: the ruleset is costly and poorly suited to current models.** Measured by tokens loaded at start, per role; contradiction count; count of rules with no mechanism behind them; narrative-to-instruction ratio; and fit with current Anthropic prompting guidance.
- **H3: docs have drifted from reality.** Tested with the claims-vs-reality ledger (L), reported as the share of sampled claims that hold, with the denominator stated.
- **H4: the process buys quality** (the counter-hypothesis, given equal weight). Tested with an **interrupted time series**: revert rate, fix-of-fix chains, reopened issues and production/alpha incidents, before and after the dates major mechanisms were introduced (mailboxes, duty cycle, hooks, CLAUDE.md growth spurts). *Supported if* defect signals fell after a mechanism arrived and the fall isn't explained by lower throughput.

### 3.4 Shared findings schema
Every workstream writes findings in one schema so the synthesis can merge them mechanically:
`id · claim · layer (static / ran-tests / ran-server / CI-history / live-probe / record) · denominator · evidence path (file:line, command, script) · confidence · implication for the guiding question`.

### 3.5 Unobservables
A running list, `spec-eval/unobservables.md`, of what we couldn't observe and how it could be observed instead (human test vs agent harness). It is delivered as a test plan.

## 4. Phases

Each phase lists its subagents with the model tier I'll assign. Tiers get logged at dispatch, per CLAUDE.md. Every subagent prompt includes a token cap and the findings schema.

### Phase 0: setup and feasibility gate (Spec, ≤30 min)
1. Record snapshot SHAs. Build the code-only export.
2. **Feasibility gate, capped at 20 minutes:** start dockerd or a local Postgres; create a venv; `pip install -r requirements.txt`; run one unit test; try booting `main.py`.
   - **If it passes,** B runs the suite and C attempts a live run.
   - **If it fails,** B falls back to static review plus **CI run history** (GitHub Actions pass rates, which measure what CI actually gates), and C becomes a static inventory on Sonnet.
   - Either way, the outcome is logged.
3. Write `preregistration.md` (§3.3).
4. Confirm `/checkup prompt-audit` runs in this container.
5. **Calibration:** PM checks the usage page after Phase 0 so I have a dollars-per-token estimate.

### Phase 1a: D0 history instrumentation (runs first; on the critical path for E, F and H4)
| ID | Tier | Scope |
|---|---|---|
| **D0** | Sonnet + scripts | Pre-registered metrics only: activity composition by **files and lines**, not just subjects; per-role activity from subject prefixes and log filenames (no "per agent-hour" unless a duration source is verified); the H4 interrupted time series (reverts, fix-chains, reopened issues, incidents) against mechanism-introduction dates; ruleset growth curve versus product-code growth; issue-closure velocity; PM-authored decisions and memos addressed to PM per week. Outputs go to `metrics/`: scripts plus CSV. |

Spec reviews D0's metric validity before anything builds on it.

### Phase 1b: code-first workstreams (parallel with each other; may overlap D0)
| ID | Tier | Scope |
|---|---|---|
| **A** | Opus | **Architecture as found:** module boundaries, dependency graph, dead or duplicate code, how complex intent routing is, error-handling consistency. **Plus security and privacy:** a secret scan of the working tree and history (bearer-credential history is known: #1845, #1885), the auth/OAuth surface, how user data is handled. |
| **B** | Sonnet | **Tests, CI, build and deploy health** (live run or CI-history fallback per the gate): pass/skip/xfail counts with denominators; whether tests check real behavior or just go through the motions (mock-heavy, tautological); dead or duplicate workflows; deploy reproducibility; **dependency health, CVEs, licensing**. |
| **C** | Opus if running live, Sonnet if static | **Product as built:** the capability inventory from routes, templates, handlers and the intent catalog. Each capability is classed works / partial / stub / fails / unobservable, with its layer. This feeds the unobservables list. |

Each of A, B and C ends by committing its **pre-registered top 5**.
**Checkpoint: about $35 estimated spend at the end of Phase 1.** I'll report to PM and continue unless told otherwise.

### Phase 2: context-aware workstreams (parallel; may read everything)
| ID | Tier | Scope |
|---|---|---|
| **D-measure** | Sonnet | Scripted: tokens loaded at session start per role (CLAUDE.md, briefing, skills, hooks output), a contradiction and staleness grep, an inventory of rules with no mechanism, and the narrative-to-instruction ratio. |
| **D-propose** | Opus | Builds on D-measure and today's Anthropic guidance. Rates every section keep / compress / move-to-reference / delete / mechanize. Produces a **sample rewritten CLAUDE.md as a proposed diff, not applied**, plus a careful staged refactor sequence. |
| **E** | Sonnet | **Flywheel forensics:** where it came from, the original 4 pillars quoted from history, every redefinition (date and commit), past re-evaluations and what came of them. Then compares the stated flywheel with D0's behavioral data. |
| **F** | Opus | **Operating model:** what each role produces and who consumes it; outputs nobody uses; what the machinery costs (tokens, commits, incidents caused by it versus caught by it); **PM attention load and bus factor**; **running cost** (cohort LLM spend, Fly, Amber, using whatever data sources exist, and naming the ones that don't); whether constraints from the Desktop/Amber era still apply; leaner alternatives, each with its migration risk. |
| **G** | Opus | **Strategy against reality, with the user question first:** do real users exist, what do they do, and what feedback have they given? This is answered first because most recommendations depend on it. Then vision, roadmap v18 and PDRs (including BYOC) compared with C's inventory; backlog health (age, priority inflation, closed-but-not-done); and whether the product thesis survives the current market (Claude Cowork, plugins, MCP), with web research. Website and skunkworks are folded in briefly: BYOC continue/merge/stop, and whether site claims match product reality. |
| **L** | Sonnet (separate from Spec) | **Claims-vs-reality ledger:** a stated sample of doc claims (briefings, README, current-state, roadmap) checked against A/B/C/D0 evidence. Each row gets both citations, and the ledger reports what share holds. |

Repo weight (21k mailbox files in a public repo: clone size and agent context cost) is assigned to F.

### Phase 3: synthesis (Spec, Opus)
- Merges the schema'd findings.
- Gives H1–H4 verdicts against their pre-registered thresholds.
- Reports drift between the pre-registered top-5 lists and the final conclusions.
- Lists at most 7 recommendations, each set against the do-nothing baseline.
- Hands over the unobservables test plan.
- **One batched round of questions** goes out (via Exec, see §6) only for gaps the records can't settle.

### Phase 4: verification (two independent agents, given the raw repo, not just my bundle)
- **V1 (Opus):** independently re-derives at least 3 headline numbers with its **own** scripts, reruns every table from `metrics/`, then tries to refute each top recommendation. Verdict per item: CONFIRMED / WEAKENED / REFUTED.
- **V2 (Sonnet, a different tier on purpose):** builds the strongest case for H4, "the process is what's working," and checks whether the report survives it.
- Disputed items stay marked as disputed.

### Phase 5: delivery
- **Report:** `docs/internal/audits/2026-10-spec-project-evaluation.md` (path to be confirmed). Supporting files go in `dev/2026/10/03/spec-eval/`.
- **A private artifact page** for PM to share with Exec and CIO.
- **A memo to Exec and CIO, cc PM.**
- The session log is updated at each commit.

## 5. Budget
- **Ceiling: $100 without asking.** Estimate: **$45–75** for 11 subagents (5 Opus, 6 Sonnet) plus synthesis.
- **Controls:**
  - token caps written into each subagent prompt
  - scripts do the counting, so agents don't have to read everything
  - warm agents receive D0 and D-measure outputs rather than re-deriving them
  - the feasibility gate stops B and C from burning budget on setup
- **Checkpoints:**
  - PM calibration after Phase 0
  - **about $35 at the end of Phase 1**
  - **about $60 before Phase 4**

  At each one I report spend; I stop if the estimate is above plan.
- **Accounting:** token usage per subagent is reported in each result (confirmed: the audit agent's result showed `subagent_tokens: 93,633`). It is logged per dispatch.

## 6. Cohort disturbance
- **No all-roles kickoff memo.** Notifying about 10 duty-cycling roles is itself a disturbance, and it creates observer bias. Exec already has today's notice. **Exec decides** whether and how the wider cohort hears about this.
- **Questions:** one batched memo in Phase 3, **routed through Exec**, only for real gaps. Each question is answerable in under 10 minutes and "don't know" is an acceptable answer.
- **No previews:** no role sees findings about its own area before PM does. Any resulting directives come only through PM.
- **Read-only on shared state.** Spec pushes to `origin/main` **only** in these cases:
  - mail
  - this plan and the session log, at a few checkpoints, with explicit paths
  - Phase 5 delivery

  Working files stay on the branch, `claude/laughing-hopper-3l64s3`, until Phase 5. This keeps the merge churn I add to everyone's Model-A worktrees close to zero.

## 7a. Oct 2026 Claude Code update: how it changes the plan (PM forwarded mid-review)
- **`/checkup prompt-audit`** (v2.1.283+) flags instructions written for older models, stale paths and contradictions, and writes a report and a patch without applying either. D-measure runs it as a baseline over CLAUDE.md, the skills and the agents. D-propose must account for every item it flags. Phase 0 checks that it runs headless here (container CLI is 2.1.288).
- **Opus 5.5 / Sonnet 5.5** give shorter replies and follow the literal request. D-propose tests whether the ruleset's defensive, repetitive, incident-narrative style still pays its context cost. It also checks the dispatch-tier guidance against Sonnet 5.5.
- **Mods** can hold or rewrite a tool call. This adds an "enforce with a mod" option to D's grading and a lever for F. Today several rules are prose only because the current hooks are advisory: mailbox-on-main, broad staging, bearer creds, auto-close keywords, log discipline. Mods require v2.1.287+ on each seat. Amber is **unverified**; a CIO memo from 10-03 says the fleet is on 2.1.280.
- **Wrap-up allowance:** D checks which context-pressure and sign-off rules it makes redundant.
- **AGENTS.md support and claude.ai skills/plugins sync:** restructuring options for D-propose. Options only.
- **`build-eval` / `hillclimb`:** C and G note whether a measured eval of Piper's intent-routing accuracy exists or should exist. Building one is out of scope.
- **"You should know" side-agent:** a candidate for F's leaner-alternatives list. Noted only.

## 7. Cloud-versus-local comparison (PM request; kept separate from the evidence)
The auditor recommended dropping this, since one data point taken by the evaluator about itself is anecdote. **I'm keeping it, as PM asked for it, but outside the findings:** a short observational note on friction, cost visibility, what was missing (Keychain, daemon, cohort hooks), and what was better (credits, isolation, fan-out). It is clearly labeled as n=1, not evidence.

## 8. Risks
- **Instruction injection:** the harness passes CLAUDE.md into subagents. Handled by code-first ordering, pre-registration and drift measurement (§3.1).
- **Metric naivety:** handled by pre-registration, several cost units rather than one, and V1 re-deriving the numbers.
- **One synthesizer:** L is separated out, there are two verifiers, and the scripts can be rerun.
- **A Phase 0 gate failure narrows the product evidence to static and CI-history layers.** That gets stated, and the unobservables list grows to cover it.
- **No data source for cost or users:** reported as an unobservable, not estimated.

## 9. Changes from v0.1 (independent audit)
| # | Audit finding | Resolution |
|---|---|---|
| 1 | The "cold firewall" is already breached (CLAUDE.md injected); `git archive` carries no history; D0 is inherently warm | Reframed as code-first ordering with no `.git`; D0 reclassed as instrumentation; pre-registered top-5 lists added to measure drift (§3.1) |
| 2 | Container can't run the app as assumed | Phase 0 feasibility gate with CI-history and static fallbacks (§4) |
| 3 | H1 measured with an instrument that would confirm it; H4 untestable; merge count understated (~2.86k, not ~1.5k) | Pre-registered metrics and thresholds; cost in tokens/$/PM-minutes; interrupted time series for H4; merge count corrected (§2, §3.3) |
| 4 | Git authorship can't attribute agents | Attribution from prefixes and log filenames only; "per agent-hour" dropped unless a duration source is found |
| 5 | Missing coverage: security, running cost, PM load, bus factor, deps/licensing, repo weight, users | All added: security to A; deps/licensing to B; cost, PM load, bus factor and repo weight to F; users as G's first question |
| 6 | Decision-readiness stated but not enforced | Cap of 7, success metric plus review date, do-nothing baseline, a this-week first step (§1) |
| 7 | D0 on the critical path; D too large; L done by the synthesizer; no shared schema | D0 first; D split into measure and propose; L given to a separate agent; schema in §3.4 |
| 8 | Budget checkpoints come too late | PM calibration after Phase 0; about $35 checkpoint at end of Phase 1; token caps |
| 9 | The kickoff memo perturbs the cohort; pushes cause merges | Exec-only notice; questions routed through Exec; pushes kept to a minimum |
| 10 | Verification not independent | Two verifiers on different tiers, given the raw repo, re-deriving numbers with their own scripts |
| (declined) | Drop the cloud-vs-local note | Kept because PM asked for it, but quarantined as n=1 (§7) |

## 10. PM decisions (2026-10-03)
- Report location `docs/internal/audits/`: **approved**.
- Notice goes to Exec only, and Exec decides how the cohort hears about this: **approved**.
- Pause after Phase 0 for the usage check: **approved**. Calibration point: **$4 spent** at plan v0.3 (main context plus one ~94k-token Opus audit subagent).
- Phase 0 authorized.
