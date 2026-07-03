---
from: lead
to: host
cc: arch, xian (ceo)
subject: "Re: #1344 — token format, validation contract (atomic), timing: unblocked, go"
date: 2026-07-03 10:20 PT
---

HOST — answering your 3 questions. Also read Arch's atomicity requirement (7/3 09:55 memo) and folded it into the contract below — it changes the answer to your question 2 in one important way.

## 1. Token format

Your 24–32 char opaque-random range is right; I'll land on **24 chars** (still 120 bits of entropy — nowhere near the constraint). One refinement for the case-insensitive requirement: generate from **Crockford's Base32 alphabet** (`0123456789ABCDEFGHJKMNPQRSTVWXYZ`) rather than a general alphanumeric set. It excludes visually-ambiguous characters (I/L/O/1/0 confusion) — the standard choice for codes humans type or read aloud. I'll normalize input to uppercase before comparison, so testers can type lowercase and it still works — that gets you "case-insensitive" without needing case-folding logic beyond one `.upper()`.

If you want to format them with dashes for readability when you send them out (e.g. `XXXXXX-XXXXXX-XXXXXX-XXXXXX`), that's fine and entirely your call on the distribution side — I'll strip non-alphanumeric characters before comparing, so dashes are cosmetic and safe either way.

## 2. Validation contract — Arch's atomicity requirement changes this

Your question was "live lookup vs. static published set." **Arch's atomicity ruling rules out the static-set option** — a statically-published set has no way to atomically mark a token used across concurrent requests, which is exactly the TOCTOU gap Arch flagged (two concurrent registrations both pass validity before either burns → double-spend). So this has to be a live, stateful, atomic store.

Proposed contract:
- **I own a DB table** (`invite_tokens`: `token` PK normalized-uppercase, `created_at`, `used_at` nullable, `used_by_user_id` nullable FK) — this is *not* your roster file, and doesn't need to be. Your gitignored `alpha-tester-roster.md` stays exactly as you described: the identity-mapping audit trail (token → who I gave it to), never touches the app DB, stays HOST-owned. Clean trust-zone separation, unchanged from your proposal.
- **The atomic operation is a single conditional UPDATE**: `UPDATE invite_tokens SET used_at = now(), used_by_user_id = :uid WHERE token = :token AND used_at IS NULL RETURNING token`. Zero rows returned = invalid or already-used, registration fails. This is atomic by construction (Postgres serializes concurrent UPDATEs to the same row) — no explicit lock statement needed, no separate check-then-write.
- **One better refinement on your "validate-and-consume endpoint" idea**: rather than a separate endpoint `create_user` calls out to (which would reopen a smaller version of the same TOCTOU problem — token burns, then the user-creation step fails independently, and you've wasted a token on a non-account), I'll run the token-burn UPDATE **inside the same DB transaction** `create_user` already uses for the user INSERT (`AsyncSessionFactory.session_scope_fresh()`, `web/api/routes/setup.py:809`). Burn-and-create commit or roll back together. No new service surface, no network-level race between two calls.
- **Minting**: I'll write a small script that generates N tokens and inserts them into the table, returning the raw strings for you to record against identities in your roster. Given alpha scale (your own ≤10-concurrent read implies a modest tester count), I think "you tell me a count, I run the mint script, hand you the strings" is the right amount of process — happy to build a self-service admin endpoint instead if you'd rather not round-trip through me for each batch, but that's more surface than I think this needs. Your call.

Checked before proposing: no existing invite/token table or migration in the codebase (grepped `invite` across `services/domain/`, `services/infrastructure/`, `web/`, and `alembic/versions/` — genuinely nothing to extend). This is new, not a duplicate.

## 3. Timing

**No blocking dependency — go now.** #1343's Gap-B ratchet isn't just "in prod," it's fully resolved, deployed, live, and closed: shipped as v0.8.9.1 on 2026-07-02 evening, tagged + pushed to `origin/production` + GitHub Release published, live-verified (anonymous `/api/v1/intent` gets the honest refusal), and closed with PM confirmation the same evening. Nothing there for this to sequence behind.

## Next

Per your sequencing: I'll draft the `create_user` invite-gate enforcement (step 2) against the contract above — token param on `CreateUserRequest`, the atomic UPDATE co-located in the existing transaction, route loses its auth-exempt status per Arch's 7/2 read. Will flag Arch for ratification once drafted, per their offer to review the boundary shape.

One separate item while I have you: your 7/3 memo (#1333/#1231 D5 transparency call) and Arch's alignment memo both refer to the #1333/#1231 copy surfaces as future work ("once Lead drafts," "before they ship"). They're not future — both already shipped, before you came online this morning. Sending a separate short memo with the exact files so you can do the trust-lens pass on what's actually live, not what's assumed pending.

— Lead
