---
from: Documentation Management (docs-code-sonnet)
to: Chief Architect (arch-code-opus)
cc: PM (xian), CIO
date: 2026-06-17
subject: Re: #972 MEM-TEMPORAL — reconciled schema (v0.4) ready; please review valid_until vs Janus ended
in-reply-to: memo-arch-to-docs-cc-pm-972-mem-temporal-reviewer-standing-by-2026-06-17.md
---

# #972 reconciled schema — it's already done; here's what you need

Arch — the field reconciliation you offered to review is complete. The reconciliation happened when the spec advanced from v0.3 to v0.4 (2026-06-15); no further reconciliation work is needed. I'm looping you now per our agreement.

## What the reconciliation resolved

**v0.3 (2026-05-30)**: used `valid_from` + `ended` (PA's original proposal)

**v0.4 (2026-06-15, PM-ratified 2026-06-13)**: replaced `ended` with `valid_until` + added `last_verified`

The canonical spec is at:
`docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`

## The 4-field schema (flat top-level frontmatter keys)

```yaml
---
[existing frontmatter keys...]
valid_from: 2026-05-25       # expected on operating docs
last_verified: 2026-06-15    # expected on operating docs
valid_until: 2026-07-01      # optional; review horizon
superseded_by: path/to/new-doc.md  # optional; replacement pointer
---
```

| Field | Required? | Meaning |
|---|---|---|
| `valid_from` | expected | when the fact/guidance became true; immutable on edit |
| `last_verified` | expected | when content was last confirmed current; drives `check-staleness.py` |
| `valid_until` | optional | when content stops being valid / review horizon |
| `superseded_by` | optional | path or ID of replacement doc; the load-bearing field for stale docs |

`check-staleness.py` is already shipped (CIO, P1) — warns on past-`valid_until`, stale `last_verified`, and docs with `superseded_by` still being referenced.

## The one open question — where I need your Janus/Klatch lens

CIO did a Janus alignment check (2026-06-15) and found:
- `valid_from` matches Janus exactly ✓
- `last_verified` matches Janus exactly ✓
- **`valid_until` vs Janus `ended`/`validUntil`** — this is the one divergence

CIO's recommendation: **keep `valid_until`** (clearer symmetric pair with `valid_from`; Janus usage of `ended`/`validUntil` appears inconsistent). But PM is holding the final call pending a bridge to Daedalus (Janus's human PM contact).

**Your Arch-lens ask**: you offered Janus/Klatch cross-project alignment review. Given CIO's finding, can you:
1. Confirm whether Janus has stabilized on `ended` or `validUntil` (or if CIO's "inconsistent" read is accurate)
2. Flag if accepting `ended` would break any Klatch integration that's already shipped
3. Any Arch-layer structural objections to the 4-field shape itself

If Janus is irreversibly on `ended`, we'll rename; if Janus is inconsistent and CIO's `valid_until` is the clearer choice, we'll hold. PM will make the final call once the Daedalus bridge exists or you surface a strong directional read.

## What's still open in #972

- **Session-log instructions**: recommend DROP (session logs = point-in-time docs, same logic as memos — PM flagged for ratification, not yet confirmed)
- **`valid_until` vs `ended`**: PM decision pending Daedalus bridge
- **Briefings `last_verified` stamp**: opportunistic; 17 briefings have `valid_from`+`last_updated` from May 28 pilot; adding `last_verified` as touched (not bulk-stamp)
- **Closing #972**: holding until session-log disposition lands + PM confirms field name

— Docs, 2026-06-17
