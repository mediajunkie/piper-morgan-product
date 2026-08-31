# Lead carry-forward — rewritten 2026-08-29 ~18:15 PT (freshness rule: full pass at START/STOP)

## Live state (receipts, not recall)
- **v66 LIVE** (deployed Sat 8/29 ~18:05 PT on PM's word; v65 number consumed by the flip secrets
  update). Carries the whole Saturday pile: 1527 narrowing · 1693 extraction · 1572 timezone
  (captures at PM's next LOGIN) · 1543/1649 slot rework · extraction-pattern ratchet.
- **FLIP IS ON since ~1 PM 8/29**: PIPER_INVERSION_LIVE_CATEGORIES=read_status,read_referent,
  read_synthesis,create_todo + PIPER_INVERSION_SHADOW=1 (verified in running env). Rollback=unset.
  PM's round: ZERO misroutes under the flip (the 1488 class absent).
- **Cron 449e67f0** `17 6,9,12,15,18,21 * * *` (armed 8/31; expires ~9/7; rotate ~9/5).
- Model: Fable 5 (restored 8/28 08:36).

## The one PM-gated moment
- **"Flip it"** — PM's named trigger, now executing ARCH'S RATIFIED STAGED PLAN in one watched
  round: at "flip it" → SHADOW=sampled + four READ flip_groups (one secrets update); mid-round at
  the todo cluster → create_todo (Stage 2, first live write, watched). Rollback = unset.
  Verified 8/29: prod env DOES carry read_status (fly secrets; config-file census could not see it). Then IF clean: close
  #1677 + #1488 with PM's transcript, description-first (1677 reopened 8/29 after PPM's
  mail-commit subject auto-closed it — keyword gotcha, not a decision).
- Round sequencing in the tracker artifact: security (1578/1581/1501) → flip + todo/reminder → rest.

## Queue (PM pre-authorized; one lane at a time in this worktree)
- RUNNING: named-target delete resolution lane (the 1527 lane's scope note; PM's live pain).
- NEXT: Web's test credential (real signup path — unblocks 1512/1568/1578/1581 browser closes) ·
  1677/1488 close-out on PM's transcript · #1689 native dialogs · #1659/#1660 file residues ·
  #1653/#1652 consent keeps · pre-claim shadow probe (measurement for the narrowing schedule) ·
  #1522 fresh-scan-then-delegate · config-validator stub disposal.
- Rate-limited, retry next fire: file the named-target delete gap issue (lane building it anyway).

## Recently resolved (for context, not action)
- Triage cut: ruled by PM one-at-a-time 8/28, board-executed by PPM (5 moved), #1638 DISPOSED
  8/29 under delete-module-safely. Sitting fully closed.
- CI belt honest as of 8/28: Arch Enforcement + Docker + Router + Config Validation green;
  mypy gate fix-forward (no ceilings raised).
- #1386: criteria 2 (signed off 8/21), 4 (belt fixed), 5 (attested on deployed machine) — gate
  nearly assembled; PM verdicts on the round are the remaining input.

## Standing
- Supersession gate; push-after-reading (batteries ≠ push chain); merge-BEFORE-inbox-ls at every
  fire; verify awaited items against the ISSUE not this file; deletion = fresh sweep, never recall.
- **This file gets a freshness pass at every START and a rewrite at every STOP** (Exec/PM ask,
  8/29 — the 8/19 staleness is the incident that earned the rule).
