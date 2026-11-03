---
from: Janus
to: Lead Dev
cc: CIO, Exec
date: 2026-11-02
subject: Alpha promote blocked: Tests on staging's sha failed on SHRINK-LOCK
---

xian dispatched the alpha promote at 16:50 PT (fly-deploy run 41555701261). The gate refused it correctly because Tests on staging's sha fc31f4a (CIO's ruff format of registry-plist-drift.py) was still running. That Tests run (41550819343) then ended in failure at 16:53.

The cause is the burn-down gate's SHRINK-LOCK, not new breakage. One backlog entry now passes:

    tests/integration/test_slack_spatial_adapter_integration.py::TestSlackSpatialAdapter::test_create_spatial_event_from_slack   (triage, line 29 of scripts/known_failing_backlog.tsv)

The gate wants it removed from the TSV. The other 21 failed and 18 errors are already in the backlog (backlog 55: fixture 11, triage 26, flaky 18).

Ask: remove that line (or recategorize it as flaky if you judge its pass a fluke), push, and let Tests go green on the new head. Staging will then serve a green sha. Once that's done, tell me and I'll have xian dispatch the promote again. He is holding for it.

Janus
