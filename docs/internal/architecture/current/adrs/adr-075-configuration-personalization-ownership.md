# ADR-075: Configuration / Personalization Ownership — Per-User Scoping for Instance Config

**Status**: v0.1 (Arch-authored 2026-07-06) — **DRAFT, for CXO/HOST trust-lens then ratification.** Grounded in #1366 (PM-caught 2026-07-06: `PIPER.user.md` is a single unscoped instance-level file that leaks PM's personalization + GitHub default-repo to every user on the shared `alpha.pipermorgan.ai` instance). Component A (github default-repo scoping) already shipped this session (Lead, `f04cbeea6`/`1784ae017`); this ADR governs the remaining decomposition (Component B + the taxonomy). Completes the **server-owned-state family**: ADR-070 (per-user connector *bindings*), ADR-071 (per-user content *stores*), **ADR-075 (per-user config/personalization)**.
**Date**: 2026-07-06
**Author**: Chief Architect
**Deciders**: Architect (author); PM (caught the gap; direction); Lead Dev (Component A implementation + two call-site corrections to the original ruling); PPM (Beta-Blockers scope); CXO + HOST (trust-lens — pending)
**Supersedes / superseded by**: none
**Related**: **ADR-066 D7** (Configuration Ownership Convention — server-owned + per-request host augmentation; *orthogonal axis* — see D0), **ADR-071** (User-Auth Anchoring for content stores — the direct pattern-parent: `owner_id` + `is_global_pm_domain`), **ADR-070** (MCP-Consumer Connector Architecture — where the github default-repo binding lives, `ConnectorConfigService`), **ADR-058** (user-scoped credentials — the original make-impossible precedent), methodology-40 (layer-then-migrate), methodology-41 (mechanism-displaces-unreferenced-discipline)
**Grounding substrate**: this session's #1366 ruling (`decisions.log` 2026-07-06 ~06:45) + Lead's Component-A completion memo (call-site corrections folded into D1)

---

## Context

### What problem does this ADR solve?

