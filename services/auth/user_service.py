"""
User Service - Identity and Context Management

Manages user identity, authentication state, and portable user context.
Provides user-owned data with secure context export capabilities.

Features:
- User registration and profile management
- Portable identity with context ownership
- Secure user context storage and retrieval
- OAuth provider linking (GitHub, Slack, future providers)
- Exportable user data and audit logs
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

logger = structlog.get_logger(__name__)


class UserStatus(Enum):
    """User account status"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class OAuthProvider(Enum):
    """Supported OAuth providers"""

    GITHUB = "github"
    SLACK = "slack"
    GOOGLE = "google"  # Future
    MICROSOFT = "microsoft"  # Future


@dataclass
class User:
    """User identity with portable context"""

    user_id: UUID
    email: str
    full_name: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    # User preferences and settings
    preferences: Dict[str, Any]

    # OAuth provider connections
    oauth_providers: Dict[str, Dict[str, Any]]  # provider -> {id, token_info, etc}

    # User-owned context data
    context_data: Dict[str, Any]  # Conversations, files, projects, etc.

    # Security and audit
    last_login_at: Optional[datetime] = None
    login_count: int = 0
    security_events: List[Dict[str, Any]] = None

    # System-wide admin role (Issue #357 - SEC-RBAC admin bypass)
    is_admin: bool = False

    def __post_init__(self):
        if self.security_events is None:
            self.security_events = []

    def can_bypass_ownership(self) -> bool:
        """Check if user can bypass ownership restrictions (admin access)"""
        return self.is_admin


@dataclass
class UserSession:
    """User session information"""

    session_id: str
    user_id: UUID
    created_at: datetime
    expires_at: datetime
    last_activity: datetime

    # Session metadata
    ip_address: str
    user_agent: str
    workspace_id: Optional[str] = None

    # Authentication details
    auth_method: str = "jwt"  # jwt, oauth, api_key
    scopes: List[str] = None

    def __post_init__(self):
        if self.scopes is None:
            self.scopes = []


