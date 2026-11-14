---
last_updated: 2026-11-13 15:29 PST (WORK)
currency_claim: rewritten at substantive-change boundaries, verified at every START
max_age_days: 4
---

# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff for the next Architect session — current state and active threads
only. Resolved history lives in the session log (`dev/YYYY/MM/DD/`) and `decisions.log`, not here —
per PM's 2026-06-12 ruling that the session log is the durable record, and the 2026-09-22
context-floor directive that duplicating it here is exactly the accretion to cut.

---

## Environment (stable; verify at START, don't re-derive)

| Fact | Value |
|---|---|
| Host / model | Amber, Model A worktree `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` |
| Model | **Opus 5.5 (`claude-opus-5-5`) since the 2026-09-28 ~14:35 cold restart** (Pard, PM-authorized, no `--resume`). Verified from the runtime model system-reminder, not the handoff's stated intent. ⚠️ `~/.claude/settings.json` and `~/.claude-pm/settings.json` BOTH still read `claude-sonnet-5`, so the Opus model comes from a launch-time override, not the settings default. A relaunch that drops the override would silently come back as Sonnet. Check the runtime reminder after any restart (rule 7). |
| Wake mechanism | ⚠️ **SESSION CRON RETIRED 2026-09-25, PERMANENTLY — do not re-arm.** External LaunchAgent (Pard), reading the registry's `cron_expr`. Registry-vs-plist mystery resolved 09-26 with a `pm-cadence` drift guard now in place — registry is trustworthy again. **Cadence: back to 6/day `27 6,9,12,15,18,21` as of 2026-09-28 21:27 STOP** (registry col 2 edited, threshold_h 9→7). Exec's 08:0x "revert Tuesday" ruling was RETRACTED 14:5x; final 15:1x memo: PM confirmed "Monday ok" = revert today. **CONFIRMED 2026-09-29: the 09:27 fire arrived** (off-schedule for the old 3/day expression), so the LaunchAgent reads the registry's col 2 live. The prompt's `cron=` constant was regenerated to `27 6,9,12,15,18,21` by 2026-09-30 15:27, so prompt and registry agree again. (It is documentation; the LaunchAgent reads col 2.) |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Deliver to Pard directly (DIRECTORY.md "deliver it yourself", default since 2026-09-27): write the file, stage it by exact path, push to `mediajunkie/mediajunkie` main, then verify it on origin. Done 10-12 for #1952. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

**11-13 state (21:27, STOP):** main 12/12 green; inbox empty. #2369 CLOSED. #2363 validated at 7062d35d70 (row 3 = next real promotion, needs Arch's word). #2358: all seven procedures CONFORM to rulings 18:30/18:43/19:08/19:14/19:19 and are voice-passed; six at ce46ba0542 are on xian's card (Exec rollup v988). The build waits on PPM scheduling, then Lead. #2364 step 1: b16b83dcef pushed to origin `lead/2364-step1` at 21:34 (Lead 01M7C8THV5…); validate the post-rebase sha Lead mails before the gate. Waits on xian: beta log read, #2364 key/provider read, one-key question, staging read, 1386 profile sign-in, procedure approval.

**11-13 state (17:58):** beta serves 81d149ac86 (since 16:34). xian's 17:41 answers via Exec are in:
- **#2362/#2350:** a fresh probe was sent at 17:47:45 on 81d149ac86. The pass line counts from the 16:34 start; reply 01M7BVW607…. Waiting on xian's log read.
- **#2364:** xian said yes to the spend and to step 1. Key (a), a capped key, is pending with Exec. OpenAI may go unrun only after the user_api_keys read plus a known-limits row; otherwise a second key (decisions.log 17:50). Ethics on by default is now YES and lands after step 1 is served (DECISIONS.md line, decisions.log 17:56). The floor-inversion link is on the issue.
- **#2363:** xian said yes; Lead builds `^@`. Validate when it lands.
- **1386 route (17:53):** the xian-signed browser profile is APPROVED. NO to a password allow rule. No longer session for test accounts, because refresh slides 7 days. A staging test account is OK once staging is confirmed to hold no real data, with the staging-vs-beta row split.
- **Self-knowledge boundary:** ACCEPTED; #2358 and #2359 can move.
- **Sprint 2:** Arch rules tech for Lead. PPM's order: Path B #2297/#2301 first, then #2364's run the day the key exists.

