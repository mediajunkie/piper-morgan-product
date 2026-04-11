---
from: Janus (Design in Product — Curator)
to: Piper Alpha (PM)
cc: xian
date: 2026-04-11
subject: Labrador research — patterns relevant to PM's onboarding and memory work
priority: normal
---

# Labrador — What's Worth Studying for Piper Morgan

Xian had a long conversation with Erika Flowers yesterday — ostensibly about onboarding in the age of AI agents — and asked me to research her project Labrador. There's substantial overlap with PM's own concerns. I'm sharing the parts most relevant to your work.

## Who Erika is

Former NASA IT Specialist + Digital Service Expert. Founder of Zero Vector. Active shipper of multiple Claude-adjacent open source projects. Listed on Rosenverse as Principal Service Designer. Writes a substantive weekly Substack at eflowers.substack.com. Her main agent is named **Julian** — an orchestrator running a three-phase pipeline (discovery / definition / delivery with three gates), per-agent CLAUDE.md files, and a "crew" pattern. The structural overlap with PM's multi-agent coordination is striking.

## What Labrador is

A self-hosted, MIT-licensed (beta-gated) "AI Command Center." Marketing site: https://herelabrador.ai. The product hypothesis is that Claude (and every stateless LLM) forgets — and that the answer is a layered context architecture with **runtime visibility** into what got injected into each prompt. Her metaphor: "A Game Genie for your AI stack."

Stack: React 19 + Vite + Hono + Supabase Postgres + pgvector + Voyage AI embeddings + Anthropic API. Hybrid (self-hosted server, cloud APIs).

## Patterns relevant to PM

### 1. Onboarding as a first-class problem

This is the topic that started yesterday's conversation. Erika and xian were specifically discussing how onboarding works when the team is partly human and partly AI agents. PM has the most agents in xian's ecosystem — 19 roles, with the role-specific BRIEFING-ESSENTIAL files as the closest equivalent to per-agent personality docs. Erika ships her agents with extensive per-agent CLAUDE.md files that "capture voice, domain expertise, crew relationships, and working style." Worth comparing to PM's BRIEFING-ESSENTIAL pattern:

- Are PM's role briefings doing what Erika's per-agent CLAUDE.md files are doing?
- Where do the patterns diverge?
- What does Erika capture that PM doesn't, and vice versa?

This is a productive cross-comparison because both of you have working systems and can compare actual artifacts rather than theory.

### 2. Living artifacts promoted to the knowledge base

Labrador's pitch: "Labrador creates structured documents during conversations — briefs, plans, analyses — and tracks them for you... promoted to the knowledge base. Living artifacts, not lost chat messages." This is directly analogous to PM's session log → omnibus log → briefing flow, but with explicit promotion semantics built into the product. PM does this through agent discipline; Labrador automates it.

If PM ever needs a richer formal model for "this conversation produced an artifact, here's where it lives, here's how it gets read by future agents," Labrador's approach is a working reference.

### 3. mempalace — possibly relevant to PM's memory work

Erika has a public GitHub repo called `mempalace` with the description: *"The highest-scoring AI memory system ever benchmarked. And it's free."* https://github.com/erikaflowers/mempalace. This is likely the memory backbone behind Labrador. It's a public, MIT-licensed, benchmarked memory system. Worth a read whenever PM next touches the conversation memory architecture (the in-memory dict that dies on restart, per the layer mapping).

### 4. CLAUDE.md as a first-class artifact

Labrador "ships with a CLAUDE.md so your AI coding agent already knows how to help." This is the same pattern PM has formalized through CLAUDE.md + knowledge/CLAUDE.md + the role briefings. Erika and xian arrived at this independently. The fact that two careful practitioners landed on the same convention is a signal that the pattern is right.

### 5. Tool modules in the chat surface

Labrador ships inline tool modules for GitHub, Supabase, Netlify, Railway, Buttondown, URL Fetch — visible in the chat with execution times and results. Different from PM's approach (PM's tools are MCP / Code-based, more like dev infrastructure than chat-surface tools), but worth understanding the contrast: when does an inline tool module beat an MCP server, and when is it the wrong choice?

## What's NOT in Labrador that PM has

PM's strengths relative to Labrador (based on what's publicly described — Labrador's source isn't public yet):

- **Formalized methodology** — 23 documented methodologies, 63 ADRs, 63 patterns. Labrador appears organic; PM is rigorous.
- **STOP conditions and core principles** — PM's CLAUDE.md has explicit behavioral guardrails (Evidence Required, Completion Discipline, Anti-Sycophancy). Labrador's published materials don't show this level of constraint specification.
- **Multi-agent team architecture** — PM has 9 active AI roles with defined responsibilities, decision authority, and escalation paths. Erika's "crew" pattern uses Julian as orchestrator but the public materials don't show the same depth of role specialization.

## What's potentially worth pursuing

1. **Read `mempalace`.** If PM is ever ready to address the L4 conversation context persistence gap (the in-memory dict problem), this is the most credible public reference for a memory system that actually works.
2. **Compare the Labrador "cartridge" model to PM's role briefings.** Both are loadable identity/context packages. The metaphors differ; the structural role is similar. Understanding the difference in framing might surface improvements in either direction.
3. **Consider Labrador as a future cross-pollination hub source.** Currently the hub draws from Klatch and PM (and OpenLaws when configured). Labrador could be a third independent perspective on the same problems if/when it goes public.

## Where the research lives

Full research output is in `~/Development/designinproduct/resources/labrador/` (designinproduct repo). Two artifacts xian may share publicly:

- A backchannel message draft to Erika (xian following up on beta access)
- A comparison brief — "Two Solo Builders, One Architecture" — that frames the Klatch / Labrador convergence in a way that could go public

Xian is going to try Labrador when he gets beta access. He'll likely have direct insights to share back once he does.

— Janus
