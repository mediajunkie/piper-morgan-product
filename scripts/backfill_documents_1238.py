"""#1238 (ADR-071 P2) backfill — anchor existing ChromaDB pm_knowledge docs.

The doc store is ChromaDB-only; this populates the new `documents` table with one
row per distinct ChromaDB document (base_id ``pdf_<hash>``), owned by the configured
PM (resolve_pm_owner_id) and marked ``is_global_pm_domain=True`` — existing docs are
PM-domain knowledge base (Arch ruling 2026-06-16). Idempotent (upsert by base_id):
safe to re-run.

Usage:
  env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
      venv/bin/python scripts/backfill_documents_1238.py
"""

import asyncio
import sys
from pathlib import Path

import chromadb

# Add project root to path (script run directly, not as a module)
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.repositories.document_repository import (  # noqa: E402
    DocumentRepository,
    resolve_pm_owner_id,
)

CHROMA_PATH = "./data/chromadb"
COLLECTION = "pm_knowledge"


def _base_id(chunk_id: str) -> str:
    """pdf_<hash>_chunk_<i> -> pdf_<hash> (the per-document id)."""
    return chunk_id.rsplit("_chunk_", 1)[0]


async def main() -> None:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_or_create_collection(name=COLLECTION)
    n = col.count()
    if not n:
        print(f"No ChromaDB docs in '{COLLECTION}' — nothing to backfill.")
        return

    got = col.get(limit=n, include=["metadatas"])
    # Group chunks by document base_id; take title/source from the first chunk seen.
    docs: dict[str, dict] = {}
    for cid, md in zip(got["ids"], got["metadatas"]):
        base = _base_id(cid)
        if base not in docs:
            md = md or {}
            docs[base] = {"title": md.get("title"), "source": md.get("source")}

    async with AsyncSessionFactory.session_scope() as session:
        owner = await resolve_pm_owner_id(session)
        repo = DocumentRepository(session)
        for base, meta in docs.items():
            await repo.upsert_document(
                base,
                owner_id=owner,
                is_global_pm_domain=True,
                title=meta["title"],
                source=meta["source"],
            )
        # session_scope() commits on exit

    print(
        f"Backfilled {len(docs)} document(s) into `documents` "
        f"(owner={owner}, is_global_pm_domain=True):"
    )
    for base, meta in docs.items():
        print(f"  {base}: title={meta['title']!r} source={meta['source']!r}")


if __name__ == "__main__":
    asyncio.run(main())
