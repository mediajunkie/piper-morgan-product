"""#2386: one machine can hold more than one copy of Piper without sharing a database.

``docker-compose.yml`` used to fix the project name, every container name, the network,
the Postgres volume and every host port. A second clone's ``docker compose up`` therefore
joined the first clone's project and its database. Every name now starts with
``${PIPER_STACK:-piper}`` and the three data services read their host port from a variable.

These tests read the file's text. They start nothing and need no Docker. The render check
(``docker compose config`` with nothing set, identical before and after) is on the issue.
"""

import re
from pathlib import Path

import pytest
import yaml

COMPOSE = Path(__file__).resolve().parents[2] / "docker-compose.yml"
STACK = "${PIPER_STACK:-piper}"
VARIABLE = re.compile(r"\$\{([A-Z_]+):-([^}]*)\}")


@pytest.fixture(scope="module")
def compose():
    return yaml.safe_load(COMPOSE.read_text())


def _rendered(text, env=None):
    env = env or {}
    return VARIABLE.sub(lambda m: env.get(m.group(1), m.group(2)), text)


def test_the_project_network_and_volume_names_carry_the_stack(compose):
    assert compose["name"] == f"{STACK}-morgan-stable"
    assert compose["networks"]["default"]["name"] == f"{STACK}-network"
    assert compose["volumes"]["piper_postgres_data"]["name"] == f"{STACK}_postgres_data_v1"


def test_every_container_name_carries_the_stack(compose):
    names = {svc: body.get("container_name") for svc, body in compose["services"].items()}
    assert len(names) == 7
    for service, name in names.items():
        assert name and name.startswith(f"{STACK}-"), f"{service}: {name!r} is a fixed name"


@pytest.mark.parametrize(
    "service,variable,default,inside",
    (
        ("postgres", "POSTGRES_PORT", "5433", "5432"),
        ("redis", "REDIS_PORT", "6379", "6379"),
        ("chromadb", "CHROMADB_PORT", "8000", "8000"),
    ),
)
def test_the_three_data_services_read_their_host_port(compose, service, variable, default, inside):
    assert compose["services"][service]["ports"] == [f"${{{variable}:-{default}}}:{inside}"]


def test_with_nothing_set_the_names_and_ports_are_the_ones_the_first_install_has(compose):
    text = _rendered(COMPOSE.read_text())
    rendered = yaml.safe_load(text)
    assert rendered["name"] == "piper-morgan-stable"
    assert rendered["networks"]["default"]["name"] == "piper-network"
    assert rendered["volumes"]["piper_postgres_data"]["name"] == "piper_postgres_data_v1"
    assert sorted(s["container_name"] for s in rendered["services"].values()) == [
        "piper-app",
        "piper-chromadb",
        "piper-ghmcp",
        "piper-postgres",
        "piper-redis",
        "piper-temporal",
        "piper-traefik",
    ]
    assert rendered["services"]["postgres"]["ports"] == ["5433:5432"]
    assert rendered["services"]["redis"]["ports"] == ["6379:6379"]
    assert rendered["services"]["chromadb"]["ports"] == ["8000:8000"]


def test_a_second_stack_shares_no_name_and_no_data_port_with_the_first():
    first = yaml.safe_load(_rendered(COMPOSE.read_text()))
    second = yaml.safe_load(
        _rendered(
            COMPOSE.read_text(),
            {
                "PIPER_STACK": "piper2",
                "POSTGRES_PORT": "5543",
                "REDIS_PORT": "6479",
                "CHROMADB_PORT": "8100",
            },
        )
    )

    def names(doc):
        found = {doc["name"], doc["networks"]["default"]["name"]}
        found |= {v["name"] for v in doc["volumes"].values()}
        found |= {s["container_name"] for s in doc["services"].values()}
        return found

    assert names(first).isdisjoint(names(second))
    for service in ("postgres", "redis", "chromadb"):
        assert first["services"][service]["ports"] != second["services"][service]["ports"]


def test_the_file_says_what_a_second_copy_must_set_before_its_first_up():
    head = COMPOSE.read_text().split("\nservices:")[0]
    for needed in ("PIPER_STACK=", "POSTGRES_PORT=", "REDIS_PORT=", "CHROMADB_PORT=", "BEFORE"):
        assert needed in head
    assert "docker compose up -d postgres redis chromadb" in head


# --- the two strings a self-hoster is shown (CXO's words, 2026-11-16) ----------------

ROOT = COMPOSE.parent


def test_the_setup_pages_services_message_names_the_three_services():
    script = (ROOT / "web" / "static" / "js" / "setup.js").read_text()
    assert (
        "If you run Piper on your own computer, start them with "
        "docker compose up -d postgres redis chromadb. "
        "On a hosted instance, tell the person who runs it." in script
    )
    assert "(docker compose up -d)" not in script


def test_the_create_account_database_error_names_the_three_services():
    route = (ROOT / "web" / "api" / "routes" / "setup.py").read_text()
    assert "docker compose up -d postgres redis chromadb. " in route
    assert "'docker compose up -d'" not in route
    assert "Cannot connect to the database. Make sure Docker is running, then " in route
    assert "Then try again." in route
