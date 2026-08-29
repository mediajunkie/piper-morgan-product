# CORE-KEYS-ROTATION-WORKFLOW: Apply Rotation Reminders to Key Management Workflows

**Sprint**: TBD (A8 or MVP)
**Priority**: Medium
**Effort**: 30-45 minutes
**Impact**: Medium (security automation)

---

## Problem

Issue #250 (CORE-KEYS-ROTATION-REMINDERS) created a comprehensive policy engine for tracking API key age and generating rotation reminders:

```python
# What exists now:
rotation_policy = RotationPolicy()
status = rotation_policy.check_key_age(key, provider)
# Returns: needs_rotation, days_old, severity, message

# What's missing:
# - Automated rotation workflow
# - User notifications
# - Guided rotation process
# - Key replacement assistance
```

Currently, rotation reminders are **displayed** but require manual action. There's no integrated workflow to help users actually rotate their keys.

**Result**: Users see warnings but may not know how to rotate keys efficiently.

---

## Proposed Solution

Build an integrated key rotation workflow that:
1. **Detects** keys needing rotation (existing policy engine)
2. **Notifies** users with actionable alerts
3. **Guides** users through rotation process
4. **Assists** with key replacement
5. **Verifies** new key strength before storage

---

## Current Rotation Detection (From #250)

### What Works

```python
# services/security/rotation_policy.py

class RotationPolicy:
    """Policy engine for key rotation"""

    DEFAULT_ROTATION_DAYS = 90
    PROVIDER_OVERRIDES = {
        'openai': 60,    # Rotate every 60 days
        'github': 180    # Rotate every 180 days
    }

    def check_key_age(self, key: APIKey, provider: str) -> RotationStatus:
        """Check if key needs rotation"""
        days_old = (datetime.utcnow() - key.created_at).days
        rotation_days = self.PROVIDER_OVERRIDES.get(provider, self.DEFAULT_ROTATION_DAYS)

        if days_old >= rotation_days:
            return RotationStatus(
                needs_rotation=True,
                days_old=days_old,
                severity="critical",
                message=f"Key is {days_old} days old (policy: {rotation_days} days)"
            )
        # ... other severity levels
```

**Status**: ✅ Detection works, ⏳ Action missing

---

## Proposed Rotation Workflow

### 1. Interactive Rotation Command

```python
# New CLI command
$ python main.py rotate-key <provider>

# Example session:
$ python main.py rotate-key openai

🔄 Key Rotation Workflow: OpenAI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Status:
  Provider: OpenAI
  Key Age: 75 days old
  Policy: 60 days
  Status: ⚠️  Rotation recommended

Step 1: Generate New Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Follow these steps to generate a new OpenAI API key:

1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name (e.g., "Piper Morgan - Nov 2025")
4. Copy the key (starts with sk-...)
5. Paste it here when ready

⚠️  Important:
   - The old key will continue working until you revoke it
   - You can test the new key before revoking the old one
   - Keep the old key as backup until rotation is verified

Ready to continue? (y/n): y

Step 2: Enter New Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Paste your new OpenAI API key: sk-...

✅ Key received
🔍 Validating key format...
✅ Format valid
🔍 Checking key strength...
✅ Strong key (entropy: 8.2 bits/char)
🔍 Testing key with OpenAI API...
✅ Key works! (Account: user@example.com)

Step 3: Store New Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Where would you like to store the new key?
1) Replace existing key (recommended)
2) Store as additional key (for testing)
3) Cancel rotation

Your choice (1-3): 1

✅ New key stored in macOS Keychain
✅ Old key backed up to: ~/.piper/keys/openai-backup-2025-10-23.enc

Step 4: Verify Rotation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Testing Piper Morgan with new key...
✅ All systems functional

Step 5: Revoke Old Key (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now that the new key is working, you should revoke the old key:

1. Visit: https://platform.openai.com/api-keys
2. Find the old key (created 75 days ago)
3. Click "Revoke"

Have you revoked the old key? (y/n/skip): y

✅ Key Rotation Complete!

Summary:
  Old Key: Created 75 days ago → Revoked
  New Key: Created today → Active
  Next Rotation: 60 days from now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 2. Automated Rotation Detection & Notification

```python
# services/security/rotation_monitor.py

