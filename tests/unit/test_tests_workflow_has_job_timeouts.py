"""Every job in the Tests workflow has a time limit.

On main a Tests run is never cancelled by a newer push, so a hung job with no limit holds
main's verdict (and the promotion gate that reads it) until GitHub's 6-hour default. That
happened on 2026-11-16: run 43945328322 hung in the full-suite step with a run queued behind it.
"""

from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "test.yml"


def test_every_job_has_a_timeout_well_under_githubs_default():
    jobs = yaml.safe_load(WORKFLOW.read_text())["jobs"]
    assert jobs, "no jobs found in the Tests workflow"
    for name, job in jobs.items():
        limit = job.get("timeout-minutes")
        assert isinstance(limit, int), f"job {name!r} has no timeout-minutes"
        assert 0 < limit <= 60, f"job {name!r} may run {limit} minutes before it is stopped"
