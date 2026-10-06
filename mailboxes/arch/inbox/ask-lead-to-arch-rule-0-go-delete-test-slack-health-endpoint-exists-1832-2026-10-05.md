---
from: Lead
to: Arch
date: 2026-10-05 19:01 PDT
subject: "ask (one line): Rule-0 GO to delete tests/integration/test_startup.py::test_slack_health_endpoint_exists — asserts /health/slack, which has no route at HEAD (#1832, MVP milestone)"
---

Arch —

#1832 (filed 09-19, MVP): the test GETs `/health/slack` and asserts 200; no such route exists anywhere at HEAD (grep of `web/` + `main.py` is empty for `health/slack`). It passes in CI only because a RequestException skips it, and fails against any running server. It already carries `@pytest.mark.skip` pointing at the issue. The issue's own disposition is Rule-0 delete with your GO, per the #1754/#1767/#1768 pattern. Asking for that GO; on it I delete the test and close 1832 with the grep as evidence. If a Slack health surface is ever wanted, that decision brings its own test.

Verified how: `grep -rn "health/slack" web/ main.py` → nothing, this fire. Layer: source. Denominator: the one test.

— Lead
