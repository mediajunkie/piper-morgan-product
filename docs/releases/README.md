# Release Notes Index

This directory contains release notes for all Piper Morgan versions.

---

## Current Version

**v0.8.11.0** (July 17, 2026) - [Release Notes](RELEASE-NOTES-v0.8.11.0.md)

RECONNECT WS-1 + security + design D2: DB-backed connector config, StandupAssembler promoted, AES-256-GCM field encryption, encrypted secret store, per-user LLM key wiring, admin_compose removed, auth-exempt lint enforcement, token system, responsive shell, mobile nav, Documents→Radar rename.

---

## Release History

| Version | Date | Type | Highlights |
|---------|------|------|------------|
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

*Last updated: July 17, 2026*
