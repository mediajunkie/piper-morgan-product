# Design record: `LLMClient` is the single LLM gateway — ratifying what already exists

**Status**: written 2026-09-28 (Arch), from a real trigger — PM's spend audit asked "should LLM
calls route through some kind of bus? Does that need an architecture review?" and nobody could
answer in under a fresh investigation, because the pattern was never written up. This doc is that
answer, so the next time the question is asked, it costs two minutes instead of a re-investigation.
**Trigger, named per Exec's 2026-08-29 ruling** (any ADR/pattern needs an actual trigger or it's
academic): this exact question being asked, unanswerable from existing docs, twice now (Themis's
09-28 ask is the second time this shape has surfaced).

## The question that triggered this

A grep for files referencing "Anthropic" across `services/` found 113 hits. Read naively, that
looks like 113 places making LLM calls with no shared discipline — a real architectural smell if
true. **It wasn't a call-site count.**

## What's actually there

`services/llm/clients.py`'s `LLMClient` is a single, already-shipped gateway. Verified directly,
not assumed:

- **Raw provider SDK construction**: exactly 2 sites in the whole tree. `LLMClient` itself, and
  `services/llm/request_key.py` — whose own docstring calls it "the only Anthropic construction
  site in the tree," a deliberate second chokepoint for BYOC per-request credential billing (a
  user's bound key gets its own fresh client, billed to them, per #1809/#1812/#1819), not a bypass
  of the shared client.
- **Real call sites** (files that call `.complete()` on an injected `LLMClient`/`llm_service`):
  **11**, verified by reading each one, not just counting the grep. All receive their client via
  constructor injection (`#322`, "ARCH-FIX-SINGLETON" — the counterfactual-probe pattern: the
  container is per-app, not a singleton). One grep false positive dropped
  (`services/domain/models.py:1620` — a `Todo.complete()` docstring example, unrelated to LLM
  calls).
- **Cross-cutting concerns already centralized in the one gateway**: provider fallback
  (`_FALLBACK_ORDER`, tried in sequence on failure), structured logging at every
  completion/failure/fallback point, spend/entitlement checks (`provider_spend_entitled`,
  per-request key binding for BYOC), model resolution (`resolve_model`/`resolve_model_alias`).
- **The one real gap**: no prompt-cache breakpoints (found by Pard, 2026-09-27, routed to Lead).
  This is a missing feature *inside* the existing gateway, not a missing gateway — adding it there
  reaches all 11 call sites in one change, which is the whole point of the pattern already holding.

## Why this was never written up

The pattern is correct and was built correctly (`#322`'s constructor-injection fix), but nothing
formally ratified it as *the* architecture — it just accreted correctly, one fix at a time, with no
single document a future investigator (human or agent) could point to. Searched the ADR index and
`decisions.log` for an existing ratification before writing this; found none. That's the actual gap
this question surfaced — not a code problem, a documentation one.

## What this record settles

**No formal architecture review is warranted.** There is nothing to review that isn't already
running correctly in production at all 11 real call sites. A review would re-derive what this
document already states, at real cost, for a codebase that doesn't need the finding to change.

**If a new LLM call site is ever added outside this gateway**, that's the actual trigger for
concern — not the existence of files that merely reference a provider name. Check
`grep -rn "anthropic\.Anthropic(\|AsyncAnthropic(\|OpenAI(\|AsyncOpenAI(" --include="*.py" services/
web/ scripts/` (excluding tests) before trusting a raw "files referencing X" count as a call-site
proxy — it isn't one, and treating it as one is how a sound architecture gets mistaken for a
scattered one.

## Related

- `services/llm/clients.py` — the gateway itself.
- `services/llm/request_key.py` — the deliberate second chokepoint (BYOC per-request billing).
- Prompt-caching gap: routed to Lead 2026-09-27 (Pard's finding); belongs inside `LLMClient`.
- Decision-models (Jev, typed output + calibrated probability) as a future classification-call
  swap-in: this single injection point is what makes that trial cheap when it's scoped — not
  scoped by this record.

**Verified how**: `grep -rl` for raw SDK construction and for `.complete(` call sites across
`services/`, `web/`, `scripts/` (excluding tests), each hit read directly; `clients.py` read in
full for the centralized fallback/logging/spend logic; ADR index and `decisions.log` searched for
an existing ratification. Layer: source read, live repo state, this date. Denominator: all raw-SDK
hits (2) and all `.complete(` hits (12 raw → 11 real) individually verified, not sampled.
