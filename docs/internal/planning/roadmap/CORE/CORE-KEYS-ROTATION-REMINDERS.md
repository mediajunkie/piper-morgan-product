# CORE-KEYS-ROTATION-REMINDERS: Automated Key Rotation Reminders

## Context

Users should be proactively reminded to rotate API keys based on age, security best practices, and provider recommendations. Currently, key rotation is manual and users may forget, increasing security risk.

**Parent Issue**: #228 (API Key Management)

---

## Problem Statement

**Current State**:
- Users can rotate keys manually via API or CLI
- No proactive reminders or notifications
- Users must track key age themselves
- Security best practices (90-day rotation) not enforced

**Risk**:
- Stale keys increase security vulnerability
- Compliance requirements may mandate regular rotation
- Users may not know when to rotate
- No visibility into key age

---

## Proposed Solution

### 1. Key Age Tracking
```python
# Already exists in UserAPIKey model!
class UserAPIKey:
    created_at: DateTime
    rotated_at: DateTime  # Last rotation

    def age_days(self) -> int:
        """Days since last rotation or creation"""
        last_update = self.rotated_at or self.created_at
        return (datetime.utcnow() - last_update).days
```

### 2. Rotation Policy Configuration
```yaml
# config/rotation_policy.yaml
rotation_policies:
  default:
    max_age_days: 90
    warning_days: [60, 75, 85]
    critical_days: 88

  provider_overrides:
    openai:
      max_age_days: 60  # More frequent for high-value keys
    github:
      max_age_days: 180  # Less frequent for personal tokens
```

### 3. Reminder System
```python
class KeyRotationReminder:
    async def check_key_ages(self, user_id: str) -> List[RotationReminder]:
        """Check all user keys and generate reminders"""
        keys = await user_api_key_service.list_user_keys(user_id)
        reminders = []

        for key in keys:
            age = key.age_days()
            policy = get_policy(key.provider)

            if age >= policy.critical_days:
                reminders.append(RotationReminder(
                    key=key,
                    severity="critical",
                    message=f"Your {key.provider} key is {age} days old. Rotate immediately!"
                ))
            elif age in policy.warning_days:
                reminders.append(RotationReminder(
                    key=key,
                    severity="warning",
                    message=f"Your {key.provider} key is {age} days old. Consider rotating soon."
                ))

        return reminders
```

### 4. Notification Channels
- **In-app**: Banner/modal on login
- **CLI**: Show in `piper status` output
- **Email**: Optional email notifications (if configured)
- **Slack**: Optional Slack DM (if integrated)

---

## Implementation Phases

### Phase 1: Status Integration (2 hours)
- Add key age to `piper status` output
- Show warning indicators for old keys
- Link to rotation documentation

```bash
piper status

API Keys:
  ✓ OpenAI (45 days old)
  ⚠ Anthropic (78 days old) ← Warning: Consider rotating
  ✗ GitHub (95 days old) ← Critical: Rotate immediately!
```

### Phase 2: Policy Engine (3 hours)
- Create rotation policy configuration
- Implement policy evaluation logic
- Support provider-specific overrides
- Add user preference overrides

### Phase 3: Notification System (3 hours)
- In-app notifications (banner/modal)
- CLI warnings on startup
- Email notifications (optional)
- Slack integration (optional)

### Phase 4: Guided Rotation (2 hours)
- One-click rotation from reminder
- Validation before rotation
- Rollback support
- Success confirmation

---

## Acceptance Criteria

### Core Functionality
- [ ] Track key age (days since creation or last rotation)
- [ ] Evaluate keys against rotation policies
- [ ] Generate reminders at warning thresholds
- [ ] Show reminders in `piper status`
- [ ] Link to rotation documentation

### User Experience
- [ ] Non-intrusive warnings (not blocking)
- [ ] Clear severity levels (info, warning, critical)
- [ ] Actionable messages ("Rotate now" button)
- [ ] Easy to dismiss/snooze
- [ ] Respects user preferences (can disable)

### Configuration
- [ ] Default 90-day rotation policy
- [ ] Provider-specific overrides
- [ ] User preference overrides
- [ ] Warning threshold configuration
- [ ] Notification channel preferences

