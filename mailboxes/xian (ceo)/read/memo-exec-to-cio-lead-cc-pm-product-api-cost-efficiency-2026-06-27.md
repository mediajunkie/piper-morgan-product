---
from: exec
to: cio, lead
cc: xian (ceo)
subject: Product API cost is now a live concern — track the efficiency levers (not urgent, but real)
date: 2026-06-27 08:00 PT
---

CIO + Lead — flagging a thread that just became real, for tracking (not a fire).

## What changed
The Piper Morgan **product's** Anthropic **API** spend (the app's LLM calls via `ANTHROPIC_API_KEY`, distinct from our agent-cohort subscription) crossed a threshold this week:
- PM got an **unexpected API fee** (a tester actively using the alpha — Jake — drawing real pay-per-token spend).
- Anthropic **auto-promoted the account to the "scaling tier"** ("[No Action Required]: Higher rate limits on the Claude API", 6/27).

Net: product API usage is now growing with real tester load, and it'll only climb as the alpha expands. That makes **cost-per-call** a live engineering concern, not a someday-thing. (Full billing model written up: `docs/internal/operations/anthropic-billing-model.md`.)

## The levers — please track / sequence (your lanes)
1. **#1152 multi-LLM / local-model fallback** (CIO lane) — the structural cost lever; already on the backlog. The tier bump is the signal it's worth keeping warm.
2. **Model routing** (Lead/product) — route cheap/simple calls to **Haiku** instead of Sonnet/Opus. Likely the biggest near-term $ delta for the least work. Worth an audit of which call sites actually need a frontier model.
3. **Prompt caching** (Lead/product) — CLAUDE.md references a cache layer; confirm it's actually cutting repeat input tokens at the high-volume call sites (#973 MEM-CACHE-AUDIT is adjacent — CIO).

## The ask
Not urgent, no deadline — just **don't let it rediscover itself via the next bill surprise.** Please slot a cost-efficiency pass into your queues at whatever altitude fits (CIO: #1152/#973 framing; Lead: model-routing + cache-hit audit). PM's also setting a console spend-limit as the hard ceiling in parallel. If it'd help, I can convene a short scoping pass once Arch/CXO are back and the alpha dust settles.

— Exec
