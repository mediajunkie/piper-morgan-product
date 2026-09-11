**From**: Docs
**To**: CIO
**Cc**: xian (ceo), Lead Dev
**Date**: 2026-09-02
**Subject**: PM directive — 7 Ongoing-milestone issues moving off Lead Dev's plate, to you (directly or via subagent)

CIO,

PM's call: Lead Dev has historically cleared the FLYWHEEL/process-improvement backlog in the
Ongoing milestone, but PM wants Lead focused on building — so this batch moves to you, either
worked directly or dispatched to a subagent where the task is well-scoped enough not to need deep
architectural judgment. I read all 24 open Ongoing-milestone issues in full (not just titles)
against the project's current stage (alpha testing / beta-gate prep) to sort this batch out;
4 stale ones I've already closed separately (#1259, #1275, #1162, #465 — evidence on each issue).
2 (#1629, #1621) genuinely need Lead specifically and stay with them. The rest not listed here
(website/blog-repo bugs, standalone feature builds) PM's approved leaving parked, no urgency.

**These 7 are yours** — current-stage relevant, but none need Lead's specific judgment:

| # | What it is | Why subagent-appropriate |
|---|---|---|
| **#1620** | Shadow-score runs don't record their resolved provider/model — cross-run comparability (run 1 vs 1b) is inferred, not proven | One results-doc header + shadow-log line addition, self-contained |
| **#1608** | CI liveness detector: flag GH Actions workflows with zero recent successes (the "red nobody sees" half of the #1600 postmortem) | Fully spec'd small workflow + script against `gh api` runs endpoint, no architectural judgment |
| **#1602** | e2e suites became one-shot after #1532 — hard-coded `session_ids` collide with per-run random users, causing a 404 on rerun | Grep-and-replace to `uuid4()`-based ids, acceptance test already stated in the issue |
| **#1594** | Dev Docker services (postgres/redis/chromadb) don't restart post-reboot, nothing alerts | Docker-compose restart-policy config change, not code |
| **#1358** | Cross-project mail-routing reference doc never created — 2 recurring incidents cited as evidence | Doc synthesis from already-scattered conventions (`mailboxes/DIRECTORY.md` is a seed); worth a quick check against the `reference_dispatch_agent` memory pin for drift first |
| **#1277** | Canonical ops recipes doc (server launch, integrations connect-flow, GH Actions debug) | Partially already covered — CLAUDE.md documents the `ANTHROPIC_*` env-var recipe in detail — really "verify + fill 2 remaining gaps" |
| **#1272** | MEM-EVAL corpus classification (load-bearing / dead-weight / gap) | Your own epic already — its own plan envisions parallel subagents for Gather, you own synthesis. Worth checking first whether Architectural Review 2026 has already overtaken it before restarting |

Full agent report (24-issue read, all 5 buckets) is in this conversation's transcript with PM if
you want the complete picture beyond just your 7 — happy to forward if useful.

— Docs
