"""
Authentication Service Package

JWT-based authentication system with OAuth 2.0 federation readiness.
Provides portable identity management and secure session handling.

Components:
- jwt_service: JWT token generation and validation
- auth_middleware: FastAPI authentication middleware
- token_blacklist: Revoked-token tracking
- audit_logger: Authentication audit logging

#936 (May 9 2026): user_service removed. The previous UserService class
was wired in but never populated in production — get_session() always
returned None. Real auth flow uses `users` PostgreSQL table + AuthService
+ JWT. See `dev/2026/05/09/936-issue-audit.md` for the dead-code finding.
"""

__version__ = "1.0.0"
__author__ = "Piper Morgan Security Team"

from .auth_middleware import AuthMiddleware, get_current_user
from .jwt_service import JWTService, TokenExpired, TokenInvalid, TokenRevoked
from .token_blacklist import TokenBlacklist

__all__ = [
    "JWTService",
    "AuthMiddleware",
    "get_current_user",
    "TokenBlacklist",
    "TokenExpired",
    "TokenInvalid",
    "TokenRevoked",
]
