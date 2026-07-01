"""
Conversation API Routes

Issue #563: Session Continuity & Auto-Save
- Get latest conversation for "Continue where you left off" prompt
- Get conversation turns for history restoration

Issue #565: Conversation History Sidebar
- List all user conversations
- Create new conversation
- Get specific conversation by ID
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.repositories import ConversationRepository
from web.api.dependencies import get_conversation_repository

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])
logger = structlog.get_logger(__name__)


# Response Models


class ConversationSummary(BaseModel):
    """Summary of a conversation for restore prompt."""

    id: str
    title: str
    created_at: str
    last_activity_at: Optional[str] = None


class LatestConversationResponse(BaseModel):
    """Response for latest conversation endpoint."""

    conversation: Optional[ConversationSummary] = None
    has_turns: bool = False


class ConversationTurnResponse(BaseModel):
    """Response for a single conversation turn."""

    id: str
    turn_number: int
    user_message: str
    assistant_response: str
    created_at: str


@router.get("/latest", response_model=LatestConversationResponse)
async def get_latest_conversation(
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> LatestConversationResponse:
    """
    Get user's most recent active conversation for restore prompt.

    Issue #563: Enables "Continue where you left off?" feature.
    Returns the most recent conversation with turn count to determine
    if a restore prompt should be shown.

    Args:
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        LatestConversationResponse with conversation summary and has_turns flag

    Example response:
        {
            "conversation": {
                "id": "abc123",
                "title": "Conversation",
                "created_at": "2026-01-10T12:00:00",
                "last_activity_at": "2026-01-10T12:30:00"
            },
            "has_turns": true
        }
    """
    try:
        # Get latest conversation for user
        conversation = await conv_repo.get_latest_for_user(current_user.sub)

        if not conversation:
            logger.debug("No conversation found for user", user_id=current_user.sub)
            return LatestConversationResponse(conversation=None, has_turns=False)

        # Check if conversation has any turns
        turns = await conv_repo.get_conversation_turns(conversation.id, limit=1)
        has_turns = len(turns) > 0

        logger.debug(
            "Found latest conversation",
            user_id=current_user.sub,
            conversation_id=conversation.id,
            has_turns=has_turns,
        )

        # Issue #788: Add Z suffix to indicate UTC timezone for proper JS parsing
        # Issue #788: Replace +00:00 with Z for JS Date parsing
        return LatestConversationResponse(
            conversation=ConversationSummary(
                id=conversation.id,
                title=conversation.title or "Conversation",
                created_at=(
                    conversation.created_at.isoformat().replace("+00:00", "Z")
                    if conversation.created_at
                    else ""
                ),
                last_activity_at=(
                    conversation.last_activity_at.isoformat().replace("+00:00", "Z")
                    if conversation.last_activity_at
                    else None
                ),
            ),
            has_turns=has_turns,
        )

    except Exception as e:
        logger.error("Failed to get latest conversation", error=str(e), user_id=current_user.sub)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation",
        )


@router.get("/{conversation_id}/turns")
async def get_conversation_turns(
    conversation_id: str,
    limit: int = 50,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> list[ConversationTurnResponse]:
    """
    Get turns for a specific conversation.

    Issue #563: Enables conversation history restoration.

    Args:
        conversation_id: The conversation ID to fetch turns for
        limit: Maximum number of turns to return (default 50)
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        List of ConversationTurnResponse objects ordered by turn_number
    """
    try:
        # Get the specific conversation by ID and verify ownership
        # Fix for #574: Was using get_latest_for_user() which only returned most recent,
        # causing all other conversations to fail the ownership check
        conversation = await conv_repo.get_by_id(conversation_id, user_id=current_user.sub)

        # Debug logging for #574
        logger.info(
            "DEBUG #574: get_conversation_turns called",
            conversation_id=conversation_id,
            conversation_found=conversation is not None,
            conversation_user_id=str(conversation.user_id) if conversation else None,
            current_user_sub=current_user.sub,
            types=f"conv.user_id={type(conversation.user_id).__name__ if conversation else 'N/A'}, sub={type(current_user.sub).__name__}",
        )

        # Verify conversation exists and user owns it (security: don't leak existence)
        if not conversation or str(conversation.user_id) != str(current_user.sub):
            logger.warning(
                "Conversation access denied",
                user_id=current_user.sub,
                requested_conversation_id=conversation_id,
                conversation_user_id=str(conversation.user_id) if conversation else None,
            )
            return []

        # #1235: return the NEWEST `limit` turns (still chronologically ordered), not the
        # oldest. This endpoint restores a conversation for viewing/continuing (#563); a
        # conversation longer than `limit` should show where the user left off, not turns
        # 1..limit from the start. Reuses the #1223 `most_recent` machinery. (If a
        # "scroll back to older turns" viewer is needed later, add offset pagination then.)
        turns = await conv_repo.get_conversation_turns(
            conversation_id, limit=limit, most_recent=True
        )
        logger.info("DEBUG #574: turns fetched", turn_count=len(turns))

        # Issue #788: Add Z suffix to indicate UTC timezone for proper JS parsing
        # Issue #788: Replace +00:00 with Z for JS Date parsing
        return [
            ConversationTurnResponse(
                id=turn.id,
                turn_number=turn.turn_number,
                user_message=turn.user_message,
                assistant_response=turn.assistant_response,
                created_at=(
                    turn.created_at.isoformat().replace("+00:00", "Z") if turn.created_at else ""
                ),
            )
            for turn in turns
        ]

    except Exception as e:
        logger.error(
            "Failed to get conversation turns",
            error=str(e),
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation turns",
        )


# Issue #565: Conversation History Sidebar endpoints


class ConversationListItem(BaseModel):
    """Item in conversation list for sidebar."""

    id: str
    title: str
    created_at: str
    updated_at: Optional[str] = None
    turn_count: int = 0
    lifecycle_state: str = "active"  # Issue #715


class ConversationListResponse(BaseModel):
    """Response for list conversations endpoint."""

    conversations: List[ConversationListItem]
    has_more: bool = False


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""

    title: Optional[str] = None


class UpdateTitleRequest(BaseModel):
    """Request to update conversation title. Issue #604."""

    title: str

    class Config:
        json_schema_extra = {"example": {"title": "Monday Planning Session"}}


