# ADR-079 — Owner-Scoping Integrity Contract (unscoped reads impossible-by-construction, mechanically enforced)

**Status**: **ACCEPTED (v0.1, 2026-07-16)** — Arch-authored, on the integrity authority PM delegated + Lead's confirmation that the #1419 multi-tenancy audit's scope is systemic. Synthesizes already-accepted per-feature owner-scoping decisions into one contract + its mechanical enforcement. **HOST trust-lens welcome** (this is a trust-boundary contract) — informative, not gating, since the constituent decisions are already accepted. **PM retains veto.**
**Author**: Chief Architect (arch)
**Deciders**: Architect (author); Lead Dev (audit + lint build); PM (Finish-the-Unfinished sprint ratification, #1424).
**Related**: **ADR-071** (content-store owner-scoping, D2) · **ADR-075** (config/personalization ownership, D1a) · **ADR-078 D1a** (session-activity ledger owner-scoping) · **#1366** (the personalization cross-user leak — the impossible-by-construction bar) · **ADR-076 D4** / **#1382** (fail-closed) · **#1308** (exempt-list/allowlist discipline) · **#849** (keychain-scoping lint, routes-only) · **#1252** (principal-threading lint) · methodology-41 (make-drift-impossible). Inventory: `docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md` (#1419) + the Finish-the-Unfinished census. **Scope boundary**: the parallel `check-silent-death` lint (#1423) enforces *honest-degradation* (ADR-060 / #1331 / #1269 family), NOT owner-scoping — it is a separate contract, not housed here.

---

## Context

The owner-scoping discipline — *every read of owner-bearing state is scoped to the acting principal; cross-user reads are not expressible* — has been ruled **case-by-case**: ADR-071 D2 (content stores), ADR-075 D1a (personalization), ADR-078 D1a (the session-activity ledger), each time as "impossible-by-construction," motivated by the #1366 cross-user leak. The #1419 multi-tenancy audit found the obvious gap: **a per-feature discipline enforced by memory is not systemic.** Unscoped reads remained *possible* across the server-owned-state family — keychain lookups with no principal, repository queries over owner-bearing tables with no owner predicate, config-file credential shadowing, provider-selection consent failing *open* on error. "We ruled it each time" is not the same as "it cannot happen."

This ADR promotes the discipline from a repeated ruling to **one contract with mechanical enforcement** — the same move ADR-077 made for routing-integrity (a lint makes the property hold by construction, not by vigilance).

## The contract (decisions)

**D1 — Every read of owner-bearing state is owner-scoped by construction; cross-user resolution is not expressible.** This is the ADR-071/075/078-D1a bar, generalized to the whole server-owned-state family. A reader that *can* return another principal's data — even behind an `owner_id=None`/admin path — violates the contract; the scoping must be structural (the WHERE keys on the resolved owner, no unscoped branch exists), not conventional.

**D2 — Enforced mechanically by `check-unscoped-reads` (the #1419 lint), CI-blocking.** Two rules:
- (a) **Credential access needs a principal**: `KeychainService.get/store/delete_api_key` + config-file credential loaders with no principal argument are violations, unless allowlisted (D4).
- (b) **Owner-bearing repository reads need an owner predicate**: a query method over an owner-bearing table whose `where` carries no owner predicate is a violation.
Warn-mode → count-as-ceiling → migrations lower it in the same commit (the `MAX_DISPATCH_SITES` ratchet discipline); the CI-blocking flip is Arch-gated.

**D3 — DERIVE the owner-bearing table set; never hand-list it.** The set of owner-bearing tables is computed at lint-time (any model with an `owner_id`/`user_id` column), not enumerated in the lint. This is make-drift-impossible applied to the enforcement itself: a hand-list drifts the moment a new owner-bearing table is added — the exact failure the lint exists to prevent, one level up. A new owner-bearing table is **auto-covered** (and auto-flagged if its reads are unscoped).

**D4 — The allowlist is justified-exceptions only, and the rationale names HOW.** A legitimately-global credential/read (the CLEARED set: server-fallback LLM keys, OAuth *app* credentials, Slack socket-mode token) is allowlisted with a one-line rationale that states *why it is global / how it is scoped* — not a bare "cleared." An unjustified unscoped read fails the build. (The #1308 exempt-list lesson: an exemption that isn't recorded with its reason is an abuse surface.)

**D5 — Scoping and consent fail CLOSED.** A keychain/store/lookup **error** must never *relax* a scoping or consent boundary. The failure mode is fail-to-the-safe-default (server-default set, empty result) with honest degradation — never fail-*open* (silently disabling the consent filter / returning unscoped data). This is the ADR-076-D4 / #1382 fail-closed discipline applied to owner-scoping + consent. (Motivating case: #1415's `get_configured_providers` failing open on keychain error silently disabled the per-user consent filter.)

**D6 — Indirect scoping is legitimate, and allowlisted-with-how.** A query owner-scoped via a join/subquery (rather than a literal `owner_id` in its own WHERE) is correct but not detectable by a naive predicate check — it goes on the D4 allowlist with a rationale naming the join/filter that carries the owner (e.g. `DocumentRepository._readable_base_ids(owner_id)`, ADR-071 P2). This keeps the lint's false-positive class explicit rather than suppressed.

## Consequences

- The impossible-by-construction bar the Architect has been holding case-by-case is now **systemic and mechanically enforced** — a new feature that reads owner-bearing state cannot ship an unscoped read past CI without an explicit, reasoned allowlist entry.
- **New owner-bearing tables are auto-covered** (D3) — the contract can't go stale as the schema grows.
- Same make-drift-impossible spine as ADR-077 (routing-integrity lint), ADR-072 (frontmatter-derive), #1106 (MANIFEST-derive), ADR-078 (ledger owner-scoping) — the recurring architectural move: promote a discipline from vigilance to construction.
- Composes with (does not replace) the parallel honest-degradation enforcement (`check-silent-death`, #1423, ADR-060 family) — the two lints are the two halves of "the server tells the truth and shows only your data."

## Open questions

- **HOST trust-lens** (welcome, non-gating): the fail-closed-on-consent rule (D5) and the allowlist-names-how discipline (D4) are the trust-load-bearing parts — a HOST pass would sharpen the allowlist-rationale bar.
- **Lint precision calibration** (build-time, not architectural): the owner-predicate detection (D2b) and the derive-the-table-set (D3) are calibrated in warn-mode before the CI-flip; the indirect-scoping false-positive class (D6) is surfaced there.

---

*ADR-079 v0.1 ACCEPTED, Arch 2026-07-16, on the #1419 multi-tenancy audit + the Finish-the-Unfinished sprint. Promotes the owner-scoping discipline (ADR-071/075/078-D1a/#1366) from a repeated per-feature ruling to one contract enforced by construction: unscoped reads of owner-bearing state fail the build unless allowlisted-with-reason; the owner-bearing table set derives itself; scoping/consent fails closed. PM retains veto; HOST trust-lens welcome.*
