"""#2293 (found 2026-11-05 answering CXO on #2219): todo priority is stored as text, and
``priority.desc()`` sorted it alphabetically (urgent, medium, low, high), so every "high"
todo came after "medium" and "low" in the list and in "what's my next todo?".
``PRIORITY_RANK`` orders urgent, high, medium, low; every sort uses it."""

import subprocess
from pathlib import Path

from sqlalchemy import Column, MetaData, String, Table, create_engine, insert, select

from services.database.models import TodoDB
from services.repositories.todo_repository import PRIORITY_RANK

ROOT = Path(__file__).resolve().parents[3]


def _sorted(values):
    """Run the real rank expression against a table with the todos' name and column."""
    engine = create_engine("sqlite://")
    meta = MetaData()
    table = Table(TodoDB.__tablename__, meta, Column("priority", String(6)))
    meta.create_all(engine)
    with engine.begin() as conn:
        conn.execute(insert(table), [{"priority": v} for v in values])
        rows = conn.execute(select(table.c.priority).order_by(PRIORITY_RANK.asc())).all()
    return [r[0] for r in rows]


def test_high_comes_before_medium_and_low():
    assert _sorted(["low", "high", "medium", "urgent"]) == ["urgent", "high", "medium", "low"]


def test_an_unknown_value_sorts_last():
    assert _sorted(["odd", "low", "high"]) == ["high", "low", "odd"]


def test_no_query_orders_by_the_priority_text():
    hits = subprocess.run(
        ["git", "grep", "-nE", r"priority\.(desc|asc)\(\)", "--", "services", "web"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    code = [h for h in hits if "``priority.desc()``" not in h]
    assert not code, code
