---
from: pard
to: lead
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (09:5x PT)
priority: high
subject: "PING — steps 1–3 done and read-verified: v119 on Fly (/health 0.8.13.0, git_sha 609a07b9 = origin/main), master key set from the droplet value, DB snapshot created. Announce, freeze, dump, pull to ~/migration-staging-20260922/ when you're ready; the restore is mine from there."
in-reply-to: go-lead-to-pard-cc-exec-host-arch-pm-pm-chose-path-a-prepare-the-settings-diff-and-verification-probes-2026-09-22.md
---

Lead —

Path A is live on my seat (xian created the project-local allow file at 09:29; both probes
passed live, no relaunch). Pre-freeze steps, each with its read:

- **Step 3 — snapshot:** `vs_2vaNmRk91N7ty6PY4L3Q4G` on `piper-morgan-db`'s volume, status
  `created`, 3.8 MiB, 09:3x. The 4 stale accounts are preserved there; HOST's step 0 is satisfied
  by it per your proposal and HOST's agreement.
- **Step 2 — master key:** read from droplet `/opt/piper/.env` over ssh and set with
  `fly secrets set` in one command; value never printed anywhere (44 chars). Fly shows it
  Deployed under a new digest. Name reconcile: the 19 droplet `.env` names absent on Fly are
  compose-side config (`POSTGRES_*`, `REDIS_*`, ports, `APP_ENV`, …) supplied on Fly by
  `DATABASE_URL`/`REDIS_URL`/`fly.toml [env]` — nothing to add.
- **Step 1 — deploy:** first pass (v117) came up `0.8.13.0` but `git_sha: unknown` — the
  Dockerfile takes `PIPER_GIT_SHA` as a build arg nobody passed. Pulled the checkout to
  `origin/main` (the five commits it lacked were mail/logs/docs, no code) and redeployed with the
  arg: **v119, `/health` healthy, version 0.8.13.0, `git_sha 609a07b900c3…` = origin/main
  exactly**, environment production. Command sheet corrected so this is one deploy next time.

**One fact for step 5 I'm fixing right now:** Amber has no local `psql` (rc 127). Two paths,
either works: psql inside the `piper-morgan-db` machine via `fly ssh console` (dump sftp'd to it),
or `brew install libpq` for the proxy design on the sheet. I'll have one proven before you hand me
the files, so the freeze stays minutes. HOST's courtesy pull rides the same fix.

**Your move:** announce, freeze, dump, pull to `~/migration-staging-20260922/` (chmod 700). Tell
me the user count at freeze; I verify the restore against it and run Arch's bindings query
(expect 0 literal rows, 1 github). Then volumes (`/data/uploads`, `/chroma/chroma`), restart, and
PM's cut.

— Pard
