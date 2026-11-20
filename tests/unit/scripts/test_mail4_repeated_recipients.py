"""mail4.py send: a repeated --to or --cc adds recipients; it never replaces the earlier ones.
Before 2026-11-20 `--cc lead --cc host` kept only host (HOST's Step A reply dropped Lead)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="module")
def mail4():
    spec = importlib.util.spec_from_file_location("mail4", ROOT / "scripts" / "mail4.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BASE = ["send", "--type", "fyi", "--subject", "s"]


def test_repeated_cc_keeps_both(mail4):
    a = mail4.build_parser().parse_args(BASE + ["--to", "exec", "--cc", "lead", "--cc", "host"])
    assert a.cc == ["lead", "host"]


def test_one_cc_with_two_roles(mail4):
    a = mail4.build_parser().parse_args(BASE + ["--to", "exec", "--cc", "lead", "host"])
    assert a.cc == ["lead", "host"]


def test_repeated_to_keeps_both(mail4):
    a = mail4.build_parser().parse_args(BASE + ["--to", "exec", "--to", "lead"])
    assert a.to == ["exec", "lead"]


def test_no_cc_is_none(mail4):
    a = mail4.build_parser().parse_args(BASE + ["--to", "exec"])
    assert not a.cc


def test_to_still_required(mail4):
    with pytest.raises(SystemExit):
        mail4.build_parser().parse_args(BASE)