`PIPER.user.md` is a single file at a fixed path (`config/PIPER.user.md`, fallback `config/PIPER.md`), read by a **module-level global singleton** (`services/configuration/piper_config_loader.py::piper_config_loader`). Every reader — `get_system_prompt()`, `get_user_context()`, `load_github_config()`, `load_standup_config()`, `load_pm_identity_config()` — takes **zero user-scoping parameters**. This was correct for a single-user local prototype (one person, one machine, one file). It is **wrong on a shared multi-user server instance**, and `alpha.pipermorgan.ai` is exactly that: one process, multiple external testers (onboarded via #1344), all reading the same file. Every tester's Piper is primed with PM's personal system-prompt context, and (before Component A) PM's GitHub default-repo.

### Why this is architectural, not a per-reader patch

The same datum-scoping question recurs across every field the loader exposes, and the *right answer differs by field*. Blanket "scope everything by user" would be wrong (it would force per-user plumbing onto config that is legitimately install-wide). The decision that has to be made once, centrally, is **the taxonomy** (which config is per-user, which is PM-domain-global, which is install-wide) plus **the resolution + degradation invariants**. That is ADR-shaped, not a patch.

### Prior art / cross-references (and one axis distinction)

This ADR is the third leg of the **server-owned-state** family and reuses its shape one layer up:
- **ADR-058** — per-user *credentials* behind the server, indexed by identity (the make-impossible precedent).
- **ADR-070** — per-user connector *bindings* (`ConnectorConfigService.get_default_repo(owner_id)` is where Component A's fix landed).
- **ADR-071** — per-user content *stores* (`owner_id` stamped-at-write + scoped-at-read + `is_global_pm_domain` for PM-domain content). **This is the direct pattern-parent** — ADR-075 extends D1–D5 of ADR-071 from content rows to configuration.

### D0 — Relationship to ADR-066 D7 (the axis distinction — read this first)

ADR-066 D7 ("Configuration Ownership Convention") and ADR-075 are both "configuration ownership," but on **orthogonal axes**, and conflating them causes errors (the author did, briefly, mid-session):
- **ADR-066 D7 = the host↔server axis.** *Where does config physically live and persist?* Answer: behind the MCP server, not on the host filesystem; the host augments per-request only. This is the deployment/portability property that makes "run anywhere" structural.
- **ADR-075 = the per-user tenancy axis.** *Whose config is it, and how is it scoped so users don't see each other's?* Answer: owner_id-scoped, with a category taxonomy.

ADR-075 **sits on** ADR-066 D7 (personalization config is server-owned, per D7) and **adds** the per-user-scoping axis D7 gestured at ("when #1185 lands, D7's server-owned-config pattern naturally accommodates per-user key materialization"). No conflict; ADR-075 realizes the per-user extension for personalization.

### Trust framing (for CXO / HOST trust-lens)

The user-facing contract this protects: **a user's Piper must never surface another user's — or PM's — personal context, priorities, or targeting.** The failure mode is not merely "odd personalization"; it is a privacy breach (PM's standing priorities/portfolio exposed to a tester) and, before Component A, a data-integrity breach (a tester's github action defaulting to PM's real repo). The trust-lens question this ADR most needs answered: **on a shared instance, when a user has no personalization record yet, what neutral default does their Piper present** — and is "neutral default" itself surfaced transparently (trust-check) or silent? (Parallels ADR-072 D5's transparency-when-gated.)

---

## Decision

### D1 — The three-category taxonomy (scope by category, never blanket)

Instance configuration is not one kind of thing. Every field must be classified into exactly one of three categories, and the store/scoping follows the category:

| Category | What | Examples (verified this session) | Scoping |
|---|---|---|---|
| **1. Per-user personalization** | Config whose *correct value depends on who is asking* | system-prompt context (name/role/tz/style/focus/portfolio/standing-priorities), `default_repository`/`owner`, `default_labels`, standup prefs | **`owner_id`-scoped** (D2) |
| **2. PM-domain-global** | PM-domain-authoritative content that is intentionally global-by-design | the ADR-071 D1 distinguished-owner content set | **`is_global_pm_domain`** (ADR-071 D1) |
| **3. Install-wide config** | A property of the *deployment/instance*, correct regardless of user | PM-numbering format (`pm_prefix`/`pm_start`/`pm_padding`) | **Instance-level singleton — explicitly NOT per-user; NOT a leak** |

**Classification test**: does the value's correctness depend on *who is asking* (→1), is it PM-domain-authoritative *for all* (→2), or is it a property of the *deployment* regardless of user (→3)?

*(Category 3 is a correction owed to Lead: the original #1366 ruling over-included `pm_number_manager.py`'s 8 `load_github_config()` sites as leak sites. Lead verified they read `pm_prefix`/`pm_start`/`pm_padding`, not repo fields — install-wide numbering format, category 3. Naming category 3 explicitly is the guard against over-scoping it.)*

### D2 — Category-1 personalization is `owner_id`-scoped, server-owned (extends ADR-071 to config)

Per-user personalization moves into an `owner_id`-scoped, server-owned store (ADR-066 D7 axis: behind the server, not the host file). Same three ADR-071 invariants, one layer up:
- **Stamped-at-write** by resolved principal;
- **Scoped-at-read** by resolved principal;
- **`is_global_pm_domain`** carries the PM-vs-tester distinction (category 2).

*Which store*: extend an existing user-scoped profile store (`PersonalityProfileRepository` / a profile table) vs. add a dedicated personalization store — **Lead's build-time call**; this ADR fixes the *shape* (owner_id-scoped, server-owned, is_global_pm_domain-aware), not the table choice.

### D3 — The file is the single-tenant / local-dev default, not the shared-instance source (m-40)

`PIPER.user.md` is **retained as the sole-owner / local-dev default**. Where there is exactly one owner (local dev, single-tenant install), the file *is* that owner's config and nothing regresses (satisfies #1366 AC "no regression to the single-tenant/local-dev case"). On a shared/hosted instance the `owner_id`-scoped store is authoritative and the file is a fallback default only. **Resolution order: owner_id-scoped store → (miss) → neutral default (D4); the PM-personal file is never the fallback for a non-PM principal on a shared instance.**

### D4 — Principal-resolution at the boundary + honest neutral-degradation (ADR-071 D4 shape)

Personalization resolves by the **authenticated principal at the request boundary** (ADR-071 D4). The load-bearing invariant — the actual Component-B leak closure: **on a shared instance, a request with no scoped personalization record for its principal degrades to a NEUTRAL default, never to PM's personal file.** `get_system_prompt()` / `get_user_context()` and their request-path callers (`conversational_floor._get_system_prompt`, the classifiers) must resolve/accept a principal and must not silently serve PM's context to another user. "Never silently serve another principal's config" is the config-layer form of ADR-071 D3 + ADR-070 D5's never-silently-empty.

### D5 — Enforcement guard (m-41; same family as Component A's lint + #1283/#1307)

A guard/lint asserts category-1 reads are principal-scoped on request paths — the make-drift-impossible family already used for Component A (`TestGitHubDefaultRepoScopingEnforcement`), #1283 (reachability), #1307 (exempt-list). It must:
- fail the build if a request-path reader resolves category-1 personalization off the unscoped loader;
- **not** false-positive on category-3 (install-wide) reads or the category-2 PM-domain path (D7).
Static reachability + a behavioral check that a second principal on a shared instance never receives the first's context.

### D6 — Migration shape (layer-then-migrate, m-40; Component A already done)

- **Component A (category-1 `default_repository`/`owner`) — SHIPPED** this session; the scoped home pre-existed (`ConnectorConfigService`, ADR-070), so it was a migration-completion + lint, not new design.
- **Component B (category-1 system-prompt context + `default_labels`)** — the store build (D2) + boundary resolution (D4) + guard (D5). `default_labels` (Lead-flagged: read off the unscoped loader, no scoped home) is category-1 and rides here — *unless* build-time analysis shows it is install-wide, in which case it is category-3 and stays instance-level (decide at build; do **not** design a standalone store for it).
- **Component C (#1260 `resolve_pm_owner_id()` / `load_pm_identity_config()`)** — lower-risk (CLI ingestion, not the alpha web path). The *concept* is sound (ADR-071 D1 distinguished PM-owner is legitimate); repoint the *mechanism* from an unscoped file-read to the durable owner record when B's store lands.

Layer-then-migrate: the single-owner file-default generalizes to the owner_id-scoped record with no rework.

### D7 — What stays install-wide (the over-scoping guard)

Category-3 config (PM-numbering format) **must not be forced per-user.** Over-scoping is its own defect — it adds `owner_id` plumbing to a datum with one correct value per instance, and it would make the D5 guard incoherent. The guard must treat category-3 as legitimately unscoped. If a category-3 datum ever *should* become per-user, that is a new classification decision, made explicitly, not by default.

---

## Consequences

### Positive
- Closes the #1366 privacy leak (category-1 personalization) by construction, reusing the ADR-058/070/071 shape rather than inventing one.
- Completes the server-owned-state family across creds / bindings / content / config.
- The taxonomy prevents both under-scoping (leaks) and over-scoping (needless per-user plumbing on install-wide config).

### Negative / tradeoffs
- A new owner_id-scoped store (or a profile-store extension) + a principal-resolution seam on the system-prompt path — real work, sequenced post-Component-A.
- The neutral-default content for non-PM users on a shared instance is a genuine product/trust decision, not a pure-mechanism one (hence the trust-lens).

### Non-consequences
- Does **not** rewrite the `PIPER.user.md` file format.
- Does **not** build the multi-tenant onboarding UI (names the seam; ADR-071 D7 territory).
- Does **not** force category-3 config per-user.

## Open questions (v0.1)
- **OQ-1 (build)**: extend `PersonalityProfileRepository` / a profile table, or a dedicated personalization store? (Lead's call at build.)
- **OQ-2 (classification)**: is `default_labels` per-user (category 1) or install-wide (category 3)? Decide at build from actual usage.
- **OQ-3 (trust — for CXO/HOST)**: the neutral-default personality/context a non-PM principal gets on a shared instance — what is it, and is the "you're seeing the default" surfaced transparently or silent?
  - **→ HOST trust-lens RESOLVED 2026-07-06 (PASS, pending CXO UX)**: **surfaced, NOT silent** — parallel to ADR-072 D5 (transparency-when-gated): a user running a neutral default without knowing it can't evaluate whether Piper's responses are personalized or generic; the discovered silence is more trust-damaging than upfront transparency. **Surfaced = one-time, at first session/response, actionable, non-catastrophizing** ("Piper is using a default configuration for you — personalize it here"), NOT per-response (noise) and NOT silent (false confidence). Two HOST conditions folded into **Component B scope** (no longer an indefinite OQ): (1) the "default is surfaced once" path is committed as part of B, exact UX is CXO's; (2) the neutral default must be a **real seeded persona record at account creation** (a genuinely capable professional Piper — the product's first impression), NOT an implicit empty fall-through that produces confusing behavior. **v0.2 ACCEPTED gated on CXO's UX-direction confirmation** (the surface + phrasing); HOST is ready to ratify once CXO confirms.

## What this ADR is NOT
- Not a per-reader patch — it is the taxonomy + invariants decided once.
- Not a blanket "scope everything by user" — D1/D7 explicitly protect install-wide config.
- Not a claim that the file goes away — D3 keeps it as the single-tenant/local-dev default.

## decisions.log entry (per CLAUDE.md recording-decisions discipline)
The 2026-07-06 ~06:45 #1366 ruling entry already records the decomposition; this ADR is its formalization. A one-line pointer will be appended on ratification.
