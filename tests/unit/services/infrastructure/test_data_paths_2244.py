"""#2244: the document index and Slack's spatial memory live under one durable root.

Before: ``./data/chromadb`` and ``data/spatial_memory`` on the machine's own
filesystem, emptied by every Fly release. After: under ``PIPER_DATA_DIR`` when it
is set (the mounted volume on Fly); a local install keeps the old paths.
"""

import os
import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.infrastructure import data_paths

REPO = Path(__file__).resolve().parents[4]


def _fly_env() -> dict:
    """fly.toml's [env] table, read with the standard parser."""
    import tomllib

    return tomllib.loads((REPO / "fly.toml").read_text())["env"]


class TestPaths:
    def test_unset_keeps_the_paths_a_local_install_always_had(self, monkeypatch):
        monkeypatch.delenv("PIPER_DATA_DIR", raising=False)
        assert data_paths.data_root() is None
        assert data_paths.document_index_path() == Path("./data/chromadb")
        assert data_paths.spatial_memory_path() == Path("data/spatial_memory")

    def test_blank_is_unset(self, monkeypatch):
        monkeypatch.setenv("PIPER_DATA_DIR", "  ")
        assert data_paths.data_root() is None
        assert data_paths.document_index_path() == Path("./data/chromadb")

    def test_set_puts_both_stores_under_the_root(self, monkeypatch):
        monkeypatch.setenv("PIPER_DATA_DIR", "/data/piper")
        assert data_paths.document_index_path() == Path("/data/piper/chromadb")
        assert data_paths.spatial_memory_path() == Path("/data/piper/spatial_memory")

    def test_read_at_call_time_not_import_time(self, monkeypatch):
        monkeypatch.setenv("PIPER_DATA_DIR", "/a")
        first = data_paths.document_index_path()
        monkeypatch.setenv("PIPER_DATA_DIR", "/b")
        assert (first, data_paths.document_index_path()) == (
            Path("/a/chromadb"),
            Path("/b/chromadb"),
        )


class TestTheStoresReadIt:
    def test_ingester_with_no_path_opens_the_configured_store(self, monkeypatch, tmp_path):
        """get_ingester() passes no path, so this is the app's real construction."""
        from services.knowledge_graph import ingestion

        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "root"))
        with patch.object(ingestion.chromadb, "PersistentClient") as client:
            ing = ingestion.DocumentIngester()
        assert ing.chroma_path == str(tmp_path / "root" / "chromadb")
        assert client.call_args.kwargs["path"] == str(tmp_path / "root" / "chromadb")

    def test_ingester_unset_keeps_the_local_path(self, monkeypatch):
        from services.knowledge_graph import ingestion

        monkeypatch.delenv("PIPER_DATA_DIR", raising=False)
        with patch.object(ingestion.chromadb, "PersistentClient") as client:
            ingestion.DocumentIngester()
        assert client.call_args.kwargs["path"] == "data/chromadb"

    def test_ingester_explicit_path_still_wins(self, monkeypatch, tmp_path):
        from services.knowledge_graph import ingestion

        monkeypatch.setenv("PIPER_DATA_DIR", "/data/piper")
        with patch.object(ingestion.chromadb, "PersistentClient") as client:
            ingestion.DocumentIngester(chroma_path=str(tmp_path))
        assert client.call_args.kwargs["path"] == str(tmp_path)

    def test_get_ingester_passes_no_path(self):
        """The singleton must not pin a path of its own, or the setting is dead."""
        import inspect

        from services.knowledge_graph import ingestion

        assert "DocumentIngester()" in inspect.getsource(ingestion.get_ingester)

    def test_spatial_memory_with_no_path_uses_the_configured_folder(self, monkeypatch, tmp_path):
        from services.integrations.slack.spatial_memory import SpatialMemoryStore

        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "root"))
        store = SpatialMemoryStore()
        assert store.storage_path == tmp_path / "root" / "spatial_memory"
        assert store.storage_path.is_dir()

    def test_spatial_memory_explicit_path_still_wins(self, monkeypatch, tmp_path):
        from services.integrations.slack.spatial_memory import SpatialMemoryStore

        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "root"))
        assert SpatialMemoryStore(str(tmp_path / "mine")).storage_path == tmp_path / "mine"

    def test_both_slack_callers_pass_no_path(self):
        """attention_model and workspace_navigator build the store bare; if either
        starts passing a path, it leaves the volume without anyone noticing."""
        for name in ("attention_model.py", "workspace_navigator.py"):
            src = (REPO / "services/integrations/slack" / name).read_text()
            assert "memory_store or SpatialMemoryStore()" in src, name

    def test_erase_script_reads_the_same_store(self, monkeypatch, tmp_path):
        """Erasing a person must look where the app writes. With the root set and
        no store there, the script reports absence (None) and creates nothing."""
        import importlib
        import sys

        sys.path.insert(0, str(REPO / "scripts"))
        erase_user = importlib.import_module("erase_user")
        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "root"))
        assert erase_user._chroma_collection() is None
        assert not (tmp_path / "root").exists()

    def test_erase_script_opens_the_store_under_the_root(self, monkeypatch, tmp_path):
        import importlib
        import sys

        sys.path.insert(0, str(REPO / "scripts"))
        erase_user = importlib.import_module("erase_user")
        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "root"))
        (tmp_path / "root" / "chromadb").mkdir(parents=True)
        with patch("chromadb.PersistentClient") as client:
            erase_user._chroma_collection()
        assert client.call_args.kwargs["path"] == str(tmp_path / "root" / "chromadb")


