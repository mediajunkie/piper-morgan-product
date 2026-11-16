# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-15 21:47 STOP; replace, don't annotate)

- **Served (21:47):** beta `460b837a47`; MCP `dfebe7f0b7` (xian's deploy 18:49, uptime 10708 s at 21:47, so no restart since). Read the live sha from `/health`. A beta promotion is GRANTED from 07:00 11-16 (Arch, six conditions: `72b7428e23`, `1ea8e7663a`, #2382, and #2375 revisions if CXO passed). Never read the connector during a promotion.
- **xian's 11-15 19:11 ruling (via Exec):** no more manual workarounds put on xian; "xian runs it" is no longer an offered answer. The fix is **ADR-084, PROPOSED** (`docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md`): seat resources, separate, granted once, bounded. Exec brings xian one card (ten one-time rows). Paid runs stay stopped until his yes.
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

- 🔒 **#2242 held-token row**, since 11-03: xian runs `mcp_allow.py remove` on his account (then re-adds).
- 🔒 **#2238 Notion**, since 11-01: xian puts a throwaway Notion key on staging.
- 🔒 **#2288 served row**, since 11-05: xian's word that Web may use an untouched dead-grant test account.
- 🔒 **ADR-084 yes (seat resources)**, since 11-15 19:11: superseded the 11-13 sign-in route. Exec brings xian one card; his yes plus the one-time rows unblock Web's served reads, #2364, the #2384 token (then #2382's deploy) and PA's seat connector. Separately, tier 1 needs xian's five staging queries (Arch `01M7BXGYZDJDA660J2AEM13MCG`).
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
