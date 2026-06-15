# F1 #1170 — Dialog/Modal component: gameplan (prep; build on CXO API-confirm)

_Lead Dev · 2026-06-15 · D1 design-floor F1. **Gated on**: CXO confirm of the `Dialog.open` signature (sync requested 2026-06-15). Approach is build-ready below; execute on confirm. CXO spec: `dev/active/design-floor-component-specs-2026-06-14.md` §F1._

## Premise — extend, don't rebuild (complete-don't-duplicate)
A global Dialog service already exists: **`web/static/js/dialog.js`** (`Dialog.show`/`Dialog.confirm`/form-mode) + `templates/components/confirmation-dialog.html` + `web/static/css/dialog.css` + `web/static/js/focus-manager.js`. It already has the **accessibility floor** CXO requires (focus-trap, ESC-closes, return-focus, `role=dialog`/`aria-modal`). F1 = **generalize it to CXO's `Dialog.open(actions[])` API + add the variant set + retire native dialogs**, NOT a new component.

## The build (3 parts)

### Part A — generalize the API (gated on CXO confirm)
- Add `Dialog.open({ title, body, actions: [{label, style:'primary'|'danger'|'ghost', onClick}], dismissible }) → closeHandle` — the general actions-array entry (CXO's exact shape).
- Refactor `Dialog.confirm` / add `Dialog.alert` / `Dialog.prompt` to be **thin wrappers over `open`** (confirm = 2 actions; alert = 1 OK; prompt = 1 token'd input + value in the close/return). Back-compat: existing `Dialog.confirm({title,message,onConfirm})` callers keep working (wrapper maps to `open`).
- Chrome to spec: Part-B Card tokens (`--surface-card`/`--radius-card`/**`--shadow-2xl`**/`--space-card-pad`); danger confirm → `--shadow-danger`/danger color. (Mostly CSS in dialog.css — and F3 token-lint now guards it.)
- `closeHandle` = a returned `{ close() }` so callers can dismiss programmatically (the "returns close handle" spec).

### Part B — migrate the ~12 native callers (the "retire native" Done)
Replace native `confirm()`/`alert()`/`prompt()` → `Dialog.*`:
| caller | native → Dialog |
|---|---|
| `home.html:1593` | `confirm('Delete conversation?')` → `Dialog.confirm` |
| `home.html:1557/1587/1618` | `alert(...)` (failure msgs) → `Dialog.alert` (or a Toast — these are error toasts, likely better as `ToastMessages.error`; confirm w/ CXO) |
| `insights.html:673` | `confirm(remove insight)` → `Dialog.confirm` (danger) |
| `insights.html:706` | `prompt(...)` → `Dialog.prompt` |
| `learning-dashboard.html:826` | `confirm(...)` → `Dialog.confirm` |
| `navigation.html:901/905` | `alert('Logout failed')` → `Dialog.alert`/Toast |
| `insight_card.html:606` | `confirm(remove)` → `Dialog.confirm` (danger) |
| `chat.js:329` | `alert('Could not save artifact')` → `ToastMessages.error` (already has a toast path) |
*(Note: several `alert()`s are error notices — likely better as Toasts than modal alerts; flag in the sync. The `confirm`/`prompt` ones are clearly Dialog.)*

### Part C — the grep gate (mirror F3 token-lint)
- A `scripts/native_dialog_lint.py` (or extend the F3 lint) + CI step: **fail on a reachable native `confirm(`/`alert(`/`prompt(` in `templates/`+`web/static/js/`** (excluding dialog.js's own internals + comments). Baseline-ratchet like F3 so it goes live immediately + ratchets to zero as Part B migrates. Done = gate green at zero.

## TDD
- `Dialog.open`: actions render with styles; `onClick` fires + closes; `closeHandle.close()` works; `dismissible:false` blocks backdrop-close; focus-trap/ESC/return-focus (extend existing dialog tests if present).
- Wrappers: confirm/alert/prompt map to `open` correctly.
- Migrations: content-assertions per template (no native `confirm(`/`alert(`; `Dialog.*` present) — the convention used for #1184/radar.
- Grep gate: catches an injected native `confirm(`; passes clean.

## Sequence
CXO confirms API → Part A (API + wrappers + chrome, TDD) → Part C grep gate (baseline) → Part B migrate callers (ratchet to zero) → close-properly (cite the CXO spec + the grep-gate-green evidence). Then F2 (page-shell) once its declaration mechanism is synced.

## Open (for the sync)
- Confirm `Dialog.open` signature + variant nuances (prompt return shape).
- The `alert()`-error-notices: modal `Dialog.alert` vs `Toast`? (UX call — I lean Toast for transient errors, modal alert for blocking ones.)
