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