class UserService:
    """
    User identity and context management service.

    Manages user lifecycle, authentication state, and portable context
    with OAuth provider federation support.
    """

    def __init__(self):
        """Initialize user service"""
        # TODO(#936): Replace in-memory dicts with database persistence
        self._users: Dict[str, User] = {}
        self._sessions: Dict[str, UserSession] = {}
        self._email_to_user_id: Dict[str, str] = {}

        logger.info("UserService initialized")

    def create_user(
        self,
        email: str,
        full_name: str,
        preferences: Optional[Dict[str, Any]] = None,
        oauth_provider: Optional[OAuthProvider] = None,
        oauth_data: Optional[Dict[str, Any]] = None,
    ) -> User:
        """
        Create new user with optional OAuth provider linking.

        Args:
            email: User email address (unique identifier)
            full_name: User's full name
            preferences: User preferences and settings
            oauth_provider: OAuth provider for registration
            oauth_data: OAuth provider data (ID, profile info)

        Returns:
            Created User object

        Raises:
            ValueError: If user with email already exists
        """
        if email in self._email_to_user_id:
            raise ValueError(f"User with email {email} already exists")

        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        oauth_providers = {}
        if oauth_provider and oauth_data:
            oauth_providers[oauth_provider.value] = oauth_data

        user = User(
            user_id=user_id,
            email=email,
            full_name=full_name,
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            preferences=preferences or {},
            oauth_providers=oauth_providers,
            context_data={},
        )

        self._users[user_id] = user
        self._email_to_user_id[email] = user_id

        logger.info(
            "User created",
            user_id=user_id,
            email=email,
            oauth_provider=oauth_provider.value if oauth_provider else None,
        )

        return user

    def get_user(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return self._users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        user_id = self._email_to_user_id.get(email)
        return self._users.get(user_id) if user_id else None

    def authenticate_user(
        self,
        email: str,
        auth_method: str = "oauth",
        oauth_provider: Optional[OAuthProvider] = None,
        oauth_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[User]:
        """
        Authenticate user via OAuth or other method.

        Args:
            email: User email address
            auth_method: Authentication method used
            oauth_provider: OAuth provider used for authentication
            oauth_data: OAuth authentication data

        Returns:
            Authenticated User object if successful, None otherwise
        """
        user = self.get_user_by_email(email)

        if not user:
            # Auto-registration for OAuth users
            if oauth_provider and oauth_data:
                full_name = oauth_data.get("name", email.split("@")[0])
                user = self.create_user(
                    email=email,
                    full_name=full_name,
                    oauth_provider=oauth_provider,
                    oauth_data=oauth_data,
                )
            else:
                logger.warning("Authentication failed: user not found", email=email)
                return None

        # Update login tracking
        user.last_login_at = datetime.now(timezone.utc)
        user.login_count += 1

        # Log security event
        security_event = {
            "event_type": "login",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "auth_method": auth_method,
            "oauth_provider": oauth_provider.value if oauth_provider else None,
            "ip_address": "unknown",  # Would be passed from request context
            "success": True,
        }
        user.security_events.append(security_event)

        logger.info(
            "User authenticated",
            user_id=user.user_id,
            email=email,
            auth_method=auth_method,
            login_count=user.login_count,
        )

        return user

    def create_session(
        self,
        user: User,
        ip_address: str,
        user_agent: str,
        scopes: List[str],
        expires_in_minutes: int = 30,
        workspace_id: Optional[str] = None,
    ) -> UserSession:
        """
        Create user session.

        Args:
            user: Authenticated user
            ip_address: Client IP address
            user_agent: Client user agent
            scopes: Session permission scopes
            expires_in_minutes: Session expiration in minutes
            workspace_id: Optional workspace context

        Returns:
            Created UserSession object
        """
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=expires_in_minutes)

        session = UserSession(
            session_id=session_id,
            user_id=user.user_id,
            created_at=now,
            expires_at=expires_at,
            last_activity=now,
            ip_address=ip_address,
            user_agent=user_agent,
            workspace_id=workspace_id,
            scopes=scopes,
        )

        self._sessions[session_id] = session

        logger.info(
            "Session created",
            session_id=session_id,
            user_id=user.user_id,
            expires_at=expires_at.isoformat(),
        )

        return session

    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get user session by ID"""
        session = self._sessions.get(session_id)
        if session and session.expires_at > datetime.now(timezone.utc):
            # Update last activity
            session.last_activity = datetime.now(timezone.utc)
            return session
        elif session:
            # Session expired
            self._sessions.pop(session_id, None)
            logger.info("Session expired", session_id=session_id)
        return None

    def revoke_session(self, session_id: str) -> bool:
        """Revoke user session"""
        session = self._sessions.pop(session_id, None)
        if session:
            logger.info("Session revoked", session_id=session_id, user_id=session.user_id)
            return True
        return False

    def update_user_context(self, user_id: UUID, context_key: str, context_data: Any) -> bool:
        """
        Update user-owned context data.

        Args:
            user_id: User ID
            context_key: Context key (e.g., "conversations", "files", "projects")
            context_data: Context data to store

        Returns:
            True if successful, False otherwise
        """
        user = self.get_user(user_id)
        if not user:
            return False

        user.context_data[context_key] = context_data
        user.updated_at = datetime.now(timezone.utc)

        logger.info("User context updated", user_id=user_id, context_key=context_key)

        return True

    def export_user_data(self, user_id: UUID) -> Dict[str, Any]:
        """
        Export all user data for portability/compliance.

        Args:
            user_id: User ID to export data for

        Returns:
            Complete user data export including context and audit logs
        """
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Convert user to exportable format
        user_export = asdict(user)

        # Add session information
        user_sessions = [
            asdict(session) for session in self._sessions.values() if session.user_id == user_id
        ]

        export_data = {
            "user": user_export,
            "active_sessions": user_sessions,
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "export_format_version": "1.0",
        }

        logger.info("User data exported", user_id=user_id)
        return export_data

    def link_oauth_provider(
        self, user_id: UUID, provider: OAuthProvider, oauth_data: Dict[str, Any]
    ) -> bool:
        """
        Link OAuth provider to user account.

        Args:
            user_id: User ID
            provider: OAuth provider to link
            oauth_data: OAuth provider data

        Returns:
            True if successfully linked, False otherwise
        """
        user = self.get_user(user_id)
        if not user:
            return False

        user.oauth_providers[provider.value] = oauth_data
        user.updated_at = datetime.now(timezone.utc)

        # Log security event
        security_event = {
            "event_type": "oauth_provider_linked",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider.value,
            "provider_user_id": oauth_data.get("id", "unknown"),
        }
        user.security_events.append(security_event)

        logger.info("OAuth provider linked", user_id=user_id, provider=provider.value)

        return True
