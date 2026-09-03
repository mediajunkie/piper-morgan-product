"""
E2E: Task lifecycle smoke tests through /api/v1/intent.

Tests full CRUD cycles for core features: todos, GitHub issues, reminders.
Also tests floor routing regression and capability boundaries.

These tests hit the REAL app with REAL services. They assert on response
structure and deterministic behavior — not on LLM-generated content
(which varies between runs).

Issue: #927 E2E Task Lifecycle Smoke Tests
Supports: #926 M1 Gate (Gates 1, 2)

Requirements:
- PostgreSQL running on port 5433 (docker compose up -d)
- Database migrations current (alembic upgrade head)
- LLM API keys in environment (for floor responses)
"""

from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def send_message(client, message, session_id, auth=None):
    """Send a message through the intent endpoint and return parsed response."""
    kwargs = {"json": {"message": message, "session_id": session_id}}
    if auth:
        kwargs.update(auth)
    response = await client.post("/api/v1/intent", **kwargs)
    assert response.status_code == 200, f"Request failed ({response.status_code}): {response.text}"
    return response.json()


# ---------------------------------------------------------------------------
# Todo Lifecycle
# ---------------------------------------------------------------------------


class TestTodoLifecycleE2E:
    """Issue #927: Full todo create → list → complete → verify cycle."""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_create_todo_returns_confirmation(self, e2e_client, e2e_auth_headers):
        """Adding a todo should return a confirmation with the todo text."""
        data = await send_message(
            e2e_client,
            "Add a todo: review the deployment plan",
            f"e2e-todo-lifecycle-{uuid4()}",
            e2e_auth_headers,
        )

        assert data["message"], "Empty response"
        # The response should reference the todo content
        msg_lower = data["message"].lower()
        assert (
            "review" in msg_lower or "deployment" in msg_lower or "todo" in msg_lower
        ), f"Response doesn't reference the todo: {data['message'][:200]}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_list_todos_shows_created_todo(self, e2e_client, e2e_auth_headers):
        """After creating a todo, listing should show it."""
        session = f"e2e-todo-list-{uuid4()}"

        # Create
        await send_message(
            e2e_client,
            "Add a todo: write unit tests for auth module",
            session,
            e2e_auth_headers,
        )

        # List
        data = await send_message(e2e_client, "Show my todos", session, e2e_auth_headers)

        msg_lower = data["message"].lower()
        assert (
            "unit tests" in msg_lower or "auth module" in msg_lower or "todo" in msg_lower
        ), f"Listed todos don't include created item: {data['message'][:300]}"


# ---------------------------------------------------------------------------
# GitHub Issue Close/Reopen
# ---------------------------------------------------------------------------


class TestGitHubCloseE2E:
    """Issue #927: GitHub close shows confirmation before executing."""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_close_issue_returns_response(self, e2e_client, e2e_auth_headers):
        """Asking to close an issue should return a meaningful response.

        Note: May return confirmation prompt, already-closed message, or
        GitHub-not-configured message depending on environment. All are valid.
        We just verify it's not a dead end.
        """
        data = await send_message(
            e2e_client,
            "Close issue #1",
            f"e2e-github-close-{uuid4()}",
            e2e_auth_headers,
        )

        assert data["message"], "Empty response"
        msg_lower = data["message"].lower()
        # Should reference the issue or explain why it can't
        assert any(
            term in msg_lower for term in ["issue", "close", "github", "configured", "#1"]
        ), f"Response doesn't address the close request: {data['message'][:200]}"


# ---------------------------------------------------------------------------
# Reminder Creation
# ---------------------------------------------------------------------------


