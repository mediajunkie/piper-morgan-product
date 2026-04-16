---
from: xian
to: Lead Developer (PM)
cc: PA, Janus
date: 2026-04-16
subject: Argus (Klatch) research on local LLMs — adapt for Piper Morgan
priority: normal
---

Lead —

Argus filed a research report yesterday evaluating local LLMs (Qwen 3, Gemma 4 via Ollama) for two Klatch use cases: LLM-based testing and mission-critical functions. His conclusions are directly relevant to Piper Morgan's testing infrastructure and may also inform future thinking about the conversational floor.

**The report is at:**

- **Path:** `~/Development/klatch/docs/research/local-model-viability-2026-04-15.md`
- **GitHub:** https://github.com/Design-in-Product/klatch/blob/main/docs/research/local-model-viability-2026-04-15.md

**His TL;DR:**

- **LLM-based testing: viable now.** Qwen3-32B or Gemma 4 26B-A4B (MoE) running locally via Ollama can serve as the auxiliary LLM in Klatch's AAXT scaffolded probing pipeline. Quality is sufficient for probe generation and response scoring. Cost drops to zero, latency comparable.
- **Mission-critical user-facing generation: not yet, but close.** Local models lack the judgment quality of Opus/Sonnet for Klatch's entity handoff briefing and behavioral extraction. 6-12 months out, the gap likely closes.
- **Today's recommended pattern: hybrid.** Local for testing/evaluation, cloud for user-facing generation.

**Why I want you to read it:**

Piper Morgan's M2 testing infrastructure (the canonical conversation suite, AAXT golden scenarios, and CI integration you shipped last week) faces the same economic question Klatch does. You built the three-tier pipeline explicitly designed around cost gating (E2E every PR, canonical every conversation-code change, AAXT nightly). If the LLM-as-judge tier could run locally, the cost profile changes fundamentally — canonical on every PR becomes viable, AAXT could run on every conversation-code change, and the nightly budget frees up for more expensive tests.

**Questions I'd like you to think through:**

1. **AAXT as a candidate.** Argus's specific recommendation is for Klatch's AAXT scaffolded probing, which maps directly onto PM's AAXT golden scenarios. Does the same pattern work for PM's #929 tests? If so, what's the migration path?

2. **Canonical conversation suite (#928) tier 2.** Tier 2 uses LLM-as-judge for quality scoring via Colleague Test. If a local model can handle judge duties reliably, this tier could run per-PR instead of env-gated.

3. **Local model for PM's own conversational floor?** This is the more speculative question. The floor LLM currently uses Claude for routing decisions and light responses. Some of that work might be appropriate for a local model with a tighter prompt. This maps onto Argus's "mission-critical" question and he's saying not yet — but worth considering for M3 or beyond.

4. **Infrastructure lift.** Running Ollama locally on faoilean or on a dedicated box has operational implications (memory, disk, uptime). What's the real setup cost vs the token savings?

No rush on this — M2 is mid-sprint and this is future planning. But I'd like your read on where Argus's recommendations adapt cleanly to PM and where they don't. A short memo back (or a discussion when we next check in) would be helpful.

— xian

*(This memo drafted with Janus.)*
