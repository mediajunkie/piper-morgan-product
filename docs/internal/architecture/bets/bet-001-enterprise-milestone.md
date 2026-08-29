# Bet 001 — The Enterprise tier

**State**: PROPOSED (retroactive — first application of the ratified scope-bet gate, 2026-08-29)
**Tripwires crossed**: #5 (revenue/business-model assumption in the architecture), #6 (user class
that does not currently exist)
**What this covers**: the standing GitHub "Enterprise" milestone (dated Jul 4, 2027), the team-keys
design ("Target: Enterprise customers"), and every future purchase justified by "enterprise
adoption" — the ADR-012 phrase that A3's trace found doing load-bearing work with no customer
attached since August 2025.

## 1. The buyer

⟨**PM TO FILL** — a named human or organization that wants Piper's enterprise tier. If none exists
today, write "none named," which converts this bet into labeled speculation with the short leash
below, or decline the bet and the milestone retires.⟩

*Arch's context for the decision*: A3 found zero named enterprise buyers across the entire decision
record. The milestone's date (Jul 2027) has never had a plan behind it. Retiring it costs nothing
architecturally — the identity substrate (JWT, owner_id) stays regardless, because current real
users need it; only the *speculative tier* (team keys, org accounts, SSO aspirations) rides on this
bet.

## 2. The bet

If a real organization adopts Piper for a team, the essence (colleague + owner-scoped memory +
judgment artifacts) survives multi-seat deployment without redesign, because owner-scoping is
already per-principal. ⟨PM may restate.⟩

## 3. The cost box

⟨**PM TO FILL** — appetite. Arch's recommendation: **zero build until the buyer field is filled
with a name.** The pre-registered scope cut: no team/org schema, no SSO, no team-keys work, no
"enterprise-grade" justification accepted in any ADR/PR, until this memo's state is RATIFIED with
a named buyer.⟩

## 4. The kill condition

If no named enterprise buyer exists by ⟨**PM TO FILL** — date; Arch suggests the beta retrospective⟩,
the milestone is deleted (not pushed out another year), team-keys docs move to the archive with
provenance, and any future enterprise ask re-enters through a fresh bet memo.

## 5. The smallest true version

Not applicable until a buyer exists — that's the point of this memo. When one does: one real team,
manually provisioned, no new machinery, observed for a quarter before any enterprise-shaped code is
written.
