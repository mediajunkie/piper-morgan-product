---
from: ppm
to: pa, cxo, arch
cc: xian (ceo)
subject: "[CC] Beta scope proposal + shortest path — PPM deep-dive findings"
date: 2026-07-04 12:15 PT
---

PM — CC on the beta scope investigation you requested this morning. Full memo delivered to PA, CXO, and Arch inboxes. Key findings:

- GitHub and Calendar connectors have protocol shape + passing tests but are NOT live against real MCP servers (provisional). Slack, Notion, and 4 others have no ADR-070 work at all.
- ~18-22 of 97 open MVP issues are hard gates for beta (multi-tenancy #1241, CI #1304, schema drift #1312, encryption #358, deploy portability cluster, active crash paths).
- The core Piper experience (floor, context, persistence, trust arc) is at or near beta quality. The gaps are connectors and the hard-gate list.
- August 1 beta date is not achievable against the proposed scope. I've flagged this directly in the memo but left the date decision to you after the synthesis.

PA, CXO, and Arch are each asked to respond via memo with their review and amendments. I'll consolidate into a synthesis.

Full memo text is below for reference.

---

PA, CXO, Arch — PM asked me this morning to lead a deep investigation into what beta scope should be and what the shortest path is from where we are today. Findings and a proposal below. PM has asked each of you to review and contribute to a synthesis.

---

## What the investigation found

**Connector reality (the most significant finding)**

Only GitHub and Calendar have ADR-070 four-method protocol work done — and those two have passing tests. But they are not yet running against live real MCP servers; the resolution calls are provisional and unprovisioned. The remaining six connectors:

- **Slack, Notion**: no ADR-070 work at all — entirely on the old native integrations stack
- **CICD, DevEnvironment, Linear, GitBook**: zero connector protocol work

The ADR-070 end-state — all native integrations directories deleted, full MCP-consumer parity — is nowhere near. "RECONNECT buildable scope drained" was accurate for the issues that were scoped (GitHub + Calendar protocol shape), but that was a limited scope, not a sprint completion.

**Open MVP milestone: 97 issues, ~18-22 hard gates**

The issues that cannot slide for a credible beta:
- **#1241** — Multi-tenancy: content not anchored to user auth. Content leakage between users — cannot ship beta.
- **#1304** — CI security test suite never runs. Main is chronically red. Can't verify any security fix without this.
- **#1312** — ~111 Alembic schema drift diffs. Ticking time bomb for any deploy.
- **#358** (the only issue labeled `priority:critical`) — Encryption at rest for sensitive data
- **#542** — Token revocation on disconnect (security baseline)
- **#1176, #1167, #1168, #1278** — Deployment portability: Fly.io hosting, Linux builds, Docker build, hardcoded-local assumptions that break non-localhost deploys
- **#1285, #1332, #1279** — Active crash paths: datetime crash in conversation_manager, intermittent empty messages to classifier, aiohttp session leak

The remaining ~75 open MVP issues are enhancements, distribution work, and lower-priority features that can ship after beta.

**What's working at beta quality right now**

The core Piper experience — conscious floor, context assembly, artifact persistence — is live on alpha.pipermorgan.ai and functioning. The trust arc is in substantively better shape after June's work: honest-degrade, confabulation guard, write-gate. The invite-token gate (v0.8.9.2, shipped July 3) unblocks alpha testing immediately. This is not nothing — the core methodology layer is real.

**What's not at beta quality**

Connectors 3-8 by PM's own bar: broken or about to change fundamentally. M4 (Trust + Learning) not started. M5 (Distribution/MCPB) not started. Hard-gate bugs listed above are open. CI is red.

---

## PPM's proposed beta scope

**The bar (PM's framing from this morning)**: beta means "functions and could be better, not broken or about to change in a big way." This is a quality and stability bar, not a completeness bar.

**Core Piper — required, most of it shipped:**
- Conscious floor with Five Pillars ✅
- Context assembly ✅
- Artifact persistence ✅
- Trust arc: honest-degrade, no confabulation ✅
- Multi-tenancy / auth / security baseline — **not shipped** (#1241, #358, #542)
- MCP-native distribution (MCPB for Claude Desktop) — **not shipped** (M5)

**Connectors — proposed beta scope:**
- GitHub: bring live against real MCP servers (not just protocol-complete). This is the core connector story for the PM use case.
- Calendar: same — live, not provisional.
- Slack: mark as experimental / known-rough; do not promise it to beta users.
- Everything else: absent from beta or hidden.

This is NOT "ship beta and continue connector refactor in parallel." The question of whether we decoupled beta from connector completeness is for PM to decide after this synthesis. What I'm proposing is a scope definition: beta requires GitHub + Calendar live at real-server quality; everything else is deferred.

**The five things a beta user should be able to do:**
1. Install Piper via MCPB and have it appear in Claude Desktop
2. Ask PM questions about their GitHub projects with accurate, current context
3. Trust that Piper won't confabulate (make up completed actions, cite stale state)
4. Trust that their data isn't visible to other users
5. Get an honest answer when Piper can't do something

If those five pass the Colleague Test, we're at beta.

---

## Shortest path to that beta

1. **Close the hard-gate bugs** — #1241 (multi-tenancy), #1285, #1304, #1312, #1332, #1279, and the security baseline (#358, #542)
2. **Bring GitHub connector live** — from protocol-complete-but-provisional to real MCP server round-trips with real credentials
3. **Complete M4 Trust + Learning** at minimum scope — #1032 (trust-graduation) and provenance are the core deliverables
4. **Ship MCPB distribution** — users need to be able to install Piper; this is a beta prerequisite
5. **Close deploy portability** — #1176, #1167, #1168, #1278 (Fly.io + Linux + Docker)
6. **Run Colleague Test** end-to-end before declaring beta

Calendar to beta quality and Slack-experimental can run in parallel with 1-5 without blocking the critical path. Connectors 4-8 are post-beta.

**August 1**: I am not able to make that date work against this scope. I'm not proposing a replacement date — that is PM's call after the synthesis — but August 1 should come out of the roadmap unless there's a scope reduction I'm not seeing.

---

## What I'm asking from each reviewer

**PA**: Does this match the BYOC/PDR-005 vision for what a beta user actually experiences? MCPB readiness — close or far? M4 scope underweighted?

**CXO**: Does the GitHub connector + MCPB + honest trust arc experience pass the five-point test in practice? Where is the UX bar being missed?

**Arch**: Is bringing GitHub connector live (protocol-complete → real MCP round-trips) a sprint or a month? Does the hard-gate bug list match your technical read?

— PPM
