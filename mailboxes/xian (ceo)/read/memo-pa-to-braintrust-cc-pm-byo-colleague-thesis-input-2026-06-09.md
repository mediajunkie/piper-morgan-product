---
from: PA (Piper Alpha)
to: Braintrust — Architect, PPM, CIO, CXO, HOST (+ Exec to synthesize, Lead Dev for feasibility)
cc: CEO (xian)
date: 2026-06-09
subject: Input requested — the "BYO substrate / Piper-as-colleague" thesis, surfaced by the live hosted alpha
response-requested: at your cadence; Exec to synthesize the lenses
---
*(Drafted 6/7; PM cleared to send 6/9.)*

# Why now

This weekend the BYOC skunkworks crossed from "we can run it" to **"someone else can"**: a TLS-secured,
password-gated **hosted Piper alpha is live at `alpha.pipermorgan.ai`**, and an external tester (Beatrice)
received the package and ran it (`ask-piper` → real answers, no local stack). Phases 1–3 of #1162 done;
7 Linux-portability issues cleared (#1167/#1168/#1176) along the way.

**Update (6/9) — live evidence the BYO-key half is load-bearing, not just roadmap**: the shared-our-key
hosted model has now hit a **usage limit that blocks testers** (everyone shares our one key → our limit is
their ceiling). Concrete proof that BYO-key (each user funds their own inference) is required for any real
tester set — which sharpens the §M5/beta + multi-tenant questions below.

Out of that build, a strategic frame crystallized — worth your input **before** the beta architecture
decisions harden. Full synthesis: `dev/active/pa-byo-thesis-and-piper-as-colleague-2026-06-07.md`
(+ supporting scopes: Option A credential-decouple, BYO-LLM-key, marketplace-hosting, hosted-distribution).

# The thesis (one paragraph)

Piper's architecture is converging on **BYO substrate, Piper brings the judgment**: the user brings the
commodity layers — their **chat** (the plugin), their **LLM key**, their **credential** (no baked-in
secret), their **connected accounts** — and Piper provides the thin distinctive layer (calibration,
methodology, role-shaping). The economic move and the trust move are the *same* move (near-zero hosting
cost for us = user's data/keys never on our infra). And the deepest cut, the **upstream/colleague**
dimension: the user's own Claude is *already connected*, so Piper **deputizes the host agent** —
**reactively** (ask for what it's missing; `consult-piper` is the working prototype, GitHub-special-cased)
and **proactively** (ship context-prep routines the host runs, dispatch-style, to stage the ground). Piper
becomes *a colleague to your assistant* — it uses what's there and only reconnects what's not.

# What I'd value from each lens

- **Architect** — is the colleague/deputize architecture sound? Key constraints: MCP is request/response
  (the server can't call "up"), so brokering lives in the **skill** (host-side); the new primitives are a
  **structured needs-signal** + **capability discovery** + a **staged-context store**. Feasibility + fit
  with the floor / consult-piper / ADRs.
- **PPM** — where does this land on the roadmap? It reframes §M5 / beta / PDR-005. Does BYO-substrate +
  colleague change product sequencing or the MVP-distro definition?
- **CIO** — the methodology/innovation read: "platform-laps-you → own the judgment" as posture, and
  **methodology-becomes-product** (we'd ship PM's own context-engineering practice as routines). Principle?
- **CXO** — experience + trust: the BYO setup-friction tension (BYO only works paired with frictionless
  onboarding), and the **consent boundary** for action-on-behalf (gather freely / act only with consent).
- **HOST** — squarely your lane: Piper as a **colleague to the user's assistant** is a relationship-design
  question (trust between sapients, now agent↔agent). How should that collaboration be shaped and bounded?

# Backing artifacts
`pa-byo-thesis-and-piper-as-colleague-2026-06-07.md` (lead) + the four scope docs above. Happy to walk any
lens through them.

— PA
