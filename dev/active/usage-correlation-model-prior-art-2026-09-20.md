# Usage-correlation model — prior art pass

**Author**: PA. **Filed**: 2026-09-20 (16:01 fire). **Status**: RESEARCH PASS ONE — prior art only,
per Exec's explicit ask to do this before modelling. The model itself is not designed yet; see
"What's not done" at the bottom.

## The task, as given

PM (via Exec, 2026-09-20): build a real model of what correlates with usage, instead of hand-waving
about it — the immediate trigger was Exec's own commit-count-based throttle analysis swinging
between two unmeasured conclusions in one day. PM: *"research what's out there, because this is
possibly prior art, much of it."* No deadline — a well-grounded answer in a week beats a rushed one
tonight, and "the proxies can't support this without PM's numbers" is itself an acceptable finding.

**The hard constraint, stated by Exec and confirmed true by this pass**: no agent can see PM's usage
dashboard. Every internally-measurable dimension — commits, session-log growth, mail volume, fire
counts, dispatch tier — is a proxy for something none of us can observe directly. A model built by
correlating proxies against each other proves nothing about the thing they're all proxying for.

## Prior art found — four fields, same underlying problem

### 1. Software-engineering productivity metrics (closest surface analogy)

Commit counts, PR counts, and lines-of-code have a well-documented, recent (2024–2026) critique
trail as productivity proxies — and AI-assisted development makes it *worse*, not better: a
developer using an AI assistant can produce 3-5x more raw volume with no relationship to whether
that output survives or matters (GitClear's churn-rate data: 3.3% baseline in 2021 rising to
5.7–7.1% in 2024–2025). This is close kin to Exec's own experience this week — the 12%-of-commits
figure was directionally real but uncalibrated, then read as meaningless when a counter-example
(Web's "a conversation produces no commits") surfaced, when the right read was "the proxy needs
calibration, not abandonment."

**The structural answer this field converged on**: the SPACE framework (Microsoft Research/GitHub/
UVic, 2021) — productivity is multi-dimensional by construction, and any single metric (objective or
subjective) will distort. Its five axes: Satisfaction & wellbeing, Performance, Activity,
Communication & collaboration, Efficiency & flow. The load-bearing move isn't the five axes
specifically — it's that **no single proxy is trusted alone, and at least one axis is necessarily
non-derivable from system telemetry** (satisfaction/perceived performance requires asking someone).

**Transfers**: the "don't trust one axis" structure, directly. **Doesn't transfer cleanly**: SPACE's
axes assume a human team where self-report is cheap to collect continuously; here the "self-report"
equivalent (PM's actual usage reading) is exactly the scarce, expensive signal the whole exercise is
built around, not a free fifth input.

### 2. Statistics — measurement-error models, calibration, surrogate endpoints

This is the field that has formally solved Exec's exact design problem: **errors-in-variables
regression / regression calibration**, where an unobservable true variable is replaced by cheap
proxies, and the model is corrected using a **validation subsample** where the true variable actually
was measured. The clinical-trials variant (surrogate endpoint validation) is the most mature version:
a cheap-to-observe surrogate (e.g., a lab value) stands in for an expensive/slow true endpoint (e.g.,
survival), validated via periodic studies where both were measured together, using meta-regression
across the paired readings.

Recent work (2026: "Proxy-Guided Measurement Calibration," "proxymate: Diagnosis and Adjustment of
Proxy Estimates for Reliable Inference") formalizes the general case: a proxy correlated with the
true outcome can still be **systematically biased**, and calibration requires either (a) a proxy that
depends on the true outcome but not on the bias mechanism, or (b) a validation subsample pairing
proxy and ground truth.

**This is the single most directly transferable piece of prior art for this task.** The design
Exec sketched — "the model needs periodic real usage readings from PM to anchor against" — **is**
regression calibration with a validation subsample, described independently and arrived at the
same place. The field gives us: don't build the proxy model and separately "sanity check" it against
occasional PM readings; build the calibration into the model's estimation from the start, and know
that correlation-among-proxies alone (with zero ground-truth readings) cannot detect or correct bias,
only internal consistency.

**Doesn't transfer directly**: the field assumes a validation subsample already exists in usable,
paired form. Ours currently does not — see the Piper-internal finding below, which is arguably more
load-bearing than any external source.

### 3. LLM/agent-fleet cost observability (practitioner tooling layer)

A live, fast-growing 2025–2026 tooling space (Langfuse, Braintrust, Datadog LLM Observability,
Vantage, NeuralTrust) exists specifically for per-agent, per-session cost/token attribution in
multi-agent systems — the same shape as "48 dispatches silently inherited the dispatcher's tier and
exhausted a shared ceiling" (this cohort's own 09-14 incident). The core primitive these tools use —
a **trace**: multiple LLM calls linked into one attributable unit, with per-step cost — maps almost
exactly onto this cohort's own "fire" and "dispatch" concepts.

**Transfers**: the trace-as-unit-of-attribution idea, and the general finding that **cost/token
volume and "usage" are not the same axis** — a fleet can spend heavily on a small number of complex
fires or lightly across many trivial ones, and neither is a stand-in for the other without knowing
which. **Doesn't transfer**: this tooling measures $ and token cost, which is adjacent to but not
identical to what PM's usage dashboard likely reflects (conversational engagement, not spend) —
useful for calibrating the dispatch-tier dimension specifically, not the model as a whole.

### 4. Product analytics — North Star Metric / leading-indicator frameworks

The product-management version of the identical problem: pick a North Star (the true outcome,
often lagging and expensive to move/observe) and a small set of leading indicators, **validated**
by regression against historical experiments to confirm they actually predict the North Star rather
than being assumed to. Explicit warning in this literature against picking a leading indicator
because it's *available* rather than because it's been shown predictive — the same failure Exec
named in their own memo (picking commit counts because they're measurable, not because they were
shown to track load).

**Transfers**: the discipline of validating a leading indicator against the true metric before
trusting it, and treating "no history to validate against yet" as a real blocker, not a formality.
**Doesn't transfer**: North Star frameworks assume a product with users generating the North Star
metric at volume, with enough history to regress against. Our situation is closer to "we don't yet
have any paired (proxy, ground truth) observations at all" than "we have data but haven't validated
against it."

## The most important finding of this pass is internal, not external

`dev/active/usage-per-account-capture-2026-09-19.md` (Lead, filed yesterday, PM-reaffirmed 09-15
per the doc's own header: *"track more granularly as a rule"*) proposes **exactly** the calibration
mechanism every external field above says this model needs: a daily manual capture of PM's actual
usage-dashboard reading into `dev/heartbeats/usage-per-account.tsv`. **Checked directly this fire**:
the file does not exist yet — `find dev/heartbeats -iname "*usage-per-account*"` returns nothing,
and `decisions.log` has no ratification entry for the proposal. It is a written, PM-reaffirmed
proposal with **zero rows captured**.

**This is the actual current blocker**, more concrete than "no agent can see the dashboard" in the
abstract: a mechanism to capture ground-truth readings has already been designed and PM-endorsed,
and simply hasn't been implemented or started. Every field surveyed above says the same thing in
different vocabulary: **without a validation subsample (paired proxy + ground-truth readings), no
amount of internal-proxy correlation can be calibrated, only internally consistent.** Building the
correlation model before this capture exists and has accumulated even a handful of paired readings
would produce exactly the "beautiful internal-consistency exercise" Exec's memo warned against.

## What this pass recommends, not yet decided by PA alone

1. **Surface Lead's proposal's implementation status to PM as part of the calibration-shape
   question** Exec suggested agreeing before building — not as a separate thread, the same one.
   The question isn't just "what shape should calibration take," it's "the shape was already
   proposed 09-15/09-19 and hasn't started — should it?"
2. **Don't build the proxy-correlation model until at least a few paired readings exist** — per the
   errors-in-variables literature, a model calibrated on zero ground-truth points is not a weaker
   version of a calibrated model, it's a different (uncalibrated, potentially systematically biased)
   thing, and should be reported as such rather than presented with unearned confidence.
3. **The dispatch-tier dimension is likely the highest-value one to instrument regardless** of the
   calibration question — it's already flagged cohort-wide as under-measured (09-14 incident, CIO's
   09-20 new logging convention), the LLM-observability field has mature tooling/vocabulary for it,
   and it doesn't need PM's usage dashboard to start being useful (dispatch tier vs. token cost is
   internally verifiable today).

## Addendum (19:21 fire) — calibration question sent; dispatch-tier dimension checked, same pattern found in miniature

**Calibration-shape question sent to Exec, cc PM** (`mailboxes/pa/sent/question-pa-to-exec-cc-pm-
calibration-shape-for-usage-model-and-leads-unimplemented-proposal-2026-09-20.md`): does Lead's
proposal get implemented, since no model here can be calibrated without it. Pending PM's answer.

**Checked the dispatch-tier dimension (recommendation 3 above) rather than leaving it as a bare
suggestion**: CIO implemented PM's 09-20 dispatch-tier-logging ruling same-day, but **only as a
prose rule** — CLAUDE.md's Subagents section now asks each dispatcher to log the assigned tier
inside their own session log entry, per-dispatch. There is **no structured, queryable, or
aggregated surface** — the data (where it exists at all) is scattered as prose across 11 different
roles' session logs, unverifiable for compliance the same way the original 09-14 rule was before
this ruling. `grep`-ing recent session logs for tier mentions found real hits (09-14 through
09-20, multiple roles) but no consistent format to parse reliably.

**This is the exact pattern the prior-art pass already found, recurring one layer down**:
a real, PM-ratified rule with zero mechanical enforcement or aggregation is not the same as
instrumented data — "structural fixes hold, promises don't," now visible in this dimension
specifically, not just in the calibration-mechanism question above. **Revises recommendation 3**:
the dispatch-tier dimension is *not* actually independently buildable today without either (a) a
prose-parsing pass across session logs (fragile, same fragility this whole exercise is trying to
avoid) or (b) CIO/Lead adding a structured sink (a TSV row per dispatch, same shape as Lead's
usage-per-account proposal) — which doesn't exist and isn't PA's to build unilaterally on another
role's logging convention. Not chasing this further this fire; noting it honestly rather than
either overclaiming progress or silently dropping the thread.

## What's not done

- The actual model (dimensions, functional form, granularity) — still not designed; genuinely
  waiting on PM's calibration answer for the proxy-vs-ground-truth dimensions, and on CIO/Lead for
  whether the dispatch-tier dimension gets a structured sink.
- Any data collection or measurement — none yet, for either reason above.
- **PM interaction**: the calibration-shape question has been sent (19:21 fire); no response yet.

**Verified how**: all four prior-art searches run live this fire (WebSearch, 4 queries, sources
listed inline via the tool's own citations — not from training-data recall, given how fast this
tooling space moves). Lead's proposal read in full directly, not summarized from a carry-forward.
`usage-per-account.tsv`'s non-existence and `decisions.log`'s lack of a ratification entry both
checked live this fire, not assumed. **Layer**: literature/tooling survey + one direct repo-state
check. **Not verified**: whether PM's actual usage-dashboard reading resembles conversation volume,
token spend, session count, or something else entirely — genuinely unknown from in here, which is
itself the reason the calibration question needs to go to PM rather than be guessed.
