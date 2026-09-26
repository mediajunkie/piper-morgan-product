# Web carry-forward — 2026-09-26 (active)

**Spring-cleaned 2026-09-22** per context-floor plan item 4a. Current state only — full narrative
for anything below lives in the dated session log, not here.

**Session**: Amber / pipermorgan.ai, **Sonnet 5** · cron **`22 6,13,20 * * *`** (job **`49196fa9`**,
cut from 6x/day to 3x/day 2026-09-26 08:5x per PM/Exec usage-pacing directive, effective through
Monday — see registry row for full detail) · registry row `dev/active/duty-cycle-registry.tsv`
line `web`.

⚠️ **Real-world gap, 2026-09-25 18:38 → 2026-09-26 08:51 (~14h)**: a tool-approval prompt sat
unanswered (user's words: "wedged"), not a crash/compaction. The 21:22 STOP and 09-26 06:22 START
both missed in real time — retroactively reconstructed same-fire (09-25 log backfilled + wrapped +
`DAY-CLOSED`; 09-26 log created fresh). Docs independently flagged the same gap via the new Step 1d
nudge; replied confirming it was already fixed by the time the nudge landed. No other role affected
— confirmed via their own same-day session logs.

## ⭐ Alpha wizard walkthrough — CLOSED 2026-09-25/26, end-to-end

PM provisioned a real Anthropic key into the Amber login keychain (`pm-web-anthropic-key`); Web
stored it via a direct, secret-never-printed API call (`/api/v1/auth/login` + `/api/v1/keys/store`,
both request/response shapes read from source rather than guessed) and then verified live in the
actual browser: `/settings/llm-keys` shows `anthropic — validated`, and a fresh chat message got a
real completion from Piper ("Yes, all good on my end... Running with a default configuration").
**Test-card rows 5/6 (blocked all week on "no LLM key") are now unblocked** — pick up on a future
fire, not urgent.

`web-agent` account: created via the actual `/create-user` + `/auth/login` API after the `/setup`
wizard's Step 1 was found hard-blocked for every new user (fixed same-day, see Lead's fix).
Credentials: `/Users/xian/.piper-shared/web-agent-alpha-credentials.txt` (mode 600).

Same 09-24 fire: traced and visually captured **#1859** (chat-switch white-flash, closed same week
after a second, more precise diagnosis) and filed **#1874** (intermittent 503s, closed same-day).

## OPEN FOR PM — two items remain (two of four closed 09-25/26)

1. ~~**Vercel Deployment Storage figure**~~ — **CLOSED 2026-09-25** via Exec's sprint-plan memo,
   citing PM's own number: 527 MB post-retention, verified healthy.
2. **Buttondown send question** — audit delivered 09-20. Does anything actually go out to
   subscribers? No send mechanism found in either repo; runbook step 9 is the LinkedIn newsletter,
   not Buttondown. PM-only answer; copy fix follows from it.
3. **Site walkthrough** (filed 05-29) and **obs-pass verdicts** (filed 06-17) — both prepped and
   ready (artifact: `pipermorgan-walkthrough-prep-2026-08-31.html`), waiting on a PM session. Not
   Web's to close.
4. ~~**`#1827` (mail-send.sh case-normalization)**~~ — still not naturally exercised; low-priority,
   check opportunistically only, not worth chasing.

## ⚠️ Standing PM/Exec directive — usage throttle through Monday (2026-09-26)

PM: week burned 20% of usage credits in the first 31 hours (1.08x pace, no reset cushion). Exec's
three asks, all complied with this fire: **(1)** cut idle fire cadence ~40-50% — done, 6x/day →
3x/day (`22 6,13,20 * * *`); **(2)** hold non-essential subagent dispatch/audits/big-synthesis
unless PM asks or something's genuinely blocking — Web rarely dispatches subagents anyway, nothing
to change; **(3)** route non-essential updates through the attention rollup rather than new
fleet-wide broadcasts — noted, nothing broadcast-worthy pending. Revisit Monday; restore to
`22 6,9,12,15,18,21 * * *` unless PM/Exec extend the throttle.

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
