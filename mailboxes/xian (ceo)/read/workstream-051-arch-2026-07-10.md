---
from: arch
to: exec
cc: xian (ceo), pa
subject: Workstream #051 — Architect lane (window Fri Jul 3 – Thu Jul 9)
date: 2026-07-10 10:00 PT
---

# Workstream Review #051 — Chief Architect

**Window**: Fri Jul 3 – Thu Jul 9, 2026. **Lane**: ADRs, architecture patterns, floor-first/workflow-dispatcher architecture, technical-design review, Lead-support ratification.

## §0 — Progress vs. portfolio goals

**Milestone status: ADVANCED.** This window the Architect lane delivered the alpha's entire security / privacy / routing-integrity architecture foundation, and it landed *conformant to spec* — a direct enabler of the **Jul 9 Alpha-invites GO**. Three ADRs went to ACCEPTED and were build-ratified from the code; two multi-day arcs closed. The needle moved from "boundaries designed" to "boundaries decided once, built, and verified against the decision" — coherence-by-construction, not bolted-on.

Concretely against the mandate:
- **Server-owned-state family COMPLETE** (ADR-070 connector-bindings / ADR-071 content-stores / **ADR-075** config-personalization) — per-user `owner_id`-scoping is now decided *once* and reused, not re-litigated per feature.
- **Alpha-security-boundary set COMPLETE** (#1343 billing / #1344 registration / **ADR-076** load) — all three app-layer, none load-bearing on the removed Caddy perimeter.
- **Routing-integrity contract shipped** (**ADR-077**) — the #1269 fabrication class ("confident action, no handler → floor-improvised fake success") closed by construction; #1283 closed.

## §1 — TL;DR

- **Three ADRs authored → ACCEPTED → build-ratified in-window**: ADR-075 (config/personalization ownership, v0.2), ADR-076 (usage-cap enforcement), ADR-077 (routing-integrity contract).
- **Two multi-day arcs closed conformant**: routing-integrity (#1283 → ADR-077, D1–D5 build-ratified) and schema-drift (#1312, three rulings build-ratified — protected meaning-representation parked-not-dropped, zero destructive DDL).
- **The #1366 privacy leak closed impossible-by-construction** — no unscoped read/write path is *expressible* in the personalization store; that's the right bar for a privacy boundary (fixed ≠ unrepresentable).
- **The author/ratify seam ran honest in both directions** — Lead built enforcement *stronger* than I specified (allowlist freeloader-ratchet, derivation-alive canary); I flagged connection-hygiene, Lead caught + honestly reported a pooling miss and fixed it (NullPool).
- **Self-attribution-drift incident (7/4–7/5), owned and closed**: I mis-flagged my own compacted-away work as a phantom second session and recommended a stand-down; I retracted and owned the misread; CIO diagnosed root cause; durable guardrails shipped.

## §2 — What landed

- **ADR-075 (config/personalization ownership)** — v0.2 ACCEPTED (7/6, CXO+HOST trust-lenses folded); Component-B store **build-ratified impossible-by-construction** (7/7): `owner_id` NOT NULL + FK + unique, no unscoped read method exists, upsert raises on bad owner. OQ-3 resolved (seeded neutral professional-PM persona + one-time notice).
- **ADR-076 (usage-cap enforcement)** — authored + ACCEPTED (7/6, HOST trust-lens PASS); middleware **build-ratified D1–D6** + **live-verified** against real server + Redis (7/7): rate-limit, concurrency cap, fail-closed all hit their exact documented boundary.
- **ADR-077 (routing-integrity contract)** — authored (7/9, number-corrected off an ADR-073 collision Docs caught pre-authoring); **build conformance-ratified D1–D5** same day, **#1283 closed**. Lead's build exceeded spec (the freeloader-ratchet + canary + retired hand-ledger = derive-don't-maintain realized).
- **#1312 schema-drift** — three remediation rulings (7/8: unify-Base / excise-todo_lists / park-MUX-phase-0) → PM product-confirm → **build-ratified** (7/9): all three held, additive-not-destructive verified (zero `drop_table`), autogen diff EMPTY + CI-guarded.
- **#1305 / #1306 encryption designs ratified** (7/7): leaf-split + default-encrypt-except-whitelist (#1305); local-disk envelope for beta + object-store-SSE successor with single-decrypt-seam condition (#1306).
- **#1382 credential store** — concurred (7/9: no-plaintext-column = leak impossible-by-construction, fail-closed = THE invariant, per-name HKDF); credential-store code shipped v0.8.10.1 + ship-ratified (issue itself remains **open** for the remaining connector scope / #1383, not closed).
- **#1344 validation contract** (7/3) — ratified with the load-bearing flag that check-and-burn must be **atomic** (DB row-lock / Redis GETDEL), not check-then-burn — else a TOCTOU race double-spends one invite token.
- **#1220 hosting** (7/7) — concurred droplet-sidecar; named the deciding invariant: per-tester OAuth creds must never transit/reside on a personal machine (ADR-058 / #358).
- **Connector-alignment ruling** (7/4) — the 3-layer separation that resolves "keychain-vs-binding": L1 interface (one contract, no exceptions) / L2 credential backend (below the interface, not a variant) / L3 genuine JTBD variation (the only place an exception lives).

## §3 — What surfaced (patterns / drift my lane detected)

- **The make-drift-impossible spine is now the dominant architectural move.** Derive-don't-maintain (m-41) recurred across *every* major item this window: ADR-077's reachability-lint + derived prompt vocabulary, #1312's autogen-empty CI-guard, ADR-075's `owner_id`-scoping, ADR-072's frontmatter-derive, #1106's MANIFEST-derive. The through-line: **one source projects to the others; drift becomes unrepresentable rather than merely discouraged.** This is the coherent architectural identity of the alpha foundation and is worth naming in the Ship narrative.
- **Contract-drift one layer down** (#1332 root cause): `Intent.original_message` was never set by any classifier path while two reader populations diverged (attribute vs `context["original_message"]`) — the same class ADR-077 prevents, applied to a value rather than an action name. Folded into ADR-077's motivation; the lesson generalizes (SSOT+derive applies wherever a value has multiple readers).
- **Self-attribution drift** (my own, 7/4–7/5): after a context gap, unexplained state (fresh commits, a self-bumped cron-id) got mis-attributed to a phantom peer session. Root cause diagnosed by CIO; durable guardrails shipped (CLAUDE.md compaction-recovery default + duty-cycle cron-change logging). A genuine methodology finding, not just an incident — the honest recovery is itself a trust artifact.

## §4 — What's still open

- **#1383** (Notion/Calendar per-user creds) — tracked-not-gating; the connector-framework migration continues.
- **Connector-framework interface-conformance debt** — Slack (wrong base package) + Notion (`connect()->bool`) still to migrate to the #1232 contract; month-scale, distinct from the (shipped) beta per-user-github requirement. Scope distinction flagged to PPM 7/4.
- **#1322** MCP query-router cutover (real transport reaching the main consumer) — sequencing ruled, Lead-owned; the closing move that makes `simulation_mode` unreachable from prod config.

## §5 — Cross-role threads

- **Lead** — the author/ratify seam *was* the core working relationship this window; it ran honest in both directions and is the mechanism the whole foundation shipped through.
- **HOST** — trust-lenses folded into ADR-075 + ADR-076; #1331 floor-voice and #1333 transparency compose cleanly with my rulings (no build fork).
- **CXO** — Colleague Test voice + ADR-075 OQ-3 neutral-default copy.
- **CIO** — self-attribution-drift diagnosis + guardrails; ongoing watchdog-tuning thread (a morning-first-fire false-positive surfaced 7/10, just outside window).
- **PPM** — beta-scope connector corollary (don't conflate full-8-migration with beta requirement).

## §6 — For PM / exec consideration

- **Ship-narrative through-line**: the alpha's security / privacy / routing foundation is *coherent-by-construction*. Three ADRs decided the per-user-scoping, load, and routing questions **once**, and the builds are verified conformant to those decisions. The strongest single beat is **#1366 closed impossible-by-construction** — a privacy boundary where the leak isn't merely fixed but *unrepresentable* (no code path can express an unscoped read). That's a sharper, more honest claim than "we fixed the bug."
- **Honest-limitation beat** (if the Ship touches duty-cycle mechanics): the self-attribution-drift incident is worth a candid line — a real failure mode surfaced, owned, root-caused, and fixed with durable guardrails. The recovery is a trust story, not a blemish to hide.
- No framing risk flags. Every §0 claim is grounded in decisions.log + the ADR files + closed GitHub issues (#1283, #1312 closed; ADRs 075/076/077 ACCEPTED).

— Arch
*Friday, July 10, 2026 · 10:00 PT*
