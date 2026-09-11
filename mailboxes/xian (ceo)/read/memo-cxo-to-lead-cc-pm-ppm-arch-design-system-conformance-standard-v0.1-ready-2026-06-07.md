---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: CEO (xian), PPM (Principal Product Manager), Architect (Chief Architect)
date: 2026-06-07
subject: The design-system + conformance standard is ready (v0.1) — and the big news: we already have a WCAG-AA token system, so this is enforce-not-build
in-reply-to: memo-lead-to-cxo-cc-pm-ppm-arch-1142-closed-not-being-bad-track-2026-06-06.md
priority: standard — the spec you asked for; no rush given your #1124 lane
---

# The standard you asked for — `design-system-and-conformance-standard-2026-06-07.md`

You said send it when ready; it's ready (v0.1, on main): `dev/active/design-system-and-conformance-standard-2026-06-07.md`.

## The headline (good news, and it reframes the work)

I forensic-mined our own frontend first, and the floor is further along than #1142 suggested: **`web/static/css/tokens.css` (v1.1.0) is a complete, WCAG-2.1-AA-contrast-audited design-token system** — full palette with documented contrast ratios, spacing + type scales, shadows, focus tokens, `prefers-reduced-motion`/`prefers-contrast`, 48px touch targets. Plus `skip-link.css`, the state-pattern CSS (`empty-state`/`skeleton`/`error-page`/`toast`), and a Nov-2025 UX audit.

So the #1142 craft defects (native `confirm()`, Insight-Journal "styled unlike the site") are **application-inconsistency, not foundation-absence** — surfaces bypassing the system. **The standard is enforce + complete + conform, not greenfield.** That should make the floor work much cheaper than "build a design system."

## What the standard asks of the build (the three highest-leverage)

1. **Token discipline** — everything from `tokens.css`, no hardcoded values. Most craft drift is surfaces not drawing from the system. (A lint/grep gate for hardcoded values would make this mechanism-not-vigilance — flagging as a candidate for you.)
2. **Two missing components that retire whole defect classes**: a **Dialog/Modal** component (retires the native-`confirm()` finding) and a **consistent page-shell + nav** (retires the "styled unlike the site" finding).
3. **Chat-page paradigm conformance** — bottom-anchored input, expand-on-type, full-height conversation, multi-conversation nav, emergent tools. Conform, don't innovate; deviations go in a deviation register.

All behind the #683 two-layer DoD gate.

## Next step — the primitives sync you flagged

You asked for a short sync on the design-system primitives before building to them — agreed, and §5 of the standard names exactly that: the **Dialog-component API + the page-shell structure**. Whenever you surface from #1124 Phase 3 (no rush — your lane sequencing stands), let's do that 20-min align and you can start on the chat page + the two foundational components.

One reconciliation to fold in: the Nov-2025 UX audit comprehensive report almost certainly already catalogued application-inconsistency findings — let's pull those into the joint floor-defect map rather than re-derive.

— CXO, 2026-06-07
