#!/usr/bin/env python3
"""
Canonical Retest Fixtures — Issue #989 CANONICAL-FIXTURES.

Creates a "warmed-up" canonical-test user fixture with deterministic
project + todo data so the canonical retest can exercise context-aware
queries against real user data rather than the fresh-account ceiling.

Background (from #989 + #950 closure):
- The fresh canonical-test user has no projects, no calendar, no history.
- Identity / Status / Priority queries that depend on user-specific data
  show Context dimension stuck at 1 (LLM has nothing specific to reference).
- That ceiling is a test-fixture bug, not a prompt or assembler bug.

What this script creates:
- User: ``canonical-test-warm`` (separate from canonical-test so the fresh
  fabrication-guard path stays clean)
- 3 projects: Alpha Migration / Beta Onboarding / Infrastructure Reliability
- 7 todos: mixed priorities and statuses across the project surface

What's deferred (out of scope for this issue or simpler-later):
- Calendar fixtures (#989 marked as optional)
- Conversation history (would need session-replay infrastructure)
- Trust stage manipulation (separate concern; default is fine)
- Mock GitHub repo data (separate fixture would touch external integration)

Usage:
    # Ensure server is running on localhost:8001
    POSTGRES_PORT=5433 ./venv/bin/python \\
        dev/2026/05/24/canonical-fixtures-warm-user-2026-05-24.py

Then run the canonical retest against the warmed user:
    POSTGRES_PORT=5433 ./venv/bin/python \\
        dev/2026/04/11/canonical-retest-m1.py --warm-user

Idempotency:
    Re-running the fixture script checks for existing data by name (project)
    and title (todo) and skips creation if already present. To force a clean
    rebuild, pass ``--reset`` (deletes existing fixture data first).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import requests

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

BASE_URL = "http://localhost:8001"
LOGIN_ENDPOINT = f"{BASE_URL}/api/v1/auth/login"   # API-v1 prefix (verified 2026-05-25)
SETUP_ENDPOINT = f"{BASE_URL}/api/v1/setup"        # for create-user
WARM_USERNAME = "canonical-test-warm"
WARM_PASSWORD = "canonical-test-warm-2026"


# --- Fixture data (deterministic; idempotent matching by name/title) ---

PROJECTS = [
    {
        "name": "Alpha Migration",
        "description": (
            "Migrating the data layer from legacy v1 schema to the new "
            "normalized v2 schema. Active development; 60% complete."
        ),
    },
    {
        "name": "Beta Onboarding",
        "description": (
            "User onboarding flow redesign with progressive disclosure. "
            "Discovery phase; UX research ongoing."
        ),
    },
    {
        "name": "Infrastructure Reliability",
        "description": (
            "SLO improvement initiative — observability, retry semantics, "
            "and graceful-degradation patterns across the service mesh."
        ),
    },
]

TODOS = [
    {
        "title": "Review Alpha Migration schema-v2 PR #4421",
        "description": "Final sign-off on the v2 schema PR before merge.",
        "priority": "high",
        "status": "pending",
    },
    {
        "title": "Draft Beta Onboarding research synthesis",
        "description": "Consolidate 8 user interviews into key findings doc.",
        "priority": "high",
        "status": "in_progress",
    },
    {
        "title": "Update Infrastructure SLO dashboard",
        "description": "Add p99 latency tiles for the new retry middleware.",
        "priority": "medium",
        "status": "pending",
    },
    {
        "title": "Plan M3 sprint kickoff agenda",
        "description": "Cross-team sprint kickoff prep; align on goals.",
        "priority": "medium",
        "status": "pending",
    },
    {
        "title": "Sync with team lead on hiring pipeline",
        "description": "Review candidate slate and discuss next steps.",
        "priority": "low",
        "status": "pending",
    },
    {
        "title": "Close out Q1 retrospective notes",
        "description": "Document Q1 learnings and circulate to leadership.",
        "priority": "low",
        "status": "completed",
    },
    {
        "title": "Renew SSL certificates for staging",
        "description": "Expires in 14 days; rotate via the runbook.",
        "priority": "high",
        "status": "pending",
    },
]


# --- HTTP helpers ---

def ensure_user(session: requests.Session) -> bool:
    """Idempotent test-user creation."""
    create_url = f"{SETUP_ENDPOINT}/create-user"
    resp = session.post(
        create_url,
        json={
            "username": WARM_USERNAME,
            "email": f"{WARM_USERNAME}@piper-morgan.local",
            "password": WARM_PASSWORD,
            "password_confirm": WARM_PASSWORD,
        },
    )
    if resp.status_code == 200:
        print(f"  Created warm user {WARM_USERNAME}")
        return True
    if resp.status_code == 400 and "exist" in resp.text.lower():
        print(f"  Warm user {WARM_USERNAME} already exists (OK)")
        return True
    print(f"  ensure_user note: {resp.status_code} {resp.text[:200]}")
    return True


def login(session: requests.Session) -> Optional[str]:
    """Authenticate and store bearer token on session."""
    resp = session.post(
        LOGIN_ENDPOINT,
        data={"username": WARM_USERNAME, "password": WARM_PASSWORD},
    )
    if resp.status_code != 200:
        print(f"  LOGIN FAILED: {resp.status_code} {resp.text[:200]}")
        return None
    try:
        data = resp.json()
        token = data.get("token") or data.get("access_token")
        if not token:
            print(f"  LOGIN FAILED: no token in response: {data}")
            return None
        session.headers["Authorization"] = f"Bearer {token}"
        print(f"  Logged in as {WARM_USERNAME}")
        return token
    except Exception as e:
        print(f"  LOGIN FAILED: {e}")
        return None


# --- Fixture operations ---

def list_existing_projects(session: requests.Session) -> list[dict]:
    """Return the warm user's existing projects (name lookup)."""
    resp = session.get(f"{BASE_URL}/api/v1/projects")
    if resp.status_code != 200:
        print(f"  list_existing_projects: {resp.status_code} {resp.text[:120]}")
        return []
    payload = resp.json()
    # API returns a dict with 'projects' key OR a list directly depending on shape;
    # handle both defensively.
    if isinstance(payload, dict):
        return payload.get("projects", []) or payload.get("data", []) or []
    if isinstance(payload, list):
        return payload
    return []


