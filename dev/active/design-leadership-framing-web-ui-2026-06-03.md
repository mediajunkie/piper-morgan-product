# Design-Leadership Framing — The Web UI We're Proud Of (v0.2)

**Owner**: CXO | **Date**: 2026-06-03 (v0.1) → updated post-talk-through (v0.2) | **Status**: DRAFT v0.2 — captures the PM talk-through of 2026-06-03 ~17:20. Two open questions remain (§6) pending PM's answer; everything else reflects where the conversation landed.

**Purpose**: Give PM + CXO (+ Lead Dev as build-side counterpart) a written frame to scope the design-leadership response to the two standing questions, rather than scoping from a blank page. PM chose: draft this first (A), then talk it through.

**PM's crystallization (2026-06-03):** the two aspects, "on a very crude level," are **"not being bad"** and **"being good."** This is the operative language going forward (clearer than the Tier-1/Tier-2 framing it replaces). The talk-through's key finding: *these are two different **kinds** of work* — see §5.

---

## 1. The two questions (PM's framing)

1. **Competitive baseline** — *Can we get the UI at least as good as any generic AI/chat product?* — with the Piper-shaped nuance that "as good as" can't just mean parity with ChatGPT/Claude.ai, because those don't cover Piper-specific surfaces (memory, lifecycle indicators, integration awareness, trust/audit).
2. **Last-mile execution** — *Can we close the last mile on the MUX work to make a web UI we're proud of?* — PM: *"a lot of that work is partly done but I need design leadership to make it happen."*

