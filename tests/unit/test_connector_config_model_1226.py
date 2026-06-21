"""RECONNECT WS-1 (#1226 / #1199) P1 — connector_configs model.

The DB-backed connector-config home (ADR-070 D4). Anchored to the settled single identity via
owner_id FK (ADR-071 D2), multi-tenant-READY via a named-not-built tenant_id (ADR-071 D7 / m-40),
and credential-free (D3 — creds stay in the keychain). These assert the model's structural
contract (the additive migration creates the matching table).
"""
import uuid

from services.database.models import ConnectorConfig


def _cols():
    return {c.name: c for c in ConnectorConfig.__table__.columns}


def test_table_name():
    assert ConnectorConfig.__tablename__ == "connector_configs"


def test_owner_id_is_not_null_fk_to_users():
    owner = _cols()["owner_id"]
    assert not owner.nullable  # config must belong to someone (the settled single identity)
    fks = list(owner.foreign_keys)
    assert fks and fks[0].column.table.name == "users"  # ADR-071 D2


def test_tenant_id_named_but_not_built():
    tenant = _cols()["tenant_id"]
    assert tenant.nullable  # m-40: present (READY) but NULL=single-tenant; no logic branches on it


def test_connector_and_config_columns():
    cols = _cols()
    assert cols["connector"].nullable is False
    assert cols["config"].nullable is False  # default '{}'; never NULL


def test_unique_owner_connector():
    uniques = {
        tuple(sorted(col.name for col in c.columns))
        for c in ConnectorConfig.__table__.constraints
        if c.__class__.__name__ == "UniqueConstraint"
    }
    assert ("connector", "owner_id") in uniques


def test_no_credential_columns_d3():
    # D3: connector config holds NO credential material — those live in the keychain.
    forbidden = ("token", "secret", "password", "credential", "api_key", "apikey")
    offenders = [n for n in _cols() if any(s in n.lower() for s in forbidden)]
    assert not offenders, f"connector_configs must not carry credential columns (D3): {offenders}"


def test_instantiable_with_owner_and_connector():
    cc = ConnectorConfig(owner_id=uuid.uuid4(), connector="github", config={"default_repository": "o/r"})
    assert cc.connector == "github"
    assert cc.config["default_repository"] == "o/r"
