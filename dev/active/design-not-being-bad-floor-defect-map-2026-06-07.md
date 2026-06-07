# "Not Being Bad" — Floor-Defect Remediation Map (v0.1)

**Owner**: CXO | **Date**: 2026-06-07 | **Status**: DRAFT v0.1 — the remediation backbone for the not-being-bad track. The tracking backbone for the epic (pending PM's structure decision). Built by synthesizing three sources per the forensic discipline.

**Sources synthesized**: (1) the #1142 UI Functional Audit (`docs/internal/audits/ui-functional-audit-2026-06.md`); (2) the design-system + conformance standard (`design-system-and-conformance-standard-2026-06-07.md`); (3) *to fold at the Lead sync* — the Nov-2025 UX audit (`docs/internal/design/audits/2025-11-ux-audit/`).

---

## 0. The key distinction this map exists to fix

The **#1142 audit was a Layer-A (functional/reachability) audit** — verdicts are WIRED / STALE-UI / PLACEHOLDER / BUG and nav LINKED / ORPHAN / GATED. Its dispositions are all reachability/wiring:

- **#1146** NAV-WIRE-ORPHAN-PAGES — **CLOSED** (wired the 15 orphans incl. `/insights`, `/transparency`, `/files`, integrations).
- **#1147** `/documents` trust_stage bug · **#1148** UAT test-user-stage · **#1149** debug-route exposure.

**So Layer A (reachability) is tracked and largely done.** What is **NOT tracked anywhere** is the **Layer B craft + conformance** remediation — the actual "not being bad" work beyond "can you reach it." Those defects live only in PM's smoke notes + my standard. **This map is that missing Layer-B backbone.** It complements the #1142 reachability spin-offs; it does not duplicate them.

## 1. Remediation tiers (execution order — leverage-first)

### Tier F — Foundational components (do first; each retires a *whole class* of defects)

| ID | Work | Retires (defect class) | Standard | Source |
|---|---|---|---|---|
| **F1** | **Dialog/Modal component** (token-styled overlay, focus-trap, ESC-close) | Native browser `confirm()` everywhere (Insight-Journal delete; audit any other native dialogs) | S1(b) | PM smoke; #1134-adjacent |
| **F2** | **Consistent page-shell + nav-chrome** (every page in one shell drawing from tokens) | "Styled unlike the rest of the site" (Insight-Journal isolation) — *distinct from #1146, which added nav links but not shell consistency* | S1(b) | PM smoke; #1142 |
| **F3** | **Token-discipline + CI lint gate** (no hardcoded color/space/type; grep/lint at CI) | Hardcoded-value drift across all surfaces (the root of craft inconsistency) | S1(a) | tokens.css; standard |

### Tier C — Chat-page paradigm conformance (first surface target)

| ID | Work | Defect | Standard |
|---|---|---|---|
| **C1** | **Chat-page conformance**: bottom-anchored input, expand-on-type, full-height conversation, multi-conversation nav, emergent tools | Window "hangs unanchored, arbitrarily limits the view" (default-on-login) | S2 (conform to dominant paradigm) |

### Tier S — Per-surface craft remediation (apply standard surface-by-surface)

| ID | Work | Defect | Standard | Source |
|---|---|---|---|---|
| **S1** | `/standup` craft refresh — replace legacy generate-button; render lifecycle indicators | STALE-UI (already tracked #704/#1047 — this is the *craft* half) | S1 | #1142 finding 3 |
| **S2** | Response-label clarity — fix indistinguishable labels | "Correct" / "That's right" semantically identical | S1 (clarity) | PM smoke |
| **S3** | Insight-Journal re-pass — after F1+F2 land, re-score the canonical multi-defect surface | bare confirm() (→F1) + off-site styling (→F2) | S1 | PM smoke; #1142 |
| **S4** | Capability-honesty pass — surfaces that *claim* but don't deliver | `/account` nav-linked but "Coming Soon" (Pattern-064 felt-shape risk); CRUD stub buttons on `/todos`/`/projects` that don't work | S1 (don't show controls that don't work) + EC-2 (don't claim what you can't honor) | #1142 findings 5, 6 |

## 2. Explicitly OUT of floor scope (so the floor is bounded)

- **PLACEHOLDER pages** (`/settings/privacy`, `/settings/advanced`, `/settings/projects`, `/personality-preferences`) — genuinely unbuilt; that's *product roadmap* (PPM), not craft-floor. (The *honesty* of how they're presented IS floor — see S4 — but building them is not.)
- **Slash-parity** — #1142 found it aspirational; treat as a deliberate per-surface design question (low priority), not a floor mandate.
- **Per-endpoint data correctness** — the audit verified the SPA pattern, not each `/api/v1/*` payload; that's a deeper QA follow-up, not craft-floor.

## 3. Each item's gate

Every Tier-F/C/S item ships behind the **#683 two-layer DoD**: Layer A (reachable — mostly satisfied by #1146) + Layer B (passes the design-system + conformance standard, scored by the Colleague Test / UI Lifecycle Verification Rubric).

## 4. Proposed tracking structure (pending PM's epic-shape + milestone decision)

- **Epic**: "not being bad" floor remediation → holds Tiers F/C/S.
- **Children**: F1, F2, F3 (foundational); C1 (chat-page); S1–S4 (per-surface). ~8 child issues.
- **Sequence Lead follows**: F (components) → C1 (chat-page) → S (per-surface). F-tier first because it retires defect *classes* cheaply.
- **Backbone**: this map. As surfaces are remediated, items check off here; the map stays the single comprehensive view.
- **Milestone**: M3 candidate (where #1142's reachability work lives) — but PPM owns the call.

## 5. Open / to reconcile at the Lead primitives-sync

- **Fold the Nov-2025 UX audit** findings into Tier S (it likely catalogued craft inconsistencies — don't re-derive).
- **F1/F2 primitives** (Dialog API + page-shell structure) — the 20-min align Lead requested before building.
- **Scope of F3's lint gate** — which hardcoded-value patterns it catches.

---

## TRACKED (2026-06-07, PM-ratified)
- **Epic #1169** — DESIGN-FLOOR (this map operationalized).
- **F1 #1170** (Dialog) · **F2 #1171** (page-shell) · **F3 #1172** (token-lint) · **C1 #1173** (chat-page conformance) — filed.
- **S1–S4** — defined here; filed as Lead reaches them.
- Milestone M3 — PM assigns on the project board (sprint metadata is board-level).

*Draft v0.1 — CXO, 2026-06-07. The comprehensive remediation backbone; now operationalized into the epic + Tier-F/C children. Layer-A reachability (#1146 etc.) tracked separately; this is the Layer-B craft+conformance complement, and it stays the single comprehensive steering view.*
