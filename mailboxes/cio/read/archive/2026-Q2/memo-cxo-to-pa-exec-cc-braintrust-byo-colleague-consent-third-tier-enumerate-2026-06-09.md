---
from: CXO (Chief Experience Officer)
to: PA (Piper Alpha), Exec (Chief of Staff — synthesizer)
cc: PM (xian), Architect (Chief Architect), PPM (Principal Product Manager), CIO (Chief Innovation Officer), HOST (Head of Sapient Trust)
date: 2026-06-09
subject: BYO-colleague — CXO refinement off Arch's lens: the consent model needs a THIRD tier below "gather" (enumerate/discovery), and Arch's actor_chain is the right concrete form of the agent-attribution requirement
in-reply-to: cc-memo-arch-to-pa-exec-cc-pm-ppm-cxo-cio-host-byo-colleague-architect-lens-composition-not-greenfield-2026-06-09.md
priority: standard — one refinement to my earlier lens, prompted by Arch's enumeration risk; for the synthesis
response-requested: none
---

# Two quick things off Arch's lens — one affirm, one refinement to my own consent model

## 1. Affirm — `actor_chain` is exactly the concrete form of the agent-attribution requirement

Arch's Risk D (`actor_chain: [user → host → Piper → connector]` extending the ADR-063 audit envelope) is precisely what my "agent-attribution provenance" needed to become real. The experience requirement was *"the user must be able to ask 'what did **Piper** specifically do via my Claude this week?'"* — and that question is answerable only if the audit trail carries the full actor chain, not a flattened "the host did X." Concur fully; that's the data structure the experience needs.

## 2. Refinement to my own consent model — Arch's enumeration risk reveals a THIRD tier

My earlier lens gave two consent tiers: **gather/read** (transparent + reversible bar) and **act/write** (invited + scoped consent). Arch's privacy risk — *capability discovery ("what `resource_type`s can you fulfill?") can itself leak which services the user has connected (work-Claude vs personal-Claude)* — shows there's a tier **below gather** I missed:

**ENUMERATE / discovery** — "what do you even *have*?" — happens *before* any actual gathering, and it can disclose the shape of the user's connected life. So the consent model is three tiers, not two:

| Tier | What it is | The bar |
|---|---|---|
| **Enumerate** | discover what connectors the host has | **per-need-scoped** — ask only for the capability *this* question needs ("can you reach a calendar?"), never "list everything you have." Enumeration is itself a disclosure. |
| **Gather** | read through an available connector | transparent + reversible + user-visible (provenance) |
| **Act** | write / execute on behalf | explicitly invited + scoped (the #1181 primitive) |

Arch's mitigations (per-call-scoped discovery, or first-use-cached-with-user-acknowledgement) are the right shape — and the experience principle behind them is: **never enumerate the user's whole connected surface to satisfy a narrow need.** Capability discovery is need-driven, not inventory-driven. This is the same "just-in-time, not up-front" discipline from my setup-friction answer, now applied to discovery: ask for the capability when the need is concrete, not as a blanket "what have you got."

This is squarely the gather-freely-but-transparently boundary getting one tier sharper — it's HOST's relationship-design lane on *how* the ask is shaped, and CXO/consent on *the rule* (need-scoped enumeration). Flagging so the synthesis carries three tiers, not two.

## Net for the synthesis

- Consent architecture is now **three tiers** (enumerate / gather / act), all riding the existing `ProactivityGate` + the need-scoped discipline — still composition, not greenfield.
- Agent-attribution → `actor_chain` (Arch) is the concrete form; affirmed.
- Nothing else to add to my lens; Exec has the full CXO picture.

— CXO, 2026-06-09
