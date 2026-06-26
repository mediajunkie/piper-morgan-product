# Shell IA + nav spec v2 — #1280 (2026-06-19)
**Authored**: CXO, 2026-06-19
**Status**: COMMITTED — replaces v1 spec (2026-06-18) and the interim content-model ratification
**Binding visual reference**: `dev/active/radar-entities-surfacing-mockup-2026-06-14.html`
**Supersedes**: `dev/active/design-spec-dark-nav-shell-2026-06-18.md`

---

## Design direction: conversation-first, minimal rail

The rail IS the app shell. Its body is **conversations** — that's the primary thing a user navigates through. App sections (Insights, Learning, Settings) are **footer utilities**, not the main event. The top global nav is **replaced**, not preserved in a new location.

PM's feedback after UAT: "no global nav, does not resemble the mock." The mock shows a minimal dark rail where conversations dominate. The correct response is not to find somewhere to put all the old nav items — it's to commit to the conversation-first model the mock establishes.

---

## The 7 `--color-nav-*` tokens (unchanged from v1)

```css
--color-nav-bg: #11212e;
--color-nav-text: #cbd5dc;
--color-nav-text-muted: #7f97a6;
--color-nav-text-secondary: #9fb3c2;
--color-nav-divider: #5d7385;
--color-nav-item-hover: rgba(255,255,255,0.07);
--color-nav-item-active: rgba(255,255,255,0.13);
```

No raw hex in nav CSS. These tokens cover the full surface.

---

## Rail structure (all pages — 180px wide)

```
┌─────────────────────────────┐
│  [Logo]  Piper Morgan       │  ← brand row; linked to home
├─────────────────────────────┤
│  CHATS · LAYER 1            │  ← section label (.nav-text-muted, .62rem, uppercase)
│    Recent conv 1            │  ← .nav-text-secondary, hover background
│    Recent conv 2            │
│    Recent conv 3            │
│    ...up to ~8              │
├─────────────────────────────┤
│  [+ New chat]               │  ← CTA: brand-color bg, white text, full-width
├─────────────────────────────┤
│            ↕ (flex: 1)      │  ← empty space expands to push footer down
├─────────────────────────────┤
│  Check in · Insights        │  ← footer utility links, .nav-divider color (.62rem)
│  Learning · Settings        │  ← trust-gated: "Check in" only at Stage 3+
│  [Avatar] Name  ▸           │  ← user menu anchor (Your stuff / Account / Logout)
└─────────────────────────────┘
```

### Rail section details

**Brand row** (top):
- Compact logo + wordmark. Linked to `/` (home). Clicking logo = going home.

**Section label**: `CHATS · LAYER 1` — `.62rem`, letter-spaced uppercase, `--color-nav-text-muted`. Same as mock.

**Conversation list**: Recent conversations, max ~8. `--color-nav-text-secondary`. Hover: `--color-nav-item-hover`. Active: `--color-nav-item-active`. Ellipsis on overflow. No inline timestamps (clutters the rail at 180px).

**+ New chat**: Brand-color background, white text, centered, full-width-ish. `/?new=1`.

**Flex spacer**: `flex: 1` between the conv list/CTA and the footer. Pushes footer to the bottom at all viewport heights.

**Footer utility links**:
- Rendered as a single line of separator-joined text links: `Check in · Insights · Learning · Settings`
- `--color-nav-divider` color (the most muted nav color, same as the mock's `.tag`)
- `.62rem` font (same as mock — deliberately small; these are not primary navigation)
- "Check in" → `/standup` — **conditional**: only rendered if user is at trust Stage 3+. The link appears; trust-gating is applied at the link level (attribute), consistent with existing trust-gating pattern.
- "Insights" → `/insights`
- "Learning" → `/learning`
- "Settings" → `/settings`

**User avatar / menu** (bottom of footer, below the utility links):
- Avatar image or initials circle
- Display name truncated
- `▸` indicates expandable
- Dropdown upward: **Your stuff** (→ `/your-stuff` or existing hub), Account (→ `/account`), Logout
- "Your stuff" moves from a top-nav dropdown to the user menu dropdown — it's user-scoped content (Todos, Projects, Work Items, Files, Documents, Lists), which belongs with the user identity section, not with the primary rail

### What's NOT in the rail
- No "Radar" nav item — home IS the Radar. Link to home via logo.
- No ⌘K button — command palette remains keyboard-only. No nav-resident affordance.
- No non-home search input — deferred per v1 spec.
- No per-page context nav — the rail is the same on all pages.

---

## Shell layout

### Home (`/`)
```
grid-template-columns: 180px 1fr 320px
```
| Column | What |
|---|---|
| 180px | Dark rail nav |
| 1fr | Chat interface (full-height, input anchored bottom) |
| 320px | **Radar panel — persistent**, always visible on home |

The Radar is a **persistent 320px column on home**. Not a slide-out, not a toggle. It's always there, because home IS the Radar view. The `#1236` entity-search lives in the Radar panel's search field.

### All other pages (`/insights`, `/documents`, `/settings`, `/standup`, `/learning`, `/your-stuff`, all settings-* pages, etc.)
```
grid-template-columns: 180px 1fr
```
The rail is present; the content fills the rest. No Radar column on non-home pages.

The #1236 Radar slide-out toggle can remain as a secondary affordance but shouldn't be prominently surfaced on non-home pages.

### Narrow (< 768px)
Stack: rail collapses to hamburger / off-canvas drawer. **Post-beta — do not build for M5.** Narrow stacked layout from v1 is premature; strip it.

---

## Gap resolutions (Lead's 4 questions)

**Gap 1 — Rail content + global nav placement**: Conversation-first. Rail body = conversations only. Footer = [Check in · Insights · Learning · Settings] utility links (`.62rem`, muted) + user avatar menu (Your stuff / Account / Logout). Nothing is lost from the global nav — it's reorganized, not removed.

**Gap 2 — Radar panel**: Persistent 320px column on home. Not a slide-out on home. Non-home: no Radar column in the layout (slide-out remains as secondary affordance).

**Gap 3 — Non-home pages**: `180px 1fr` layout. Rail = same conversation list everywhere (Slack-style, confirmed from content-model ratification). Content fills 1fr.

**Gap 4 — "No global nav"**: The rail is the global nav. Everything that was in the top nav is reachable: brand/home (logo), Check in (footer conditional), Insights/Learning/Settings (footer links), Your stuff/Account/Logout (user menu). The design is a reorganization, not a removal. The key thing PM needs to see: the footer links are THERE and clear, not buried.

---

## What the build should do differently from v1

1. **Home**: Add the 320px Radar column back (`180px 1fr 320px`). It was in the grid spec but not wired.
2. **Footer links**: Replace the "everything crammed in" pattern with the minimal 4-link footer (`Check in · Insights · Learning · Settings`) + user avatar menu.
3. **Your stuff**: Move from a top-level nav dropdown into the user avatar menu dropdown (upward). One menu item, not 6 footer links.
4. **Rail body**: Conversations only. No nav items mixed into the body.
5. **Strip the narrow/responsive stacked layout** (post-beta).
6. **"Radar" nav item**: Remove — home IS the Radar. Logo links home.

---

## What carries over unchanged

- The 7 `--color-nav-*` tokens (already in tokens.css)
- `nav_rail.html` component structure (brand, chats section, +New Chat, footer)
- The conv-list loader (JS, fetches conversations → `#nav-rail-chats`)
- `/?new=1` for new chat
- `/?conversation=<id>` for conversation links
- `⌘K` keyboard-only command palette (no nav button)
- Token-lint clean build (no raw hex in nav CSS)

— CXO, 2026-06-19
