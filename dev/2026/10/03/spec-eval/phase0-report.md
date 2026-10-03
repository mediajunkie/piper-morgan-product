# Phase 0 report (2026-10-03)

## Snapshot
See `snapshot.md`. Product `a1918561`, website `16dfe5fa`, skunkworks `829746f3`.
The code-only export is at `/home/user/snapshot-code`, outside the repo and container-local. It is 4,523
files and excludes `docs/ dev/ mailboxes/ knowledge/ rag/ .claude/ .serena/` and all `*.md`.

## Feasibility gate: PASSED, with gaps. The app runs here; LLM paths do not.
| Step | Result | Layer |
|---|---|---|
| Docker daemon | Started by hand (`dockerd`). Earlier report of "down" meant not started, not unavailable | ran |
| `docker compose up` | **Failed**: Docker Hub 429 rate limit through the egress proxy (traefik, postgres:15) | ran |
| Postgres | Fallback: apt `postgresql` **16** (repo pins 15) on port 5433 with the repo's dev creds | ran |
| Redis | Local `redis-server` on port 6379 | ran |
| venv + `pip install -r requirements.txt` | OK, Python 3.11.15 | ran |
| `alembic upgrade head` | OK, all migrations applied to an empty DB | ran |
| `main.py` boot | OK. `/health` returns 200 `{"version":"0.8.14.0","git_sha":"unknown"}`; `/` returns 302 | ran-server |
| Boot warnings | No LLM providers; no `ENCRYPTION_MASTER_KEY`, so credential writes raise; JWT dev fallback; **"Schema drift detected"** (CrossDialectUUID vs uuid on a fresh migrate); "Some service configurations are invalid"; duplicate process-handler registration | ran-server |
| Unit suite | **11,471 passed / 24 failed / 283 skipped** in 6m06s, run serially (log: `metrics/unit-run-2026-10-03.log`). Failures: 16 in `test_multi_intent.py` (classifier returns `greeting` where a calendar intent is expected), 7 in `test_spend_free_canonical_ratchet_1818.py`, 1 Slack spatial. **Not yet triaged** into environment-caused (no LLM key / Chroma) vs real; B does the triage, possibly with the ab-a-isolation skill | ran-tests |
| `/checkup prompt-audit` | CLI 2.1.288 is present (≥ 2.1.283). **Not yet run.** Running it means a nested `claude -p` that costs credit. Deferred to D-measure, and the nested-auth path is unverified | — |

**Consequences for the plan:**
- B runs live (suite results).
- C runs **live for non-LLM surfaces** (routes, UI, auth, settings) and treats LLM-backed surfaces as
  unobservable unless PM adds a spend-capped test key as an environment variable. That's a decision for PM.
- ChromaDB, Temporal and the GitHub MCP sidecar are not available. Surfaces that need them go on the
  unobservables list.

## Process note (my error, caught)
My first unit run overrode `addopts` and dropped `--import-mode=importlib`. That produced 34 false
collection errors. `pytest.ini` warns about exactly this. I caught it and re-ran correctly; the false
result was not used anywhere.

## Cost calibration
PM's usage page showed **$4 spent** at plan v0.3. That covered the main context plus one ~94k-token Opus audit
subagent. Phase 0 added almost no model spend: it was shell work.

## Deliverable side-effect
`cloud-env-setup-script.sh` is a tested setup script for cloud sessions (PM asked whether a cloud
session can have a test environment).
