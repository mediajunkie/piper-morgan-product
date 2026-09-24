"""
Standalone Integration Test for API Key Audit Logging

Tests audit logging integration with UserAPIKeyService (store, delete, rotate).
Bypasses pytest-asyncio fixtures to avoid event loop issues.

Issue #249 CORE-AUDIT-LOGGING Phase 3C
"""

import asyncio
import sys
from datetime import datetime
from uuid import UUID, uuid4

# Add project root to path
sys.path.insert(0, "/Users/xian/Development/piper-morgan")

from sqlalchemy import select

from services.database.models import AuditLog, User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.audit_logger import Action, EventType, Severity
from services.security.user_api_key_service import UserAPIKeyService


async def main():
    """Run API key audit logging integration tests"""
    print("=" * 80)
    print("API Key Audit Logging - Standalone Integration Test")
    print("=" * 80)
    print()

    # Test user
    test_user_id = uuid4()
    test_user_email = "api_key_audit@example.com"

    # Mock keychain service for testing
    class MockKeychainService:
        def __init__(self):
            self.keys = {}

        def store_api_key(self, provider: str, api_key: str, username: str):
            key = f"{username}_{provider}"
            self.keys[key] = api_key

        def get_api_key(self, provider: str, username: str):
            key = f"{username}_{provider}"
            return self.keys.get(key)

        def delete_api_key(self, provider: str, username: str):
            key = f"{username}_{provider}"
            if key in self.keys:
                del self.keys[key]

    # Mock LLM config service to bypass actual API validation
    class MockLLMConfigService:
        async def validate_api_key(self, provider: str, api_key: str) -> bool:
            # Always return True for testing
            return True

        async def validate_api_key_detailed(self, provider: str, api_key: str):
            # #1870: UserAPIKeyService.validate_user_key()/rotate_user_key() now
            # call validate_api_key_detailed() (the #1718 pattern) instead of the
            # bare-bool validate_api_key() — this mock needs to answer that call
            # too, or a validate=True path here raises AttributeError.
            from services.config.llm_config_service import ValidationResult

            return ValidationResult(provider=provider, is_valid=True)

    try:
        # ====================================================================
        # Test 1: Create Test User
        # ====================================================================
        print("Test 1: Creating test user...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Clean up any existing test user first
            result = await session.execute(select(User).where(User.id == test_user_id))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                # Clean up user's API keys first
                result = await session.execute(
                    select(UserAPIKey).where(UserAPIKey.user_id == test_user_id)
                )
                api_keys = result.scalars().all()
                for key in api_keys:
                    await session.delete(key)
                await session.delete(existing_user)
            await session.commit()

            # Create fresh test user
            test_user = User(
                id=test_user_id,
                username="api_key_audit_user",
                email=test_user_email,
                is_active=True,
            )
            session.add(test_user)
            await session.commit()
            print(f"✅ Created user: {test_user_id}")

        # ====================================================================
        # Test 2: Store API Key with Audit Logging
        # ====================================================================
        print("\nTest 2: Testing API key storage audit logging...")

        # Create service with mock dependencies
        mock_keychain = MockKeychainService()
        api_key_service = UserAPIKeyService(keychain_service=mock_keychain)
        api_key_service._llm_config = MockLLMConfigService()

        async with AsyncSessionFactory.session_scope_fresh() as session:
            user_key = await api_key_service.store_user_key(
                session=session,
                user_id=test_user_id,
                provider="openai",
                api_key="sk-test-key-12345",
                validate=True,
                audit_context={
                    "ip_address": "192.168.1.200",
                    "user_agent": "Test-Agent/3.0",
                    "request_id": "req_api_key_001",
                    "request_path": "/api/v1/keys/store",
                },
            )
            await session.commit()

            print(f"✅ API key stored: {user_key.provider}")

            # Verify audit log was created
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.API_KEY,
                    AuditLog.action == Action.KEY_STORED,
                    AuditLog.user_id == test_user_id,
                )
            )
            store_log = result.scalar_one()

            print(f"✅ Found audit log: {store_log.id}")
            print(f"   Event Type: {store_log.event_type}")
            print(f"   Action: {store_log.action}")
            print(f"   Resource Type: {store_log.resource_type}")
            print(f"   Resource ID: {store_log.resource_id}")
            print(f"   Status: {store_log.status}")
            print(f"   IP: {store_log.ip_address}")
            print(f"   Details: {store_log.details}")

            # Assertions
            assert store_log.event_type == EventType.API_KEY
            assert store_log.action == Action.KEY_STORED
            assert store_log.resource_type == "api_key"
            assert store_log.resource_id == "openai"
            assert store_log.status == "success"
            assert store_log.severity == Severity.INFO
            assert store_log.user_id == test_user_id
            assert store_log.ip_address == "192.168.1.200"
            assert store_log.user_agent == "Test-Agent/3.0"
            assert store_log.request_id == "req_api_key_001"
            assert store_log.request_path == "/api/v1/keys/store"
            assert store_log.details["provider"] == "openai"
            assert store_log.details["validated"] is True
            assert store_log.details["operation"] == "create"
            print(f"✅ Verified: API key storage audit log complete")

        # ====================================================================
        # Test 3: Update Existing API Key with Audit Logging
        # ====================================================================
        print("\nTest 3: Testing API key update audit logging...")

        async with AsyncSessionFactory.session_scope_fresh() as session:
            user_key = await api_key_service.store_user_key(
                session=session,
                user_id=test_user_id,
                provider="openai",
                api_key="sk-test-key-updated",
                validate=True,
                audit_context={
                    "ip_address": "192.168.1.201",
                    "user_agent": "Test-Agent/3.1",
                    "request_id": "req_api_key_002",
                    "request_path": "/api/v1/keys/update",
                },
            )
            await session.commit()

            print(f"✅ API key updated: {user_key.provider}")

            # Verify audit log for update was created
            result = await session.execute(
                select(AuditLog)
                .where(
                    AuditLog.event_type == EventType.API_KEY,
                    AuditLog.action == Action.KEY_STORED,
                    AuditLog.user_id == test_user_id,
                )
                .order_by(AuditLog.created_at.desc())
            )
            logs = result.scalars().all()

            # Should have 2 logs now (create from Test 2 + update from Test 3)
            assert len(logs) == 2
            update_log = logs[0]  # Most recent

            assert update_log.details["operation"] == "update"
            print(f"✅ Verified: API key update audit log has operation='update'")

        # ====================================================================
        # Test 4: Rotate API Key with Audit Logging
        # ====================================================================
        print("\nTest 4: Testing API key rotation audit logging...")

        async with AsyncSessionFactory.session_scope_fresh() as session:
            rotated_key = await api_key_service.rotate_user_key(
                session=session,
                user_id=test_user_id,
                provider="openai",
                new_api_key="sk-test-key-rotated",
                validate=True,
                audit_context={
                    "ip_address": "192.168.1.202",
                    "user_agent": "Test-Agent/3.2",
                    "request_id": "req_api_key_003",
                    "request_path": "/api/v1/keys/rotate",
                },
            )
            await session.commit()

            print(f"✅ API key rotated: {rotated_key.provider}")

            # Verify audit log for rotation was created
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.API_KEY,
                    AuditLog.action == Action.KEY_ROTATED,
                    AuditLog.user_id == test_user_id,
                )
            )
            rotate_log = result.scalar_one()

            print(f"✅ Found rotation audit log: {rotate_log.id}")
            print(f"   Old Value: {rotate_log.old_value}")
            print(f"   New Value: {rotate_log.new_value}")
            print(f"   Details: {rotate_log.details}")

            # Assertions
            assert rotate_log.event_type == EventType.API_KEY
            assert rotate_log.action == Action.KEY_ROTATED
            assert rotate_log.resource_type == "api_key"
            assert rotate_log.resource_id == "openai"
            assert rotate_log.status == "success"
            assert rotate_log.user_id == test_user_id
            assert rotate_log.ip_address == "192.168.1.202"
            assert rotate_log.old_value is not None
            assert rotate_log.new_value is not None
            assert "keychain_ref" in rotate_log.old_value
            assert "keychain_ref" in rotate_log.new_value
            assert rotate_log.details["zero_downtime"] is True
            print(f"✅ Verified: API key rotation audit log with old/new values")

        # ====================================================================
        # Test 5: Delete API Key with Audit Logging
        # ====================================================================
        print("\nTest 5: Testing API key deletion audit logging...")

        async with AsyncSessionFactory.session_scope_fresh() as session:
            deleted = await api_key_service.delete_user_key(
                session=session,
                user_id=test_user_id,
                provider="openai",
                audit_context={
                    "ip_address": "192.168.1.203",
                    "user_agent": "Test-Agent/3.3",
                    "request_id": "req_api_key_004",
                    "request_path": "/api/v1/keys/delete",
                },
            )
            await session.commit()

            print(f"✅ API key deleted: {deleted}")
            assert deleted is True

            # Verify audit log for deletion was created
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.event_type == EventType.API_KEY,
                    AuditLog.action == Action.KEY_DELETED,
                    AuditLog.user_id == test_user_id,
                )
            )
            delete_log = result.scalar_one()

            print(f"✅ Found deletion audit log: {delete_log.id}")
            print(f"   Old Value: {delete_log.old_value}")
            print(f"   Message: {delete_log.message}")

            # Assertions
            assert delete_log.event_type == EventType.API_KEY
            assert delete_log.action == Action.KEY_DELETED
            assert delete_log.resource_type == "api_key"
            assert delete_log.resource_id == "openai"
            assert delete_log.status == "success"
            assert delete_log.user_id == test_user_id
            assert delete_log.ip_address == "192.168.1.203"
            assert delete_log.old_value is not None
            assert "keychain_ref" in delete_log.old_value
            print(f"✅ Verified: API key deletion audit log with old_value")

        # ====================================================================
        # Test 6: Query All API Key Audit Logs
        # ====================================================================
        print("\nTest 6: Querying all API key audit logs for user...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(AuditLog)
                .where(
                    AuditLog.user_id == test_user_id,
                    AuditLog.event_type == EventType.API_KEY,
                )
                .order_by(AuditLog.created_at)
            )
            api_key_logs = result.scalars().all()

            print(f"✅ Found {len(api_key_logs)} API key audit logs for user")
            for log in api_key_logs:
                print(f"   - {log.event_type}.{log.action}: {log.message}")

            # Should have 4 logs:
            # - KEY_STORED (create, Test 2)
            # - KEY_STORED (update, Test 3)
            # - KEY_ROTATED (Test 4)
            # - KEY_DELETED (Test 5)
            assert len(api_key_logs) == 4
            actions = [log.action for log in api_key_logs]
            assert actions.count(Action.KEY_STORED) == 2  # create + update
            assert actions.count(Action.KEY_ROTATED) == 1
            assert actions.count(Action.KEY_DELETED) == 1
            print(f"✅ Verified: All 4 API key operations logged correctly")

        print("\n" + "=" * 80)
        print("✅ ALL API KEY AUDIT LOGGING TESTS PASSED (6/6 = 100%)")
        print("=" * 80)
        print()
        print("Summary:")
        print("  ✅ API key storage audit logging works (create + update)")
        print("  ✅ API key rotation audit logging works (with old/new values)")
        print("  ✅ API key deletion audit logging works (with old_value)")
        print("  ✅ Audit context captured correctly (IP, user_agent, request_id, path)")
        print("  ✅ All API key audit events queryable by user_id and event_type")
        print("  ✅ Resource type and resource_id correctly set to 'api_key' and provider")
        print()
        print("Phase 3 (API Key Integration) functionality CONFIRMED WORKING! 🎉")
        print()

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        # Cleanup
        print("Cleaning up test data...")
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Delete API key audit logs
            result = await session.execute(
                select(AuditLog).where(
                    AuditLog.user_id == test_user_id,
                    AuditLog.event_type == EventType.API_KEY,
                )
            )
            logs = result.scalars().all()
            for log in logs:
                await session.delete(log)

            # Delete test user (cascade will delete any remaining user_api_keys)
            result = await session.execute(select(User).where(User.id == test_user_id))
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)

            await session.commit()
            print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(main())
