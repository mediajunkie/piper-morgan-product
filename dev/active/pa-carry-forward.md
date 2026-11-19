# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-18 21:47 STOP; replace, don't annotate)

- **Served (11-19 09:47):** beta `f34fe7bef5` (CXO stale sentences in one map, `STALE_FACTS`; connector line unchanged); MCP `dfebe7f0b7` (uptime 269928 s, no restart since xian's 11-15 deploy), so the connector still serves the old stale-token line until the next MCP deploy (CXO accepted 11-18; no extra deploy). Read the live sha from `/health`. Never read the connector during a promotion.
- **Clock rule (CIO 11-18, `752547e88e`):** no estimated minutes anywhere committed or mailed; quoted times in backticks; log headings via `scripts/log-entry.sh`.
- **xian away from Amber until Fri 11-20 (Exec 11-17 18:27).** Steps A, C, D and F0's script half wait until his Friday sitting (order A, C, D, F0, F; G after F if time). So the signed-in reads, the seat browser's first run, `seat-github-1` and Step G wait until then at the earliest. Step H waits on #2384, not on Amber. PA's note `01M7P89JH1…`. When Exec mails "Step A started", don't run `sync-pm-local.sh` until "done" or "stopped".
- **PA's ADR-084 items:** (1) **#2384** MCP deploy job: OPEN, 3 comments, nothing built (Lead). Then Step H (xian's token). Its first run deploys **#2382** (stateless MCP). Then **PA reads row 4**: MCP `/health` sha plus `uptime_seconds`, and one connector read that must serve on the first try; quote to CXO and on #2382. That deploy also carries CXO's stale-token words (`85c4717da1`); quote the served line to CXO (PA's mail `01M7R6PJJ4…`). (2) **Step G** (final, `50ebf686e0`) after F0 (#2389) and F; PA's zero-install read between connect and install; part 3's result to HOST's custody row; on FAIL file on #2242 the same hour.
- **`piper-morgan-test` key (xian 11-17):** nothing of his uses it; seats may spend through it. Arch: conforms to D2. xian's console 11-17: $16.19 of **$40** spent (resets Dec 1 UTC), so plan against about $23.81. HOST's custody answer was owed at 13:36. Keep-true: log planned turns before a sitting; a turn is several model calls; a pause stops every seeded account's chat.
- **Spend tone (xian 11-17):** agent spend is nominal inside the monthly credit; still track (caps, PLANNED/COST lines, $10 a run). Write spend asks short and don't frame them as a risk.
- **#2379 served rows (Lead):** wait on `seat-github-1`, #2400 and the test key above. Not routed to xian's screen. PA writes the quotes for CXO. **#2401/#2402** are open for a signed-in read on the same route.
- **Web's served reads** (#2364 x3, #2328, #2366, #2367, Q12, #2294, #2295) ride Steps C and D. Results go to PA for #2355; then ask for the #2364 after-fix run.
- **#2342:** open rows: the zero-install line (needs the seat account), the named-repo refusal, the too-many line, row 4. Record `uptime_seconds` beside every first connector read.
- **Browser-launch guard (CIO 11-17):** a Bash hook refuses an unflagged Chrome/Chromium launch (heredoc text going to a file is exempt since `aafb9da58a`). **Step 1j**, `scripts/browser_keychain_check.py`, runs every fire. PA launches no browser outside the helper.
- **Pre-push hook pass memory (CIO):** the first time a PA push prints `already passed on this content N min ago`, mail CIO that line. **Commit scan (#2392):** no skip variable; build test values from parts.
- **CIO seat rule:** never `scripts/alpha-setup.sh`; never `docker compose up`/`down` on the shared stack.
- **Tier 1 staging:** waits on xian's five staging queries (Arch `01M7BXGYZD…`). **Q9** #2313; **Q8** invite hold; **R7 (#1282)** README needs a permitted push.
- **mail4 gotchas:** `inbox --role pa`; ack is `ack <id> done --as pa`; a subject naming a day needs `--due none`; on `cannot lock ref`, loop the push until `origin/main..HEAD` is empty. zsh has no `timeout`.
- **Sprint 2 started Fri 11-13.** v3 is the mail fallback until 11-23.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only; each with the date it became PM-gated and the smallest unblocking answer.)*

- 🔒 **#2242 removal check**, since 11-03: Exec agreed 11-16 (`01M7KN3SAN…`). It is now Step G part 3 on `seat-github-1`. Arch said it conforms with two additions, and HOST asked two small things; all four are in `50ebf686e0`; Arch's final read (11-16 18:47): conforms. It runs in xian's Step G sitting; no separate card. The MCP test-plan card was cut as overtaken.
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **ADR-084 one-time rows**, since 11-15 19:11; xian said yes 11-16 06:20. Remaining PM-hand rows: Steps A, C, D, F0 (his Friday 11-20 sitting on Amber), the #2384 deploy token (Step H, after the job is built), Step G for PA's seat connector (after F0/F). Separately, tier 1 needs xian's five staging queries (Arch `01M7BXGYZDJDA660J2AEM13MCG`).
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
