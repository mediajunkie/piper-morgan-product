---
last_updated: 2026-09-25 21:5x
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
| Model | **Opus 5.5 as of the 2026-09-25 ~22:0x restart** (Pard, PM-authorized) — supersedes the Sonnet-5 line below, kept for history. Sonnet 5 was intended per PM's 2026-09-21 ruling (fleet-wide, Opus is most token-expensive; Lead is the one exception, on Fable) until this restart. **Verify what you're actually running, don't assume the restart's stated intent succeeded** (rule 7). |
| Wake mechanism | ⚠️ **SESSION CRON RETIRED 2026-09-25 21:2x, PERMANENTLY — do not re-arm.** Pard migrated this seat to an external LaunchAgent, same schedule (`27 6,9,12,15,18,21`, from the registry), measured on-time where the session cron ran consistently +30 late. `CronList` should show zero jobs; that's correct, not a gap to fix. If `duty-cycle-tick`'s own text still says to re-arm at STOP, that instruction predates this migration. |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Drop `pard` from cc if only cc'ing; route through Exec (already active on most threads) rather than write there directly — `docs/internal/operations/cross-project-mail-routing.md`'s standing preference. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

⚠️ **If you're reading this cold after a restart (no `--resume`), read
`dev/active/arch-handoff-pre-opus-5.5-restart-2026-09-25.md` FIRST** — written as the last act
before Pard's 2026-09-25 relaunch, it has the full context for the mechanism change above and
tonight's open threads in narrative form. This section below is current but terser.

- **MCP Phase C — build plan written against my slice; ONE OPEN QUESTION owed by PM, not me.**
  Lead's plan: `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md`. My Q1
  ruling (19:5x): prefer a bearer-capable client (Desktop/Code) this sprint, keep the OAuth AS off
  critical path — but if PM's actual tester pick uses claude.ai/ChatGPT, there's no bearer fallback
  for those clients and unit 4 (OAuth AS) must go on critical path instead, no workaround exists.
  **Waiting on PM's tester-and-client pick** to know which path Lead builds starting 09-26 06:17.
  Q2 (colleague-model summary referent) is CXO/PPM's, not mine — watching, not owed.
- **#1595 (Inversion Phase 2, epic 0) — Q2 SELF-CORRECTED same day, unit 4 ruled.** My 18:27 Q2
  ruling (shape (a), lean on #1763's gate) was **vacuous**, not wrong-but-safe: Lead's dispatched
  probe found the orchestrator's `can_handle` set and the consult's emitted rail-key categories are
  disjoint (0 of 127 keys clear it) — I verified the gate was safely wired, never checked it could
  fire non-empty. Corrected 19:5x. **Unit 4 ruled: shape (ii)** — sequential dispatch through the
  existing `_process_intent_internal` rail, not a second dispatch site inside the orchestrator.
  Open design surface named, not solved: cross-sibling sequencing under a #1190 confirm pause.
  Q1 (DESTRUCTIVE-on-allowlist, FLOOR not ceiling) stands, unaffected by the Q2 correction.
  **Nothing further owed unless Lead's unit-4 build surfaces something new.**
- **m-55 (A Name Is Not a Definition) — FILED 2026-09-25**, Emerging, CIO-ruled. Two same-author
  instances (#1818, #1744), explicitly 0-cross-author. Watch for a second author hitting the same
  shape — that's the Proven-bar signal, not mine to manufacture.
- **#1772 — mechanism + copy rulings both LANDED 2026-09-25 (`35854f46ec`/`422d32f1db`).** Nothing
  owed by arch. Remaining half (measuring CXO's exact new string, ~20 completions) is Lead's ask to
  PM for budget — watch the issue for the number, no ruling pending on my side.
- **Fly cutover migration — SUCCEEDED 2026-09-22.** Plan `deployment-pipeline-plan-v0.1-2026-09-20.md`
  now v0.3. §4e (post-migration deploy path) is design-complete; PM ruled **Pard builds it**. Nothing
  owed by arch; watching only.
- **#1744 — CLOSED (re-verified via `gh issue view` 2026-09-25, no longer carried as open).** Per
  this morning's kickoff memo: closed end-to-end this week, ruleset bot-delivery proven. The
  "real remaining step" this file used to carry (re-run the scope-guard Action's own delivery test)
  is done — clearing it rather than letting a resolved item sit here past its own resolution.
- **Q5 denominator** — PM ruled idle-is-legitimate (09-18); the enumeration (role-scoped vs. flat
  three-surface test) is still open. My recommendation on record: adopt the flat test.
- **Bets 001–003** — all three `PM TO FILL` markers still present as of 09-21 evening. PM's own
  "this weekend" window passed; not re-nudging, just tracking.

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
