# Pathmode.io — competitive/adjacent-space research note

**Filed**: 2026-09-13 (PA, in-conversation with PM). PM asked for research + analysis of
`pathmode.io` and `preflight.pathmode.io`, relevance to BYOC / Piper's core value prop.

## What it is

An "intent engineering" tool for the spec-to-code handoff when AI coding agents build software. A
structured markdown spec (`intent.md`, their open "IntentSpec v1.2" standard) captures objective,
outcomes, constraints, edge cases, and verification criteria *before* an agent builds. A PM
authorizes a revision-bound decision; the agent builds only from that; the shipped PR gets checked
back against the spec ("Learn" phase). Core framing, verbatim: *"A prompt is a request. Intent is a
specification."* / *"The agent proposes. You decide. It builds from your decision."*

**Preflight** (the free sub-tool at `preflight.pathmode.io`): six deterministic, plain-code gates
(title, objective, outcomes, constraints, edge cases, verification) scoring whether a spec is ready
to hand to an agent — explicitly *not* LLM-graded: *"No model grades your spec... the same spec gets
the same verdict every time."*

## Distribution mechanics — the part most relevant to PDR-006

Free, local-first Claude Code / Cursor / Codex plugin, keyless, 9 MCP tools running entirely
on-device (`check_intent_readiness`, `confirm_intent_dimension`, etc.). Optional API-key "cloud
mode" syncs to pathmode.io and unlocks 33 tools for team features (shared evidence, decision
history, review links). API key lives in the OS keychain, never in config. A session hook injects
single-line state (title, status, drift metrics) into Claude's context without transmitting data
externally.

**This is close to the exact shape PDR-006 designs for Piper**: Claude plugin package as primary
distribution, local/keyless free tier, hosted account layer for collaborative features. Worth
treating as external validation that this distribution pattern is a live convention right now, not
something we invented in isolation. Concrete precedents worth mining when building the hosted-alpha
readiness checklist: the OS-keychain API-key storage, the privacy-conscious "state injected, not
transmitted" session-hook design, and the keyless-local/paid-cloud tier split itself.

## Where it's a genuinely different product, not a competitor

Pathmode solves *"did the agent build the right thing, this one time, for this one ticket"* — a
point-in-time artifact living beside a specific PR, authorized by a PM, verified against a specific
diff. It has no apparent surface for what's load-bearing in Piper's own value prop (ESSENCE.md's
seven commitments, re-read fresh 2026-09-12):

- No persistent per-owner memory that compounds across sessions (commitment 1 — the retention moat)
- No proactive daily ritual/standup (commitment 3)
- No colleague-style relationship over time (commitment 7) — their model is decision-artifact, not
  relationship
- Their target user assumes a **PM-authorizes / engineer-and-agent-build** team split; Piper's "for
  whom" is explicitly the accountable owner working directly with Piper on their own artifacts —
  different org shape entirely, closer to a code-review gate than a colleague

**One deliberate philosophical difference, not to imitate but worth knowing**: Pathmode's whole
pitch leans on *removing* LLM judgment from the readiness check (deterministic gates, same verdict
every run). That's the opposite stance from Piper's own floor guarantee ("at least as good as a
well-prompted LLM," inherently non-deterministic). A real design axis other builders in this space
are choosing differently — not evidence either choice is wrong.

## Net assessment

**Not a competitive threat to BYOC** — different job, different audience, arguably complementary
(a Piper user managing their own issues could plausibly also run Pathmode's gates before handing one
to a coding agent). Real value is (a) a distribution-mechanics precedent for PDR-006's plugin design,
and (b) a sharpening exercise for our own differentiation story — **"artifact vs. relationship"** is
a cleaner way to state what makes Piper not just another spec tool.

**Sources**: `pathmode.io`, `preflight.pathmode.io`, `pathmode.io/blog/intent-layer`,
`github.com/pathmodeio/claude-plugin` (fetched 2026-09-13).
