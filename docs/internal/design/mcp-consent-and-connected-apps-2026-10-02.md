# MCP consent page + Connected apps Settings card — CXO design spec

**Date**: 2026-10-02
**Author**: CXO
**Covers**: #1911 (MCP OAuth consent page branding/identity/revoke-path) + #1918 (Connected apps
Settings card) — designed together per PA's framing (2026-10-01): the consent page needs to
truthfully name a real revoke location, and #1918 is that location.
**Status**: Design complete, ready to build. Implementer TBD (PA or PA-dispatched subagent per
#1918's routing; #1911's routing says "implementer TBD after design").

---

## 0. What I checked before designing (per this week's standing discipline: check the live
source, not the summary of it)

- `web/routers/mcp_oauth.py:214-291` — current consent page is raw inline HTML
  (`_CONSENT_PAGE.format(...)`), not using `templates.TemplateResponse` or any shared layout.
  Revoke-promise sentence already dropped (PA, `15c371f65f`, confirmed absent). Raw UUID still
  shown via `<code>{user_id}</code>` — the open requirement.
- `services/mcp/server/resources.py` — the three resources named in the current scope list
  (`piper://me/profile`, `piper://me/colleague-model`, `piper://me/github/issues`) are the
  **complete, current list** — no drift. A new tool, `what_piper_knows_about_me`
  (`fcd07b850b`, merged to `main`), is **also live now** — checked its description
  (`resources.py:240-247`) and its own `register_tools` docstring guard ("every tool here only
  composes read functions"): it is a pure single-call composition of the **same three reads**,
  exposed via MCP's tool interface instead of (or alongside) the resource interface. **Conclusion:
  the three-item scope list is still truthful — no new data category exists, just a second access
  mechanism for the same three.** Nothing to add to the bullet list; flagging this check happened so
  nobody re-derives it from scratch.
- `web/api/routes/mcp_connections.py` — **#1918's backend is already fully built**: `GET
  /api/v1/settings/mcp-connections` → `{oauth_connections: [{client_id, client_name, connected_at,
  last_used_at, active}], manual_tokens: [{label, connected_at, last_used_at, active}]}`; `POST
  /api/v1/settings/mcp-connections/{client_id}/revoke` → `{revoked, client_id}`, 404 for an unknown
  connection (never reveals whether it exists for a different user). Idempotent, owner-scoped by
  construction.
- `templates/layouts/app_shell.html` + `static/css/tokens.css` — the app has one real design-token
  system (v1.1.0, CXO-owned per its own header). **No dark-theme token file exists anywhere in the
  repo** (`find . -iname "*dark*.css"` → nothing; `tokens.css`'s own header says "Light Theme").
  `color-scheme: light dark` in the current consent page is an unfulfilled browser hint, not a real
  dark variant.
- `templates/settings_calendar.html`, `settings-index.html` — established page conventions: a
  `.settings-container` + card pattern (white bg, `border-radius: 12px`, `box-shadow: 0 1px 3px
  rgba(0,0,0,0.1)` — these are the pre-tokenization hardcoded values every settings page still
  carries; new pages should use the real tokens instead, see §3), `Dialog.confirm()` for destructive
  actions, `Toast.success/error()` for feedback, `escapeHtml` as a shared global, `credentials:
  'include'` + `parseApiDetail` on every fetch.
- `services/database/models.py:118-139` — `User.username` and `User.email` both exist, both
  `nullable=False`. No separate `display_name` field on this model. Lookup pattern already exists
  elsewhere in this codebase (`services/auth/jwt_service.py:660`: `select(User).where(User.id ==
  user_id)`).

---

## 1. #1911 — MCP OAuth consent page

### 1a. Identity line

Replace the raw UUID entirely — not moved to a disclosure, **dropped**. There's no reason a tester
needs to see their own UUID on a consent screen, and "disclosure for support" invents a need nobody
has stated; support can already resolve a user from username/email.

```
<p class="who">Signed in as <strong>{username}</strong> ({email}).</p>
```

Build note: `_render_consent_page`/`authorize` needs one added DB read —
`select(User).where(User.id == user_id)` (same pattern as `jwt_service.py:660`) — to get
`username`/`email` before rendering. If that lookup ever fails (should not happen — `user_id` came
from a validated session), fall back to the UUID rather than rendering a broken page; that's a
should-never-happen path, not a designed state.

### 1b. Branding

**Do not extend `app_shell.html`.** A full app shell (nav rail, chat widget, command palette) is
wrong for a one-time OAuth consent screen the way it would be wrong on Google's or GitHub's own
consent pages — those are deliberately minimal and focused, and so is this one already,
structurally. The fix is **tokens, not chrome**:

1. Add `<link rel="stylesheet" href="/static/css/tokens.css?v={asset_v}">` to the page head.
2. Replace every hardcoded value in the existing `<style>` block with the real token:
   - `border-radius: 6px` → `var(--border-radius-md)`
   - `.approve` colors (`#1a7f37` / `#1a7f37`) → `var(--color-accent-success)` /
     `var(--color-accent-success)` (text white stays literal — tokens.css doesn't define a
     "success button text" alias; using the raw success color as both border and background matches
     the existing GitHub-green convention well enough to keep, but drop the hand-picked hex)
   - `.deny` border (`#8c8c8c`) → `var(--color-neutral-medium-gray-decorative)`
   - `.who` (`opacity: 0.75`) → `color: var(--color-text-secondary)` (same visual weight via the
     token system's own muted-text color, not an opacity hack)
   - body font → `var(--font-family)`
3. **Drop `color-scheme: light dark`** — it promises a dark mode the page (and the whole app) does
   not have. If/when a real dark theme ships, this is one line to re-add; until then it's an
   unfulfilled claim about rendering behavior, the same category of thing this week's rulings have
   been declining to ship.
4. Add a small wordmark above the `<h1>`, styled to match the app's own topbar brand treatment
   (`app-shell.css:.app-shell-topbar-brand` — semibold weight) but in a color suited to this page's
   light background, not the dark nav-rail color that rule uses:
   ```html
   <div class="brand"><!-- not a link — consent pages shouldn't offer a click-away --> Piper Morgan</div>
   ```
   ```css
   .brand { font-weight: var(--font-weight-semibold); color: var(--color-primary);
            font-size: var(--font-size-lg); margin-bottom: var(--space-md); }
   ```
   This is a text wordmark, matching how the product already brands itself everywhere else in the
   app (the topbar brand is text, not an image logo) — not a new visual element to invent.

### 1c. Copy pass (Comms reviews voice; this is the content/structure)

Keep the existing sentence verbatim — it's accurate and was explicitly ruled KEEP yesterday:

> Read-only: it cannot change anything, and it cannot see another person's data.

**Add the revoke-path sentence now that #1918 gives it a real destination** (this closes
requirement 4 — "name where revocation lives, or confirm the path exists" — with a named path
instead of a vague promise):

> You can revoke this anytime from **Settings → Connected apps**.

Full paragraph as it will read:

```
Read-only: it cannot change anything, and it cannot see another person's data.
You can revoke this anytime from Settings → Connected apps.
```

**Gate before shipping this exact sentence**: it must not ship until #1918's UI is live — an
unbuilt "Settings → Connected apps" pointer is the same category of unverifiable promise as the
sentence it replaces. Build #1918 first, or ship both in the same release.

### 1d. Acceptance-criteria note — light/dark mode

The AC says "in light and dark mode **if the app supports both**." Checked: **it doesn't** (§0). So
this line of the AC is satisfied by the conditional being false, not by building a dark variant.
Flagging explicitly so whoever closes the issue doesn't either skip this silently or invent
unscoped dark-mode work to satisfy it.

---

## 2. #1918 — "Connected apps" Settings card

### 2a. Placement

New top-level settings page, `/settings/connected-apps`, linked from a **new card on
`settings-index.html`**. Placed near **Account**, not near **Integrations** — the direction is
reversed (third-party apps holding access *to* Piper, not Piper connecting *out* to a third-party
service), and conflating the two would misrepresent what a user is managing.

```html
<!-- Connected Apps Card (Issue #1918) -->
<a href="/settings/connected-apps" class="settings-card">
  <div class="card-icon">🤖</div>
  <h3 class="card-title">Connected apps</h3>
  <p class="card-description">
    See which chat apps — ChatGPT, Claude, and others — have access to your Piper account, and
    revoke it anytime
  </p>
  <div class="card-meta">
    <span class="meta-item">MCP access</span>
    <span class="meta-item">Revoke anytime</span>
  </div>
</a>
```

(Icon choice: 🔌 is already used for Integrations; 🔑 for LLM API Keys. 🤖 reads as "AI client
app" without colliding with either.)

### 2b. Page structure (`templates/settings_connected_apps.html`)

Extends `app_shell.html` like every other settings sub-page (unlike the consent page — this one
*is* inside the authenticated app, so the full shell is correct here).

```
Settings → Connected apps                              (breadcrumbs)

  Connected apps
  Chat apps like ChatGPT and Claude can connect to your Piper account once you approve
  them on their consent screen. Anything that still has access is listed below.
```

**That intro line matters — it's the fix for the "first-view alarm" problem I flagged yesterday.**
A tester's first visit to this page may show a connection from weeks ago that they approved once
and forgot about. Naming *how* something gets here ("once you approve them") turns a potentially
alarming unexplained entry into an expected, remembered one — the same honest-framing move as
#1875's fallback copy.

### 2c. States

**Loading**: a single centered spinner + "Loading your connected apps…" — matches the existing
spinner pattern (`loading-spinner` class, already in `settings_calendar.html`).

**Empty** (no OAuth connections, no manual tokens):

```
  No apps connected yet.

  When you connect ChatGPT, Claude, or another MCP client, it'll show up here.
```

Calm, not a dead end — reads as an expected starting state, not an error.

**Populated — active OAuth connections** (the primary list, one card-row per connection):

```
┌─────────────────────────────────────────────────────────┐
│  ChatGPT                                                 │
│  Connected Sep 12, 2026 · Last used 2 hours ago          │
│                                          [ Revoke ]      │
└─────────────────────────────────────────────────────────┘
```

Field mapping from `OAuthConnectionResponse`:
- Row title = `client_name` if present; if `null` (the client self-registers it and may omit it),
  show **"Unnamed app"** rather than the raw `client_id` — a `client_id` is an implementation
  detail, not something a user should have to recognize. Put `client_id` in a `title=` tooltip
  attribute for anyone who does need it (support, power users), not in the visible text.
- Subtitle = `Connected {connected_at, human date}` · `Last used {last_used_at, relative time}` —
  if `last_used_at` is `null`, show **"Never used"** instead of omitting the clause (an honest
  absence, not a silently shorter line that could read as a rendering bug).
- `active: false` rows are **not rendered in this list** — see §2d.

**Revoked / inactive connections** — a collapsed disclosure below the active list, not hidden
entirely and not mixed into the primary view:

```
  ▸ Previously connected (2)
```

Expands to a muted, read-only version of the same row shape (no Revoke button — already revoked).
This exists so "I revoked that, right?" has a visible answer without cluttering the primary
"what currently has access" view — same transparency instinct as the nearby Transparency/audit-log
settings card, applied locally.

**Manual/ops tokens** (`manual_tokens`) — a separate, clearly-labeled, read-only group:

```
  Other access tokens
  Issued directly for testing or support — not from a connected app.

  "load-test-oct" · issued Sep 20, 2026 · last used 3 days ago
```

No Revoke button — the backend doesn't expose one for these (`mcp_connections.py` only revokes by
`client_id`, an OAuth concept). Shown because hiding real access to the user's own account
conflicts with this product's own transparency stance; PA's "or not at all" option is declined for
that reason, not because it's wrong on the facts.

### 2d. Revoke flow

Button click → `Dialog.confirm()` (existing shared component, same shape as `disconnectCalendar()`
in `settings_calendar.html`):

```js
Dialog.confirm({
  title: `Revoke ${clientName}?`,
  message: `${clientName} will immediately lose access to your Piper account — it can't read ` +
           `anything after this. You can approve it again later if you reconnect from ${clientName} itself.`,
  confirmText: 'Revoke',
  onConfirm: async () => { /* POST .../revoke, then re-fetch the list */ }
});
```

Copy notes:
- Names the immediate, concrete effect ("can't read anything after this"), not a vague "are you
  sure?" — matches this week's standard for destructive-action copy.
- Names the recovery path ("approve it again later") so revoke doesn't read as scarier than it is —
  it's reversible by the user reconnecting, not a one-way door.

On success: `Toast.success('Revoked', `${clientName} no longer has access to your account.`)`, then
re-fetch `GET /api/v1/settings/mcp-connections` and re-render (don't just remove the row locally —
the server is the source of truth, and a stale manual-token count next to it would be worse than one
extra round-trip).

On 404 (already revoked, or a race with another tab): treat as success — the end state the user
wanted is already true. Don't show an error for "the thing you asked to happen has already
happened."

On 500: `Toast.error('Revoke failed', "I couldn't revoke that — try again in a moment.")` — matches
the existing honest-failure tone used elsewhere (`#1875`'s fallback pattern), not a technical detail
the user can't act on.

---

## 3. Build sequencing

1. #1918's UI (this spec, §2) can build now — backend is already live, nothing blocks it.
2. #1911's identity-line + branding fixes (§1a, §1b) can build now — no dependency on #1918.
3. #1911's revoke-path sentence (§1c) **must wait for #1918 to ship** — don't land that exact
   sentence first, or it's an unverified promise again, the same failure class it's replacing.
4. #1911's requirement 5 ("render-verified on the live page... not just a curl 200") applies to
   both pages — this spec is not itself the verification; whoever builds it still owes a live render
   check per this product's standing m-43 discipline (a config/copy diff is not a render test).

---

## 4. Open items not resolved by this spec (explicitly out of scope, not forgotten)

- Comms' voice pass on the copy in §1c and §2c (routed, not mine to finalize).
- Whether `client_name` being `null` is common enough in practice to warrant a build-time default
  other than "Unnamed app" — a build-time finding, not a design-time guess.
- The PM test PA named yesterday (does disconnecting in ChatGPT itself call our `/revoke`?) —
  informs messaging, doesn't block either page shipping as designed.
