"""Tests for Slack OAuth user_scopes defaults (#1085 slice 3 prep).

Verifies that the OAuth flow defaults to including `search:read` on the
user-token scope list, enabling Slack search.messages API for the
recent-activity aggregator's mentions-of-user lookup path.

Per Pattern-073 discipline: the test is bounded — checks the default
scope list contents, not the OAuth flow's full behavior (which requires
live Slack integration).
"""

from pathlib import Path


SOURCE_FILE = Path("services/integrations/slack/oauth_handler.py")


def test_user_scopes_default_includes_search_read() -> None:
    """The OAuth handler's default user_scopes block includes search:read."""
    src = SOURCE_FILE.read_text()
    # Locate the user_scopes default block
    block_marker = "Default user-token scopes (Issue #1085 slice 3 prep)"
    assert block_marker in src, (
        "OAuth handler must have a documented user_scopes default block"
    )
    # search:read must appear after the marker (within the same defaults block)
    start = src.find(block_marker)
    end = src.find("# Build authorization parameters", start)
    block = src[start:end] if end > start else src[start:]
    assert '"search:read"' in block, (
        "Default user_scopes must include search:read for the search.messages API"
    )


def test_user_scopes_block_is_caller_overridable() -> None:
    """The default is only applied when no user_scopes are passed in
    (preserving the existing caller-supplies-scopes shape)."""
    src = SOURCE_FILE.read_text()
    block_marker = "Default user-token scopes (Issue #1085 slice 3 prep)"
    start = src.find(block_marker)
    end = src.find("# Build authorization parameters", start)
    block = src[start:end]
    # The default block must guard with `if not user_scopes:`
    assert "if not user_scopes:" in block, (
        "Defaults must only apply when caller hasn't passed user_scopes"
    )


def test_change_documented_with_issue_reference() -> None:
    """Code comment cites #1085 for future-reader traceability."""
    src = SOURCE_FILE.read_text()
    block_marker = "Default user-token scopes (Issue #1085 slice 3 prep)"
    start = src.find(block_marker)
    end = src.find("# Build authorization parameters", start)
    block = src[start:end]
    assert "#1085" in block, "Change must cite #1085"
    assert "search.messages" in block, (
        "Comment must explain why search:read is required"
    )


def test_search_read_is_user_token_scope_not_bot() -> None:
    """search:read is in the user_scopes block, NOT the bot scopes block.

    Slack's search.messages API requires a USER token with search:read;
    bot tokens cannot use search. Verifying we put it in the right place.
    """
    src = SOURCE_FILE.read_text()
    # The bot scopes block is the FIRST scopes default; user_scopes is SECOND.
    bot_start = src.find("# Default scopes for spatial metaphor capabilities")
    user_start = src.find("# Default user-token scopes")
    assert bot_start >= 0 and user_start >= 0
    assert user_start > bot_start, "user_scopes block must come AFTER bot scopes block"
    bot_block = src[bot_start:user_start]
    # search:read must NOT appear in the bot scopes block
    assert '"search:read"' not in bot_block, (
        "search:read is a user-token scope; must not be in bot scopes block"
    )
