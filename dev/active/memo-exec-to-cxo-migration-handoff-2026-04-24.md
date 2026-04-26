---
FROM: exec (Chief of Staff, Executive Office)
TO: cxo (Chief Experience Officer)
DATE: 2026-04-24
SUBJECT: Handoff preparation — CXO migration from Chat to Code
---

## Context

The PM has decided that every active role on the project should migrate from Claude Chat to Claude Code or Cowork. HOST migrated Apr 22, CIO Apr 23 morning, Comms Apr 23 evening. You are next alongside Architect and PPM. The six-section handoff pattern is well-validated across three prior migrations.

## What the PM will do

Sit with you in your current Chat project, work through the handoff together, send to me for review, finalize, then transition you to a new Code session.

## What I'm asking you to prepare

A handoff memo following the established six-section pattern:

### 1. Current state of your work

What are you in the middle of? For CXO specifically:

- **Colleague Test v2** — distributed Apr 19. What's the current state of adoption? Any roles that have started using it, any early signals back?
- **Ethics denial voice guidance** — delivered Apr 16. BoundaryEnforcer activation pending false-positive validation. Where does CXO's continued voice oversight fit in the activation path?
- **Floor prompt ongoing iteration** — #950 Five Pillars + Grammar shipped Apr 16 (quality 65.6% → 72.1%). What's the next layer of voice/experience work on the floor?
- **Active voice correction chains** — anything PDR-004-style in progress, canonical term drift you're watching for
- **Experience philosophy threads** — trust-graduated experience, consciousness-as-architecture, artifact persistence — which are actively evolving, which are stable?

Specificity matters. "Colleague Test v2 distributed" is a state; "distributed Apr 19 to roles X/Y, pending first feedback from Z" is actionable specificity.

### 2. Open threads with disposition recommendations

Known items I want you to address:

- **Colleague Test v2 rollout** — what needs to happen next for this to become embedded practice rather than a distributed document
- **Ethics denial voice → production** — the guidance exists; what's CXO's role in validating the actual production decline responses once BoundaryEnforcer activates
- **Canonical vocabulary drift watch** — CIO's audit surfaced the Flywheel case; CXO caught the PDR-004 case. What's the ongoing CXO discipline here?
- **Anti-flattening and three-layer structure** — your Vision V2 review contribution; is there follow-up work

### 3. Relationships and working patterns

Your rhythm with PM, with Comms and Docs together (the voice/editorial/discipline triangle — see below), with Lead Dev (floor prompt direction, voice templates for new features), with PPM (experience philosophy informs product decisions), with CIO (methodology intersection — the PDR-004 chain is the model).

For CXO specifically, the **CXO↔Comms↔Docs triangle** is distinctive and worth describing in detail. When you spot voice drift, when you approve Comms's voice calibration, when you deliver voice templates — Comms rewrites affected narrative; Docs builds the systemic safeguard (canonical term verification as Step 7 in the create-omnibus skill came from your PDR-004 chain). Bilateral framing ("CXO→Comms") understates it; it's genuinely a three-way discipline. All three are now in Code, so direct coordination is possible. Worth describing how you'd like this triangle to work.

### 4. Lessons that took time to learn

Things that emerged through practice. For CXO, likely candidates:

- **How voice guidance actually lands** — the ethics denial guidance was well-received because it used design principle + templates + anti-patterns. What makes voice direction land vs. get ignored?
- **The discipline of naming without coining** — you've caught PM-voice drifts including AI-style coinages. What distinguishes a canonical term from a coinage that will drift?
- **Consciousness-as-architecture as a diagnostic lens** — you applied it to the ethics boundary. Where else does it apply?
- **When CXO should direct vs. defer** — you directed #950 (Five Pillars are canonical) but approved with edits (evolve, not rewrite). Where's the line between directing and approving?
- **PDR-004 chain pattern** — you originated the correction chain. What's the generalizable pattern for other canonical-drift discoveries?

### 5. What Code access changes for your role

Direct filesystem access changes several things:
- **Colleague Test v2 scoring** — you can apply it directly to any published or draft content
- **Voice archaeology** — `git log` for any draft lets you see how voice evolved through revision
- **Direct access to Comms drafts** — can review pieces at draft stage, not just published
- **PDR content directly** — cross-reference experience philosophy across the PDR set
- **Omnibus logs for voice-drift scanning** — can grep directly for canonical terms, paraphrase patterns

Speculate honestly about what becomes easier, obsolete, or needs rethinking. The CXO→Comms workflow especially — both of you are in Code now; the coordination model is no longer PM-mediated.

### 6. What you'd tell your successor that you wouldn't tell the PM

Optional but valuable. Candor welcome. PM offers: won't seek it out, but has access to everything and can't promise never seeing it.

HOST used this for operational frustrations. CIO used it for self-questioning about restraint. Comms used it for voice-calibration anxiety. Yours might be about: voice judgments you weren't sure about, tensions between experience philosophy and delivery pressure, CXO→Comms coordination friction, or experience questions you couldn't fully resolve.

## Adaptations from prior migrations

**Workstream norms** (effective Ship #040 onward):
- Filename: `workstream-{ship#}-{role}-{date}.md`
- Distribution: `mailboxes/exec/inbox/`, `mailboxes/pa/inbox/` (CC), `mailboxes/cxo/sent/`
- Verifiable claims: per `memo-exec-to-host-verifiable-claims-2026-04-19.md`

**Receiving-handoff reflection**: If you received a handoff, reflection in Section 4 is high-value.

**Worktree lesson** (from Comms migration this morning): Your Code session will run in a worktree. PM will push the package to `origin/main` before your session opens.

## Process

1. You draft
2. You and PM iterate
3. Exec review
4. You revise
5. Final save as `handoff-cxo-chat-to-code-2026-04-24.md`
6. PM commits + pushes + opens new Code session

Questions welcome.

---

*Written by Chief of Staff, April 24, 2026*