class RotationMonitor:
    """Monitor keys and trigger rotation workflows"""

    async def check_all_keys(self, user_id: str) -> list[RotationAlert]:
        """Check all keys for rotation needs"""
        alerts = []

        policy = RotationPolicy()
        keys = await self._get_user_keys(user_id)

        for key in keys:
            status = policy.check_key_age(key, key.provider)

            if status.needs_rotation:
                alert = RotationAlert(
                    provider=key.provider,
                    days_old=status.days_old,
                    severity=status.severity,
                    message=status.message,
                    action_url=self._get_rotation_guide_url(key.provider)
                )
                alerts.append(alert)

        return alerts

    async def send_rotation_alerts(self, user_id: str):
        """Send rotation alerts to user"""
        alerts = await self.check_all_keys(user_id)

        if not alerts:
            return

        # Send via configured channels
        await self._send_email_alert(user_id, alerts)
        await self._send_slack_alert(user_id, alerts)
        await self._log_audit_event(user_id, alerts)
```

---

### 3. Provider-Specific Rotation Guides

```python
ROTATION_GUIDES = {
    'openai': {
        'key_generation_url': 'https://platform.openai.com/api-keys',
        'steps': [
            'Click "Create new secret key"',
            'Give it a descriptive name',
            'Copy the key (starts with sk-...)',
            'Keep the key secret - it won\'t be shown again'
        ],
        'revocation_steps': [
            'Visit API keys page',
            'Find the old key',
            'Click "Revoke"'
        ]
    },
    'anthropic': {
        'key_generation_url': 'https://console.anthropic.com/settings/keys',
        'steps': [
            'Click "Create Key"',
            'Enter a name for the key',
            'Copy the key (starts with sk-ant-...)',
            'Store it securely'
        ],
        'revocation_steps': [
            'Visit Keys page',
            'Find the old key',
            'Click "Delete"'
        ]
    },
    'github': {
        'key_generation_url': 'https://github.com/settings/tokens',
        'steps': [
            'Click "Generate new token" → "Fine-grained token"',
            'Set expiration date',
            'Select repository access',
            'Copy the token (starts with github_pat_...)'
        ],
        'revocation_steps': [
            'Visit Personal access tokens',
            'Find the old token',
            'Click "Revoke"'
        ]
    }
}
```

---

### 4. Key Backup & Rollback

```python
class KeyBackupService:
    """Backup keys before rotation for rollback capability"""

    async def backup_key(
        self,
        provider: str,
        key_value: str,
        user_id: str
    ) -> str:
        """
        Backup key before rotation

        Returns: backup file path
        """
        # Encrypt the key
        encrypted = self._encrypt_key(key_value)

        # Generate backup filename
        timestamp = datetime.utcnow().strftime('%Y-%m-%d')
        filename = f"{provider}-backup-{timestamp}.enc"
        backup_path = self._get_backup_dir(user_id) / filename

        # Write encrypted backup
        backup_path.write_bytes(encrypted)

        # Log backup event
        await self._log_backup(user_id, provider, backup_path)

        return str(backup_path)

    async def rollback_key(self, backup_path: str, user_id: str):
        """Restore key from backup"""
        # Read encrypted backup
        encrypted = Path(backup_path).read_bytes()

        # Decrypt key
        key_value = self._decrypt_key(encrypted)

        # Restore to keychain
        await self._store_key(key_value, user_id)

        # Log rollback event
        await self._log_rollback(user_id, backup_path)
```

---

### 5. Integration with Key Validation

```python
async def rotate_key_interactive(provider: str, user_id: str):
    """Interactive key rotation workflow"""

    # Step 1: Show current status
    current_key = await get_current_key(provider, user_id)
    status = rotation_policy.check_key_age(current_key, provider)
    print_rotation_status(status)

    # Step 2: Show provider-specific guide
    guide = ROTATION_GUIDES[provider]
    print_rotation_guide(guide)

    # Step 3: Collect new key
    new_key = input("Paste your new API key: ").strip()

    # Step 4: Validate new key (from #252!)
    validator = KeyValidator()
    report = await validator.validate_key(new_key, provider)

    if not report.is_valid:
        print(f"❌ Key validation failed: {report.issues}")
        return

    print(f"✅ Key validated successfully")

    # Step 5: Test new key
    if await test_key_works(new_key, provider):
        print(f"✅ Key works with {provider} API")
    else:
        print(f"❌ Key test failed - key may not be active yet")
        return

    # Step 6: Backup old key
    backup_path = await backup_service.backup_key(provider, current_key.value, user_id)
    print(f"✅ Old key backed up to: {backup_path}")

    # Step 7: Store new key
    await store_key(new_key, provider, user_id)
    print(f"✅ New key stored")

    # Step 8: Prompt for revocation
    print_revocation_guide(guide)
    confirmed = input("Have you revoked the old key? (y/n/skip): ")

    if confirmed.lower() == 'y':
        await mark_key_revoked(current_key.id)
        print(f"✅ Rotation complete!")
    else:
        print(f"⚠️  Remember to revoke the old key when ready")
