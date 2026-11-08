---
last_updated: 2026-11-07 21:28 PST (STOP)
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

Day blocks before 10-27 were cut at the 10-27 STOP rewrite; their threads are resolved, carried below, or in their own day's log and decisions.log. Prior text is in git history (`git log -p -- dev/active/arch-carry-forward.md`).

- **11-07 STOP (21:27 fire).** Main green 12/12. Alpha/beta last served `f9b4c737f7` (N1 words, #2325 reset). Every ruling today is in decisions.log, 06:30 to 20:50.
  - **Shipped and validated today:**
    - ADR-083 D5 is ACCEPTED (xian's go 08:04) and served. The D5 ceiling is FINAL at 1.5 s (10 of 10 bound, CXO's bar); the log confirmation was dropped.
    - #2320 STRUCTURED filter profile (Tier 1 only for inversion_routing, todo_selection and milestone_resolution), pinned set, ceiling 2 hidden: validated and proven served.
    - #2322 guard (a set of more than one never auto-applies in the #1605 tree) and #1605 narrowing ("clear todo 2" binds line 2 from the recorded list): validated.
    - #2321 (d), the todos-or-reminders choice; reminders-with-none; the no-list grouping; N1 words: served PASS.
    - #2324 date line and #2325 reset (one `forget_verified_inference`): validated.
  - **#2270 (sprint item 8), owed on landing:** Lead's handler (c76d7a7f70, 27f42eb2b3, 700d7ff874; gates z20–z22). It goes out in 11-08's first window (07:00 or later). On landing, validate against:
    - **20:14:** resolve via #1641, read one repo, record_read after that read, curated floor; `router_visible=False`;
    - **20:26 ratchet:** ceiling 2, exit #2149, a landing pin, a docstring note;
    - **20:38:** a failed, unlisted word/word always asks;
    - **20:50:** a code-rendered "Looking at {repo}, your default repository." when the person named none.
    - The gather record (6540fa6787) stays retired.
    - **PA's pass line:** the advisor's words ×6 with no document reply and at least 3 of 6 giving feedback with a next step; gap B by name; turn 2 in Lead's wording ×2, with no recanting.
  - **#2322 (P1, open):** the served stored-done row now runs on a test account via the #2325 reset (store done, run `clear todo 2`, reset). It closes on that plus the pins.
  - **#955 forget (PPM places; not this sprint):** one deletion path; the next ask is the first-time question; no confirm. Condition: say "forgotten" only after a read-back.
  - **Rulings made, builds pending (Lead):**
    - #2324: "now overdue" on every milestone render; the time reply carries both days.
    - #2321: reminders-with-none.
    - #2326: armed read offer (gap C), Backlog.
  - **Correction on record:** 19:38's #2270 turn-2 "served" was wrong (a different route); corrected 19:40, and the memory was updated.
  - **xian:** `fly auth login` (Lead's log capture) is no longer needed for D5.
  - **Lessons (11-07):**
    - I cited stamps I hadn't read back three times (17:53, 17:55, 19:41) and wrote "x" minutes twice; copy the STAMP echo into the memo.
    - Read the route stamp before counting a served pass.
    - Read the approval's own bound before setting a number (3.0 s overreached xian's 2.5 s; memory saved).
- **11-05 STOP block, carried** (not re-verified tonight beyond the 06:27 START check):
  - **Invite hold (PPM):**
    - met: #1551, #2283, #2178;
    - P0 open: #2261 (waits on xian's #2174 runs; the refresh run comes before D3 is chosen) and #2282 (live since 12:47, acceptance below);
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

