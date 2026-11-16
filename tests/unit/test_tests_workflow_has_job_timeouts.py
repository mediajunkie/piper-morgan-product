"""Every job in the Tests workflow has a time limit.

On main a Tests run is never cancelled by a newer push, so a stuck job with no limit holds
main's verdict (and the promotion gate that reads it) until GitHub's 6-hour default. On
2026-11-16 run 43945328322 spent 36 minutes in its checkout step and held a queued run for
54 minutes; nothing bounded how long that could have gone on.
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
