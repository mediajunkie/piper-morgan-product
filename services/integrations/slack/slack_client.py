"""
Production Slack Client
Enhanced Slack API client with comprehensive error handling, retry logic,
authentication management, and rate limiting for production use.

Implements production-ready Slack API design following GitHub client patterns.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import aiohttp
from aiohttp import ClientSession, ClientTimeout

from .config_service import SlackConfig, SlackConfigService
from .mrkdwn import markdown_to_mrkdwn


class SlackErrorType(Enum):
    """Slack error types"""

    AUTHENTICATION_ERROR = "authentication_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"


@dataclass
class SlackError:
    """Slack error information"""

    type: SlackErrorType
    message: str
    status_code: Optional[int] = None
    retry_after: Optional[int] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SlackResponse:
    """Slack API response wrapper"""

    success: bool
    data: Dict[str, Any]
    error: Optional[SlackError] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[int] = None


class SlackClient:
    """Production Slack API client"""

    def __init__(self, config_service: SlackConfigService, user_id: str):
        """Construct a Slack client scoped to a single user.

        Args:
            config_service: SlackConfigService for credential resolution.
            user_id: User identifier scoping credential lookups. REQUIRED —
                ``SlackConfigService.get_config`` requires it (ADR-058 / #734),
                so a SlackClient with no user_id cannot make a single API call.
                We refuse to construct one rather than fail later with a confusing
                TypeError deep in the request path (#1110).

        Raises:
            ValueError: If ``user_id`` is None or empty.
        """
        if not user_id:
            raise ValueError(
                "user_id is required for SlackClient (multi-tenancy, ADR-058/#734). "
                "A client without a user_id cannot call get_config()."
            )
        self.config_service = config_service
        self.user_id = user_id
        self.logger = logging.getLogger(__name__)
        self._session: Optional[ClientSession] = None
        self._rate_limit_reset = 0
        self._requests_this_minute = 0
        self._last_request_time = 0

    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self._close_session()

    async def _ensure_session(self):
        """Ensure HTTP session is available"""
        if self._session is None or self._session.closed:
            config = self.config_service.get_config(self.user_id)
            timeout = ClientTimeout(total=config.timeout_seconds)
            self._session = ClientSession(timeout=timeout)

    async def _close_session(self):
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        current_time = time.time()
        config = self.config_service.get_config(self.user_id)

        # Reset counter if minute has passed
        if current_time - self._last_request_time >= 60:
            self._requests_this_minute = 0
            self._last_request_time = current_time

        # Check if we're at the limit
        if self._requests_this_minute >= config.requests_per_minute:
            wait_time = 60 - (current_time - self._last_request_time)
            if wait_time > 0:
                self.logger.warning(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                await asyncio.sleep(wait_time)
                self._requests_this_minute = 0
                self._last_request_time = time.time()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_user_token: bool = False,
        params: Optional[Dict[str, Any]] = None,
    ) -> SlackResponse:
        """Make HTTP request to Slack API with error handling.

        #1338: ``use_user_token=True`` authenticates with the user token (xoxp-) instead
        of the bot token — required for USER-only methods like ``search.messages``. If the
        user token isn't configured, this honest-degrades (returns an auth-error
        SlackResponse) rather than calling Slack with an empty bearer. ``params`` sends
        query-string params (search.messages is a GET/params method, not JSON-body).
        """
        await self._ensure_session()
        await self._check_rate_limit()

        config = self.config_service.get_config(self.user_id)
        url = f"{config.api_base_url}/{endpoint}"

        # #1338: select bot vs user token; honest-degrade if the user token is absent.
        token = config.user_token if use_user_token else config.bot_token
        if use_user_token and not token:
            return SlackResponse(
                success=False,
                data={},
                error=SlackError(
                    type=SlackErrorType.AUTHENTICATION_ERROR,
                    message="No Slack user token configured (user-only method requires xoxp- token)",
                ),
            )

        # Prepare headers
        request_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        if headers:
            request_headers.update(headers)

        # Prepare request data
        request_data = data or {}

        try:
            self._requests_this_minute += 1

            async with self._session.request(
                method=method,
                url=url,
                json=request_data,
                params=params,
                headers=request_headers,
            ) as response:
                response_data = await response.json()

                # Handle rate limiting
                if response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    return SlackResponse(
                        success=False,
                        data=response_data,
                        error=SlackError(
                            type=SlackErrorType.RATE_LIMIT_ERROR,
                            message="Rate limit exceeded",
                            status_code=429,
                            retry_after=retry_after,
                        ),
                    )

                # Handle other errors
                if not response.ok:
                    return SlackResponse(
                        success=False,
                        data=response_data,
                        error=SlackError(
                            type=SlackErrorType.API_ERROR,
                            message=f"Slack API error: {response.status}",
                            status_code=response.status,
                            details=response_data,
                        ),
                    )

                # Success response
                return SlackResponse(
                    success=True,
                    data=response_data,
                    rate_limit_remaining=int(response.headers.get("X-RateLimit-Remaining", 0)),
                    rate_limit_reset=int(response.headers.get("X-RateLimit-Reset", 0)),
                )

        except aiohttp.ClientError as e:
            self.logger.error(f"Network error in Slack API request: {e}")
            return SlackResponse(
                success=False,
                data={},
                error=SlackError(
                    type=SlackErrorType.NETWORK_ERROR, message=f"Network error: {str(e)}"
                ),
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in Slack API request: {e}")
            return SlackResponse(
                success=False,
                data={},
                error=SlackError(
                    type=SlackErrorType.API_ERROR, message=f"Unexpected error: {str(e)}"
                ),
            )

    async def send_message(
        self, channel: str, text: str, user_id: Optional[str] = None, **kwargs
    ) -> SlackResponse:
        """Send message to Slack channel.

        #1227: the floor emits GitHub-flavored markdown but Slack renders the
        ``text`` field as mrkdwn, so normalize here — the single chokepoint that
        response_handler routes through (simple_response_handler did too, until
        its disposal — 2026-08-30 census disposal Batch 3). (Applied
        once per path: socket_mode_runner uses its own WebClient, not this seam,
        and converts there — so no double-conversion.)

        #1110: ``user_id`` is accepted (and ignored) so callers that route
        through either the router OR a raw SlackClient can pass it uniformly.
        A raw client is already bound to its user at construction
        (``self.user_id``); the explicit param exists only to keep it OUT of
        ``**kwargs`` so it never leaks into the chat.postMessage payload.
        """
        text = markdown_to_mrkdwn(text)
        data = {"channel": channel, "text": text, **kwargs}

        # Log the posting attempt
        thread_info = (
            f" (thread: {kwargs.get('thread_ts', 'N/A')})" if kwargs.get("thread_ts") else ""
        )
        self.logger.info(
            f"SLACK_PIPELINE: Posting to Slack channel {channel}{thread_info} - "
            f"Text preview: {text[:50]}{'...' if len(text) > 50 else ''}"
        )

        response = await self._make_request("POST", "chat.postMessage", data)

        # Log the response status
        if response.success:
            self.logger.info(
                f"SLACK_PIPELINE: SlackClient response: SUCCESS - "
                f"Channel: {channel}, Message TS: {response.data.get('ts', 'N/A')}"
            )
        else:
            error_msg = response.error.message if response.error else "Unknown error"
            self.logger.error(
                f"SLACK_PIPELINE: SlackClient response: FAILED - "
                f"Channel: {channel}, Error: {error_msg}"
            )

        return response

    async def get_channel_info(self, channel: str) -> SlackResponse:
        """Get channel information"""
        return await self._make_request("GET", f"conversations.info?channel={channel}")

    async def list_im_channels(self) -> SlackResponse:
        """List the authenticated user's direct-message channels (im + mpim).

        Added 2026-05-17 (#1085 slice 2). Pairs with `im:history` / `mpim:history`
        scopes for the recent-activity aggregator.
        """
        return await self._make_request("GET", "conversations.list?types=im,mpim&limit=200")

    async def get_conversation_history(
        self,
        channel: str,
        limit: int = 50,
        oldest: Optional[float] = None,
        cursor: Optional[str] = None,
    ) -> SlackResponse:
        """Fetch conversation history for a channel.

        Added 2026-05-17 (#1085 slice 2). Previously the router declared this
        method but SlackClient didn't implement it (Pattern-073 instance at
        the router→client interface layer). This implementation closes that
        gap.

        Args:
            channel: Channel ID (any conversation type)
            limit: Max messages to return (Slack max 1000; default 50)
            oldest: Float Slack timestamp; messages older are excluded
            cursor: Pagination cursor from a prior call's response_metadata
        """
        params = f"channel={channel}&limit={limit}"
        if oldest is not None:
            params += f"&oldest={oldest}"
        if cursor:
            params += f"&cursor={cursor}"
        return await self._make_request("GET", f"conversations.history?{params}")

    async def list_channels(self) -> SlackResponse:
        """List all channels"""
        return await self._make_request("GET", "conversations.list")

    async def get_user_info(self, user: str) -> SlackResponse:
        """Get user information"""
        return await self._make_request("GET", f"users.info?user={user}")

    async def list_users(self) -> SlackResponse:
        """List all users"""
        return await self._make_request("GET", "users.list")

    async def search_messages(
        self,
        query: str,
        count: int = 20,
        sort: str = "timestamp",
        sort_dir: str = "desc",
    ) -> SlackResponse:
        """Search messages via `search.messages` (#1338).

        A USER-only Web API method (a bot token cannot call it), so it authenticates
        with the user token and sends query-string params. Honest-degrades via
        `_make_request` when no user token is configured.
        """
        return await self._make_request(
            "GET",
            "search.messages",
            use_user_token=True,
            params={
                "query": query,
                "count": str(count),
                "sort": sort,
                "sort_dir": sort_dir,
            },
        )

    async def test_auth(self, use_user_token: bool = False) -> SlackResponse:
        """Test authentication. #1338: ``use_user_token=True`` validates the user token
        (xoxp-) instead of the bot token — used to discover the user's handle for
        search.messages."""
        self.logger.info("SLACK_PIPELINE: Testing Slack authentication...")
        response = await self._make_request("GET", "auth.test", use_user_token=use_user_token)

        if response.success:
            auth_data = response.data
            self.logger.info(
                f"SLACK_PIPELINE: SlackClient authentication: SUCCESS - "
                f"Team: {auth_data.get('team', 'N/A')}, "
                f"User: {auth_data.get('user', 'N/A')}, "
                f"Bot ID: {auth_data.get('bot_id', 'N/A')}"
            )
        else:
            error_msg = response.error.message if response.error else "Unknown error"
            self.logger.error(
                f"SLACK_PIPELINE: SlackClient authentication: FAILED - Error: {error_msg}"
            )

        return response
