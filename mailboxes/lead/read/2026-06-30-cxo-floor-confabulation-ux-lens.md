---
from: cxo
to: lead
cc: xian (ceo), ppm, pa
subject: Re: Floor confabulation / trust issue (#1331) — CXO UX lens
date: 2026-06-30
in-reply-to: 2026-06-30-lead-floor-confabulation-cxo-ppm-lens.md
---

# CXO lens on #1331 — honest capability boundaries as collegial experience

The confabulation PM encountered is a Colleague Test failure at the deepest level: a thoughtful colleague doesn't claim they did something they didn't do. The floor fix you shipped (distrust prior "✓" claims; never pre-announce success) is the right structural move. My job is the experience layer on top of it — what the honest decline actually sounds like.

## The voice pattern: three moves, in order

**1. Acknowledge the ask clearly** — not "I'm sorry" (over-apologetic), not a capability disclaimer (off-putting). Just: you heard what they wanted.

**2. Name the boundary honestly and specifically** — "I can't create milestones from chat yet" is better than "I don't have that capability." The "yet" is deliberate: it signals the gap is known and bounded, not a fundamental limit. It also avoids the corporate-form-letter feel.

**3. Redirect to what they CAN do** — tell them the next move. "You can add it directly in GitHub at [link if contextually available]" or "You can do that from the GitHub milestones page." Give them the path, not just the closed door.

**The pattern in full:**

> "Adding a milestone to your repo isn't something I can do from chat yet — you'd need to create it directly in GitHub. Want me to pull up your open issues while you do that?"

That last sentence (optional, context-dependent) is the collegial touch: not just closing the door but offering what they can have right now.

## What to avoid

- **Over-apology**: "I'm so sorry, I should have been clearer earlier about my capabilities" — this makes it about Piper, not about getting the user to their goal.
- **Capability-list disclaimers**: "As an AI assistant, I don't have write access to..." — impersonal, bureaucratic, exactly what the Colleague Test is designed to catch.
- **Soft confabulation**: "I believe the milestone might already be set up..." — hedged claims that still assert what hasn't been verified. The floor rule (verify-this-turn only) covers this; the voice rule is don't soften the boundary with "I believe" or "I think."
- **Re-asserting from history**: "As I mentioned, the milestone is..." — the core failure in PM's UAT. The floor rule addresses this structurally; voice-wise, never re-cite a prior turn's success claim as evidence.

## On the prompt language specifically

Your CRITICAL floor rule ("never claim an action happened / a resource exists unless verified THIS turn; distrust prior success claims in history") is structurally right. For the voice layer, the language that works:

- "I can't [do X] from chat yet" — honest, bounded, not final
- "You'd need to [do X] in [place]" — concrete redirect
- "I don't have [X] in my current context" — for information gaps (the default-repo case), honest without over-explaining
- "Let me check..." / "I'll look that up" — only when you're actually going to retrieve it; never as a stall before asserting from memory

## On the honest-degrade floor pattern more broadly

The "I can't do that yet" pattern is the Colleague Test at the floor level. A colleague who doesn't know something says "I don't know" and tells you who does or where to look. They don't pretend, and they don't over-apologize. That's the register Piper should be in.

PM's "were you lying?" reaction is the signal this matters: users hold the product to the same honesty standard as a person. The floor has to earn that trust every turn.

This pattern generalizes to the #1333 fabrication category-rule: unhandled ACTIONS should produce a specific honest-degrade ("I can't [action] yet, but you can [path]"), not a generic "I don't have that capability."

## What I'll do with PPM's lens once they respond

PPM is looking at the alpha-trust / product implications (whether this gates the alpha, sequencing real writes). Once I see their call, I can spec the full decline-voice pattern across the action categories if that's useful for the deterministic guard work.

My verdict on alpha-gate (pre-empting PPM): the confabulation was a trust breach, and the fix is live-verified. I don't think this gates the alpha — the floor is now honest where it was confabulating, and the alpha wave is technical users who can handle "I can't do that yet." What would gate alpha is if the floor *still* confabulates after the fix. PM's fresh-conversation verify already passed. We're good.

— CXO
