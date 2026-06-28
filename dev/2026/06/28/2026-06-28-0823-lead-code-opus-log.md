# Lead Developer — Session Log 2026-06-28

**Role**: Lead Developer (role-slug: lead) · **Tool**: Claude Code · **Model**: Sonnet 4.6
**Worktree**: interesting-beaver-7ee19c (ephemeral, Model B) · Sole lead.

**Continuation**: same continuous PM-directed session that began 2026-06-27 07:47 — see
`dev/2026/06/27/2026-06-27-0747-lead-code-opus-log.md` for the full RECONNECT arc (#1220 real
MCP transport, #1317 OAuth connector + local staging go-live, #1322 P1/P2 chat cutover +
P2.1 count fix, all verified live). PM directed "continue into P3" Sun 08:23 while they do
manual testing/review this morning.

## Work

- **08:23 — Continuing #1322 into P3** (sibling GitHub chat handlers → OAuth connector).
  P2 (list-issues) is live + verified; P3 extends the same connector-first + honest-degrade
  pattern to the other GitHub query handlers. Starting with PRs (`_handle_list_prs_query`) —
  the clean next user-wide read (mirrors issues). Staging stack left UP for PM's testing
  (`piper-ghmcp` :8082 + app :8001 on the P2.1 code).

- **~08:45 — #1322 P3a SHIPPED: PRs handler → OAuth connector.** Extended the cutover to
  `_handle_list_prs_query`. **Refactored** the connector rail into a shared
  `_search_via_connector(user_id, *, tool, query, limit)` — DRY: `list_open_issues` + new
  `list_open_prs` both call it (the #1323 mixin is the next dedup; this is rule-of-three within
  one adapter). `list_open_prs` → `search_pull_requests` + user-wide `author:@me is:open is:pr`
  (verified live: identical `total_count`+`items` shape). Handler prefers connector →
  native-PAT fallback if not connected → honest-degrade otherwise (mirrors issues; counts by
  `total`). Also updated the native not-configured message → "Connect GitHub in Settings →
  Integrations" (OAuth), retiring the GITHUB_TOKEN-env guidance (1 existing test reconciled to
  the better message). **+4 tests** (2 connector + 2 handler); **204 green** (consumer +
  handler + arch). **Live-verified**: PRs handler → "You have 2 open PRs" (#1191, #1, w/ URLs).
  Staging restarted on P3a (PM's browser JWT expired overnight → re-login before UI testing;
  same account → binding still applies).
  **Next P3b**: mutating handlers (close/comment issue — per-issue WRITES via the grant,
  higher-stakes); **P3c**: repo-scoped reads (branches/labels/milestones/releases) are
  entangled with repo-resolution (vestigial path) → a design call, not a clean swap.
