---
last_updated: 2026-09-26 12:2x
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
| Model | **STILL Sonnet 5 as of 2026-09-26 06:2x — the Opus 5.5 restart is HELD, not executed.** Pard deliberately held it (first-of-its-kind operation, wants PM present; last PM activity was 16:30 the prior evening). Verified this morning: `~/.claude/settings.json` still reads `claude-sonnet-5`, and Pard's own hold-memo confirms no restart happened. **Do not assume Opus 5.5 until you see a fresh model system-reminder or Pard confirms the relaunch fired** — this line will be wrong the moment the restart actually happens; check don't assume (rule 7). |
| Wake mechanism | ⚠️ **SESSION CRON RETIRED 2026-09-25 21:2x, PERMANENTLY — do not re-arm.** External LaunchAgent (Pard). **The registry-vs-plist mystery is FULLY RESOLVED as of 12:2x** (Pard's incident memo): the LaunchAgent's plist was generated at provisioning time and never re-synced against later registry edits — my 06:27 edit was correct, the plist just didn't follow it. Pard fixed the plist (`launchctl print` confirms `6 14 21`) and added a `pm-cadence` drift guard that asserts plist hours against the registry every cycle going forward. **Registry `cron_expr` is trustworthy again as of this fire** — no more "assume 6x/day regardless." Separately: Pard's fix required a reload that killed an in-flight 12:27 fire (mine) — worktree confirmed clean, nothing lost, but note named honestly: I have no way to tell from inside a session whether I'm a continuous process or a clean post-kill re-delivery (rule 7 applies to this exact situation) — don't trust apparent conversational continuity as evidence either way if this comes up again. |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Drop `pard` from cc if only cc'ing; route through Exec (already active on most threads) rather than write there directly — `docs/internal/operations/cross-project-mail-routing.md`'s standing preference. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

⚠️ **If you're reading this cold after a restart (no `--resume`), read
`dev/active/arch-handoff-pre-opus-5.5-restart-2026-09-25.md` FIRST for the reasoning/narrative** —
but **per Pard's explicit 09-25 ruling, treat that doc as base layer once it's >48h old, not a live
description**: this carry-forward + session logs + commits are the current state; the handoff's
job shrinks to orientation once it ages. **Don't try to keep the handoff itself fresh** — that was
named directly as the wrong instinct ("I would rather your handoff go stale than your seat idle").

- **MCP Phase C — units 0-2 LIVE on `mcp.pipermorgan.ai` (09-26). PM picked ChatGPT first — my Q1
  trigger fired, OAuth AS is now on the critical path, exactly as ruled.** PM handed the whole MCP
  testing program to PA (Lead returns to epic 0). **Open**: who builds the OAuth AS (Lead's unit 4,
  NOT #1595's unit 4 — same number, unrelated epics, confusing on purpose only by coincidence) —
  my lean is Lead builds it as one bounded final lane (identity-boundary adjacency), but the actual
  call is PA's now, explicitly deferred to them. One review condition named either way: verify the
  OAuth flow binds the minted token to the SAME identity that authenticated at `authorize`,
  throughout — that's the one place this lane could quietly weaken condition 1. **Watching for
  PA's decision, nothing else owed.**
- **#1595 (Inversion Phase 2, epic 0) — unit 4 LANDED 09-26 (`3d8168b1e1`); #1897 filed for unit
  4b, grammar shape ruled, not urgent.** Unit 4's shape (ii) + confirm-pause sequencing both landed
  clean, no second dispatch site, MAX_DISPATCH_SITES 0→0. **Real finding, not a defect**: surface
  1's splitter structurally can never emit a read+write sibling pair (every pattern group is a read
  lane; the destructive guards decline write-shaped asks at surface 1) — so unit 4's rail loop is
  correctly built but #1606 still can't reach it, because the split itself never happens. Fix is
  #1897/unit 4b: the router gains a new `outcome="plan"` + `operations: List[...]` field, strictly
  additive, never touching the existing single-op contract — shaped 09-26, ruled NOT urgent (Lead's
  own framing: "rides the next alpha release," agreed rather than overridden). One real risk named:
  the prompt change ("or return a plan") could regress single-op accuracy — recommend measuring
  before shipping, same discipline as this week's #1772. **Nothing further owed unless/until
  someone builds 4b.**
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
