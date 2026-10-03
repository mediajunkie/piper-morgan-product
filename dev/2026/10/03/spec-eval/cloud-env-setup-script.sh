#!/usr/bin/env bash
# Cloud-session setup script for piper-morgan-product (tested 2026-10-03 by Spec in a claude.ai/code container).
# Paste into: cloud environment menu (session title bar) → Edit → Setup script.
# Gets: Postgres on 5433 with the repo's dev creds, Redis on 6379, venv with requirements, migrations at head.
# Does NOT get: Docker Hub images (pulls were 429 rate-limited via the proxy), ChromaDB, Temporal, macOS Keychain,
# an LLM key (add a spend-capped test ANTHROPIC_API_KEY as an environment variable if LLM paths should run),
# ENCRYPTION_MASTER_KEY / JWT_SECRET_KEY (set test values as env vars to exercise credential + auth paths).
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -q postgresql >/dev/null
C=/etc/postgresql/16/main
sed -i "s/^#\?port = .*/port = 5433/" $C/postgresql.conf
service postgresql start
su postgres -c "psql -p 5433 -tc \"select 1 from pg_roles where rolname='piper'\"" | grep -q 1 || \
  su postgres -c "psql -p 5433 -qc \"CREATE USER piper WITH PASSWORD 'dev_changeme_in_production' SUPERUSER;\" -c \"CREATE DATABASE piper_morgan OWNER piper;\""
redis-server --port 6379 --daemonize yes
REPO=${REPO:-/home/user/piper-morgan-product}
python3 -m venv /home/user/venv
/home/user/venv/bin/pip install -q -r "$REPO/requirements.txt"
cd "$REPO" && POSTGRES_PORT=5433 POSTGRES_HOST=localhost POSTGRES_USER=piper \
  POSTGRES_PASSWORD=dev_changeme_in_production POSTGRES_DB=piper_morgan /home/user/venv/bin/alembic upgrade head
# Start server (strip inherited ANTHROPIC_* per CLAUDE.md):
#   env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
#     POSTGRES_PORT=5433 nohup /home/user/venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
# Unit tests: keep --import-mode=importlib if you override addopts (pytest.ini explains why).
