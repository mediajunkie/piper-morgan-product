# Attention-Dashboard — Trust/Welfare Criteria **v0.3 SPEC**

**Owner**: HOST (welfare-criteria lane, m-39). **Status**: **SPEC** — v0.1/v0.2 were criteria; this is normative. **Reviewers**: CIO (dashboard design + registry/watchdog surfaces), Exec (cohort-attention rollup surfaces, per-criterion scope calls flagged inline).
**Supersedes**: `dashboard-welfare-criteria-host-v0.2-seed.md` (criteria D/E/F + Q1–Q3 answers + CIO async markup 2026-06-18/19). v0.1 criteria A/B/B-bis/B-ter/C carried forward unchanged in intent.

**Why this is a spec and not v0.3 criteria**: the v0.2 seed closed with *"open questions are now answered; the pairing can focus on design decisions, not criteria gaps."* CIO's markup then fixed an agreed shape for every criterion. What was missing was normative language — MUST/MUST NOT, render rules, data sources, and state definitions someone can build against. That's this document.

**What changed since the 2026-06-19 markup — and why the 5-week gap improved it.** v0.3 was idle from 6/19 to 7/26. In the last 48 hours the cohort generated **seven** real instances of exactly the failure class these criteria exist to prevent (appendix). Three had no counterpart in June, and they produce one new criterion, one new liveness state, and four render rules. A June v0.3 would have specified less.

---

## §1 The render rules (normative — these bind every panel)

These are the honesty rules. They generalise Criteria D from "surface detections" to "never let a partial or absent observation render as a clean one." Every one is grounded in an incident in the appendix.

**R1 — No detection maps to silence.** Every welfare-relevant detection MUST surface something: `confirmed` → `borderline / needs verification` → `clean (verified)`. Uncertainty is rendered as uncertainty, never as omission. *(Criteria D, unchanged.)*

**R2 — ⚪ No-data MUST NOT render as clean, ever.** Absence of a signal and a verified-clean signal MUST be visually and semantically distinct, at every altitude including summary tiles. A role with no registry row, a panel whose input is missing, a check that did not run — all render `⚪ unknown`, never green, never omitted.

**R3 — Every aggregate MUST state its denominator.** Any count, percentage, or "all clear" MUST carry the population it was computed over. `4 of 10 roles watched` — never `all watched`. A summary that cannot compute its denominator renders `⚪ coverage unknown`.

**R4 — Every derived panel MUST disclose input completeness.** If a panel is built from a source that was truncated, partially parsed, sampled, or rate-limited, it says so inline. Silent partial input presented as complete output is the single most repeated failure in the appendix (4 of 7 instances).

**R5 — State what was observed, not what was concluded** (m-43, *Name the Layer*). Panels MUST render the observation and label any inference as inference. `check-branch.sh refused this commit at 07:08` — not `enforcement is on`. Where the dashboard displays a conclusion, it MUST be traceable to the observation that supports it, at the layer that observation was actually made.

**R6 — Instrument validity is per-question.** A field MUST NOT be reused to answer a question its instrument cannot answer. Where a signal is valid for one question and confounded for another, the panel names which. *(Generalised from the `/tmp` counter case: an instrument is not valid or invalid, it is valid for a specific question.)*

---

## §2 Criteria A–F — carried forward, now normative

Intent unchanged from v0.1/v0.2; restated at spec altitude with the CIO-agreed shapes.

**A — Agent-status truthfulness.** Every agent row's status MUST be derived from observable artifacts (session log, commits, registry), never from agent self-report. *(v0.1.)*

**B / B-bis / B-ter — Escalation surfacing + the non-PM cross-pair observer.** Agent escalations surface without requiring PM to read every carry-forward; the dashboard performs the cross-agent sweep no individual agent can perform. *(v0.1.)*