These are really **"where are we?"** (Q1 = assessment: where's the bar, how far below it are we) and **"how do we finish?"** (Q2 = plan: sequence the last mile). That's why **assessment-before-plan** is the right ordering — you can't sequence the finish until you've measured the gap.

**#1142** (Lead Dev's UI-vs-architecture-mismatch audit, M3) is the evidence base for both — the first hard data on how far the *delivered* UI has drifted from the architecture and from the bar.

## 2. Defining "the bar" (Q1 made concrete)

"As good as a generic chat product, Piper-shaped" decomposes into two aspects — PM's language: **"not being bad"** and **"being good."** **The bar is both — "not being bad" is necessary, "being good" is the reason we exist.**

**"Not being bad" — generic-chat-UI table stakes** (what ChatGPT / Claude.ai / Gemini all do; we should simply match):
- Clean conversation thread; correct rendering of markdown, code, artifacts
- Responsive input; streaming; stop / regenerate / edit
- Conversation history + session management (reachable, searchable)
- Discoverable affordances (what *can* I do here?); no dead ends or URL-only pages
- Consistent visual system + navigation across every surface
- Graceful loading / error / empty states

**"Being good" — Piper-specific surface quality** (the differentiators generic chat UIs *don't have*; ours have to be genuinely good, not merely present):
- **Memory** — what Piper knows about you/your work, visible and inspectable
- **Lifecycle indicators / experience phrases** — work-state surfaces (standup, etc.)
- **Integration awareness** — what's connected (GitHub/Calendar/Notion/Slack), what Piper can see
- **Trust / audit transparency** — why Piper did X (Surface 7 audit-envelope read)
- **The MUX surface set** (Surfaces 1–7) at the v0.2 design intent we've already specified

**Position (talk-through, CXO — PM to confirm calibration):** the trap is chasing "not being bad" parity and under-investing in "being good." "Not being bad" is table stakes — get to "fine" and stop. "Being good" is where "proud of" actually lives, because it's the only part a generic chat product *can't* copy. The bar for "being good" should be *higher* than "as good as generic chat" — there's no generic baseline to be "as good as."

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

## 5. The talk-through's key finding: "not being bad" and "being good" are two *different kinds of work*

This is the most useful thing the framing produced (PM talk-through, 2026-06-03). The two aspects aren't two points on one quality scale — they're two tracks, run differently:

**Track 1 — "not being bad" (a floor).** Mostly *objective*: is the surface reachable, consistent, does it render, no dead ends, no bare browser `confirm()`. **Checklist-able** — the #683 two-layer DoD (Layer A reachability + the table-stakes half of Layer B) basically *is* the checklist. The work is **remediation + a design system** (the "styled unlike the rest of the site" finding is a *consistency* failure → a design-system problem, not per-page). Once the system exists, most of this **parallelizes/delegates**: CXO sets the standard + bar, Lead Dev executes against it. Gate-driven, delegable, finite.

**Track 2 — "being good" (a ceiling).** *Not* checklist-able: "does the memory surface make you feel Piper actually knows you?" has no rubric line — it's taste and design judgment, the part a generic chat product structurally can't copy. The work is **design-led, surface-by-surface, deeper-on-fewer** — the MUX-doc discipline (proven on Surfaces 2/4/7) extended to the surfaces that matter most. CXO leads directly; it doesn't delegate the same way.

**Why the distinction is load-bearing:** the failure mode is *conflating* them — either burning scarce design energy doing "not being bad" by hand surface-by-surface (when it should be a system), or shipping the differentiators half-baked because we treated "being good" as a checklist. Different tracks, different methods, different owners; keep honest about which is which.

**Sequencing (CXO position):** reachability comes first — you can't judge whether the memory surface is *good* if you can't reach it or it's visually broken. So Track-1's floor (esp. Layer A + worst offenders) is somewhat prerequisite to honestly assessing Track 2. They overlap, but the floor enables the ceiling assessment.

## 5b. What design-leadership means here (the Q2 "I need design leadership" ask)

Concretely, the things I'd own as CXO across this arc:
- **The bar definition** (§2) — make it explicit and testable, so "proud of" isn't a vibe.
- **The Layer-B experience-quality assessment** — the read #1142 doesn't cover.
- **Per-surface design intent** — extend the MUX-doc discipline (already proven on Surfaces 2/4/7) to the surfaces that don't have it yet, at whatever weight each needs.
- **A coherent visual + interaction system** — the "consistent across every surface" Tier-1 item is a design-system question, not a per-page one (the Insight-Journal-styled-unlike-the-site finding is the symptom).
- **Voice across surfaces** — the CXO→Comms cadence, applied to UI text (labels, empty states, errors), so the "Correct/That's right" class of failure doesn't happen.

Lead Dev is the build-side counterpart; PM sets scope + priority + the "proud of" bar.

## 6. Open questions — status after the talk-through

**Still genuinely open (the two I asked PM at the end of the talk-through; awaiting answer):**
- **Q-A — Two-track confirmation.** Does the split in §5 feel right — "not being bad" as a system/gate-driven remediation track (delegable), "being good" as a design-led per-surface track (CXO leads directly)?
- **Q-B — "Being good" scope.** Which surfaces are in the "being good" set — all of memory / lifecycle / integration-awareness / trust-audit, or the one or two where it matters most *first*? (Subsumes the old Q1-scope; this is the version that matters once we've split the tracks.)

**Leaning resolved in the talk-through (PM can still push):**
- **Bar calibration (old Q2):** higher than generic-chat on "being good"; "fine" on "not being bad." (PM's "not bad / good" framing essentially endorses this shape; confirm.)
- **Assessment depth (old Q3):** one lightweight-but-complete scoring pass → ranked map, then parallelize fixes. CXO lean; not contested.
- **Division of labor (old Q4):** #1142 (Lead) = Layer A / "not being bad" reachability+remediation; CXO = Layer B / "being good." Maps cleanly onto the two tracks.

**Still to set with PM (lower urgency, after the two above):**
- **"Proud of" success criterion (old Q5):** candidate — every in-scope surface passes the #683 two-layer DoD + one end-to-end demo flow that *feels* good. Needs PM's definition.
- **Sequencing against M2/M3 (old Q6):** #1142 is M3; how the design-leadership arc interleaves with the milestone plan.

---

## Canonical references
- PM's two questions: handoff `dev/active/cxo-handoff-to-successor-session-2026-06-02.md` §2 Thread 2
- #1142 + discovered-work: Lead memo `mailboxes/cxo/read/memo-lead-to-cxo-cc-pm-ui-architecture-mismatch-discovered-during-m2-smoke-2026-06-02.md`; #1133/#1134/#1132
- #683 two-layer DoD (the assessment instrument): `docs/internal/development/interface-verification-dod-layer-a.md` + `experience-verification-dod-layer-b.md`
- Experience philosophy: PDR-004 `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`
- MUX surfaces (v0.2 design intent): `docs/internal/design/mux/surface-{2,4,7}-*.md`
- Colleague Test rubric (Layer-B scorer, v2.3.2): `docs/internal/testing/colleague-test-rubric.md`
- PDR-005 §experience (EC-1..EC-5): `dev/active/PDR-005-bring-your-own-chat-draft-v0.6-2026-06-03.md`

*Draft v0.2 — CXO, 2026-06-03 (post-talk-through). Next: PM answers Q-A (two-track confirmation) + Q-B ("being good" scope); then I revise to v0.3 and we start Step 1 (assessment) on the in-scope surfaces.*