```

---

## Status Checker Integration

```python
# Enhanced status output (from #255)

async def show_key_rotation_status():
    """Show rotation status in status checker"""

    print("\n=== Key Rotation Status ===\n")

    monitor = RotationMonitor()
    alerts = await monitor.check_all_keys(user_id)

    if not alerts:
        print("✅ All keys are current (no rotation needed)\n")
        return

    for alert in alerts:
        icon = "🔴" if alert.severity == "critical" else "⚠️"
        print(f"{icon} {alert.provider}:")
        print(f"   Age: {alert.days_old} days old")
        print(f"   {alert.message}")
        print(f"   Action: python main.py rotate-key {alert.provider}\n")
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] Interactive rotation command works for all providers
- [ ] Provider-specific guides displayed
- [ ] New key validation before storage (integrates #252)
- [ ] Old key backup with encryption
- [ ] Rollback capability if rotation fails
- [ ] Audit logging of all rotation events

### User Experience
- [ ] Clear step-by-step guidance
- [ ] Progress indicators during validation/testing
- [ ] Actionable error messages
- [ ] Success confirmation with summary
- [ ] Revocation reminder with links

### Integration Requirements
- [ ] Uses KeyValidator from #252
- [ ] Uses RotationPolicy from #250
- [ ] Updates status checker from #255
- [ ] Logs to audit system

---

## Testing

### Unit Tests

```python
async def test_rotation_workflow_happy_path():
    """Test successful key rotation"""
    # Simulate user input
    mock_input(['y', 'sk-new-key-12345', '1', 'y'])

    # Run rotation
    await rotate_key_interactive('openai', user_id)

    # Verify new key stored
    new_key = await get_current_key('openai', user_id)
    assert new_key.value == 'sk-new-key-12345'

    # Verify backup created
    backups = list_backups(user_id, 'openai')
    assert len(backups) == 1

async def test_rotation_with_invalid_key():
    """Test rotation fails gracefully with invalid key"""
    mock_input(['y', 'invalid-key', '1'])

    await rotate_key_interactive('openai', user_id)

    # Old key unchanged
    current_key = await get_current_key('openai', user_id)
    assert current_key.value == 'sk-old-key-12345'

async def test_key_rollback():
    """Test rolling back to previous key"""
    # Create backup
    backup_path = await backup_service.backup_key('openai', 'sk-old-key', user_id)

    # Store new key
    await store_key('sk-new-key', 'openai', user_id)

    # Rollback
    await backup_service.rollback_key(backup_path, user_id)

    # Verify old key restored
    current = await get_current_key('openai', user_id)
    assert current.value == 'sk-old-key'
```

---

## Security Considerations

### Key Backup Encryption

```python
def _encrypt_key(self, key_value: str) -> bytes:
    """Encrypt key for backup using user's master key"""
    from cryptography.fernet import Fernet

    # Use user's master key (from keychain)
    master_key = self._get_user_master_key()
    cipher = Fernet(master_key)

    encrypted = cipher.encrypt(key_value.encode('utf-8'))
    return encrypted
```

**Key Points**:
- Backups encrypted with user's master key
- Master key stored in OS keychain
- Backup files useless without master key
- Automatic cleanup after 90 days

---

## Related Issues

- **#250: CORE-KEYS-ROTATION-REMINDERS** - Created rotation policy engine
- **#252: CORE-KEYS-STRENGTH-VALIDATION** - Key validation integration
- **#255: CORE-UX-STATUS-USER** - Status checker integration point

---

## Future Enhancements

### Phase 2
- Automated key rotation (with provider API support)
- Email/Slack notifications for rotation reminders
- Calendar reminders for upcoming rotations

### Phase 3 (MVP)
- Zero-downtime rotation (dual key support)
- Rotation verification tests
- Provider-specific rotation APIs (where available)
- Team coordination for shared keys

---

## Success Metrics

- % of users completing rotation within 7 days of reminder
- Time to complete rotation (target: <5 minutes)
- Rollback rate (<5% indicates good UX)
- User satisfaction with rotation process

---

**Sprint**: TBD
**Milestone**: TBD (A8 or MVP)
**Labels**: security, enhancement, automation, key-management
**Estimated Effort**: 30-45 minutes
