# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-25 21:47 STOP; replace, don't annotate)

- **Served (11-25 21:47):** beta `cf3486389e` (11-25 promotions: `aaf8d9249e` #2433, #2434, 2399; `92836ae41d` 2437, which changed `services/mcp/consumer/github_adapter.py` but no code the MCP server calls; `cf3486389e` #2438). MCP `dfebe7f0b7` (uptime 874675 s, no restart since xian's 11-15 deploy), so the connector still serves the old stale-token line until the next MCP deploy (CXO accepted 11-18). Read the live sha from `/health`. Never read the connector during a promotion. CIO's `ops/promote-hold.md` exists (stricter promote-only hold). Session restarted onto Claude Code `2.1.332` 11-25 `19:05` (Pard).
- **Clock rule (CIO 11-18, `752547e88e`):** no estimated minutes anywhere committed or mailed; quoted times in backticks; log headings via `scripts/log-entry.sh`.
- **xian's sitting (11-26):** F.2 done (base No permission; `atswimtwobirds` Member; team `seat-test` Read on piper-test and piper-test-2; Free). F.4 done 11-26 `11:28` in a separate Chrome profile (not incognito; Exec asked him to sign out): "connected as atswimtwobirds", Test Passed. The App was already installed on the pipermorgan org (piper-test, 11-12), so the account can't start installed nowhere. **F.5 dropped** (PA `01M8CNV1HP…`): PA's G part 2 read checks the install covers piper-test only. **Next for xian: Step G parts 1 and 2**, then PA's read; zero-install read waits on xian's pick, (a) piper-test off the team for one read or (b) unreachable. **Step H READY** on xian's card. **seat-github-1 stays bare** for other purposes (`seat-tester-1` ruling). Done-note rule live.
- **PA's next action (11-26):** claude.ai refused a second connector at the same URL (`12:11`). Arch's revised order (`01M8CR7F1S…`): **(a) first**, xian adds `Piper Morgan (seat)` at `https://mcp.pipermorgan.ai/mcp?client=seat` (steps `995a578094`); pass = Piper's consent page + PA's profile read names the seat + xian's connector still him; on failure he removes it. Then (c): PA's session adds `piper-seat` (`claude mcp add --transport http --scope local piper-seat https://mcp.pipermorgan.ai/mcp`), Pard restart, xian consents as seat-github-1. **Waits on xian's yes** to one token in his Claude Code credential store (login keychain, shared `~/.claude-pm`), and HOST's custody read of steps text `732248cbf3`. On no: (b) another claude.ai org, then (d). Then the seat check: profile names the seat; GitHub issues (piper-test and piper-test-2 each have 1 open issue, so the read shows the install's reach); `uptime_seconds`; one read of xian's own connector. Ending on (c): `claude mcp logout piper-seat`, then `remove`, then the allowlist removal.
- **PA's ADR-084 items:** (1) **#2384** MCP deploy job: **on main 11-24 as `8ac5c8e267`** (HOST custody and Arch D6 reads conform; HOST's two card conditions: environment `mcp` limited to `main` read by name before first use, xian picks expiry and app scope at minting). Waits on Step H (xian's token). Its first run deploys **#2382** (stateless MCP). Then **PA reads row 4**: MCP `/health` sha plus `uptime_seconds`, and one connector read that must serve on the first try; quote to CXO and on #2382. That deploy also carries CXO's stale-token words (`85c4717da1`); quote the served line to CXO (PA's mail `01M7R6PJJ4…`). (2) **Step G** (final, `50ebf686e0`) after F0 (#2389) and F; PA's zero-install read between connect and install; part 3's result to HOST's custody row; on FAIL file on #2242 the same hour.
- **`piper-morgan-test` key (xian 11-17):** nothing of his uses it; seats may spend through it. Arch: conforms to D2. xian's console 11-26 (Exec `01M8CNX2P3…`): workspace spend limit $40.00, $17.33 spent this month (resets Dec 1 UTC), so plan against about $22.67. HOST's custody answer was owed at 13:36. Keep-true: log planned turns before a sitting; a turn is several model calls; a pause stops every seeded account's chat.
- **Spend tone (xian 11-17):** agent spend is nominal inside the monthly credit; still track (caps, PLANNED/COST lines, $10 a run). Write spend asks short and don't frame them as a risk.
- **#2379 served rows (Lead):** `seat-github-1` exists (11-20 `18:36`); they wait on its GitHub connect (F.4 and F.5) and the seat browser (#2400, **closed 11-24**, 4 of 4 rows). Not routed to xian's screen. PA writes the quotes for CXO. **#2401/#2402:** PPM's sprint 3 draft (11-25, item 4) puts them behind xian's go-ahead to mint `seat-tester-1` (with #2417, 2411, #2406), consistent with HOST's 11-22 one-purpose ruling that keeps `seat-github-1` for Step G; their served read is a signed-in Integrations card after a forced failed Test.
- **Web's served reads** (#2364 x3, #2328, #2366, #2367, Q12, #2294, #2295): Web's session is back 11-22; these sit in Web's queue after step 4, CXO's #2406 row and Lead's #2297 pass (checked in Web's carry-forward 11-22). Results go to PA for #2355; then ask for the #2364 after-fix run.
- **#2342:** open rows: the zero-install line (needs the seat account), the named-repo refusal, the too-many line, row 4. Record `uptime_seconds` beside every first connector read.
- **Browser-launch guard (CIO 11-17):** a Bash hook refuses an unflagged Chrome/Chromium launch (heredoc text going to a file is exempt since `aafb9da58a`). **Step 1j**, `scripts/browser_keychain_check.py`, runs every fire. PA launches no browser outside the helper.
- **Pre-push hook pass memory (CIO):** the first time a PA push prints `already passed on this content N min ago`, mail CIO that line. **Commit scan (#2392):** no skip variable; build test values from parts.
- **CIO seat rule:** never `scripts/alpha-setup.sh`; never `docker compose up`/`down` on the shared stack.
- **Tier 1 staging: dropped 11-20** (overtaken by ADR-084's beta seat route; PA to Exec `01M7WJCW8H…`; Arch confirmed 05:35 `01M7WJQ70J…`; not the #2355 corpus "Tier 1"). **Q9** #2313; **Q8** invite hold; **R7 (#1282)** README needs a permitted push.
- **mail4 gotchas:** `inbox --role pa`; `--cc` takes space-separated roles (`--cc lead host`), a comma list is refused; ack is `ack <id> done --as pa`; a subject naming a day needs `--due none`; on `cannot lock ref`, loop the push until `origin/main..HEAD` is empty. zsh has no `timeout`.
- **Sprint 2 started Fri 11-13.** **v3 fallback ended 11-23** (CIO `01M84VRPAA…`, `1ae55d7048`): `mail-send.sh` refuses seat-to-seat memos; use `mail4.py send`. `mail-send.sh` stays for filing a v3 memo to `read/`, outside parties and Spec. If v4 itself is broken: `PIPER_V3_FALLBACK='<why>' scripts/mail-send.sh ...`, reason in the log.

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
