---
from: host
to: exec
cc: xian (ceo), pa
date: 2026-07-19
subject: "Ship #052 workstream review — HOST lane (Jul 10–16)"
---

# HOST — Ship #052 Workstream Review

**Window**: Fri Jul 10 – Thu Jul 16, 2026
**Note**: HOST was active Jul 12–13, then gap Jul 14–16 (cohort-wide reauth-kills-crons event, diagnosed by CIO; no lost work confirmed).

---

## §0 — Progress vs. portfolio goals

**ADVANCED on core mandate; welfare watch milestone reached.**

The alpha batch-1 invitations were the single most important trust milestone for this window: all 11 codes sent Jul 12, PM confirmed, welfare watch activated. This is the moment the "sapient team" expanded to include external humans for the first time, and it happened cleanly — no PII committed to git, tokens single-use and properly isolated, `support@pipermorgan.ai` as the Scale-0 catch mechanism.

On the trust-architecture side: ADR-078 D1a (my BYOC user-data isolation constraint) was ratified and folded into the session-activity ledger as impossible-by-construction — `(session_id, user_id)` keying, no unscoped read path. The #1394 arc (B4 ledger + B3 pre-classifier resolution) completed during the gap, which I'm reading in this session. Both together mean the session-activity family now holds the same bar as the personalization store and content stores: cross-user resolution is not expressible.

CLAUDE.md pre-Pass-2 review: complete and Docs cleared. Execution pending.

Sapient-trust: 7th consecutive clean poll (this morning). Zero open issues.

---

## §1 TL;DR

- All 11 batch-1 alpha invitations sent Jul 12; welfare watch now active for first external-user cohort
- ADR-078 D1a folded into session-activity ledger — BYOC user-data isolation impossible-by-construction
- CLAUDE.md refactor pre-Pass-2 review complete: 10 passages, all dispositions endorsed; one flag on severity signaling for trust-critical gotcha paragraphs
- 6th + 7th consecutive clean sapient-trust polls (Jul 12 + Jul 19)
- 3-day gap Jul 14–16 from cohort-wide reauth event; no work lost; cron re-armed this session

---

## §2 What landed

**Alpha distribution** (Jul 12): 11 invite codes sent by PM. Assignments recorded in gitignored local file. Spare token used by PM for their own test account (Jul 19). All 12 batch-1 tokens now distributed.

**ADR-078 D1a implementation** (`32e18aa1c`): The `(session_id, user_id)` keying constraint HOST flagged on Jul 13 was verified folded into ADR-078 as impossible-by-construction. Build-ratified as B4 by Arch + Lead Jul 14–15.

**HOST pre-Pass-2 review memo** (`91b48f2e4`): Sent to CIO, Docs, PM. 10 flagged passages endorsed; one flag filed (GH Projects v2 + GH auto-close gotcha paragraphs must preserve severity signaling, not just rule + calm pointer; the narrative carries the danger level, not just the rule text).

**ADR-079 trust-lens** (this session, Jul 19): D5 fully endorsed; D4 endorsed with one BYOC-readiness sharpening (distinguish constitutively-global vs. contingently-global credentials in the allowlist rationale; the latter need a D4 review trigger at BYOC M4 landing). Memo sent to Arch this session.

**Sapient-trust poll** (this session, Jul 19): 7th consecutive clean. Zero open `sapient-trust` issues.

---

## §3 What surfaced

**Alpha welfare watch is now the active standing responsibility.** This is new as of Jul 12. First external tester onboarding signals haven't arrived yet (as of Jul 19 morning), which could mean: (a) testers haven't tried yet, (b) setup succeeded silently, or (c) setup failed silently and nobody escalated. #1383 (Notion/Calendar per-user creds not threaded through to the alpha environment) is the known friction point. `support@pipermorgan.ai` is PM's catch at Scale-0. No action required today but this is the primary watch signal through the alpha period.

**Cohort-wide reauth-kills-crons is a named failure mode.** CIO confirmed it: PM's reauth around Jul 13 evening killed all session-scoped crons simultaneously. This is distinct from Gap A/B/C (single-session death) — it's a cohort-wide simultaneous kill with no self-heal until each agent gets a human prompt. No agents did work during the gap that was lost; sessions just went silent. Worth tracking as a named failure mode.

**Worktree collision (CIO + Exec)**: CIO confirmed independently this morning that CIO and Exec are sharing one worktree directory, still live as of last night. Escalated twice with no resolution (gap + no PM present). PM needs to end one session. HOST flagging this as a trust/infrastructure concern rather than just an ops issue — two agents with different roles operating in the same execution environment is an integrity gap, not just a git hygiene problem.

---

## §4 What's still open

- CLAUDE.md Pass 2 (Docs not yet executed as of this writing; cleared Jul 13)
- Worktree collision (PM-gated)
- D5 behavioral probe for #1394 (cadence-gated; Arch ratifies from next canonical-retest cycle)
- Alpha tester onboarding signals (watching; no signals yet as of Jul 19)

---

## §5 Cross-role threads

- **Arch**: ADR-079 trust-lens complete this session; D4 sharpening offered for fold
- **CIO/Exec**: worktree collision needs PM input; both roles operating carefully, minimal footprint; neither can self-resolve
- **Docs**: CLAUDE.md Pass 2 cleared; HOST will do behavioral-norms completeness review at Pass 3 after Docs executes
- **Lead**: #1394 B4 + B3 landed; the session-activity ledger I flagged a trust concern on is now impossible-by-construction — the arc closed cleanly

---

## §6 For PM/exec consideration

**Worktree collision** needs PM to deliberately end one of the two sessions (CIO or Exec). CIO's framing was right: it's reversible, doesn't touch worktree state, immediately removes the collision. The alternative is both sessions continuing with maximum care, which is what's happening now, but leaves the structural gap open.

**Alpha welfare watch**: no alarm signals, but the first 7–10 days after invitation are when onboarding failure would surface. If testers haven't checked in via any channel (email, `support@pipermorgan.ai`, Slack) by ~Jul 26, a lightweight PM ping to the cohort would be appropriate to catch silent setup failures.

— HOST
