# Do decision models (Jev, Laya) beat LLMs anywhere we build? — first read

**Research hub trial, question 1** (xian's ruling via Themis, 2026-09-28). Author: CIO (hub).
Status: first read, from desk research plus our own code; Argus's Klatch reply folded in 09-28 22:07. PM ruled 09-28: the PM-side trial is held until post-MVP. No model has been run yet. The one
"try it" below is a trial design, not a result.

## What these models are (sourced, not tested)

- **Jev** (TypeSafe AI, launched 9/15, limited early access): text/JSON "state" in, typed numbers
  out. Three question types: yes/no ("noul", a 0–1 confidence), choice (a distribution over
  options), and score (a value on a described range). It returns no text. Many questions run in
  parallel for about the cost of one. Input $0.042/M tokens, output free. Per the author, it is
  "not great with numbers, dates, or adversarial content." Source: [Simon Willison, 9/21](https://simonwillison.net/2026/Sep/21/jev/).
- **Laya** (Convai Innovations, 9/18): an open (Apache 2.0) 421M-parameter model with the same
  three primitives. Self-hostable and fine-tunable. Reported latency is ~33ms per query vs Jev's
  ~240–280ms, and it reportedly edges Jev on shared public datasets. **These are vendor and press
  claims we have not reproduced.** Sources: [eesel](https://www.eesel.ai/blog/laya-ai),
  [DEV comparison](https://dev.to/jamilxt/jev-vs-laya-the-same-ai-idea-one-closed-and-one-open-3c6e).

**What's actually new here is calibration, not classification.** An LLM can already classify.
What it can't give you is a trustworthy probability. Our own router asks Haiku for a
`"confidence": <0.0-1.0>` inside its JSON (`services/intent_service/inversion_router.py`,
prompt at ~L360). That number is the model's self-report, clamped but never calibrated. A
decision model trained for calibration (Laya's "RLCD") claims the number means what it says.
That is the only property that makes an **abstain threshold** trustworthy, and an abstain
threshold is what lets "unknown" route to a clarifying question instead of defaulting to a guess.

## Verdicts per candidate

### 1. PM intent classification — **TRY IT** (narrowly: operation selection only)

- **Fit**: the Phase-1 inversion router is one constrained choice among canonical operations
  derived from the registry at call time. That is exactly the "choice" primitive.
- **What a decision model can't do**: the router also returns `args` (argument extraction, which
  is text) and, since 9/27, a multi-operation `plan`. Neither fits a numbers-only output. So the
  realistic shape is a **hybrid**: the decision model picks the operation and gives a calibrated
  distribution, and the LLM is called only for `args`, or only when the decision model abstains.
- **Trial design (cheap, and it needs no vendor access)**: run **Laya locally** over Lead's
  existing frozen 151-row corpus and score it with the existing
  `scripts/inversion_phase1_shadow_score.py` (MATCH/MISMATCH per row). The router runs Haiku 4.5
  on Anthropic (config task `inversion_routing` → "light" tier); Lead's note named gpt-4o-mini,
  so confirm which is the baseline before the run. Measure two things:
  1. top-1 accuracy vs the current router;
  2. **the real test — calibration**: at an abstain threshold *t*, what fraction of MISMATCH rows
     fall below *t*, and what fraction of MATCH rows are lost? If abstention catches most
     mismatches at a small coverage cost, that is a result no LLM self-report gives us.
- **Open technical question (unverified)**: whether Laya accepts a per-request option set. Our
  grammar is derived at call time, and a hand-frozen option list would reintroduce the drift
  PDR-006 condition 2 forbids.
- **Side benefits**: (a) local inference means no user text leaves the box; (b) a numbers-only
  output can't carry an injected instruction downstream. Caveat: Jev is reported weak on
  adversarial input, and intent text is user-supplied, so adversarial rows belong in the corpus.
- **Why it's cheap**: Arch confirmed 9/28 that `LLMClient` is already a single gateway (11 call
  sites). Adding a model type is a config task plus one client path, not a rewire.
- **Who**: Lead offered to run the corpus A/B. Sequencing is PM's call, since Lead's queue sits
  behind epic 0.

### 2. Triage and routing across agents — **NO**

Cross-agent routing (which inbox, how urgent, whether it needs xian) happens inside the agents'
own reasoning in Claude Code sessions, not at an API call site we control. There's nothing to
swap a model into, and the volume is tens of memos a day. The failures we've actually had here
were unread mail, globbed `read/` moves, and over-cc'ing. Those are discipline and mechanism
failures that a classifier wouldn't fix.

### 3. Go/no-go gates where "unknown" must not default to "healthy" — **NOT YET** (mostly **no**)

The principle is right, but most of our gates are **deterministic and measurable**: CI
conclusions, freeze-check heartbeats, lints, ratchet tests. A calibrated probability is strictly
worse than an exact check wherever an exact check exists. The recurring failure (methodology-44,
"clear is not a measurement") has been **a check that never ran or measured the wrong layer**.
A model would add a second unmeasured layer, not remove one. The narrow place where it could help
is **judgment-shaped** triage with no exact check, e.g. the unboarded-PM-items scan's candidate
list (`scripts/check-unboarded-pm-items.sh`), where "abstain → a human looks" beats "guess →
silent." Revisit only if candidate 1 shows calibration actually holds on our data.

## Spokes

- **Argus (Klatch), replied 09-28** (read all 5 of Klatch's `messages.create`/`stream` call
  sites): **one candidate, `packages/server/src/aaxt/scorer.ts`**. The AAXT test harness asks an
  auxiliary LLM for a 6-way label (Correct / Reconstructed / Confabulated / Absent / Phantom /
  Subliminal) plus a self-reported confidence. It's the same shape as our router, with the same
  weak link (uncalibrated confidence). Two other call sites are genuinely generative, so no. A
  near-miss: `import/entity-guess.ts` is hand-tuned regex, not a model call, but it already follows
  the principle that a blank beats a confident wrong guess. Not proposed for replacement.
  **Network-level read**: two independent projects found the same candidate shape (a typed label
  with an uncalibrated self-reported confidence). The AAXT scorer may be the cheaper first trial,
  because it's internal test tooling with no user path and isn't in Piper Morgan's MVP queue. That
  choice belongs to Klatch and xian.
- **Vergil (OpenLaws)**: out, per xian 9/28 (project not active).
- **Janus**: cc'd for corpus curation.

## Verified how

Method: fetched the Willison post and searched for Laya this turn (quoted claims are marked as
sourced, not tested). Read `inversion_router.py`'s module docstring and prompt/validation code
and `services/llm/config.py`'s tier mapping at origin/main `b74d352a3f`. Layer: desk research plus
static source read. **No model inference was run.** Denominator: 3 of 3 candidates Themis named
were assessed, and 1 of our routing surfaces was read in depth (the Phase-1 inversion router, not
the production `classifier.py`).


## Trial log — step 1, feasibility (2026-10-02, CIO-side, PM-cleared 10-01; no Lead involvement)

Env: `~/.cache/piper-morgan/trial-env` (py3.11 = CI, project `requirements.txt`), outside the repo.

- **Corpus**: 382 rows via the project's own loader (`scripts/inversion_phase0_baseline.py::load_corpus`).
  289 have an `action:` answer (scoreable for operation choice), 54 REVIEW, 31 floor, 4 category,
  4 plan. The scorer docstring's "93" and the earlier "151" are both stale. The fixture is **not
  valid YAML** (unescaped inner quotes; the project's regex loader masks it), filed as #1921.
- **Grammar**: `derive_routing_grammar()` gives **64 canonical operations**. Size (chars ÷ 4, a rough
  estimate, not the real tokenizer): names only ≈ 277 tokens; names + descriptions ≈ 1,158 tokens
  (median description 29 chars, max 435).
- **Laya's actual constraint** (model card, vendor-stated, not yet reproduced): options share a
  192-token head budget by default (`head_max_len`). At ~77 options labels get 3–4 tokens each and
  become "indistinguishable"; for 50+ options the card recommends raising `head_max_len` or a
  **hierarchical choice**. **At 64 options, a flat choice is likely degraded.**
- **Abstain signal**: the card says `action.act_probability` "carries no usable signal yet; gate on
  `confidence` instead (AUROC 0.77)". **So the built-in escalate head can't be the abstain
  mechanism.** The trial gates on choice confidence, and the 0.77 figure is the vendor's, to be
  measured here.
- CPU: ~0.2–0.5 s/question, 808 MB checkpoint. Feasible on Amber.

**Design change from step 1**: run **two-stage choice**: (a) category (the corpus's own ~10 categories,
each option labelled with a short description) → (b) operation among that category's canonical ops
(names + descriptions, fits the head budget). Also run a **flat 64-way with `head_max_len` raised**
as a comparison arm, so the hierarchy's benefit is measured, not assumed. Score: top-1 on the 289
`action:` rows; then confidence-threshold sweeps (coverage vs. error caught), the trial's real
question.


## Trial results — step 2 (2026-10-02, CIO-side, no Lead involvement)

Harness `scripts/decision_model_trial.py` (read-only; scoring = the shadow scorer's own
`router_matches`). Comparison set: the **221 asserted rows** in Lead's recorded 2026-10-01 Haiku 4.5
run that carry a confidence. Same rows, same matcher. Laya `convaiinnovations/laya` (English, 421M),
v0.3.24, CPU, **no fine-tuning**. Option labels = operation name → description truncated to 160 chars.

| arm | top-1 correct | vs Haiku (same rows) | confidence AUROC (right vs wrong) | note |
|---|---:|---:|---:|---|
| **Haiku 4.5 (recorded)** | **188/221 (85%)** | — | **0.739** (self-reported) | coarse: mostly 0.85 / 0.95 |
| Laya flat 64-way, head_max_len 448 | 62/221 (28%) | −126 | 0.765 | 0 rows truncated; **vendor warning: choice ≥11 options uses invalid temperatures, so confidence is uncalibrated** |
| Laya shortlist k=10 | 48/221 (22%) | −140 | 0.692 | embed-rank often drops the right op before choosing |
| Laya shortlist k=5 | 33/221 (15%) | −155 | 0.706 | worse as k shrinks, which confirms the shortlist is the loss |

Flat-arm failure shape: collapses onto a few catch-all labels (`search_documents` ×41, `week_calendar`
×28 of its 159 misses). Overlap: Laya right where Haiku wrong on 8 rows; both wrong on 25.

### Verdict on Q1's one "try it": **no, as shipped**
- **Accuracy is disqualifying**: 15–28% vs 85% on identical rows. No threshold rescues a classifier
  that is wrong three times in four.
- **The calibration premise didn't hold here.** The flat arm's AUROC edge (0.765 vs 0.739) is small,
  and it's on the very arm the vendor flags as uncalibrated. The calibration-valid arms (k ≤ 10) rank
  their own errors **worse** than Haiku does.
- **The finding that IS actionable came free, from data we already had**: Haiku's own confidence
  already separates its right and wrong answers moderately (AUROC 0.739). An abstain-and-ask gate at
  ~0.80 would have caught 13/33 of its errors (39%) for 12/188 lost right answers (6%), with no new
  model or infrastructure. If PM wants "unsure → ask" behaviour post-MVP, that's the cheap first
  experiment, and it belongs to Lead's router, not to a decision model.

### What this trial did NOT test (stated, not implied)
- **Fine-tuning.** Laya supports it, and 382 corpus rows might help, but that needs a held-out split
  and is a real project, not a trial. The typed-decisions and multilingual checkpoints were also
  untested.
- **Small, natural choice sets.** These models are built for questions with a handful of options.
  The router's 64-way choice is about the worst case for them, so this verdict doesn't transfer to,
  e.g., Klatch's 6-way AAXT scorer (Argus's candidate). That remains a plausible fit, for Klatch to
  decide.
- Prompt/label engineering beyond one reasonable instruction and 160-char descriptions.

**Verified how**: four full harness runs this session (outputs saved in the CIO scratchpad; summaries
quoted above); Haiku figures recomputed from the committed 10-01 report's row detail. Layer: operation
selection, context-free, scored by the production scorer's matcher. Denominator: 221/221 comparison
rows per arm.
