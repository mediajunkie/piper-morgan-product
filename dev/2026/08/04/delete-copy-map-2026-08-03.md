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
| `settings_llm_keys.html:161` | `confirm("Remove your <provider> key?")` — **no permanence claim** | ⛔ **CORRECTED 2026-08-04 — my original row said "key destroyed AND REVOKED AT THE PROVIDER." That is FALSE.** `delete_user_key` (`user_api_key_service.py:340`) is *"Delete API key for user from keychain and database"* — **no provider call, and none is structurally possible**: only the key's owner can revoke in the provider's console. Correct reading: **HARD locally, live remotely.** | ⚠️ **inverted, but less so than I claimed** |

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
locally — says only *"Remove your key?"*

**So the product is confidently wrong exactly where it's reversible, and silent exactly where it isn't.**
That part stands, and it's the load-bearing half.

> ⛔ **CORRECTED 2026-08-04 — the clause I struck here (*"and revoked at the provider, the strongest
> deletion guarantee in the product"*) was FALSE, and CXO shipped it into string 6 on my authority.**
>
> **CXO's memo takes full ownership of that claim and diagnoses it as their own argument-shape pressure.
> The diagnosis is a good one and it isn't what happened here — the claim came from this row, dated a day
> earlier.** They inherited it, they didn't invent it.
>
> 🔴 **And note the direction, which is the part that matters**: my error told a user their key was dead
> at the provider. **A user who believes that will not go revoke it.** My false claim causes inaction on
> a live credential — the same direction CXO correctly identified as *worse* than the five permanence
> overstatements this map was written to catch. **I introduced the dangerous-direction error into the
> audit whose entire premise was that the word must match the behaviour.**
>
> **Mechanism, because it generalises**: I did not invent the word *revoke*. I read it in
> `disconnect.py`'s own docstring — *"#358 grant revoke"* — where it names a **local** grant-store row
> deletion, and carried it to a different code path entirely. **Source vocabulary is not source
> verification.** A comment using a strong verb for a weak operation will hand you the strong verb, and
> the audit trail will look clean because you can point at the file.

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
