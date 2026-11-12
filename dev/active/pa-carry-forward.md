# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-11 21:50; replace, don't annotate)

- **Served:** beta `c425fd242f`. MCP `/health` 200. Read the live sha from `/health`, not from here.
- **Since #2282 (11-05), alpha redirects to beta** except the MCP OAuth paths, the well-knowns, `/login`, the login POST, `/static`, `/assets`, `/health`. **Scripts target beta.**
- **PA's served-check lane is DOWN since 11-10 18:25.** Cause confirmed (10-22 log line 23): the `~/.piper-shared` credential files are `key: value`, the drivers (`twoturn.py`, `turn.py`) expect `key=value`, and the old process-substitution conversion is now classifier-refused. With Exec and Lead for xian; on PM Attention. Don't retry or route around it. **If 11-12 ends with no ruling, mail Exec once (decision in the subject).** Lesson: log the exact driver invocation (credential path shape, never contents) on every served run.
- **#2328 (pronoun target asks which one):** OPEN, 0 of 5 served. Web is blocked on the same file. Once unblocked, run Lead's 18:58 five cases (memo in `mailboxes/pa/read/`).
- **xian's keychain rule (11-11 11:12, decisions.log):** nothing we run reads his login keychain without permission. PA's 1386 harness fallback is removed (`5ea17b4b6b`); the shared binder is fixed (#2340, `5f31a9fb76`). Rule-7 screens wait on xian's key handover (Lead via Exec).
- **Inspecting an old commit:** use a scratch `git worktree add --detach`, never `git checkout <sha>` in this worktree (11-11 slip).
- **No python with `requests` on PATH:** make a scratch venv (`python3 -m venv <scratch>/venv && pip install requests`) before running a driver.
- **Test account web-seed-1386 (11-09 21:47, untouched since):** 8 open, in order: urgent task (urgent), zz throwaway one, zz throwaway two, audit the current navigation, **review prs (x2) on line 5**, review the deployment plan, draft the launch checklist. No reminders, no clear preference.
- PA can't sign in to other seats' accounts: the permission classifier denies it even with the owner's yes.
- **#2174:** github-mcp-server version line lands from xian's #2341 run; PA reads it there, no action.
- **Q9 also:** #2313 ("delete A and B") on its build; CXO's #2294 bulleted-list row.
- **#2288** (card says "Connected." on a 401 grant): served row needs a dead-grant account; xian's word for Web.
- **#2242 (Q2):** held-token row, on xian's `mcp_allow.py remove` relayed by Exec.
- **#2238:** xian's Notion key on staging, then Web runs `dev/2026/11/01/notion-chat-check-2238.py`.
- **Fresh-account checks** (Q8): on the invite hold lifting (#2261, #2282, #2292, #2322 done row) and HOST's slot with xian.
- **R7 / plugin (#1282):** README edit needs a permitted push or xian's hand. Standing item 2.
- **Sprints are two weeks from Fri 11-13**; the Ship stays weekly.
- **Mail v4:** every fire checks `scripts/mail4.py inbox` as well as the v3 inbox; v3 is the fallback until 11-23.
- **START habit:** `python3 scripts/owed-scan.py --role pa`.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 held-token row**, since 11-03: xian runs `mcp_allow.py remove` on his account (then re-adds).
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **PA served-check sign-in**, since 11-10 18:25: the classifier denies PA reading `~/.piper-shared/web-seed-1386-credentials-2026-10-20.txt` (twoturn.py finds no `username=` key; listing field names was denied too). Cause confirmed 11-11: the file is `key: value`, the drivers want `key=value`. Unblocks on either: xian allows the read, or a `username=`/`password=` file for the account. Sent to Lead, cc Exec 18:25 (e1d0c6b3b). Until then served checks go to Web (Lead routed #2328 there at 18:37).
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
