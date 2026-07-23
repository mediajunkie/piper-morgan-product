"""
Test suite for Issue #280: CORE-ALPHA-DATA-LEAK
Verify personal data isolation between users

These tests define what "done" means for the data leak fix:
- PIPER.md must contain zero personal/company information
- User-specific data must be stored in database (alpha_users.preferences)
- ConfigService must properly isolate data by user_id
- No data leakage between users
"""

import re
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from services.database.models import User


class TestDataIsolation:
    """Verify PIPER.md has no personal data and user data is isolated.

    #1452 (2026-07-23): four tests removed — they pinned the #280 migration's
    implementation snapshot: a generic `services.config.config_service.
    ConfigService` that no longer exists (personalization became DB-backed and
    owner-scoped via services/configuration — live coverage in
    tests/unit/services/configuration/test_personalization_*_1366.py), and a
    literal 'xian' alpha_users row with a 2025 preferences schema (q4_goals).
    The live contract this file still guards: PIPER.md carries zero personal
    data and stays generic.
    """

    def test_piper_md_has_no_personal_data(self):
        """
        Verify PIPER.md contains zero personal/company information.

        Success Criteria:
        - No mentions of: Q4, VA, DRAGONS, Kind Systems, Christian, xian
        - No specific project names or team structures
        - Only generic capabilities and personality
        - No company-specific examples
        """
        piper_md_path = Path("config/PIPER.md")

        assert piper_md_path.exists(), "PIPER.md must exist"

        content = piper_md_path.read_text()

        # Check for personal data patterns
        personal_patterns = [
            r"\bQ4\b",
            r"\bVA\b",
            r"\bDRAGONS\b",
            r"\bKind\s+Systems\b",
            r"\bChristian\b",
            r"\bxian\b",
            r"\bVeterans\s+Affairs\b",
            # Add more patterns as needed
        ]

        violations = []
        for pattern in personal_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append(f"Found personal data: '{pattern}' matched {len(matches)} times")

        assert not violations, f"PIPER.md contains personal data:\n" + "\n".join(violations)

    def test_piper_md_has_generic_capabilities(self):
        """
        Verify PIPER.md contains generic system capabilities.

        Success Criteria:
        - Documents available capabilities
        - Describes personality traits
        - Lists integrations
        - All content is generic (not user-specific)
        """
        piper_md_path = Path("config/PIPER.md")
        content = piper_md_path.read_text().lower()

        # Check for expected generic sections
        expected_sections = [
            "capabilities",
            "integrations",
            "personality",
        ]

        for section in expected_sections:
            assert section in content, f"PIPER.md should document '{section}' generically"





    def test_piper_md_backup_exists(self):
        """
        Verify backup was created before modifications.

        Success Criteria:
        - Backup file exists with date suffix
        - Backup contains original content (before extraction)
        """
        backup_files = list(Path("config").glob("PIPER.md.backup-*"))

        assert len(backup_files) > 0, "PIPER.md backup should exist before modifications"


# Fixtures for database session
@pytest.fixture
async def db_session():
    """Provide database session for tests"""
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield session