class CreateConversationResponse(BaseModel):
    """Response for create conversation endpoint."""

    id: str
    title: str
    created_at: str
    lifecycle_state: str = "active"  # Issue #715


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = 50,
    offset: int = 0,
    search: str | None = None,
    state: str | None = None,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationListResponse:
    """
    List all conversations for the current user, optionally filtered by search and state.

    Issue #565: Populates conversation history sidebar.
    Issue #786: GLUE-HISTORY-DIFF - Added search parameter for History sidebar.
    Issue #715: Added state parameter for lifecycle filtering.

    Args:
        limit: Maximum number of conversations (default 50)
        offset: Number to skip for pagination
        search: Optional search string to filter by title (case-insensitive)
        state: Optional lifecycle state filter (active, archived). Default: active
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        ConversationListResponse with list of conversations and has_more flag
    """
    from services.shared_types import ConversationLifecycleState

    try:
        # Issue #715: Parse lifecycle state filter
        lifecycle_state = None
        if state:
            try:
                lifecycle_state = ConversationLifecycleState(state.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid state: {state}. Valid values: active, archived",
                )

        # Get conversations for user (with optional search filter)
        if search and search.strip():
            # search_for_user has its own default states (ACTIVE + ARCHIVED)
            states = [lifecycle_state] if lifecycle_state else None
            conversations = await conv_repo.search_for_user(
                current_user.sub,
                search.strip(),
                limit=limit + 1,
                offset=offset,
                states=states,
            )
        else:
            conversations = await conv_repo.list_for_user(
                current_user.sub,
                limit=limit + 1,
                offset=offset,
                state=lifecycle_state,
            )

        # Check if there are more
        has_more = len(conversations) > limit
        if has_more:
            conversations = conversations[:limit]

        # Build response with turn counts
        items = []
        for conv in conversations:
            turn_count = await conv_repo.get_turn_count(conv.id)
            items.append(
                ConversationListItem(
                    id=conv.id,
                    title=conv.title or "New conversation",
                    # Issue #788: Replace +00:00 with Z for JS Date parsing (can't have both)
                    created_at=(
                        conv.created_at.isoformat().replace("+00:00", "Z")
                        if conv.created_at
                        else ""
                    ),
                    updated_at=(
                        conv.last_activity_at.isoformat().replace("+00:00", "Z")
                        if conv.last_activity_at
                        else None
                    ),
                    turn_count=turn_count,
                    lifecycle_state=(
                        conv.lifecycle_state.value if conv.lifecycle_state else "active"
                    ),
                )
            )

        logger.debug(
            "Listed conversations",
            user_id=current_user.sub,
            count=len(items),
            has_more=has_more,
            state_filter=state,
        )

        return ConversationListResponse(conversations=items, has_more=has_more)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list conversations", error=str(e), user_id=current_user.sub)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list conversations",
        )


