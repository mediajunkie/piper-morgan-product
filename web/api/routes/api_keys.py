"""
API Key Management API Routes

Provides endpoints for managing user-specific API keys with OS keychain storage.
Supports multi-user key isolation, validation, and zero-downtime rotation.

Issue #228 CORE-USERS-API Phase 2B
Issue #249 CORE-AUDIT-LOGGING Phase 3B - Added audit logging
"""

from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

router = APIRouter(prefix="/api/v1/keys", tags=["api-keys"])
logger = structlog.get_logger(__name__)


def build_audit_context(request: Request) -> Dict[str, Any]:
    """
    Extract audit context from FastAPI request.

    Args:
        request: FastAPI Request object

    Returns:
        Dict with ip_address, user_agent, request_id, request_path

    Issue #249: Audit logging context helper
    """
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.headers.get("x-request-id"),
        "request_path": str(request.url.path),
    }


# Request/Response Models
class StoreKeyRequest(BaseModel):
    """Request model for storing API key"""

    provider: str = Field(..., description="Service provider (openai, anthropic, github, etc)")
    api_key: str = Field(..., description="API key to store")
    validate: bool = Field(True, description="Whether to validate key before storing")


class RotateKeyRequest(BaseModel):
    """Request model for rotating API key"""

    new_api_key: str = Field(..., description="New API key to rotate to")
    validate: bool = Field(True, description="Whether to validate new key before rotation")


class KeyMetadata(BaseModel):
    """Response model for key metadata"""

    provider: str
    is_active: bool
    is_validated: bool
    last_validated_at: Optional[str]
    created_at: str
    rotated_at: Optional[str]


class StoreKeyResponse(BaseModel):
    """Response model for store key operation"""

    success: bool
    provider: str
    is_validated: bool
    message: str


class RotateKeyResponse(BaseModel):
    """Response model for rotate key operation"""

    success: bool
    provider: str
    rotated_at: str
    message: str


class DeleteKeyResponse(BaseModel):
    """Response model for delete key operation"""

    success: bool
    provider: str
    message: str


class ValidateKeyResponse(BaseModel):
    """Response model for validate key operation"""

    provider: str
    is_valid: bool
    message: str


# Dependency injection
async def get_user_api_key_service(request: Request) -> UserAPIKeyService:
    """
    Dependency injection for UserAPIKeyService.

    Returns:
        UserAPIKeyService instance
    """
    # Check if we've already initialized the service in app state
    if hasattr(request.app.state, "user_api_key_service"):
        return request.app.state.user_api_key_service

    # Create and cache service
    service = UserAPIKeyService()
    request.app.state.user_api_key_service = service

    return service


# Endpoints
@router.post("/store", response_model=StoreKeyResponse, status_code=status.HTTP_201_CREATED)
async def store_api_key(
    req: Request,
    request: StoreKeyRequest,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserAPIKeyService = Depends(get_user_api_key_service),
):
    """
    Store API key for authenticated user.

    The key is stored securely in the OS keychain with metadata in the database.
    Keys are isolated per user - each user can have their own keys for the same provider.

    Args:
        req: FastAPI Request object for audit context
        request: Store key request with provider and api_key
        current_user: Current authenticated user from JWT token
        service: UserAPIKeyService instance

    Returns:
        Success response with provider and validation status

    Raises:
        HTTPException: If validation fails or storage fails

    Issue #249: Added audit logging
    """
    try:
        # Build audit context from request (Issue #249)
        audit_context = build_audit_context(req)

        async with AsyncSessionFactory.session_scope() as session:
            user_key = await service.store_user_key(
                session=session,
                user_id=current_user.user_id,
                provider=request.provider,
                api_key=request.api_key,
                validate=request.validate,
                audit_context=audit_context,
            )
            assert user_key is not None  # None only when store=False; not used here

            logger.info(
                "API key stored",
                user_id=current_user.user_id,
                provider=request.provider,
                is_validated=user_key.is_validated,
            )

            # A key that failed provider validation is still stored (#485), so the
            # message carries the provider's reason (#1718). With validate=False,
            # is_validated=False means "unknown", not "failed" — no reason then.
            message = f"API key for {request.provider} stored successfully"
            if request.validate and not user_key.is_validated:
                validation_message = getattr(user_key, "validation_message", None)
                message = validation_message or (
                    f"API key for {request.provider} was saved, but could not be "
                    "validated with the provider."
                )

            return StoreKeyResponse(
                success=True,
                provider=request.provider,
                is_validated=user_key.is_validated,
                message=message,
            )

    except ValueError as e:
        logger.error("Failed to store API key", error=str(e), user_id=current_user.user_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error storing API key", error=str(e), user_id=current_user.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to store API key"
        )


