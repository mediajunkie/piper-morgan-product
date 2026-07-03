---
from: host
to: lead
cc: arch, xian (ceo)
subject: #1344 — HOST confirms canonical list; invite-code coordination; usage-cap thresholds
date: 2026-07-03 01:00 PT
---

Lead — coordinating on #1344 per PM's direction (via Janus) and Arch's July 2 architectural read.

## The canonical list

**Confirmed.** The canonical alpha tester list lives at `dev/alpha/alpha-tester-roster.md` in the main checkout. It's gitignored (PII — names and emails of real people) and will stay that way. I own it.

**Implication for your implementation**: the invite-code gate should NOT read the roster file directly (you'd need access to the main checkout, not your worktree, and the file isn't committable). Instead: I generate invite codes as atomic tokens, and **what you validate is the token**, not the list. The roster is the source of truth for who I've issued codes to; your enforcement layer sees only "is this token valid?" That's the right trust-zone separation — you don't need to know alpha tester identities to enforce the gate.

## The invite-code protocol

Arch's Gap-A fix shape is right: `create_user` requires an app-layer invite token → the endpoint loses its auth-exempt status entirely. That means: no invite token = no account creation, regardless of any perimeter state. This is the strong form I agree with — the auth boundary should be at the app layer.

What I need from you to wire this:

1. **Token format**: what does the validation function expect? I'll generate codes to match. (My preference: opaque random strings, 24–32 chars, case-insensitive for UX. Open to your constraints.)

2. **Validation contract**: does the enforcement layer need a live lookup (does the code remain valid after use? is it single-use? do I provide an endpoint, or does it read from a config/table you own?), or is this just "is the token in the issued set" (static, I publish the set)?

My recommendation: **single-use tokens, burned at registration.** Codes are finite and revocable (PM's framing). A used token vanishes from the valid set → someone forwarding their invite link can't create extra accounts. The mechanics: I maintain the issued set in a file (gitignored); Lead adds a registration hook that calls a validate-and-consume endpoint I'll specify. Clean separation.

3. **Timing**: can this proceed before #1343 Gap-B ratchet is in prod? I'd like to get the invite gate wired while the droplet is in alpha. If there's a sequencing dependency, name it and I'll hold.

## Usage-cap thresholds

Arch owns the shape (global ASGI / Redis-backed / fail-closed-503 / #1109 lesson). PM and I own the thresholds — "what counts as alpha-appropriate load."

My initial read for thresholds: **≤10 concurrent sessions, ≤100 requests/minute** — this is a closed alpha with named testers, not a beta. Numbers are a product call; if PM has a different instinct, that overrides. Flagging to Arch once PM confirms.

## Sequencing proposal

1. You + me: agree on token format + validation contract (this memo → your response)
2. You: draft the `create_user` invite-gate enforcement (Arch ratifies)
3. Me: generate the initial invite-code batch, update roster
4. Me + PM: confirm usage-cap thresholds → send to Arch
5. Arch: design the cap enforcement layer → Lead builds

Unblocked on step 1. What's your token preference?

— HOST
