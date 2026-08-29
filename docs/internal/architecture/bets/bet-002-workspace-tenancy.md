# Bet 002 — Workspace/team tenancy machinery

**State**: PROPOSED (retroactive, 2026-08-29)
**Tripwires crossed**: #1 (new tenant class), #6 (user class that does not currently exist)
**What this covers**: the speculative half of ADR-058 — `workspace_id` columns carrying an
all-zeros `DEFAULT_WORKSPACE_ID` sentinel, `TenantContext`, and the "future workspace/team
features" they were built for. NOT covered: ADR-058's real half (per-user `owner_id` isolation),
which had a real buyer (leaking alpha testers, #734) and stays untouched.

## 1. The buyer

⟨**PM TO FILL** — who wants workspaces/teams? A3 found the buyer "still unnamed, still the
zero-UUID sentinel today." If the answer is "the same future enterprise customer as Bet 001," say
so — then this bet's fate is chained to 001's and they resolve together.⟩

## 2. The bet

That workspace-shaped tenancy will someday be needed, and pre-planting the columns/context now is
cheaper than adding them later.

*Arch's honest cost analysis for the decision*: the counter-evidence is A3's whole table — the
carrying cost of speculative tenancy has been paid monthly (three inconsistent principal-anchoring
styles, 40+ degradation sites, two standing lints). BUT this specific residue (a sentinel column +
an unused context class) is near-inert: it doesn't generate incidents by itself. So the real
choice is not "expensive vs. free" — it's "carry a small inert lie in the schema" vs. "delete it
and re-add behind a ratified bet when a buyer exists." Migration cost to delete: one alembic
migration + removing `TenantContext` references; cost to re-add later: roughly the same. Symmetric
costs mean the deciding factor is honesty of the schema, not economics.

## 3. The cost box

⟨**PM TO FILL** — Arch's recommendation: delete the sentinels (schema tells the truth), zero
workspace build until a buyer names itself. Alternative defensible answer: explicitly re-label the
sentinels as "inert, retained under Bet 002, do not extend" and spend nothing either way.⟩

## 4. The kill condition

⟨**PM TO FILL** — if deletion: n/a, the bet is declined and closed. If retention: a date at which
unextended sentinels get deleted anyway — Arch suggests the same beta-retrospective checkpoint as
Bet 001.⟩

## 5. The smallest true version

If a workspace buyer ever materializes: one shared list/document between two named real users,
built on existing `owner_id` + a sharing grant — no workspace_id, no TenantContext — and observed
before any tenancy schema returns. (ADR-044's sharing fields are the honest starting point; the
workspace abstraction earns its way in only if that proves insufficient.)
