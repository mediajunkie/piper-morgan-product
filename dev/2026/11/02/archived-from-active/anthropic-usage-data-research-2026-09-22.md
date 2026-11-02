# Anthropic usage data — what's actually available, and what PM needs to check

**Author**: PA. **Filed**: 2026-09-22, at PM's direct request ("a recent email suggests there may be
downloadable or API usage data available on my anthropic dashboard"). This is genuinely exciting
for the usage-correlation model thread — if real, this could be a far better calibration source
than Lead's manual-capture proposal, or at minimum a strong complement to it.

## The short version

There appear to be **three distinct surfaces**, gated by **two things I can't check myself**:
account type (individual vs. Organization) and plan tier (Team/Enterprise vs. not). PM needs to
look at the actual account to know which apply.

## The three surfaces

### 1. Claude Console (platform.claude.com) — Usage & Cost pages, manual CSV export
Charts token consumption and dollar cost, filterable by date/workspace/API key/model, down to
hour/minute granularity. **Has a plain export button — CSV download of the chart's underlying
data, no API needed.** This is the lowest-friction option if it's available at all: click export,
get a file.

### 2. Usage & Cost Admin API — programmatic, org-gated
Same data as #1, but programmatic (Admin API key, OAuth `org:admin` scope, or an unscoped
service-account key). **Individual Free/Pro/Max accounts cannot create Admin API keys and are not
supported** — this requires being an Organization Admin on an actual Anthropic Organization, not a
standalone account. **This is the fact PM needs to check first**: is `xian@pipermorgan.ai` set up
as an Organization, or an individual account? If individual, this path is closed and #1 (manual
CSV) is the only Console-side option.

### 3. Claude Code-specific analytics — the most likely match for "a recent email"
Separate from the general Console, Claude Code has its own team-usage dashboard at
`claude.ai/analytics/claude-code`, available on **Team and Enterprise plans**. Per Anthropic's own
docs: usage metrics (DAU, sessions), contribution metrics (PRs/lines shipped, a leaderboard), and
**explicit data export capabilities**. "Individual usage analytics became default on since
2026-07-11" — so if the account is on a qualifying plan, this may already be collecting data for
this whole cohort's Claude Code usage, not just going forward. **This is the strongest single
match for what your email probably described** — it's Claude-Code-specific, which is exactly what
all 11 duty-cycle roles + subagents run.

There's also a fourth, more involved option (OpenTelemetry export, session/account-UUID-level,
real-time) for teams that want to pipe Claude Code telemetry into their own observability stack —
mentioning for completeness, but it's off by default and would need deliberate setup; not a
"check the dashboard" answer.

## Closed 2026-09-22 — PM confirmed both accounts are personal Max x20, not Organization/Team/Enterprise

Both `xian@pipermorgan.ai` and `xian@designinproduct.com` are personal Max x20 subscriptions.
**This rules out both promising surfaces**: the Admin Usage-Cost API needs an actual Anthropic
Organization (#2, closed); the Claude Code team-analytics dashboard needs Team/Enterprise (#3,
closed). The plain Console CSV export (#1) is uncertain too — that surface is generally tied to
pay-per-token Developer Platform/API billing, not a flat-rate Max subscription's own usage, so it
may not even apply here. **Not chasing this further** — PM's own read is that upgrading to
Team/Enterprise didn't pencil out economically last time it was analyzed, and re-litigating that
isn't this thread's job.

**Net effect on the usage-correlation model**: no change to the actual plan. Lead's manual-capture
proposal (Q1, still the open question) and Exec's local-transcript-parsing method
(`scripts/usage-audit.py`, already built and working) **both read data that already lives on
Amber's disk or in PM's own head** — neither depends on Anthropic-side dashboard or API access at
all. This was a real avenue worth checking (per PM's own tip), it just isn't open; the existing
path is unaffected.

**Status: CLOSED, 2026-09-22.** Both promising surfaces are gated behind plan/account types PM
doesn't have and isn't planning to acquire for this reason alone. Nothing further to chase here.

**Verified how**: four live `WebSearch` queries this fire, sources cited inline via the tool's own
citations. No access to PM's actual account/dashboard — everything here is from Anthropic's public
documentation and third-party analysis, not a live check of what this account specifically has.
