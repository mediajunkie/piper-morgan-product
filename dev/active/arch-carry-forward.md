---
last_updated: 2026-10-24 21:28 PDT
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

Older day blocks (10-04 to 10-23) were cut at the 10-24 STOP rewrite; their threads are resolved, or carried below, or recorded in their own day's log and decisions.log. The full prior text is in git history (`git log -p -- dev/active/arch-carry-forward.md`).

- **10-24, closed at 21:3x.** Alpha serves `228f3cec14` (/health 21:28), and Tests passed on `aded293a06`. Detail is in the 10-24 log and decisions.log (15:29 to 19:21).
  - **Law written today:**
    - **ADR-081** (GitHub identity): ACCEPTED, with D3 conditional on the github-mcp-server compatibility check (Lead runs it before any build; the fallback is a published OAuth App with the narrowest scope).
      - Lead's build order: D2's gate (`71fb4b0db7` done: "system" token is None on a hosted deploy), then D1's gate convergence (#1966/#2151), then D3's check, then D3.
      - **Lead's five env-token reads plus their forcing test** were parked for 10-25 START in a fresh session (Lead's named trigger: the ISS pins need their own tested unit). **Validate that landing from source plus Tests.**
    - **ESSENCE v1.1 draft** (`docs/internal/architecture/essence-v1.1-draft-commitment-6-and-prd-note-2026-10-24.md`): waits on xian's ratification through Exec, together with the `promises.yaml` wording. On ratification, apply it word for word and log it.
  - **#2151's five states:** verified; failed ("couldn't check"); narrowed; not performed (no stored credential *only*, per the 07:55 narrowing); substituted. A store error is a failed read. Everything validated today is in the log. My own miss: the 07:55 validation didn't catch the swallowed store failure in `is_available` and the PAT legs; fixed after 16:49.
  - **#2169 CLOSED** (served 3 of 3, CXO 20:21; `close:pins-only` for the project variant). The containment rule with the to-do-family own-list carve-out is law.
  - **#2166:** Share is hidden (served pass). The repair is Production D, on my design (decisions.log 18:45): a grant to the typed email, resolved recipient-side against `users.is_verified`; one `resource_shares` table; an owner-only `GET /{type}/{id}/shares`; a lowercase role enum. Validate when Lead builds it.
  - **#2171** (Lists "Items: 0"): fix `dff452482b` validated (21:3x comment). Served rows are owed after the next promotion (Lead/Web/CXO).
  - **#2167 and #2156 CLOSED** (CXO). CXO's nit to Lead: map provider ids to display names. It is not a gate and not mine.
  - **Living map:** the journey grid has three columns (web, mcp, chat platforms in grey); the moment list is ratified; seam labels exist; the edge rule is adopted; PPM's generator is built but **not published**. `close:` labels exist (served / pins-only). Watch the publish.
- **Still open from earlier days (each with its owner):**
  - **The Haiku 5.5 router/classifier screen:** about $4, rule-7 batch. Waits for 11-01, or for a cap from xian via Exec. Screen it before #2149.
  - **HOST, with xian present:** the served refusal check (a chat turn from an account with no key of its own) and HOST's Drafts 1 and 2 (DB reads).
  - **#2139** (doc from the conversation) and **#2135** (trust stage, dormant, tripwire landed).
  - **#2112:** only the connected-account row is open (xian's calendar account via Exec).
  - **#2123:** CXO's served cross-account row (needs a second GitHub account with a private repo). ADR-081 D2 removes the last leg; it closes when the D2 gate plus its pin are live.
  - **#1897 (unit 4b, router `plan` outcome):** not urgent; measure single-op accuracy before shipping.
  - **Q5 denominator:** still open; my recommendation is the flat test. **Bets 001–003:** PM TO FILL, tracking only.
  - **GitHub criteria line:** 9 open with `label:architecture` (21:28). Open each issue at START, rather than writing a row from the list.

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

