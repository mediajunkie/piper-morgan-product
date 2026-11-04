---
last_updated: 2026-11-03 21:27 PST (STOP)
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

- **11-03 STOP (21:27 fire).** Main is green, 12 of 12 workflows. Alpha serves `63d486043a` (Lead promoted at 20:00 under the standing grant; the earlier one, dispatched at 18:26, was `b0f774aabb`). Every ruling for today is in decisions.log (07:10 to 19:40).
  - **Closed today (by CXO):** #2258 and #2197. #2042's aside passed its served check; whether the issue closes is PPM's and Lead's read.
  - **Validated on main and served on `63d486043a`; checks owed in the morning:**
    - #2098, answer-turn bind (`176136c063`, `f85ecfe3b7`). My 11-02 re-ask was reversed for that turn. PA runs T1c then "file it as is", a "no" then file, and a "yes" to case 1 then file.
    - #2265: the window starts at the local start of yesterday (`e5a61be77d`). CXO's row. The strict calendar day rides #2186.
  - **Ruled, not built:** #1858's write-leg not-found amendment (decisions 18:53, four conditions). Lead builds it at the 11-04 START. Validate the landing against all four conditions and the five pins. PA's F1 waits for the promotion after that.
  - **#2264 (`data/postgres`):** untracked (`66e4e8fdce`, validated). The early Piper schema has a `stakeholders` table, so my no-rewrite advice lost its premise. Next: xian runs Lead's read-only line, then decides on the rewrite. Agents don't read it.
  - **#2238:** the staging-account guard is validated (`2e562df09e`, an allowlist on `FLY_APP_NAME`). Waiting on xian to run the `fly machine exec` line.
  - **#2244:** confirmed. Lead owes the fix: one durable data-root config for chromadb and `SpatialMemoryStore`. Validate it when it lands.
  - **#2262** (Notion writes unaudited): validate against my ratchet notes when it's built (`notion_adapter.py` goes in `TRANSPORT_MODULES`; `publisher.py` gets deleted or registered).
  - **#2242:** the last row is xian's (remove, PA's refused call, add, reconnect). **#2235:** the wizard half needs an account that signs in only through Google; per Lead it can run on staging. **#1680:** the row judgement is Lead's.
  - **#2226:** about 475 MB of headroom on alpha (Exec 17:13). Still waits on placement. **#2259:** not built; PPM places it.
  - **PDR-102 trigger:** I write the connector-source ADR when the first connector-ingest unit is placed. #2262 is not that trigger.
  - **Lessons today:**
    - Read every line of a served listing (the `postgres` entry was the finding).
    - Where a turn sits sets how much an unsure router counts: on the answer to Piper's own question, a CONFIRM binds.
    - Stamp at the clock, never ahead of it (18:55 was corrected to 18:51).
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