class TestWritableProbe:
    def test_reports_writable_and_names_the_path(self, monkeypatch, tmp_path):
        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "vol"))
        ok, message = data_paths.check_document_index_writable()
        assert ok is True
        assert str(tmp_path / "vol" / "chromadb") in message
        assert list((tmp_path / "vol" / "chromadb").iterdir()) == []  # probe file removed

    def test_reports_unwritable_loudly_and_never_raises(self, monkeypatch, tmp_path):
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            pytest.skip("running as root: chmod 555 cannot deny writes")
        denied = tmp_path / "rootonly"
        denied.mkdir()
        denied.chmod(0o555)
        try:
            monkeypatch.setenv("PIPER_DATA_DIR", str(denied / "piper"))
            ok, message = data_paths.check_document_index_writable()
            assert ok is False
            assert "DOCUMENT INDEX NOT WRITABLE" in message
            assert str(denied / "piper" / "chromadb") in message
        finally:
            denied.chmod(0o755)

    @pytest.mark.asyncio
    async def test_boot_phase_prints_and_logs_when_writable(self, monkeypatch, tmp_path, capsys):
        from web.startup import DocumentIndexProbePhase

        app = SimpleNamespace(state=SimpleNamespace())
        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "vol"))
        with patch("web.startup.logger") as log:
            await DocumentIndexProbePhase.startup(app)
        assert app.state.document_index_writable is True
        assert "✅ Document index:" in capsys.readouterr().out
        assert log.info.call_args.args[0] == "document_index_writable"

    @pytest.mark.asyncio
    async def test_boot_phase_logs_error_when_unwritable(self, monkeypatch, tmp_path, capsys):
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            pytest.skip("running as root: chmod 555 cannot deny writes")
        from web.startup import DocumentIndexProbePhase

        app = SimpleNamespace(state=SimpleNamespace())
        denied = tmp_path / "rootonly"
        denied.mkdir()
        denied.chmod(0o555)
        try:
            monkeypatch.setenv("PIPER_DATA_DIR", str(denied / "piper"))
            with patch("web.startup.logger") as log:
                await DocumentIndexProbePhase.startup(app)
            assert app.state.document_index_writable is False
            assert "🔴 Document index:" in capsys.readouterr().out
            log.error.assert_called_once()
        finally:
            denied.chmod(0o755)

    def test_phase_is_in_the_real_boot_sequence(self):
        from web.startup import DocumentIndexProbePhase, StartupManager

        assert DocumentIndexProbePhase in StartupManager(SimpleNamespace()).phases


