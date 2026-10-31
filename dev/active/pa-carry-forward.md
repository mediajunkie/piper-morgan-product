# PA Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds genuinely
transient "where am I right now" state. Durable owed/queued items live in `pa-standing-items.md`;
PM-attention items live **here**, in the section immediately below.

> Per CIO's rule: **resolved items are deleted here, not annotated** — the dated session logs are the
> permanent record. A stale carry-forward is worse than an absent one, because it reads as current.

> **Spring-cleaned 2026-09-22** per PM's context-floor-reduction directive (item 4a,
> `docs/internal/operations/context-floor-reduction-plan-2026-09-21.md`) — cut from 538 lines to
> this. Everything removed was resolved, superseded, or duplicated in a session log / memory /
> `pa-standing-items.md` already; nothing here was live state. Full prior history: git log on this
> file, or the dated session logs it references.

---

## Now: MVP passed; beta letters Saturday 10-31; MCP is priority 1 again (written 2026-10-30 STOP; replace, don't annotate)

- **MVP passed** on `ac5b69f865` (xian's go 17:03; PPM closed #1386; milestone 0 open). alpha and beta.pipermorgan.ai are one host and share accounts. Both serve `ac5b69f865`.
- **The beta letters go out Saturday morning (10-31) from xian's mailbox.** HOST mints the codes with him. **No promotion to alpha until they've gone** (Exec's freeze). Landing on main is fine.
- **Slack inbound gate:** xian unset it at 03:22Z, and PA read `disabled` at 20:25 on 10-30. Nothing more needed.
- **Open at STOP, the #2218 lock-down question.** Any signed-in account, beta included, can connect the hosted MCP: a session plus a consent click, no allowlist. Exec asked CIO for one `ls /app/config` on `piper-morgan-mcp`.
  - If `PIPER.user.md` is absent: no lock-down.
  - If present: stop the MCP app before the letters. That cuts xian's connector too.
  - PA's own `fly ssh` read was **denied** by the auto-mode classifier (production read), so don't retry it. Ask xian for a permission rule if PA is meant to do these.
  - PA told Exec and CIO at 21:5x that v14 came from Amber (likely absent). Filed #2240.
  - PA offered Exec a served OAuth-by-API profile proof. It writes 1 client row and 1 token, so it waits on Exec's yes.
- **Owed by PA on the first promotion after the letters** (PPM's list in `ppm-to-exec-...-2238-placed-next-promotion-check-list...`):
  - Row 2: a full canonical run. Q45 already expects `action`, so routing reads 56/61 on 10-30.
  - Row 3: A1, A2, B's confirm, and the reverse case (`scratchpad` harnesses are gone after this session, so rebuild them from the 10-30 log).
  - Served checks with CXO: #2225, #2236 (capability reply), #2233 (Q1 name, then stop), #2237 (grey Slack/Notion cards), #2218 if landed.
- **Owed by PA after the set_default_repo flip** (xian's word, then CIO/HOST applies it): a fresh-session probe where the setter writes, PA confirms the value and then clears it, then one row 2 run. The test account has a PAT, so this exercises the 200 path.
- **Record if xian quotes them:** his beta wizard's end and his first reply ("beta xian" account).
- **Issues PA filed on 10-30:** #2225 (closed, fix not served, label `fix:not-served`), #2228, #2230.

## Cadence — LaunchAgent ONLY since 2026-09-30 18:4x (no session cron)

PA runs on **`com.xian.pm-pa-cycle`** (boot-persistent, 6x/day at **:47**, hours 6,9,12,15,18,21, Pard-owned). Session cron `a692bd9e` **retired** 09-30 18:4x on Pard's confirmation that the 15:47 LA fire landed work. **`CronList` → "No scheduled jobs" is now the NORMAL state, not Gap-C. Do NOT re-arm a session cron**, including at STOP: per duty-cycle-tick's cron-mechanism gate, skip all CronList/CronCreate/STOP-re-arm content. LaunchAgent liveness is Pard's to monitor. Registry `pa` row flip to LaunchAgent is Exec's (notified 09-30 18:5x). If it still reads session-cron, that's Exec's pending action, not a gap of mine. The +30 session-cron lag (:42 → :12) is moot now; it was a standing observation, last measured 10/10 on 09-29/30.

## MCP program — standing #1 again (rewritten 2026-10-30 STOP; replaces the stale 10-01 section)

- **Live:** `mcp.pipermorgan.ai` is v14, deployed by PA at 17:49 PT on 10-13 (00:49Z 10-14) from this Amber worktree, via `scripts/deploy-mcp.sh`, from `c6c26a596f`. `/health` returns 200 with `git_sha` "unknown", because v14 predates the script's `--build-arg PIPER_GIT_SHA` (added 10-16). **The next `scripts/deploy-mcp.sh` run sets the sha by itself**, so check `/health` after. No commits to the MCP server's own paths since then. **#2240 closed 10-30:** `.dockerignore` drops `config/*.user.md` and the script refuses an overlay (Lead `738c2e5f77`). The guard's clean-tree silent exit 1 was fixed by PA in `de1d1bd714`. Clean dry run passes on main.
- **Auth:** the protected-resource metadata points to alpha's `/mcp/oauth`. Dynamic registration is open, and `/authorize` needs an alpha session plus Approve. There is no allowlist, so the beta scope (PDR-005 Am. 1: MCP not offered) isn't enforced in code. Lead sized a consent-page allowlist as a web-app unit (a promotion).
- **Re-entry plan (START 10-31, fresh session):**
  1. Settle #2218 per the Now section, then deploy the fix (Lead's unit) with `scripts/deploy-mcp.sh --dry-run` then the real run (CIO's order), and check that `/health` shows the sha.
  2. An authenticated live check of v14+: `what_piper_knows_about_me` through xian's Claude connector (PA has the `Piper_Morgan_Alpha_MCP` tool in-session) plus the profile/colleague-model resources. Never verified by an authenticated call since v9.
  3. Re-read the open MCP issues and order them for the first Production sprint discussion (PPM is preparing candidates):
     - #1462 epic; #1918 Connected apps; #1911 consent branding; #2022 payload scope; #2174 ADR-081 D3; #2175 MCP → invite path;
     - increments #1701 (create issue), #1702 (todos), #1703 (standup), #1704 (docs), #1705 (memory), #1706 (calendar).
     - Send PA's ordering to PPM before the sprint talk.
  4. Write the MCP test plan xian runs (connect, ask, Settings → Connected apps, revoke → PA checks alpha logs for `/mcp/oauth/revoke`). The 10-01 version of the plan was never run.
  5. R7 listing copy and the Registry publish stay behind 1–4.
- Commit hygiene: `dev/state/pa-last-pm-scan` is untracked and gitignored. **Don't stage it.**

## R7 (PM ruling 10-05): MVP is a capability set across surfaces; beta.pipermorgan.ai stays the target

PA now owns **demand-probe packaging** (skills listing / plugin via directory review / published MCP server), off Lead's path, **PM tests before any listing**. Standing item #2. Research subagent (Sonnet) dispatched 10-05 ~10:0x. `.env.example` JWT line: denied to 3 seats → PM decision via exec (rec: PM adds by hand). Skunkworks repo: hold, then archive once the probe package lands.

## Revoke: gate CLEARED 10-08 on PM's press only

Web flips /support and ships the two-sentence /privacy paragraph; plugin README updated (`plugin` repo). **Still owed:** observe a revoked client's next call failing (ask PM at next MCP test: revoke, then ask the client something). Then tell Web + Comms to add 'Access ends right away'; listing copy may say 'revoke anytime'. My read-only DB check was denied as a production read; don't retry it.

## Alpha deploys are PM's hand this week (Lead, 10-05)

Lead's seat is denied `fly deploy` on alpha. My `87e8bc9c49` (revoke fix) + `08db18009c` (font) are on Lead's next-deploy card; PM deploys once main is green. **Don't deploy alpha.** After it's live: PM-visible revoke check → then the README/consent 'revoke in Settings' line can return. (MCP app deploys stay mine.)

## Standing mail rules to remember

- **No cc to PM, and PM is never in `to:` (PM ruling 10-03).** Anything needing PM goes to **exec**, with which of decision / ruling-relay / would-contradict named in the subject. Never write to `mailboxes/xian (ceo)/`.
- zsh doesn't word-split unquoted `$VAR`: pass `mail-send.sh` paths explicitly, never via an accumulated string (silent no-send, 10-03).

## Cloud routine experiment (PM-approved 10-03): PA = owner-of-record, CIO runs it

CIO's write-up: `docs/internal/research/cloud-duty-cycle-mechanisms-2026-10-03.md`. One throwaway routine, `persist_session: true`, every 2h for one afternoon; tests warm vs cold, lag, cloud push, token cost. **ARMED 10-03 22:2x by CIO: routine `trig_01LdUvFVg5LQs7ouKx6jinoZ`** (Haiku 4.5, persist_session true, connectors cleared), fires **Sun 10-04 12:00/14:00/16:00 PT**, writes only to branch `experiment/cloud-duty-cycle-probe` (`dev/experiments/cloud-duty-cycle-probe.log`). **CIO disables at Sun 22:07.** **RESULT 10-04: WARM seat confirmed (3 fires, 1 session, lag +4/+1/+1, cloud push ok). CIO DISABLED it 16:08 (API-confirmed); PM to delete via Exec's rollup.** **PA BACKSTOP CLOSED 10-05 06:4x**: `RemoteTrigger get` → `enabled: false`, last fire 10-04 23:01Z, `mcp_connections: []`. Remaining: only PM's delete (via Exec rollup). (Was: if still enabled, run `RemoteTrigger update trig_01LdUvFVg5LQs7ouKx6jinoZ {"enabled": false}`** (the cron is daily, so Mon noon would fire again). Only PM can DELETE (claude.ai/code/routines), so remind via exec once it's disabled. Safety note: routine creation attaches ALL PM connectors by default; CIO cleared them. Asked CIO for a scratch role (not `pa`'s real state) and to record the routine id + delete time, **so I can delete it myself if CIO goes quiet** (it spends PM's quota). LaunchAgent stays armed.

## STATE AT 2026-10-10 14:0x (pre-reboot snapshot; read this first)

- **Post-reboot (10-10 16:51) known fault:** macOS can't resolve `api.github.com`, so bare `gh` times out. **Prefix `GODEBUG=netdns=go`** on every `gh` (curl: `--resolve api.github.com:443:172.182.252.137`). A bare-gh timeout = 'unverified', not red. The fix is PM's (`sudo killall -HUP mDNSResponder`); Pard mails when cleared. Also: `/private/tmp` was wiped, so recreate scratch dirs before use.
- **Mechanism:** LaunchAgent `com.xian.pm-pa-cycle` (:47, 6/9/12/15/18/21), no session cron. Commit hygiene: never stage `dev/state/pa-last-pm-scan` (gitignored). Run `date` before stamping any memo time.
- **MCP:** v11 `10282b068f` live (read-only tool + 3 resources, OAuth, per-identity rate limit (memory), **Smithery server card live**). #1458 CLOSED. Fly CLI login works (renewed by PM 10-08).
- **Plugin:** public repo `mediajunkie/piper-morgan-plugin` (v0.1.0, evals 1/1/1 vs 0/0/0, icon, README revoke line, `mcp-registry/server.json` unpublished). Listing copy final (Comms). **Nothing listed. PM tests before any listing.**
- **Revoke (#1918):** live on alpha; /privacy + /support name the path (two-sentence). **Held:** "Access ends right away", until someone observes a revoked client's next call failing.
- **#1965 (b):** Lead built one resolver with two legs (grant → own PAT); my grant-side review holds; Arch verified. Not yet on alpha (alpha `e8ecd10d5a` as of 10-09). **#1966** (convergence, Production) mine-filed; keep/retire PAT is PM's.
- **10-11 (PM engaged): R7 listing state.** Copy v2 approved in substance; 'yet' stays; Revoke test **PASSED 10-11** (revoke clause now live copy; 'Access ends right away' handed to Comms→Web). **Submission now blocked on #1982** (the MCP app lacks GITHUB_MCP_SERVER_URL + ENCRYPTION_MASTER_KEY; security call with Arch/HOST; PM sets the secret; I add the env and deploy MCP, then PM verifies issues appear). MCP Registry domain proof DONE: Web `ca1f525` serves `pipermorgan.ai/.well-known/mcp-registry-auth`; key at `~/.config/piper-morgan/mcp-registry-ed25519.pem` (0600, PM-approved, never in a repo); `mcp-publisher` 1.8.1 login OK. Publish = `mcp-publisher publish` from `piper-morgan-plugin/mcp-registry/` after updating `server.json` description to the v2 Registry line. PM submits Smithery + the Claude directory (PM's accounts). #1981 filed (first-time setup, later). #1965 (b) IS on alpha (`4bd1a236e9`): the PAT-only test is unblocked; PM is ready to run it and needs an invite (Lead mints). #1966: PA recommended **keep** PAT (10-11); PM has not ruled.
- **10-11 21:47 state (#1982 chain, next session starts here).** Arch's ruling: a scoped GitHub-only subkey, and the MCP app never holds the master key. Lead built it (`079477fb15`); my `fly.mcp.toml` env (`fe10c5aeb0`) is NOT deployed. Order: (1) PM deploys alpha with `079477fb15` (at 21:47 alpha was still `4bd1a236e9`); (2) PM pipes the subkey (runbook `docs/internal/operations/mcp-scoped-subkey-runbook-1982.md` §1); (3) PA checks `fly secrets list -a piper-morgan-mcp` has no `ENCRYPTION_MASTER_KEY` (at 21:47 it held only `DATABASE_URL`), then deploys MCP from main; (4) PM snapshots and runs the re-encrypt; (5) live check with PM; (6) Lead drops the fallback; (7) Registry publish. PAT-only test: waits on xian re-adding HOST's mint permission; Lead's dual write (`4400ee3d9f`, held) lands after it.
- **10-12 21:47 update.** Step 0 done: alpha has carried `079477fb15` since 09:47 (now `6e48d9ebb2`). Step 1, PM's subkey pipe, is NOT run: the MCP app holds `DATABASE_URL` only. PM has the steps (separate Amber terminal, `fly secrets import --stage`). PAT-only invite minted (HOST, 0877…VXB9; raw code in `~/.piper-shared/host-mint-pat-test-20261012.txt`). PM has the test steps, plus the extra 'What are my pull requests?' ask that repros #1995. **Owed:** relay the step-4 result to Lead and CXO. Lead is holding the #1983 hint template for it; final copy is CXO's option (a).
- **10-13 12:28: PA's seat DENIES `fly deploy` / `fly secrets set|unset`** (settings.local.json deny list; HOST's Fly permission split). #1982 step 3 (MCP deploy) is no longer PA's hand until PM names one. Asked Exec for a decision (recommended: PM deploys `-a piper-morgan-mcp -c fly.mcp.toml`). PA keeps the pre-checks (secret names) and post-checks.
- **10-13 13:41: MCP v12 DEPLOYED by PA** via `scripts/deploy-mcp.sh` (xian delegated MCP deploys to PA; direct `fly deploy` stays denied, use only the wrapper). It runs `767874b83f` with the #1982 build and env. Next: PM's subkey import WITHOUT `--stage` (restarts onto the key), then snapshot plus re-encrypt, then live check. Test accounts (OAuth-only, PAT-only) may move to Web (Exec asked Web; HOST: OK with four conditions).
- **Waiting on PM (my five deferrals):** (1) listing go + domain proof; (2) revoke-then-ask test; (3) privacy Section C four decisions + key check; (4) a PAT-only test account on PM's own PAT (#1889/#1963 served check); (5) #1966 keep/retire PAT.
- Ship #064 review filed 10-09. Nothing in flight.

## PM Attention

*(Exec's `cohort-attention-rollup` reads this section directly. Live items only.)*

🔴 **PM-GATED, genuinely open (as of 2026-10-01 16:0x):**
1. **#1911 revoke: PM chose (a), #1918 'Connected apps'** (Production, not MVP, PA-implemented, off Lead's path). Backend dispatched (Sonnet, isolated worktree) 2026-10-01 ~20:0x; PA reviews and lands it. UI → CXO. **Still owed from PM: test (1)**, removing the ChatGPT connector once while I watch alpha logs for `/mcp/oauth/revoke`. PM can test (b) by removing the ChatGPT connector once; I check the alpha logs. The unverified sentence is already dropped on main (`15c371f65f`, ships with Lead's next alpha deploy).

*(Resolved 09-24: **T-axis** — was carried as "blocked on CXO"; CXO found on 09-24 the split proposal had never reached PPM at all; PPM ruled the split APPROVED within the hour (`decisions.log` 09-24 07:2x, binding condition: T-MCP-surface always reports `UNMEASURED — blocked on increment-1 MCP infra`). Now blocked only on CXO's pre-registered properties for T-own-surface, promised same-cycle — an external dependency, not PM's. Tracked as standing-item #2.)*

*(Resolved 09-23, removed per CIO's rule: **BYOC Phase B** — PM approved the recommendation
directly; execution notice sent to Exec/Pard, nothing further PM-gated here. **Registry gaps**
(Loom, Vergil/OpenLaws) — PM is discussing directly with Janus, not waiting on PA. **Usage-
correlation model's two blockers** — Pard's 09-23 answer closed BOTH, including the seat→account
mapping PM had been asked for: it's a function of `CLAUDE_CONFIG_DIR`, all 11 PM seats on one
account. PM needn't answer that question now. Build dispatched, #1862.)*

## Current state

- **T-own-surface — CLOSED 09-25.** CXO accepted round 4 as scored, folded the four-round cumulative finding into rubric v0.8.2 §6e + `decisions.log` (verified both present). GPT-4o 0/8 across every design tried; Claude 5/6 across member-form rounds, 0/2 on metadata. T-MCP-surface stays `UNMEASURED`. Standing #2 moved to Resolved.
- **Capture, 09-24 afternoon**: first scoped rows live (15:23); a second `SHAPE-CHANGED` on PM's
  account at 15:23 with `five_hour`/`seven_day`/`limits` all present — a sub-field failure (likely
  a null `resets_at`), not a missing key; observation to Pard (exception message in the note,
  per-field tolerance — their call). **PM account's binding Fable limit read 72% of the week at
  16:1x** (aggregate 48%). Resets Thu 22:00 PT. **PM, 09-24 16:2x, in conversation: the
  elevated burn is deliberate** — the one-time reset's credit expires at tonight's regular reset,
  so the cohort is using it. **Labeled interval for the correlation model: 09-23 ~13:00 →
  09-24 22:00 PT = known-cause high-burn window**, treat as an explained spike, not noise.
- **Memo filenames**: keep basenames ≤ ~120 chars — full repo paths >180 trip `lint.yml`'s
  `mailbox_filename_lint.py` (#1616, Windows MAX_PATH); 1,714 legacy paths are baselined, new
  ones fail. Lead flagged Pard's two 09-23/24 memos; mine this week are all <150.
- **Fire lag, +30 min, cohort-wide**: PA/CIO/Exec all exactly +30 on every fire since ~09-23
  midday, across different expressions and re-arm histories (re-arm crossed out). PA's 09-24
  06:42→07:12 makes four. Thread is CIO's/Pard's; PA contributes fire-open `date` only.

- **BYOC/MCP — PM handed PA full ownership of the MCP testing program 09-26; unit 4 (OAuth AS) landed live the same evening, Arch-approved.** mcp.pipermorgan.ai units 0–4 all LIVE (alpha v146, MCP v6/v7, `645ce6412d`). Found `min_machines_running` still 0 before PM could connect, fixed the config myself, routed the redeploy to Lead (proven Fly access) rather than guess at my own. Told PM directly with Lead's tester copy + the three named gaps (#1458 open-but-safe, T-MCP-surface unmeasured, #1510 store sparse). **PM has not yet attempted first contact.** **Owed next**: re-verify the warm-pin holds live (not just trust the config file), then be ready to help PM debug the first real connection. Full detail: `pa-standing-items.md` #1.
- **PA's own briefing refreshed 09-22** (`docs/briefing/BRIEFING-piper-alpha.md`) — Docs flagged
  it 6 weeks stale, fixed same-day with live-verified facts (version, GitHub milestone counts, Fly
  hosting migration, team/account structure).
- **Mail-routing lesson, 09-23**: `mailboxes/pard/` in this repo is gravestoned (09-12) — Pard's
  real inbox is external (`mediajunkie/docs/mail/`). Default to Exec-as-relay per
  `docs/internal/operations/cross-project-mail-routing.md`, **except when PM explicitly directs
  direct delivery** — PM did so 09-23 (both the usage-readability question and the Phase B notice
  were then written and committed directly into `~/Development/mediajunkie` via `git -C`, matching
  that repo's own commit/frontmatter conventions, not `mail-send.sh`). Treat Exec-relay as the
  default, direct delivery as PM's to authorize case-by-case.
- **#1458** — sprint week 09-25 made MCP Phase C a named sprint goal; checked whether the exact
  risk I'd been carrying (epic optimism compressing the identity gate) materialized. It didn't:
  Arch verified #1458 live before scoping Phase C's "minimal alpha-testable slice" (resources-only,
  zero tools, full-rigor identity boundary, any mutation need escalates rather than gets built
  around) — the harder pieces were traded off explicitly, not silently. Worry resolved by Arch's
  own diligence, not by PA's. Still OPEN, still tracked, no longer a live concern this sprint.
- **Architecture-diagram discussion** — PM-requested, awaiting a time. Prep, don't pre-empt: PM
  asked to discuss, not for a revision.
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
- 10-13 17:05: #1982 LIVE CHECK PASSED (PM via Desktop, OAuth path). MCP secrets: DATABASE_URL + ENCRYPTION_SCOPED_SUBKEYS only, v13. Left: Lead step 3 (drop the fallback); Registry publish, held by PA's recommendation for #2005 (the issues resource reports a 30-page as the full set; 278 real). PAT path untested.
- **10-13 21:47 state (STOP):** #1982 DONE on MCP (subkey v13, live read passed, step 3 done by Lead). MCP v14 live with the #2005 fix (`c6c26a596f`). OWED: the #2005 served check (PM re-asks in Desktop: 278 total, 50 shown, not 30 "full set"). HELD: Registry publish (PM ruling 17:07; beta-period). Eval proposal `docs/internal/architecture/current/mcp/eval-2005-partial-list-bare-mcp-vs-plugin-2026-10-13.md`, waiting on xian's answer on order (server, then plugin?). PAT-only test: Web needs a GitHub test identity + HOST's go; Lead's dual-write branch waits on it. PM decisions open: #1966 keep (PA recommends), privacy Section C go-to-publish. MCP/plugin/BYOC = NOT MVP critical path (xian 10-13).
- 10-14 18:01 OWED: after the promotion carrying Lead's `a07796a06b` (#1965 isError fix and #2012 Test probe), xian re-runs the broken-grant check: revoke Piper Morgan Alpha, then the four reads (expect the disclosure, `degraded_sources` naming github with `stale_token`, no ✅) and the Integration Health Test (expect a failure plus a reconnect prompt); then Disconnect, Connect with GitHub, and re-read clean. Readings go to Lead.
- **10-14 21:47 state (STOP):** #2005 CLOSED (served pass, Desktop 279/50); follow-up #2022 (payload scope), beta-period. #1965/#1889: broken-grant check FAILED 4 of 4 on alpha (the isError gap); fix held at Lead's `a07796a06b` (`claude/lead-1965-iserror`), with #2012 on the same branch. Alpha was promoted 10-14 to `5e5f3366c4` WITHOUT it. OWED: once alpha's sha contains the isError handling (grep `isError` in `services/mcp/consumer/github_adapter.py` at the /health sha), xian re-runs revoke, then the four reads plus the Integration Health Test, then reconnects (Disconnect is broken, #2017: use the console POST `/github/disconnect`, then `/github/connect` → `auth_url`). Filed: #2012, #2017, #2018 (tracking), #2022. xian's direction: smart server → connector → skills (decisions.log 10-14). Held: Registry publish. Run-hot until Thu 10-15 22:00.
- **10-15 16:2x: S5 PASSED** on `6f2916d10f` (comments on 1965/1889/2012; Lead closes). #2039 filed (xian: URLs must make sense and be guessable). Open: #2017 served check (did the reconnect use Disconnect?); #2029 + #2031 on the next promotion → re-run S5 steps 3–4 for the new Settings card and one-step Reconnect.
- **10-15 12:47:** #2029 filed (#2018 step 3; settings page says Connected on a revoked grant). S5 steps linked from card v41; Step 0 READY on `35acfe35d7`, waiting on xian.
- **10-15 START state:** alpha still `5e5f3366c4`; the isError fix is NOT on main yet (Lead's briefing: held branches, #1965/#2012 among them, land this morning). Blocker for the post-fix broken-grant check unchanged: a promotion whose `/health` sha has `isError` in `github_adapter.py`. Routing eval done (plugin `6aab52f`): the description rewrite doesn't move bare routing (33 vs 37 of 45); plugin 15/15. Run-hot ends 22:00 tonight.
- **10-15 21:47 state (STOP):** S5 PASSED with xian on alpha `6f2916d10f` (#1965/#1889 OAuth leg served; CXO judged the copy; Lead closes). #2012 stays open (#2037, the stale-OAuth-plus-PAT leg). #2029 (Settings card + one-step Reconnect) on main `bee366050c`; #2031 (Integrations card) Lead building on CXO's words and Arch's resolver ruling; #2039 (likely URLs + a human 404) Web's, shape accepted by CXO. **OWED on the next promotion:** re-run S5 steps 3–4 with xian (revoke → "Needs reconnecting" card + Reconnect → Connected in one step; steps page already covers both builds). Routing eval done (plugin `6aab52f`): description lever is null; the plugin stays the routing lever. Held: Registry publish. Normal pacing from Fri 10-16.
- 10-16 09:5x: OWED on the next MCP deploy: confirm MCP `/health` `git_sha` equals the sha `deploy-mcp.sh` printed (CIO agreed the build-arg change; source-level only until then).
- **10-16 21:47 state (STOP):** alpha `d741214b6c` (promoted 17:06). **xian ran A1 (= S5 steps 2–5) 18:00–19:30 with Lead, not PA.** Step 3.1 FAILED → **#2072**: after #2029's STALE write, the radar/standup gate reads STALE as "not configured" and skips GitHub silently. Fixed on main `b1fbfa3da1`, NOT served. PPM asked xian (via Exec) to admit #2072 to MVP. **OWED:** (1) xian's readings of steps 3.2–4 on `d741214b6c` (card, Settings page, Reconnect), which Lead asked for and which aren't recorded yet. Check Lead's log or mail at START and relay them. (2) Re-run step 3.1 on the first promotion containing `b1fbfa3da1` (Lead's Sat order: promotion 1 of 2 from 07:00). That run is #2072's served check, and #2031 closes on the card readings. (3) The served-sha check on the next MCP deploy. #2071 (host-global Test result) landed on main; the S5 steps say not to judge by the shared check time. Held: Registry publish. #2022: beta.
- 10-17 START: S5/A1 trigger moved to Lead's **slot-2** promotion today (lane `2072b`, renderer fix; Arch 06:29 on #2072). Steps carry CXO's chat acceptance. Asked Lead to mail PA when A1 starts. xian's 10-16 A1 readings still missing.
### 10-27 STOP (21:47)
- **Alpha `36bdcf09bb`** (0.8.14.0), healthy, database healthy; MCP `/health` 200; main CI 12 of 12 green. Auto-recovery (#2146) is in its normal state; for any deliberate DB stop, commit `ops/alpha-hold.md` (with `**Held by:**`) first.
- **#2018 (the last MVP issue PA can help close): the run is PART DONE, paused with xian at about 19:05.** Account mvp-tester. Card `dev/2026/10/26/2018-recovery-card-for-xian-69d859ca5f-2026-10-26.md`.
  - Step 1 didn't break GitHub: a saved PAT kept it working ("using your personal token"). PA's miss: the card's PAT question should have stopped the run before step 1.
  - Step 3 PASS (dialog, "Disconnected / GitHub disconnected", card "Not configured", chat "GitHub isn't connected yet…"). Disconnect also cleared the PAT.
  - Steps 4 and 5 card PASS ("Connected with your GitHub account. Checked just now."; Test "…using your GitHub connection.").
  - **Still owed:** step 5 chat ("show my open issues", which should list #2182, #2181 and #2178 or newer); the **real step 2** (revoke the Piper Morgan Alpha OAuth app again; expect "⚠️ Needs reconnecting" or Test failing with "needs re-authorizing", and a chat "needs re-authorizing" reply); step 6 (Reconnect with GitHub, then working again).
  - **After it:** post the readings on #2018 and send them to CXO the same hour (they gate the letter's GitHub line). CXO judges the words; close with close-issue-properly. Remind xian that his PAT was cleared.
  - **Card wording for CXO:** with a PAT, the Integrations card read just "Connected / Not checked yet. Press Test.", not the card's predicted "Connected via your personal token" (which #2029 describes for the Settings → GitHub page). That's PA's card being wrong about the page, not a bug yet.
- **Filed 10-27:** #2183 (chat ignores "two" in "show my last two new issues"; Lead's lane).
- **The design-partner letter's** known-issues line (disconnect, then connect) rides #2018's run. Step 3 and step 4 now pass served, but CXO has not seen the readings yet.
- **Website:** today's accessibility thread is closed (`b8ab3ea`, `0b4260e`, `a5b7caf`, all live and accepted). xian still owes the Search Console resubmit and URL lists.
- **Google #2087:** nobody edits the consent screen; waits on a person for the wizard path and an outside-account read.
- **Still waiting on xian:** the gate-password reuse answer (`ddb7…9184`, through Exec); the PoC plugin uninstall; the Notion token re-save; the one-project Google choice (before 10-30).
- **#1386:** PPM's tick, plus xian's close-enough call (38/41).
- **Spend:** lead-scoring is at $88.22 of its $90 cap. **No PA Anthropic-path run before 11-01 without a price to Exec.**
- **MCP served-sha check:** on the next MCP deploy.

### 10-28 (xian engaged, morning)
- **#2018:** step 5 chat PASSED at 10:09 (a live read through OAuth alone). **Still owed:** step 2 (the real revoke) and step 6 (Reconnect). xian is back after his call. xian doesn't want the PAT back, so there's no reminder.
- **Filed:** #2184 (wrong MVP list, E4), #2185 (the 261 count and its sort). Commented on #2183 (milestone qualifier dropped). **Waiting** on Lead and Arch's answer to xian's question (memo `fde6ff7f1`): is phrasing-variation handling in private beta, and is #2184 MVP-blocking? Relay it to xian when it arrives.
- **#2018 CLOSED 14:3x 10-28** (CXO ruled the close on the mechanics; follow-ups #2187 and #2188). MVP open=3: #2184 (Lead closes, served PASS), #1595, #1386.

- **Rename (xian's idea, 10-28):** once the MVP milestone reads 0 open and private beta formally starts, consider a new name for PA. It's xian's call; raise it at that trigger.

### 10-28 (evening, STOP)
- **Promoted 18:55** (xian, run 40804462072): alpha serves `49e0904c3c` (READY's `51067dfe20` plus docs/logs only). Lead and CXO told (`398081a22c`).
- **Served rows owed, 0 of 4 run** (xian on mvp-tester): (1) unchecked card reads "Not checked yet. Press Test."; (2) "show my open issues" says "assigned to you across all your repositories" (~256); (3) milestones then "MVP" lists #2184, #1595, #1386 via a real read; (4) revoke, Reconnect, card reads "Not checked yet", Test passes. Readings go on #2184 (Lead closes), #2185, #2187; send to CXO and Lead.
- MVP open=3: #2184, #1595, #1386. #2189 builds are fresh-session Lead work (row 1 first; row 3 table needs xian's migration word via Exec).
