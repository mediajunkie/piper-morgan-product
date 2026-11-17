# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-16 06:47 START; replace, don't annotate)

- **Served (06:47):** beta `460b837a47`; MCP `dfebe7f0b7` (uptime 43136 s, no restart since xian's 18:49 11-15 deploy). Read the live sha from `/health`. Beta promotion GRANTED from 07:00 (Arch, six conditions). Never read the connector during a promotion.
- **ADR-084 ACCEPTED (xian 11-16 06:20 via Exec `01M7JBP51M…`):** $10 a run without asking; `lead-scoring` workspace $150/month as the bound. PPM places `seat_session.py`, `seat_account_create.py`, `ops_reader`, #2384. Paid runs stay stopped until Step A lands and Lead's check passes. Step A read tests are Lead/HOST/CIO, not PA.
- **#2379 served rows (Lead 11-16 18:16):** beta `74caa06638`. One ordinary turn, the uninstalled-repo read refusal, five write refusals with no confirm first, one installed-repo control. PA can't run them (the connector has no chat; no seat chat on beta). They wait on `seat-github-1` (F0/F) plus D3's seat browser (Web's lane) plus a seat-workspace key. PA writes the quotes up for CXO. Replied `01M7KN2J5E…`.
- **Pre-push hook remembers a pass (CIO 11-16 12:53, recipe 5):** push the branch checked out. The first time a push of PA's prints `already passed on this content N min ago`, mail CIO that line (CIO's one ask).
- **CIO seat rule (11-16, corrected 09:55, recipe 14):** never run `scripts/alpha-setup.sh` on Amber; never `docker compose up`/`down` on the shared stack from a worktree; after a reboot `docker start piper-postgres piper-redis piper-chromadb`. (`stop.sh`, `start.sh`, `db_migrate_to_volume.sh` deleted; `run_tests.sh` no longer starts services.)
- **PA's ADR-084 items:** (1) **#2384** MCP deploy job (Lead builds now; xian's token goes in an environment limited to `main`, though row 7's wording is for Arch to align). Its first run deploys **#2382** (stateless MCP, on main `40523ea6b9`). Then **PA reads row 4**: MCP `/health` sha plus `uptime_seconds`, and one connector read that must serve on the first try. Quote it to CXO and on #2382. (2) A **second connector "Piper Morgan (seat)"** consented as the GitHub-connected seat account (card row 9: allowlist write plus consent, xian's one try; if claude.ai refuses a second connector, stop and tell Exec). The seat account's zero-install read comes between connect and install, so ask Web to connect first.
- **#2342:** rows 1 and 3 PASS; the #2374 connector reach PASSED (CXO 18:58: 366 to 1, `pipermorgan/piper-test` only). Open: the zero-install line (needs the seat account), the named-repo refusal, the too-many line, row 4 (UNREACHABLE). Record `uptime_seconds` beside every first connector read ("Connection closed": 2 of 2 after deploys, 1 of 3 without).
- **#2375/#2376 (CXO 19:16):** #2376 PASS for an App account with no token. The #2375 link FAILED; Lead's card version `144745bf7d` (validated; CXO passed the words, with the no-slug note changed) is to land and promote 11-16.
- **Web's served reads** (#2364 ×3, #2328 five, #2366, #2367, Q12, #2294 cases 1–2, #2295) now ride ADR-084 D3 (`seat_session.py` helper plus a persistent seat browser), not a xian sign-in. Results come to PA, who writes them on #2355 and asks for the #2364 after-fix run (Q13).
- **#2364:** step 1 held on `lead/2364-step1`; option (a) (xian runs it) is withdrawn. It runs on the seat key (ADR-084 A) after xian's yes.
- **Tier 1 staging account:** waits on xian's five staging queries (Arch `01M7BXGYZD…`). That may become ADR-084 C endpoints.
- **xian's keychain rule (11-11)** stands. **Inspecting an old commit:** a scratch `git worktree add --detach`. **No `requests` on PATH:** use a scratch venv.
- **Q9:** #2313; CXO's #2294 row. **Q8** on the invite hold. **R7 (#1282):** README needs a permitted push. **#2174:** read only.
- **mail4 gotchas:** `--cc a b c`; `--type` is one of fyi, task, decision-request, ruling-relay, reply, canary. On a `cannot lock ref` error, retry. Ack `read` when work is owed. zsh: never `echo ==...` (it errors as `=` expansion).
- **Sprint 2 started Fri 11-13.** v3 is the mail fallback until 11-23.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 removal check**, since 11-03: Exec agreed 11-16 (`01M7KN3SAN…`). It is now Step G part 3 on `seat-github-1` (`d909c9af5a`), and Arch's read was asked in `01M7KN873G…`. It runs in xian's Step G sitting; no separate card. The MCP test-plan card was cut as overtaken.
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **ADR-084 one-time rows**, since 11-15 19:11; xian said yes 11-16 06:20. Remaining PM-hand rows: Step A (this morning), the #2384 deploy token (Step H, after the job is built), Step G for PA's seat connector (after F0/F). Separately, tier 1 needs xian's five staging queries (Arch `01M7BXGYZDJDA660J2AEM13MCG`).
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