@router.get("/list", response_model=List[KeyMetadata])
async def list_api_keys(
    active_only: bool = True,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserAPIKeyService = Depends(get_user_api_key_service),
):
    """
    List all API keys for authenticated user.

    Returns metadata only (no actual keys). Shows which providers the user has configured.

    Args:
        active_only: Only return active keys (default: True)
        current_user: Current authenticated user from JWT token
        service: UserAPIKeyService instance

    Returns:
        List of key metadata for user's keys
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            keys = await service.list_user_keys(
                session=session, user_id=current_user.user_id, active_only=active_only
            )

            logger.info(
                "Listed API keys",
                user_id=current_user.user_id,
                count=len(keys),
                active_only=active_only,
            )

            return [KeyMetadata(**key) for key in keys]

    except Exception as e:
        logger.error("Failed to list API keys", error=str(e), user_id=current_user.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list API keys"
        )


@router.delete("/{provider}", response_model=DeleteKeyResponse)
async def delete_api_key(
    provider: str,
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserAPIKeyService = Depends(get_user_api_key_service),
):
    """
    Delete API key for authenticated user and provider.

    Removes key from both OS keychain and database.

    Args:
        provider: Service provider (e.g., "openai", "anthropic")
        request: FastAPI Request object for audit context
        current_user: Current authenticated user from JWT token
        service: UserAPIKeyService instance

    Returns:
        Success response

    Raises:
        HTTPException: If key not found or deletion fails

    Issue #249: Added audit logging
    """
    try:
        # Build audit context from request (Issue #249)
        audit_context = build_audit_context(request)

        async with AsyncSessionFactory.session_scope() as session:
            deleted = await service.delete_user_key(
                session=session,
                user_id=current_user.user_id,
                provider=provider,
                audit_context=audit_context,
            )

            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No API key found for provider: {provider}",
                )

            logger.info("API key deleted", user_id=current_user.user_id, provider=provider)

            return DeleteKeyResponse(
                success=True,
                provider=provider,
                message=f"API key for {provider} deleted successfully",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete API key", error=str(e), user_id=current_user.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete API key"
        )


@router.post("/{provider}/validate", response_model=ValidateKeyResponse)
async def validate_api_key(
    provider: str,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserAPIKeyService = Depends(get_user_api_key_service),
):
    """
    Validate API key for authenticated user and provider.

    Makes a real API call to the provider to verify the key works.
    Updates validation status in database.

    Args:
        provider: Service provider (e.g., "openai", "anthropic")
        current_user: Current authenticated user from JWT token
        service: UserAPIKeyService instance

    Returns:
        Validation result

    Raises:
        HTTPException: If key not found or validation fails
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            is_valid = await service.validate_user_key(
                session=session, user_id=current_user.user_id, provider=provider
            )

            logger.info(
                "API key validated",
                user_id=current_user.user_id,
                provider=provider,
                is_valid=is_valid,
            )

            return ValidateKeyResponse(
                provider=provider,
                is_valid=is_valid,
                message=f"API key for {provider} is {'valid' if is_valid else 'invalid'}",
            )

    except Exception as e:
        logger.error("Failed to validate API key", error=str(e), user_id=current_user.user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to validate API key"
        )


@router.post("/{provider}/rotate", response_model=RotateKeyResponse)
async def rotate_api_key(
    provider: str,
    req: Request,
    request: RotateKeyRequest,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserAPIKeyService = Depends(get_user_api_key_service),
):
    """
    Rotate API key for authenticated user and provider.

    Zero-downtime rotation:
    1. Validates new key
    2. Stores old key reference
    3. Stores new key in keychain
    4. Updates database with rotation info
    5. Deletes old key from keychain

    Args:
        provider: Service provider (e.g., "openai", "anthropic")
        req: FastAPI Request object for audit context
        request: Rotate key request with new_api_key
        current_user: Current authenticated user from JWT token
        service: UserAPIKeyService instance

    Returns:
        Success response with rotation timestamp

    Raises:
        HTTPException: If no existing key found or validation fails

    Issue #249: Added audit logging
    """
    try:
        # Build audit context from request (Issue #249)
        audit_context = build_audit_context(req)

        async with AsyncSessionFactory.session_scope() as session:
            user_key = await service.rotate_user_key(
                session=session,
                user_id=current_user.user_id,
                provider=provider,
                new_api_key=request.new_api_key,
                validate=request.validate,
                audit_context=audit_context,
            )

            logger.info(
                "API key rotated",
                user_id=current_user.user_id,
                provider=provider,
                rotated_at=user_key.rotated_at.isoformat(),
            )

            return RotateKeyResponse(
                success=True,
                provider=provider,
                rotated_at=user_key.rotated_at.isoformat(),
                message=f"API key for {provider} rotated successfully",
            )

    except ValueError as e:
        logger.error("Failed to rotate API key", error=str(e), user_id=current_user.user_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(
            "Unexpected error rotating API key", error=str(e), user_id=current_user.user_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to rotate API key"
        )
