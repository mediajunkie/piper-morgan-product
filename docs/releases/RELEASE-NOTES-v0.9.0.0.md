# Release Notes — v0.9.0.0 (private beta)

**Cut**: 2026-10-31 from `main` · **Type**: beta (the first 0.9 release; the MVP milestone closed
2026-10-30 17:03 PT on xian's GO) · **Hosting**: alpha.pipermorgan.ai and beta.pipermorgan.ai are
both served by Fly from the same cut; the beta invitations go out with this release.

> **Status of this file (2026-10-31 09:28 PT, Lead):** the version files and this skeleton land on
> main ahead of the morning's promotion so the promoted build reports 0.9.0.0. The prose sections
> marked *Docs* are written by Docs before the tag; the tag and the GitHub release follow PPM's
> re-check list on the served build (Exec's order, 09:14). Until the tag exists, the version
> mechanics below are the plan, not the record.

## Summary

0.9.0.0 closes the MVP milestone and opens the invitation-only private beta. Since v0.8.14.0
(2026-09-23) main took 1,138 code commits (`services/`, `web/`, `tests/`, `scripts/`, `alembic/`)
and 361 issues closed, including the whole of milestone 5 (MVP: 1,291 closed, 0 open). Seven
Alembic migrations ship in this range (listed under Upgrade). *Docs: one paragraph on the theme.*

## What's New (user-facing)

*Docs: rewrite for this release from the closed-issue list `gh issue list --state closed --search
"closed:>=2026-09-23" --limit 1000` and the omnibus logs 09-23 → 10-31. Organize by theme; each
item links its issue. Do not carry v0.8.14.0's bullets.*

## Under the hood

*Docs, with Lead's list: routing-stack ratchets (dispatch sites, extraction patterns, mypy
ceilings), the hosted MCP server (`mcp.pipermorgan.ai`, OAuth, `what_piper_knows_about_me`), the
rule-7 screening harness, the landing gate.*

## Known limitations (beta)

*Docs: from `gh issue list --label bug --state open` and `docs/ALPHA_KNOWN_ISSUES.md`, rewritten
for beta testers. Include: the connectors offered in beta are GitHub and Google Calendar only;
the MCP connector is private-beta work, not on the MVP path.*

## Version mechanics

- Version string `0.9.0.0`: the four-part form used since v0.8.9.2 (`v0.8.11.0` … `v0.8.14.0`);
  0.9 is the line reserved for the beta (milestone-gated on MVP, decisions.log 2026-08-30).
- `VERSION` and `pyproject.toml` at `0.9.0.0` (`scripts/check-version-consistency.py`: OK).
- Cut commit: the `main` commit carrying this bump; the tag `v0.9.0.0` goes on it, or on a later
  `main` tip if fixes land between the bump and the tag (the tag names the build PPM's re-checks
  passed on, not an earlier one).
- Deploys come from `origin/main`; `production` was retired 2026-09-29. Promotion to alpha and
  beta is xian's dispatch under the standing grant; the beta letters go first.
- Parity gate at the bump: `scripts/check-release-parity.sh origin/main` → PARITY OK (09:25).

## Upgrade

Hosted: nothing to do; the promotion carries it. `/health` on alpha, beta and the MCP app reports
`version: 0.9.0.0` once each is deployed from a commit at or after the bump.

Local: `git pull && alembic upgrade head`. Migrations since v0.8.14.0:
`a1599admin` (changed), `n1462mcpt_mcp_access_tokens`, `o1462oaut_mcp_oauth_as`,
`p1522drop_drop_action_humanizations`, `q2009nn_owner_id_not_null`,
`r2013kgnn_knowledge_owner_not_null`, `s2014items_base_item_has_list`.