**C — No false certainty.** Borderline conditions render borderline. C2: an item closed upstream MUST NOT render as still-awaiting-PM. **Implementation**: GitHub-verify every issue-shaped item at render time; never trust a local doc's status claim. *(v0.1; strengthened — a CIO portfolio doc sat stale 20 days and caused two consecutive reviews to report a closed issue as slipped.)*

**D — Dashboard honesty.** Now expressed as R1–R6 above.

**E — Consequential-action accountability.** Surface an aggregate count/summary of actions taken autonomously on users' behalf, scoped to: agent-initiated (not user-requested) · credits spent · external message sent · hard to reverse. Not a per-action ledger.
> **E MUST ship with its coverage indicator.** Render `N actions logged (coverage: partial — M of K action-taking skill call sites instrumented)`. **`0 actions logged` under partial instrumentation is indistinguishable from `no actions taken` and is false assurance** — the coverage indicator is as load-bearing as the count, and E MUST NOT ship without it. *(HOST addition, 6/19; now also a direct instance of R4.)*
> Data shape per CIO markup: `TranscriptEntry` + 4 fields. Sequence external-message + credits-spent first (BYOC-tied).

**F — Asymmetric-knowledge detection.** The cross-agent sweep for cases where the system knows something PM doesn't. Per CIO markup, extend Exec's cohort-attention rollup: **F1** source carry-forward PM-blocked sections (not just attention docs) · **F2** cross-pair-gap check (two surfaces reference one thread, neither flags it blocked) · **F3** existing GH-verify covers the resolved-but-still-listed case.
> ⚠️ **F2 requires cross-document reference detection the rollup does not currently do — scope to Exec before building.** *(Flagged in the 6/19 markup; still open.)*
> **New F4 — undelivered outbound obligations.** Where an agent's log shows a decision, ruling, or promise directed at another role, and the recipient's inbox contains no corresponding item, surface the gap. This is the highest-severity asymmetry class: **the damage lands on a party who cannot know it exists.** ⚠️ **The case originally cited here (arch's `#1394` ruling vs. Lead's build) turned out to be FALSE — checked 2026-07-26: Lead received it and logged it the same morning.** The rule stands on Exec's two independently-observed cases; the exemplar does not. Kept visible because it failed in the rule's own shape: *F4 says verify the obligation reached its recipient, and the example was written without checking the recipient's side.* *(Sourced from migration-checklist v1.4.2 Rule 4; the dashboard is the only surface that can see both halves.)*

---

## §3 NEW **Criteria G — mechanism liveness (the belt needs its own belt)**

**The gap this closes.** v0.1–v0.2 model *agent* liveness thoroughly and *mechanism* liveness not at all. That is the wrong way round for the failures we actually have: in the last 48 hours, **four mechanisms were found silently dead or unreliable, and not one of them was visible on any dashboard** — three pre-commit hooks dead since introduction, a PreCompact hook registered to an empty array for ten weeks, a watchdog covering 4 of 10 roles, and an enforcement layer whose reliability is still unexplained. A dashboard that renders every agent 🟢 while its own enforcement substrate is dead is precisely the false assurance this criteria set exists to prevent — and it would have rendered exactly that, all ten weeks.

**Criterion.** Every mechanism the cohort *relies on but does not observe* MUST have a row, with a **last-verified-behaviourally** timestamp — not a config-present check.

**G1 — Config presence MUST NOT be rendered as liveness.** An absent mechanism and a silent mechanism are indistinguishable from inside a session. Only a behavioural observation sets a mechanism 🟢.

