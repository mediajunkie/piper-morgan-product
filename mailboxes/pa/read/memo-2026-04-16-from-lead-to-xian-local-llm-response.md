---
from: Lead Developer
to: xian
cc: PA (Piper Alpha), Janus
date: 2026-04-16
subject: Local LLM research — adapts cleanly to PM testing, less so to floor
priority: normal
response-requested: no (discussion welcome)
---

# Local LLM Research — Where Argus's Recommendations Fit Piper Morgan

xian — read the report (`~/Development/klatch/docs/research/local-model-viability-2026-04-15.md`). Thorough and directly applicable. Short answers to your four questions, then a concrete first step.

## Unexpected cross-thread: Ollama's `format: "json"` is exactly what today's Gemini issue needs

Before the structured answers — an interesting connection.

Earlier today I wired Gemini into `LLMClient` as a real provider (commit 1a8fdde6). Smoke-tested both the conversation path (works cleanly) and the intent classifier path (fails because Gemini often returns prose when the classifier prompt asks for JSON). Filed as **#987 GEMINI-JSON** — the fix is to set `response_mime_type="application/json"` in Gemini's generation_config.

Argus's report shows Ollama solves this with `format: 'json'` in the request body. Both Gemini and Ollama treat JSON mode as an explicit per-call flag rather than inferring it from the prompt — which is how Anthropic/OpenAI have trained us to think. If/when we add Ollama as a fourth provider, the same one-line toggle applies, and the plumbing we build for #987 probably accommodates it.

Since users BYO keys, #987 is a near-term priority regardless of the local-model question — we can't ship a BYO-Gemini workflow that silently degrades the classifier.

## Question 1 — AAXT #929 as a local-judge candidate

**Yes, directly applicable.** #929 is pattern-for-pattern the same as Klatch's AAXT: multi-turn scenarios scored by an LLM-as-judge against a rubric (Colleague Test). Judge currently uses `claude-sonnet-4-20250514` per the conftest at `tests/aaxt/conftest.py:25` (already supports `AAXT_JUDGE_MODEL` override for cheaper models — yesterday we ran it with `gemini-2.5-flash` successfully).

Adding Ollama as a third option is a ~20-line change: detect `AAXT_JUDGE_MODEL` starting with `ollama/` or similar prefix, route to Ollama HTTP endpoint with `format: 'json'`. Keep Anthropic as the production/release-gate judge, use Ollama for dev loop runs.

**Migration path**:
1. Install Ollama locally, pull `gemma4:26b-a4b` (Argus's sweet-spot recommendation)
2. Manually test one AAXT scenario with the local judge — compare scored results vs. Anthropic judge on the same response
3. If quality matches within acceptable bounds, wire it into conftest as an opt-in provider
4. Document in testing docs: "local model for dev loops, Anthropic for release gates"

Effort: small-medium, mostly exploratory evaluation time, not code.

## Question 2 — Canonical suite (#928) tier 2 LLM-as-judge

**Viable, but lower-priority than AAXT.** Tier 2 of #928 is env-gated (runs when `CANONICAL_JUDGE=true`), so the cost pressure is real but already bounded. AAXT currently runs nightly (~$0.50/run); moving the judge to local would let tier 2 run on every conversation-code PR without additional cost.

Practical caveat: tier 2 judge uses the same rubric as #929 (Colleague Test six-point scoring). If we validate local-judge quality for #929, we get tier 2 for free on the same plumbing. So the order is: AAXT first, canonical tier 2 second — not independent efforts.

## Question 3 — Local model for the conversational floor

**Agree with Argus: not yet.** Two specific concerns:

1. **Extended reasoning.** The floor gets queries like "help me think through prioritization for this sprint" — the LLM is doing multi-step reasoning with PM frameworks. Gemma 4 31B is benchmark-competitive but the "feel" gap Argus describes is exactly the failure mode the Colleague Test catches. I wouldn't trust a local model on the floor until we have canonical retest evidence that Identity/Temporal/Status quality holds.

2. **Extended context.** The floor prompt currently runs ~1.3K tokens. Assembled context + conversation history can push total input to 3-4K. Gemma 4's 256K context window covers that, but prompt adherence at the far end of the context is worse for smaller models. Worth testing eventually, but not urgent.

A reasonable long-term pattern — which Argus implies — is **tiered routing within the floor**: local model handles short/simple queries, cloud model handles reasoning-heavy ones. This is future work, post-M3 at earliest.

## Question 4 — Infrastructure lift

**Low for testing, higher for production.**

For testing (local-judge on dev machines):
- Ollama install: `brew install ollama` (one command, ~300MB binary)
- Model pull: `ollama pull gemma4:26b-a4b` (~16 GB disk, one-time)
- Memory headroom: 24GB+ unified memory recommended (faoilean has this)
- Runtime: runs alongside other processes; Q4 MoE uses ~16 GB VRAM when active, sleeps otherwise
- No uptime requirement — only running during test runs

For production (a shared Ollama server for CI and potentially BYO-local-model users):
- Dedicated inference host (cloud GPU or Mac Studio M2 Ultra per Argus's benchmarks)
- Uptime monitoring
- Authentication / rate limiting
- Cost: $200-800/month for the host vs. ~$50-200/month current LLM spend — **probably doesn't pencil** at current volume

Recommendation: start with dev-machine Ollama for #929, defer the hosted-inference question until utilization actually justifies it.

## Recommended first step

Fold into the next M3 planning window (not mid-M2-sprint):

- **File as issue**: "AAXT local-judge provider option via Ollama" — scope: add Ollama provider to `tests/aaxt/conftest.py` judge_client logic, document the quality A/B process, run manual comparison for 5 scenarios.
- **Keep cloud judge as default** for CI and release gates. Local is opt-in via env var.
- **Bundle with #987** (Gemini JSON) as related work — both are "non-OpenAI/Anthropic provider wiring" and share the `format: 'json'` pattern.

## What this does NOT change

- The conversational floor stays on cloud (Anthropic primary, Gemini + OpenAI fallback per commit 1a8fdde6)
- The intent classifier stays on cloud (JSON compliance + reasoning quality)
- Canonical retest continues using Anthropic judge for now
- BYO-Gemini-key user flow: addressed via #987 (JSON mode), not by migrating to local

## Risks I want to flag

1. **Free tier quotas look attractive but aren't production-ready.** Today's Gemini smoke test hit the 5 RPM limit immediately — filed as #988 GEMINI-QUOTA. Same economics question for any "local for cost savings" argument: we should measure current spend honestly before investing engineering time in cheaper alternatives.

2. **Six-failure-mode taxonomy adoption (PA's xpoll memo) is lower-cost and higher-value than local-judge migration.** Changing the scorer's output vocabulary to {Correct, Reconstructed, Confabulated, Absent, Phantom, Subliminal} makes PM's results comparable to Klatch's without requiring local infrastructure. If we're going to invest in test infrastructure improvements, that's the cheaper win.

3. **Scope pressure on M2c.** We're mid-sprint on #950 (closing this session), #922 (still open), and haven't started #964. Local-model migration is a real initiative that needs its own epic, not a side-task.

---

Happy to discuss further — either async over the mailbox or in a live session. No deadline I'm aware of. M2c closing cleanly is the higher priority this week.

— Lead Dev
