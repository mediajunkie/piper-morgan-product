"""Where the app keeps the data it derives and must not lose at a deploy (#2244).

One setting, ``PIPER_DATA_DIR``, names a durable root. On Fly it points under the
mounted volume (``fly.toml`` ``[env]``; ``deploy/docker-entrypoint.sh`` creates the
folder and hands it to the app user). Unset, each store keeps the relative path it
always had, so a local install is unchanged.

Until #2244 the document index (``./data/chromadb``) and Slack's spatial memory
(``data/spatial_memory``) sat on the machine's own filesystem, which a Fly release
rebuilds from the image: both emptied at every deploy while uploads survived.

Read at call time, never at import, like ``UPLOAD_DIR`` (#1401).
"""

import os
from pathlib import Path
from typing import Optional

DATA_DIR_ENV = "PIPER_DATA_DIR"

# The paths each store used before #2244. A local install keeps them.
LOCAL_DOCUMENT_INDEX_PATH = "./data/chromadb"
LOCAL_SPATIAL_MEMORY_PATH = "data/spatial_memory"


def data_root() -> Optional[Path]:
    """The durable root, or None when ``PIPER_DATA_DIR`` is unset or blank."""
    value = os.getenv(DATA_DIR_ENV, "").strip()
    return Path(value) if value else None


def document_index_path() -> Path:
    """The folder ``DocumentIngester``'s Chroma store lives in."""
    root = data_root()
    return root / "chromadb" if root is not None else Path(LOCAL_DOCUMENT_INDEX_PATH)


def spatial_memory_path() -> Path:
    """The folder ``SpatialMemoryStore`` writes to."""
    root = data_root()
    return root / "spatial_memory" if root is not None else Path(LOCAL_SPATIAL_MEMORY_PATH)


def check_document_index_writable() -> tuple[bool, str]:
    """Can the RUNNING PROCESS write the document index's folder?

    The same probe uploads got in #1656, for the same reason: on Fly the volume
    mounts root-owned and the app runs as ``piper``, so a missing or root-owned
    folder fails every ingest and nothing says so. Makes the folder, writes a
    file, removes it. Returns (ok, message naming the path); never raises.
    """
    base = document_index_path()
    probe = base / f".writability-probe-{os.getpid()}"
    try:
        base.mkdir(parents=True, exist_ok=True)
        probe.write_bytes(b"ok")
        probe.unlink()
        return True, f"document index writable: {base}"
    except OSError as e:
        return False, (
            f"DOCUMENT INDEX NOT WRITABLE: {base} ({e}): document ingest and search "
            f"will fail until this is fixed (#2244: check {DATA_DIR_ENV} and the "
            "folder's owner; deploy/docker-entrypoint.sh prepares it on Fly)."
        )