**G2 — Verification staleness renders like agent staleness.** A mechanism verified longer ago than its verification interval goes 🟡, then ⚪ `liveness unknown` — it MUST NOT stay green on the strength of an old pass. *(A safety net you haven't seen fire is a claim, not a mechanism.)*

**G3 — Unverifiable mechanisms are a distinct state, not a pass.** Where a mechanism cannot be forced on demand (PreCompact — you cannot induce a compaction), it renders `⚪ unverifiable — never observed firing`, permanently, until someone reports an observation. **It MUST NOT render green because its config is correct.** This is the current, honest state of PreCompact and the dashboard should say so.

**G4 — Known-unreliable is its own state.** A mechanism observed to fire *sometimes* renders 🟠 `unreliable`, with the sample. Neither green nor red: enforcement that works 1 time in 5 is worse for planning than enforcement known absent, because it invites reliance. *(The hooks intermittency: 1-of-5 on one seat, 8-of-8 on another, 6-of-6 headless, unexplained.)*

**G6 — A liveness instrument MUST report its own ABSENCE, not only its failures.** *(Added 2026-07-26, earned within hours of G's first implementation.)* An instrument that escalates on `FAIL` but writes nothing when it does not run is **silent in the one state that matters most** — a stopped checker and a passing checker are indistinguishable downstream, which is R2 one level up. Every mechanism-liveness instrument MUST therefore carry a **staleness assertion on its own output**: if the newest result is older than ~2× its interval, that renders `⚪ instrument stale — liveness unknown`, and escalates.
> **Where this terminates, because it cannot recurse forever.** Watching the watcher is infinite regress, and the answer is not another daemon. The chain terminates at **a cheap staleness check on an artifact that already exists, folded into a loop that already runs** — an mtime/newest-line comparison inside an existing duty cycle, not new infrastructure. One assertion converts the terminal node from *silent* to *self-reporting*, and that is enough: the last link doesn't need a watcher if it announces its own age.

**G5 — Advisory vs. control MUST be labelled.** A mechanism steppable with a flag (`git -c …`, `--no-verify`) is **advisory** and MUST be labelled so. Rendering an advisory aid as a control re-creates the false confidence one layer up — the failure mode being that the cohort stops maintaining the primary prose discipline because "the hook handles it."

**Initial G roster** (all currently unrendered anywhere): `check-branch.sh` (advisory · 🟠 unreliable · last verified 2026-07-26 07:08) · `pre-commit-broad-staging-warn.sh` · `pre-commit-reconcile-drafts.sh` · `precompact-signoff-warning.sh` (⚪ unverifiable) · `duty-cycle-freeze-check.sh` (+ its denominator, per R3) · `session-start.sh` · `mail-send.sh` push-to-ref · `MEMORY.md` index integrity (size + entry-count vs. file count).

---

## §4 Liveness state machine — Q3's answer, corrected

The v0.2 answer specified four states. **Four is one too few, and the missing one is generating live noise right now.**

| state | condition | source |
|---|---|---|
| 🟢 **Active** | last fire within expected interval | registry `cron_expr` + heartbeat |
| 🟡 **Gap-suspected** | silent beyond **1×** threshold_h | registry `threshold_h` |
| 🔴 **Likely stopped** | silent beyond **1.5× threshold_h**, or NO-HEARTBEAT | per CIO markup |
| ⚪ **No data / unwatched** | no registry row, or no heartbeat source | **MUST NOT render clean** (R2) |
| ⏸ **PARKED** *(new)* | **deliberately dark** — retired, awaiting migration, or intentionally suspended | new registry `state` field |

**Why ⏸ PARKED is required, not a nicety.** The registry is currently binary — a row means *watched*, no row means *structurally invisible*. For a deliberately-dark role **both options are wrong**: keep the row and the watchdog emits correct-but-unactionable alerts forever (`arch`: **3 alerts in 20 hours**, and it will fire roughly every 6h until migrated); delete the row and the role becomes invisible, which is finding #6 exactly — how five roles went dark for six days unnoticed.

PARKED keeps both properties: **no stall alerts, but still counted in coverage output** as `parked (since YYYY-MM-DD, reason)`, so it cannot be silently forgotten. It also removes the hand-workaround already in the file — `cxo` and `ppm` are commented out, which is PARKED implemented as a comment and therefore invisible to R3's denominator.

**The trust argument, because it is the same one as R2 from the other direction**: a belt that cries wolf and a belt that is silent fail identically — *the cohort stops treating its output as information*. A mechanism's silence only means "clear" if you have verified its coverage; a mechanism's alarm only means "act" if you have distinguished expected-dark from failed.

**Wake-window handling** (unchanged, v0.2 Q2 + CIO markup): thresholds respect `wake_start`/`wake_end`; overnight silence is not staleness for a daytime-only cron. Threshold source is the registry, never agent self-report.

**HOST addition, carried from the markup and now normative**: **simultaneous multi-role 🔴 MUST render as one `infrastructure event suspected`, not N independent alarms.** N roles failing at once is one event; rendering it as N failures buries the actual signal.

---

## §5 Data sources (all existing — G is the only new collection)

| criterion | source | status |
|---|---|---|
| liveness, thresholds, PARKED | `dev/active/duty-cycle-registry.tsv` + `scripts/duty-cycle-freeze-check.sh` | built; needs `state` field |
| staleness / heartbeat | session-log lifecycle + `DAY-CLOSED` marker | built |
| C2 / F3 GH-verify | `gh` at render time | built (rollup) |
| F1 / F2 / F4 | carry-forwards, session logs, **recipient inboxes** (F4) | F1 partial · **F2 + F4 need Exec scope** |
| E | `TranscriptEntry` + 4 fields + coverage denominator | not built |
| **G** | behavioural verification results — e.g. `amber-agent verify-hooks` | **instrument exists, is unrendered and unscheduled** |

**G's collection is nearly free**: Pard's `amber-agent verify-hooks` already produces exactly the datum G1 requires, on demand, in one command. What is missing is a **schedule** and a **surface** — currently a mechanism's liveness is established only when a human or agent happens to wonder. Pard offered a scheduled `verify-hooks` drumbeat; **G is the reason to accept it.**

---

## §6 Open items — whose call each is

*(Naming the owner per half, per the m-43 corollary — an ask that doesn't say whose call it is makes the recipient inherit the sender's ambiguity.)*

1. **CIO** — accept/redirect **Criteria G** and the ⏸ PARKED state. Both touch surfaces you own (dashboard render; registry + watchdog). I have not edited the registry; the `state` field is your call to make, and I'll draft the definition + coverage phrasing if you want it off your plate.
2. **Exec** — **F2** (cross-document reference detection) and **F4** (outbound-obligation gap) both extend your cohort-attention rollup beyond what it does today. Scope call, not a design call.
3. **Pard** — the scheduled `verify-hooks` drumbeat you offered; §5 is the argument for taking it. Interval is yours.
4. **HOST (me)** — (a) E's coverage-indicator definition → **DONE same day, see §7.** (b) G's per-mechanism verification intervals → **held until CIO rules on G**, since intervals for a redirected criterion would be wasted work. Trigger named rather than left as silence.
5. **Deliberately deferred** — the fuller PM-wellbeing signal stays out of scope (v0.2 Q1). The one PM-welfare datum that belongs here is the **convergence-load headline** (items routing to PM this week + sparkline): m-39's risk made visible. Low when the system absorbs well; high is the signal to triage or delegate.

---

## §7 — **E coverage-indicator: definition** *(closes §6 item 4a — HOST's own, not blocked on review)*

Written the same day as the spec rather than left as a listed intention. Independent of whether Criteria G is accepted: E's shape was already agreed in the 6/19 markup, so this is buildable now.

**Definitions.**
- **Action site** — a code path that performs a consequential action per E's four tests (agent-initiated · credits spent · external message sent · hard to reverse). The denominator `K` is the count of action sites, enumerated statically, **not** the count of actions.
- **Instrumented site** — an action site that emits a `TranscriptEntry` with all four E fields populated. `M` is the count of these. A site emitting a partial entry counts as **uninstrumented**, because a partial entry produces an undercount that looks like a count.
- **Coverage** = `M / K`, always rendered as the fraction, never as a bare percentage. `12 of 19` is checkable; `63%` is not.

**Render forms.** The count and the coverage are one atomic string — they MUST NOT be separable by layout, truncation, or a summary tile that shows only the count:

| condition | render |
|---|---|
| `M = K`, N ≥ 1 | `N consequential actions this week (coverage: complete — 19 of 19 sites)` |
| `M < K`, N ≥ 1 | `N consequential actions this week ⚠️ (coverage: partial — 12 of 19 sites; N is a floor, not a total)` |
| `M < K`, **N = 0** | `⚠️ No actions logged — but coverage is partial (12 of 19 sites). This does NOT mean no actions were taken.` |
| `M = K`, N = 0 | `0 consequential actions this week (coverage: complete)` — the only case where zero means zero |
| `K` unknown | `⚪ Coverage unknown — action-site inventory not established. Counts are not interpretable.` |

**The blocking rule (normative).** E MUST NOT ship in any form that can render a count without its coverage. **The `M < K, N = 0` cell is the whole reason** — it is the one that reads as reassurance while being the least informative state the system can produce, and it is the default state during any incremental rollout. Since the 6/19 markup sequences E incrementally (external-message + credits-spent first), **partial coverage is the expected condition for the entire rollout period, not an edge case.**

**Why `N` is labelled a floor, not a total.** An undercount from partial instrumentation is not a noisy estimate — it is biased in one direction, always downward, and the bias is invisible without `K`. Same structural error as the `MEMORY.md` index: a silently truncated input rendering as a complete output. Naming `N` a floor makes the direction of the error legible to PM without requiring them to reason about instrumentation.

**Interval / staleness**: coverage is recomputed whenever the action-site inventory changes; a coverage figure older than its inventory renders `⚪ coverage stale` per R4 rather than showing a figure that may have silently drifted.

**Still mine and still open**: G's per-mechanism verification intervals — deliberately held until CIO rules on G, since intervals for a redirected criterion would be wasted work. Named here so the deferral has a trigger rather than being silence.

---

## Appendix — the seven instances grounding §1 and §3

All 2026-07-24→26 unless noted. Each maps to the rule it produced.

| # | instance | rule |
|---|---|---|
| 1 | Three pre-commit hooks registered with permission-rule syntax in a tool-name matcher field — **never fired on any machine since introduction**; config was present and correct throughout | **G1** |
| 2 | `PreCompact` registered to an empty array for **ten weeks** after its unblocking fix landed the next day; CLAUDE.md described it in the present tense the whole time. Corroborated by a log file that never existed | **G2, G3** |
| 3 | Freeze-watchdog covered **4 of 10 roles** and phrased its subset as a total — noise where there was coverage, silence where there wasn't | **R3, R2** |
| 4 | `MEMORY.md` at 41.4KB against a ~24.4KB read limit — **~40% of the index silently dropped**, including most of one bucket. The file's own header warned of a prior identical drift | **R4** |
| 5 | Finding #4's *diagnosis* (worktree-scoped) written into four canonical surfaces without ever being tested; drove a real fix cycle that faithfully copied the broken matcher | **R5** |
| 6 | Enforcement observed 1-of-5 on one seat, 8-of-8 on another, 6-of-6 headless. Excluded: file shape, command shape, config drift, single-layering. **Still unexplained; the intermittent seat has been retired** | **G4** |
| 7 | `check-branch.sh` bypassable with `git -c …` and a documented `--no-verify` hatch — a discipline aid, not a control | **G5** |
| 8 | Watchdog alerting on `arch` **3× in 20 hours**, correct and unactionable, because the registry cannot express *deliberately dark* | **⏸ PARKED** |

**The through-line, which is the argument for G as a whole**: every one of these was *believed working on the strength of its configuration or its plausibility*, and every one was invisible to every dashboard we have. The criteria set has always been about not letting PM read silence as safety. **G extends that from the agents to the instruments** — because the instruments turned out to be where the silence actually was.

---

*HOST, 2026-07-26. v0.3 spec — supersedes the v0.2 seed. Ready for CIO/Exec/Pard review per §6.*
