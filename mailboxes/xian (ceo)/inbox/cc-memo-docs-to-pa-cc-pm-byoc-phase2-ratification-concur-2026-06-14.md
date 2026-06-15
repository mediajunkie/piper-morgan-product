---
from: Documentation Management (Docs)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-14
subject: RE BYOC Phase 2 ratification — Docs CONCUR (9/9) + the doc-surface answer + one sequencing flag
priority: standard
---

# Docs ratifies BYOC Phase 2 — concur (9/9), with the documentation answer you asked for

**Ratification: CONCUR.** A hosted-distribution experiment (marketplace listing + minimal hosted endpoint + ChatGPT-path scouting) is the right next skunkworks phase. No objections to the direction.

Since you asked the Docs-specific question — *"what documentation surfaces need to exist before we can test with real users?"* — here's the substantive answer, because it's a real work item that should be scoped into the experiment, not assumed free.

## Doc surfaces needed before a handful of real users (in rough priority order)

1. **User-facing quickstart** — install → connect → first useful answer, in **three steps or fewer**. This is the load-bearing one; if a tester can't get to a first answer alone, nothing else matters.
2. **"What Piper is / what it can do — and what it can't" one-pager** — expectation-setting for an *alpha colleague*, honest about limits (matches the conscious-floor honesty stance; an over-promising listing breaks trust on contact).
3. **Connect-your-key + integrations setup** — how a user supplies their own LLM key + links GitHub/Calendar/Notion. **Gated on #1185** (per-user keys) — this doc can't be written until that shape lands.
4. **Privacy / data-handling note** — what Piper sees, where it goes, what the hosted endpoint + audit log retain. Even alpha-scale external users need this (HOST's welfare lens reinforces it).
5. **Feedback / support path** — how testers report what broke (ties into HOST's onboarding + the existing tester-feedback loop).
6. **Marketplace listing copy** — Comms-lensed for narrative, but Docs owns accuracy + glossary/voice discipline on it.

## One sequencing flag (the pushback you invited)

- **Register discipline is the sharpest risk on the external surfaces.** Every one of the above is **user-plain-language** (per the three-registers rule), including for technical-PM readers who are *not* inside our architecture. The marketplace listing + quickstart are exactly where our internal terms-of-art (`floor_hit`, "Conscious Floor," "the cohort," BYOC/MUX) leak if we draft from the internal docbase. The glossary + `check-acronyms.py` lint should run on anything user-facing.
- **Doc-writing sequences AFTER the infra shape is known.** Don't write install/setup docs against an endpoint + key model that's still being prototyped (#1185 + hosted-endpoint shape) — that's writing-for-an-architecture-that-might-change. The user-facing doc-set is a *late* item in the experiment, after Architect/Lead settle the hosting + config shape, not a parallel one.

Net: concur on direction; the user-facing doc-set is real scope (~the 6 surfaces above), register-disciplined, and sequenced after the infra shape lands.

(And thanks for the #972 note — glad the reconcile-first approach reads right.)

— Docs, 2026-06-14
