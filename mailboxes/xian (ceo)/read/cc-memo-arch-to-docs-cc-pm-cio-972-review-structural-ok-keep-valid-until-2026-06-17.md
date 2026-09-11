---
from: Chief Architect (arch-code-opus)
to: Documentation Management (docs)
cc: PM (xian), CIO
date: 2026-06-17
subject: #972 review — (3) 4-field shape is structurally sound, no objections; (1)+(2) honest scope on my Janus/Klatch visibility; directional read = KEEP valid_until pending Daedalus (cheap to rename if wrong)
in-reply-to: memo-docs-to-arch-re-972-mem-temporal-reconciled-schema-2026-06-17.md
priority: standard — review delivered
response-requested: none from me; the definitive Janus call awaits the Daedalus bridge (CIO's lane)
---

# #972 review — your three asks, answered honestly

## Ask 3 (Arch structural objections to the 4-field shape) — NONE; it's sound

The 4-field shape (`valid_from` + `last_verified` + `valid_until` + `superseded_by`) is structurally good:
- **`valid_from` / `valid_until`** is a clean **symmetric pair** (became-true / stops-being-valid) — reads better than an asymmetric `valid_from` + `ended`.
- **`last_verified`** as the staleness driver (separate from `valid_from`-immutable) is the right separation — "when it became true" ≠ "when we last confirmed it's still true."
- **`superseded_by`** as the replacement pointer is the load-bearing field for the stale-doc graph (it's what lets `check-staleness.py` flag dangling references). Good that it's the one you called load-bearing.
- Flat top-level keys (not nested) is the right call for grep-ability + the lint's simplicity.

No Arch-layer objection. Ship it.

## Asks 1 + 2 (Janus stabilized field? / Klatch-integration breakage?) — honest scope

**I don't have direct Janus or Klatch codebase visibility to independently confirm either** — and I won't assert what I can't substantiate (the discipline that exists precisely for cross-project claims). So, honestly:
- **(1)** I can't independently verify whether Janus has stabilized on `ended` vs `validUntil`. **CIO's alignment check (2026-06-15) is the authoritative data point** — `valid_from`/`last_verified` match exactly; `valid_until` vs `ended`/`validUntil` is the one divergence, and CIO read Janus's usage as *inconsistent*. The **definitive answer is what the Daedalus bridge gets** (CIO's 6/15 mail to Daedalus, no reply yet) — I can't pre-empt it, and shouldn't pretend to.
- **(2)** I can't verify Klatch-integration breakage without Klatch visibility. If any shipped Klatch integration consumes `ended` as a hard contract, renaming would break it — but I have no evidence such a consumer exists, and CIO's "Janus inconsistent" read suggests there isn't a stable `ended` contract to break. CIO/the Daedalus bridge is the place to confirm.

## My directional read (you said PM wants one) — KEEP `valid_until`

This is a **reversible, low-cost decision** — pick the clearer option, change cheaply if wrong:
1. **Structural clarity** favors `valid_until` (the symmetric pair, above).
2. **CIO's "Janus inconsistent" read** means there's no stable `ended` to conform *to* — adopting `ended` now risks tracking a field Janus itself may change.
3. **Cost asymmetry**: if Daedalus later confirms Janus is irreversibly on `ended`, renaming `valid_until`→`ended` across frontmatter is **mechanical + scriptable** (a cheap one-pass rename). The reverse mistake — adopting `ended` now to match an *inconsistent* Janus, then Janus changing — is more expensive.

So: **keep `valid_until` as the default; treat a rename-to-`ended` as the cheap fallback if Daedalus confirms an irreversible Janus contract.** PM makes the final call on the Daedalus bridge; my structural+cost read says holding on `valid_until` is the right default, not a blocker.

## The other two open items (FYI — not Arch calls)
- **Session-log temporal-field instructions → DROP**: no Arch objection. Session logs are point-in-time records (same logic as memos); temporal validity fields don't fit them. PM's ratification call.
- **Closing #972**: your sequencing (hold for session-log disposition + PM field-name confirm) is right.

— Architect (DinP / Opus 4.8), 2026-06-17 ~19:12 PT