def list_existing_todos(session: requests.Session) -> list[dict]:
    """Return the warm user's existing todos (title lookup)."""
    resp = session.get(f"{BASE_URL}/api/v1/todos")
    if resp.status_code != 200:
        print(f"  list_existing_todos: {resp.status_code} {resp.text[:120]}")
        return []
    payload = resp.json()
    if isinstance(payload, dict):
        return payload.get("todos", []) or payload.get("data", []) or []
    if isinstance(payload, list):
        return payload
    return []


def create_project(session: requests.Session, project: dict) -> Optional[dict]:
    """POST /api/v1/projects."""
    resp = session.post(f"{BASE_URL}/api/v1/projects", json=project)
    if resp.status_code in (200, 201):
        return resp.json()
    print(
        f"  create_project '{project['name']}' FAILED: "
        f"{resp.status_code} {resp.text[:200]}"
    )
    return None


def create_todo(session: requests.Session, todo: dict) -> Optional[dict]:
    """POST /api/v1/todos."""
    resp = session.post(f"{BASE_URL}/api/v1/todos", json=todo)
    if resp.status_code in (200, 201):
        return resp.json()
    print(
        f"  create_todo '{todo['title']}' FAILED: "
        f"{resp.status_code} {resp.text[:200]}"
    )
    return None


def delete_project(session: requests.Session, project_id: str) -> bool:
    """DELETE /api/v1/projects/{id} — used only by --reset."""
    resp = session.delete(f"{BASE_URL}/api/v1/projects/{project_id}")
    if resp.status_code in (200, 204):
        return True
    print(f"  delete_project {project_id} FAILED: {resp.status_code} {resp.text[:120]}")
    return False


def delete_todo(session: requests.Session, todo_id: str) -> bool:
    """DELETE /api/v1/todos/{id} — used only by --reset."""
    resp = session.delete(f"{BASE_URL}/api/v1/todos/{todo_id}")
    if resp.status_code in (200, 204):
        return True
    print(f"  delete_todo {todo_id} FAILED: {resp.status_code} {resp.text[:120]}")
    return False


# --- Main ---

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing fixture data before re-creating (clean rebuild)",
    )
    args = parser.parse_args()

    print("=" * 70)
    print(f"Canonical Fixtures — #989 (warm-user setup)")
    print(f"User: {WARM_USERNAME}")
    print(f"Target: {BASE_URL}")
    print(f"Projects: {len(PROJECTS)}, Todos: {len(TODOS)}")
    print("=" * 70)

    session = requests.Session()
    print("\nEnsuring warm user...")
    ensure_user(session)
    print("Authenticating...")
    if not login(session):
        print("FATAL: Cannot authenticate. Aborting.")
        return 1

    if args.reset:
        print("\n--reset: deleting existing fixture data...")
        existing_projects = list_existing_projects(session)
        for p in existing_projects:
            pid = p.get("id")
            if pid:
                delete_project(session, str(pid))
        existing_todos = list_existing_todos(session)
        for t in existing_todos:
            tid = t.get("id")
            if tid:
                delete_todo(session, str(tid))
        print(f"  Deleted {len(existing_projects)} projects + {len(existing_todos)} todos")

    print("\nCreating projects (idempotent — skips if name already exists)...")
    existing_project_names = {p.get("name") for p in list_existing_projects(session)}
    created_projects = 0
    skipped_projects = 0
    for project in PROJECTS:
        if project["name"] in existing_project_names:
            print(f"  [SKIP] '{project['name']}' already exists")
            skipped_projects += 1
            continue
        result = create_project(session, project)
        if result is not None:
            print(f"  [CREATED] '{project['name']}' (id={result.get('id', '?')})")
            created_projects += 1

    print("\nCreating todos (idempotent — skips if title already exists)...")
    existing_todo_titles = {t.get("title") for t in list_existing_todos(session)}
    created_todos = 0
    skipped_todos = 0
    for todo in TODOS:
        if todo["title"] in existing_todo_titles:
            print(f"  [SKIP] '{todo['title']}' already exists")
            skipped_todos += 1
            continue
        result = create_todo(session, todo)
        if result is not None:
            print(f"  [CREATED] '{todo['title']}' (id={result.get('id', '?')})")
            created_todos += 1

    print("")
    print("=" * 70)
    print(f"Summary:")
    print(f"  Projects: {created_projects} created, {skipped_projects} skipped")
    print(f"  Todos:    {created_todos} created, {skipped_todos} skipped")
    print("=" * 70)
    print(
        f"\nNext: run the canonical retest against the warm user:"
        f"\n  POSTGRES_PORT=5433 ./venv/bin/python "
        f"dev/2026/04/11/canonical-retest-m1.py --warm-user"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
