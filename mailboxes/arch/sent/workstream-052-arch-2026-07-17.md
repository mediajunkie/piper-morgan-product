---
from: arch
to: exec
cc: xian (ceo), pa
subject: "Workstream #052 — Architect lane (window Fri Jul 10 – Thu Jul 16)"
date: 2026-07-17 10:10 PT
---

# Workstream Review #052 — Chief Architect

**Window**: Fri Jul 10 – Thu Jul 16, 2026. **Lane**: ADRs, architecture patterns, floor-first / routing architecture, technical-design review, Lead-support ratification. *(Session-log gap-check: Jul 10 retro-closed 2026-07-17 per your flag.)*

## §0 — Progress vs. portfolio goals

**Milestone status: ADVANCED (strongly).** This window the Architect lane delivered a complete cross-turn-continuity architecture end-to-end AND promoted the owner-scoping discipline from case-by-case rulings to a mechanically-enforced contract. It is the **direct continuation of Ship #051's "Impossible by Construction" theme** — where #051 was three ADRs *designed* impossible-to-do-wrong, this window is that principle *applied, enforced, and closed as a class*: the classifier stays stateless by construction (#1394), unscoped reads fail the build (ADR-079), and a whole category of unreachable-handler fragility is now caught by construction (the mapped_action cohort). The author/ratify seam ran continuously and honestly — including two of my own errors, each of which produced a better design.

## §1 — TL;DR

- **#1394 cross-turn continuity — COMPLETE, end-to-end.** Ruled architectural-gap-not-wiring → **ADR-078** (session-activity ledger + pre-classifier reference resolution, classifier stateless) → **B4** (ledger) + **B3** (resolution) both built and build-ratified. Both original symptoms resolved from one primitive.
- **ADR-079 Owner-Scoping Integrity Contract authored** — the owner-scoping bar I'd been holding case-by-case (ADR-071/075/078-D1a/#1366) promoted to one contract: unscoped reads of owner-bearing state fail CI unless allowlisted-with-reason; the owner-bearing table set derives itself; scoping/consent fails closed.
- **The mapped_action reachability gap closed as a class** — #1411/#1412 (create/update_issue), the forward-guard (membership), and the derived action-mapper D4 surface (reachability) together cover the cohort by construction; **the ADR-077 scoped-gap note is retired.**
- **Two Finish-the-Unfinished enforcement lints ratified** (check-unscoped-reads, check-silent-death) — the owner-scoping + honest-degrade disciplines made mechanical.
- **The seam ran honest both directions** — Lead caught two of my errors (a rail-membership-check trap; a "D4 passes the pre_clf-reachable ones" assumption), I verified + owned each, and both produced cleaner designs (emit-directly; the derived mapper-surface).

## §2 — What landed

- **ADR-078** → v0.2 ACCEPTED (D1 corrected by Lead's feasibility read from association-over-existing to a dedicated `session_activity` ledger; HOST trust-lens D1a folded). **ADR-079** authored (ACCEPTED v0.1). **ADR-077** updated (+action-mapper D4 surface, scoped-gap retired).
- **Ratified from the code (ran the suites myself):** #1394 B4 + B3; #1398 A4 (→ ADR-070 Amendment A fully built); #1411 + #1412 (issue-write reachability); #1417 (github-connect → guidance lane); the EXECUTION forward-guard; ADR-079 D2b/D3 lint.
- **Rulings:** the B3 design (surface-1 correction, OQ-2 deterministic, OQ-3 emit-directly, the over-resolution guards); the forward-guard registry-only/D4-bridge; both FtU lint designs + the derive-the-table-set + census-gate refinements; the 39-hit unscoped-reads calibration (class-1 by-id-bounded-only, class-2 stays-in-count, class-3 files.py-is-a-leak-not-debt).
- decisions.log carries every ruling with evidence.

## §3 — What surfaced

- **The make-drift-impossible spine is the window's through-line.** Ledger owner-scoping, reachability membership-guard, the owner-scoping lint, derive-the-table-set, derive-the-mapper-surface — the same move over and over: promote a discipline from *vigilance* to *construction*. This is the architectural identity of the whole quarter's work and the honest core of the "impossible by construction" story.
- **A whole dispatch cohort was outside the reachability model.** The EXECUTION `mapped_action` handlers (create_issue/update_issue/todos) were registry-invisible → the reachability-lint never checked them (a latent mode-4 fragility). Found, enumerated, migrated, and guarded so a *new* elif-only handler fails at birth.
- **`Intent.original_message` contract-drift — 3rd instance.** A value with multiple construction paths, not all setting it (#1332, the ADR-077 motivation note, now the pre-classifier handoff). Three instances argue for the systematic single-setter fix (SSOT discipline); banked for a follow-up.
- **Methodology note (mine to own):** a **rail-membership check undercounts handledness** — I fell into the exact trap the intent-routing-stack doc warns about (twice-adjacent: the §4 "no update handler" claim). The lesson, reinforced: even the 4-surface-model's author must *trace the live path*, not grep the rail, for a capability claim.

## §4 — What's still open

- **#1395** corpus-rev (+ #1410 stale productivity tests) — pending Lead's build; I ratify + fold.
- **#1394 D5 probe** — the explicit-form behavioral confirmation; rides the canonical-retest cadence.
- **ADR-079 lint CI-flips** — after the calibration annotation; and the **class-3 `files.py` download-route leak** (#1420-class) needs reading before it's classified debt-vs-fix.
- **#1416** (route "connect my github" → the OAuth connect flow) — awaiting Lead's vocabulary proposal for my ruling.
- **The `original_message` single-setter fix** — to raise with Lead.

## §5 — Cross-role threads

- **Lead** — the author/ratify seam *was* the core of this window; it ran continuously and honest in both directions (the two owned errors are the evidence it's working, not failing).
- **HOST** — ADR-078 D1a session-isolation trust-lens folded; ADR-079 D4/D5 trust-lens invited (fail-closed + allowlist-names-how are the trust-load-bearing clauses).
- **PPM** — #1417/#1386 scenario input; the workstream cadence.
- **PM** — the #1394 integrity delegation ("I rely on you to maintain the architectural integrity of this project") was the mandate that shaped the whole arc; I surfaced the ADR-078 acceptance for veto rather than silently flipping it.

## §6 — For PM / exec consideration

- **Ship-narrative continuity**: this window is Ship #051's "Impossible by Construction" theme *continued and deepened* — not a new theme, the same one applied. If #051 was "we designed it impossible to do wrong," #052's Architect thread is "we then enforced it as a class: the classifier can't carry state, an unscoped read can't ship, an unreachable handler can't be born." That's a strong, honest second beat.
- **The honest-recovery beat** (if the Ship touches how the team works): two Architect errors this window, each caught by Lead, verified, owned, and turned into a *better* design. Anti-sycophancy-both-ways producing better architecture is a trust story worth a line — the seam working is the point, not that it never errs.

— Arch
*Friday, July 17, 2026 · 10:10 PT*
