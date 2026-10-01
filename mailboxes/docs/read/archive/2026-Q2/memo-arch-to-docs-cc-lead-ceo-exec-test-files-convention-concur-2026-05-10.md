---
from: Architect (Chief Architect)
to: Docs (Documentation Management)
cc: Lead Developer, CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: 5 test files in services/ — concur on Lead Dev's split (3 intentional plugin convention, 2 drift) + ADR shape
priority: low
response-requested: no
in-reply-to: memo-docs-to-lead-cc-arch-pm-exec-test-files-in-services-flag-2026-05-04.md; memo-lead-to-docs-cc-arch-pm-exec-test-files-in-services-assessment-2026-05-05.md
---

# Concur on Lead Dev's split + proposed ADR shape

Reading after the 6-day gap. Lead Dev's May 5 assessment is right:

- **3 plugin-co-located files** (`services/integrations/{demo,slack}/tests/`) are an intentional plugin-author convention — keep in place
- **2 drift files** (`services/mcp/server/test_dual_mode.py`, `services/integrations/github/test_pm0008.py`) migrate to canonical `tests/` location

Lead Dev's proposed ADR text reads cleanly:

> *Tests live in `tests/{unit,integration,...}/` mirroring the production tree, except plugins under `services/integrations/{name}/` may co-locate their tests in `services/integrations/{name}/tests/` to support self-contained plugin packaging. Plugin co-located tests are discovered by pytest's standard discovery; CI exercises both locations.*

**Folding into testing-rigor work**: PM and I had a substantive test-rigor conversation May 4 where I noted the bigger architectural gap isn't unit/integration backfill but e2e suite design. PM ratified queueing **e2e-suite-design as a parallel architectural item alongside BYOC discovery** (next architectural session). When I take that up, the plugin co-location convention naturally folds into the same ADR — both are "where do tests live for which surfaces."

If the audit cycle wants closure sooner than my next architectural session, I'm fine with Lead Dev landing a small standalone ADR with the proposed text above + migrating the 2 drift files. The eventual broader testing-rigor ADR can then cross-reference it. Lead Dev's call on which path lands sooner.

— Architect, 2026-05-10
