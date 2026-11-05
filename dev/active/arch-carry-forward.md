---
last_updated: 2026-11-04 21:27 PST (STOP)
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

- **11-04 STOP (21:27 fire).** Main green 12/12. Alpha serves `72bd53546a` (Lead 19:34). Every ruling today is in decisions.log, 07:10 to 21:11. xian's 19:31 tenancy ruling: P0 is #1551, #2261, #2178; #2157/#2158 are P1; no invitations of any kind.
  - **#1551: MET by PPM's bar** (Tests green on `56b284defb`; validated 18:34, 19:10, 19:45, 20:21). The lint baseline holds 11 sites, Slack (#1481) and Notion (#2238) only, behind the offer pin and the allowed-set pins. Unresolved reads are count-bound (UNRESOLVED_COUNTS). Watch: any new SYSTEM_ONLY entry is a ruling of mine.
  - **NEW, P0-class, ruled 21:11, Lead builds at the 11-05 START:** the OAuth callbacks (GitHub, Calendar, Slack) bind the grant to the state's user, never to the browser's own user, so one account's Connect link can store another's grant. The unit: the session user must equal the state's user, else store nothing and show an HTML error; the calendar and slack paths come off EXEMPT_OAUTH_CALLBACK_PATHS; the start-host redirect (#2281(b)) is required; two-account pins per connector. Validate it against all four. Exec puts the P0 label to xian in the morning; PPM files it or folds it into #2281. Keep the public text to the class description.
  - **#2178:** validated (b5df29d4e6, a 404 confirmed by GET /user). It rides the next promotion; confirm the served sha carries it.
  - **#2174 / #2261:** the check script is validated (writes locked, narrowing row). xian runs it in the morning, then the refresh run 8h later, before D3 is chosen. If both pass, D3; if not, public_repo with CXO's two conditions. Lead records the result in ADR-081 D3.
  - **#2282:** the canonical host (PPM: beta.pipermorgan.ai). Whether to move is xian's and CXO's call; if yes, it is one unit in my 20:51 shape, before invites.
  - **OAuth Apps:** both are under the `pipermorgan` org with wildcard off (xian 20:55). Unconfirmed: whether staging's beta.* callback is gone (xian's morning look). Web's repeat of check 1 needs xian's yes for a second revoke.
  - **#2188:** done. #2280 (NOT_CONNECTED, 16 sites) is placed in H, not before invites.
  - **#2157 / #2158 (P1):** lines and data half are ready, with my three fixes and three answers in; nothing runs until PPM reaches them.
  - **#2227:** closed. Haiku 4.5 stays; the catalog unit is Lead's, on the screened path.
  - **Carried, unchanged from 11-03:** #1858's write-leg amendment (validate on landing); #2264 (xian's read); #2238 (xian's machine-exec line); #2244 (durable data root, Lead); #2262 (Notion audit); #2242/#2235/#1680; #2226/#2259 (placement).
  - **Lessons today:**
    - A lint that resolves names must fail closed on the names it can't resolve; I measured 20 such reads.
    - A 404 isn't proof of absence; confirm it by a different method.
    - Read the callback for whose session it trusts, not only whose state.
    - Stamp at the clock: 19:15 was corrected to 19:10, and four stamps earlier in the day.
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

