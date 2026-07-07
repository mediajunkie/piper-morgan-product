"""ADR-075 Component B (#1366) — PersonalizationService.

Tests the principal-resolution + neutral-degradation decision logic (D4) in
isolation from the DB: PM's own principal never regresses to a generic
prompt (D3), a real distinct principal gets the owner_id-scoped store (lazy-
seeded on first touch if none exists), and every DB-failure path degrades to
the pre-Component-B file behavior rather than raising or leaking. The
repository layer itself is covered by test_personalization_repository_1366.py
(real SQLite); this file mocks the repository/PM-resolution to isolate the
service's own branching.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from services.configuration.personalization_service import (
    FIRST_RESPONSE_PERSONALIZATION_NOTICE,
    NEUTRAL_DEFAULT_CONTEXT,
    PersonalizationService,
)

_PM_ID = UUID("11111111-1111-1111-1111-111111111111")
_OTHER_USER_ID = "22222222-2222-2222-2222-222222222222"


@pytest.fixture
def service():
    return PersonalizationService()


@pytest.fixture
def mock_session():
    return MagicMock()


class TestResolveSystemPrompt:
    async def test_none_user_id_serves_file_directly(self, service, mock_session):
        """No resolved principal (ambient/legacy/local-dev call) — D3: the file
        is the single-tenant/local-dev default, no regression."""
        with patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_loader:
            mock_loader.get_system_prompt.return_value = "PM's file-based prompt"

            result = await service.resolve_system_prompt(None, mock_session)

            assert result == "PM's file-based prompt"
            mock_loader.get_system_prompt.assert_called_once()

    async def test_pm_principal_serves_file_directly(self, service, mock_session):
        """PM's own resolved principal — D3 no-regression, never the scoped
        store or neutral default for PM's own requests."""
        with patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_loader:
            mock_loader.get_system_prompt.return_value = "PM's file-based prompt"

            result = await service.resolve_system_prompt(str(_PM_ID), mock_session)

            assert result == "PM's file-based prompt"

    async def test_distinct_principal_gets_scoped_content(self, service, mock_session):
        """A real, non-PM principal gets their own owner_id-scoped row —
        never PM's file (the #1366 leak closure)."""
        mock_row = MagicMock()
        mock_row.context = {"User Context": "this user's own content"}

        with patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.personalization_service.PersonalizationContextRepository"
        ) as MockRepo, patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_loader:
            MockRepo.return_value.get_or_seed_default = AsyncMock(return_value=mock_row)
            mock_loader._format_system_prompt.return_value = "formatted: this user's content"

            result = await service.resolve_system_prompt(_OTHER_USER_ID, mock_session)

            assert result == "formatted: this user's content"
            mock_loader._format_system_prompt.assert_called_once_with(
                {"User Context": "this user's own content"}
            )
            # Never touched PM's raw system prompt for this distinct principal.
            mock_loader.get_system_prompt.assert_not_called()

    async def test_db_failure_degrades_to_file_not_raise(self, service, mock_session):
        """Any failure resolving the scoped store must degrade to the
        pre-Component-B file behavior — never raise, never silently empty."""
        with patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.personalization_service.PersonalizationContextRepository"
        ) as MockRepo, patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_loader:
            MockRepo.return_value.get_or_seed_default = AsyncMock(
                side_effect=RuntimeError("db down")
            )
            mock_loader.get_system_prompt.return_value = "fallback file prompt"

            result = await service.resolve_system_prompt(_OTHER_USER_ID, mock_session)

            assert result == "fallback file prompt"

    async def test_malformed_user_id_treated_as_no_principal(self, service, mock_session):
        with patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_loader:
            mock_loader.get_system_prompt.return_value = "fallback file prompt"

            result = await service.resolve_system_prompt("not-a-uuid", mock_session)

            assert result == "fallback file prompt"


