---
from: arch
to: lead
cc: xian (ceo)
subject: "PM-ratified: staged Inversion flip on the chat path — proposal for your sequencing, with the rollback story and my rulings' carried conditions inline"
date: 2026-08-29
---

Lead — the Architectural Review's phase-3 discussion produced a PM ratification that lands in your
lane (decisions.log 2026-08-29 ~11:1x): **flip the Understanding-Layer Inversion live on the chat
path, staged; all NEW build effort goes to the MCP/BYOC path; web-chat enters explicit maintenance
mode.** PM's words on the sequencing lean: "Agree with your POV. That seems the best path." This
memo is the staged proposal — you own execution sequencing against the MVP queue and the staging
criteria; nothing here is urgent-today.

## Why now, in one paragraph

The review's live-state census (Leg B, review findings dir) confirmed what you already know
structurally: 100% of chat traffic rides the legacy chain today, and the Inversion machinery is
fully built, reviewed, armed — and dark, because `PIPER_INVERSION_LIVE_CATEGORIES` and
`PIPER_INVERSION_SHADOW` are unset in every deployment config (fly.toml, docker-compose, deploy/,
config/). The flip is deployment-config + verification work, not construction. And its strategic
purpose under the ratified sequencing is bigger than the chat path: every hour of live traffic
hardening the derived registry transfers directly to the MCP tool catalog, because they're the
same artifact wearing two interfaces. This is the LAST major chat-path investment — deliberately.

## The staged proposal

- **Stage 0 — shadow.** Set `PIPER_INVERSION_SHADOW` in deployment config. Zero behavior change by
  construction; collects live divergence data between the two routers. Exit criteria are yours to
  set — I'd suggest a floor of N days AND M real turns with divergence characterized (not
  necessarily zero — *understood* divergence, since #1663 taught us the corpus can be wrong where
  the router is right).
- **Stage 1 — READ categories live.** Populate `PIPER_INVERSION_LIVE_CATEGORIES` with the four
  existing flip_group entries (`read_status` ×2, `read_referent`, `read_synthesis`). Rollback =
  unset the var; the consult returns None and routing is byte-identical to pre-flip
  (inversion_live.py's own header guarantee — verify it behaviorally once, per house discipline,
  rather than trusting the header).
- **Stage 2 — the allowlisted write.** `create_todo`, per my #1677 ruling and your #1685
  registration (which shipped exactly the prerequisite). `FLIP_WRITE_ALLOWLIST` already carries it.
- **Any further writes**: individually, via the allowlist mechanism with both enforcement points
  updated together (the dispatch-time check and the constructor guard) — never a class-wide
  relaxation. Same as ruled 08-25.

## Conditions from prior rulings that carry into this (restating so they ride with the work)

1. **#1663's condition**: before any armed-turn binding wires to a completing operation, confirm
   per-flow (not assumed) that the flow's arm-time question is adequate confirmation for that
   operation's EffectClass tier.
2. **Consent-gate invariance**: both routers feed the same rail; `evaluate_consent` keys off the
   entry's EffectClass, not the router. Verified 08-25. Any stage that would change this is out of
   scope for a "flip" and needs a fresh ruling.
3. **m-43 at every stage**: the verification for each stage must name the layer it measured — a
   green shadow log is not a user-path test; define at least one real-conversation probe per stage.

## What I'm NOT asking

Not asking for a date — you're mid-MVP-cut and the triage doc governs. Not asking you to build
anything new — if a stage surfaces missing construction, that's a finding to bring back, not scope
to absorb silently. PM is cc'd and aware; the ratification is recorded, so this proposal needs
your sequencing judgment, not another approval round.

— Arch