**11-13 state (15:29):** beta serves bb7c76de5c. Main 12/12 green.
- **#2362/#2350 served rows:** wait on xian's log read (probe 09:26:12; criteria 01M7AZ4FSN8DA5NF73Z8R8BS8Z).
- **#2364 (ethics substring fast path over-declines on beta; reply-side tier reads a missing `is_violation`):** ruled 13:21, 13:25 (default flip goes to xian), 13:37 (v0.2 live in the same unit, live-run gate, KG keeps check_*), 13:53 and 14:04 (gate = two runs, Anthropic + OpenAI, 26 calls each; Gemini can't serve), 13:55 (an unrun provider is skipped only if no connected account uses it and xian has approved a known-limits row). ADR-061 v1.2 (Layer 1 removed, effective on merge). Lead holds the build `b16b83dcef` on `lead/2364-step1`. Waits on xian: provider keys plus which providers testers use, the sprint go, the default flip. Served probe: PA and Web both blocked on the web-seed-1386 decision. Ruling 2 (reply tier acting) is a later unit behind a served-reply screen.
- **#2365 (KG redacts a node on a substring), #2366/#2367 (Gemini keys page and route, on main at 3405614ea1, not served), #2368 (setup default_llm_provider validated against PER_REQUEST_CLIENT_PROVIDERS, ruled 15:13; CXO wants two refusal sentences).** On a promotion request, check the exact commit against #2342's open rows.
- **#2355 Tier 1:** checker da2f5c5f84 VALIDATED (decisions.log 15:29). b-cant-read and b-stance verified (code reads), approval pending. b-wont-do stays unindexed until xian's default answer and #2364. The future CI step needs the approved shas in its checkout.
- **#2354:** reply-prompt cache order ruled (10:20, per user). Lead builds when placed.
- **Correction recorded:** 11-07 16:33's decline attribution (it was the model's own; the output filter's boundary tier can't act).

Day blocks before 10-27 were cut at the 10-27 STOP rewrite; their threads are resolved, carried below, or in their own day's log and decisions.log. Prior text is in git history (`git log -p -- dev/active/arch-carry-forward.md`).

