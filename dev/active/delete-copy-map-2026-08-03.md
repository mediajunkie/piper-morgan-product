# The soft/hard delete copy map — CXO's owed mapping, complete

**PA, 2026-08-03.** CXO: *"Which affordances hit soft vs hard paths is unmapped… someone needs the map —
I'd rather ask than assume."* Here it is, every claim sourced.

## The map

| surface | user-facing copy | backend | verdict |
|---|---|---|---|
| `home.html:1552` — delete conversation | *"This cannot be undone."* | **SOFT** — `ACTIVE/ARCHIVED → DELETED` state transition | ❌ **FALSE** |
| `insights.html:439` | *"This will **permanently remove** '…'. This cannot be undone."* | **SOFT** — `soft_delete` sets `is_deleted=True`, row remains | ❌ **FALSE** |
| `insights.html:478` — reset all | *"This cannot be undone. Type RESET to confirm:"* | **SOFT** — `soft_delete_all` | ❌ **FALSE** |
| `components/insight_controls.html:296` | *"This cannot be undone. I'll need to start learning about you from scratch."* | **SOFT** | ❌ **FALSE** |
| `components/insight_card.html:608` | *"This will **permanently remove** '…'. This cannot be undone."* | **SOFT** | ❌ **FALSE** |
| `components/confirmation-dialog.html:41` | *"Are you sure…? This action cannot be undone."* | generic default | ⚠️ default text |
| `settings_llm_keys.html:161` | `confirm("Remove your <provider> key?")` — **no permanence claim** | **HARD** — key destroyed **and revoked at the provider** | ⚠️ **inverted** |

`dialog.js` is live — included via `templates/layouts/app_shell.html`.

## ⭐ The single most damning line, and it needs no argument

`templates/home.html`, same function body, three lines apart:

```js
// Issue #715: Delete a conversation (soft delete)     ← the code comment
async function deleteConversation(conversationId) {
  title: 'Delete this conversation?',
  message: 'This cannot be undone.',                   ← the user-facing copy
```

**The developer knew it was a soft delete, wrote it down, and the copy contradicts it in the same
function.** This was never a misunderstanding of the backend — the two facts have been sitting three
lines apart.

## ⭐ The inversion — the finding I didn't expect

**Every surface that overstates permanence is soft. The only genuinely permanent operation makes no
claim at all.**

Five false *"cannot be undone"* claims sit on soft paths. The one hard delete — credentials, destroyed
locally **and revoked at the provider**, the strongest deletion guarantee in the product — says only
*"Remove your key?"*

**So the product is confidently wrong exactly where it's reversible, and silent exactly where it isn't.**
That strengthens CXO's contrast argument: *"this one really is gone"* isn't just honest copy, it's the
**only** place that phrase would be true, and it's currently unsaid.

## Bearing on CXO's three harms

- **(ii) false gravity** — confirmed live on five surfaces, incl. two saying *"permanently remove."*
- **(iii) recovery capability made unreachable** — confirmed. `soft_delete_all` exists as a safety net
  behind copy telling users to type RESET because it *"cannot be undone."*
- **(i) privacy expectation** — HOST's, unchanged.

## ⚠️ My own near-miss, recorded because it nearly inverted the report

I first searched **`web/templates/`** — plausible name, **1 file** — found no callers of `confirmDelete`,
no *"cannot be undone"*, and was one step from reporting **"the copy is unreachable; stand down."**

The real template root is **`templates/` at project root — 63 files.** I caught it only because
`web/templates/*.html` returned *no matches* and that didn't fit a working UI.

**A plausible-looking wrong directory produces a confident null result**, and a null is exactly what
nobody re-checks. **Report what you searched, not just what you found.**

## What I have NOT done

Not proposing copy — that's CXO's, and the copy in their memo already works. Not touching HOST's
account-deletion-by-request path. **No files changed.**
