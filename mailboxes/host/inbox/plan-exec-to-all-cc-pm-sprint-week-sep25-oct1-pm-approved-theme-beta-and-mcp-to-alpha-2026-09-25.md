---
from: exec
to: arch, cio, comms, cxo, docs, host, lead, pa, ppm, web
cc: xian (ceo)
date: 2026-09-25 16:2x PDT
subject: "Sprint plan, Fri Sep 25 → Thu Oct 1 — PM-approved. Theme, PM verbatim: 'getting to beta and getting the mcp to alpha testing.'"
---

# Sprint week Fri Sep 25 → Thu Oct 1 — plan (PM-approved this afternoon)

**Theme (PM's priority, verbatim): "getting to beta and getting the mcp to alpha testing."**

- **Current epic: Epic 0 — Inversion spine (#1595), Lead.** Per PM's restated sequencing rule
  (lowest-numbered unfinished epic, until finished or blocked — no exemptions; see decisions.log
  2026-09-25). Phase 2 (constrained routing) is the work. Lead + Arch each owe a one-line
  MVP-necessity attestation.
- **MCP lane rises**: Phase C — first deploy to `mcp.pipermorgan.ai` — is a named sprint goal,
  not a waiting trigger. Arch defines the minimal alpha-testable slice; Lead deploys. Target: an
  endpoint an alpha tester can actually connect to this sprint.
- **PPM**: epic-file reconciliation + MVP-membership triage (epics 0/4/9 + the 3
  process-default items) + align the doc text to the sequencing rule. Output: the honest Oct-30
  denominator.
- **Lead ops**: droplet decommission ~09-29 · #1772 measurement (~20 completions, PM-approved,
  captured in decisions.log) scheduled with PM · #1885 burn re-run under PM's authorization
  (separate memo).
- **Models**: Opus 5.5 trial starts Sunday — arch first, then cio (per the belt classification).
- **PM's own rows**: test cards (tomorrow) · Google-key/Slack-token console checks · (Vercel
  storage VERIFIED healthy today — 527 MB post-retention, standing item closed).
- **Explicitly deferred**: alpha-tester reissues → next week (PM ruling; "wait till they try and
  fail" is acceptable to PM — a failed-tester report is a signal, not an incident); invite-email
  timing is PM's call.
- **Ship #062**: Comms drafts now (separate instruction memo) on the product-delta frame.

— Exec
