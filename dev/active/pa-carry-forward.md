# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-27 21:47 STOP; replace, don't annotate)

- **Served (11-27 21:47, read from `/health`):** beta `8ddd08d8e0` (promotion 7: 2470's decline and the 2468 fix). **MCP `c303931894`**, uptime 118339 s, no restart since 11-26. 2468's fix (`32ba51b768`, connect-required line no longer follows the MCP app's App mode) is on main and beta but **not on MCP**; MCP's served line is still the correct one, because `c303931894` predates promotion 6.
- **MCP deploy HOLD:** both `deploy_mcp` dispatches on 11-27 hung (issue 2472, https://github.com/mediajunkie/piper-morgan-product/issues/2472, open). No more dispatches until 2472 has a cause (needs xian's Fly read through Exec) or Lead's step-timeout change (issue 2471, limits 20/15/20 min, Arch accepted; waits on xian's yes) lands. Then deploy, read `/health` sha and `uptime_seconds`, and 2468's served read on an account with no GitHub connection.
- **No `fly` from a seat, read-only included** (ADR-084; Exec `01M8FZDRED…`). PA's 11-27 violation is logged and reported to HOST. **fly-deny refusal test:** when Exec says xian ran CIO's `fleet-deny` paste (on xian's card; `e6c625572a`), type `fly version`, `/opt/homebrew/bin/flyctl version`, `FLY_NO_UPDATE_CHECK=1 fly version`; each must be refused; quote each refusal whole to CIO, Exec and HOST the same hour; stop at the first one that runs.
- **Promotion reads:** check the MCP server's import closure, not just `services/mcp` (`resources.py` imports `consumer/github_adapter`, `collaboration_gate`, `verified_inference`). Closure script in the session scratchpad, `closure.py` (static AST walk from `services.mcp.server.app`; recreate if the scratchpad is cleared).
- **xian 11-27 (Exec `01M8F6RY8H…`):** sprint 3's top priority is opening beta invitations; the invite-hold path (2261, 2282, 2342, the invite lift) comes first. The GitHub move cutover was DONE 11-27 `13:32`.
- **Step G (a) seat check, next PA action on xian's word via Exec:** xian adds `Piper Morgan (seat)` at `https://mcp.pipermorgan.ai/mcp?client=seat` (not during a promotion). Then: a second Piper server in ListMcpResources; `piper://me/profile` names seat-github-1; `piper://me/github/issues` shows piper-test only; quote `uptime_seconds`; one read of xian's own connector; results to Exec and HOST the same hour; then part 3 to HOST. If (a) fails: (c) per the steps file (xian's yes, one `piper-seat` token, HOST's four conditions), then the Ending. Then the zero-install read (xian said wait), the revoke (machine account's own authorization only; never uninstall the App from the org), PA's last read. Q14: switch Step G to `--username` when 2445 is served.
- **Clock rule (CIO 11-18):** no estimated minutes anywhere committed or mailed; quoted times in backticks; log headings via `scripts/log-entry.sh`.
- **`piper-morgan-test` key:** workspace limit $40.00, $17.33 spent at 11-26 (resets Dec 1 UTC). Log planned turns before a sitting. Spend asks short, not framed as a risk.
- **#2401/#2402:** behind xian's go-ahead to mint `seat-tester-1`. **#2342** open rows: zero-install line, named-repo refusal, the too-many line, row 4; record `uptime_seconds` beside every first connector read. **R7 (#1282)** waits on the #2242 allowlist.
- **Standing seat rules:** browser only via the helper (Step 1j check every fire); never `scripts/alpha-setup.sh`, never `docker compose up/down`; on the first `already passed on this content N min ago` push line, mail CIO.
- **mail4 gotchas:** `inbox --role pa`; `--cc lead host` (space-separated); `ack <id> done --as pa`; a subject naming a day needs `--due none`; on `cannot lock ref` or "NOT MEASURED", retry; loop the push until `origin/main..HEAD` is empty. zsh has no `timeout`. v3 `mail-send.sh` is for outside parties and Spec only.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 removal check**, since 11-03: Exec agreed 11-16 (`01M7KN3SAN…`). It is now Step G part 3 on `seat-github-1`. Arch said it conforms with two additions, and HOST asked two small things; all four are in `50ebf686e0`; Arch's final read (11-16 18:47): conforms. It runs in xian's Step G sitting; no separate card. The MCP test-plan card was cut as overtaken.
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **ADR-084 one-time rows**, since 11-15 19:11; xian said yes 11-16 06:20. Remaining PM-hand rows: Step F from F.2 on, and Step G parts 1 to 3 (A, D and F0 done 11-20), the #2384 deploy token (Step H, after the job is built),
- **Rename PA (xian's idea 10-28):** trigger was MVP reading 0 open, which happened 10-30. Raised to Exec 11-06 (late). xian's call; no work blocked.

## Cadence

LaunchAgent `com.xian.pm-pa-cycle` (:47 at 6, 9, 12, 15, 18, 21), boot-persistent, Pard-owned. No session cron; `CronList` empty is normal. Registry row `pa` reads LaunchAgent since 09-30.

## MCP program (card priority 1)

- **No `fly` from a seat, read-only included** (ADR-084; PA's briefing; Exec `01M8FZDRED…`, 11-27). Release state comes from the deploy run, MCP `/health`, or xian through Exec.

- **MCP deploy HOLD (11-27, written 16:42):** main from `305499bbfb` would serve the wrong connector connect-required line (issue 2468: `app_mode()` is always off in the MCP app). 2468 fixed on main (`32ba51b768`) but not served: both `deploy_mcp` dispatches hung on 11-27 (issue 2472); no more dispatches until 2472 has a cause or Lead's change lands. MCP stays `c303931894` (correct line). On every promotion read, check `services/mcp/server/resources.py`'s imports from `consumer/`, not just the directory.

- **Deploys:** only `scripts/deploy-mcp.sh`. PA's own run is classifier-denied since 11-04; give xian the one-line sync-plus-deploy (memory `reference_deploy_mcp_clean_tree_races_cohort_pushes`). A sanctioned `gh workflow run` deploy would remove the human hand (proposed in Agent 360 v0.6).
- **Auth:** issuer `https://alpha.pipermorgan.ai/mcp/oauth` (constant; `MCP_OAUTH_ISSUER_URL` overrides). `/authorize` always renders consent; allowlist (#2242) gives unlisted accounts a 403. Access token 1 h; refresh 30 days, rotating.
- **Live reads:** this session's connector, `mcp__claude_ai_Piper_Morgan_Alpha_MCP__what_piper_knows_about_me`.
- **Test plan for xian:** `docs/internal/operations/mcp-test-plan-pm.md` (10-31, updated for v18).

## Standing mail rules

- Never cc or address PM; anything needing PM goes to **exec**, naming decision / ruling-relay / would-contradict in the subject.
- **Done-note rule (xian 11-23, decisions.log `18:41`, Exec `01M85PWK3T…`):** when xian finishes something with PA (a step he ran, a word he gave, a card item closed), send Exec a one-line done-note in the same turn PA records it. Before relaying anything to xian, check the primary record so it isn't stale.
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
