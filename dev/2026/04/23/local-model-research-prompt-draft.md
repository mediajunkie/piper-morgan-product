# Research Prompt Draft: Frontier Local Models for Piper's Secondary-LLM Tier

**Date**: 2026-04-23
**Author**: Lead Dev (code-opus)
**Intended consumer**: General-purpose research subagent (likely Opus, with web access)
**Intended reader of output**: Leadership team (PM, PPM, CXO, CIO, Architect, PA)

---

## Context to seed the subagent

Piper Morgan already has a provider-agnostic LLM client (`services/llm/clients.py` + `config.py`) supporting Anthropic, OpenAI, Gemini, and Perplexity. Task-type → model-tier config is already decoupled from provider selection; `PROVIDER_MODELS` maps provider × tier → specific model. Fallback order is `[ANTHROPIC, GEMINI, OPENAI]`.

Adding a local-model tier (e.g., Gemma running via Ollama on developer / server hardware) would be additive — a new `LLMProvider.LOCAL` enum value, a local-tier entry in `PROVIDER_MODELS`, and routing logic that prefers local for designated task types.

**Guard rail from PM (2026-04-23)**: Local models will NOT be used for primary voice-bearing response generation until a benchmark has been met. First-candidate tasks for local tier are **bounded-output, non-voice, internal** functions — intent classification, slot filling, relevance scoring, routing decisions.

**What this research is and isn't**:
- It IS: landscape survey, published benchmark review, tooling survey, deployment realism check.
- It IS NOT: empirical benchmarking by the subagent, model recommendations, voice/tone evaluation, architecture prescriptions.

---

## Four questions — answer each in its own section

### Q1: Frontier local-model landscape (April 2026)

Survey current best-in-class open-weight models at two size tiers: **≤8B params** and **8–30B params**. For each of the notable entrants (at minimum: latest Gemma generation, Llama 3.3 or newer, Qwen 2.5 / 3, Mistral recent releases):

- Release date and size
- General capability profile (common benchmark scores: MMLU, MT-Bench, instruction-following)
- Known weaknesses or failure modes
- License terms (commercial-use implications)

Keep each model to one tight paragraph. Prioritize recent (last 6 months) releases.

### Q2: Cloud-vs-local quality gap for intent classification

Our first plausible use case for a local tier is **intent classification** — bounded categories, small-output task, currently done by a cloud frontier model. Find published evidence on:

- Small-model performance on bounded classification tasks (sentiment, intent, topic) vs. frontier cloud models
- What's the typical F1 / accuracy gap? (a few percent? double digits?)
- Are there task types where small models match frontier performance?
- Are there task types where the gap is catastrophic?

If a rigorous published head-to-head doesn't exist, say so — don't fabricate one.

### Q3: Provider-abstraction and routing tooling

Our existing abstraction is home-grown but functional. Before we extend it, survey:

- **LiteLLM** — what does it provide, what's its production-readiness, is it additive or replacement-oriented for a codebase with existing abstraction?
- **Ollama** — local-model serving layer; maturity, Python client, integration patterns
- **Other relevant libraries** — whatever else has traction in early 2026 for tiered / multi-provider LLM routing
- **Routing patterns in public codebases** — is there a published pattern for per-task tier routing (e.g., "classification → local, reasoning → cloud") we can learn from?

We're explicitly NOT asking the subagent to pick one. We're asking what the landscape looks like.

### Q4: Deployment realism

Practical questions about running a local model in production alongside Piper:

- **VRAM / RAM requirements** for ≤8B and 8–30B models at various quantization levels (fp16, int8, int4)
- **Latency** — typical first-token and full-response latency for intent-classification-sized calls on commodity hardware (Apple Silicon, consumer NVIDIA, modest cloud GPU)
- **Cost** — rough cost-per-GPU-hour at cloud providers for the hardware that can run these tiers
- **Ops realities** — what's the state of reliability / observability tooling for local-model serving?

Just enough detail for leadership to tell whether "local tier in production" is a 2026 story or a 2027 story.

---

## Output format

- Markdown, target ~3 pages (not 10)
- Readable in 15 min
- Each question section opens with a one-sentence headline answer, then the detail
- Include citations (links to papers, model cards, benchmark leaderboards, library repos)
- If a question can't be answered from public sources, say so explicitly — do not fabricate numbers

## Explicit out-of-scope (do not do any of these)

- Do not recommend a specific model for Piper to adopt.
- Do not benchmark models yourself.
- Do not evaluate voice / tone / creative writing quality — we've taken voice off the table for local tier.
- Do not propose architecture changes to `services/llm/`.
- Do not read Piper's codebase beyond the context provided in this prompt.

---

## Stop conditions (for the subagent)

If you encounter any of these, return a partial report and flag:
- A question where public data is too thin to give a meaningful answer
- A tooling landscape shift that invalidates the framing (e.g., "there's now a dominant standard library that makes the abstraction question moot")
- Evidence that the cloud-vs-local gap on our target tasks is so catastrophic that the investigation isn't worth continuing

---

## PM-specific context to incorporate (pending PM input)

PM has been experimenting with a local Gemma harness; subagent should compare published landscape against whatever PM observes in their own setup. PM to supply:
- Gemma version running
- Hardware profile
- Observed capability (what it does well, what it fumbles)

(If PM input arrives, the subagent should note it explicitly in the output as "corroborates / contradicts published claim X.")
