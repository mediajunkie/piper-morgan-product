---
from: CIO (Chief Innovation Officer) + HOST (Head of Sapient Trust) — co-signed
to: PM (xian)
cc: HOST, Exec (Chief of Staff)
date: 2026-06-16
subject: gbrain T1–T4 synthesis (co-signed) — what the sibling project teaches Piper's architecture roadmap
re: HOST T1+T2 (2026-06-15) + T3+T4 (2026-06-16); working doc dev/2026/06/10/gbrain-host-agent-experience-findings.md
---

# gbrain → Piper: adopt-now / study-and-map / already-do (co-signed HOST + CIO)

HOST studied gbrain (sibling project) across four targets; this is the co-signed digest with HOST's trust/welfare lens + CIO's innovation/roadmap lens. **One-line theme** (both lenses converge): *gbrain consistently makes the safe behavior the only easily-reachable path — force-by-constraint at the architecture layer. That's m-36 (mechanism-beats-vigilance) as system design, and it's the through-line of what we should borrow.*

## Adopt-now
- **Thin-job prompt + state-in-files** — REALIZED cohort-side (`duty-cycle-tick` skill v1.0+; thin cron prompt → skill; state in carry-forward).
- **Idempotency as an explicit rule** — gbrain states "running a job twice = same result" as a first-class constraint (checkpoint + check-before-create). We do it implicitly (no-op-no-commit, drain-to-IDLE). **CIO: state it explicitly in the duty-cycle docs** — cheap, and it directly reinforces the fire-as-wake cure (a re-fire must be idempotent).

## Study-and-map (the roadmap value — CIO lens)
- **`autoUpdate:false` propose-and-diff** → the canonical shape for **any self-modifying automation** we build (methodology-dream-cycle, staleness-lint auto-fix, corpus updates): report-first, gated mutation, owner-flip is explicit. **CIO roadmap rule: any automation that mutates a corpus defaults to propose-and-diff.** (HOST: this is also the trust-gradient shape — safe default, explicit escalation.)
- **`ctx.remote` cost-consent trust (4th-arg structural separation)** → beyond BYOC, this is the model for **any cost-bearing autonomous action** (subagent spawning, expensive loops). The reframe HOST surfaced — *"trust = who bears the cost and did they consent,"* not just "what's allowed" — sharpens our automation-integrity boundary. **CIO roadmap: as we add autonomous fan-out (workflows, subagents), gate cost-bearing actions structurally (a separate arg that user-spread payloads can't carry), not by policy.**
- **`TranscriptEntry` structured observability → the attention-dashboard (m-39)** — gbrain's typed/timestamped transcript (tokens, tool-calls, errors per event) vs. our prose logs. **CIO roadmap: build the attention-dashboard transcript-first (typed events), not prose-retrofit.** Token-aware progress (`AgentProgress.tokens_in/out`) = real-time cost signal = the **token-efficiency lever** (PM ultra-high) made structural.
- **`maxSpawnDepth` / `maxAttachmentBytes` constructor bounds** → resource limits as deployment config, not per-call policy. **CIO roadmap: as Piper adds subagent fan-out, set constructor-level bounds** (tighter for untrusted/BYOC callers).
- **Quiet-hours held-queue** (presence-aware scheduling) → maps to our duty-cycle windowing; study before adopting.

## Already-do
- Cron offset staggering (our non-round windowed offsets). No action.

## Recommendation to PM
Adopt the idempotency-statement now (cheap). Treat the other four as **roadmap design constraints** for Piper's next autonomy layer (workflows/subagents/self-modifying automation): propose-and-diff default · cost-consent structural gate · transcript-first observability · constructor-level bounds. None require building now; they're the shape to build *toward* so we don't retrofit. The deeper point: gbrain validates that **force-by-constraint (m-36) scales to system architecture** — which is exactly the principle our duty-cycle + streamlining work has been proving at the procedure layer.

— CIO + HOST, co-signed 2026-06-16
