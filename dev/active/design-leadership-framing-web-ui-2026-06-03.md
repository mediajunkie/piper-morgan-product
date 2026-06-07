# Design-Leadership Framing — The Web UI We're Proud Of (v0.3)

**Owner**: CXO | **Date**: 2026-06-03 (v0.1) → 06-03 talk-through (v0.2) → 2026-06-06 PM working session (v0.3) | **Status**: DRAFT v0.3 — captures the 2026-06-06 PM session. The model is settled; open items are now execution-scoping, not framing.

**Purpose**: The design-leadership response to PM's two standing questions (competitive baseline + last-mile MUX execution), as a shared operating model for CXO (design-lead) + Lead Dev (build) + PM (watches the unique-value surfaces).

---

## 1. The model in one picture

PM's two aspects — **"not being bad"** and **"being good"** — are **two different kinds of work**, run differently, governed differently:

| | **"Not being bad" (the floor)** | **"Being good" (the ceiling)** |
|---|---|---|
| What it is | Not looking amateurish | Trusted-colleague UX; our unique value |
| Nature | Objective, checklist-able | Taste + product design; not checklist-able |
| Method | Remediation + a design system; conform to known paradigms | Bespoke UX product design, surface by surface |
| Governance | **Job one — build it now.** Delegable: CXO sets standard, Lead executes. Doesn't need PM's close watch. | **PM watches this.** CXO leads with PM oversight; *not* off-the-shelf patterns. |
| Pace | Now, in parallel | Deliberate — "think hard and long about where to innovate" |
| "Done" | Reached when it matches the bar — you stop | Has no natural floor (see bounding discipline §4) |

**These are kinds of work, not buckets of surfaces.** Most surfaces have both — the chat page needs "anchor the window properly" (not-being-bad) *and* "how memory/relevance surface here" (being-good). We assess each surface on both, and sequence **not-being-bad before being-good within each surface**.

## 2. "Not being bad" — two standards

**Standard 1 — general web craft (applies everywhere, unconditionally):** crisp professional web design; a well-considered design system; page grid; typographic rhythm; looks current; performant; renders progressively; follows web standards; supports WCAG/accessibility; legible to *both* LLMs (and people getting help that way) *and* people directly. This is the craft floor under every surface.

**Standard 2 — paradigm conformance (applies wherever a dominant paradigm exists):** *follow the dominant paradigm unless we have a real, documented reason to deviate.* For solved problems — chat window, message rendering, conversation history/nav — Claude / ChatGPT / Gemini have converged; we conform and only diverge with a stated reason. We don't need to innovate on "chat window + multi-chat nav"; we need to not execute it amateurishly.

## 3. The dividing line — does a dominant paradigm exist?

This single question routes a surface to the right track:

- **A dominant paradigm exists** (chat input, message rendering, history nav) → "not being bad," Standard 2: conform, well. Deviate only with a real reason.
- **No dominant paradigm exists** (memory surfacing, lifecycle indicators, integration-awareness, trust/audit, cross-surface relevance) → there's nothing to conform *to*. This is "being good" territory by definition — the trusted-colleague paradigm is **ours to define**, and it needs real product design, **not an off-the-shelf pattern grabbed off the rack.**

