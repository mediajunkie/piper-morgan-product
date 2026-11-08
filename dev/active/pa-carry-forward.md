# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Transient "where am I now" state only. Durable owed and queued items live in `pa-standing-items.md`. PM-attention items live in the section below.

> Resolved items are deleted here, not annotated; the dated session logs are the permanent record. A stale carry-forward is worse than none, because it reads as current.

> **Rewritten 2026-11-06 06:47 START** after CIO's staleness run 3: the 10-01 PM Attention block, the 10-10 snapshot and the 10-13 to 10-28 dated entries were removed (all resolved or superseded; full text in `git log -p dev/active/pa-carry-forward.md`).

---

## Now (written 2026-11-07 21:47 STOP; replace, don't annotate)

- **Served:** beta `f9b4c737f7` at 21:47; MCP `/health` 200. Read the live sha from `/health`, not from here. Tomorrow's first promotion (07:00 or later) carries Lead's z22/z23: the #2270 handler, always-ask, the default lead, the couldn't-find sentence, and #2321's "one todo at a time".
- **Since #2282 (11-05), alpha redirects to beta** except the MCP OAuth paths, the well-knowns, `/login`, the login POST, `/static`, `/assets`, `/health`. **Scripts target beta** (`dev/2026/11/06/turn.py`, run from the dated dir).
- **First checks on 11-08, after the promotion serves:**
  1. #2321 no-list rerun: `delete the first two todos` with no list. Expect `I can delete one todo at a time for now.` (Q9).
  2. #2270 (Q10): the advisor's turn 1 ×6. Expect `I couldn't find "project/repository" among your repositories. Which repository should I use…` and no document reply.
  3. Name answers: `piper-test-activity` should bind and give feedback with a next step (at least 3 of 6, CXO 21:47: `owner/name` and the bare name each at least once; counts-only fails). `Harbor Pilot` should re-ask honestly (gap B can't pass until the list-form unit).
  4. Default lead: only on an account with a default. If web-seed-1386 has none, don't set one; tell CXO, and it moves to Q8.
  5. Turn 2 in Lead's words ×2 after a real read.
- **web-seed-1386 must keep no clear preference**: never answer clear's verb question with done or delete. #2322's done row waits on Q8.
- PA can't sign in to other seats' accounts: the permission classifier denies it even with the owner's yes.
- **Test account web-seed-1386 (21:47):** 8 open, in order: urgent task (urgent), zz throwaway one, zz throwaway two, audit the current navigation, **review prs (×2) on line 5**, review the deployment plan, draft the launch checklist. No reminders, no clear preference.
- **Q9 also:** #2313 ("delete A and B") on its build; CXO's #2294 bulleted-list row; #2324 "tomorrow" and gap A on Lead.
- **#2288** (card says "Connected." on a 401 grant): served row needs a dead-grant account; xian's word for Web.
- **#2242 (Q2):** held-token row, on xian's `mcp_allow.py remove` relayed by Exec.
- **#2238:** xian's Notion key on staging, then Web runs `dev/2026/11/01/notion-chat-check-2238.py`.
- **Fresh-account checks** (Q8): on the invite hold lifting (#2261, #2282, #2292, #2322 done row) and HOST's slot with xian.
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
