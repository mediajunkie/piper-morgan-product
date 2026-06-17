# F2 — Page-Shell Spec (#1171) — the buildable spec

**Owner**: CXO | **Track**: not-being-bad (the spec Lead builds to) | **Date**: 2026-06-16
**Parent**: #1169 (F2). **Builds on**: design-floor specs (6/14), the start-screen IA app-frame, Part-B tokens/Card, F1 Dialog (#1170 built), F3 token-lint (#1172 built).
**Resolves**: the ⚠ "page-declaration mechanism" sync-point from the 6/14 floor specs. **Decision: server-side template-include + per-page content block (NOT JS mount).** Lead confirmed this matches reality (only `insights.html` extends a base today; ~6 pages are standalone with their own nav = the drift F2 kills).

---

## 0. The property F2 must guarantee

**A page cannot drift off-chrome, structurally.** A page declares *only its content*; the header/nav-chrome is the shell's and is **not a block a page can override**. That's what retires the Insight-Journal-isolation defect class — not discipline, but structure.

## 1. The shell — `layouts/app_shell.html`

The canonical full shell. (Today's `layouts/base.html` provides only a bare `{% block content %}` — too thin; it's what let pages render chrome-less.) `app_shell.html` provides the **chrome + content region + the override blocks**, drawing exclusively from `tokens.css`.

```
app_shell.html
├── <head>: token'd base styles + {% block page_title %} + {% block head_extra %}
├── HEADER / NAV-CHROME   ← shell-owned, NOT page-overridable (the drift-killer)
│     └── global nav (the components/navigation.html include) + left-nav (L1 chat, where present)
├── <main> CONTENT REGION
│     ├── {% block main %}          ← the page's content (the one block every page overrides)
│     └── {% block aside %}         ← optional Radar/Layer-2 aside (default: Radar; page may suppress)
├── FOOTER                ← shell-owned
└── {% block scripts %}            ← page-specific end-of-body scripts
```

## 2. The block contract (what a page may override — Lead's exact question)

| block | who | purpose |
|---|---|---|
| `page_title` | page | the `<title>` text |
| `head_extra` | page | page-specific `<head>`: meta, a page CSS `<link>`, preloads. **(How page `<head>` slots in.)** |
| `main` | page | **THE page content — required; the only block most pages need.** |
| `aside` | page (optional) | Radar/Layer-2 aside. Default = the Radar include; a page suppresses it with `{% block aside %}{% endblock %}` or a `show_radar=false` context flag. |
| `scripts` | page | page-specific scripts at end-of-body. **(How page scripts slot in.)** |
| **header / nav / footer** | **SHELL ONLY** | **not page-overridable.** A page physically cannot restyle or omit the chrome. This is the F2 guarantee. |

## 3. Chrome token/spacing rules (Lead's question)

The chrome uses **tokens exclusively — zero inline styles** (F3 lint now enforces this):
- **Nav/header**: background, text, hover, spacing, typography all from tokens (`--color-neutral-*`, `--space-*`, type scale). The `components/navigation.html` include is the single source.
- **Content region** `<main>`: max-width + centered; padding `--space-lg` (24px); `--color-neutral-off-white` page background, content surfaces use `--surface-card`.
- **Aside (Radar)**: fixed width, `--border-card` left border; the Radar component (#1236) drops in (it's already frame-agnostic per Lead — F2 provides the aside, #1236's component fills it).
- **Footer**: token'd, minimal.

## 4. Migration (the ~6 standalone pages)

1. `app_shell.html` lands (chrome + blocks above; may itself `{% extends base.html %}` adding chrome, or replace base's role).
2. Each standalone page: strip its bespoke nav/`<html>` boilerplate → `{% extends 'layouts/app_shell.html' %}` + move its content into `{% block main %}` (+ `head_extra`/`scripts` as needed).
3. `insights.html` (extends `base.html` today) re-points to `app_shell.html` — and its item-2 design-system drift (§#1251) cleans up in the same pass (inline styles → tokens; bespoke components → Part-B Card/Dialog).
4. **Done = every route renders inside the shell**; a grep/test confirms no page defines its own `<html>`/nav. Verify with a real `template.render()` on each migrated page (not curl-200), per the UI-fix-render-test discipline.

## 5. Relationship to #1090/#1236 (no double-build)
F2 provides the **shell + the `aside` slot**; #1236's Radar is the **frame-agnostic component that drops into the aside** (Lead already built it that way). So F2 and Radar build the same frame once — F2 = the shell, Radar = the aside's content. No conflict.

---

*CXO, 2026-06-16. The F2 "go" spec. Block contract + chrome-token rules + migration. The structural guarantee (chrome is not page-overridable) is the load-bearing part — it's what makes the drift impossible rather than merely discouraged.*
