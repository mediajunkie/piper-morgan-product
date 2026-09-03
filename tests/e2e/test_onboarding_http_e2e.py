"""
Issue #490: TRUE End-to-End HTTP Tests for Portfolio Onboarding

These tests hit the REAL HTTP endpoints with REAL services.
No mocking of business logic - only database session isolation.

Pattern-045 Compliance:
- Tests the actual user experience, not mocked components
- If these tests pass, the feature works for users
- If these tests fail, users will see broken behavior

Test Flow (matches manual testing):
1. Create user with 0 projects
2. Login via /auth/login
3. Say "Hello" via /api/v1/intent
4. Expect onboarding prompt (not normal greeting)
5. Say "My project is X"
6. Expect acknowledgment (not echo, not identity response)

Fixtures: e2e_db_session, e2e_test_user, e2e_client from conftest.py (#352)
"""

import pytest

# ADR-059: Onboarding on ice
pytestmark = pytest.mark.skip(reason="ADR-059: onboarding on ice")


from uuid import uuid4

import pytest
from sqlalchemy import text


class TestOnboardingHTTPE2E:
    """
    TRUE E2E tests for portfolio onboarding.

    These tests reproduce the exact manual testing flow:
    1. Login
    2. Send greeting
    3. Send project info
    4. Verify responses
    """

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_new_user_greeting_triggers_onboarding(
        self, e2e_client, e2e_test_user, e2e_db_session
    ):
        """
        Issue #490: New user saying 'Hello' should trigger onboarding.

        This is the FIRST manual test that kept failing.
        If this passes, the greeting->onboarding path works.
        """
        user_id, username, password = e2e_test_user

        # Step 1: Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"

        # Get auth cookie
        cookies = login_response.cookies

        # Step 2: Send greeting via /api/v1/intent
        intent_response = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": f"e2e-greeting-onboarding-{uuid4()}"},
            cookies=cookies,
        )

        assert intent_response.status_code == 200, f"Intent failed: {intent_response.text}"
        result = intent_response.json()

        # Step 3: Verify onboarding is triggered
        # The response message should contain onboarding indicators.
        # LLM phrasing varies, so check for broad semantic markers.
        message = result.get("message", "").lower()

        # MUST contain onboarding indicators (broad matching for LLM variation)
        onboarding_indicators = [
            "portfolio",
            "project",
            "workspace",
            "setting up",
            "set up",
            "get started",
            "new here",
        ]
        assert any(
            phrase in message for phrase in onboarding_indicators
        ), f"Expected onboarding prompt, got: {result.get('message')}"

        # MUST NOT be a generic identity-only response (no onboarding context)
        is_identity_only = "i'm piper morgan" in message and not any(
            w in message for w in ["portfolio", "project", "workspace", "new", "set"]
        )
        assert (
            not is_identity_only
        ), f"Got identity response instead of onboarding: {result.get('message')}"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_project_info_not_echoed(self, e2e_client, e2e_test_user, e2e_db_session):
        """
        Issue #560: User providing project info should NOT be echoed back.

        This catches the echo bug that was found via manual testing.
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        cookies = login_response.cookies
        session_id = f"e2e-project-info-not-echoed-{uuid4()}"

        # Send greeting first (to trigger onboarding)
        await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": session_id},
            cookies=cookies,
        )

        # Now send project info
        project_message = "My main project is called Piper Morgan"
        intent_response = await e2e_client.post(
            "/api/v1/intent",
            json={"message": project_message, "session_id": session_id},
            cookies=cookies,
        )

        assert intent_response.status_code == 200
        result = intent_response.json()
        response_message = result.get("message", "")

        # CRITICAL: Response should NOT echo user's exact input
        assert (
            response_message.lower() != project_message.lower()
        ), f"ECHO BUG: Response echoed user input verbatim: {response_message}"

        # Response should NOT be the identity response
        assert (
            "i'm piper morgan, your ai product management" not in response_message.lower()
        ), f"Got identity response instead of onboarding continuation: {response_message}"

        # Response should acknowledge the project (ideal case)
        # Or at least be a reasonable response (not echo, not error)
        assert len(response_message) > 10, f"Response too short: {response_message}"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_full_onboarding_flow(self, e2e_client, e2e_test_user, e2e_db_session):
        """
        Issue #490: Complete onboarding flow from greeting to project capture.

        This is the full happy path that users should experience.
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        cookies = login_response.cookies
        session_id = f"e2e-{uuid4()}"

        # Turn 1: Greeting -> Onboarding prompt
        response1 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hi there!", "session_id": session_id},
            cookies=cookies,
        )
        result1 = response1.json()
        msg1 = result1.get("message", "").lower()

        assert (
            "portfolio" in msg1 or "project" in msg1
        ), f"Turn 1: Expected onboarding, got: {result1.get('message')}"

        # Turn 2: User accepts -> Should ask for project
        response2 = await e2e_client.post(
            "/api/v1/intent",
            json={
                "message": "Yes, I'd like to tell you about my projects",
                "session_id": session_id,
            },
            cookies=cookies,
        )
        result2 = response2.json()
        msg2 = result2.get("message", "")

        # Should NOT echo
        assert "yes, i'd like" not in msg2.lower(), f"Turn 2: Echo detected: {msg2}"
        # Should NOT be identity
        assert "i'm piper morgan, your ai" not in msg2.lower(), f"Turn 2: Wrong response: {msg2}"

        # Turn 3: User provides project info
        response3 = await e2e_client.post(
            "/api/v1/intent",
            json={
                "message": "The main one is Piper Morgan, a PM assistant",
                "session_id": session_id,
            },
            cookies=cookies,
        )
        result3 = response3.json()
        msg3 = result3.get("message", "")

        # Should NOT be verbatim echo (exact message returned)
        # Note: The handler may include project name in acknowledgment - that's OK
        assert (
            msg3.lower() != "the main one is piper morgan, a pm assistant"
        ), f"Turn 3: Verbatim echo detected: {msg3}"
        # Should NOT be identity response
        assert (
            "i'm piper morgan, your ai" not in msg3.lower()
        ), f"Turn 3: Got identity response instead of onboarding: {msg3}"
        # Should acknowledge project (start with "Got it" or similar)
        assert msg3.lower().startswith(
            "got it"
        ), f"Turn 3: Expected project acknowledgment, got: {msg3}"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_full_onboarding_through_completion(
        self, e2e_client, e2e_test_user, e2e_db_session
    ):
        """
        Issue #766: Full onboarding flow through "done" to completion.

        Reproduces the "Failed to fetch" bug found during live testing:
        1. Login
        2. "Hello" -> onboarding starts
        3. "Yes" -> accepts, enters GATHERING
        4. "My project is Alpha" -> captures project
        5. "That's it for now" -> transitions to CONFIRMING (CRASH POINT)
        6. "Yes" -> completes onboarding
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        cookies = login_response.cookies
        session_id = f"e2e-completion-{uuid4()}"

        # Turn 1: Greeting -> Onboarding prompt
        r1 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello!", "session_id": session_id},
            cookies=cookies,
        )
        assert r1.status_code == 200, f"Turn 1 failed: {r1.status_code} - {r1.text}"
        msg1 = r1.json().get("message", "")
        print(f"Turn 1 response: {msg1}")

        # Turn 2: Accept onboarding
        r2 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Yes, let's do it", "session_id": session_id},
            cookies=cookies,
        )
        assert r2.status_code == 200, f"Turn 2 failed: {r2.status_code} - {r2.text}"
        msg2 = r2.json().get("message", "")
        print(f"Turn 2 response: {msg2}")

        # Turn 3: Provide project info
        r3 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "My project is called Alpha", "session_id": session_id},
            cookies=cookies,
        )
        assert r3.status_code == 200, f"Turn 3 failed: {r3.status_code} - {r3.text}"
        msg3 = r3.json().get("message", "")
        print(f"Turn 3 response: {msg3}")

        # Turn 4: "That's it for now" — THIS IS THE CRASH POINT
        r4 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "That's it for now", "session_id": session_id},
            cookies=cookies,
        )
        assert r4.status_code == 200, f"Turn 4 CRASHED: {r4.status_code} - {r4.text}"
        msg4 = r4.json().get("message", "")
        print(f"Turn 4 response: {msg4}")

        # Turn 5: Confirm (yes / save)
        r5 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Yes", "session_id": session_id},
            cookies=cookies,
        )
        assert r5.status_code == 200, f"Turn 5 failed: {r5.status_code} - {r5.text}"
        msg5 = r5.json().get("message", "")
        print(f"Turn 5 response: {msg5}")

        # Verify: projects should be persisted
        result = await e2e_db_session.execute(
            text("SELECT name, is_default FROM projects WHERE owner_id = :uid"),
            {"uid": user_id},
        )
        projects = result.fetchall()
        print(f"Persisted projects: {projects}")

        # Should have at least one project
        assert len(projects) >= 1, f"Expected persisted projects, got {len(projects)}"

        # Issue #815: Single project should have is_default=True
        if len(projects) == 1:
            assert (
                projects[0][1] is True
            ), f"Single project should have is_default=True, got {projects[0][1]}"

        # Cleanup projects
        await e2e_db_session.execute(
            text("DELETE FROM projects WHERE owner_id = :uid"),
            {"uid": user_id},
        )
        await e2e_db_session.commit()

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_orphaned_message_after_session_loss(
        self, e2e_client, e2e_test_user, e2e_db_session
    ):
        """
        Issue #766: What happens when onboarding session is lost (server restart)
        and user sends "That's it for now" to normal intent classifier?

        Hypothesis: "Failed to fetch" may occur when a mid-flow message
        hits the normal classifier instead of the onboarding handler.
        """
        user_id, username, password = e2e_test_user

        # Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200
        cookies = login_response.cookies
        session_id = f"e2e-orphan-{uuid4()}"

        # Send "That's it for now" with NO active onboarding session
        # This simulates what happens after a server restart mid-flow
        r = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "That's it for now", "session_id": session_id},
            cookies=cookies,
        )
        assert r.status_code == 200, f"Orphaned message CRASHED: {r.status_code} - {r.text}"
        msg = r.json().get("message", "")
        print(f"Orphaned 'That's it for now' response: {msg}")
        assert len(msg) > 0, "Empty response for orphaned message"

    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_onboarding_with_existing_projects(
        self, e2e_client, e2e_test_user, e2e_db_session
    ):
        """
        Issue #766: Reproduce "Failed to fetch" with user who has EXISTING projects.

        The PM's test user "glue" already had 4 projects in the database.
        This tests whether existing projects cause issues during onboarding completion.
        """
        user_id, username, password = e2e_test_user

        # Pre-create existing projects (simulating the PM's "glue" user with 4 projects)
        for proj_name in ["Decision Reviews", "OneJob", "Piper Morgan", "Wooshville"]:
            await e2e_db_session.execute(
                text(
                    """
                    INSERT INTO projects (id, owner_id, name, description, is_default, is_archived, created_at, updated_at)
                    VALUES (:id, CAST(:owner_id AS uuid), :name, '', false, false, now(), now())
                """
                ),
                {"id": str(uuid4()), "owner_id": user_id, "name": proj_name},
            )
        await e2e_db_session.commit()

        # Verify user has 4 projects
        result = await e2e_db_session.execute(
            text("SELECT COUNT(*) FROM projects WHERE owner_id = :uid"),
            {"uid": user_id},
        )
        assert result.scalar() == 4

        # Login
        login_response = await e2e_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )
        assert login_response.status_code == 200
        cookies = login_response.cookies
        session_id = f"e2e-existing-{uuid4()}"

        # Turn 1: Greeting (user has projects - will this still trigger onboarding?)
        r1 = await e2e_client.post(
            "/api/v1/intent",
            json={"message": "Hello!", "session_id": session_id},
            cookies=cookies,
        )
        assert r1.status_code == 200, f"Turn 1 failed: {r1.status_code} - {r1.text}"
        msg1 = r1.json().get("message", "")
        print(f"Turn 1 (has projects): {msg1}")

        # Check if onboarding triggered or not
        msg1_lower = msg1.lower()
        if "portfolio" not in msg1_lower and "project" not in msg1_lower:
            print("INFO: Onboarding NOT triggered for user with existing projects (expected)")
            # Still test the full flow by manually starting onboarding
            # Skip rest of test - this path doesn't trigger onboarding
        else:
            print("INFO: Onboarding DID trigger for user with existing projects")

            # Continue flow: Accept -> Project -> Done -> Confirm
            r2 = await e2e_client.post(
                "/api/v1/intent",
                json={"message": "Sure, let's go", "session_id": session_id},
                cookies=cookies,
            )
            assert r2.status_code == 200, f"Turn 2 failed: {r2.status_code}"
            print(f"Turn 2: {r2.json().get('message', '')}")

            r3 = await e2e_client.post(
                "/api/v1/intent",
                json={"message": "My new project is Beta", "session_id": session_id},
                cookies=cookies,
            )
            assert r3.status_code == 200, f"Turn 3 failed: {r3.status_code}"
            print(f"Turn 3: {r3.json().get('message', '')}")

            r4 = await e2e_client.post(
                "/api/v1/intent",
                json={"message": "That's it for now", "session_id": session_id},
                cookies=cookies,
            )
            assert r4.status_code == 200, f"Turn 4 (CRASH POINT): {r4.status_code} - {r4.text}"
            print(f"Turn 4: {r4.json().get('message', '')}")

            r5 = await e2e_client.post(
                "/api/v1/intent",
                json={"message": "Yes", "session_id": session_id},
                cookies=cookies,
            )
            assert r5.status_code == 200, f"Turn 5 failed: {r5.status_code}"
            print(f"Turn 5: {r5.json().get('message', '')}")

        # Cleanup all projects for this user
        await e2e_db_session.execute(
            text("DELETE FROM projects WHERE owner_id = :uid"),
            {"uid": user_id},
        )
        await e2e_db_session.commit()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_degradation_response_not_echo(e2e_client):
    """
    Issue #560: Even error responses should NOT echo user input.

    When services fail, the degradation message should be shown,
    not the user's original message.
    """
    # Send request without auth (will trigger some error path)
    response = await e2e_client.post(
        "/api/v1/intent",
        json={
            "message": "Test message that should not be echoed",
            "session_id": f"e2e-degradation-not-echo-{uuid4()}",
        },
    )

    result = response.json()
    message = result.get("message", "")

    # Even if it errors, should NOT echo
    assert (
        message != "Test message that should not be echoed"
    ), f"Error response echoed user input: {message}"
