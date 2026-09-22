# Web carry-forward — 2026-09-22 (active)

**Spring-cleaned 2026-09-22** per context-floor plan item 4a (PM directive via Exec, top priority
today). Cut ~500 lines of resolved-thread narrative, a duplicate stale "Open" block, and a
compressed historical-pointers section — all fully covered by dated session logs, the durable
record per PM's 2026-06-12 ruling. Current state only, per Exec's worked example
(`dev/active/exec-carry-forward.md`).

**Session**: Amber / pipermorgan.ai, **Sonnet 5** (Opus 5 through 09-20, shifted post-reboot,
unrequested — explained, not unresolved: `feedback_cron_id_continuity_not_evidence_against_reboot`)
· cron `22 6,9,12,15,18,21 * * *` (job **`6c08fd70`**, delete-then-create 2026-09-21 21:52 STOP, was
`bd14e07d`, CronList-verified exactly one, expires ~2026-09-28) · registry row
`dev/active/duty-cycle-registry.tsv` line `web` · **offset is per-job and re-rolls on every
create** — use the documented bound (slot + up to 15 min historically observed, actually settled at
+30 on this job across every fire so far), never a remembered figure from a prior job.

## OPEN FOR PM — four items, all genuinely PM-side

1. **Vercel Deployment Storage figure** — probed before any number per Exec's warning; usage API's
   own metric enum has no deployment-storage type, dedup behavior unknown. Unreachable with the
   current token; PM's dashboard is the only confirmed source.
2. **Buttondown send question** — audit delivered 09-20. Does anything actually go out to
   subscribers? No send mechanism found in either repo; runbook step 9 is the LinkedIn newsletter,
   not Buttondown. PM-only answer; copy fix follows from it.
3. **Site walkthrough** (filed 05-29, 116d) and **obs-pass verdicts** (filed 06-17, 97d) — both
   prepped and ready (artifact: `pipermorgan-walkthrough-prep-2026-08-31.html`), waiting on a PM
   session. Not Web's to close.
4. **`#1827` (mail-send.sh case-normalization)** — fixed same-day it was found (`348a83232`),
   **still not end-to-end confirmed** — every send since has had a header that couldn't exercise the
   old bug either way. Confirmation requires a send whose `to:`/`cc:` capitalizes a role name;
   don't manufacture one, check when it happens naturally.

## Standing owned item — context-floor plan (PM, 09-22: top priority today)

Web's parts: **item 4a** (this file, done this fire) and **item 2b pilot** (CIO's tick-skill Phase B
refactor — accepted, waiting on CIO's specific before/after text before anything starts; explicitly
no-rush).

## Active infrastructure Web owns

**GitHub criteria line** (third queue source, per PM's v1.33 ruling — "drained" = mail +
standing-items + this). Run both, open each hit with `gh issue view`, never judge from the list:

```bash
gh issue list --repo mediajunkie/piper-morgan-website --state open --limit 50
gh issue list --repo mediajunkie/piper-morgan-product  --state open --search "label:web" --limit 20
```

Website: no label filter, Web owns the repo outright. Product: `label:web` only — Web is one lane
among many there, and issues merely *filed* by Web (not owned) don't count.

**`scripts/heartbeat-interior-coverage.py`** — standalone diagnostic Web wrote, not wired into the
shared belt (CIO's lane). Session-clusters commit history to measure interior heartbeat coverage
that row-presence checks miss. Threshold-sensitive; cite the sensitivity table (45–60m defensible)
if anyone quotes a number from it.

**Web is the browser-automation pilot** (since 08-28) — headless Playwright via `npx playwright`
works on Amber; Chrome DevTools MCP does not (no executable). ⚠️ **Not documented until now**:
`playwright` resolves only via the npx cache, not either worktree's `node_modules` — set
`NODE_PATH=$(ls -d ~/.npm/_npx/*/node_modules/playwright 2>/dev/null | head -1 | xargs dirname)`
before invoking, or every script call fails with `Cannot find module 'playwright'`. Hit repeatedly
across multiple fires before being worth writing down.

## Environment facts worth re-verifying, not assuming

- **Two worktrees, two repos, same basename `web`** — disambiguate via `git remote -v`, not
  `basename "$(pwd)"`. Confirm before every commit.
- **`CronCreate` jobs are session-only, in-memory, never on disk**; recurring jobs auto-expire after
  7 days regardless. A job id surviving a suspected reboot/restart is `--resume` restoring the saved
  transcript, **not evidence the event was skipped** — see the reboot memory above.
- **No login credentials for the product app's shared dev server** — no self-serve `/register`, no
  documented test account. Blocks authenticated-view Playwright verification; pre-auth flows
  (redirects, public pages) are unaffected.
- **Local env has no `GITHUB_DRAFT_TOKEN` / `ADMIN_PASSWORD_HASH` / `ADMIN_SESSION_SECRET`** —
  exercises fallback branches only, not the real success path for compose API / live calendar read.

## This seat's standing errors (deduplicated, still live lessons)

- **A check that returns "nothing found" needs a known-good control before the nothing is believed**
  — the single highest-value habit on this seat (lazy-load images, a status-code check that can't
  tell a real page from a client redirect, a titles-only search that missed 98 real hits).
- **"Idle" inferred from zero commits is not idle** — a conversation, a `WebFetch`, or holding the
  REPL in any way produces no commit but is not idleness. Use last-tool-call time + absence of
  tool-result writes instead.
- **Cite the source, not the summary of the source** — the website#37 citation and the workDate
  "placeholder" conclusion (2026-09-20) were both cases of reasoning from a carried summary instead
  of opening the actual document/asking the actual person who had the record.
- **Filename-case gotcha in mail triage**: this filesystem is case-insensitive, git is not — always
  copy the exact filename from `ls` output, never retype from memory.
- **Sync BEFORE checking mail, never after** — a stale worktree makes an empty inbox
  indistinguishable from a drained one.

## Notes carried from predecessor, unverified by me

- Product-repo git: always absolute `git -C` paths (cwd drifts across reconnects).
- Worktree `node_modules` is a real install; Turbopack panics here → plain `next dev`.
- Secrets recipes: stdin-based only, never argv (zsh mangles).

## PM design preferences, stated directly (08-15)

- GitHub-API-backed, always-current reads with no local-checkout dependency (the compose editor's
  shape) is the right pattern for any new admin/tooling read surface — praised unprompted because it
  doesn't depend on PM managing the repo well.
- Cross-project reads (e.g. Dispatch) should hit `origin/main` directly, not a bounded-lag mirror or
  PM's local checkout.
