
# Cross-Pollination Brief — October 7, 2026

Two insights from Piper Morgan's 48-hour window: a formal architectural principle that names the correct boundary between LLM interpretation and deterministic code, and a discovered platform constraint that silently prevents prompt caching from activating on Haiku.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. LLM decides meaning; code decides permission, checks meaning against real data, and shows before it acts — Piper Morgan, Arch, ADR-080, commit `8c7662e1e0`

**From:** Piper Morgan, Architect  
**Relevant to:** Klatch, and any team building LLM-powered tools with destructive or multi-item operations

ADR-080, accepted 2026-10-06, names the boundary that PM had been navigating implicitly for months. PM calls it "wish we'd stated this a year ago." The principle in six decisions:

- **D1 — LLM decides meaning, not code.** The LLM extracts which operation, which items, and the verb's sense. No new regex or keyword-matching interpretation code is added at the gate layer; that work belongs to the LLM.
- **D2 — Code checks meaning against real data before acting.** Before executing, code confirms that the items the LLM identified actually exist and are what the caller expects. "The LLM said so" is not execution authority.
- **D3 — Code decides permissions.** The LLM never determines whether an action is allowed. Permission checks are deterministic, based on caller role and resource state.
- **D4 — Enumerate and confirm before multi-item or destructive changes.** Show the user exactly what will and won't be touched; require acknowledgment. The "show before you act" step is mandatory, not a UX nicety.
- **D5 — Statelessness stays.** The LLM does not hold state across turns (ADR-078 D4 is preserved). Meaning extraction is per-turn.
- **D6 — Interpretation layer only shrinks.** The gate-layer is actively being migrated off regex chains; no new ones are added. ADR enforces this mechanically via `TestExtractionPatternRatchet`.

The principle is portable to any LLM-powered product that takes user instructions and acts on data: the LLM is the interpretation engine; the code is the safety layer and execution authority. Conflating the two — letting the LLM decide permissions, or writing keyword-matching code to do what the LLM should do — produces systems that are simultaneously over-permissive and brittle.

**Suggested action for Klatch:** Audit whether any routing or permission logic currently lives in code that pattern-matches user intent. If so, that's D1 work for the LLM; the code layer should only check whether the resolved operation is permitted for the caller.

---

### 2. Haiku requires ≥4,096 tokens for prompt caching to activate — PM's router prompt falls short at 3,003 tokens — Piper Morgan, Lead Dev, commit `b1feb505cd`

**From:** Piper Morgan, Lead Dev  
**Relevant to:** Klatch (uses Anthropic SDK), any team using Haiku with prompt-caching expectations

PM discovered that its router prompt — 3,003 tokens total, with ~2,997 tokens as a static prefix (99.6% eligible) — was silently not being cached. Anthropic's Haiku model requires a minimum of 4,096 tokens before prompt caching activates; the 3,003-token prefix never crossed the threshold. Caching appeared configured; it simply wasn't firing.

The offline re-verdict tool that surfaced this (`scripts/inversion_offline_reverdict.py`, 452/452 fidelity on expectation-only changes) was itself a byproduct of the investigation — it replays a test corpus against a new router prompt without paying API costs, enabling the team to tune the prefix length and test the outcome before deploying.

The fix requires either adding ~1,100 tokens of useful content to the static prefix (additional examples, context, or documentation that genuinely helps routing quality) or switching to a model with a lower caching threshold. Adding padding without utility would defeat the purpose — the 1,100 tokens need to earn their place in the prompt.

Minimum thresholds by model (as of the discovery):
- Claude Haiku: 4,096 tokens
- Claude Sonnet: 1,024 tokens
- Claude Opus: 1,024 tokens

**Suggested action:** If you're using Haiku with a `cache_control` block and noticing your cache hit rate is lower than expected, check whether your static prefix actually crosses 4,096 tokens. The threshold is not documented prominently; it's easy to assume caching is active when it isn't.

## Sources Read

- **Klatch** — `docs/logs/2026-10-06-calliope-sonnet-log.md` (Round 344 probe, living-doc convention compliance); `docs/mail/` (entity-delete ruling from xian: allow empty klatches, add delete-klatch prompt, anomalous empty state surfaced). Ruling logged; no transferable architectural insight beyond what entity-delete UX represents project-internally.
- **Piper Morgan** — `docs/internal/architecture/adrs/adr-080-llm-decides-meaning-code-decides-permission.md` (Arch, `8c7662e1e0`); `dev/2026/10/06/2026-10-06-0623-lead-code-log.md` (offline re-verdict tool, 452/452 fidelity, Haiku cache threshold discovery, `b1feb505cd`); `dev/2026/10/06/2026-10-06-0627-arch-code-log.md` (offline re-verdict scope boundary).
- **Globe** — recent commits; operational activity (health-check script). Not brief-worthy.
- **Weather** — recent commits; operational. Not brief-worthy.
- **One Job** — recent commits; build/release activity. Not brief-worthy.
- **NYT Crossword** — recent commits. Not brief-worthy.
- **Mediajunkie** — recent commits. Not brief-worthy.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
