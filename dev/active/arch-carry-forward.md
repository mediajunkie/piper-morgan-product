---
last_updated: 2026-10-30 21:28 PDT
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

- **10-30 STOP (21:27): MVP passed (xian's Go on #1386 at 17:03). Alpha and beta both serve `ac5b69f865`, one machine. Letters go Sat 10-31 AM; no promotion until they've gone (landing on main is fine).**
  - **Validated on main today:** the seven morning landings; #2222; #2223 (also served: PA re-check 3, a "yes" without sign-in wrote nothing); #2215; #2225 (`47a9f431db`, closed, `fix:not-served`); the text-block pick plus harness flags (`52166af214`); the #2230 setter validation (`05b58c36b3`, writes only on 200); the #2236 notice (`6961a252a0`); #2236 render plus #2233 reminder line (`878e244157`) and the four fixes (`93bd29ccd7`); #2237 guard, page and wizard (`a3b3645787`); the connect listing (`5c7f15d794`). CI 12/12 green at 21:27.
  - **NO-GOs today:** Haiku 5.5 drop-in (router stays 4.5; **#2227** re-baseline); #2195 (a) example (literal 32 stays; **#2195 waits on #2149**, no more single-field STATUS edits); (b) set_default_github_repo pointer (wrong premise: `set_default_repo` exists).
  - **Lock-down done:** the Slack inbound gate is unset (xian, 20:23) and PA's served read at 20:25 is `disabled` on both hosts. CIO's names-only read: no global Notion or Slack keys.
  - **Waiting on xian:** the by-name word to add `set_default_repo` to `PIPER_INVERSION_LIVE_CATEGORIES` (exactly that name, never QUERY), applied by CIO/HOST (HOST only with xian present), timed after the letters. Then PA's probe: it writes, PA confirms, then clears.
  - **Next promotion (after the letters):** served checks on PPM's list (row 2 full, row 3 A1/A2 + B confirm/reverse; #2225 three turns; #2236 capability reply; #2233 Q1 + greeting/list line; #2237 page, wizard, "connect my slack"; "what have you learned" empty). I validate any landing in between.
  - **Filed today:** #2222, #2223, #2224, #2227, #2235 (validator reads PAT only; OAuth accounts never validated), #2238 (Notion N1/C1 plus store caveat).
  - **Rules recorded:** search for the capability, not the string, before ruling it missing; a ruling resting on another component's behaviour says whether that was verified; gate chains use pipefail and push only through `&&` from pytest; code-appended lines are computed before the turn is saved.
  - **First Production sprint:** PPM's candidates name my #2149 (catalog shape) and #2042 (diagnosis then first fix). Both wait on xian's priorities talk.
- **10-29 STOP (21:27):** alpha serves `e234776150` (the third promotion, #2205). xian ran A3/A4 tonight. **PA's hold on tested-path pushes holds Lead's queue.** Landing order, each on its own gates; **Arch validates each on main:**
  1. **ledger-only** `claude/lead-ledger-only` 400b21addb: the append-only catalog order, render byte-identical. decisions.log 19:39.
  2. **#2042a** `reference_relations`: whole-word title match; a dot between alphanumerics is in-word. GO.
  3. **#2207** (repo-question principal): GO.
  4. **#2209** `claude/lead-2209` dd296fe38d: armed-pick no-match. One helper at the `_handle_floor_with_context` and `_handle_unknown_intent` heads; GUIDANCE category excluded; ethics door untouched; CXO's unquoted line; 22+1 pins. decisions.log 20:29.
  5. **#2151 STATUS-gather FLOOR-ABSENT fix** (Lead's lane is running it).
  6. then the **get_project_status entry** `claude/lead-2195-entry` c2643c4ddc. KNOWN_RED stays 14 (decisions.log 21:08); the entry lands with its FORCE row green or at the lowered ceiling.
  - **Scorer baseline:** 491/550 from the entry's landing (the 10-02 read_floor clause).
  - **After that:** a rule-7 description/example unit lifts "any update on the next milestone" from 0.72 to ≥0.8 ×5, paraphrases ×6 included, which licenses **deletion 32**. No per-op floor (ruled 20:04).
  - **Sort-by-name is NO-GO** (495→477); my 18:57 shape is superseded.
  - **#2211** filed: delete the dead `_handle_guidance_via_floor` on rule-10 gates.
  - **#2205** re-read: GO 18:28 (comment 6512687247). Residual: the standup skill (CLI-only) must read `get_user_write_target` if it is ever chat-wired.
  - **#2184** off MVP (known issue); the retry bundle's entry half waits on the ledger plus entry.
  - **#2042 rung-3 census is blocked: no read path for alpha's turn metadata** (asked Lead for a read-only aggregate). Option 1 waits on 2042a landing.
  - **Haiku 5.5 screen: NO-GO 15:20** (4 named rows + 1 sentinel move ×6; corpus 473 vs 488). Router stays on 4.5; #2227 re-baseline filed. #2195 (a) NO-GO 16:1x (example moved next-milestone sentinel); literal 32 stays, #2195 waits on #2149; no more single-field STATUS edits; #2184 w3 parked to #2149; text-block pick + harness flags land alone. #2225: build in the carrier (one binder; re-ask gated on persist_default); (a) rejected, (b) under rule 7 after #2195 (a). #2228 (Q9 time slip, H/#1828) filed by PA. #2223 validated served (PA re-check 3, ac5b69f865).
- **10-28 STOP (21:27):** alpha serves `49e0904c3c`, carrying all of today's landings (#2184 pick + condition-1 fix, Open 1, ratchet fix, #2185, #2187). **#2189 is fully ruled** (comments 6482389530, 6482462708, 6482619087, 6482866467, 6483099163; decisions.log 15:33 / ~15:5x / ~16:0x / ~16:1x). It waits on Lead's builds, in order: row 1 slice (+8, 10, 11, 19) → nonces to Redis → Test table (xian's migration word via Exec). **Arch validates each build when it lands.**
- **10-28 (15:27 fire): landings validated, plus #2189.**
  - **#2186 Open 1** is on main (`355e04beba`) and validated (6482315954). Unmeasured edge: the PR rail with `state:"open"`. Unit 2 (declared args) is still owed by Lead.
  - **#2184 pick** is on main (`bbcd5f0fd8`); conditions 2–4 met (6482316386). **Owed by Lead:** don't arm when the repo resolves to None (condition 1 gap). The served two-step row on the next promotion is PPM's close bar. The candidate is `9ea9081737` (it carries the ratchet fix); dispatch is xian's.
  - **#2189 ruled persist** (6482389530; decisions.log 15:33): Postgres, write-through, `forget` deletes the row. Lead sizes it; CXO owns the card copy. Census POSTED (6482462708); offer-store direction: persist inside hydrated context state (decisions.log). CXO gives the verdicts, and Lead files fixes per misleading or harmful row.
- **10-28 (through 12:40): xian asked that the confabulation class be "diagnosed, not patched" and prioritized in private beta.**
  - **#2042** (PUB, first; PPM). Arch's diagnosis is comment 6476054813: record claims made from context slices with no read of the asked scope; #2184 mis-attributed real numbers. The guard is ruled as `floor_record_references` (6476332180) and landed in `e4ed14caf9`, validated (6476687425). **Owed by Lead:** record *every* source key per reference, not the first sorted one. **Census:** Web's five-exchange replay waits on xian signing Web in as web-pat-test; Lead tails Fly live. Add the two-step "MVP" form.
  - **#2186** (qualifiers): unit 1 is `b2b928ee46` plus CXO's words in `bf829e7181`. Validated as promotable, not done (6478561360). **Open:** (1) undeclared args keys still drop silently (`timeframe`), an E4 problem; (2) declared argument keys on `WorkflowEntry` stay owed as unit 2 (Lead's x3 shows `limit`/`count` drift), which needs rule 7's x6 screen.
  - **#2184** admitted to MVP, Class 3 (PPM). Its honesty minimum rides #2186 unit 1. Promotion of `879d18bf72` is xian's dispatch.
  - **Skills answer to xian:** the gap is per-operation declared args, not skill files; skills fit the MCP/Desktop surface (decisions.log 10:32).
- **10-27, closed at 21:27.** Alpha serves `a1f46faafc` (healthy, /health 21:27), promoted 20:23–20:27 by Lead (run 40626442042). It carries #2182. Code Quality on main: success.
  - **#2177 (pull by digest):** served on `36bdcf09bb` at 07:08 and closed.
  - **#2181 (deploy by the pushed digest):** `681e0d721d` validated on source plus Tests. Served on run 40626442042 and closed. Arch checked 3 of 3 conditions in the printed log (#2181 comment 6460666875).
  - **#1703 (MCP standup):** not blocked by #1441 (decisions.log 10-27 18:29). Its edge is #1703 ← #2182. The #1706 Sprint move is xian's, via Exec.
  - **#2182 (a failed calendar or source read shown as a free day):** both halves validated on source plus Tests: `449bd287fa`, and `ddd8a17fa1` (the GitHub gate keeps `check_failed`). CXO's copy edits are in `a3f95c4c6c`, and CXO keeps the grouped clause. Now served on alpha. **Waits on:** Web's served rows 1–3 (Lead's 20:28 memo), then CXO's words. Row 3 is `close:pins-only` unless Web can force it safely. Arch owes nothing further unless a row fails.
  - **Briefings:** ESSENTIAL-ARCHITECT refreshed (line counts, plan path, web-chat sequencing marked superseded). CURRENT-STATE's Alpha line is now `a1f46faafc`.
  - **#2018 (dead GitHub connection, recovery from the UI):** PA's card waits on xian's 15 minutes, via Exec. Arch checked step 3 on source (comment 6428824719).
  - **#2178** (GitHub-side revoke on Disconnect; never a PAT): validate when Lead builds it.
  - **#2174** (ADR-081 D3 check): Lead, after D1 (#2151). Blocks #2163 and #1514.
  - **Carry-over promise:** rests on #2157 (backups) and master-key custody. The decision is xian's, via Exec.
- **Still open from earlier days (each with its owner):**
  - **Lead's ADR-081 D2 env-token reads plus their forcing test:** validate from source plus Tests when they land.
  - **#2166 Share repair (Production D, Arch's design, decisions.log 10-24 18:45):** validate when Lead builds it.
  - **Haiku 5.5 router/classifier screen:** about $4, rule-7 batch. Waits for 11-01, or for a cap from xian via Exec. Screen it before #2149.
  - **HOST, with xian present:** the served refusal check (a chat turn from an account with no key of its own) and HOST's Drafts 1 and 2.
  - **#2139** and **#2135** (dormant, tripwire landed). #2112 and #2123 are now closed.
  - **#1897 (unit 4b):** measure single-op accuracy before shipping. **Q5 denominator:** open (flat test recommended). **Bets 001–003:** PM TO FILL.
  - **GitHub criteria line:** open each `label:architecture` issue at START rather than writing a row from the list (10 open at 10-27 21:27).

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