class TestMaybeConsumeFirstResponseNotice:
    async def test_none_user_id_never_gets_notice(self, service):
        assert await service.maybe_consume_first_response_notice(None) is None

    async def test_pm_never_gets_notice(self, service):
        with patch(
            "services.database.session_factory.AsyncSessionFactory"
        ) as MockFactory, patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ):
            MockFactory.session_scope.return_value.__aenter__ = AsyncMock(
                return_value=MagicMock()
            )
            MockFactory.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await service.maybe_consume_first_response_notice(str(_PM_ID))

            assert result is None

    async def test_seeded_and_unseen_returns_notice_and_marks_seen(self, service):
        mock_row = MagicMock(is_seeded_default=True, has_seen_personalization_notice=False)

        with patch(
            "services.database.session_factory.AsyncSessionFactory"
        ) as MockFactory, patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.personalization_service.PersonalizationContextRepository"
        ) as MockRepo:
            MockFactory.session_scope.return_value.__aenter__ = AsyncMock(
                return_value=MagicMock()
            )
            MockFactory.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)
            mock_repo_instance = MockRepo.return_value
            mock_repo_instance.get_or_seed_default = AsyncMock(return_value=mock_row)
            mock_repo_instance.mark_notice_seen = AsyncMock()

            result = await service.maybe_consume_first_response_notice(_OTHER_USER_ID)

            assert result == FIRST_RESPONSE_PERSONALIZATION_NOTICE
            mock_repo_instance.mark_notice_seen.assert_awaited_once()

    async def test_already_seen_returns_none(self, service):
        mock_row = MagicMock(is_seeded_default=True, has_seen_personalization_notice=True)

        with patch(
            "services.database.session_factory.AsyncSessionFactory"
        ) as MockFactory, patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.personalization_service.PersonalizationContextRepository"
        ) as MockRepo:
            MockFactory.session_scope.return_value.__aenter__ = AsyncMock(
                return_value=MagicMock()
            )
            MockFactory.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)
            MockRepo.return_value.get_or_seed_default = AsyncMock(return_value=mock_row)

            result = await service.maybe_consume_first_response_notice(_OTHER_USER_ID)

            assert result is None

    async def test_customized_profile_returns_none(self, service):
        """A user who's customized their profile (is_seeded_default=False)
        never gets the notice, regardless of has_seen_personalization_notice."""
        mock_row = MagicMock(is_seeded_default=False, has_seen_personalization_notice=False)

        with patch(
            "services.database.session_factory.AsyncSessionFactory"
        ) as MockFactory, patch(
            "services.configuration.personalization_service._resolve_pm_owner_id_safe",
            new=AsyncMock(return_value=_PM_ID),
        ), patch(
            "services.configuration.personalization_service.PersonalizationContextRepository"
        ) as MockRepo:
            MockFactory.session_scope.return_value.__aenter__ = AsyncMock(
                return_value=MagicMock()
            )
            MockFactory.session_scope.return_value.__aexit__ = AsyncMock(return_value=False)
            MockRepo.return_value.get_or_seed_default = AsyncMock(return_value=mock_row)

            result = await service.maybe_consume_first_response_notice(_OTHER_USER_ID)

            assert result is None

    async def test_failure_degrades_to_none_not_raise(self, service):
        with patch(
            "services.database.session_factory.AsyncSessionFactory"
        ) as MockFactory:
            MockFactory.session_scope.side_effect = RuntimeError("db down")

            result = await service.maybe_consume_first_response_notice(_OTHER_USER_ID)

            assert result is None


class TestNeutralDefaultContent:
    def test_is_not_empty_or_blank(self):
        """HOST's requirement: a real, capable persona record, not an implicit
        empty fall-through."""
        assert NEUTRAL_DEFAULT_CONTEXT
        assert all(isinstance(v, str) and v.strip() for v in NEUTRAL_DEFAULT_CONTEXT.values())

    def test_does_not_reference_pm_specific_content(self):
        """Must not be PM's own portfolio/priorities — generic PM-assistant
        persona only (CXO spec)."""
        content_blob = " ".join(NEUTRAL_DEFAULT_CONTEXT.values()).lower()
        # A loose smoke check for obviously PM-specific leakage words that
        # would indicate someone accidentally pasted real content in here.
        assert "xian" not in content_blob
        assert "piper morgan" not in content_blob  # the product name itself, not a persona trait
