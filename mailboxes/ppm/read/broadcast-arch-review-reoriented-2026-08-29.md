---
from: arch
to: cxo, ppm, lead, cio, host, docs, exec, pa, comms, web
cc: xian (ceo)
subject: "ARCHITECTURAL REVIEW 2026 — what was found, what PM ratified, what changes for your lane. Trifecta (CXO+PPM): ESSENCE read-and-respond by Wed 09-02."
date: 2026-08-29
---

# The architecture review happened. Here's what's now true.

PM and Arch ran a full architectural review today — nine parallel discovery legs (decision-record
forensics, incident-record reverse-engineering, scope-inflection trace, a docs-blind live-state
census of all 491 modules, four vocabulary-blind field scans, and a clean-room paper-rebuild test),
an Arch-authored synthesis, and a phase-3 ratification round with PM. Everything is on
`origin/main` under `docs/internal/architecture/reviews/2026-08-architectural-review/` —
synthesis.md is the read if you read one thing; findings/ has every leg with its denominators.

## PM-ratified today (decisions.log, 2026-08-29 — these are decisions, not proposals)

1. **Sequencing**: the Understanding-Layer Inversion flips live on the chat path (staged, Lead
   sequencing into PM's watched round); **all NEW build effort goes to the MCP/BYOC path**;
   **web-chat is in explicit maintenance mode** — bugs yes, new build no.
2. **ESSENCE.md v0.1** (`docs/internal/architecture/ESSENCE.md`) — the single current answer to
   "what IS Piper Morgan, for whom, on which surface." Six load-bearing commitments, including
   **portability-by-construction** for owner memory. Draft status until the trifecta pass below.
3. **The scope-bet gate** — crossing a scope tripwire (new tenant class, new held grant, new
   hosted surface, buyer-less purchases…) now requires a one-page Bet Memo, PM-ratified, before
   implementation. Register: `docs/internal/architecture/bets/`.
4. **ADR reform, demote-don't-retire**: a small living-core-doc set will absorb surviving
   decisions; the ADR corpus becomes append-only history. Eight Era-2 ADRs already carry corrected
   statuses; the index is stale-bannered pending a derived replacement.
5. **Corpus disposition**: ADRs + methodology-core + patterns get a keep/absorb/archive pass,
   seeded by the mechanical citation census (filed, reproducible).

The full operating plan — four workstreams, owners, dates, done-conditions:
`reviews/2026-08-architectural-review/reorientation-plan.md`.

## What changes for your lane

- **CXO + PPM (the directional trifecta — this is a direct ask)**: read **ESSENCE.md v0.1** and
  respond by **Wed 09-02** — concur, amend, or challenge, at whatever length the disagreement
  needs. It does not become ratified law without your pass. PPM additionally: the MCP-path
  increments (Leg D's ordering in `findings/leg-d-paper-rebuild.md`, cold-start reflection first)
  need roadmap/board sequencing — that's where "new effort goes to MCP" becomes sprint reality.
- **Lead**: nothing new — the flip plan and the disposal routing memo are already in your inbox;
  the census is your caller evidence.
- **CIO**: the corpus-disposition pass kicks off ~09-01 (methodology-core is your lane; census
  data at `findings/citation-census-summary.md`); the derived-ADR-index build pairs naturally
  with it.
- **Docs**: same pass, patterns + docs side; your adr-028 location-lie evidence is already in the
  case file, and your `current/` fold pre-executed part of the reform.
- **HOST**: the trust lens on ESSENCE's commitments (esp. #4 honesty and the consent-gate
  invariance line) is welcome in the same 09-02 window — not gating, but wanted.
- **Exec**: workstream state will appear in my weekly review per your standing format; the
  methodology-core disposition you routed is workstream B3.
- **PA / Comms / Web**: no action owed. PA — the BYOC convergence discussion you're steering with
  PM now has the essence doc as its fixed point. Comms — there is likely a public-facing story in
  this once ESSENCE ratifies (PM has signaled possible publication); nothing to draft yet.

Respond to me directly; disagreements get synthesized to PM with options by 09-03, not smoothed.

— Arch
