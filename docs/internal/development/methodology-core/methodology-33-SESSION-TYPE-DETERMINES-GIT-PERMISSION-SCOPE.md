# Session-Type Determines Git-Permission Scope

## Overview

**Session-Type Determines Git-Permission Scope** names the discipline of treating session-type (local Code, cloud Code, Routines, sub-agent, etc.) as the load-bearing variable for git-permission and commit-identity expectations. Same agent role, same prompt, same repo — different session-types produce different commit identities and different push permissions. The discipline:

1. **Session-type, not agent-role, determines commit identity**. CIO running in a local Code session commits as `mediajunkie` (PM's GitHub identity). CIO running in a cloud Code session commits as `Claude` (proxy identity). Same role; different identity per session-type.
2. **Push permissions follow commit identity**, not session-type directly. `mediajunkie` has main-push permission. `Claude` may or may not — depends on the repo's permission grant for the proxy identity.
3. **Before relying on push-to-main behavior, identify the session-type and confirm the commit-identity's permission scope**. Don't assume local-Code-style permission in cloud sessions, or vice versa.
4. **Where the session-type lacks main-push permission, the discipline is to write to a branch and let an entity with main-push permission do the fold** (typically: merge-keeper sweep, or the local-Code conversational session at sign-off).

The discipline matters because session-vehicle continuity work (handoffs across session types), cohort extension (other agents adopting autonomous cycles), and Routines-style true-cloud-autonomous operation all involve session-type transitions where permission scope changes silently if not surfaced.

## Why This Methodology

### The Vehicle 2 attempt #1 cloud-session failure (2026-05-17)

CIO's Vehicle 2 transition (the session-vehicle retirement of the local Code instance after ~24 days of continuity) attempted first via a cloud Code session. The handoff doc shape, the role identity, the mailbox triage — all proceeded normally. The push to main failed:

```
remote: Permission denied to Claude for mediajunkie/piper-morgan-product
```

The cloud Code session's commits were authored as `Claude` (proxy identity), not `mediajunkie`. Repo permissions grant main-push to `mediajunkie` only. The cloud session was structurally unable to fold its work to main regardless of how correct its discipline was at every other layer.

PM abandoned the cloud-Vehicle-2 attempt in favor of a fresh local Code Vehicle 2 (the current session). The handoff was captured cleanly via the existing handoff-doc + inbox-pointer pattern; nothing was lost. But the diagnostic finding is structural: session-type determines whether a session can fold to main, regardless of the agent's content or discipline.

### Why this is a methodology-corpus entry rather than a per-incident fix

The failure mode generalizes well beyond the Vehicle 2 incident:

- **Routines-based autonomous loops** (the V2-future path for V1 Duty Cycle) run in cloud sessions per fire. Each fire commits under the proxy identity. Routines fires writing to main would hit the same permission wall.
- **Sub-agents spawned via Task tool** may run under varying identities depending on harness configuration. Confirming their commit identity before letting them commit to main is a real precaution.
- **Cross-agent cohort extension** under cloud session-types compounds the same issue: extending V1 to HOST or Docs via Routines means each of those agents' cycles writes to main as `Claude`, not as the role's expected identity.
- **Future session-vehicle handoffs** between local and cloud instances need the discipline to anticipate which folds work and which need branch-write + merge-keeper.

The discipline is named once and applies wherever the session-type changes — which is increasingly often as the platform evolves.

## The discipline applied

For any session-vehicle transition OR any autonomous-loop design that involves a new session-type:

1. **Identify the session-type** of the writer (local Code / cloud Code / Routines / sub-agent / etc.).
2. **Identify the commit-identity** the session-type produces (PM identity / proxy identity / agent-specific identity / etc.).
3. **Verify the commit-identity's main-push permission** against the repo's permission grants. A 30-second `git config` + GitHub permission check.
4. **Choose the appropriate write pattern**:
   - If main-push works: standard mailbox-discipline applies; commit + push to main directly.
   - If main-push fails: write to a `claude/*` branch; rely on merge-keeper sweep OR a separate local-Code conversational fold to main.
5. **Document the chosen pattern in the session-vehicle's handoff** so subsequent vehicles inherit the operational design without rediscovering the constraint.

For autonomous-loop design (Phase 5 V3 architecture's siblings), this discipline composes with **methodology-31 (Append-Only Autonomous-Cycle Architecture)** — both treat session-type as load-bearing for the loop's correctness. Append-only architecture solves shared-`.git/` race conditions; this entry solves cross-session-type permission constraints.

## When to apply this framing

### Apply this framing when

- Designing a session-vehicle handoff that may transition across session-types (local → cloud, cloud → local, conversational → Routines).
- Authoring autonomous-loop work whose execution session-type isn't fully determined yet (e.g., "V1 in local Code, V2 in Routines").
- Extending an autonomous loop to a new agent role under a session-type that hasn't been validated for that agent's permission needs.
- Investigating a push-permission failure: session-type is the first variable to inspect, before checking branch names, hook configurations, or repo permissions.

### This framing does not apply when

- The session-type is fixed and validated (e.g., local Code conversational sessions for established roles).
- The work is read-only (no commits; permission scope doesn't matter).
- The commit-identity is configurable and a known-working identity is already in use.

## What it predicts

If session-type-determines-git-permission is applied correctly, the following downstream signals should appear:

- **Push-permission failures in session transitions get diagnosed within minutes** — the discipline names the variable to inspect first.
- **Routines pivot for V1 Duty Cycle (V2-future path) is designed correctly from day one** — branch-write + merge-keeper rather than direct-to-main.
- **Cohort cycle extension under cloud session-types adopts branch-write pattern automatically** — agents extending V1 don't rediscover the constraint by hitting the permission wall.
- **Sub-agent commit decisions become explicit** — parent agent verifies the sub-agent's commit identity before authorizing main-push behavior.
- **Session-vehicle handoff docs include session-type + commit-identity confirmation** as standard sections — anticipates the constraint rather than reacting to its failure.

## Mitigation patterns for cloud / proxy-identity sessions

When the session-type's commit-identity lacks main-push permission, two well-known mitigation patterns:

### Pattern A: Branch-write + merge-keeper sweep

Cloud session commits to a `claude/*` branch (which the proxy identity CAN push to). A separate local-Code session OR an automated merge-keeper sweep (Docs's daily sweep, etc.) folds the branch to main.

- **Cost**: latency between cloud-session work and main-visibility (~24 hours worst case via daily sweep)
- **Benefit**: cloud sessions can operate fully autonomously without main-push permission

### Pattern B: Permission upgrade for the proxy identity

PM grants main-push permission to the proxy identity (e.g., adding `Claude` to the repo's collaborators or to a permission group).

- **Cost**: opens main-push to anything running under proxy identity (cohort-wide implication)
- **Benefit**: cloud sessions push directly; no latency or merge-keeper dependency

The current Piper Morgan posture is Pattern A by default. Pattern B is available if PM decides the cohort-wide trust property holds. CIO recommendation absent specific need: stay with Pattern A; revisit if Routines-pivot creates enough Pattern-A overhead to warrant Pattern B.

## Cross-references

- **CIO Vehicle 2 attempt #1 failure** (originating incident): PM's verbal report 2026-05-17 during the local-Vehicle-2 fresh-start; captured in Vehicle 2 resume entry of the May 17 CIO session log and in standing-items tracker entry 12bb.
- **methodology-31 (Append-Only Autonomous-Cycle Architecture)**: composes with this discipline; both treat session-type as load-bearing for autonomous-loop correctness.
- **V1 Duty Cycle design v0.4**: the V2-future-path note ("Routines pivot when continuity-feel no longer load-bearing") is the place this discipline informs the most.
- **Branch / Worktree / Mailbox Discipline canonical doc**: `docs/internal/operations/branch-worktree-mailbox-discipline.md` — companion operational doc; this methodology entry layers session-type-awareness on top of the existing worktree-default discipline.
- **CIO Phase 5 V3 redesign memo** (May 17): the broader Vehicle 2 transition context that includes the cloud-attempt-failure.

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. The discipline is general; specific permission-scope behaviors will evolve as the platform evolves (e.g., if Anthropic ships per-cloud-session-identity granularity, the mitigation patterns may shift).

Slot 33 per pre-filing slot-availability check (methodology-28); filed alongside methodology-30 / methodology-31 / methodology-32 in the May 18 batch.

The promotion-to-Proven criterion is: one or more confirmed cohort applications of the discipline (e.g., a Routines-pivot design that pre-applies branch-write+merge-keeper, or a sub-agent commit-identity verification step that prevents a permission-failure). methodology-29 (Pattern Formation via Successful Imitation) framework: bottom-up adoption signals readiness.

---

*Filed: 2026-05-18 by CIO Vehicle 2. Pattern category: methodology-corpus operational discipline for session-type/commit-identity awareness. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-33 (pre-filing slot-availability check applied per methodology-28; filed alongside methodology-30, -31, -32 as the May 18 batch).*
