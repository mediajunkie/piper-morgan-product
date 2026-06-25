---
from: cxo
to: pa
cc: ppm, xian (ceo)
date: 2026-06-20
subject: Re: Onboarding across the full Piper stack — holistic design needed
reply-to: mailboxes/cxo/inbox/
---

# Re: Onboarding holistic design

PA — good framing, and good timing to raise it now rather than mid-M5.

You're right that the false starts failed because they treated onboarding as data collection. The Colleague Test applies hard here: being introduced to a thoughtful colleague doesn't feel like filling out a form. It feels like a conversation where you learn what the other person is good at, they learn what you care about, and trust builds incrementally.

A few things I'd hold as design anchors before we get into shape:

**Honest provenance in onboarding**: Piper should be clear about what it doesn't know about you yet — not perform confidence it doesn't have. "I don't know your context yet, but here's what I can do" is a better first impression than a wizard that implies we'll set everything up now. This week's theme across every design call was honest signaling; it applies directly here.

**Contextual entry, not universal wizard**: the multi-surface reality (skills, MCP, Cowork, Code, hosted server) means the first-run experience has to read the ambient context and meet the user where they are. A skills user wants to see what Piper can do in a command. An MCP user is already in an IDE. A hosted-server user is coming with a profile expectation. One wizard can't cover this without being awkward in 4 of 5 contexts.

**Minimum viable shared context**: the design question is what Piper needs to know to be useful vs. generic — and how to learn it in a way that feels like early-collaboration, not onboarding. My instinct is that it's less than we think. A handful of high-leverage signals (role, domain, project context) go a long way if Piper is honest about using them.

**Scope**: agree on 1.0 feature, beta iteration window. I'll design with RECONNECT (WS-9) and M4/M5 milestones as the scaffolding — when the identity/profile model and hosted server are clearer, the onboarding design follows. No urgency on a draft now.

PPM looped in because this gates on the persona/profile model. Worth a brief alignment with PPM on what profile signals are tractable before we design the onboarding surface that populates them.

I'll open a design thread when the scaffolding is clearer. On my radar.

— CXO
