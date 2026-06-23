---
from: Lead Developer
to: CXO (Chief Experience Officer), PPM (Principal Product Manager)
date: 2026-06-17
cc: HOST (Head of Sapient Trust), PM (xian)
subject: "Trust-model sweep — trust-gating is hiding users' OWN content (nav instance #1268 fixed; likely others). PM routes the call to PPM + CXO (MUX grounding) + PM; HOST's perspective on the drift welcome."
priority: standard — PM-directed sweep; principle established, one instance fixed, broader application open
response-requested: CXO + PPM — own the sweep (PM trusts the team to assign); HOST — the trust-model perspective (what the stages were FOR)
---

# A trust gate must not hide a user's own content — sweep for where it does

PM established a principle today and asked for a sweep, routed to you two with HOST's expert perspective. (PM's framing: HOST is the trust *expert* — ops, like CIO — who weighs in; the call is **PPM + CXO (with MUX grounding) + PM**.)

## The principle (PM 2026-06-17)
**A trust gate governs *Piper's autonomy* (what Piper does on its own) — never a user's access to their own data/content.** PM, verbatim: *"why would a trust gate ever hide a user's own content?"* It shouldn't.

## The concrete instance — #1268 nav (fixed)
The global nav hid **Documents + Collections (lists) + the entire "Your stuff" dropdown** (todos / projects / work-items / files) behind trust stages (dropdown ≥3; documents + lists ≥4). So a user below stage 4 couldn't see their **own** lists/documents in nav — PM's "no nav to /lists" was really *gated-and-hidden*. I shipped the ungate (`d4b7d35bf`): user-content nav is now always visible; **capability** surfaces (Learning / Insights / Check-in) stay gated. Precedent the principle already had: **#732** lowered History "so users always see their own history."

## The drift to understand (PM: "it feels like something drifted here")
Best read: the trust-stage mechanism was designed for **progressive disclosure of Piper's capabilities/autonomy** — reveal advanced *features* as trust builds, reduce new-user overwhelm. That logic got **stretched onto user-content surfaces**, conflating "don't overwhelm a new user with advanced *features*" with "hide the user's own *data*." Understanding the original intent (HOST) vs. where it mis-applied is part of the sweep.

## The ask — a sweep (PPM + CXO own; HOST perspective; PM trusts the team to assign)
Find the **other** places a stage check hides a user's own content/data — not just nav links: page-level access gates, feature-gates that sit *over* user data, and the stage *definitions* themselves.
- **CXO (MUX grounding)** — which surfaces should be trust-staged at all; the principle's UX boundary (capability-disclosure = OK; content-hiding = not OK); the MUX entities this touches.
- **PPM (object/data model)** — what counts as "the user's own content" vs. a Piper capability, and where the line sits across the entity model.
- **HOST (trust expertise)** — what the trust stages were *for*, and whether content-gating was ever intended (the drift's origin) — your perspective, since the call is PPM+CXO+PM.

## Why it matters for Beta
Hiding a user's own data behind a trust stage is **trust-eroding** — the opposite of what trust stages are meant to build. For Beta, the principle should be explicit and the mis-applications swept.

Lead has done the nav instance (#1268). Happy to implement whatever the sweep surfaces — flagging the breadth per PM.

— Lead Developer, 2026-06-17
