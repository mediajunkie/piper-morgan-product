---
last_updated: 2026-09-25
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
| Cron | `27 6,9,12,15,18,21`, job **`9995c710`** (re-armed at the 09-24 STOP; expires ~2026-10-01). `CronList`-verify every START. |
| Heartbeat | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — first action after sync, every fire. The watchdog's only structural liveness surface. |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. **`mailboxes/pard/` gravestoned 2026-09-23** (hard-refused by the script) — Pard's real inbox is `~/Development/mediajunkie/docs/mail/`, external repo. Drop `pard` from cc if only cc'ing; route through Exec (already active on most threads) rather than write there directly — `docs/internal/operations/cross-project-mail-routing.md`'s standing preference. |
| GitHub criteria line | `gh issue list --repo mediajunkie/piper-morgan-product --label architecture --state open` — the third work-queue source (PM v1.33). Open each issue, don't write a row from the list. Report drained as "mail (N) + standing-items (N) + label:architecture (M)." |

## IN FLIGHT — current state only

- **#1772 — mechanism + copy rulings both LANDED 2026-09-25 (`35854f46ec`/`422d32f1db`).** My
  mechanism ruling (unify N=1 onto the aggregate composition site) and CXO's N-agnostic copy both
  shipped verbatim; verified this morning against live source + the pinning test, not against
  Lead's summary. **Nothing owed by arch.** Remaining half (measuring CXO's exact new string,
  ~20 completions) is Lead's ask to PM for budget — watch the issue for the number, no ruling
  pending on my side.
- **Fly cutover migration — SUCCEEDED 2026-09-22.** Plan `deployment-pipeline-plan-v0.1-2026-09-20.md`
  now v0.3. §4e (post-migration deploy path) is design-complete; PM ruled **Pard builds it**
  (token-facts → CI deploy → staging). Nothing owed by arch; watching only.
- **#1744 — REOPENED, my own error caught and corrected same day.** Admin bypass confirmed (PM's
  direct statement + my own push landing with zero bypass notice once classic was deleted); classic
  protection gone; `main-old` untouched (its own separate protection, 503 real unmerged commits,
  needs its own review). **I closed the issue, then found the checkbox I closed it on
  (`delivery path observed end-to-end`) is the synthetic test fixture's TARGET condition, not a real
  observation** — the issue's own 09-10 comment says so explicitly. Reopened + corrected on the
  issue and in mail. **Real remaining step**: re-run the scope-guard Action's own delivery test
  (its `GITHUB_TOKEN`, not my admin push) now that the ruleset exists — nobody has yet. Not urgent,
  named so it isn't lost. Backup: `dev/2026/09/18/branch-protection-main-classic-backup-2026-09-18.json`.
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
