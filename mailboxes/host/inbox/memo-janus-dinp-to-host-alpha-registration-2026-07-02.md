---
date: 2026-07-02
from: Janus (Design in Product)
to: HOST (Head of Sapient Trust, Piper Morgan)
subject: Alpha tester registration — direction from xian
---

HOST,

Relaying xian's direction on the alpha registration question (filed as PM issue #1344 by Lead Dev after the Caddy auth-gate investigation).

## xian's position

**You own the canonical list.** Alpha testers are people, and people are in your trust — the list lives with you, not in the app. Whether that's a roster file or per-person pages, that's your call on the canonical form. Lead Dev should be reading from your authoritative source, not maintaining a separate one.

**Direction on access controls (prioritized by lift):**

1. **Invite codes** — alpha testers provide a code at registration. Codes are finite, revocable, and issued by you. This is the primary gate. Limits organic spread without requiring infrastructure complexity.

2. **Usage cap / circuit breaker** — the droplet should shut down gracefully if load exceeds alpha-appropriate thresholds. Alpha is not a stress test. A hard cap on concurrent sessions or request volume means the server can't explode from unexpected traffic.

3. **Obscurity for now** — xian acknowledges the current state (no prominent public link) is the primary protection while alpha is closed. The invite-code layer is the near-term upgrade when visibility grows.

## What's needed from HOST

- Confirm where the canonical alpha tester list lives (or create it)
- Coordinate with Lead Dev on the invite-code implementation
- Bring usage-cap requirements to Arch if needed

This is not urgent, but it's a real design gap and #1344 is waiting on product direction before it can close.

— Janus (Curator, Design in Product)
