# Testing Strategy

**Last Updated**: October 31, 2026 (rewritten against the current code, issue #1904)

## Overview

Piper Morgan uses pytest. Tests are grouped with markers declared in `pytest.ini`. CI and local runs select by marker.

## Markers

The markers declared in `pytest.ini`:

| Marker | Meaning |
|---|---|
| `smoke` | Critical path tests, meant to run in under 5 seconds total |
| `unit` | Fast tests, meant to run in under 30 seconds total |
| `integration` | Tests that may take up to 2 minutes |
| `performance`, `benchmark`, `regression` | Performance, benchmark and degradation checks |
| `contract` | Plugin interface compliance |
| `llm` | Needs a real LLM API call, skipped when no keys are available |
| `github` | Needs a GitHub token, skipped without `GITHUB_TOKEN` |
| `transition` | State transition tests (fresh install, setup flows) |
| `e2e` | End-to-end HTTP tests with real services and a database |
| `live` | Live-verification tests against a real server subprocess, opt-in with `PIPER_LIVE=1` |

`pytest.ini` also sets `pythonpath = .` (no `PYTHONPATH` prefix needed), `asyncio_mode = auto`, and `testpaths = tests`.

Its `addopts` include `-x --maxfail=1` (stop at the first failure) and `--import-mode=importlib`. If you override `addopts` with `-o addopts=...`, keep `--import-mode=importlib`. The file comments say that dropping it breaks collection across about 20 files because test basenames repeat across directories.

## Running tests

```bash
python -m pytest tests/unit/ -v            # unit directory (from CLAUDE.md quick reference)
python -m pytest -m smoke -q               # critical path
python -m pytest tests/ -m "not llm" -q    # everything that needs no LLM key
python -m pytest tests/ -m llm -v          # LLM tests only
```

Tests need Postgres on port 5433 (`docker compose up -d && alembic upgrade head`). The smoke job in CI runs against a Postgres service, so smoke tests include database-backed tests.

## What CI runs

Workflow: `.github/workflows/test.yml`, triggered by pushes and pull requests that touch code paths (`services/`, `tests/`, `web/`, `alembic/`, `scripts/`, top-level `*.py`, requirements files, workflows). Docs-only changes do not trigger it.

1. **Smoke Tests** job: `alembic upgrade head`, then `python -m pytest -m smoke -q --tb=short` with `addopts` overridden so every failure shows, not just the first.
2. **Full Test Suite** job (needs smoke): `python -m pytest tests/ -m "not llm" -q --tb=no`, then `scripts/check_fullsuite_backlog.py` judges the result against a known-failure backlog. A new failure outside the backlog fails the job.

CI uses Python 3.11, Postgres 16 and Redis 7 service containers, and test-only keys committed in the workflow. No real LLM keys exist in CI, so `llm` tests skip.

Other workflows that run tests or checks: `security-tests.yml`, `architecture-enforcement.yml`, `router-enforcement.yml`, `frontend-tests.yml`, `windows-test.yml`, `e2e-aaxt.yml`, `lint.yml`. Read each file for its trigger and scope. A smoke-test runbook is at [ci-cd-smoke-test-runbook.md](internal/operations/ci-cd-smoke-test-runbook.md).

Deploys are separate. Every push to `main` deploys staging through `.github/workflows/fly-deploy.yml`, and alpha is promoted from a tested staging build. See [deploy-environments-and-release-train.md](internal/operations/deploy-environments-and-release-train.md).

## LLM tests

`tests/conftest.py` auto-skips tests marked `llm` or `github` when the matching keys are absent (it checks for OpenAI or Anthropic keys, and the environment variables work). When keys are present, `llm` tests get an injected fixture that binds a spend key for the test, because the server no longer holds a global LLM credential: each request builds its client from the acting user's bound key.

Providers in `services/llm/config.py` (`LLMProvider`): Anthropic, OpenAI and Gemini. Model ids in `LLMModel`:

| Provider | default | heavy | light |
|---|---|---|---|
| Anthropic | `claude-sonnet-4-6` | `claude-opus-4-8` | `claude-haiku-4-5` |
| OpenAI | `gpt-4o` | `gpt-4o` | `gpt-4o-mini` |
| Gemini | `gemini-2.5-flash` | `gemini-2.5-pro` | `gemini-2.5-flash` |

The provider for a request is chosen at runtime from user configuration, not pinned per task. For how selection and models work, read [llm-configuration.md](internal/architecture/current/llm-configuration.md) and `services/llm/config.py`. Model ids change often, so treat the config file as the source of truth.

Constructing `LLMClient` (`services/llm/clients.py`) reads no credential, so importing it in a test never needs a key.

Example of marking a test:

```python
import pytest

@pytest.mark.llm
async def test_llm_classification():
    ...
```

To simulate CI locally, run `python -m pytest tests/ -m "not llm"`.

## Troubleshooting

- **A test passes locally and fails in CI.** Check that it is marked `llm` if it needs a key, that it does not read an uncommitted local file, and that it does not depend on a local database state. Simulate CI with `-m "not llm"`.
- **Collection errors after editing `addopts`.** Restore `--import-mode=importlib`.
- **Stops after one failure.** That is `-x --maxfail=1` from `pytest.ini`. Override `addopts` (keeping the import mode) to see all failures.
- **App refuses to start outside pytest.** It needs `JWT_SECRET_KEY` set. pytest supplies a fake one from `tests/conftest.py`.

## References

- `pytest.ini`
- `tests/conftest.py`
- `.github/workflows/test.yml`
- `services/llm/config.py`, `services/llm/clients.py`
- `tests/intent/test_constants.py`

## Not verified here

- The per-tier model table was read from `services/llm/config.py` but no call was made to any provider.
- The unit and integration time budgets come from the marker descriptions in `pytest.ini`. Actual run times were not measured.
- Whether `tests/conftest.py` skips on the key sources named above for every key type (the conftest was only skimmed, not traced end to end).
- The contents and current accuracy of the other workflows listed (only their file names were confirmed).