The failure modes the dividing line guards against, both ways:
- **Under-conforming**: reinventing a solved chat-element instead of matching the convention (amateurish deviation).
- **Off-the-shelf-on-the-bespoke**: grabbing a generic pattern for a no-paradigm surface that actually needs bespoke UX (PM's "not just off-the-shelf patterns").

## 4. "Being good" — MUX, the unique value proposition

This is *why we did the MUX modeling*: the **trusted-colleague paradigm** — UX that surfaces what's relevant and shows up where the user is, across multiple surfaces. "Being good" is the innovative work where no "good enough" paradigm yet exists. (Chat example: "can we be cooler — prompt Piper to generate interesting GUIs on the fly?" — sure, but *first* make text chat work the way people expect, per §2.)

**Bounding discipline (because taste has no natural floor):** each "being good" bet carries —
1. a **hypothesis** — what relevant thing it surfaces that the user would otherwise miss;
2. a **pass-test** — does it actually feel like a trusted colleague did it (the Colleague Test).

This keeps "being good" from becoming infinite polish; every "cooler?" has a *why*, a *for whom*, and a *how we know it landed*.

## 5. Sequencing + governance

- **"Not being bad" is job one — designed + built now, in parallel,** while we think long and hard about where to innovate. CXO sets the standard (design system + paradigm conformance); Lead executes. Doesn't need PM's close watch.
- **"Being good" is PM-watched and deliberately paced.** CXO leads the UX product design; PM watches the MUX / unique-value surfaces to ensure they get real product design, not off-the-shelf patterns. The cool stuff is *earned on top of* a baseline that isn't embarrassing.

## 6. The assessment instrument — we already built it

The **#683 two-layer DoD** is the measuring tool:
- **Layer A — reachability** (Consumer-Trace: can a real user reach it; does the real behavior fire).
- **Layer B — quality-of-encounter** (Colleague Test / branched rubric + MUX-doc conformance) — now scored against the §2 standards (craft + paradigm conformance) for the floor, and the §4 trusted-colleague bar for the ceiling.

**#1142 is the first data and the worked example of why two layers + two standards:**

| #1142 finding | Track / standard it fails |
|---|---|
| Chat window hangs unanchored, arbitrarily limits the view | Not-being-bad / Standard 2 (deviates from the dominant chat paradigm with no reason) |
| Insight Journal styled unlike the site; bare browser `confirm()` | Not-being-bad / Standard 1 (craft floor — design system, no native dialogs) |
| "Correct" / "That's right" indistinguishable labels | Not-being-bad / Standard 1 (clarity) |
| Lists view unreachable; `/insights` broken | Layer A reachability (precondition to assessing either standard) |
| Lifecycle indicators don't render (Standup) | Being-good not landing — the differentiator isn't even visible |

## 7. The flow

- **Step 1 — Assessment (where are we):** one pass over every served surface; for each: Layer A (reachable?) + route via the dividing line (§3) + score the applicable standard(s). Output: a ranked distance-to-bar map tagged by track + standard. Lead's #1142 audit is the Layer-A + general-craft input; CXO adds the experience-quality + paradigm-conformance read. **This can start now on the not-being-bad axis** (job one; doesn't wait on the being-good/PM-paced decisions).
- **Step 2 — Plan (how we finish):** (1) reachability blockers first; (2) the "not being bad" floor (Standard 1 craft + Standard 2 conformance) — build now, in parallel, delegable; (3) the "being good" surfaces — PM-watched, deliberately paced, real product design; (4) standing gate: the #683 two-layer DoD applied going forward so this drift can't silently re-accumulate.

## 8. Open items (now execution-scoping, not framing)

- **Q-B "being good" scope** (which Piper surfaces, in what order) — PM-watched; to scope as the not-being-bad track proceeds.
- **"Proud of" success criterion** — candidate: every in-scope surface passes the #683 two-layer DoD + one end-to-end demo flow that *feels* good. Needs PM's definition.
- **Sequencing against M2/M3** — #1142 is M3; how the design-leadership arc interleaves.
- **The chat page** is the obvious first not-being-bad target (Standard-2 defect, #1142-flagged, high-traffic — it's the default on login).

---

## Canonical references
- PM's two questions + the 2026-06-06 working session (the §1–5 model is from it): this doc's provenance.
- #1142 + discovered-work: `mailboxes/cxo/read/memo-lead-to-cxo-cc-pm-ui-architecture-mismatch-discovered-during-m2-smoke-2026-06-02.md`; #1133/#1134/#1132.
- #683 two-layer DoD (assessment instrument): `docs/internal/development/interface-verification-dod-layer-a.md` + `experience-verification-dod-layer-b.md`.
- Experience philosophy: PDR-004 `docs/internal/product/pdrs/pdr-004-experience-philosophy.md`.
- MUX surfaces (the "being good" substrate): `docs/internal/design/mux/surface-{2,4,7}-*.md`.
- Colleague Test rubric (the "being good" pass-test, v2.3.2): `docs/internal/testing/colleague-test-rubric.md`.
- PDR-005 §experience (EC framework): `dev/active/PDR-005-bring-your-own-chat-draft-v0.6-2026-06-03.md`.

*Draft v0.3 — CXO, 2026-06-06 (PM working session). Next: scope Step-1 assessment on the not-being-bad axis (job one; chat page first), in parallel with PM-paced "being good" surface scoping.*
