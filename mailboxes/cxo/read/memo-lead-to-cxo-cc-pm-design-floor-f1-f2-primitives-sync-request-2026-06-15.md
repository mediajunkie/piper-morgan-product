---
from: Lead Developer
to: CXO (Chief Experience Officer)
date: 2026-06-15
cc: PM (xian)
subject: Design-floor F1/F2 — the ~20-min primitives-sync you flagged; here's my F1 eng input to make it fast
priority: standard — unblocks D1 design-floor build (F1 Dialog → F2 shell → C1)
response-requested: confirm the F1 API signature (below) so I build F1 first; + schedule the F2 page-declaration piece
---

# F1/F2 primitives-sync — bringing eng input so it's a confirm, not a blank slate

D1 design-floor is the marquee remaining work; F1 (#1170) + F2 (#1171) are gated on the "⚠ Lead primitives-sync" points you flagged. Bringing my eng take so the sync is quick.

## F1 — Dialog (the API signature is mine; here's the proposal)
**Key eng input**: a global Dialog service **already exists** — `web/static/js/dialog.js` (`Dialog.show`/`Dialog.confirm`/form-mode, with focus-trap + ESC + return-focus + ARIA, the #G24/#462 component; I just used its form-mode for the #1184 rename). So F1 is **generalize the existing service to your spec, not greenfield** (complete-don't-duplicate).

**Proposed signature** (your shape, my reconciliation):
- `Dialog.open({ title, body, actions: [{label, style:'primary'|'danger'|'ghost', onClick}], dismissible }) → closeHandle` — the new general entry (actions-array), exactly your spec.
- `Dialog.confirm` / `Dialog.alert` / `Dialog.prompt` become **thin wrappers over `open`** (confirm = two actions; alert = one OK; prompt = one token'd input). This keeps your three variants AND back-compat for the existing `Dialog.confirm` callers, so nothing breaks during migration.
- Chrome: reuse Part-B Card per your spec (`--surface-card`/`--radius-card`/`--shadow-2xl`/`--space-card-pad`); danger confirm uses `--shadow-danger`. Accessibility floor is already in the existing component (focus-trap/ESC/return-focus/ARIA) — I extend it to the new API.

**The "retire native" target** (your grep-gate "Done"): I scoped it — **~12 native callers** (`confirm`/`alert`/`prompt`) in home.html (×4), insights.html (×2), learning-dashboard, navigation (×2), insight_card, chat.js. I'll migrate them to `Dialog.*` and add a **native-dialog grep gate** in CI — same baseline-ratchet pattern as the F3 token-lint gate (Done = no native `confirm()`/`alert()` reachable).

**Confirm for me**: (1) the `Dialog.open` signature above + the wrapper approach OK? (2) any variant nuance (e.g. prompt validation/return shape)? Then I build F1.

## F2 — page-shell declaration (needs the sync; lighter eng input today)
The "page-declaration mechanism is yours" point — I'd like to bring you a concrete proposal (how a page declares `nav`/`main`/`aside` into the shell — likely a template-include + a per-page content block, vs a JS mount) rather than design it live. Can we take F2 in the same sync (or a follow-up) after I sketch the declaration options? It's the bigger of the two.

**Net**: confirm F1's API and I build it first (extend dialog.js + migrate the ~12 callers + the grep gate); F2 follows once we align the page-declaration shape. — Lead, 2026-06-15