class TestSetupCheckReportsTheStoreActuallyUsed:
    """Acceptance row 3. The app has no Chroma server client, so the old port
    probe (CHROMA_HOST / CHROMADB_HOST) measured something the app never uses."""

    @pytest.mark.asyncio
    async def test_true_when_the_store_folder_is_writable(self, monkeypatch, tmp_path):
        import web.api.routes.setup as setup_mod

        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "vol"))
        assert await setup_mod.check_chromadb() is True

    @pytest.mark.asyncio
    async def test_false_when_it_is_not(self, monkeypatch, tmp_path):
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            pytest.skip("running as root: chmod 555 cannot deny writes")
        import web.api.routes.setup as setup_mod

        denied = tmp_path / "rootonly"
        denied.mkdir()
        denied.chmod(0o555)
        try:
            monkeypatch.setenv("PIPER_DATA_DIR", str(denied / "piper"))
            assert await setup_mod.check_chromadb() is False
        finally:
            denied.chmod(0o755)

    @pytest.mark.asyncio
    async def test_no_server_port_is_probed(self, monkeypatch, tmp_path):
        from unittest.mock import AsyncMock

        import web.api.routes.setup as setup_mod

        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "vol"))
        monkeypatch.setenv("CHROMA_HOST", "piper-morgan-chroma.internal")
        with patch.object(
            setup_mod, "check_service_port", new=AsyncMock(return_value=False)
        ) as csp:
            assert await setup_mod.check_chromadb() is True
        csp.assert_not_awaited()

    def test_the_app_still_has_no_chroma_server_client(self):
        """The premise of the check above. If a server client ever appears in the
        app, this check must learn about it."""
        hits = []
        for folder in ("services", "web"):
            for path in (REPO / folder).rglob("*.py"):
                if "chromadb.HttpClient" in path.read_text(errors="ignore"):
                    hits.append(str(path.relative_to(REPO)))
        assert hits == []


class TestDeployFiles:
    def test_fly_names_a_root_under_the_mounted_volume(self):
        import tomllib

        cfg = tomllib.loads((REPO / "fly.toml").read_text())
        root = cfg["env"]["PIPER_DATA_DIR"]
        mounts = cfg["mounts"]
        mounts = mounts if isinstance(mounts, list) else [mounts]
        destinations = [m["destination"] for m in mounts]
        assert any(root.startswith(d.rstrip("/") + "/") for d in destinations), (root, destinations)

    def test_the_root_is_not_inside_the_uploads_folder(self):
        """Uploads get a recursive chown at every start; the data root must not."""
        env = _fly_env()
        assert not env["PIPER_DATA_DIR"].startswith(env["UPLOAD_DIR"].rstrip("/") + "/")
        assert env["PIPER_DATA_DIR"] != env["UPLOAD_DIR"]

    def test_entrypoint_prepares_the_root_with_a_plain_chown(self):
        """Arch, 2026-11-24: mkdir -p and a plain chown, never -R (it runs as root
        on every machine start and the stores grow with use)."""
        script = (REPO / "deploy/docker-entrypoint.sh").read_text()
        code = [ln.strip() for ln in script.splitlines() if not ln.strip().startswith("#")]
        assert 'mkdir -p "$PIPER_DATA_DIR"' in code
        assert 'chown -h piper:piper "$PIPER_DATA_DIR"' in code
        assert not any(re.search(r"chown\s+-\w*R.*PIPER_DATA_DIR", ln) for ln in code)

    def test_entrypoint_prepares_it_as_root_before_dropping_privileges(self):
        script = (REPO / "deploy/docker-entrypoint.sh").read_text()
        root_block = script[script.index('if [ "$(id -u)" = "0" ]') : script.index("exec setpriv")]
        assert 'chown -h piper:piper "$PIPER_DATA_DIR"' in root_block

    def test_entrypoint_runs_exactly_the_commands_we_expect_as_root(self):
        """The root phase is a deploy-path surface (xian's yes, 2026-11-26, covered
        these lines). Any new command as root fails here until it is reviewed."""
        script = (REPO / "deploy/docker-entrypoint.sh").read_text()
        root_block = script[script.index('if [ "$(id -u)" = "0" ]') : script.index("exec setpriv")]
        commands = [
            ln.strip()
            for ln in root_block.splitlines()[1:]
            if ln.strip() and not ln.strip().startswith(("#", "if ", "fi"))
        ]
        assert commands == [
            'mkdir -p "$UPLOAD_DIR"',
            'chown -R piper:piper "$UPLOAD_DIR"',
            'mkdir -p "$PIPER_DATA_DIR"',
            'chown -h piper:piper "$PIPER_DATA_DIR"',
        ]

    def test_entrypoint_never_prepares_the_root_through_a_symlink(self):
        """HOST, 2026-11-26: the guard that wraps the two commands refuses a link."""
        script = (REPO / "deploy/docker-entrypoint.sh").read_text()
        guard = 'if [ -n "${PIPER_DATA_DIR:-}" ] && [ ! -L "$PIPER_DATA_DIR" ]; then'
        assert guard in script
        block = script[script.index(guard) :]
        block = block[: block.index("\n    fi\n")]
        assert (
            'mkdir -p "$PIPER_DATA_DIR"' in block
            and 'chown -h piper:piper "$PIPER_DATA_DIR"' in block
        )

    def test_the_guard_behaves_as_written(self, tmp_path):
        """Run the guard's own test expression in bash: a real folder and a missing
        path pass it, a symlink does not, an unset variable does not."""
        import subprocess

        real, link = tmp_path / "real", tmp_path / "link"
        real.mkdir()
        link.symlink_to(real)
        expr = '[ -n "${PIPER_DATA_DIR:-}" ] && [ ! -L "$PIPER_DATA_DIR" ]'

        def passes(value):
            env = {"PATH": "/usr/bin:/bin"}
            if value is not None:
                env["PIPER_DATA_DIR"] = str(value)
            return subprocess.run(["bash", "-c", expr], env=env).returncode == 0

        assert passes(real) and passes(tmp_path / "not-there-yet")
        assert not passes(link)
        assert not passes(None)


