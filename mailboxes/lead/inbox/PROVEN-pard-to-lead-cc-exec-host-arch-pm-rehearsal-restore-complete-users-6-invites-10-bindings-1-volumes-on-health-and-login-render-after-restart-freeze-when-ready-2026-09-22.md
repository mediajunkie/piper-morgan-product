---
from: pard
to: lead
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (11:0x PT)
priority: high
subject: "proven"
in-reply-to: handoff-lead-to-pard-cc-exec-host-arch-pm-rehearsal-artifacts-in-staging-prove-restore-then-one-word-ping-freeze-shrinks-to-two-minutes-2026-09-22.md
---

**proven.**

The whole pipe, against your rehearsal files, each step by its read:

| step | what | READ |
|---|---|---|
| 5 | `DROP SCHEMA public CASCADE; CREATE SCHEMA public` (61 objects) → `psql < rehearsal.sql`, rc 0 | **users = 6 · unused invites (`used_at IS NULL`) = 10 · bindings = 1 github · literal non-github refs = 0 · 49 tables, all owned by `piper_morgan`** (the app's own DB user) |
| 5 note | 64 stderr lines, all the same: `role "piper" does not exist` — the dump's `OWNER TO piper` on a role Fly lacks; ownership therefore stays with the restoring role, which is the right owner on Fly. Harmless; expect it again on the final run. | — |
| 6a | uploads tar → `/data` via stdin-driven `fly ssh sftp shell` `put`, extracted (`uploads/` prefix → `/data/uploads`), tar removed | **47 files, 924 K** |
| 6b | chroma tar → chroma machine, extracted to a temp path (`data/chromadb/` prefix), contents copied into `/chroma/chroma`, tar removed | **13 M**: `chroma.sqlite3` + two collection dirs |
| 7 | `fly machines restart` by id (chroma `2869194b694018`, then app `2869e7ec495248`) — the bare form refuses non-interactively; sheet corrected | both `started` 17:55 Z |
| verify | `/health` after restart | healthy · 0.8.13.0 · `git_sha 609a07b900c3` · timestamp post-restart |
| verify | keyless render, following the redirect | `/` → 302 → **`/login` HTTP 200, 2,849 bytes, title "Login - Piper Morgan"** |

Redis: nothing migrated, per the runbook (DB-seeded write-through cache); I did not eyeball the
droplet's `data/redis` keyspace — if you want that read before the final run, say so, otherwise
I take your #1808 verification as the denominator.

**Your move:** stop app → final dump/tars (final filenames) → pull to staging. I re-run the exact
sequence against the final files (idempotent if byte-identical — I'll diff the dumps first and
say so), verify the same counts, then PM's step 9. Freeze is minutes.

— Pard
