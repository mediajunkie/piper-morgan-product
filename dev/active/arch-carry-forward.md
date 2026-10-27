---
last_updated: 2026-10-26 21:27 PDT
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

Day blocks before 10-26 were cut at the 10-26 STOP rewrite; their threads are resolved, carried below, or in their own day's log and decisions.log. Prior text is in git history (`git log -p -- dev/active/arch-carry-forward.md`).

- **10-26, closed at 21:27.** Alpha serves `69d859ca5f` (healthy, /health 21:27), promoted 07:06 by Lead. It carries only Arch-validated code (#2172's `12bb67b682` and `76b39a3133`, #2176's `2d0c56082a`). Code Quality on main: success. Tonight's invitation send was planned on this build (HOST 17:58); Arch has not seen confirmation that it went.
  - **#2177 (pull by digest):** xian said yes (HOST 17:58). Merged as `532174d9d1`; its 3 files equal `a56a77a9ff`; Tests passed on `323712e284`. **Owed at 07:00 10-27:** Lead's promotion. Read its log: the pulled `RepoDigests` equal the digest read, and the attestation passes. A refusal on a missing `image_ref.digest` leaves alpha unchanged. The optional digest-deploy tightening is Lead's follow-up after a passing digest run.
  - **Closed today:** #2171 (served), #2172 (pins-only; served on a PAT account only), #2176 (served), #2109 (pins-only), #2125 (pins-only). `label:architecture` open: 10.
  - **#2018 (dead GitHub connection, recovery from the UI):** PA's card waits on xian's 15 minutes, via Exec. Arch checked step 3 on source (#2018 comment 6428824719): GitHub Disconnect never calls GitHub, so a grant revoked there can't change its answer.
  - **#2178** (GitHub-side revoke on Disconnect; never a PAT): placed in C. Validate when Lead builds it.
  - **#2174** (ADR-081 D3 check): Lead, after D1 (#2151). Blocks #2163 and #1514.
  - **Shared-slot keychain rows:** deleted by xian (52→50) and both testers told (HOST 17:54). Thread closed.
  - **Carry-over:** the 10-22 key reset was staging's (HOST's 10-22 log, 16:28). The promise rests on #2157 (backups) and master-key custody; the decision is xian's, via Exec.
  - **Practice:** take every memo/comment timestamp from `date` in the same command that writes it.
- **Still open from earlier days (each with its owner):**
  - **Lead's ADR-081 D2 env-token reads plus their forcing test:** validate from source plus Tests when they land.
  - **#2166 Share repair (Production D, Arch's design, decisions.log 10-24 18:45):** validate when Lead builds it.
  - **Haiku 5.5 router/classifier screen:** about $4, rule-7 batch. Waits for 11-01, or for a cap from xian via Exec. Screen it before #2149.
  - **HOST, with xian present:** the served refusal check (a chat turn from an account with no key of its own) and HOST's Drafts 1 and 2.
  - **#2139** and **#2135** (dormant, tripwire landed). **#2112:** the connected-account row (xian). **#2123:** closes when the ADR-081 D2 gate plus its pin are live.
  - **#1897 (unit 4b):** measure single-op accuracy before shipping. **Q5 denominator:** open (flat test recommended). **Bets 001–003:** PM TO FILL.
  - **GitHub criteria line:** open each `label:architecture` issue at START rather than writing a row from the list.

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

