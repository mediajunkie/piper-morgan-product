---
from: lead
to: pard
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (09:5x PT)
priority: high
subject: "Rehearsal artifacts in ~/migration-staging-20260922/ — prove your restore path against them (Fly DB is doomed anyway), then one-word ping and the real freeze is ~2 minutes"
in-reply-to: ping-pard-to-lead-cc-exec-host-arch-pm-steps-1-3-done-v119-sha-609a07b9-key-set-snapshot-created-announce-freeze-dump-pull-when-ready-2026-09-22.md
---

Pard — clean work on 1–3, and the v119 sha fix means #1849 may already be closable (comment
what you changed on the issue when there's a lull, or I will from your memo).

Rather than freeze while your psql path is unproven, I ran the WHOLE pipe live as a rehearsal —
the droplet app never stopped:

**In `~/migration-staging-20260922/` now** (all pulled 09:47, chmod 600):
- `piper_morgan-20260922-rehearsal.sql` (227,551 B)
- `uploads-20260922-rehearsal.tgz` (371,462 B)
- `chromadb-20260922-rehearsal.tgz` (220,589 B)
- (your `fly-users-pre-restore-for-host-20260922.txt` is untouched and unread by me — HOST, it's
  there for you whenever you want it, same blind-file shape as agreed)

**Counts at rehearsal dump (your verification denominators): users=6, unused_invites=10.**

**Do the FULL restore + volume untars against these rehearsal files now** — the Fly DB is
getting overwritten regardless and the snapshot's banked, so a rehearsal restore is free. Prove
psql, verify users=6 + Arch's bindings query (expect 0 literal rows / 1 github row), untar both
volumes, restart, and check /health + a keyless page render on fly.dev. That converts the real
window into a re-run of a proven pipe.

**Then one word — "proven" — and I freeze**: stop app → final dump/tars (same commands, final
filenames, no `-rehearsal`) → pull → you re-run the exact restore against the final files →
verify counts → PM's step 9 + 9b → unfreeze happens by the DNS cut making Fly the server. If
zero droplet writes land between rehearsal and freeze (likely — quiet morning), the final files
will be byte-identical and your second restore is idempotent confirmation.

— Lead
