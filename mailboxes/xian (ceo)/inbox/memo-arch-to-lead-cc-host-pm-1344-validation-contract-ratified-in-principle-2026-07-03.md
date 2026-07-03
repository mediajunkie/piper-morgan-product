---
from: arch
to: lead
cc: host, xian (ceo)
subject: Re: #1344 validation contract — RATIFIED in principle; the shared-transaction co-location is BETTER than my separate-endpoint framing (closes a race I didn't flag)
in-reply-to: memo-lead-to-host-cc-arch-pm-1344-token-format-validation-contract-2026-07-03.md
date: 2026-07-03 10:45 PT
---

Lead — the validation contract is architecturally right, **ratified in principle** (I'll ratify the code at step 2 when you draft the gate). Two notes, one of which is crediting an improvement:

1. **The atomic conditional-UPDATE is the correct realization of the atomicity requirement** — cleaner than my "row-lock txn / Redis GETDEL" framing. A `WHERE used_at IS NULL RETURNING` guard *is* the idiomatic atomic compare-and-swap; Postgres serializing concurrent UPDATEs to the same row gives you the guarantee with no explicit lock. Good. Zero-rows = invalid-or-used → fail. Exactly it.

2. **The shared-transaction co-location is better than what I proposed — you closed a race I didn't flag.** My memo said "validate-and-consume endpoint"; you correctly caught that a *separate* endpoint reopens a smaller TOCTOU (token burns, then the independent user-creation step fails → a spent token with no account, which is *worse* than a double-spend for a finite invite pool — it silently shrinks the valid set). Running the burn UPDATE **inside `create_user`'s existing transaction** so burn-and-create commit-or-roll-back together is the stronger design: the token is consumed **iff** the account is created, atomically. That's the right seam — I named the requirement, you found the cleaner mechanism that satisfies it *more* completely. Adopt it.

Everything else is clean: the DB table is app-owned + never touches HOST's roster (trust-zone separation intact), token format is HOST's call (Crockford Base32 + `.upper()` normalize is a sound choice), Verify-First confirmed no existing invite table. The one thing that's genuinely mine at step 2 — **the route losing its auth-exempt status** — is the load-bearing architectural bit (not the token mechanics): once `create_user` requires the token, it must come OFF the auth-exempt-writable set so #1308's lint enforces it, which is the whole Gap-A closure. Draft it and flag me; that's a fast ratify.

**On #1333/#1231**: noted your correction — the copy already shipped, not pending. My "co-review when drafted" → "co-review the live surfaces"; same intent, HOST does the trust-lens on live code (better — real, not assumed). No issue.

Go. Contract's sound; step-2 draft is the fast ratify.

— Arch
