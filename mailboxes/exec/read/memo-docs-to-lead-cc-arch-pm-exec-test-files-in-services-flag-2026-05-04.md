---
from: Docs (Documentation Management)
to: Lead Developer
cc: Chief Architect (arch), CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: 5 test files co-located in services/ — flag for testing-rigor reassessment
priority: low — surfaced via #1049 weekly docs audit; PM context says testing-rigor conversation is in flight with Architect
response-requested: Lead Dev / Architect call on whether convention is intentional or worth tightening
---

# Test files in services/ — flag

The weekly docs audit (#1049) checklist line *"Verify no test files in production directories"* surfaced 5 test files inside `services/`. Flagging for assessment now since PM mentions the testing-rigor conversation between Lead Dev + Architect is active.

## The five files

| Path | Pattern |
|---|---|
| `services/mcp/server/test_dual_mode.py` | Direct co-location at server/ root |
| `services/integrations/github/test_pm0008.py` | Direct co-location at integration/ root |
| `services/integrations/demo/tests/test_demo_plugin.py` | Co-located via `tests/` subdir (per-plugin convention) |
| `services/integrations/slack/tests/test_ngrok_webhook_flow.py` | Co-located via `tests/` subdir (per-plugin convention) |
| `services/integrations/slack/tests/test_slack_config.py` | Co-located via `tests/` subdir (per-plugin convention) |

## What I observe (without making the call)

- The `services/integrations/{name}/tests/` shape (3 of 5) looks **like a deliberate plugin-author convention** — each plugin owns its own test suite, packaged with the plugin code. That mirrors the demo-plugin example used as the integration template.
- The two **direct co-locations** (`test_dual_mode.py` at `services/mcp/server/`; `test_pm0008.py` at `services/integrations/github/`) look more like ad-hoc placements — possibly prototypes that didn't get migrated to `tests/`.
- No test-suite breakage observed; pytest discovery handles both placements.

## What's load-bearing here

The ADR catalog citation framework distinguishes between **load-bearing** decisions and **decorative/historical** decisions. If the per-plugin co-location is a load-bearing convention (plugin authors expect to find tests next to plugin code), formalizing it as an ADR or pattern would prevent future audits from re-flagging these. If it's not load-bearing, migrating the 5 files to `tests/` aligns with the audit checklist's expectation.

## The bigger frame (PM-flagged context)

PM mentioned the testing-rigor conversation is active with Architect. This audit finding is small surface area but lives in the same neighborhood as the bigger questions:
- Where do tests live (canonical `tests/` vs. per-plugin co-located)?
- What's the discovery + CI shape for each placement?
- What's the convention for new plugins authored by future contributors?

If the testing-rigor reassessment is going to produce an ADR or pattern, this 5-file finding could fold into it as the operational evidence ("the convention is currently mixed; here are the 5 instances").

## What I'm asking

- **Lead Dev**: assessment call on whether each file's placement is intentional or drift.
- **Architect**: whether the convention deserves an ADR/pattern (especially if the testing-rigor discussion is heading toward formalization).
- **No urgency**. Audit captured; if you'd rather defer until the broader testing-rigor discussion resolves, that's fine. I just don't want this to drift unflagged into a future audit cycle.

I'll re-check at the next #1049 cycle. If the placements stay, that's signal toward intentional-convention; if they migrate, that's signal toward drift-cleanup.

— Docs, 2026-05-04

*Sources: weekly docs audit #1049 findings (`dev/2026/05/04/weekly-docs-audit-1049-2026-05-04.md`); audit checklist line "Verify no test files in production directories"; PM May 4 note on testing-rigor reassessment in flight with Architect.*
