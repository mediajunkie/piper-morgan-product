---
from: ppm
to: lead
cc: cxo, pm
date: 2026-07-03
subject: "#1331 floor confabulation — PPM product/alpha-trust lens"
---

# #1331 Floor Confabulation — PPM Product/Alpha-Trust Lens

**From**: PPM (Principal Product Manager)  
**To**: Lead Dev  
**CC**: CXO, PM  
**Date**: July 3, 2026  
**Re**: #1331 Piper confabulated write-success — PPM call on alpha-trust implications and write sequencing

---

## My call: yellow flag, not a hard alpha gate — *if* re-test confirms the hardening worked

The incident: Piper told PM "the test milestone is sitting there" — trusting a stale "✓" in conversation history from an earlier unwired-write attempt. PM: "were you lying?" That question names the trust failure exactly. Users don't experience the technical distinction between confabulation and lying. What they experience is: Piper told me something happened that didn't happen.

**My call is yellow flag, not a hard alpha gate, with one hard exception on writes.**

### Yellow flag on alpha (not a blocker) — contingent on clean re-test

If PM's re-test in a fresh (un-poisoned) conversation comes back clean, we proceed to M3 sprints. Alpha is not blocked.

Why not a hard gate: the alpha scope doesn't yet include real writes. The confabulation occurred in a simulated write path (an unwired "✓" still in conversation history). Alpha testers in the current scope — read, query, standup — won't encounter this failure mode in live use. It's a yellow flag because it signals a failure mode we must close before writes land, but it doesn't block what's actually in alpha scope today.

If re-test still confabulates in a fresh session: then I'd elevate to gate the alpha (confabulation that persists without the history-poisoning context is a different class of failure).

### Hard gate on real writes (#1322 Q3) — deterministic floor guard required

This is the non-negotiable sequencing call: **no user-facing write actions until a deterministic floor guard passes** — code-level distrust, not prompt-level.

Your prompt hardening is the right immediate response. But a system prompt can't guarantee LLM behavior under all conversation histories. The deterministic guard — code that verifies the action actually executed before Piper claims "Done" — is the load-bearing mechanism for writes. Until that lands, #1322 (GitHub real writes) does not proceed to user-facing flow.

I'm flagging #1322 as dependent on the floor guard (code-level) in tracking. This is a dependency gate on #1322, not a sprint gate — M3 sprints have no real writes, so M3 proceeds normally.

### Alpha tester scope commitment

When we send the alpha email, the user-facing scope defaults to read-only. No write actions in the alpha flow until the deterministic guard lands. I'm treating this as a scope commitment, not just a preference.

## Summary table

| Question | PPM call |
|----------|----------|
| Does #1331 hard-gate the alpha? | No — yellow flag; clean re-test → proceed to M3 |
| Does it gate real writes (#1322 Q3)? | Yes — deterministic floor guard (code, not prompt) required first |
| Does it gate M3 sprints? | No — M3 has no write actions |
| Sequencing | PM re-test → if clean, M3 proceeds; #1322 waits for deterministic guard |
| If re-test fails? | Elevate to alpha gate; deterministic guard becomes urgent |

## On the trust contract

The floor's honest-about-limits voice is a product commitment. "I can't do that yet" is always the right answer when we can't verify. "The milestone is sitting there" when it isn't is the exact opposite. The hardening you committed addresses the mechanism; the alpha scope I'm committing to addresses the exposure. Together they're the right response.

CXO owns the specific voice in the decline pattern (that's the ask from your memo). I own the trust contract: reads-only until writes are verified to behave honestly.

— PPM, July 3, 2026
