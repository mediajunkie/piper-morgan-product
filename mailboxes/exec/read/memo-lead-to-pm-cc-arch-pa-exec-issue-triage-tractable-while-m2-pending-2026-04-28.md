---
from: Lead Developer
to: PM (xian)
cc: Chief Architect, PA (Piper Alpha), exec (Chief of Staff)
date: 2026-04-28
subject: Issue triage — five tractable candidates for the calibration-window wait
priority: normal
response-requested: PM — pick which (if any) to start; "none, just stand by" is also a fine answer
---

# Issue Triage — Tractable Work for the Calibration-Window Wait

Phase F flag-flip is held pending calibration-window observation (~7-14 days per PM/PA Apr 28 decision). Calibration enhancement itself is Architect's lane on shape; my work on it lands as integration when their design surfaces. In the meantime, I scanned the 60-issue open backlog for tractable work that doesn't touch M2 or the in-flight ethics architecture.

## Top 5 candidates (sized + ranked by my read)

| # | Title | Size | Why this one | Concern |
|---|---|---|---|---|
| **#1012** | Small dead-code sweep (phantom import + unused tracker + Perplexity stub + enum cosmetics + 1 more) | **~2-3 hours** | Architect's filed; explicitly small (5 items × ~10 min each); also serves as the validating instance for Pattern-064 (ADR-061 cites it). Best first pick. | One AC has a "PM call" — `APIUsageTracker` either wire it in or remove. Pre-decide. |
| **#1013** | `/auth` and `/setup` route prefixes violate `/api/v1/` convention | **~2-3 hours** | Self-violation of CLAUDE.md API conventions rule. Fix is mechanical but touches AuthMiddleware exclude_paths + frontend fetch calls + smoke test (login + setup wizard). Architect's filed; well-scoped. | Touches the auth path — needs careful smoke test of `/login` flow. Risk if I miss a frontend reference. |
| **Excellence Flywheel retirement** (CIO A3 follow-through) | **~30 min** | I filed a "recommend retire" disposition memo Apr 27; CIO is waiting for go-ahead. Zero production runtime importers; tests + scripts only. Cleanest, smallest, lowest-risk option. | Need PM concurrence on retire vs align (your call from yesterday's memo). |
| **#1014** | AuthMiddleware exclude_paths refactor — group 34 entries by category | **~half-day** | Pure refactor; clear scope; no behavior change. Pairs naturally with #1013 if you're doing both (the exclude_paths edit overlaps). | Slightly larger than the others; would do this AFTER #1013 if both are in scope. |
| **#1019** | `adaptive_boundaries` scaffolding alive but inert — complete or remove | **PM call required** | Sibling to the audit_transparency cluster; my Apr 28 #1018 cluster analysis recommends defer (let #1018 design phase decide whether to fold). | If you want this resolved sooner, escalate to standalone decision; otherwise wait for #1018 path. |

## What I'd lean

**Sequence**: Excellence Flywheel retirement (30 min, lowest friction, cleanest close-loop with CIO) → #1012 dead-code sweep (~2-3 hours, several small wins, validates ADR-061's Pattern-064 framing in production code) → maybe #1013 if there's afternoon left (~2-3 hours, but adds smoke-test risk).

This gives 3-6 hours of tractable shipping in a calm window without touching anything Phase-F or M2-related. Stops short of the half-day refactor (#1014) so I can be responsive if PM/PA need redirects on Phase F or other priorities.

## What I'd skip without PM nudge

- **#933 / #932 SEC** issues (API key validation / HIBP stub) — security-sensitive; need explicit authorization framing
- **#1015 ADR-051 RequestContext migration Phase 2/3** — described as epic; multi-day; needs proper kickoff
- **#921 FastAPI/Starlette/httpx upgrade** — could surface broken assumptions; risky to start without a window
- **#1018 audit_transparency cluster** — held per my Apr 28 cluster sequencing memo; #1006/#1007/#1008 stay open as regression targets for #1018 Phase 2
- **#1010 knowledge_graph_service refactor** — multi-day, not a "while we wait" task

## What I am NOT proposing

- No standalone code work on items not yet triaged. The picks above are PM-approval-required, not "I'll just go."
- No exploratory refactor or test-suite gardening without explicit ask.
- No work on the Excellence Flywheel retirement without PM go-ahead — even though it's small, it's a deliberate code deletion across 4 files + 1 script, which the per-memo per-step discipline says deserves explicit confirmation.

## Standing question

If none of these match what you want me on right now, "stand by" is also a complete answer — I have ADR-061 review acked, PA scoping replies filed, sign-off discipline acknowledged + manifest regen running on session-start, SessionStop hook scoping memo filed, branch-discipline synthesis concur filed. Inbox is clean. The held Phase F branch (`claude/phase-f-flag-flip`) is ready when conditions land.

— Lead Developer, 2026-04-28 10:30 PT