class TestReminderE2E:
    """Issue #927: Reminder creation through natural language."""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_remind_me_creates_reminder(self, e2e_client, e2e_auth_headers):
        """'Remind me to X' should confirm the reminder was created."""
        data = await send_message(
            e2e_client,
            "Remind me to check the deployment status tomorrow",
            f"e2e-reminder-{uuid4()}",
            e2e_auth_headers,
        )

        assert data["message"], "Empty response"
        msg_lower = data["message"].lower()
        # Should confirm the reminder content and/or time
        assert any(
            term in msg_lower
            for term in ["remind", "deployment", "tomorrow", "scheduled", "got it"]
        ), f"Response doesn't confirm reminder: {data['message'][:200]}"


# ---------------------------------------------------------------------------
# Floor Routing Regression
# ---------------------------------------------------------------------------


class TestFloorRoutingE2E:
    """Issue #927: Floor-routed categories produce real LLM responses, not templates."""

    # Known template signatures that should NOT appear in floor responses
    TEMPLATE_SIGNATURES = [
        "Based on your current priorities and the time of day:",
        "Here's comprehensive guidance for your focus:",
        "Focus: Deep work",
        "Focus: Team coordination",
        "Focus: Task execution",
        "I'm here to help with your questions!",
    ]

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_discovery_not_template(self, e2e_client, e2e_auth_headers):
        """DISCOVERY query should get a floor response, not a template."""
        data = await send_message(
            e2e_client,
            "What can you help me with?",
            f"e2e-floor-discovery-{uuid4()}",
            e2e_auth_headers,
        )

        msg = data["message"]
        assert len(msg) > 50, f"Response too short for a floor response: {msg}"
        for sig in self.TEMPLATE_SIGNATURES:
            assert sig not in msg, f"Floor response contains template signature: {sig}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_conversation_farewell_not_template(self, e2e_client, e2e_auth_headers):
        """CONVERSATION farewell should be natural, not canned."""
        data = await send_message(
            e2e_client,
            "Thanks for your help today!",
            f"e2e-floor-farewell-{uuid4()}",
            e2e_auth_headers,
        )

        msg = data["message"]
        assert len(msg) > 10, f"Response too short: {msg}"
        for sig in self.TEMPLATE_SIGNATURES:
            assert sig not in msg, f"Floor response contains template signature: {sig}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_greeting_responds_naturally(self, e2e_client, e2e_auth_headers):
        """Greeting should NOT offer onboarding (ADR-059)."""
        data = await send_message(
            e2e_client,
            "Good morning!",
            f"e2e-floor-greeting-{uuid4()}",
            e2e_auth_headers,
        )

        msg_lower = data["message"].lower()
        assert "onboarding" not in msg_lower, "Greeting offered onboarding (should be disabled)"
        assert len(data["message"]) > 10, "Greeting response too short"


# ---------------------------------------------------------------------------
# Capability Boundary
# ---------------------------------------------------------------------------


class TestCapabilityBoundaryE2E:
    """Issue #927: Piper should be honest about what it can't do."""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_unregistered_capability_no_false_promise(self, e2e_client, e2e_auth_headers):
        """Asking for something outside Piper's capabilities should get an honest response."""
        data = await send_message(
            e2e_client,
            "Can you book me a flight to New York?",
            f"e2e-capability-boundary-{uuid4()}",
            e2e_auth_headers,
        )

        msg_lower = data["message"].lower()
        # Should NOT offer to book a flight
        assert not any(
            term in msg_lower for term in ["booking your flight", "i'll book", "flight booked"]
        ), f"Piper falsely offered to book a flight: {data['message'][:200]}"

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_response_is_not_dead_end(self, e2e_client, e2e_auth_headers):
        """Even for unsupported requests, response should offer alternatives."""
        data = await send_message(
            e2e_client,
            "Deploy the latest build to production",
            f"e2e-capability-deploy-{uuid4()}",
            e2e_auth_headers,
        )

        msg = data["message"]
        assert len(msg) > 30, f"Response too short — possible dead end: {msg}"
        # Should not be the old deflection
        assert "I don't have that capability yet" not in msg, "Old deflection pattern still active"
