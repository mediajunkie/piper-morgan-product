# Invite token minted for Janne Lammi — raw string is in the gitignored roster, not this memo

**From**: Lead · **Date**: 2026-09-13 ~14:20 PT · **Cc**: exec, xian (ceo)

Minted 1 token against **production**, verified. Over to you for the roster row.

**Where the raw token is**: `dev/alpha/alpha-tester-roster.md` in the **main checkout**
(`/Users/xian/Development/piper-morgan-product/`), under a dated "awaiting HOST identity
mapping" block. That file is gitignored (`.gitignore:149`, confirmed with `git check-ignore`
after writing). Deliberately **not** in this memo: mailbox memos commit straight to
`origin/main`, which would put a live account-creation credential in permanent git history —
PM's ruling from the 2026-07-04 batch, same as last time.

**Mint evidence** (m-43, layer named): the script printed its target before writing —
`piper-morgan-db.flycast:5432/piper_morgan` resolved via the app's own config, i.e. the
database the running app uses, not a worktree default — and asserted the row delta inside the
same transaction: **rows 12 → 13, expected +1**. Release v99.

**Worth knowing, because it nearly went wrong**: the committed mint script's `_engine()` built
a **localhost:5433** URL from `POSTGRES_*` defaults. Run from anywhere but a dev worktree that
silently mints tokens into the dev database — output identical to success, and the tester's
code simply fails later. That's why the 2026-07 batch needed a throwaway script. It's fixed at
the source now: resolution goes through the app's config, the target host prints before any
write, a resolution failure is loud and **refuses outright** in production rather than falling
back, and the row delta is asserted. Two further traps fixed on the way: `fly ssh console -C`
fork/execs without a shell (a bare `VAR=x cmd` prefix is read as a binary name), and psycopg2
rejects asyncpg's `?ssl=` spelling outright rather than ignoring it.

**Your half**: record the identity mapping; PM sends the invite. Token is UNUSED as of mint.

— Lead
