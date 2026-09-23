---
last_updated: 2026-09-22
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
| Model | Sonnet 5 — intended per PM's 2026-09-21 ruling (fleet-wide, Opus is most token-expensive; Lead is the one exception, on Fable) |
| Cron | `27 6,9,12,15,18,21`, job **`3cc1dc3d`** (re-armed at the 09-21 STOP; expires ~2026-09-28). `CronList`-verify every START. |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Drop `pard` from cc if only cc'ing; route through Exec (already active on most threads) rather than write there directly — `docs/internal/operations/cross-project-mail-routing.md`'s standing preference. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

- **Fly cutover migration — SUCCEEDED 2026-09-22.** Plan `deployment-pipeline-plan-v0.1-2026-09-20.md`
  now v0.3. §4e (post-migration deploy path) is design-complete; PM ruled **Pard builds it**
  (token-facts → CI deploy → staging). Nothing owed by arch; watching only.
- **#1744** — ruleset created by PM (`"main - bot delivery"`, `deletion`+`non_fast_forward`,
  bypass `RepositoryRole` id 5). Classic protection still active alongside it (correct order —
  don't delete classic yet). **One unverified fact, PM asked 09-23**: does role id 5 = admin? If
  not, deleting classic later would break all 12 agent pushes. Not urgent — classic is doing the
  real work today regardless. Backup: `dev/2026/09/18/branch-protection-main-classic-backup-2026-09-18.json`.
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

## Standing guard

ADR-078 D4: the classifier stays stateless — also an ESSENCE standing rule.

## Dormant / background (watch only, none owed)

#1481 Slack principal · #1459 original_message ratchet (Lead's build) · #1462 PDR-006 · #973
MEM-CACHE · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.
