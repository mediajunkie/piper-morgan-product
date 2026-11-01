---
last_updated: 2026-10-31 21:30 PDT (STOP)
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

- **10-31 STOP (21:27 fire, closed 21:30).** **Alpha serves 0.9.0.0 `c44dd081cb` (the #2245 promotion, which carries `5df1db03fa`); the morning build `5f0112c00c` carried every landing I validated today (`66d4b58492`, `e394cb4c21`, `eef219a196`, `4580960112`). xian dispatched the #2245 promotion tonight (run 41272799100). **PPM holds the v0.9.0.0 tag** until that build's PA quote, parity and row 2 are in. The hosted MCP serves v18 `a8a01b96b4`, with no services/mcp diff from the validated guard.
  - **First Production sprint set** (PPM 21:2x; `docs/internal/planning/first-production-sprint-candidates-2026-10-30.md` "xian's answers").
    - **Mine:** #2149's design and #2042's diagnosis plus its first fix. **Both done tonight:**
      - #2149: two-stage routing, record `design-records/2149-router-catalog-shape.md`, licence preregistered. **Next: draft the `route_group` enum with Lead** (first cut from Lead or me), then validate each build step.
      - #2042: option 1 specified. CXO's Time bullet arrived by 21:33 (CXO's memo, filed), so option 1 is fully specified. Lead builds it.
    - **Lead's order:** #2242 (a) at 11-01 06:47 (go given, on my 3 gate points and 3 store conditions), then #2238 and #2235, the #2184 family, #2149, then #2195 and #2197. **I validate each on main.**
  - **#2226 (local embeddings) ruled:** int8 MiniLM on onnxruntime in our own Chroma function; conditions (a)–(l) on the issue. Waits on placement. **#2244** (vector store at `/app/data/chromadb`, off the volume; filed by me) comes first.
  - **#2245** validated at `5df1db03fa`. Its served quote rides the promotion above.
  - **#2247** (Slack as a source via the hosted MCP, back in 1.0 on xian's word): six conditions are on the issue. Lead sized it at 4.5–5.5 days. It needs xian's `tools/list` token test and #1514's app review (xian's). Not in this sprint.
  - **Q37/Q38** relabelled to canonical (`f769c74ed8`). The #1979 condition is met by branch order (`workflow_entries.py:1277` before `:1383`).
  - **Waiting on xian:**
    - the `PIPER_INVERSION_LIVE_CATEGORIES` paste (CIO's memo: printenv, then append exactly `set_default_repo`), after the tag's row 2. CIO's mirror `79004122c0` is read and correct.
    - the #2244 `ls` and #2226 condition (i)'s RSS. **No agent seat can do Fly production reads.**
    - a fresh account for A1/A2 (PPM's call).
  - **Rules learned today:**
    - read the clock before every stamp; I wrote four stamps ahead of it today, all corrected;
    - quote a sha only from origin/main after the push;
    - wait for a likely product view before ruling a disposition (#1780);
    - read the call before naming a second site (#2245);
    - don't assume a seat can do production reads.
- **Still open from 10-27..10-30** (the full text is in git history and those days' logs):
  - **#2186:** unit 2 (declared args keys) is owed by Lead, with Rule 7. `timeframe` still drops silently.
  - **#2184:** owed by Lead: don't arm when the repo resolves to None. The served two-step row is PPM's close bar.
  - **#2189:** waits on Lead's builds, in order: row 1 slice, then nonces to Redis, then the Test table (xian's migration word).
  - **#2209:** waits beside #2197.
  - **#2227:** ruled 11-01 09:28: #2149 runs on the served Haiku 4.5 first, then the 5.5 re-baseline runs on whichever shape survives. Owed by Lead after #2149's result.
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

