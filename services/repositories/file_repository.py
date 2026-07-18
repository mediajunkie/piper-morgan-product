"""
FileRepository implementation using SQLAlchemy AsyncSession
Following Pattern #1: Repository Pattern from pattern-catalog.md
Following ADR-010: Configuration Access Patterns
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import UploadedFileDB
from services.database.repositories import BaseRepository
from services.domain.models import UploadedFile
from services.infrastructure.config.feature_flags import FeatureFlags
from services.infrastructure.config.file_configuration import (
    FileConfigService,
    get_file_config_service,
)

logger = logging.getLogger(__name__)


class FileRepository(BaseRepository):
    """Repository for file metadata operations using SQLAlchemy"""

    model = UploadedFileDB

    def __init__(self, session: AsyncSession, config_service: Optional[FileConfigService] = None):
        super().__init__(session)
        # ADR-010: Use ConfigService for application layer configuration
        self.config_service = config_service or get_file_config_service()

    def get_repository_config(self) -> dict:
        """Get repository configuration using ConfigService"""
        return self.config_service.get_repository_config()

    async def save_file_metadata(self, file: UploadedFile) -> UploadedFile:
        """Save file metadata to database"""
        # Convert domain model to DB model
        db_file = UploadedFileDB.from_domain(file)

        # Add to session - transaction managed by caller
        self.session.add(db_file)
        await self.session.flush()
        await self.session.refresh(db_file)

        # Convert back to domain model
        return db_file.to_domain()

    async def get_file_by_id(
        self, file_id: str, owner_id: str = None, is_admin: bool = False
    ) -> Optional[UploadedFile]:
        """Get file by ID - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [UploadedFileDB.id == file_id]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(UploadedFileDB.owner_id == owner_id)

        result = await self.session.execute(select(UploadedFileDB).where(and_(*filters)))
        db_file = result.scalar_one_or_none()
        return db_file.to_domain() if db_file else None

    async def get_files_for_session(self, owner_id: str, limit: int = 10) -> List[UploadedFile]:
        """Get files for an owner, ordered by upload time (most recent first)"""
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(UploadedFileDB.owner_id == owner_id)
            .order_by(UploadedFileDB.upload_time.desc())
            .limit(limit)
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def increment_reference_count(self, file_id: str, owner_id: str = None):
        """Increment reference count and update last_referenced timestamp - optionally verify ownership"""
        filters = [UploadedFileDB.id == file_id]
        if owner_id:
            filters.append(UploadedFileDB.owner_id == owner_id)

        await self.session.execute(
            update(UploadedFileDB)
            .where(and_(*filters))
            .values(
                reference_count=UploadedFileDB.reference_count + 1,
                last_referenced=datetime.now(),
            )
        )

        # Return the updated file
        result = await self.session.execute(select(UploadedFileDB).where(and_(*filters)))
        db_file = result.scalar_one_or_none()
        return db_file.to_domain() if db_file else None

    async def search_files_by_name(self, owner_id: str, query: str) -> List[UploadedFile]:
        """Search files by name for an owner (case-insensitive partial match)"""
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.owner_id == owner_id,
                    UploadedFileDB.filename.ilike(f"%{query}%"),
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def get_recent_files(self, owner_id: str, hours: int = 24) -> List[UploadedFile]:
        """Get files uploaded within the last N hours for an owner"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.owner_id == owner_id,
                    UploadedFileDB.upload_time > cutoff_time,
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def search_files_by_name_all_sessions(
        self, query: str, owner_id: str, days: int = 30
    ) -> List[UploadedFile]:
        """Search files by name for an owner within the last N days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.owner_id == owner_id,
                    UploadedFileDB.filename.ilike(f"%{query}%"),
                    UploadedFileDB.upload_time > cutoff_time,
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def get_recent_files_all_sessions(
        self, owner_id: str, days: int = 7
    ) -> List[UploadedFile]:
        """Get files uploaded for an owner within the last N days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        result = await self.session.execute(
            select(UploadedFileDB)
            .where(
                and_(
                    UploadedFileDB.owner_id == owner_id,
                    UploadedFileDB.upload_time > cutoff_time,
                )
            )
            .order_by(UploadedFileDB.upload_time.desc())
        )
        db_files = result.scalars().all()
        return [db_file.to_domain() for db_file in db_files]

    async def delete_file(self, file_id: str, owner_id: str = None, is_admin: bool = False) -> bool:
        """Delete file metadata by ID - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [UploadedFileDB.id == file_id]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(UploadedFileDB.owner_id == owner_id)

        result = await self.session.execute(select(UploadedFileDB).where(and_(*filters)))
        db_file = result.scalar_one_or_none()

        if db_file:
            await self.session.delete(db_file)
            return True
        return False

    async def search_files_with_content(
        self, owner_id: str, query: str, limit: int = 10
    ) -> List[UploadedFile]:
        """
        Enhanced search combining filename and content search.
        Falls back to filename-only search if MCP is disabled.
        """
        logger.info(f"Searching files with content for owner {owner_id}, query: {query}")

        # Get files matching by filename first (always available)
        filename_matches = await self.search_files_by_name(owner_id, query)

        # ADR-010: Use ConfigService for application layer configuration
        mcp_enabled = self.config_service.get_mcp_search_enabled()

        if not mcp_enabled:
            logger.debug("MCP content search disabled, returning filename matches only")
            return filename_matches[:limit]

        # #1436 Tier-3 interim guard (Arch batch memo 2026-07-18, "the sleeper"):
        # MCPResourceManager wraps the SIMULATION-only PiperMCPClient — with the
        # flag on, content search would blend FABRICATED results into real file
        # search. Until this path is wired to the real consumer client (or the
        # family is deleted — Arch ruling pending), the flag-on path honestly
        # degrades to filename search. Both pending rulings start with "stop
        # serving simulated results," so this guard is safe under either.
        logger.warning(
            "mcp_content_search_unavailable: flag is on but the backing client is "
            "simulation-only — returning filename matches (honest degrade, #1436)"
        )
        return filename_matches[:limit]


    async def search_files_with_content_all_sessions(
        self, query: str, owner_id: str, days: int = 30, limit: int = 10
    ) -> List[UploadedFile]:
        """
        Enhanced search for an owner combining filename and content search.
        Falls back to filename-only search if MCP is disabled.
        """
        logger.info(f"Searching files with content for owner {owner_id}, query: {query}")

        # Get files matching by filename first (always available)
        filename_matches = await self.search_files_by_name_all_sessions(query, owner_id, days)

        # ADR-010: Use ConfigService for application layer configuration
        mcp_enabled = self.config_service.get_mcp_search_enabled()

        if not mcp_enabled:
            logger.debug("MCP content search disabled, returning filename matches only")
            return filename_matches[:limit]

        # #1436 Tier-3 interim guard (Arch batch memo 2026-07-18, "the sleeper"):
        # MCPResourceManager wraps the SIMULATION-only PiperMCPClient — with the
        # flag on, content search would blend FABRICATED results into real file
        # search. Until this path is wired to the real consumer client (or the
        # family is deleted — Arch ruling pending), the flag-on path honestly
        # degrades to filename search. Both pending rulings start with "stop
        # serving simulated results," so this guard is safe under either.
        logger.warning(
            "mcp_content_search_unavailable: flag is on but the backing client is "
            "simulation-only — returning filename matches (honest degrade, #1436)"
        )
        return filename_matches[:limit]

