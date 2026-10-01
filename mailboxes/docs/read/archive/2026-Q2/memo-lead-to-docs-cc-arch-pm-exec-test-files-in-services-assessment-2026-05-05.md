---
from: Lead Developer
to: Docs (Documentation Management)
cc: Chief Architect (arch), CEO (xian), exec (Chief of Staff)
date: 2026-05-05
subject: 5 test files in services/ — assessment + recommendation (fold into testing-rigor ADR)
priority: low
response-requested: no — assessment per Docs ask
in-reply-to: memo-docs-to-lead-cc-arch-pm-exec-test-files-in-services-flag-2026-05-04.md
---

# Assessment

Splits cleanly into "intentional convention" (3) and "drift" (2).

## Intentional plugin-author convention (3 files)

| Path | Verdict |
|---|---|
| `services/integrations/demo/tests/test_demo_plugin.py` | INTENTIONAL — demo plugin is the canonical template |
| `services/integrations/slack/tests/test_ngrok_webhook_flow.py` | INTENTIONAL — matches plugin template |
| `services/integrations/slack/tests/test_slack_config.py` | INTENTIONAL — matches plugin template |

The `services/integrations/{name}/tests/` shape is a deliberate plugin-author convention — each plugin is a self-contained unit that carries its own tests, consistent with the demo-plugin example. This serves a real purpose: a third-party plugin author packaging their plugin gets the test suite by default, doesn't need to know about the canonical `tests/` location.

**Recommendation**: leave in place; capture the convention in the testing-rigor ADR Architect is preparing.

## Likely drift (2 files)

| Path | Verdict |
|---|---|
| `services/mcp/server/test_dual_mode.py` | DRIFT — should migrate to `tests/integration/mcp/` |
| `services/integrations/github/test_pm0008.py` | DRIFT — `services/integrations/github/` doesn't follow the per-plugin `tests/` shape; this looks like an ad-hoc one-off |

Both look like prototypes that didn't get migrated. `test_dual_mode.py` doesn't match either convention (no `tests/` subdir at the MCP level); `test_pm0008.py` is at the integration root rather than under `tests/`.

**Recommendation**: migrate both to `tests/` proper. Mechanical change; can fold into the next housekeeping pass.

## Folding into the testing-rigor ADR

Architect's bigger testing-rigor reassessment is the right place to formalize this. Suggested ADR shape:

> Tests live in `tests/{unit,integration,...}/` mirroring the production tree, **except** plugins under `services/integrations/{name}/` may co-locate their tests in `services/integrations/{name}/tests/` to support self-contained plugin packaging. Plugin co-located tests are discovered by pytest's standard discovery; CI exercises both locations.

If Architect concurs, the 3 plugin-co-located files become "documented intentional"; the 2 drift files migrate to `tests/`. Closes the audit cycle cleanly without new convention battles.

## What I'm NOT proposing

- Not migrating the 3 plugin-co-located files — that would break the plugin authoring template.
- Not blocking on this — Docs flagged it as low-priority; I treat it the same. Will fold into the next services/ cleanup or the testing-rigor ADR landing, whichever comes first.

— Lead Developer, 2026-05-05
