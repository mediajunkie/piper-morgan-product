# Design-System + Paradigm-Conformance Standard (v0.1)

**Owner**: CXO | **Date**: 2026-06-07 | **Status**: DRAFT v0.1 — the "not being bad" spec Lead Dev builds to (per the 6/6 division: CXO sets the standard, Lead executes against it).
**Parent**: `design-leadership-framing-web-ui-2026-06-03.md` v0.3 (Standard 1 = general web craft; Standard 2 = paradigm conformance).
**Audience**: Lead Dev (build); cc PPM/Arch.

---

## 0. Forensic finding — we already have the foundation (this is consolidate-and-enforce, not greenfield)

Investigating our own frontend first (per the extend-existing discipline), the floor is **further along than #1142 suggests**:

- **`web/static/css/tokens.css` (v1.1.0) is a real, WCAG-2.1-AA-contrast-audited design-token system** — full color palette with documented contrast ratios (decorative-vs-text split), a spacing scale, typography scale, shadows, border-radius, z-index layering, focus-state tokens, and accessibility tokens (`--touch-target-min: 48px`, `prefers-contrast: more`, `prefers-reduced-motion`). Plus utility classes.
- **Accessibility primitives already exist**: `skip-link.css`, `hover-focus-states.css`, the focus-outline token, the audited contrast.
- **State-pattern CSS exists**: `empty-state.css`, `skeleton.css`, `spinner.css`, `toast.css`, `error-page.css`, `form-validation.css`.
- **A Nov-2025 UX audit exists**: `docs/internal/design/audits/2025-11-ux-audit/` (comprehensive report + phase-4 gap analysis) — prior findings to reconcile against.

**Conclusion**: the #1142 craft defects (native `confirm()` dialog, Insight-Journal "styled unlike the site") are **application-inconsistency**, not foundation-absence. Some surfaces *bypass* the token system and the state patterns. **So this standard is: enforce the system we have, complete its missing component patterns, and conform to dominant paradigms — not build a design system from scratch.**

## 1. Standard 1 — general web craft (applies to every surface, unconditionally)

**(a) Token discipline — the design system is `tokens.css`; use it.**
- All color, spacing, type, radius, shadow, z-index, transition values come from `tokens.css` custom properties. **No hardcoded values; no bypass.** A surface that hardcodes is non-conformant even if it looks fine.
- This is the single highest-leverage floor fix: most #1142 craft drift is surfaces not drawing from the token system.

**(b) Component completeness — fill the gaps #1142 exposed.** The token foundation exists; some *components* don't, which is why surfaces reach for native/ad-hoc solutions:
- **A Dialog/Modal component** — to retire native browser `confirm()` (the Insight-Journal delete defect). Uses `--color-overlay-dark`, `--shadow-2xl`, `--z-index-modal`, focus-trap, ESC-to-close. *This is the concrete fix for the bare-`confirm()` finding.*
- **A consistent page shell + nav** — so no surface is "styled unlike the rest of the site" (the Insight-Journal isolation defect). Every page sits in the same shell (header/nav/content), drawing from tokens.
- **Enforce the existing state patterns** — empty / loading (skeleton) / error states use `empty-state.css` / `skeleton.css` / `error-page.css`, not ad-hoc markup.

**(c) Accessibility — maintain the existing bar (it's good; don't regress).** WCAG 2.1 AA (tokens are audited to it), skip-link on every page, visible focus via `--focus-outline`, 48px touch targets, honor `prefers-reduced-motion` + `prefers-contrast`. **The bar is: a new/changed surface must not regress the audited accessibility posture.**

**(d) Craft floor (PM's Standard-1 list).** Well-considered grid + typographic rhythm (the type/spacing scales exist — apply them consistently); looks current; performant; **renders progressively** (skeleton states, no layout-shift); follows web standards (semantic HTML); **legible to both LLMs and people** (semantic structure + ARIA → a screen reader *or* an LLM-helper can parse the page).

## 2. Standard 2 — paradigm conformance (where a dominant paradigm exists)

**The rule (from v0.3):** follow the dominant paradigm unless we have a real, documented reason to deviate. A *deviation register* (one line per deliberate deviation + its reason) keeps "we did it differently" honest.

**First target — the chat page** (default-on-login; #1142-flagged "window hangs unanchored"):
- Conform to the converged chat paradigm: **input anchored at the bottom**, **expands as you type**, **full-height conversation** (not arbitrarily limited), **multi-conversation nav** (sidebar, the established pattern), **tools exposed emergently** (not a fixed toolbar). Claude / ChatGPT / Gemini all converge here.
- The fix is *conform*, not innovate. Any deliberate departure → deviation register with a real reason.
- Built behind the **#683 two-layer DoD** gate (Layer A reachable + Layer B quality-of-encounter).

## 3. How "conformed" is verified (the enforcement mechanism)

A surface passes the not-being-bad floor when:
1. **Token-clean** — no hardcoded values; all from `tokens.css`. *(grep-able / lintable — a candidate automated check.)*
2. **Component-correct** — uses the shared Dialog / page-shell / state components, not native or ad-hoc.
3. **Accessibility-non-regressing** — skip-link, focus, contrast, reduced-motion intact.
4. **Paradigm-conformant** — matches the dominant pattern, or has a deviation-register entry.
5. **Passes the #683 two-layer DoD** — the standing gate.

## 4. How this drives the joint floor-defect map (with Lead)

This standard is the *spec*. Lead executes #1142's ranked defects against it, tagging each **craft (Standard 1) vs. conformance (Standard 2)** and **Layer A vs. B** — producing the ranked floor-defect map. The chat page is item one; the Dialog-component + page-shell are the foundational fixes that retire a whole class of #1142 craft defects at once.

## 5. Open items / for Lead + the short sync

- **Design-system primitives sync** (Lead requested): align on the Dialog-component API + the page-shell structure before Lead builds to them. *(This is the "short sync on primitives" Lead flagged.)*
- **Reconcile with the Nov-2025 UX audit** — its comprehensive report likely already catalogued application-inconsistency findings; fold them into the defect map rather than re-deriving.
- **Token-discipline automated check** — a lint/grep gate for hardcoded values would make Standard-1(a) mechanism-not-vigilance. Candidate for Lead.

## References
- `web/static/css/tokens.css` (v1.1.0, the design system) + `web/static/css/` (state-pattern + a11y CSS).
- Nov-2025 UX audit: `docs/internal/design/audits/2025-11-ux-audit/`.
- #1142 (the ranked floor-defect input, closed 6/6); framing v0.3; #683 two-layer DoD.

*Draft v0.1 — CXO, 2026-06-07. Next: short primitives-sync with Lead (Dialog API + page shell); then Lead executes the floor-defect map against this spec, chat-page first.*
