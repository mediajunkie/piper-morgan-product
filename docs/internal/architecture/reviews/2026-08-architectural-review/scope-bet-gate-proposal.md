# The Scope-Bet Gate — proposal v0.1

**Author**: Chief Architect, 2026-08-29, at PM's request ("I like this idea quite a lot and would
like your help designing that gate")
**Status**: DRAFT for PM ratification
**Design spec in negative**: Leg A3 — eleven scope inflections June 2025 → June 2026; one shaped
like a decision; none cost-boxed; the pivotal one ("alpha = multiple external users") has no
artifact at all. The gate exists so that the *next* "should we become X" is asked as a question.

---

## The one-sentence rule

**Crossing a scope tripwire requires a one-page Bet Memo, PM-ratified, before implementation
starts.** Not before *thinking*, not before *prototyping in a branch* — before the architecture
absorbs it.

## The tripwires (crossing ANY one triggers the gate)

1. **A new principal or tenant class** — a second kind of human user, org/team accounts,
   workspaces, sharing between people. *(The one that cost the most, per A3.)*
2. **A new hosted or public surface** — a new domain, a new always-on service, a new inbound
   channel (webhook, socket, listener).
3. **A new external integration where WE hold the grant** — any connector whose OAuth
   token/credential lives in Piper's backend. *(C4's decision rule made procedural: host-mediated
   reads don't trip the gate; held grants do.)*
4. **A new standing infrastructure dependency** — a queue, database, vendor service, or runtime
   the system won't start without.
5. **A revenue or business-model assumption entering the architecture** — anything justified by
   "customers will…" or "at scale we'll need…".
6. **The catch-all, and the most important**: any purchase whose justification names a user class
   that does not currently exist. *(A3's speculative-complexity definition, verbatim, as a
   tripwire.)*

What does NOT trip the gate: bug fixes, completing already-ratified work, refactors within
existing scope, experiments clearly labeled and flag-gated, anything for a currently-real named
user doing a currently-real task. The gate is for *becoming*, not for *building*.

## The Bet Memo — five fields, one page hard limit

1. **The buyer.** A named human who wants this. A person, not a persona, not a benchmark, not
   "PMs like Sarah." If no such human exists, the memo says so explicitly — that doesn't
   auto-reject the bet, but it converts it into a labeled speculation with a shorter leash.
2. **The bet.** What we believe becomes true if we build it — one falsifiable sentence.
3. **The cost box.** The appetite, Shape-Up style: a time/complexity ceiling we will not exceed,
   and one named thing we will NOT do even if tempted (the pre-registered scope cut).
4. **The kill condition.** The observable signal that would mean the bet failed, and the DATE we
   check it. A bet without a check date is a permanent tenant — that's how the Jul-2027 Enterprise
   milestone happened.
5. **The smallest true version.** What ships end-to-end to a real user first. (PM's ship-early
   principle, structural; also Leg D's increment discipline.)

## Process

- Memos live in `docs/internal/architecture/bets/` — `bet-NNN-slug.md`, append-only, with an
  INDEX.md listing every bet and its state: `proposed / ratified / declined / won / lost /
  expired`.
- **PM ratifies or declines explicitly** — silence is not ratification (per the standing
  ratification rule). Arch reviews for architectural cost honesty before it reaches PM.
- The kill-condition date goes onto the review-owner's standing items when ratified. When it
  arrives, the check runs and the state updates — `won` absorbs into core docs; `lost`/`expired`
  triggers the same delete-with-provenance pipeline the July deletions modeled.

## Enforcement — honest about which layer does what (m-43)

- **Checkable mechanically**: the artifact's existence. A PR-template line ("Does this cross a
  scope tripwire? → link the Bet Memo") plus a lightweight CI grep that a PR touching known
  tripwire surfaces (new alembic migration adding a tenant-shaped column, new OAuth-grant storage,
  new service in deploy config) carries a `bet:` reference. Imperfect by design — it catches the
  common shapes, not all shapes.
- **Not mechanizable, and we don't pretend**: judging whether something IS a scope change. That
  stays prose discipline, same as the mailbox rule — the hook is advisory, the discipline is
  primary. The gate's real mechanism is cultural: it gives any agent or human a *named, cheap,
  legitimate move* ("this needs a bet memo") at the exact moment scope tries to slide in as a
  technical default. A3 shows that moment came at least eleven times and nobody had a move.

## Retroactive first uses (proposed — these make the gate real instead of ceremonial)

1. **The standing Enterprise milestone (Jul 4, 2027)** — gets a Bet Memo or gets retired. Buyer
   currently: none named.
2. **`workspace_id` / `TenantContext` sentinels** (ADR-058's speculative half) — same treatment.
3. **The Notion connector's held grant** — tripwire 3 applied to the one genuinely ambiguous case
   from the synthesis (Convergence 4): if its only use is in-conversation reads, the memo should
   fail its own cost-box test on the BYOC path, and that tells us something we currently only
   suspect.

## What this gate does not do (scope statement)

It does not slow down building for real users — nothing a current named user needs trips it. It
does not prevent ambition — it prices it. It does not replace ADRs/PDRs — a ratified bet that
matures into lasting architecture still gets its decision record; the memo is the *pre*-decision
artifact that eleven inflections never had.
