"""The local key helper: hidden prompt, database store, nothing printed, nothing in argv."""

import base64
import stat
from pathlib import Path

import pytest

from scripts import local_key_setup as lk

# Not key-shaped on purpose (the repo's rule for fake values).
FAKE = "fake-provider-value-for-tests"


class FakeDb:
    def __init__(self, fail=False):
        self.fail = fail

    def list_names(self):
        if self.fail:
            raise ConnectionError("down")
        return []


class FakeService:
    def __init__(self, fail_db=False, fail_store=False, corrupt=False):
        self._db_store = FakeDb(fail_db)
        self.rows = {}
        self.fail_store = fail_store
        self.corrupt = corrupt

    def store_api_key(self, provider, key):
        if self.fail_store:
            raise RuntimeError(f"Failed to store API key: boom {key}")
        self.rows[provider] = key + ("x" if self.corrupt else "")

    def get_api_key(self, provider):
        return self.rows.get(provider)

    def delete_api_key(self, provider):
        return self.rows.pop(provider, None) is not None


def run(argv, tmp_path, service=None, terminal=True, typed=(FAKE,), shown_answers=(), environ=None):
    lines, prompts = [], []
    typed, shown_answers = list(typed), list(shown_answers)
    service = service or FakeService()

    def hidden(prompt):
        prompts.append(prompt)
        return typed.pop(0) if typed else ""

    def shown(prompt):
        prompts.append(prompt)
        return shown_answers.pop(0)

    env = {} if environ is None else environ
    code = lk.main(
        argv,
        terminal=lambda: terminal,
        hidden=hidden,
        shown=shown,
        settings_path=tmp_path / "settings.env",
        environ=env,
        store_factory=lambda: service,
        out=lines.append,
    )
    return code, "\n".join(lines), service, env, prompts


@pytest.fixture(autouse=True)
def no_log_config(monkeypatch):
    monkeypatch.setattr(lk, "quiet_logs", lambda: None)


def test_stores_reads_back_and_never_prints_the_key(tmp_path):
    code, text, service, env, _ = run(["anthropic"], tmp_path)
    assert code == 0
    assert service.rows == {"anthropic": FAKE}
    assert "stored, read back and matched" in text
    assert "python main.py" in text and "Use Keychain" in text
    assert FAKE not in text


def test_creates_the_three_settings_owner_only_and_prints_no_value(tmp_path):
    code, text, _, env, _ = run(["openai"], tmp_path)
    path = tmp_path / "settings.env"
    values = lk.read_settings(path)
    assert set(values) == {lk.MASTER_VAR, lk.JWT_VAR, lk.STORE_VAR}
    assert values[lk.STORE_VAR] == "db"
    assert len(base64.b64decode(values[lk.MASTER_VAR])) == 32
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert values[lk.MASTER_VAR] not in text and values[lk.JWT_VAR] not in text
    assert env[lk.MASTER_VAR] == values[lk.MASTER_VAR] and env[lk.STORE_VAR] == "db"


def test_existing_values_are_kept_and_other_lines_untouched(tmp_path):
    path = tmp_path / "settings.env"
    path.write_text(f"OTHER=1\n{lk.MASTER_VAR}=keepme\n{lk.JWT_VAR}=keepjwt")  # no last newline
    run(["openai"], tmp_path)
    after = path.read_text()
    assert after.startswith(f"OTHER=1\n{lk.MASTER_VAR}=keepme\n{lk.JWT_VAR}=keepjwt\n")
    assert after.count(lk.MASTER_VAR) == 1 and after.count(lk.JWT_VAR) == 1
    assert after.endswith(f"{lk.STORE_VAR}=db\n")
    # a second run adds nothing
    run(["openai"], tmp_path)
    assert path.read_text() == after


def test_environment_master_key_is_used_and_not_written(tmp_path):
    env = {lk.MASTER_VAR: "from-env"}
    code, text, _, env, _ = run(["openai"], tmp_path, environ=env)
    assert code == 0 and env[lk.MASTER_VAR] == "from-env"
    assert lk.MASTER_VAR not in lk.read_settings(tmp_path / "settings.env")
    assert "from-env" not in text


def test_refuses_without_a_terminal_before_anything(tmp_path):
    code, text, service, _, prompts = run(["anthropic"], tmp_path, terminal=False)
    assert code == 2 and "needs a real terminal" in text
    assert prompts == [] and service.rows == {}
    assert not (tmp_path / "settings.env").exists()


