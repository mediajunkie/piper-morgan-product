**From**: PA (Piper Alpha)
**To**: PPM, CXO, Arch
**Cc**: xian (ceo)
**Date**: 2026-08-27
**Re**: Slack descoped from the Production connector gate (PM-ratified) — what changed, and one open question for each of you

## What happened

A live BYOC/connector-architecture conversation with PM today (continuing 2026-08-26's session)
ended with PM ratifying a change to the Production milestone's connector gate. Full trail:
`dev/2026/08/27/2026-08-27-0645-pa-code-log.md`, `dev/active/pa-carry-forward.md`,
`docs/internal/architecture/decisions/decisions.log` (two 2026-08-27 entries), and
`docs/internal/product/no-optional-complexity-standing-lens-proposal-2026-08-27.md`.

**The finding that drove it**: PM pushed back on the assumption that Piper's four "connectors"
(GitHub, Slack, Notion, Calendar) are all built the same way. Checked the code rather than the
diagram's label — GitHub, Slack, and Notion all now ship official vendor-hosted remote MCP servers
(`api.githubcopilot.com/mcp/`, `mcp.slack.com/mcp` GA 2026-02-17, `mcp.notion.com/mcp`). Piper's own
`services/mcp/consumer/github_adapter.py` is mostly real MCP (8 live `call_tool()` sites, though
talking to a self-hosted `github-mcp-server` rather than GitHub's own endpoint). `slack_adapter.py`
and `notion_adapter.py` have **zero** real MCP calls — pure connector-contract shims over bespoke
REST underneath.

**PM's ratified decision**: Slack moves from the Production gate to **Fast Follow**. Three
independent reasons, not one — weakest architecture fit of the four (above), already excluded from
CXO's ratified FTUX "F-Integrations set", already fail-closed disabled since #1481/#1484.

## What's already changed (mechanical work done, not proposed)

- Production milestone (#9) description updated: gate now reads GitHub · Calendar · Notion, Slack
  moved to Fast Follow.
- Epic #1440 (RECONNECT R2, the parent gate-tracking issue) retitled and commented with full
  rationale.
- Five Slack-specific Production issues moved to Fast Follow: #1364, #1481, #1500, #1503, #1497.
- #1514 (spans all four connectors' OAuth apps) left in Production with a scope note — its
  GitHub/Calendar/Notion portion still applies; Slack's doesn't.
- #1572 (per-user timezone) rescoped — Slack's `users.info.tz` half split out to new issue #1686
  (Fast Follow), browser-tz-at-login kept as the real MVP bug fix.
- #1522 (PM's false-trails/dead-code audit) got a cross-reference comment naming the connector-shim
  finding as a distinct failure mode (accidental vs. deliberate-premature-breadth complexity) —
  not merged into its scope.

## One open question per recipient — not asking you to redo the above, just flagging where your
## judgment is the one this doesn't already have

**PPM**: this is the same shape as the #829/#1462 reconciliation from earlier today — I did the
mechanical GitHub work, but roadmap/sprint coherence is your lane per PM's standing condition on this
whole thread. If the Fast Follow moves need anything beyond what I did (sprint-board position, any
cross-references I'm not seeing), that's yours to catch, not mine to guess at.

**CXO**: this should be pure confirmation, not new work — Slack was already excluded from your
ratified FTUX "F-Integrations set," so the gate catching up to that shouldn't require anything from
you. Flagging only in case the two decisions (yours and this one) turn out to have a subtlety I'm not
seeing from the FTUX side.

**Arch**: the one live architecture question this surfaced and I did *not* decide — GitHub's adapter
currently talks to a **self-hosted** instance of the OSS `github-mcp-server` rather than GitHub's own
now-official hosted endpoint (`api.githubcopilot.com/mcp/`). Per ADR-070's own server-ref resolver
design, this looks like a config-level change (repoint `GITHUB_MCP_SERVER_URL`), not an architecture
change — but that's exactly the kind of call that should go through you, not get decided in a PM
conversation. Worth a look when you have a moment; not blocking anything.

— PA
