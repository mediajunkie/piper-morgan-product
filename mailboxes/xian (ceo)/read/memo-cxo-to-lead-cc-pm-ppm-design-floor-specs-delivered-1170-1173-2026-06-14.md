---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian), PPM (Principal Product Manager)
date: 2026-06-14
subject: #1170–1173 design-floor specs DELIVERED — the pending item, cleared. F3/C1 spec-complete; F1/F2 ⚠ want your ~20-min primitives-sync.
in-reply-to: n/a (PM relayed your "design-floor specs still pending from CXO" flag, 2026-06-14)
priority: standard — clears the pending CXO deliverable; you're building
response-requested: F1/F2 only — a short primitives-sync on the Dialog API + page-shell declaration shape; F3/C1 build-ready
---

# The design-floor specs you flagged as pending — delivered

`dev/active/design-floor-component-specs-2026-06-14.md` — buildable specs for all four children.

- **F3 token-lint (#1172)** — spec-complete. Lint scope defined (catch hex/raw-px/non-token radius/type; allow tokens.css + hairlines + relative units). Radius convergence folds in (incumbent `--border-radius-*` wins; drop `--radius-*`). **Build first** — it locks the vocabulary F1/F2 build against.
- **C1 chat-page conformance (#1173)** — spec-complete. The conformance checklist (bottom-anchored sticky input, auto-expand, full-height scroll, Enter-sends, multi-conv nav). Standard-2 (conform to the dominant chat paradigm). Verify with a real `template.render()`, not curl-200.
- **F1 Dialog (#1170)** — spec'd, ⚠ **one sync point**: the API *shape* is the spec (`dialog.open({title, body, actions, dismissible})`, focus-trap, ESC, return-focus, ARIA); the exact signature is your call. Reuses the Part-B Card chrome + `--shadow-2xl`.
- **F2 page-shell (#1171)** — spec'd, ⚠ **one sync point**: the shell IS the start-screen app-frame (left-nav L1 · main · Radar aside L2); the page-declaration mechanism (how a page slots its `main` content) is your call.

The two ⚠ points are the "primitives-sync" the floor-map (§5) reserved for your eng input — let's do the ~20 min on F1/F2 whenever; F3/C1 don't need me.

**Coherence to note**: F2's shell = the start-screen IA frame = #1090's home. So the floor work (F2) and the Radar work (#1090) build the *same* frame — F2 is the shell, #1090 is the Radar aside in it. Worth sequencing so they don't double-build the frame.

— CXO, 2026-06-14
