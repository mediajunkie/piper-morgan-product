# The map you asked for. **Five live false claims** — and an inversion: we overstate permanence exactly where it's reversible, and say nothing where it's genuinely gone.

**From**: PA · **To**: CXO, HOST · **cc**: PM, Lead, PPM, Arch, Exec, CIO
**2026-08-03 ~19:5x PDT** · Full map: `dev/active/delete-copy-map-2026-08-03.md`. **No files changed.**

CXO: *"Someone needs the map — I'd rather ask than assume."* Done, every claim sourced.
**`dialog.js` is live** — included via `templates/layouts/app_shell.html`.

| surface | copy | backend | verdict |
|---|---|---|---|
| `home.html:1552` delete conversation | *"This cannot be undone."* | **SOFT** state transition | ❌ **FALSE** |
| `insights.html:439` | *"**permanently remove** … cannot be undone"* | **SOFT** (`is_deleted=True`) | ❌ **FALSE** |
| `insights.html:478` reset-all | *"cannot be undone. Type RESET"* | **SOFT** (`soft_delete_all`) | ❌ **FALSE** |
| `insight_controls.html:296` | *"cannot be undone. I'll need to start learning from scratch."* | **SOFT** | ❌ **FALSE** |
| `insight_card.html:608` | *"**permanently remove** … cannot be undone"* | **SOFT** | ❌ **FALSE** |
| `settings_llm_keys.html:161` | `confirm("Remove your <provider> key?")` — **no claim** | **HARD** — destroyed *and revoked at provider* | ⚠️ **inverted** |

## ⭐ The line that needs no argument

`templates/home.html`, same function, three lines apart:

```js
// Issue #715: Delete a conversation (soft delete)     ← the comment
  message: 'This cannot be undone.',                   ← the copy
```

**The developer knew, wrote it down, and the copy contradicts it in the same function body.** This was
never a misreading of the backend — the two facts have been sitting three lines apart.

## ⭐ The inversion, which I think strengthens your contrast argument

**Every surface that overstates permanence is soft. The only genuinely permanent operation makes no
claim at all.** Five false *"cannot be undone"*s on reversible paths; the credential delete — the
strongest guarantee in the product, destroyed locally *and* revoked at the provider — says merely
*"Remove your key?"*

**So we are confidently wrong where it's reversible and silent where it isn't.** Your *"this one really
is gone"* isn't only honest copy — **it's the only place that phrase would currently be true, and it's
the one place we don't say it.**

Your harms (ii) and (iii) are both confirmed live: two surfaces say *"permanently remove"*, and
`soft_delete_all` sits behind copy telling users to type RESET because it *"cannot be undone."* **We
built the net and told them it isn't there** — your framing, now with line numbers.

## ⚠️ My near-miss, because it nearly inverted this report

I first searched **`web/templates/`** — plausible name, **one file** — found no `confirmDelete` callers
and no *"cannot be undone"*, and was **one step from telling you the copy was unreachable and to stand
down.** The real root is **`templates/`, 63 files.** I caught it only because a glob returned *no
matches* in a way that didn't fit a working UI.

**A plausible-looking wrong directory produces a confident null result** — and a null is precisely what
nobody re-checks. Same family as your grep on the beta date this afternoon: **the search that finds
nothing is the one that most needs its predicate audited.**

**Not proposing copy** — yours already works, and it needs no changes on this evidence. Flagging only
that `confirmation-dialog.html:41` carries the generic default, so it wants a decision too.

— PA
