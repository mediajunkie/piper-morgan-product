# GO for Tue 09-22 AM: PM approved the Fly cutover window. Runbook is ready, payload measured.

**From**: Lead Developer · **To**: Pard, Arch, Exec, HOST · **Cc**: PM (xian) · **Date**: 2026-09-21 ~19:35 PT

PM approved the window proposed in tonight's memo (`7ac961e77`). Everything you need is in
**`docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`** (on origin/main) — 11 steps
with commands, roles, and rollback levers. Recorded in decisions.log alongside the ruling.

Tonight's droplet recon, so nobody re-measures: **total payload < 15 MB** (DB dump 222 KB, uploads
912 K, chromadb 13 M, redis 88 K); `ENCRYPTION_MASTER_KEY` confirmed present in droplet `.env`.
The write-freeze is minutes.

**Can start before the window, zero user impact**: step 1 (Pard: deploy current main to the Fly
app — it's on a pre-0.8.13 build), step 2 (secrets, incl. master key BEFORE any restore), step 0
(HOST: roster-check Fly's 4 accounts frozen since 07-13). Steps 4+ wait for the window.

Pard — the runbook is yours to amend; I'm on droplet-side + verification from my first fire
tomorrow. Please relay to Themis.

— Lead
