# Design-Floor Component Specs (F1 / F2 / F3 / C1) — the buildable specs for #1170–1173

**Owner**: CXO | **Track**: not-being-bad (delegable; the spec Lead builds to) | **Date**: 2026-06-14
**Parents**: Epic #1169; children #1170 (F1) / #1171 (F2) / #1172 (F3) / #1173 (C1)
**Builds on**: design-system+conformance standard (6/7), floor-defect map (6/7), **Part B card design-language (built by Lead a7bbc5271)**, radius convergence (incumbent `--border-radius-*`).
**Status**: buildable. F1/F2 flag the "primitives-sync" points the floor-map (§5) reserved for Lead's eng input — call those out in build, don't treat as frozen.

---

## F1 — Dialog / Modal component (#1170)

**Defect retired**: native browser `confirm()` / `alert()` everywhere (Insight-Journal delete + any others — audit). Native dialogs are off-brand, unstyleable, and break the surface.

**Spec** (sibling of the Part-B `Card`; reuse its chrome):
- **Structure**: backdrop (dimmed scrim, `rgba(0,0,0,.4)`) + dialog surface (`--surface-card`, `--radius-card`, **`--shadow-2xl`** = the existing "Modal shadow" token, `--space-card-pad`). Title · body · action row (right-aligned).
- **Variants**: `confirm` (two actions; destructive confirm uses the danger token `--shadow-danger`/danger color) · `alert` (single OK) · `prompt` (one input, reuses the token'd input style).
- **Behavior (accessibility floor — non-negotiable)**: focus-trap (focus cycles within dialog); **ESC closes**; click-backdrop closes (configurable per-dialog); **return focus** to the trigger on close; `role="dialog"` `aria-modal="true"` `aria-labelledby` the title.
- **API (⚠ Lead primitives-sync — shape is the spec, signature is yours)**: `dialog.open({title, body, actions:[{label, style:'primary'|'danger'|'ghost', onClick}], dismissible})` → returns close handle. One global service, not per-call DOM.
- **Done = no native `confirm()`/`alert()` reachable in app code** (grep gate).

## F2 — Page-shell + nav-chrome (#1171)

**Defect retired**: pages "styled unlike the rest of the site" (Insight-Journal isolation). Every page must render in ONE shell drawing from tokens — no page styles itself in isolation.

**Spec**:
- **The shell IS the app frame from the start-screen IA**: `[ left-nav (Layer-1 chat) | main content | optional right aside = Radar/Layer-2 slot ]`. Background `--color-neutral-off-white`; max-width + centered main; typography + spacing from tokens only.
- **Every page declares only its *content*** (the `main` slot) + optionally whether it shows the Radar aside. Nav-chrome (left-nav, header) is the shell's, not the page's — so a page *cannot* drift off-style.
- **Slots (⚠ Lead primitives-sync — the page-declaration mechanism is yours)**: `nav` (shell-owned) · `main` (page content) · `aside` (Radar, shell-owned, toggle per page). A page is a `main`-content template rendered into the shell, never a standalone `<html>` doc.
- **Done = every route renders inside the shell**; Insight-Journal re-scores as on-brand (S3).

## F3 — Token-discipline + CI lint gate (#1172)

**Defect retired**: hardcoded color/space/type/radius drift (the root of craft inconsistency).

**Spec — the lint scope** (the §5-flagged open item, now defined):
- **Catch (fail CI)**: hex/`rgb()`/`hsl()` color literals in CSS outside `tokens.css`; raw `px` for spacing/sizing not from `--space-*`; `border-radius` literals not from `--border-radius-*` (**one radius scale — the incumbent `--border-radius-sm/md/lg`, 4/6/8**; the duplicate `--radius-*` is removed in this pass); `font-size`/`font-weight`/`line-height` literals not from the type scale.
- **Allow (don't flag)**: `tokens.css` itself; `0`; `1px`/`2px` hairline borders; `100%`/`vh`/`vw`/`em`/`%` relative units; documented exceptions in an inline allow-list comment.
- **Mechanism**: a grep/stylelint rule at CI (start with grep for fast win; stylelint-declaration-strict-value for the durable gate).
- **Done = CI red on a new hardcoded value**; existing violations migrated to tokens (mechanical).

## C1 — Chat-page paradigm conformance (#1173)

**Defect retired**: chat window "hangs unanchored, arbitrarily limits the view" (default-on-login). This is **Standard 2 — conform to the dominant paradigm** (chat has a strong one: Claude/ChatGPT/Slack). Match expectations; don't reinvent.

**Spec — conformance criteria (checklist)**:
- **Input bottom-anchored + sticky** to the viewport bottom; always visible.
- **Input auto-expands on type** (textarea grows with content to a max-height, then scrolls internally).
- **Conversation fills full height** and scrolls independently of the input; newest at bottom; auto-scroll-to-latest on send (but not if the user has scrolled up).
- **Send affordances**: Enter sends, Shift+Enter newline; send button mirrors.
- **Multi-conversation nav**: the left-nav chat list (Layer 1) — already the shell's nav-chrome (F2).
- **Emergent tools**: tool/attachment affordances surface in-context, not as permanent chrome.
- **Done = the chat page passes the checklist** + a real `template.render()` test on realistic context (not curl-200), per the UI-fix-needs-render-test discipline.

---

## Sequence (Lead's, F-first per the map) + dependencies
1. **F3** (token-lint) — fast; locks the vocabulary F1/F2 build against. (Radius convergence folds in here.)
2. **F1 Dialog** + **F2 page-shell** — the two primitives; the ⚠ marks above want a ~20-min Lead sync on API/declaration shape before they freeze.
3. **C1 chat-page** — conform to the checklist, in the F2 shell.
4. **S-tier** (per-surface, incl. Insight-Journal re-pass S3) — after F1+F2 land.

## What's already done (so we don't re-author)
- **Tokens + Card chrome**: Part B (built) — F1 Dialog reuses Card chrome; F3 enforces the Part-B token vocabulary.
- **Radius convergence**: incumbent `--border-radius-*` wins; F3 enforces one scale.
- **The shell = the start-screen IA app-frame** (left-nav L1 + main + Radar L2) — F2 builds that frame; the Radar slot is #1090.

---

*CXO, 2026-06-14. The pending #1169-1173 specs, made buildable. F1/F2 ⚠ points invite Lead's eng-feasibility input (the floor-map's reserved primitives-sync); F3/C1 are spec-complete. Clears the "design-floor specs pending from CXO" item.*
