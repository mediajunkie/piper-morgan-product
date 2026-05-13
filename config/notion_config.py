"""Notion integration configuration."""

import os
from typing import Optional


class NotionConfig:
    """Notion API configuration."""

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get Notion API key.

        Resolution order (#304 / Issue #1059 follow-up):
        1. `NOTION_API_KEY` env var (legacy + dev convention)
        2. macOS Keychain via `KeychainService().get_api_key("notion")`
           — worktree-friendly; survives worktree-isolation gap (mirrors
           the #1070 `canonical-retest-run8.py` fallback pattern).

        Returns the first hit; None if neither is set.
        """
        key = os.environ.get("NOTION_API_KEY")
        if key:
            return key
        try:
            from services.infrastructure.keychain_service import KeychainService

            return KeychainService().get_api_key("notion")
        except Exception:
            # Keychain unavailable or library missing — fall through silently.
            # env is the primary path; keychain is the convenience fallback.
            return None

    @staticmethod
    def get_workspace_id() -> Optional[str]:
        """Get default workspace ID."""
        return os.environ.get("NOTION_WORKSPACE_ID")

    @staticmethod
    def validate_config() -> bool:
        """Validate Notion configuration."""
        api_key = NotionConfig.get_api_key()
        if not api_key:
            print("WARNING: NOTION_API_KEY not set")
            return False
        if not (api_key.startswith("secret_") or api_key.startswith("ntn_")):
            print(
                "WARNING: NOTION_API_KEY format may be invalid (should start with 'secret_' or 'ntn_')"
            )
            return False
        return True

    @staticmethod
    def get_config_status() -> dict:
        """Get detailed configuration status."""
        api_key = NotionConfig.get_api_key()
        workspace_id = NotionConfig.get_workspace_id()

        return {
            "api_key_set": bool(api_key),
            "api_key_format_valid": bool(
                api_key and (api_key.startswith("secret_") or api_key.startswith("ntn_"))
            ),
            "workspace_id_set": bool(workspace_id),
            "fully_configured": NotionConfig.validate_config(),
        }
