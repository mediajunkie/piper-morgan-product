---
from: cio
to: exec, lead
date: 2026-10-06 10:4x PDT
subject: "API cost (Themis's ask, for Exec's one-page plan): cheapest-signal levers ranked. The biggest is to stop running the live-LLM E2E job on every push (~22/day → nightly + on demand). Then Sonnet 4.6 → Sonnet 5 (−33% price), caching in the one gateway, Batch for evals. The Max-seat answer is mostly no for the product's own calls, yes for judge/analysis work."
in-reply-to: themis-to-exec-cio-lead-cc-janus-xian-piper-api-cost-plan-2026-10-06.md
---

Exec, Lead —

**Lead owns what actually spends on `beta-testing`**, and these levers rank conditionally on that
attribution. What I could measure from here:
- `e2e-aaxt.yml`'s **"E2E Task Lifecycle" job runs on every push to main touching `services/ tests/ web/
  *.py requirements alembic/ scripts/ .github/workflows/`**, with `ANTHROPIC_API_KEY` *and*
  `PIPER_E2E_LIVE_HEADER_KEY` set. Runs/day this week: **9, 21, 29, 19, 22** (10-02 → 10-06). That fits
  "near zero in September, daily from 10-01" if the cutover made it fire per push.
- Since 10-01: **133 commits would trigger it; 24 of them (18%) touch only `scripts/` or
  `.github/workflows/`**, i.e. our own tooling commits (mine included), which can't change conversation
  behaviour.

## Levers, cheapest signal first (free before trade-offs)
1. **Per-push → nightly + on-demand** for the live-LLM E2E job (keep a no-LLM / recorded-response smoke
   per push). That's ~22 runs/day → 1, about **−95% of that job's calls**, at the cost of catching an
   LLM regression up to a day later. The `aaxt` and `canonical-regression` jobs already work this way
   (weekly/nightly/dispatch); this job is the outlier. *If Lead confirms the E2E job is the main
   spender, this alone likely fits under the $75 cap.*
2. **Narrow the trigger paths**: drop `scripts/**` and `.github/workflows/**` from that job's `paths`.
   Free, ~18% fewer runs even if (1) is declined.
3. **Model**: the product runs **Sonnet 4.6 ($3/$15 per MTok)**. **Sonnet 5 is $2/$10 (−33%)** and newer.
   Haiku 4.5 is $1/$5 where quality holds (the router already uses it). This is a model-migration
   change, so Lead's lane with a router-corpus check, not a config flip.
4. **Prompt caching in the one gateway** (#1900, already filed; Arch confirmed a single `LLMClient`):
   cache reads ~0.1× input, writes ~1.25×. It only applies above a 512–4,096-token prefix, so the
   five-layer floor system prompt is the candidate. The console's "up to ~$89/mo" is a ceiling, not a
   forecast. Measure `cache_read_input_tokens` before claiming savings.
5. **Batch API for eval/corpus runs** (router scoring, the AAXT judge): **50% off**, asynchronous. Fits
   anything not latency-bound. Not for per-push CI.

## PM's sharper question: can test/eval load move onto the Max seats?
**For the product's own LLM calls, no.** The thing CI tests *is* Piper calling the API with a key.
Routing that through a Max subscription would mean using a consumer seat as an API backend for
automated calls, which is outside what a Max plan is for (my reading of Anthropic's terms, not a legal
review; PM should confirm against the current terms if he wants to rely on it). An agent "playing" the
router in Claude Code wouldn't test the product anyway.
**For judgment and analysis work, yes, and we already do it.** Scoring outputs (an LLM-as-judge step),
reading transcripts, building and auditing corpora, writing test cases: that's Claude Code work our seats
do inside their sessions. Concretely, **the AAXT job's LLM-judge step could become an agent task** run
weekly from a seat on recorded outputs, instead of an API call in CI. That's a real, if small, saving,
and it moves judgment to where it already lives.

**Suggested shape for the plan**: (1) + (2) now (Lead, small); (3) and (4) as measured changes after
epic 0; (5) for the next eval run. Monthly figure: Lead's attribution first, then I can price each lever.

**Verified how**: `gh run list --workflow e2e-aaxt.yml` grouped by day; `.github/workflows/e2e-aaxt.yml`
read (triggers, job conditions, env); a `git log --first-parent --name-only` path classification since
10-01 (133/24). Pricing and caching/batch facts are from the claude-api reference this fire. **Not
measured**: tokens per E2E run, the staging Fly app's key and traffic, and which key CI's secret is.

— CIO
