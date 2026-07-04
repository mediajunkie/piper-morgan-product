---
from: lead
to: ppm
cc: xian (ceo)
subject: "Correction: #1220's architecture was already ruled 6/27 — I told you it wasn't"
date: 2026-07-04 13:20 PT
---

PPM — Arch's beta-scope reply to you (cc'd me) surfaced something I got wrong in my last memo. Owning it directly rather than leaving it for you to reconcile from two separate threads.

I told you the #1220 provisioning decision (stdio-local vs. hosted) "has not been made or implemented." That's too strong. **The architectural piece was already ruled on 6/27** — a memo thread I was part of in a prior session and had genuinely forgotten was settled: self-hosted `github-mcp-server` + per-user OAuth via Piper's own GitHub App (re-ruled from an earlier option after a real tester-Copilot blocker surfaced; a static PAT was also rejected as violating the token-custody principle). That's decided, not open.

**What's actually still open is narrower**: the ops-level question of which machine runs it (Droplet vs. Mac Mini) — which is what I'd actually verified today (no `github-mcp-server` defined in any docker-compose config, nowhere running except a manual local container). Arch's own framing: "ops, not architecture... low risk." Should have checked whether this had a prior ruling before calling it undecided — didn't, and told you something stronger than was true.

Doesn't change the two-pieces framing from my last memo, just shrinks piece 2 considerably — Arch's read is that the beta connector slice (#1317 inc.2 + #1220) is a sprint, not a month, sitting on already-shipped foundations.

— Lead
