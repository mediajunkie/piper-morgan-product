"""#1435: list/todo metadata must survive the domain -> DB constructor.

Regression: ListDB.from_domain / TodoDB.from_domain passed ``metadata=`` to the
declarative constructor. SQLAlchemy ACCEPTS that kwarg (every declarative class
has ``metadata`` as its class-level MetaData attribute), binds it as a plain
instance attribute mapped to no column, and silently drops it on flush — so
every list/todo save discarded its metadata with no exception anywhere
(census B3, sprint #1424).

These tests pin the constructor-level mapping (where the drop happened) and the
full domain -> DB -> domain round-trip, no database required.
"""

from services.database.models import ListDB, TodoDB
from services.domain.models import List as DomainList
from services.domain.models import Todo as DomainTodo

META = {"source": "test-1435", "flags": {"pinned": True}}


def test_list_metadata_reaches_the_mapped_column():
    lst = DomainList(name="census list", metadata=dict(META))
    db_obj = ListDB.from_domain(lst)
    assert db_obj.list_metadata == META


def test_list_metadata_round_trips():
    lst = DomainList(name="census list", metadata=dict(META))
    assert ListDB.from_domain(lst).to_domain().metadata == META


def test_todo_metadata_reaches_the_mapped_column():
    todo = DomainTodo(text="census todo", metadata=dict(META))
    db_obj = TodoDB.from_domain(todo)
    assert db_obj.list_metadata == META


def test_todo_metadata_round_trips():
    todo = DomainTodo(text="census todo", metadata=dict(META))
    assert TodoDB.from_domain(todo).to_domain().metadata == META
