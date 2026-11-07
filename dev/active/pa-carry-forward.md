# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-07 12:47 WORK; replace, don't annotate)

- **Served:** beta `8633405573` (D5 measurement build, `D5_CONSULT_CEILING_S = 5.0`) as of 12:47; MCP `/health` 200. Read the live sha from `/health`, not from here.
- **Since #2282 (11-05), alpha redirects to beta** except the MCP OAuth paths, the well-knowns, `/login`, the login POST, `/static`, `/assets`, `/health`. **Scripts target beta** (`dev/2026/11/06/turn.py`, run from `dev/2026/11/07`).
- **#2318 row 5:** binds 5 of 5 at 5 s; the extra 2 to 3 s is app-side (Lead 12:17). Next promotion is Lead's diagnostic build (`latency_ms`, 1.5 s stall watch, Arch 12:28). On it: row 5 three to five times, **one disposable per run** (complete writes with no confirm). If the round doesn't name the cause, the following promotion ships at most 2.5 s (Arch 12:43, Exec 12:36; 3.0 s is put to xian). Then row 5 at the shipped ceiling.
- **Armed-pick rows owed once served:** reminder-clear arms (`d6e23453d1`, validated); Lead's sites 1 to 4 (complete and delete "Which one should I …?" with no list or unresolved); clear sites 5 and 6 wait on CXO's pick among (a)/(b)/(c).
- **Test account web-seed-1386:** 8 open. `review the deployment plan` and `draft the launch checklist` were re-added 12:11 and sit at lines 6 and 7.
- **Q9 also:** #2313 ("delete A and B") on its build; CXO's #2294 bulleted-list row.
- **#2288** (card says "Connected." on a 401 grant): served row needs a dead-grant account; xian's word for Web.
- **#2242 (Q2):** held-token row, on xian's `mcp_allow.py remove` relayed by Exec.
- **#2238:** xian's Notion key on staging, then Web runs `dev/2026/11/01/notion-chat-check-2238.py`.
- **Fresh-account checks** (Q8): on the invite hold lifting (#2261, #2282, #2292) and HOST's slot with xian.
- **R7 / plugin (#1282):** README edit needs a permitted push or xian's hand. Standing item 2.
- **Mail v4** opens to every seat Mon 11-09; then also `python3 scripts/mail4.py inbox --role pa`. v3 fallback until 11-23.
- **START habit:** `python3 scripts/owed-scan.py --role pa`.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

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