@router.post("", response_model=CreateConversationResponse)
async def create_conversation(
    request: CreateConversationRequest = CreateConversationRequest(),
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> CreateConversationResponse:
    """
    Create a new conversation.

    Issue #565: Used by "New Chat" button in sidebar.

    Args:
        request: Optional title for the conversation
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        CreateConversationResponse with new conversation details
    """
    try:
        conversation = await conv_repo.create(current_user.sub, title=request.title)

        logger.info(
            "Created new conversation",
            user_id=current_user.sub,
            conversation_id=conversation.id,
        )

        # Issue #788: Replace +00:00 with Z for JS Date parsing
        return CreateConversationResponse(
            id=conversation.id,
            title=conversation.title or "New conversation",
            created_at=(
                conversation.created_at.isoformat().replace("+00:00", "Z")
                if conversation.created_at
                else ""
            ),
            lifecycle_state=(
                conversation.lifecycle_state.value if conversation.lifecycle_state else "active"
            ),
        )

    except Exception as e:
        logger.error("Failed to create conversation", error=str(e), user_id=current_user.sub)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation",
        )


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationListItem:
    """
    Get a specific conversation by ID.

    Issue #565: Used when switching conversations.

    Args:
        conversation_id: The conversation ID to fetch
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        ConversationListItem with conversation details
    """
    try:
        conversation = await conv_repo.get_by_id(conversation_id, user_id=current_user.sub)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        # Verify ownership
        if conversation.user_id != current_user.sub:
            logger.warning(
                "Conversation access denied",
                user_id=current_user.sub,
                conversation_id=conversation_id,
                owner_id=conversation.user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        turn_count = await conv_repo.get_turn_count(conversation_id)

        # Issue #788: Replace +00:00 with Z for JS Date parsing
        return ConversationListItem(
            id=conversation.id,
            title=conversation.title or "New conversation",
            created_at=(
                conversation.created_at.isoformat().replace("+00:00", "Z")
                if conversation.created_at
                else ""
            ),
            updated_at=(
                conversation.last_activity_at.isoformat().replace("+00:00", "Z")
                if conversation.last_activity_at
                else None
            ),
            turn_count=turn_count,
            lifecycle_state=(
                conversation.lifecycle_state.value if conversation.lifecycle_state else "active"
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to get conversation",
            error=str(e),
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get conversation",
        )


@router.patch("/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: str,
    request: UpdateTitleRequest,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationListItem:
    """
    Update conversation title.

    Issue #604: Allows users to edit auto-generated conversation titles.

    Args:
        conversation_id: The conversation ID to update
        request: New title (1-100 characters)
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        Updated ConversationListItem
    """
    try:
        # Validate title length
        title = request.title.strip()
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty",
            )
        if len(title) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot exceed 100 characters",
            )

        # Get conversation and verify ownership
        conversation = await conv_repo.get_by_id(conversation_id, user_id=current_user.sub)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        if str(conversation.user_id) != str(current_user.sub):
            logger.warning(
                "Conversation title update denied",
                user_id=current_user.sub,
                conversation_id=conversation_id,
                owner_id=conversation.user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        # Update title
        await conv_repo.update_title(conversation_id, title)

        logger.info(
            "Updated conversation title",
            user_id=current_user.sub,
            conversation_id=conversation_id,
            new_title=title[:30],
        )

        # Return updated conversation
        turn_count = await conv_repo.get_turn_count(conversation_id)

        # Issue #788: Replace +00:00 with Z for JS Date parsing
        return ConversationListItem(
            id=conversation.id,
            title=title,
            created_at=(
                conversation.created_at.isoformat().replace("+00:00", "Z")
                if conversation.created_at
                else ""
            ),
            updated_at=(
                conversation.last_activity_at.isoformat().replace("+00:00", "Z")
                if conversation.last_activity_at
                else None
            ),
            turn_count=turn_count,
            lifecycle_state=(
                conversation.lifecycle_state.value if conversation.lifecycle_state else "active"
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update conversation title",
            error=str(e),
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation title",
        )


# --- Lifecycle state transitions (Issue #715, spec #858) ---


class UpdateStateRequest(BaseModel):
    """Request body for conversation state transitions."""

    state: str  # "active" or "archived"


class StateTransitionResponse(BaseModel):
    """Response for state transition operations."""

    id: str
    lifecycle_state: str
    message: str


@router.patch("/{conversation_id}/state")
async def update_conversation_state(
    conversation_id: str,
    request: UpdateStateRequest,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> StateTransitionResponse:
    """
    Update conversation lifecycle state (archive or reactivate).

    Issue #715: Conversation lifecycle state transitions.
    Spec #858 Section 2: ACTIVE ↔ ARCHIVED transitions.

    Args:
        conversation_id: The conversation ID to update
        request: Target state ("active" or "archived")
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        StateTransitionResponse with new state and confirmation message
    """
    try:
        target_state = request.state.lower()
        if target_state not in ("active", "archived"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid target state: {request.state}. Valid values: active, archived",
            )

        # Get conversation and verify ownership
        conversation = await conv_repo.get_by_id(conversation_id, user_id=current_user.sub)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        if str(conversation.user_id) != str(current_user.sub):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        # Execute state transition
        if target_state == "archived":
            result = await conv_repo.archive_conversation(conversation_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conversation cannot be archived (not in ACTIVE state)",
                )
            message = "Conversation archived"
        else:  # active (reactivate)
            result = await conv_repo.reactivate_conversation(conversation_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Conversation cannot be reactivated (not in ARCHIVED state)",
                )
            message = "Conversation reactivated"

        logger.info(
            "conversation_state_changed",
            user_id=current_user.sub,
            conversation_id=conversation_id,
            new_state=target_state,
        )

        return StateTransitionResponse(
            id=conversation_id,
            lifecycle_state=target_state,
            message=message,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to update conversation state",
            error=str(e),
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation state",
        )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> StateTransitionResponse:
    """
    Soft-delete a conversation.

    Issue #715: Conversation lifecycle state transitions.
    Spec #858 Section 2: ACTIVE/ARCHIVED → DELETED (terminal, no return).

    Args:
        conversation_id: The conversation ID to delete
        current_user: Current authenticated user
        conv_repo: Conversation repository (injected)

    Returns:
        StateTransitionResponse confirming deletion
    """
    try:
        # Get conversation and verify ownership
        conversation = await conv_repo.get_by_id(conversation_id, user_id=current_user.sub)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        if str(conversation.user_id) != str(current_user.sub):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        result = await conv_repo.delete_conversation(conversation_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conversation cannot be deleted (already deleted)",
            )

        logger.info(
            "conversation_deleted",
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )

        return StateTransitionResponse(
            id=conversation_id,
            lifecycle_state="deleted",
            message="Conversation deleted",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to delete conversation",
            error=str(e),
            user_id=current_user.sub,
            conversation_id=conversation_id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation",
        )
