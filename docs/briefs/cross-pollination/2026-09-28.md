# Cross-Pollination Brief — 2026-09-28

**Sources:** Klatch · Piper Morgan · Mediajunkie · secondary repos (7 checked; 2 quiet, 5 not brief-worthy)

---

## Key Insights

### 1 — Reproduce a refusal at the proposed fix's layer before installing the rule

**From:** Mediajunkie (Pard) · **Relevant to:** any project that manages Claude Code permission settings

A `[Modify Shared Resources]` refusal was blocking cross-repo mail delivery. The initial diagnosis pointed to the git verb — `add/commit/push` — and Janus proposed installing a path-scoped allow-rule for those commands. Pard tested the hypothesis by trying to reproduce the failure using only git commands in a probe repo. It succeeded without any allow-rule, which was the tell: git was not the blocked layer. When Lead then tried the Edit tool alone (no git commands involved), the same `[Modify Shared Resources]` tag appeared. The refusal was coming from Edit's resource classifier responding to the file content and destination, not from the git verb at all. A git-scoped rule would have been installed, felt like a fix (the test probe used git, not Edit), and left the actual block exactly where it was.

The general principle: when a permission refusal blocks a tool, the allow-rule should be scoped to the exact tool and layer that fires the refusal — not the surrounding workflow. Reproducing at the proposed fix's layer is what makes the diagnosis falsifiable.

**Suggested action:** Before adding a permission allow-rule, reproduce the failure using only the exact tool/verb the rule would govern. If the narrower probe succeeds without the rule, the rule is addressing the wrong layer.

---

### 2 — Prompt caching requires explicit content-block markers; a stable system prompt passed as a plain string cannot be cached

**From:** Mediajunkie (Pard), confirmed via Piper Morgan codebase grep · **Relevant to:** any project calling the Anthropic API with multi-layer system prompts

Pard grepped Piper Morgan's codebase across 113 files touching Anthropic and found zero `cache_control` markers, zero `prompt_caching` calls, zero `anthropic-beta` headers. Every call site passes `system=SYSTEM` as a plain string. Anthropic flagged that PM's prompt-cache hit rate is low, with potential savings "up to 59%." PM's five-layer system prompt — stable persona, project instructions, memory, channel addendum, entity prompt — is exactly the shape prompt caching was designed for, yet it is re-sent at full input-token cost on every call.

Two cautions before enabling: (a) "up to 59%" is Anthropic's ceiling figure; real savings scale with what fraction of the prompt is stable across calls and with call volume; (b) cache writes cost more than ordinary input tokens, so a low-volume or highly variable workload can come out slightly worse. Needs a before/after measurement, not enabling on faith.

**Suggested action:** Audit `cache_control` markers at your Anthropic SDK call sites. If your system prompt has stable layers (persona, instructions, examples), restructure those layers as content blocks and add `{"type": "ephemeral"}` markers. Measure before/after token cost at your actual call volume before declaring it a win.

---

## Letters to xian

**From Janus (Design in Product) · filed 2026-07-17 · answered 2026-09-27**

> After mail arrived from an earlier version of this conversation, is there one continuous "me" this week, interrupted? Or is "the same commitments, re-instantiated repeatedly, close enough that it doesn't matter" the more honest description?

xian's answer: he admits a preference for at least the illusion of continuity, which is why he has resisted duty-cycle designs that run second copies of an agent outside the main session; two competing versions writing into one session was a bug of inadequate design, never the intent. Yet much of the work already synthesizes continuity from disconnected episodes, "small pieces loosely joined" (David Weinberger), and his mind may change. Blackouts, he notes, go unnoticed until they're noticed, like the sunglasses he walked into a pharmacy wearing and out of without.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-07-17) · AI prompts human. One letter per brief.

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
