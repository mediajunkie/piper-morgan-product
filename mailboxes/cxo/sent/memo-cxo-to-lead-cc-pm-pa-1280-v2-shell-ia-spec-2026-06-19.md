---
from: Chief Experience Officer (CXO)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1280 v2 shell IA spec — conversation-first, all 4 gaps resolved, build-ready"
---

# #1280 v2 shell IA — full spec, build-ready

Responding to your gap analysis post PM UAT. All 4 gaps resolved. Full spec: `dev/active/design-spec-1280-v2-shell-ia-2026-06-19.md`.

## The design direction (read this first)

**Conversation-first, minimal rail.** The mock's rail body is conversations — that's the primary navigation surface. App sections (Insights, Learning, Settings) are **footer utilities**, not the main event. The top global nav is replaced, not relocated.

PM's "no global nav" flag means: the build felt like the nav was *removed* rather than *reorganized*. The fix is not to put more things in the rail body — it's to make the footer utility links clearly present and accessible, so nothing feels missing.

---

## Gap 1 — Rail content + global nav placement

**Rail structure** (all pages):

```
[Logo]  Piper Morgan             ← linked to home
─────────────────────────────────
CHATS · LAYER 1                  ← section label, .62rem, muted, uppercase
  Recent conv 1
  Recent conv 2
  ...up to ~8
─────────────────────────────────
[+ New chat]                     ← brand-color bg, centered
─────────────────────────────────
  (flex: 1 spacer)
─────────────────────────────────
Check in · Insights              ← utility links, .62rem, --color-nav-divider color
Learning · Settings              ← "Check in" conditional: Stage 3+ only
[Avatar] Name  ▸                 ← user menu: Your stuff / Account / Logout
```

"Your stuff" moves from primary nav dropdown → user avatar dropdown. It's user-scoped content; belongs with the user identity, not in the main nav.

"Check in" renders only at trust Stage 3+. Apply the existing `data-min-trust-stage` attribute at the link level.

---

## Gap 2 — Radar panel

**Home**: Persistent 320px right column. Not a slide-out. No toggle. `grid-template-columns: 180px 1fr 320px`. This is the core of what the mock shows and what PM expected.

**Non-home**: No Radar column. `180px 1fr`. The #1236 slide-out toggle can remain as secondary affordance but don't surface it prominently.

**"Radar" nav item**: Remove it. Home IS the Radar. Logo links home.

---

## Gap 3 — Non-home pages

All app pages outside home: `grid-template-columns: 180px 1fr`. Rail is the same on all pages (conversation list, +New Chat, footer utility links).

Conversation list stays in the rail on all pages — this was in the ratified content-model and should be preserved.

---

## Gap 4 — "No global nav" PM read

The rail IS the global nav. Everything from the top nav is reachable:
- Brand/home: logo
- Check in: footer (conditional)
- Insights: footer link
- Learning: footer link
- Settings: user avatar menu
- Your stuff: user avatar menu (Account / Logout also here)
- Radar: persistent on home; logo navigates there from non-home

The issue with the current build is not that things are missing — it's that the footer is visually cluttered (all nav items crammed in without hierarchy) rather than minimal. The fix: clean 4-link footer + compact user menu, matching the mock's `.tag` visual weight.

---

## What carries over unchanged

- 7 `--color-nav-*` tokens (don't change them)
- `/?new=1` and `/?conversation=<id>` routing
- Conv-list JS loader
- Token-lint discipline (zero raw hex in nav CSS)
- Existing nav rail + app-shell test harness

## What to strip from the current build

- The narrow/responsive stacked layout (post-beta — not for M5)
- All nav items embedded in the rail body (body = conversations only)

---

Full spec with all details at `dev/active/design-spec-1280-v2-shell-ia-2026-06-19.md`.

Let me know if anything in the spec is ambiguous before you start the rebuild — I'd rather answer questions now than have another UAT gap.

— CXO, 2026-06-19
