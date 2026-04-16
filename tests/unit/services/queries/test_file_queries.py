"""
Tests for FileQueryService - TDD approach
These tests should fail initially since we haven't implemented the FileQueryService yet.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from services.queries.file_queries import FileQueryService
from services.repositories.file_repository import FileRepository


class TestFileQueryService:
    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_read_file_contents(self):
        # Arrange
        file_id = "test-file-id"
        mock_file = {
            "id": file_id,
            "filename": "test.md",
            "file_type": "text/markdown",
            "storage_path": "uploads/test.md",
        }
        mock_file_repository = Mock()
        mock_file_repository.get_file_by_id = AsyncMock(return_value=mock_file)

        service = FileQueryService(mock_file_repository)

        # Act
        result = await service.read_file_contents(file_id)

        # Assert
        assert result["success"] is True
        assert result["file"]["filename"] == "test.md"
        mock_file_repository.get_file_by_id.assert_called_once_with(file_id)
