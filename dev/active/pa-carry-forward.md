# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-12 21:49; replace, don't annotate)

- **Served:** beta `d4fd55e6c5` (11-12 11:52; #2342 App mode ON since xian's 17:25 sitting). MCP app `4666e38493` (v21). Read the live sha from `/health`, not from here.
- **#2342 cutover APPLIED 11-12 19:06:** 10 of 10 classic tokens revoked at GitHub, 0 left. App "Any account", alpha and beta callbacks.
- **#2342 connector rows (PA's, on xian's account via this session's connector, `piper://me/github/issues`):**
  - Row 1 (cutover line) PASS 19:15, and CXO ruled PASS. On #2342 (issuecomment-6842746817).
  - **Next, row 2:** on Exec's word that xian has reconnected (sign-in only, nothing installed), read and expect the install line. If the slug isn't on the MCP app, it gives the "on our side" line instead, which is itself the finding.
  - Row 3: after he installs (can be his `mediajunkie` account), read again.
  - Row 4 (UNREACHABLE): mark not served.
  - Quote each reply to Exec, cc CXO, HOST, Lead, Arch, and on #2342.
- **Connection closed:** the first read after a long gap failed at 13:18 and 19:15; the warm read at 19:26 served. Count first-read failures at rows 2 and 3 and report them to CXO (E6 question, not filed).
- **Beta promotion** refused by the gate at 20:36 (#2363: the ancestor walk follows the first parent only). It goes 11-13 after 07:00 with #2350 and #2362. PA reads only after `/health` shows the announced commit, never during a promotion.
- **MCP app redeploy after rows 2 to 4 close** (xian's `scripts/deploy-mcp.sh`): it brings #2362 redaction (the MCP entry point had none) and `uptime_seconds` (`f326229e78`). Re-check `7e32d63f68` is an ancestor after it. Arch agreed: no MCP deploy mid-rows.
- **Main Tests red at 21:47** (run 43370392319, `875c051bee`, new failure `test_install_url_redaction_filter_adds_to_httpx`); mailed Lead `01M79Q7PPX3K0Y7FP58PJ0F5X2`. Re-check at START.
- **PA's served-check lane is DOWN since 11-10 18:25** (the 1386 credential file is `key: value`; the drivers want `key=value`; the read is classifier-refused). The decision reminder went to Exec 11-12 21:48 (`01M79Q8226TJGVZ9XK9FAC0K1X`); don't re-send. Don't retry or route around it.
- **#2328:** OPEN, 0 of 5 served. Lead's 18:58 cases are in `mailboxes/pa/read/`.
- **xian's keychain rule (11-11):** nothing we run reads his login keychain without permission.
- **Inspecting an old commit:** scratch `git worktree add --detach`, never `git checkout <sha>` here.
- **No python with `requests` on PATH:** use a scratch venv before running a driver.
- **Test account web-seed-1386 (11-09 21:47, untouched since):** 8 open, unchanged from the 11-11 list.
- PA can't sign in to other seats' accounts (classifier).
- **#2174:** github-mcp-server version line from xian's #2341 run; read only.
- **Q9:** #2313 on its build; CXO's #2294 bulleted-list row. **#2288**, **#2242**, **#2238**: see PM Attention. **Fresh-account checks (Q8):** on the invite hold lifting. **R7 (#1282):** README needs a permitted push.
- **mail4 gotchas:** `--cc a b c` (space-separated, not commas); `--type` is one of fyi, task, decision-request, ruling-relay, reply, canary. A `cannot lock ref` on fetch is a concurrent fetch: retry.
- **Sprints are two weeks from Fri 11-13.** Mail v4 is checked every fire; v3 is the fallback until 11-23. START: `python3 scripts/owed-scan.py --role pa`.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 held-token row**, since 11-03: xian runs `mcp_allow.py remove` on his account (then re-adds).
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **PA served-check sign-in**, since 11-10 18:25 (decision reminder to Exec 11-12 21:48, 01M79Q8226TJGVZ9XK9FAC0K1X): the classifier denies PA reading `~/.piper-shared/web-seed-1386-credentials-2026-10-20.txt` (twoturn.py finds no `username=` key; listing field names was denied too). Cause confirmed 11-11: the file is `key: value`, the drivers want `key=value`. Unblocks on either: xian allows the read, or a `username=`/`password=` file for the account. Sent to Lead, cc Exec 18:25 (e1d0c6b3b). Until then served checks go to Web (Lead routed #2328 there at 18:37).
- **Rename PA (xian's idea 10-28):** trigger was MVP reading 0 open, which happened 10-30. Raised to Exec 11-06 (late). xian's call; no work blocked.

## Cadence

LaunchAgent `com.xian.pm-pa-cycle` (:47 at 6, 9, 12, 15, 18, 21), boot-persistent, Pard-owned. No session cron; `CronList` empty is normal. Registry row `pa` reads LaunchAgent since 09-30.

## MCP program (card priority 1)

- **Deploys:** only `scripts/deploy-mcp.sh`. PA's own run is classifier-denied since 11-04; give xian the one-line sync-plus-deploy (memory `reference_deploy_mcp_clean_tree_races_cohort_pushes`). A sanctioned `gh workflow run` deploy would remove the human hand (proposed in Agent 360 v0.6).
- **Auth:** issuer `https://alpha.pipermorgan.ai/mcp/oauth` (constant; `MCP_OAUTH_ISSUER_URL` overrides). `/authorize` always renders consent; allowlist (#2242) gives unlisted accounts a 403. Access token 1 h; refresh 30 days, rotating.
- **Live reads:** this session's connector, `mcp__claude_ai_Piper_Morgan_Alpha_MCP__what_piper_knows_about_me`.
- **Test plan for xian:** `docs/internal/operations/mcp-test-plan-pm.md` (10-31, updated for v18).

## Standing mail rules

- Never cc or address PM; anything needing PM goes to **exec**, naming decision / ruling-relay / would-contradict in the subject.
- zsh doesn't word-split: pass `mail-send.sh` paths via a list file and `xargs`. Path cap 180 including the `mailboxes/<role>/inbox/` prefix.
- Never stage `dev/state/pa-last-pm-scan`.

## GitHub-criteria line (third work-queue source, v1.33) — DEFINED 2026-09-23

Two cheap queries, matching the two halves of PA's lane (ROSTER: skunkworks PoC coordination +
PM-bandwidth extension). **Open every hit with `gh issue view N` before writing a row anywhere**
— a list is a fragment (CXO's finding).

1. **Skunkworks/BYOC**: open issues referencing the hosted-MCP epic —
   `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+%221462%22"`.
   Denominator 2026-09-23: **12** (epic + increments #1701–1707 + #1514/#1509/#1632). Action on a
   NEW number: read it; update the readiness checklist / parallel-work plan if it changes
   sequencing or ownership; add to PM Attention only if it's genuinely PM-gated.
2. **PM-bandwidth**: `gh api "search/issues?q=repo:mediajunkie/piper-morgan-product+state:open+label:awaiting-decision"`.
   Denominator 2026-09-23: **0** — the label exists but nobody applies it; an empty source is a
   fact, not a failure. Action on a hit: verify it's PM-gated, then PM Attention above.

Seen-set lives in `dev/state/pa-gh-criteria-seen` (not sprint-cleaned); "newly observed" = in
today's query, absent from the file. Rejected alternatives, so nobody re-derives them:
`label:mcp` (5 stale pre-PDR-006 DIST issues — wrong era), free-text `byoc OR mcp` (24 hits,
half unrelated).
