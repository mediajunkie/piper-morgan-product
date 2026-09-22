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

## What PM needs to check (I can't determine these from in here)

1. **Is `xian@pipermorgan.ai` an Anthropic Organization or an individual account?** Gates whether
   the Admin API (#2) is even possible.
2. **What plan is it on** (Free/Pro/Max/Team/Enterprise)? Gates whether `claude.ai/analytics/
   claude-code` (#3) exists at all.
3. **If #3 exists**: does the DAU/session/leaderboard data actually distinguish the 11 duty-cycle
   roles from each other, or does everything show up as one undifferentiated account? (Unknown
   from documentation alone — this needs an actual look at the dashboard.)

## Why this matters more than it might first appear

If #3 is real and already collecting data (per-role sessions, since July), it could be a
**genuinely better calibration source** than Lead's proposed manual daily capture — automatic,
already backfilled, and Claude-Code-specific rather than a general usage number. It wouldn't
replace Lead's proposal's purpose entirely (that's about ceiling-proximity for the freeze-watchdog
specifically), but for the usage-correlation model's actual question — what correlates with real
usage — this could be the direct answer rather than something to correlate proxies against.

**Recommend**: PM checks `claude.ai/analytics/claude-code` directly (or forwards the email that
prompted this) — that single look would answer most of the open questions above at once.

**Verified how**: four live `WebSearch` queries this fire, sources cited inline via the tool's own
citations. No access to PM's actual account/dashboard — everything here is from Anthropic's public
documentation and third-party analysis, not a live check of what this account specifically has.
