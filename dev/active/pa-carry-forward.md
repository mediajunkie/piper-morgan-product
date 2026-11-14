# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-13 21:48; replace, don't annotate)

- **Served:** beta `81d149ac86` (11-13 16:34, #2366/#2367/#2368). MCP app `4666e38493` (v21). Read the live sha from `/health`, not from here.
- **#2342 connector rows (PA's, on xian's account via `piper://me/github/issues`):** row 1 PASS 11-12 19:15 (CXO ruled). **Next, row 2:** on Exec's word that xian has reconnected (sign-in only, nothing installed), read; expect the install line (or the "on our side" line if the slug is missing, which is itself the finding). Row 3 after he installs. Row 4 (UNREACHABLE) not served. Quote each to Exec, cc CXO, HOST, Lead, Arch, and on #2342. Count first-read "Connection closed" failures (13:18 and 19:15 on 11-12; warm read served) and report to CXO. Never read during a promotion.
- **MCP app redeploy after the rows close** (xian's `scripts/deploy-mcp.sh`): brings #2362 redaction and `uptime_seconds`. Re-check `7e32d63f68` is an ancestor after it.
- **1386 route RULED 11-13 17:53 (Arch, decisions.log):** xian signs in once on Web's chrome-devtools beta `/login` page; seats drive the profile; the session slides 7 days with use. No seat reads a password file (option (b) withdrawn, Arch NO). Web's page was open and signed out at 18:03. On his sign-in, **Web runs**: #2364 probe (3 rows), #2328 five, #2366 select, #2367 gemini POST, and **Q12** in PA's order (`01M7BW7MKJ2QJDNRDCQ0V06FN2`; plan `dev/2026/11/13/known-limits-served-reads-plan-2355.md`). Results come to PA and Docs; **PA writes them on #2355 and asks for the #2364 after-fix run** (Q13).
- **Tier 1 staging account:** approved in principle; waits on xian's five name-and-count queries on staging (Arch `01M7BXGYZDJDA660J2AEM13MCG`). A staging read records both shas plus Lead's per-row diff.
- **#2364:** step 1 built and held on `lead/2364-step1`; Lead's live run of about 26 probes needs a provider key (xian/Exec). The ethics default flips to on after step 1 is served (xian, 17:56).
- **xian's Fly log read** for #2362/#2350: Arch's fresh probe 17:47:45 on `81d149ac86`; pass line uses the 16:34 start.
- **xian's keychain rule (11-11):** nothing we run reads his login keychain without permission.
- **Inspecting an old commit:** scratch `git worktree add --detach`, never `git checkout <sha>` here. **No python with `requests` on PATH:** use a scratch venv before running a driver.
- **Q9:** #2313 on its build; CXO's #2294 row. **#2288**, **#2242**, **#2238**: see PM Attention. **Q8** on the invite hold lifting. **R7 (#1282):** README needs a permitted push. **#2174:** read only.
- **mail4 gotchas:** `--cc a b c` (space-separated); `--type` is one of fyi, task, decision-request, ruling-relay, reply, canary. A `cannot lock ref` or a timeout on fetch: retry. Ack `read`, not `done`, when work is still owed.
- **Sprint 2 started Fri 11-13.** v3 is the mail fallback until 11-23. START: `python3 scripts/owed-scan.py --role pa`.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 held-token row**, since 11-03: xian runs `mcp_allow.py remove` on his account (then re-adds).
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **Served-check sign-in**, since 11-10 18:25, route ruled 11-13 17:53 (Arch): xian signs in once as web-seed-1386 on Web's open chrome-devtools beta `/login` page and tells Exec. Web then runs #2364, #2328, #2366, #2367 and Q12 in one sitting. Separately, tier 1 (staging account) needs xian's five staging queries (Arch `01M7BXGYZDJDA660J2AEM13MCG`).
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
