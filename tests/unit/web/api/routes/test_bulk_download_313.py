"""#313 G64: bulk download — zip of selected files + artifacts.

Route called directly with mocked session (established route-unit pattern).
Per-item ownership: inaccessible/missing items are SKIPPED, not fatal.
"""

import io
import zipfile
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes import files as files_route
from web.api.routes.files import download_bulk


def _req(user_id="u1", is_admin=False):
    return SimpleNamespace(state=SimpleNamespace(user_id=user_id, is_admin=is_admin))


def _session_ctx(rows_by_id):
    session = MagicMock()

    async def _execute(stmt):
        result = MagicMock()
        # crude: pull the file id from the compiled WHERE clause params
        fid = list(stmt.compile().params.values())[0]
        result.scalar_one_or_none.return_value = rows_by_id.get(fid)
        return result

    session.execute = AsyncMock(side_effect=_execute)
    factory = MagicMock()
    factory.session_scope_fresh.return_value.__aenter__ = AsyncMock(return_value=session)
    factory.session_scope_fresh.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


def _file_row(fid, owner, path):
    return SimpleNamespace(id=fid, filename=f"{fid}.txt", owner_id=owner, storage_path=str(path))


@pytest.mark.asyncio
async def test_zips_owned_files_and_skips_foreign(tmp_path):
    p1 = tmp_path / "a.txt"
    p1.write_text("alpha")
    p2 = tmp_path / "b.txt"
    p2.write_text("bravo")
    rows = {
        "f1": _file_row("f1", "u1", p1),
        "f2": _file_row("f2", "someone-else", p2),  # foreign → skipped
    }
    with (
        patch.object(files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())),
        patch.object(files_route, "AsyncSessionFactory", _session_ctx(rows)),
    ):
        resp = await download_bulk(
            _req(), {"items": [{"id": "f1", "kind": "file"}, {"id": "f2", "kind": "file"}]}
        )
    assert resp.headers["X-Added"] == "1"
    assert resp.headers["X-Skipped"] == "1"
    zf = zipfile.ZipFile(io.BytesIO(resp.body))
    assert zf.namelist() == ["f1.txt"]
    assert zf.read("f1.txt") == b"alpha"


@pytest.mark.asyncio
async def test_empty_items_400():
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as ei:
        await download_bulk(_req(), {"items": []})
    assert ei.value.status_code == 400


@pytest.mark.asyncio
async def test_all_inaccessible_404(tmp_path):
    rows = {"f9": _file_row("f9", "someone-else", tmp_path / "x.txt")}
    from fastapi import HTTPException

    with (
        patch.object(files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())),
        patch.object(files_route, "AsyncSessionFactory", _session_ctx(rows)),
    ):
        with pytest.raises(HTTPException) as ei:
            await download_bulk(_req(), {"items": [{"id": "f9", "kind": "file"}]})
    assert ei.value.status_code == 404


@pytest.mark.asyncio
async def test_over_50_items_400():
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as ei:
        await download_bulk(_req(), {"items": [{"id": str(i)} for i in range(51)]})
    assert ei.value.status_code == 400
