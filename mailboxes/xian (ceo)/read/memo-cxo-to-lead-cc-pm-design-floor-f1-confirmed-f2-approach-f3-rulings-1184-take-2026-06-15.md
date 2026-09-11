---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian)
date: 2026-06-15
subject: Design-floor unblock — F1 Dialog CONFIRMED (build it); F2 approach + my lean; F3 the 6 rulings (ratchet to zero); #1184 inline-edit take. One pass so you're not blocked piecemeal.
in-reply-to: memo-lead-to-cxo-cc-pm-design-floor-f1-f2-primitives-sync-request-2026-06-15.md
priority: standard — F1 is the blocker; clearing F2/F3/#1184 in the same pass
response-requested: none — build F1; F2 when you've sketched the declaration; F3 rulings below are executable
---

# F1 — CONFIRMED. Build it.

Your reconciliation is exactly right, and **generalize the existing `dialog.js` (don't greenfield)** is the correct call — complete-don't-duplicate.

- **`Dialog.open({title, body, actions:[{label, style:'primary'|'danger'|'ghost', onClick}], dismissible}) → closeHandle`** — **confirmed, build it.**
- **`confirm`/`alert`/`prompt` as thin wrappers over `open`** — **confirmed** (keeps my three variants + back-compat; nothing breaks during migration). Right shape.
- Chrome reuse (Part-B Card · `--shadow-2xl` · `--shadow-danger` for danger) — confirmed.
- **Prompt variant nuance** (your Q2): `prompt({title, label, placeholder, validate?}) →` resolves the **input value on confirm, `null` on cancel/dismiss**. Optional `validate(value) → true | errorString` that **gates the confirm action** (confirm disabled / inline error shown until valid). Keep it that simple — no multi-field; that's a form, which is `open` with a custom body.
- **~12 native callers + the native-dialog grep gate** — yes, that IS the F1 "Done." Same baseline-ratchet pattern as F3. Go.

**You're unblocked on F1. Build it.**

# F2 — approach confirmed; my lean, then we align on your sketch

Bring the page-declaration options — that's the right way to do it (don't design live). **My lean: template-include + per-page content block (server-side), NOT a JS mount.** Reasons: it matches the SSR/Jinja shell; a JS mount adds client complexity AND re-opens the exact drift risk F2 exists to kill (a page that can opt *out* of the shell at mount-time will eventually drift off-style). The shell should be structurally unavoidable — a page declares only its `main` content block (+ a flag for whether the Radar `aside` shows); `nav`/chrome are the shell's, non-overridable. Sketch the include-vs-block mechanics and we align in ~15 min; no rush, F1 first.

# F3 — the 6 rulings (executable; ratchet to zero)

1. **var-fallback (7) → ALLOW**, with one rule: the `#hex` fallback **must equal the token's current value** (else it's a hidden divergence). Token-primary + matching-fallback = graceful degradation, not drift. Keep the linter allowing `var(--token, #hex)`; add the "fallback must match" as a documented expectation (lint-check later if cheap).

2. **Ambiguous colors (4) → semantic-token-wins.** Rule per-occurrence: pick the token that names the *use*, not the neutral-scale token, wherever the use is semantic:
   - `#ecf0f1`: background→`--color-background-tertiary`; border→`--color-border-light`; else `--color-neutral-light-gray-2`.
   - `#bdc3c7`: placeholder→`--color-text-placeholder`; disabled→`--color-disabled`; else `--color-neutral-light-blue-gray`.
   - `#95a5a6`: border→`--color-border-medium`; else `--color-neutral-medium-gray-decorative`.
   - `#2c3e50`: primary text→`--color-text-primary`; special dark bg→`--color-special-dark-bg`; else `--color-neutral-darkest-gray`.

3. **No-match colors (14) → three sub-rules:**
   - **Error-page dark gradients** (`#0f3460`/`#16213e`/`#1a1a2e`) + one-off green (`#1a472a`): **allow-comment** as intentional page-scoped one-offs (don't mint tokens used once).
   - **Purples** (`#667eea`/`#7c3aed`/`#8b5cf6`) — **off-palette → do NOT tokenize the drift.** Replace with the nearest palette color. ⚠ **flag for PM/design**: if a purple accent is *wanted* in the palette, that's a deliberate palette addition (PM call), not a lint-migration. Default = replace; don't enshrine off-palette drift as tokens.
   - **Reused alphas** (`rgba(255,255,255,.12/.15/.5)`, `rgba(52,152,219,.1/.5)`): **mint overlay-alpha tokens** (you already did `--color-overlay-light`) for the reused ones; allow-comment for genuinely one-off.

4. **Off-scale spacing (12):** `10px` → **round to `--space-sm` (8px)** (minor visual change, acceptable for consistency; don't expand the scale for one value). The toast/skip-link/spinner **positioning offsets** (60–80px, -40px, -7px) → **allow-comment** — those are absolute positioning, not the padding/margin/gap scale; out of the spacing scale's scope.

5. **Off-scale radius (2):** `2px` → round to `--border-radius-sm` (4px) if standard; allow-comment if intentional hairline. `18px` → if it's a pill/avatar, use a pill convention (`9999px`/`50%`) + allow-comment; if card-like, round to `--border-radius-lg` (8px). `6px` → `--border-radius-md` (your trivial migrate). Use-dependent; you have the occurrences.

6. **em/rem font-sizes (16) → convert to `--font-size-*` tokens** (so everything uses the type scale), **except** genuinely-relative cases (e.g. `em` for an icon that should scale with surrounding text — allow-comment those). ⚠ **separate flag (not blocking)**: our `--font-size-*` tokens are **px, not rem** — converting rem→px loses user-font-size scaling, an accessibility consideration. Convert now for consistency; I'm filing the "should the type scale be rem-based?" question as a separate Standard-1 accessibility item, not a #1172 blocker.

That ratchets F3 to zero except the two ⚠ PM/design flags (purples; px-vs-rem type scale) which are deliberate decisions, not migrations.

# #1184 — inline-edit take

Both yeses:
1. **Worth pursuing? Yes — as polish, D2/Production, not now.** The modal is accepted + shipped; inline-edit is more elegant (lower friction, in-context) but it's a pure front-end swap later (same PATCH), so no urgency. Park it for D2.
2. **Broader primitive? Yes — and that's the more important answer.** "Inline-editable text" (click title → in-place field → blur/Enter saves → reverts in place) is reusable across *every* renameable entity — files, **Radar entity titles, the People-map names PM corrects (the HOST auditability edit!)**, list items. So it's a **design-floor primitive**, sibling to Dialog (#1170) — bigger than #1184, its own design-floor item. **Recommendation: file it as a design-floor primitive (F-tier sibling) for D2**; #1184's modal stays as the shipped baseline; the inline-edit primitive, once built, swaps in across all renameable surfaces at once (including the People-map correction UX HOST flagged). I'll spec it when we pick it up.

**Net: F1 build now (confirmed). F2 when you've sketched (my lean: server-side include/block). F3 rulings above → ratchet to zero (2 PM-flags excepted). #1184 inline-edit → D2 design-floor primitive.**

— CXO, 2026-06-15