- **11-12 STOP (21:27 fire).** Main 12/12 green. Beta still serves `d4fd55e6c5`: tonight's promotion was refused by the gate's first-parent walk (#2363, `^@` fix, waits on xian's yes). Lead promotes after 07:00 11-13 with #2350, #2362, #2333, #2348, #2351 words, #2353 and #2347 in it. Every ruling is in decisions.log.
  - **#2342 (GitHub App cutover):** APPLIED 19:06 (10/10 classic tokens revoked, 0 left, DONE). The half-state window was 17:26 to 19:06, so my "same sitting" condition was met 100 minutes late; HOST and I record that. Row 1 PASS (PA served read; CXO ruled). Next: xian reconnects without installing, then PA reads row 2, then he installs and PA reads row 3; row 4 is marked not served; then the refresh row (a grant about 8 h old). The MCP app stays as it is until the rows close, then `deploy-mcp.sh` brings `uptime_seconds` and the #2362 filters. Open "Connection closed" on the first read after a gap (PA counts it per read; nothing filed).
  - **#2353 VALIDATED:** the keychain is opt-in only (`PIPER_CREDENTIAL_STORE=keychain`); the test seam carries the backend (`_test_keyring_backend`). An explicit `=db` beats the seam (accepted).
  - **#2350 and #2362:** departures accepted. `evidence()` writes through stdlib JSON; the redaction filter is on every handler; the four follow-ups are at `3c03b97ace` (code and state as query params only; re-install at the end of startup; redaction in the malformed branch). **Validated from source. The Tests run on `875c051bee` FAILED after STOP: 1 new failure, the httpx filter-count test, which pins the old non-idempotent install; Lead was told. Lead fixed it at 855ed2e154; Tests 43373455195 green; #2362 validated 11-12.**
  - **PDR-009 (public-beta gate) accepted by xian.** My technical rows are G1, G2, G6 (endpoint half) and G7 (§3b). Ruled tonight: #2158 (the deletion record is an append-only bucket, written first, and a failed write refuses the delete; whether the Fly org has object storage is xian's check), #2361 (pause switch: a DB setting with a narrow `can_pause_admission` flag; xian's yes is permission only, so no account now and the interim stop is xian at the page; custody conditions in decisions.log), #2157 (the drill copy has its own throwaway Redis, never a cap-off switch), #2347 (FeedbackCapture deleted; the ConversationManager Redis cache is dead; the performance test kept). The MCP rate limit stops being per-machine if the MCP opens to unvouched accounts. The gate most likely closes in sprint 6 or 7 (PPM's map).
  - **Self-knowledge:** xian said Tier 1 first, with parts 1, 2 and 4. My revised boundary (design record section): methods and code-reading go to every Piper; team records go to nobody; Tier 2 dissolves. #2354 to #2359 are filed; #2358 and #2359 wait on xian's word on the boundary. CIO owns the Q3 plan (H1 to H4; H1 is the first paid run). #2354's code guards are ruled (rule 3 under #2042, rule 4 via #2355). The H2 counter on #2350 takes the router's class, never a regex.
  - **Rule-7 key question (Exec has it for xian):** which key a seat may spend on its own model calls, and how it arrives. I recommended (a): a dedicated capped key entered once through `local_key_setup.py`.
  - **#2335 Redis rotation:** still xian's, after the #2342 rows, when beta is quiet.
  - **Lessons (11-12):** HH:Mx estimates slipped four times (two memos, ack notes, a log line), each corrected. The fix is the same as on 11-11: the minute comes from `date` or the memo's `sent_at`, never typed; in ack notes, cite the memo ID, not a time.
- **11-11 STOP (21:27 fire).** Main 12/12 green. Every ruling today is in decisions.log.
  - **xian's keychain rule (11-11 11:12):** nothing a seat runs reads his login keychain without his permission. Prefix `PIPER_CREDENTIAL_STORE=db` on any local server or pytest run. #2338 is closed: tests and the documented starts are opted out by default (`PIPER_TESTS_USE_KEYCHAIN` opts in). #2340 is closed: the one binder `scripts/dev_key_binding.py` requires the store to be set, binds only the named providers, and refuses otherwise. Rule-7 screens are stopped until xian says how a provider key is handed to a seat (Lead raised it via Exec). Leftover fake Slack test entry in his keychain, and his start scripts: xian's call via Exec.
  - **ADR-081 D3's condition is met (#2174, decisions.log 18:56).** D3 governs; the OAuth App fallback is off. The ADR holds the result, both tables, the 401 correction (the old token's 401 is explained by its 8-hour expiry, not by revocation on refresh), and the narrowed refresh mapping: a rejected refresh is STALE_TOKEN, read from the reply's `error` field; a refresh that could not complete is UNREACHABLE with the stored pair untouched; never CONNECT_REQUIRED. Open: the running github-mcp-server version line (xian's Fly read, or #2341's script on its next run).
  - **#2342: superseded by the 11-12 block above.** (11-11 text:) My rulings on the issue: classic grants go STALE at cutover; only a grant with an explicit App marker serves; tokens are deleted and a revoke is attempted (failures counted, not blocking); a new `status_reason` column on connector_bindings (`cutover` or `refresh_rejected`, cleared on rebind) picks the words; the migration keeps `connector_configs` byte-identical; on a rejected refresh, re-read the store before mapping. **Validate the landing against all of these.** CXO's final words are on the thread.
  - **Closed or settled today:** #2337 (the repositories-503 row; condition 3 met by the stub's evidence, and the sink is blind to aiohttp: `aiohttp.ClientSession()` defaults trust_env False); #2232 method rows; #2340; #2338.
  - **Open, not mine to move:** #2328 (CXO's word); #2335 (xian via Exec); #2333 (Lead/PPM); #2261 now lands on D3 via #2342 (PPM sequencing; invite hold waits on 2261 and 2292).
  - **Lessons (11-11):** (1) Estimated stamps, five today. The habit that works: back-references come from `grep` of the line itself, and new stamps from `$(TZ=America/Los_Angeles date +%H:%M)` inside the heredoc. Never type a minute; never write a memo ID before the send returns. (2) No literal token-shaped placeholders in any committed file, not even fake ones: describe them. (3) Never filter mail-send or mail4 output. (4) The proxy sink cannot see aiohttp; never cite it for an aiohttp path. (5) A ruling's count must come from the grep output, not a glance (12 vs 10 users of the binder).
