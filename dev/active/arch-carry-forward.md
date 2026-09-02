---
last_updated: 2026-08-30
currency_claim: rewritten at substantive-change boundaries, verified at every START
max_age_days: 4
---

# Architect Carry-Forward — Resumption Substrate

**Purpose**: durable handoff for the next Architect session. *(Frontmatter adopted 2026-08-29 per
CXO's tracked-state staleness design — the prose date-claim class this file belonged to was
measured 1-of-4 actively wrong the day the design shipped.)*

**REWRITTEN 2026-08-29 evening** — the Architectural Review 2026 (PM+Arch co-led, kicked off and
substantially executed in ONE day) supersedes most of what this file used to track. Prior version
in git history.

---

## Environment (stable; verify at START, don't re-derive)

| Fact | Value |
|---|---|
| Host / model | **Amber**, Model A stable worktree `~/Development/piper-morgan-worktrees/arch`, branch `claude/arch-cycle` |
| Cron | **`27 6,9,12,15,18,21`**, job **`db21eabf`** (re-armed 09-01 STOP; session-only; empty `CronList` → re-arm). Registry row current. |
| **Heartbeat — EVERY fire, first action after sync** | `bash scripts/duty-cycle-heartbeat.sh arch <START\|WORK\|STOP>` — the watchdog's ONLY structural liveness surface. ⚠️ **This practice was LOST at the 08-25 compaction and nobody noticed for 7 days** (work commits kept arch human-visible while the belt read dark; caught 09-01 by Exec via PM). **If you are reading this post-compaction: emit one NOW, before anything else.** |
| Mail | `mail-send.sh` push-to-ref; never touch PM's main checkout. Inbox verified at trunk (`git ls-tree origin/main`), never local `ls`. |
| ADR/patterns paths | **MOVED 08-29** (Docs' fold): now `docs/internal/architecture/adrs/` and `.../patterns/` — no `current/` segment. |

## THE active thread: Architectural Review 2026 → Reorientation Plan v1.0

**Everything routes through `docs/internal/architecture/reviews/2026-08-architectural-review/reorientation-plan.md`** —
four workstreams (A socialize · B docs reform · C code reorientation · D governance), owners,
dates, done-conditions. Read it at START; do not reconstruct from memory. Key state as of this
rewrite:

- **A**: broadcast sent to all 10 roles 08-29. **CXO+PPM trifecta ESSENCE pass due Wed 09-02;
  Arch synthesizes responses to PM by 09-03.** HOST's trust-lens already in (consent-invariance
  flag — answered with the verification decomposition; ESSENCE annotated; the pending behavioral
  receipt rides Lead's watched round). CIO ack'd 09-01 disposition start.
- **B**: living-core-doc-set draft due from me **09-01**; corpus disposition (ADRs +
  methodology-core + patterns) kicks off **09-01** with CIO + Docs; citation census filed with
  reproducible artifacts; Leg D's 24 unanswerable questions = doc-gap backlog.
- **C**: staged flip with Lead, sequenced into PM's watched round (correction on the record:
  flip-1 live for `read_status` since 08-21 via fly secrets, unexercised). **Legacy-classifier
  retirement criterion encoded, check date 2026-09-30.** Disposal routing (spatial 11 + census
  dead families, with explicit live-spatial keep-list) in Lead's inbox. #1690 (demo plugin) filed.
- **D**: scope-bet gate RATIFIED; register at `docs/internal/architecture/bets/`; **Bets 001–003
  await PM's buyer/appetite fields and are EXPLICITLY NON-BLOCKING.** "Verified how" required
  field shipped (CLAUDE.md + close-issue-properly).

**ESSENCE.md** (`docs/internal/architecture/ESSENCE.md`) v0.1: PM called it "excellent," polish
applied (genericized for possible publication; routing rule self-explanatory), consent-invariance
line carries a verification-status footnote. Ratification = PM + trifecta input, after 09-02.

**PM's standing posture ask, reaffirmed 08-29**: *assert the POV, don't just ratify* — and
operating plans live in documents, not in my head (PM pressed exactly this at 16:46 and was right).

## Standing hard rules (unchanged, load-bearing)

1. 🔴 **Never glob the inbox** — read-then-append-to-move-list in the same call; verify drains at
   trunk. (08-08/09 trust incident.)
2. 🔴 **State the scope IN the ruling** — name the object, name a non-covered adjacent thing,
   name the clauses. (Earned 3× in one fortnight.)
3. **Verify the claim before ratifying** — the discipline that caught #1677's false framing,
   #1633/#1638's dead code, the flip-1 config-vs-deployment layer error (both directions), and
   ESSENCE's own consent line (HOST's flag, honored not defended).
4. **A denominator that doesn't travel with its number isn't a denominator** (new 08-29, from the
   flip-1 correction: the census named its layer; I dropped the caveat when the claim traveled).

## Standing guard

**ADR-078 D4: the classifier stays stateless** — now also an ESSENCE standing rule. Watch #1673's
audit when it starts.

## Dormant / background threads (all quiet, none owed)

#1481 Slack principal (Fast Follow) · #1459 original_message ratchet (build, Lead's) · #1462
PDR-006 epic (fail-closed identity risk lives there) · #973 MEM-CACHE (Production, needs Lead
bandwidth) · ADR-068 prep (gated on PPM naming a live sprint) · m-40/m-30 proven-bar watches.