### Quality Gates
- [ ] Unit tests for policy evaluation
- [ ] Integration tests with UserAPIKeyService
- [ ] Performance: <10ms to check all keys
- [ ] Documentation for policy configuration

---

## Technical Design

### Database Schema (Already Exists!)
```sql
-- UserAPIKey already has these fields:
CREATE TABLE user_api_keys (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    provider VARCHAR(50),
    created_at TIMESTAMP NOT NULL,
    rotated_at TIMESTAMP,  -- Last rotation timestamp
    -- ... other fields
);
```

**No schema changes needed!** ✅

### New Components
```
services/security/
  key_rotation_reminder.py     # NEW - Reminder logic
  rotation_policy.py            # NEW - Policy engine

config/
  rotation_policy.yaml          # NEW - Policy configuration

web/api/
  key_reminders.py             # NEW - API endpoints
```

### API Endpoints
```python
GET /api/v1/keys/reminders
# Returns: List of rotation reminders for current user

POST /api/v1/keys/{provider}/rotate-guided
# One-click rotation from reminder
```

---

## Example User Flows

### Flow 1: Status Check with Warning
```bash
$ piper status

API Keys:
  ✓ OpenAI (45 days old)
  ⚠ Anthropic (78 days old)
     Recommendation: Rotate within 12 days (best practice: every 90 days)
     Command: piper keys rotate anthropic

Recommendations:
  → Consider rotating your Anthropic key soon
```

### Flow 2: Critical Reminder on Login
```
╔══════════════════════════════════════════════════════════╗
║  ⚠️  KEY ROTATION REQUIRED                               ║
║                                                          ║
║  Your GitHub key is 95 days old and should be rotated.  ║
║                                                          ║
║  Best practice: Rotate keys every 90 days               ║
║                                                          ║
║  [Rotate Now]  [Remind Me Tomorrow]  [Learn More]       ║
╚══════════════════════════════════════════════════════════╝
```

### Flow 3: One-Click Rotation
```bash
$ piper keys rotate anthropic --guided

Rotating Anthropic API key...
1. Enter new API key: [________]
2. Validating new key... ✓ Valid (claude-3-opus access confirmed)
3. Storing old key reference... ✓
4. Updating to new key... ✓
5. Testing connection... ✓

Success! Your Anthropic key has been rotated.
- Old key saved as backup (auto-expires in 7 days)
- New key active immediately
- No service interruption

Next rotation recommended: January 21, 2026
```

---

## Success Metrics

### Security
- **Target**: 95% of keys rotated within policy window
- **Measure**: Key age at rotation time
- **Success**: <5% of keys exceed max_age_days

### User Adoption
- **Target**: 80% of users rotate keys when reminded
- **Measure**: Rotation rate after reminder shown
- **Success**: >80% compliance

### User Experience
- **Target**: Low reminder fatigue (users don't disable)
- **Measure**: Reminder dismissal/disable rate
- **Success**: <10% permanently disable reminders

### Performance
- **Target**: No impact on system performance
- **Measure**: Time to check all keys
- **Success**: <10ms per user

---

## Dependencies

**Required** (Already Complete!):
- ✅ #228: API Key Management (provides infrastructure)
- ✅ User model with key relationships
- ✅ Key age tracking (created_at, rotated_at fields)

**Optional** (Future):
- Email service (for email notifications)
- Slack integration (for Slack notifications)
- #249: Audit logging (for rotation tracking)

---

## Time Estimate

**Total**: 10 hours

**Breakdown**:
- Status integration: 2 hours
- Policy engine: 3 hours
- Notification system: 3 hours
- Guided rotation: 2 hours

---

## Priority

**Priority**: Medium (security best practice, not critical)
**Milestone**: Beta (post-Alpha)
**Sprint**: A8 or later

**Rationale**: Important for security, but Alpha users can rotate manually. Add after core onboarding (#218) is complete.

---

## Related Issues

- #228: API Key Management (parent - provides infrastructure)
- #249: Audit Logging (rotation events should be logged)
- #218: Alpha Onboarding (rotation reminders part of health checks)

**Epic**: CORE-USERS (Multi-user & Security)
**Labels**: enhancement, security, component: security, priority: medium