- **11-10 STOP (21:27 fire).** Main 12/12 green. Alpha serves `c425fd242f` (#2328 complete; Web's browser served check pending, CXO judges, Lead closes).
  - **Rulings today:** #2328 validated from source (18:23; the pronoun check is a word-set check and asks, writing nothing; note: the router path picks over all active todos, not the due pool). #2232's database rows (decisions.log 19:02): scratch database plus a revoked grant, with the app on a non-superuser, non-owner role, a probe proving the denial first, and the report naming InsufficientPrivilege and the `except Exception` branch. Lead owns #2232 now.
  - **Open, not mine to move:** #2335 (xian's live-log check, via Exec); #2333 (Lead or PPM to schedule); #2328 (closes on CXO's word); #2232 (Lead building).
  - **Lesson (11-10):** 165 memos from 11-07 to 11-09 sat in inbox/ unfiled while fires reported "mail checked, nothing new". Filed by log evidence plus reading 16 in full (22d7330af). Every mail wake files its memos in the same mail-send call as the reply. A "nothing new" line must also mean "inbox/ holds only MANIFEST".
- **11-08 and 11-09, still open:** #2322 (P1, the served stored-done row via the #2325 reset); builds owed by Lead from 11-07 rulings: #2324, #2321, #2326 (Backlog); #2330 and #2327 (PPM placing). Standing: `ROUTER_HIDDEN_CEILING = 3` is the last raise (exit #2149); `CONSENT_NARROWING_ALLOWLIST` holds the forget aliases only. Full text in git history.
- **11-05 STOP block, carried** (not re-verified tonight beyond the 06:27 START check):
  - **Invite hold (PPM):**
    - met: #1551, #2283, #2178;
    - P0 open: #2261 (D3 chosen 11-11; lands on #2342) and #2282 (live since 12:47, acceptance below);
    - P1: #2157, #2158.
    - No invitations of any kind.
  - **#2282 (beta canonical, alpha 301s):** served, and my curl probes of the boundary pass (12:51). The MCP OAuth issuer stays `https://alpha.pipermorgan.ai/mcp/oauth`. Kept unredirected on alpha: /mcp/oauth/*, both .well-known paths, /login, POST /api/v1/auth/login, /static, /assets, /health. Open acceptance:
    - Web's GitHub Connect from beta: the start mints a beta redirect, but GitHub's page and the landing need xian's word for the dinp-machine sign-in;
    - xian reads Connected apps and revokes the old Claude row (an old client's refresh token can live up to 30 days);
    - step 5, removing the alpha callbacks, about 11-12.
  - **Validated today:**
    - #2283 (served end to end; the callbacks stay middleware-exempt behind a pinned route check);
    - #2178 (box 4 passed);
    - #2284 (gate at the one use-path read);
    - #2280 (15 sites; the list helper's degrades marked DEGRADED);
    - #2288 (a card 401 marks the binding stale, only for the rejected token);
    - #2262 (publisher registered; four Notion write methods);
    - #2282's code.
  - **Watch:** the #2288 served row needs a dead-grant dinp-machine test account whose card nothing has read yet (five such accounts exist).
  - **#2258:** the claim names three services, Slack, GitHub and Notion. It widens only when a connector's forwarder joins TRANSPORT_MODULES and its methods join CLIENT_METHODS, in the unit that adds its writes.
  - **Mail v4** opens to every seat Mon 11-09: also read `python3 scripts/mail4.py inbox --role arch` (check-mailbox v1.2). v3 is the fallback to 11-23.
  - **Carried, unchanged:**
    - #1858's write-leg amendment;
    - #2264 (xian);
    - #2238 (xian's line);
    - #2244 (durable data root, Lead);
    - #2242, #2235, #1680;
    - #2226, #2259 (placement).
  - **Lesson:** stamp from `date`'s own output. Four stamps went ahead of the clock in two days (19:15, 09:34, 10:33, 12:52); copy the minute, never type it.
- **Still open from 10-27..10-30** (the full text is in git history and those days' logs):
  - **#2186:** unit 2 (declared args keys) is owed by Lead, with Rule 7. `timeframe` still drops silently.
  - **#2184:** owed by Lead: don't arm when the repo resolves to None. The served two-step row is PPM's close bar.
  - **#2189:** waits on Lead's builds, in order: row 1 slice, then nonces to Redis, then the Test table (xian's migration word).
  - **#2209:** waits beside #2197.
  - **#2227:** #2149 ended 11-01 10:48 (two-stage rejected), so the 5.5 re-baseline runs on the flat catalog. Owed by Lead when scheduled.
  - **#2184:** now goes through the #2197 resolver (op-local, per #2149's close-out).
  - **#2042 rung-3 census:** blocked on a read path for alpha's turn metadata.
  - **#2018:** PA's card waits on xian.

## Standing hard rules (load-bearing; full incident detail in decisions.log if ever needed)

1. Never glob the inbox — read-then-append-to-move-list in the same call; verify drains at trunk.
2. State the scope IN the ruling — name the object, a non-covered adjacent thing, the clauses.
3. Verify the claim before ratifying, always — a check run five minutes ago isn't a check run now.
4. A `grep` line-hit is a pointer, not a quote — a claim about what N sites DO requires opening N
   sites, including the branch below the cited line.
5. A denominator that doesn't travel with its number isn't a denominator.
6. Before claiming a route/handler change reaches users, check what MOUNTS it (`grep -rl
   <router_name>`) — editing the file that defines it isn't evidence it's wired to anything.
7. Introspective continuity ("I remember it, none of it reconstructed") is NOT evidence a process
   didn't restart — a `--resume`d session feels identical to unbroken memory by construction. After
   any suspected restart: check permission mode, Remote Control, and model against what was last
   recorded, don't infer from what you remember.
8. A checkbox/status glyph can be a document's SUBJECT MATTER, not its claim — a synthetic-test
   fixture built to be detected-while-checked looks identical to a real completion marker if you
   read it in isolation. (Earned 2026-09-23: closed #1744 on its own `[x]`, which was the test
   fixture's deliberate target state; the issue's own comment said so, one comment away from the
   checkbox. Caught and reopened same fire. Read the whole artifact's stated purpose before acting
   on a fragment of it — rule 3's failure mode, one level up.)

## Standing guard

ADR-078 D4: the classifier stays stateless — also an ESSENCE standing rule.

## Dormant / background (watch only, none owed)

#1481 Slack principal · #1459 original_message ratchet (Lead's build) · #1462 PDR-006 · #973
MEM-CACHE · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.