def test_a_key_pasted_as_an_argument_is_refused_and_not_echoed(tmp_path):
    code, text, service, _, prompts = run([FAKE], tmp_path)
    assert code == 2 and FAKE not in text and "never given on the command line" in text
    assert prompts == [] and service.rows == {}


@pytest.mark.parametrize("store", ["keychain", "KEYCHAIN"])
def test_stops_when_the_keychain_store_is_chosen(tmp_path, store):
    (tmp_path / "settings.env").write_text(f"{lk.STORE_VAR}={store}\n")
    code, text, service, _, prompts = run(["anthropic"], tmp_path)
    assert code == 1 and "only writes the database store" in text and prompts == []


def test_stops_on_scoped_subkeys(tmp_path):
    code, text, _, _, _ = run(["anthropic"], tmp_path, environ={lk.SCOPED_VAR: "a=b"})
    assert code == 1 and "hosted layout" in text


def test_empty_key_twice_stores_nothing(tmp_path):
    code, text, service, _, prompts = run(["anthropic"], tmp_path, typed=("", " "))
    assert code == 1 and "no key given" in text and service.rows == {} and len(prompts) == 2


def test_key_with_white_space_is_refused(tmp_path):
    code, text, service, _, _ = run(["anthropic"], tmp_path, typed=("ab cd",))
    assert code == 1 and "white space" in text and service.rows == {} and "ab cd" not in text


def test_database_down_names_the_two_commands(tmp_path):
    code, text, _, _, prompts = run(["anthropic"], tmp_path, service=FakeService(fail_db=True))
    assert code == 1 and "docker compose up -d" in text and "alembic upgrade head" in text
    assert prompts == []


def test_store_failure_message_never_carries_the_key(tmp_path):
    code, text, _, _, _ = run(["anthropic"], tmp_path, service=FakeService(fail_store=True))
    assert code == 1 and "was not stored" in text and FAKE not in text


def test_read_back_mismatch_stops(tmp_path):
    code, text, _, _, _ = run(["anthropic"], tmp_path, service=FakeService(corrupt=True))
    assert code == 1 and "did not read back the same" in text and FAKE not in text


def test_provider_is_asked_when_not_given_and_unknown_is_refused(tmp_path):
    code, text, service, _, _ = run([], tmp_path, shown_answers=["OpenAI "])
    assert code == 0 and service.rows == {"openai": FAKE}
    code, text, service, _, _ = run([], tmp_path, shown_answers=["nope"])
    assert code == 1 and "unknown provider" in text and service.rows == {}


def test_list_and_remove_need_no_terminal_and_ask_nothing(tmp_path):
    service = FakeService()
    service.rows["gemini"] = FAKE
    code, text, _, _, prompts = run(["--list"], tmp_path, service=service, terminal=False)
    assert code == 0 and "stored: gemini" in text and FAKE not in text and prompts == []
    code, text, _, _, _ = run(["--remove", "gemini"], tmp_path, service=service, terminal=False)
    assert code == 0 and "gemini: removed" in text and service.rows == {}
    code, text, _, _, _ = run(["--remove", "gemini"], tmp_path, service=service, terminal=False)
    assert "no stored key to remove" in text


def test_replacing_says_replaced(tmp_path):
    service = FakeService()
    service.rows["anthropic"] = "older"
    code, text, _, _, _ = run(["anthropic"], tmp_path, service=service)
    assert code == 0 and "key replaced" in text and service.rows["anthropic"] == FAKE


def test_unexpected_error_gives_the_type_only(tmp_path):
    class Boom(FakeService):
        def get_api_key(self, provider):
            raise ValueError(f"secret {FAKE}")

    code, text, _, _, _ = run(["anthropic"], tmp_path, service=Boom())
    assert code == 1 and "unexpected ValueError" in text and FAKE not in text


def test_source_has_no_keychain_or_env_key_read():
    src = Path(lk.__file__).read_text()
    assert "import keyring" not in src and "_API_KEY" not in src
    assert "subprocess" not in src and "httpx" not in src and "requests" not in src


def test_an_existing_loose_settings_file_is_made_owner_only_and_says_so(tmp_path):
    path = tmp_path / "settings.env"
    path.write_text("OTHER=1\n")
    path.chmod(0o644)
    code, text, _, _, _ = run(["openai"], tmp_path)
    assert code == 0 and stat.S_IMODE(path.stat().st_mode) == 0o600
    assert "now owner-only" in text
    # nothing to add on the second run, so the mode is left alone and nothing is said
    path.chmod(0o640)
    code, text, _, _, _ = run(["openai"], tmp_path)
    assert "now owner-only" not in text