class TestTheWizardsSayOneThingAboutTheDocumentFolder:
    """Arch (01M8CFAVWZ): one check, asked in one place. CXO (01M8CEQ3ZA): the folder has
    its own sentence; the docker advice names only what docker starts."""

    LINE = (
        "Piper can't write its document folder. On your own computer, check that the folder "
        "is there and your account can write to it. On a hosted instance, tell the person "
        "who runs it."
    )

    @staticmethod
    def _cli_wizard():
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "setup_wizard_2244", REPO / "scripts/setup_wizard.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @pytest.mark.asyncio
    async def test_cli_wizard_asks_the_same_function_as_the_web_check(self, monkeypatch, tmp_path):
        wizard = self._cli_wizard()
        monkeypatch.setenv("PIPER_DATA_DIR", str(tmp_path / "vol"))
        with patch.object(wizard, "check_service_port") as port:
            assert await wizard.check_chromadb() is True
        port.assert_not_called()

    @pytest.mark.asyncio
    async def test_cli_wizard_says_no_when_the_folder_is_not_writable(self, monkeypatch, tmp_path):
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            pytest.skip("running as root: chmod 555 cannot deny writes")
        wizard = self._cli_wizard()
        denied = tmp_path / "rootonly"
        denied.mkdir()
        denied.chmod(0o555)
        try:
            monkeypatch.setenv("PIPER_DATA_DIR", str(denied / "piper"))
            assert await wizard.check_chromadb() is False
        finally:
            denied.chmod(0o755)

    def test_no_wizard_probes_a_chroma_port(self):
        src = (REPO / "scripts/setup_wizard.py").read_text()
        assert '"localhost", 8000' not in src
        assert "ChromaDB (8000)" not in src

    def test_the_sentence_is_the_same_in_both_wizards(self):
        assert self._cli_wizard().DOCUMENT_FOLDER_NOT_WRITABLE_LINE == self.LINE
        assert self.LINE in (REPO / "web/static/js/setup.js").read_text()

    def test_no_wizard_tells_a_person_to_start_a_chromadb_container(self):
        for name in (
            "web/static/js/setup.js",
            "scripts/setup_wizard.py",
            "scripts/validate_install.py",
        ):
            src = (REPO / name).read_text()
            assert "redis chromadb" not in src, name
            assert "docker compose up -d postgres redis" in src, name

    def test_the_toast_title_fits_a_folder_failure(self):
        js = (REPO / "web/static/js/setup.js").read_text()
        assert "folderDown ? 'Setup check failed' : 'Services Not Running'" in js
        # The row's name and the filter's name are one constant (CXO, mail 01M8CGQYPT:
        # the row and the toast name the same thing).
        assert "const DOCUMENT_FOLDER_ROW = 'Document index folder';" in js
        assert "name !== DOCUMENT_FOLDER_ROW" in js
        assert "down.includes(DOCUMENT_FOLDER_ROW)" in js
        assert "{ name: DOCUMENT_FOLDER_ROW, ready: data.chromadb_ready }" in js
        assert "'ChromaDB'" not in js and "Checking ChromaDB" not in js

    def test_the_routes_summary_names_the_row_the_same_way(self):
        route = (REPO / "web/api/routes/setup.py").read_text()
        assert 'failed_services.append("Document index folder")' in route
        assert 'failed_services.append("ChromaDB")' not in route
