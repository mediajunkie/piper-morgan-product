# Architectural Review 2026 — Reorientation Plan v1.0

**Author**: Chief Architect, 2026-08-29 (phases 5–7 of the review, made explicit)
**Status**: ACTIVE — this is the operating plan; PM may amend any line
**One rule up front**: the pending Bet Memos (001–003) are **explicitly non-blocking**. Nothing in
this plan waits on them; they resolve whenever PM's fields arrive, and their outcomes adjust
scope, not sequence.

---

## The four workstreams, each with an owner, a next action, and a done-condition

### A — Socialize (owner: Arch · starts TODAY)

The review's outputs are on `origin/main`, but on-main is not socialized — most of the cohort has
partial visibility via cc trails at best. Actions:

- **A1 (today)**: cohort-wide broadcast memo from Arch (cc PM): what the review found, what PM
  ratified, where every artifact lives, and what changes for each role. SENT — see
  `mailboxes/*/inbox/broadcast-arch-review-reoriented-2026-08-29.md`.
- **A2 (today)**: direct trifecta ask to **CXO and PPM** — a read-and-respond pass on ESSENCE v0.1
  specifically, by **Wed 09-02**. They are the directional trifecta; ESSENCE doesn't graduate from
  v0.1 to ratified law without their pass. (PM ratifies last, after their input, per the normal
  order.) SENT — folded into A1's broadcast with a named ask line for each.
- **A3 (by 09-03)**: Arch synthesizes all responses; disagreements surface to PM with options, not
  buried. Hard calls are PM's.
- **Done when**: ESSENCE v1.0 carries PM's ratification line + trifecta input recorded; every
  leadership role has either responded or explicitly passed.

### B — Documentation reform (owner: Arch, with Docs + CIO · the "formal plan to refactor the architecture documentation" — yes, and this is it)

- **B1**: ESSENCE ratification per A. The anchor document everything else hangs from.
- **B2 (Arch drafts by 09-01)**: name the **living core doc set** — the small list that absorbs
  all surviving decisions. Proposal to be confirmed in the draft: ESSENCE.md · a current-state
  architecture overview (successor to architecture.md, rewritten against Leg B) ·
  intent-routing-stack.md (already maintained) · data-model.md (corrected) · a connector map ·
  the glossary. Each with an owner and a staleness contract (max age before auto-flagged).
- **B3 (kickoff 09-01, target ~1 week)**: the **corpus-disposition pass** over three corpora —
  ADRs (absorb-into-core-docs + mark "absorbed into X"), methodology-core (64 files), patterns
  (81 files) — using the citation census (already filed, reproducible) as the mechanical first
  axis and effective/inert judgment as the second. Arch runs it with CIO (methodology owner) and
  Docs (docs owner); dispositions execute through the same fix-or-delete pipeline as code.
  Leg A1's silently-abandoned list and Docs' adr-028 location-lie are already in the case file.
- **B4 (with B3)**: replace the hand-maintained ADR index with a **derived view** generated from
  ADR Status headers (same move as reachability-map; the stale banner placed 08-29 is the interim).
- **B5 (backlog, seeded now)**: Leg D's **24 unanswerable questions** become the doc-gap backlog —
  each gets answered in a core doc or explicitly deferred with a reason. This is the measured
  to-do list for "could the docs rebuild the product."
- **Done when**: core docs named and owned; every ADR marked absorbed/superseded/historical; both
  corpora dispositioned; the index is derived; the 24 questions each have a home or a dated
  deferral.

### C — Code reorientation (owner: Lead executes, Arch gates architecture calls)

- **C1 (in motion)**: the staged Inversion flip — Lead has it sequenced into PM's watched round.
  Nothing further from Arch until the divergence debrief.
- **C2 (encoded here, per PM's deprecation question)**: **legacy-classifier retirement criterion**
  — when (a) flip coverage reaches all registered categories, (b) shadow/live divergence over a
  Lead-defined turn count is characterized and accepted, and (c) the write wave has migrated the
  registered EXECUTION set through the allowlist — the legacy LLM-classifier surface is DELETED
  with provenance, July-style. **Check date: 2026-09-30.** If not met by then, we say why out
  loud rather than letting it linger (the A1 zombie pattern, refused in advance).
- **C3 (memo today)**: spatial disposal (11 modules, PM-ruled 08-15/16) + Leg B's newly-census'd
  dead families (~88 modules / ~23.7K LOC) routed to Lead's fix-or-delete pipeline with the
  census as caller evidence. SENT — `mailboxes/lead/inbox/routing-arch-to-lead-disposal-*.md`.
- **C4**: #1690 (demo plugin default gating) — filed, sits in Lead's queue like any bug.
- **C5**: MCP-path increments (Leg D's ordering, cold-start reflection first) enter roadmap
  sequencing via PPM — this is part of what A1's broadcast asks PPM to pick up, and it's where
  "all new build effort goes to the MCP path" becomes sprint reality instead of a log entry.
- **Done when**: C2's criterion is met or its miss is explained; the dead 19% is dispositioned;
  MCP increments appear on the board with milestones.

### D — Governance (owner: Arch · mostly done, listed for completeness)

- Scope-bet gate: RATIFIED, register live at `docs/internal/architecture/bets/`. Bets 001–003
  await PM fields — **non-blocking by design**.
- "Verified how" field: SHIPPED (CLAUDE.md + close-issue-properly), skills-wide sweep rides B3.
- Era-2 ADR statuses: CORRECTED 08-29. decisions.log carries every ratification.

## The one-line answer to "how do we operationalize today's insights"

**Each ratified insight is now a workstream line with an owner, a next action, and a
done-condition — and the two that need other people (A's trifecta pass, C5's roadmap entry) were
put in their inboxes today rather than waiting to be discovered.** Arch owns the plan's integrity
and reports workstream state in each weekly review until all four close.
