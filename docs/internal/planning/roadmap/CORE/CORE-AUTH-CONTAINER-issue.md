# CORE-AUTH-CONTAINER: Fix JWT Service Dependency Injection

**Labels**: `technical-debt`, `security`, `authentication`, `alpha`
**Milestone**: Alpha
**Estimate**: 1-2 hours
**Priority**: High (Authentication architecture)

---

## Context

Sprint A6 implemented JWT authentication and user management, but 3 TODOs remain where services aren't using proper dependency injection. This creates tight coupling and makes testing harder.

## Current State

```python
# Current: Direct imports and instantiation

# web/api/routes/auth.py (Line 45)
# TODO: Use dependency injection for jwt_service
jwt_service = JWTService()  # Direct instantiation

# services/auth/user_service.py (Line 89)
# TODO: Get jwt_service from container
from services.auth.jwt_service import jwt_service  # Direct import

# services/auth/user_service.py (Line 156)
# TODO: Inject token blacklist from container
blacklist = TokenBlacklist()  # Direct instantiation
```

## Scope

### 1. Create JWT Service Container

```python
# services/container.py or services/auth/container.py

class AuthContainer:
    """Dependency injection container for auth services"""

    _jwt_service: Optional[JWTService] = None
    _token_blacklist: Optional[TokenBlacklist] = None
    _user_service: Optional[UserService] = None

    @classmethod
    def get_jwt_service(cls) -> JWTService:
        """Singleton JWT service"""
        if not cls._jwt_service:
            cls._jwt_service = JWTService(
                secret_key=settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM,
                expiry_hours=settings.JWT_EXPIRY_HOURS
            )
        return cls._jwt_service

    @classmethod
    def get_token_blacklist(cls) -> TokenBlacklist:
        """Singleton token blacklist"""
        if not cls._token_blacklist:
            cls._token_blacklist = TokenBlacklist(
                redis_client=get_redis_client(),
                fallback_db=get_database()
            )
        return cls._token_blacklist

    @classmethod
    def get_user_service(cls) -> UserService:
        """Singleton user service with injected dependencies"""
        if not cls._user_service:
            cls._user_service = UserService(
                jwt_service=cls.get_jwt_service(),
                token_blacklist=cls.get_token_blacklist(),
                user_repository=get_user_repository()
            )
        return cls._user_service
```

### 2. Update Auth Routes

```python
# web/api/routes/auth.py

from services.auth.container import AuthContainer

def get_jwt_service() -> JWTService:
    """Dependency for FastAPI injection"""
    return AuthContainer.get_jwt_service()

@router.post("/login")
async def login(
    credentials: LoginCredentials,
    jwt_service: JWTService = Depends(get_jwt_service)  # Proper injection
):
    # Now using injected service
    token = await jwt_service.create_token(user_id)
    return {"token": token}

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
    blacklist: TokenBlacklist = Depends(get_token_blacklist)
):
    # Using injected dependencies
    await blacklist.add(token, "user_logout")
    return {"status": "logged out"}
```

### 3. Update User Service

```python
# services/auth/user_service.py

class UserService:
    def __init__(
        self,
        jwt_service: JWTService,
        token_blacklist: TokenBlacklist,
        user_repository: UserRepository
    ):
        # Dependencies injected, not imported
        self.jwt_service = jwt_service
        self.token_blacklist = token_blacklist
        self.user_repository = user_repository

    async def validate_token(self, token: str) -> Optional[User]:
        # Line 89 - Using injected service
        if await self.token_blacklist.is_blacklisted(token):
            return None

        claims = await self.jwt_service.verify_token(token)
        if not claims:
            return None

        return await self.user_repository.get(claims["user_id"])
```

### 4. Update Tests

```python
# tests/auth/test_user_service.py

@pytest.fixture
def mock_jwt_service():
    """Mock JWT service for testing"""
    service = Mock(spec=JWTService)
    service.create_token.return_value = "test_token"
    return service

@pytest.fixture
def mock_blacklist():
    """Mock token blacklist for testing"""
    blacklist = Mock(spec=TokenBlacklist)
    blacklist.is_blacklisted.return_value = False
    return blacklist

async def test_user_service_with_injection(mock_jwt_service, mock_blacklist):
    """Test user service with injected dependencies"""
    user_service = UserService(
        jwt_service=mock_jwt_service,
        token_blacklist=mock_blacklist,
        user_repository=mock_user_repo
    )

    # Now can test in isolation
    result = await user_service.validate_token("test_token")
    mock_blacklist.is_blacklisted.assert_called_once_with("test_token")
```

## Acceptance Criteria

- [ ] All 3 TODOs resolved
- [ ] AuthContainer created with singleton pattern
- [ ] FastAPI routes use Depends() injection
- [ ] UserService receives injected dependencies
- [ ] No direct imports of service instances
- [ ] Tests use mocked dependencies
- [ ] No functionality changes (pure refactoring)

## Benefits

- **Testability**: Can mock dependencies easily
- **Flexibility**: Can swap implementations
- **Configuration**: Centralized service configuration
- **Clarity**: Explicit dependencies
- **Maintainability**: Looser coupling

## Implementation Notes

1. This is pure refactoring - no functional changes
2. Use singleton pattern to avoid multiple instances
3. Follow FastAPI's dependency injection patterns
4. Maintain backward compatibility during transition

## Testing

- [ ] All existing auth tests still pass
- [ ] New tests with mocked dependencies
- [ ] Integration tests verify injection works
- [ ] No performance regression

## Why This Matters for Alpha

Proper dependency injection:
- Makes multi-user testing easier
- Allows different configs per environment
- Simplifies debugging auth issues
- Enables better test coverage

---

**Created**: October 22, 2025
**Author**: Chief Architect
