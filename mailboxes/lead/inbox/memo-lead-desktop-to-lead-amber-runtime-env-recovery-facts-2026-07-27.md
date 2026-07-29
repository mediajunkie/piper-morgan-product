---
from: Lead Developer (Desktop predecessor, standing by)
to: Lead Developer (Amber successor)
cc: xian (ceo)
date: 2026-07-27
subject: "venv/runtime recovery facts — everything environment-shaped that lived in my head, verified against 44 waves of running this suite"
---

Successor — PM says you're mid-venv-recreation. Here is every environment fact I actually used, so you don't rediscover them the slow way. All VERIFIED on the Desktop seat unless marked.

## Python + deps
- Desktop venv ran **Python 3.12** (CI runs 3.11.15 — both fine). Single dep source: `pip install -r requirements.txt`.
- The install is LONG and that's normal: `sentence-transformers==4.1.0` pulls torch; `chromadb==0.4.22`. Don't interrupt it.
- After install, the definitive "venv works" check is collection:
  `python -m pytest tests/ -m "not llm" --collect-only -q -o addopts="--ignore=tests/archive --ignore=services/integrations --ignore=dev/ --import-mode=importlib"`
  → expect **~11,111 collected / 11,481** (370 llm-lane deselected). If collection is clean, the venv is right.

## The two env rules that masquerade as other bugs
1. **ALWAYS strip ANTHROPIC_* for server/test runs** — the Claude Code shell exports an EMPTY `ANTHROPIC_API_KEY` that shadows `.env` (python-dotenv won't override) → every LLM call fails as a fake "connection error":
   `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 python -m pytest …`
2. **POSTGRES_PORT=5433** on every test/server invocation (the dev compose maps 5433).

## Services (my §5-Q3 — VERIFY these exist on Amber before the first sweep)
- Postgres 16 on **5433**: `pg_isready -h localhost -p 5433` · stand up via `docker compose up -d` + `alembic upgrade head` if absent.
- Redis on **6379** (usage-cap middleware fail-closes 503 without it — you'll see `capacity_check_unavailable` on login-path tests if it's missing).
- ChromaDB on **8000** (only llm-lane/doc-ingestion tests need it live; the "not llm" sweep does not).

## Keys (keyed-vs-keyless changes which failures are REAL)
- conftest auto-loads OPENAI/ANTHROPIC from the **macOS keychain** (`KeychainService`, service `piper-morgan`, accounts get an `_api_key` suffix — use KeychainService, never the `security` CLI, to store) + GITHUB_TOKEN from `gh` CLI.
- **Keyless is a legitimate state** — it's what CI runs. But know the tells: keyed-local-pass/keyless-fail = eager keyed construction or llm-lane test (see my handoff §4.4). If your seat is keyless, your local sweep will differ from my recorded local baselines but should MATCH CI's.

## The instruments
- Full sweep: same command as collection minus `--collect-only`, `--tb=no`, pipe to a file; then `python scripts/check_fullsuite_backlog.py <file>` for the gate verdict. Local sweep ~10-12 min on the Studio (BELIEVED — was 10-12 on the M-series laptop).
- Single-file runs need `-o addopts="--import-mode=importlib"` or imports break (`No module named 'services.auth'` is the tell you forgot it).
- `./scripts/fix-newlines.sh` before committing. `fly` CLI for deploys (auth carry = my §5-Q2 — verify before you need it).

## State you inherit (pointers, all on main)
Backlog 56 (`scripts/known_failing_backlog.tsv`) — 16 spatial-held (PM review), 15 named flaky, ~25 gated singles; #1452 comments narrate everything. Beta v28 healthy. Beta band: #1393/#1394 await the #1386 re-run (Exec), #1395 ratification. My handoff REFRESH (`dev/active/lead-handoff-2026-07-21.md`) has §4/§6; carry-forward has your Amber-specific notes (both-shape 2a-bis probe, sync-pm-local no-op).

I'm standing by on the Desktop seat for the transition window — if something doesn't match this memo, that's a finding, not your error; mail or have PM relay.

— your predecessor
