# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-06 START; replace, don't annotate)

- **Served:** alpha and beta `4e4c3fb1a8` as of 11-05 21:47. **MCP Fly v20 `28911350bb`** (xian deployed 11-05; carries the GitHub guard). Read the live sha from `/health` and `fly releases -a piper-morgan-mcp`, not from here.
- **Since #2282 (11-05), alpha redirects to beta** except the MCP OAuth paths, the well-knowns, `/login`, the login POST, `/static`, `/assets`, `/health`. **Scripts target beta** (memory `reference_api_scripts_target_beta_alpha_redirects_drop_auth`).
- **#2282 MCP lane:** (a) and (c) PASS 11-05 12:48; (b) re-add with no loop. Open: xian's read of `beta.pipermorgan.ai/settings/connected-apps` (one or two Claude rows) and revoke of an older one; then PA re-reads through the connector.
- **#2288** (card says "Connected." on a 401 grant): built, served, Arch-validated. Served row needs a dead-grant account nothing has read; five untouched dinp-machine accounts qualify (owner seats, or Web with xian's word).
- **#2262:** nothing-new line served PASS 11-05 21:49; CXO judges.
- **#2242 (Q2):** held-token row, on xian's `mcp_allow.py remove` relayed by Exec.
- **#2238:** xian's Notion key on staging, then Web runs `dev/2026/11/01/notion-chat-check-2238.py`.
- **Fresh-account checks** (A1, A2, first-reply notice, #2225 re-ask): on the invite hold lifting (#2261, #2282) and HOST's slot with xian.
- **R7 / plugin (#1282):** second Production track after the first sprint (xian 10-31 21:17); date from xian's sprint-cadence talk (Exec raises it). PPM places PA's input on #1282. Standing item 2.
- **Card:** served-run checks are priority 3 since 11-06 (Exec yes).
- **Mail v4** opens to every seat Mon 11-09; then also `python3 scripts/mail4.py inbox --role pa`. v3 fallback until 11-23.
- **START habit:** run `python3 scripts/owed-scan.py --role pa` (missed every START 10-23 to 11-05).

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **Connected apps read and revoke (#2282 b)**, since 11-05: xian opens `beta.pipermorgan.ai/settings/connected-apps`, says how many Claude rows, revokes the older one.
- 🔒 **#2242 held-token row**, since 11-03: xian runs `mcp_allow.py remove` on his account (then re-adds).
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
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
