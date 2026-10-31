# Release Notes Index

This directory contains release notes for all Piper Morgan versions.

---

## Current Version

**v0.9.0.0** (October 31, 2026) - [Release Notes](RELEASE-NOTES-v0.9.0.0.md)

"Trust in what Piper tells you" — the first private beta release, closing the MVP milestone. Invited-tester setup no longer ends in "Setup Failed" (#2078), the Integrations Test and status reflect the real connection (#2012, #2045), failed calendar and GitHub reads are reported as failures rather than empty days (#2182), and chat fixes cover todos, reminders and GitHub issues. Send feedback and chat delete are reachable in the app (#2096, #2065), and a hosted MCP server ships at mcp.pipermorgan.ai.

---

## Release History

| Version | Date | Type | Highlights |
|---------|------|------|------------|
| [v0.9.0.0](RELEASE-NOTES-v0.9.0.0.md) | Oct 31, 2026 | Beta | First private beta release, closes the MVP milestone (1,138 code commits and 361 issues closed since v0.8.14.0): invited-tester setup works (#2078), Integrations Test and status reflect the real connection (#2012, #2045), failed calendar and GitHub reads reported as failures (#2182), todo/reminder/GitHub-issue chat fixes, send-feedback and chat delete, hosted MCP server at mcp.pipermorgan.ai; seven Alembic migrations |
| [v0.8.14.0](RELEASE-NOTES-v0.8.14.0.md) | Sep 23, 2026 | Fast follow | "On Your Clock": preferences persist (#1574), every clock face in the user's zone + agenda 'TBD' fixed (#1576/#1575/#1577/#1556), add-project one-liner (#1856), honest 404-close (#1858), any-provider gate + four honest LLM-error sentences first deployed (#1823/#1824), preferences routes fixed (#1864), one Slack OAuth start (#1499), 13 dead modules + 5 dead tables removed (#1774/#1797); first release targeting the Fly-served alpha |
| [v0.8.13.0](RELEASE-NOTES-v0.8.13.0.md) | Sep 21, 2026 | Fast follow | Dogfood fixes: standup trust rebuild (#1837/#1836), keyless first contact (#1818b), server-key concept deleted (#1812 complete), /health deploy identity (#1839) |
| [v0.8.12.0](RELEASE-NOTES-v0.8.12.0.md) | Sep 20, 2026 | Feature | BYOC/tenancy arc complete — your key/your billing, honest refusals, security six, acceptance contract, truth-in-rendering; first full-belt-green cut |
| [v0.8.11.0](RELEASE-NOTES-v0.8.11.0.md) | Jul 17, 2026 | Feature | Finish-the-Unfinished — multi-tenancy correctness (per-user provider, personality restored), honest conversation (no false claims/denials), completion ratchets |
| v0.8.9.1–v0.8.10.14 | Jul 2–16, 2026 | Hotfix train | production-only cherry-pick cuts: #1343/#1344 security, Fly beta cutover (#1278), tester-loop fixes, login regression (.14) — all content since merged to main |
| [v0.8.9](RELEASE-NOTES-v0.8.9.md) | Jun 22, 2026 | Feature | RECONNECT WS-1 + security + design D2 — connector infra, field encryption, token system |
| [v0.8.8](RELEASE-NOTES-v0.8.8.md) | Jun 19, 2026 | Feature | D1/RECONNECT — BYOC keys, Radar default, nav IA, home UX |
| [v0.8.7](RELEASE-NOTES-v0.8.7.md) | Jun 14, 2026 | Feature | M1+M2+M3 — Conscious Floor, dispatch rail complete, files UX, Slack inbound |
| [v0.8.6](RELEASE-NOTES-v0.8.6.md) | Mar 4, 2026 | Feature | M0 Conversational Glue, 27 issues resolved |
| [v0.8.5.3](RELEASE-NOTES-v0.8.5.3.md) | Feb 11, 2026 | Patch | Windows compatibility, setup UX, 14 issues resolved |
| [v0.8.5.2](RELEASE-NOTES-v0.8.5.2.md) | Feb 6, 2026 | Patch | Chat persistence, date formatting, calendar fixes |
| [v0.8.5.1](RELEASE-NOTES-v0.8.5.1.md) | Jan 31, 2026 | Patch | 14 alpha testing bug fixes |
| [v0.8.5](RELEASE-NOTES-v0.8.5.md) | Jan 27, 2026 | Feature | MUX-IMPLEMENT complete, WCAG 2.1 AA accessibility |
| [v0.8.4.3](RELEASE-NOTES-v0.8.4.3.md) | Jan 18, 2026 | Patch | Fresh install fixes (#605-#609), UI polish |
| [v0.8.4.2](RELEASE-NOTES-v0.8.4.2.md) | Jan 15, 2026 | Patch | Calendar bug fixes (#596, #588), markdown rendering |
| [v0.8.4.1](RELEASE-NOTES-v0.8.4.1.md) | Jan 14, 2026 | Patch | Calendar/TEMPORAL timezone fixes, intent routing |
| [v0.8.4](RELEASE-NOTES-v0.8.4.md) | Jan 12, 2026 | Feature | Integration Settings, Portfolio Onboarding |
| [v0.8.3.2](RELEASE-NOTES-v0.8.3.2.md) | Jan 8, 2026 | Feature | Interactive Standup Assistant (Epic #242) |
| [v0.8.3.1](RELEASE-NOTES-v0.8.3.1.md) | Jan 7, 2026 | Patch | FTUX improvements (greeting panel, empty states, post-setup orientation) |
| [v0.8.3](RELEASE-NOTES-v0.8.3.md) | Jan 2, 2026 | Feature | Epic #314 CONV-UX-PERSIST complete |
| [v0.8.2](RELEASE-NOTES-v0.8.2.md) | Dec 2025 | Feature | UX polish, accessibility improvements |
| [v0.8.1](RELEASE-NOTES-v0.8.1.md) | Nov 2025 | Feature | Version display, startup refactoring |

---

## Versioning Strategy

Piper Morgan uses semantic versioning with the following pattern:

- **Major (0.x.x)**: Pre-1.0 alpha phase
- **Minor (x.8.x)**: Feature releases, epic completions
- **Patch (x.x.3)**: Bug fixes, small improvements

See [versioning.md](../versioning.md) for full versioning strategy.

---

## Known Issues

For current known issues and limitations, see [ALPHA_KNOWN_ISSUES.md](../ALPHA_KNOWN_ISSUES.md).

---

## For Alpha Testers

- [Alpha Testing Guide](../ALPHA_TESTING_GUIDE.md) - How to test Piper Morgan
- [Alpha Quickstart](../ALPHA_QUICKSTART.md) - Getting started fast
- [Alpha Agreement](../ALPHA_AGREEMENT_v2.md) - Terms for alpha testing

---

*Last updated: October 31, 2026*
