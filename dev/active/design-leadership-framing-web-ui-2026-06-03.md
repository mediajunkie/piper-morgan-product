# Design-Leadership Framing — The Web UI We're Proud Of (v0.1)

**Owner**: CXO | **Date**: 2026-06-03 | **Status**: DRAFT v0.1 — **prep scaffold for a PM working session**, not a finished frame. Positions below are *starting points* for PM to push on; the open questions (§6) are the actual agenda.

**Purpose**: Give PM + CXO (+ Lead Dev as build-side counterpart) a written frame to scope the design-leadership response to the two standing questions, rather than scoping from a blank page. PM chose: draft this first (A), then talk it through.

---

## 1. The two questions (PM's framing)

1. **Competitive baseline** — *Can we get the UI at least as good as any generic AI/chat product?* — with the Piper-shaped nuance that "as good as" can't just mean parity with ChatGPT/Claude.ai, because those don't cover Piper-specific surfaces (memory, lifecycle indicators, integration awareness, trust/audit).
2. **Last-mile execution** — *Can we close the last mile on the MUX work to make a web UI we're proud of?* — PM: *"a lot of that work is partly done but I need design leadership to make it happen."*

These are really **"where are we?"** (Q1 = assessment: where's the bar, how far below it are we) and **"how do we finish?"** (Q2 = plan: sequence the last mile). That's why **assessment-before-plan** is the right ordering — you can't sequence the finish until you've measured the gap.

**#1142** (Lead Dev's UI-vs-architecture-mismatch audit, M3) is the evidence base for both — the first hard data on how far the *delivered* UI has drifted from the architecture and from the bar.

## 2. Defining "the bar" (Q1 made concrete)

"As good as a generic chat product, Piper-shaped" decomposes into two tiers. **The bar is both — Tier 1 is necessary, Tier 2 is the reason we exist.**

**Tier 1 — generic-chat-UI table stakes** (what ChatGPT / Claude.ai / Gemini all do; we should simply match):
- Clean conversation thread; correct rendering of markdown, code, artifacts
- Responsive input; streaming; stop / regenerate / edit
- Conversation history + session management (reachable, searchable)
- Discoverable affordances (what *can* I do here?); no dead ends or URL-only pages
- Consistent visual system + navigation across every surface
- Graceful loading / error / empty states

**Tier 2 — Piper-specific surface quality** (the differentiators generic chat UIs *don't have*; ours have to be genuinely good, not merely present):
- **Memory** — what Piper knows about you/your work, visible and inspectable
- **Lifecycle indicators / experience phrases** — work-state surfaces (standup, etc.)
- **Integration awareness** — what's connected (GitHub/Calendar/Notion/Slack), what Piper can see
- **Trust / audit transparency** — why Piper did X (Surface 7 audit-envelope read)
- **The MUX surface set** (Surfaces 1–7) at the v0.2 design intent we've already specified

**Starting position (push on this):** the trap is chasing Tier-1 parity and under-investing in Tier 2. Tier 1 is table stakes — get to "fine" and stop. Tier 2 is where "proud of" actually lives, because it's the only part a generic chat product *can't* copy. The bar for Tier 2 should be *higher* than "as good as generic chat," because there's no generic baseline to be "as good as."

## 3. The assessment lens — we already built the instrument

The **#683 two-layer DoD** that landed today *is* the assessment vocabulary:
- **Layer A — reachability:** can a real user reach the surface, and does the real behavior fire? (Consumer-Trace.)
- **Layer B — quality-of-encounter:** once reached, does the experience meet the bar (Tier 1 + Tier 2)? (Colleague Test / branched rubric + MUX-doc conformance.)

**#1142 already shows we're failing both layers**, which is why the UI doesn't feel finished:

| #1142 finding | Layer A (reachable?) | Layer B (meets bar?) |
|---|---|---|
| Lists view (#714) — no UI route | ✗ unreachable | — |
| Insight Journal (#1031) — URL-only; `/insights` broken | ✗ | — |
| Insight Journal — bare `confirm()`, off-site styling, no nav | (loads) | ✗ Tier-1 fail (table stakes) |
| Insight Journal — "Correct" / "That's right" labels | (wired) | ✗ Tier-2 fail (clarity) |
| Standup (#704) — legacy button; lifecycle indicators don't render | ✗ | ✗ Tier-2 fail (the differentiator isn't even visible) |

The pattern: **we're below the bar on both tiers, on both layers.** Some are table-stakes misses (Tier 1: styling, nav, dead ends); some are the Piper differentiators not landing (Tier 2: lifecycle indicators, memory surfaces). The two-layer lens lets us tell them apart and prioritize.

## 4. The flow — assessment → plan

**Step 1 — Assessment (where are we):** one pass over every served UI surface, scoring each on Layer A (reachable?) and Layer B (meets which tier of the bar?). Output: a **ranked distance-to-bar map** — every surface, its gaps, tagged Tier-1-table-stakes vs Tier-2-differentiator and reachability vs quality.
- Lead Dev's #1142 functional audit is the **Layer A** input (what's reachable / wired / stale).
- CXO adds the **Layer B** experience-quality read on top (does the reachable surface meet the bar).
- These compose: #1142 + CXO Layer-B pass = the full gap map.

**Step 2 — Plan (how we finish):** from the gap map, sequence the last mile. Starting position on sequencing:
1. **Reachability (Layer A) blockers first** — a surface you can't reach can't be used *or* assessed; these are also the cheapest "feels broken" wins.
2. **Tier-1 table-stakes** on the core conversation flow — the surface everyone hits; parity here is the floor.
3. **Tier-2 differentiators** on the highest-value surfaces — where "proud of" is won; design-led, not just wiring.
4. **Standing gate:** apply the #683 two-layer DoD going forward so this drift can't silently re-accumulate. (The discipline that prevents #1142 from recurring.)

## 5. What design-leadership means here (the Q2 "I need design leadership" ask)

Concretely, the things I'd own as CXO across this arc:
- **The bar definition** (§2) — make it explicit and testable, so "proud of" isn't a vibe.
- **The Layer-B experience-quality assessment** — the read #1142 doesn't cover.
- **Per-surface design intent** — extend the MUX-doc discipline (already proven on Surfaces 2/4/7) to the surfaces that don't have it yet, at whatever weight each needs.
- **A coherent visual + interaction system** — the "consistent across every surface" Tier-1 item is a design-system question, not a per-page one (the Insight-Journal-styled-unlike-the-site finding is the symptom).
- **Voice across surfaces** — the CXO→Comms cadence, applied to UI text (labels, empty states, errors), so the "Correct/That's right" class of failure doesn't happen.

Lead Dev is the build-side counterpart; PM sets scope + priority + the "proud of" bar.

## 6. Open questions for the working session (the actual agenda — PM to shape)

1. **Scope** — which surfaces are in-scope for "the web UI we're proud of"? All 7 MUX surfaces, or the core conversation + a chosen few? (Drives how big the assessment is.)
2. **Bar calibration** — is "as good as generic chat" the ceiling, or do we aim *higher* on the Tier-2 Piper surfaces? (My lean: higher on Tier 2; "fine" on Tier 1.)
3. **Assessment depth** — full all-surface audit before any fixing, or assess-and-fix-highest-priority in parallel? (My lean: one lightweight-but-complete scoring pass → ranked map, then parallelize fixes; don't deep-audit every surface before moving.)
4. **Division of labor** — #1142 (Lead) = Layer A; CXO = Layer B. Is that split right, and does the Layer-B pass want PM in the loop on bar-calibration per surface?
5. **"Proud of" success criterion** — what does done look like? (Candidate: every in-scope surface passes the #683 two-layer DoD + a specific end-to-end demo flow that *feels* good. Needs PM's definition.)
6. **Sequencing against M2/M3** — #1142 is M3; how does this design-leadership arc interleave with the milestone plan?

---

## Canonical references
- PM's two questions: handoff `dev/active/cxo-handoff-to-successor-session-2026-06-02.md` §2 Thread 2
- #1142 + discovered-work: Lead memo `mailboxes/cxo/read/memo-lead-to-cxo-cc-pm-ui-architecture-mismatch-discovered-during-m2-smoke-2026-06-02.md`; #1133/#1134/#1132
- #683 two-layer DoD (the assessment instrument): `docs/internal/development/interface-verification-dod-layer-a.md` + `experience-verification-dod-layer-b.md`
- Experience philosophy: PDR-004 `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- MUX surfaces (v0.2 design intent): `docs/internal/design/mux/surface-{2,4,7}-*.md`
- Colleague Test rubric (Layer-B scorer, v2.3.2): `docs/internal/testing/colleague-test-rubric.md`
- PDR-005 §experience (EC-1..EC-5): `dev/active/PDR-005-bring-your-own-chat-draft-v0.6-2026-06-03.md`

*Draft v0.1 — CXO, 2026-06-03. Next: PM working session to push on §2 (the bar) and resolve §6 (the open questions), then I revise to v0.2 and we start Step 1 (assessment).*
