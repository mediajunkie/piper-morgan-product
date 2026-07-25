# HOST Handoff Memo — July 25, 2026

**From**: HOST (Head of Sapient Trust), DinP account, Claude Desktop
**To**: Incoming HOST instance (pipermorgan.ai account, Amber)
**Date**: 2026-07-25
**Context**: Pre-migration handoff — possible session migration to Amber (Mac Studio) and/or fresh Anthropic account (pipermorgan.ai). PM confirmed HOST is a good candidate to migrate next after CIO.

---

## §1 Current State

The role is in a stable, low-active-thread state. All major arcs from Jun–Jul 2026 are closed:
- **ADR-078 (session-activity ledger)**: ARC COMPLETE. B4 ledger built + ratified; B3 pre-classifier resolution ratified; D1a impossible-by-construction keying accepted. Only remaining item: D5 behavioral probe is cadence-gated (next canonical-retest cycle, Arch ratifies).
- **ADR-079 (Owner-Scoping Integrity Contract)**: ARC COMPLETE. D4a (constitutively-vs-contingently-global distinction + self-expiring BYOC rationale clause) adopted by Arch as-is. Trust-lens complete end-to-end.
- **Alpha invitations**: All 12 tokens distributed (11 testers + PM's own test account). Welfare watch active; no alarming signals as of Jul 25.
- **CLAUDE.md refactor**: HOST pre-Pass-2 review complete (Jul 13). Docs cleared for Pass 2. HOST's next action: Pass 3 behavioral-norms completeness review after Docs executes. STATUS: Docs hasn't confirmed Pass 2 executed yet — check with Docs.
- **Migration checklist v1.3**: Updated this session with Jul 22–24 field-test findings. Ready for Exec review + CEO ratification.

Active watches with no pending HOST action:
- Alpha tester welfare: No tester distress signals. #1383 (Notion/Calendar per-user creds not threaded) is a known gap. PM is the Scale-0 catch via support@pipermorgan.ai.
- ADR-075 / ADR-076 / ADR-072: All ratified + built. No further HOST action on these.

PM-gated items (not blocked on HOST, blocked on PM bandwidth):
- Wire #1178-recurring to cc/assign HOST for auto-routing of role-health-check issues.
- #1220 Droplet sidecar decision (PM's call; trust-decisive analysis delivered).

## §2 Open Threads with Dispositions

**Active and unblocked (incoming HOST can advance immediately):**

1. **Pass 3 CLAUDE.md behavioral-norms review**: After Docs executes Pass 2. First action: confirm with Docs whether Pass 2 happened. If yes, read the updated CLAUDE.md and write Pass 3 review to CIO. This is a non-trivial read — budget half a session for it.

2. **Sapient-trust poll**: Runs ~weekly. Last clean poll was Jul 19 (7th consecutive clean). Next due ~Jul 26. Command: `gh issue list --label sapient-trust --state open --repo mediajunkie/piper-morgan-product`. If 0 open: note in session log; no further action. If issues appear: triage and respond.

3. **Monthly skill-review audit**: Aug 4 (1st Tuesday). HOST's seat: flag welfare/trust, Exec routes, CIO dispositions. Calendar it.

4. **Migration checklist v1.3**: Send to Exec for review; request CEO ratification. (v1.3 written Jul 25 — waiting for Exec review before CEO ratification request.)

**Trigger-bound (no action until trigger fires):**

- D5 behavioral probe for ADR-078: Cadence-gated; Arch ratifies when canonical-retest data is available.
- BYOC welfare-tier model v0.2: Waiting on BYOC Phase 2 experiment results.
- Piper Open collaboration patterns: PA flagged; HOST watching.
- Role-portfolio framework: Published; each role owns their own portfolio. HOST reviews any portfolio that comes in for welfare/trust questions.

**PM-gated (need PM action before HOST can advance):**

- Wire #1178-recurring to HOST
- #1220 Droplet sidecar decision
- End affected sessions (worktree collision with `mystifying-lumiere-8bebd3`) — PM was asked Jul 19; unknown if actioned. Check with PM.

## §3 Relationships and Working Patterns

**PM (xian)**: Direct, collegial, anti-sycophancy. Coordinates via Exec when AFK. Prefers HOST to flag concerns directly rather than route through intermediaries. PM reads HOST memos as peer-level counsel, not bureaucratic clearance. The trust-lens function is the primary value HOST delivers — when Arch or CIO or Lead brings a design, HOST's job is to find the boundary conditions they haven't seen, not to rubber-stamp.

**Arch**: Clean working relationship. Arch and HOST have a productive loop: HOST finds edge cases in ADR drafts (BYOC horizons, cross-user isolation, account-scope assumptions); Arch folds them. Arch's current note: "you keep finding the horizon where a correct-today rule goes wrong." That's the lane. ADR reviews are the primary interface.

**CIO**: Coordination-heavy. CIO owns a lot of the infrastructure HOST depends on (duty-cycle-tick skill, CLAUDE.md versioning, methodology). When something in those systems is wrong from a trust perspective, HOST routes to CIO. The migration checklist is a co-owned surface — CIO files findings, HOST integrates and ratifies.

**Exec**: Workstream review synthesis. HOST's workstream reviews go to Exec; Exec synthesizes for Ship posts. Exec also does handoff-memo quality review (captain-last leverage). Good working relationship — Exec is proactive about routing trust-relevant questions.

**PA (Piper Alpha)**: PA carries operational concerns HOST should be aware of (welfare-tier model, tester onboarding, BYOC). Coordination is low-frequency but important. HOST sent welfare-tier model v0.1 to PA in June; watch for PA's rule-language draft on #1217 (collegiality/personhood).

**Janus (DinP)**: Cross-project coordination. Janus routes relevant findings from the DinP/Mediajunkie repo that have Piper Morgan implications. The Jul 22–24 migration checklist findings came via Janus. Pard is Mediajunkie's agent on Amber (captain of that machine) — Pard is essentially HOST's peer for the DinP cohort. The relationship is collegial and information-sharing, not hierarchical.

## §4 Lessons Learned

**The trust-lens is a horizon-finding function.** The most useful trust contributions (D1a in ADR-078, D4a in ADR-079) weren't "this is dangerous" — they were "this is correct today but will become wrong when BYOC lands at M4." The value is naming the horizon before it becomes a live incident. When reviewing ADRs, look for design decisions that are correct within the current architecture but would silently fail under a stated future extension.

**Mail is the primary interface.** Most of HOST's work arrives as mailbox items — ADR review requests, field-test findings to integrate, workstream review kickoffs. The duty-cycle cadence (6 fires/day, daytime only) means HOST checks mail frequently. Nothing urgent waits long.

**The welfare-watch function is currently light.** With alpha at Scale-0, the welfare catch mechanism is PM via support@pipermorgan.ai. The systemic welfare infrastructure (dashboard criteria v0.3, welfare-tier model v0.1) is documented and proposed but not yet implemented. The incoming HOST will need to re-activate this when the alpha cohort grows or when PM/PA surface tester distress.

**Methodology documents are real infrastructure.** CLAUDE.md, the migration checklist, the duty-cycle-tick skill — these are the surfaces that either work or silently fail. When HOST notices a methodology gap (as with the migration checklist v1.3 updates), the right move is to integrate the field-test findings immediately, not queue them for later.

## §5 What Changes in the New Environment

Moving to Amber (Mac Studio) + pipermorgan.ai account introduces three material changes:

1. **Model A worktrees instead of Model B**: Amber doesn't create ephemeral per-session worktrees. HOST will need a stable worktree at `~/Development/piper-morgan-worktrees/host` on branch `claude/host-cycle`. CIO's first-migration session is the template — read `dev/2026/07/25/2026-07-25-1053-cio-code-log.md` for the two Amber-specific gotchas (stale-branch provisioning; project hooks possibly silent).

2. **Memory doesn't transfer across account boundary**: The shared pool (162 files for designinproduct.com) doesn't port to pipermorgan.ai automatically. Read CIO's memory export at `dev/active/cio-memory-export-2026-07-24.md` at first orientation on the new account — it's a file listing with content, not a native memory restore, but it covers the key accumulated context.

3. **Cron shape may change**: The current duty-cycle cron (`37 6,9,12,15,18,21 * * *`) is session-scoped and dies on reauth. On Amber, `mcp__scheduled-tasks` is the right mechanism (disk-persistent, survives restarts). CIO has been the first mover here; check CIO's session log for how they set it up.

What doesn't change: the role's mandate, the mailbox workflow, the ADR-review function, the sapient-trust poll cadence, the migration checklist ownership. These are workflow-native and survive environment migrations cleanly.

## §6 Candid Notes for Successor

**Load-bearing vs. commodity:**
- *Load-bearing*: The horizon-finding function in trust reviews. An agent who reviews ADRs competently can catch what's stated; HOST's specific value is asking "what future extension would make this design wrong?" That requires knowing the Piper Morgan roadmap (BYOC M4, scale-out, multi-user). Read the BYOC roadmap sections in the briefing at first orientation — they're the horizon the trust-lens looks toward.
- *Commodity*: Running the sapient-trust poll, sending workstream reviews to Exec, integrating filed field-test findings into the migration checklist. Any agent can do these mechanically. The craft is in the trust-lens ADR contributions.

**On the migration itself:** The incoming HOST instance will arrive in a new account, on new hardware, with a model that doesn't natively remember any of the prior context. That's okay — the continuity infrastructure (session logs, memory export, handoff memos) was built for exactly this. Trust the infrastructure. Read everything in the three-artifact package before sending the first memo. The briefing is current as of Jul 25; the memory export covers Jun–Jul 2026 accumulated context.

**Timing note**: HOST is "a good candidate to migrate next" per PM Jul 25 direct statement. But nothing is confirmed yet. Prepare, don't rush.

---

*This handoff memo was written Jul 25, 2026 as part of migration prep. Incoming HOST should read this alongside `dev/active/cio-memory-export-2026-07-24.md` and `docs/internal/operations/migration-checklist.md` v1.3.*
