# CORE-KEYS-OAUTH-PROVIDERS: OAuth & Integration Key Support

**Sprint**: TBD (A8 or later)
**Priority**: Medium
**Effort**: 45-60 minutes
**Impact**: Medium (completeness)

---

## Problem

Issue #252 (CORE-KEYS-STRENGTH-VALIDATION) implemented key validation for **direct API key providers**:
- OpenAI (sk-...)
- Anthropic (sk-ant-...)
- GitHub (ghp_..., github_pat_...)
- Perplexity (pplx-...)
- Gemini (AIza...)

However, Piper Morgan also uses **OAuth-based integrations** and **other authentication patterns** that are not currently covered:
- **Slack** - OAuth 2.0 with bot tokens (xoxb-...)
- **Notion** - Internal integration tokens (secret_...)
- **Google Calendar** - OAuth 2.0 with refresh tokens

These credentials have different:
- Format patterns
- Security requirements
- Rotation policies
- Validation needs

---

## Current State

### What's Missing

**Slack Integration**:
- Bot tokens: `xoxb-...`
- User tokens: `xoxp-...`
- App-level tokens: `xapp-...`
- No validation in current system

**Notion Integration**:
- Internal integration tokens: `secret_...`
- Database IDs and page IDs
- No validation in current system

**Google Calendar**:
- OAuth 2.0 refresh tokens
- Access tokens (short-lived)
- Client credentials
- Complex refresh flow

---

## Proposed Solution

Extend the key validation system to support OAuth-based providers and integration tokens with appropriate validation patterns for each authentication type.

### Key Differences from API Keys

| Aspect | Direct API Keys | OAuth/Integration Keys |
|--------|----------------|----------------------|
| **Format** | Fixed prefix pattern | Variable patterns |
| **Lifetime** | Long-lived (months/years) | Refresh tokens: long, Access tokens: short (hours) |
| **Rotation** | Manual replacement | Automatic refresh (OAuth) |
| **Validation** | Format + strength + leak | Format + expiry + refresh capability |
| **Storage** | Keychain/env | Token database + refresh logic |

---

## Implementation

### 1. Slack Provider Support

```python
class SlackKeyValidator:
    """Validator for Slack OAuth tokens"""

    VALID_PATTERNS = {
        'bot_token': r'^xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+$',
        'user_token': r'^xoxp-[0-9]+-[0-9]+-[0-9]+-[a-f0-9]+$',
        'app_token': r'^xapp-[0-9]+-[A-Z0-9]+-[0-9]+-[a-f0-9]+$'
    }

    async def validate(self, token: str) -> ValidationReport:
        """Validate Slack token"""

        # 1. Format check
        token_type = self._identify_token_type(token)
        if not token_type:
            return ValidationReport(
                valid=False,
                issues=["Invalid Slack token format"]
            )

        # 2. Live validation (optional - tests with Slack API)
        if await self._should_test_token():
            is_valid = await self._test_slack_token(token)
            if not is_valid:
                return ValidationReport(
                    valid=False,
                    issues=["Token rejected by Slack API"]
                )

        # 3. Expiry check (Slack tokens don't expire but can be revoked)
        # Check last successful use timestamp

        return ValidationReport(
            valid=True,
            token_type=token_type,
            recommendations=self._get_recommendations(token_type)
        )

    async def _test_slack_token(self, token: str) -> bool:
        """Test token with Slack API (auth.test endpoint)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://slack.com/api/auth.test',
                    headers={'Authorization': f'Bearer {token}'},
                    timeout=5
                ) as response:
                    data = await response.json()
                    return data.get('ok', False)
        except Exception as e:
            logger.warning(f"Slack token test failed: {e}")
            return False  # Assume invalid if test fails
```

**Key Features**:
- Format validation for 3 token types
- Optional live API validation
- Revocation detection
- Usage tracking

---

### 2. Notion Provider Support

```python
class NotionKeyValidator:
    """Validator for Notion integration tokens"""

    VALID_PATTERN = r'^secret_[a-zA-Z0-9]{43}$'

    async def validate(self, token: str) -> ValidationReport:
        """Validate Notion integration token"""

        # 1. Format check
        if not re.match(self.VALID_PATTERN, token):
            return ValidationReport(
                valid=False,
                issues=["Invalid Notion token format (should be secret_...)"]
            )

        # 2. Length check (Notion tokens are exactly 50 chars)
        if len(token) != 50:
            return ValidationReport(
                valid=False,
                issues=[f"Invalid token length: {len(token)} (expected 50)"]
            )

        # 3. Live validation (optional - tests with Notion API)
        if await self._should_test_token():
            is_valid = await self._test_notion_token(token)
            if not is_valid:
                return ValidationReport(
                    valid=False,
                    issues=["Token rejected by Notion API"]
                )

        return ValidationReport(
            valid=True,
            recommendations=[
                "Notion tokens don't expire but can be regenerated",
                "Monitor integration usage in Notion workspace settings"
            ]
        )

    async def _test_notion_token(self, token: str) -> bool:
        """Test token with Notion API (list users endpoint)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.notion.com/v1/users',
                    headers={
                        'Authorization': f'Bearer {token}',
                        'Notion-Version': '2022-06-28'
                    },
                    timeout=5
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.warning(f"Notion token test failed: {e}")
            return False
```

**Key Features**:
- Fixed format validation
- Exact length requirement (50 chars)
- Optional live API test
- Workspace integration awareness

---

### 3. Google Calendar OAuth Support

```python
class GoogleOAuthValidator:
    """Validator for Google OAuth credentials"""

    async def validate(self, credentials: dict) -> ValidationReport:
        """
        Validate Google OAuth credentials

        credentials = {
            'refresh_token': '...',
            'access_token': '...',
            'token_expiry': '...',
            'client_id': '...',
            'client_secret': '...'
        }
        """
        issues = []

        # 1. Check required fields
        required = ['refresh_token', 'client_id', 'client_secret']
        missing = [f for f in required if f not in credentials]
        if missing:
            return ValidationReport(
                valid=False,
                issues=[f"Missing required fields: {', '.join(missing)}"]
            )

        # 2. Check access token expiry
        if 'token_expiry' in credentials:
            expiry = datetime.fromisoformat(credentials['token_expiry'])
            if expiry < datetime.utcnow():
                issues.append("Access token expired (will auto-refresh)")

        # 3. Validate refresh token works
        if await self._should_test_token():
            can_refresh = await self._test_refresh_token(
                credentials['refresh_token'],
                credentials['client_id'],
                credentials['client_secret']
            )
            if not can_refresh:
                return ValidationReport(
                    valid=False,
                    issues=["Refresh token is invalid or revoked"]
                )

        return ValidationReport(
            valid=True,
            issues=issues,
            recommendations=[
                "OAuth tokens refresh automatically",
                "Monitor refresh failures in logs",
                "Re-authenticate if refresh token revoked"
            ]
        )

    async def _test_refresh_token(
        self,
        refresh_token: str,
        client_id: str,
        client_secret: str
    ) -> bool:
        """Test if refresh token can obtain new access token"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://oauth2.googleapis.com/token',
                    data={
                        'refresh_token': refresh_token,
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'grant_type': 'refresh_token'
                    },
                    timeout=5
                ) as response:
                    data = await response.json()
                    return 'access_token' in data
        except Exception as e:
            logger.warning(f"Google refresh token test failed: {e}")
            return False
```

**Key Features**:
- Multi-field credential validation
- Access token expiry detection
- Refresh token testing
- Auto-refresh awareness

---

## Enhanced KeyValidator Integration

```python
class KeyValidator:
    """Enhanced validator supporting all provider types"""

    def __init__(self):
        # Existing validators
        self.format_checker = FormatChecker()
        self.strength_checker = StrengthChecker()
        self.leak_detector = KeyLeakDetector()

        # New OAuth/integration validators
        self.slack_validator = SlackKeyValidator()
        self.notion_validator = NotionKeyValidator()
        self.google_oauth_validator = GoogleOAuthValidator()

    async def validate_key(
        self,
        key: str | dict,
        provider: str
    ) -> ValidationReport:
        """Validate any key type (API key or OAuth)"""

        # Route to appropriate validator
        if provider == "slack":
            return await self.slack_validator.validate(key)

        elif provider == "notion":
            return await self.notion_validator.validate(key)

        elif provider == "google_calendar":
            # Expect dict with OAuth credentials
            if not isinstance(key, dict):
                return ValidationReport(
                    valid=False,
                    issues=["Google Calendar requires OAuth credentials dict"]
                )
            return await self.google_oauth_validator.validate(key)

        else:
            # Existing API key validation
            return await self._validate_api_key(key, provider)
```

---

## Rotation Policy Differences

### API Keys (Existing)
```python
# From #250: CORE-KEYS-ROTATION-REMINDERS
DEFAULT_ROTATION_DAYS = 90
PROVIDER_OVERRIDES = {
    'openai': 60,    # Rotate every 60 days
    'github': 180    # Rotate every 180 days
}
```

### OAuth/Integration Keys (New)
```python
OAUTH_ROTATION_POLICIES = {
    'slack': {
        'rotation_days': None,  # No expiry, but monitor revocation
        'check_validity': 'daily',  # Test token daily
        'revocation_action': 'alert_user'
    },
    'notion': {
        'rotation_days': 365,  # Rotate yearly as best practice
        'check_validity': 'weekly',
        'revocation_action': 'alert_user'
    },
    'google_calendar': {
        'rotation_days': None,  # Refresh tokens don't expire
        'check_validity': 'on_use',  # Validate on each use
        'revocation_action': 'trigger_reauth'
    }
}
```

---

## Status Checker Integration

```python
# Enhanced status output (from #255)

async def show_api_keys_status():
    """Show status of all keys including OAuth"""

    print("\n=== API Keys ===")
    for provider in ['openai', 'anthropic', 'github']:
        key = get_api_key(provider)
        if key:
            report = await validator.validate_key(key, provider)
            print(f"{provider}: {format_key_status(report)}")

    print("\n=== OAuth Integrations ===")

    # Slack
    slack_token = get_slack_token()
    if slack_token:
        report = await validator.validate_key(slack_token, 'slack')
        print(f"Slack: {format_oauth_status(report)}")

    # Notion
    notion_token = get_notion_token()
    if notion_token:
        report = await validator.validate_key(notion_token, 'notion')
        print(f"Notion: {format_oauth_status(report)}")

    # Google Calendar
    google_creds = get_google_credentials()
    if google_creds:
        report = await validator.validate_key(google_creds, 'google_calendar')
        print(f"Google Calendar: {format_oauth_status(report)}")

def format_oauth_status(report: ValidationReport) -> str:
    """Format OAuth token status"""
    if not report.valid:
        return f"❌ Invalid - {', '.join(report.issues)}"

    status_parts = ["✅ Valid"]

    if report.issues:  # Non-fatal issues (e.g., expired access token)
        status_parts.append(f"⚠️  {', '.join(report.issues)}")

    return ' '.join(status_parts)
```

---

## Testing Strategy

### Unit Tests

```python
async def test_slack_token_format_validation():
    """Test Slack token format patterns"""
    validator = SlackKeyValidator()

    # Valid bot token
    assert await validator.validate('xoxb-123-456-abc123') is valid

    # Invalid format
    assert not await validator.validate('invalid-token') is valid

async def test_notion_token_validation():
    """Test Notion token format and length"""
    validator = NotionKeyValidator()

    # Valid Notion token (50 chars)
    token = 'secret_' + 'a' * 43
    assert await validator.validate(token) is valid

    # Invalid length
    short_token = 'secret_abc'
    assert not await validator.validate(short_token) is valid

async def test_google_oauth_expiry_detection():
    """Test Google OAuth token expiry detection"""
    validator = GoogleOAuthValidator()

    # Expired access token
    creds = {
        'refresh_token': 'refresh_xyz',
        'access_token': 'access_abc',
        'token_expiry': '2024-01-01T00:00:00Z',  # Past
        'client_id': 'client_123',
        'client_secret': 'secret_456'
    }

    report = await validator.validate(creds)
    assert 'expired' in report.issues[0].lower()
```

### Integration Tests

```python
async def test_slack_live_validation():
    """Test Slack token with actual API call"""
    # Requires real Slack test token
    validator = SlackKeyValidator()
    token = os.getenv('SLACK_TEST_TOKEN')

    if token:
        report = await validator.validate(token)
        assert report.valid is True

async def test_google_refresh_flow():
    """Test Google OAuth refresh token works"""
    # Requires real Google test credentials
    validator = GoogleOAuthValidator()
    creds = load_google_test_credentials()

    if creds:
        report = await validator.validate(creds)
        assert report.valid is True
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] Slack token validation (3 token types)
- [ ] Notion token validation (format + length)
- [ ] Google OAuth credential validation
- [ ] Live API testing (optional, configurable)
- [ ] Integration with existing KeyValidator
- [ ] Status checker shows OAuth integrations

### Validation Features
- [ ] Format validation for each provider
- [ ] Expiry detection (where applicable)
- [ ] Revocation detection (where possible)
- [ ] Usage tracking
- [ ] Recommendations specific to auth type

### Testing Requirements
- [ ] Unit tests for all validators
- [ ] Mock tests for API calls
- [ ] Integration tests with real credentials (optional)
- [ ] Edge case handling

---

## Configuration

```yaml
# config/security.yaml

oauth_providers:
  slack:
    enabled: true
    test_on_validation: false  # Live API test
    check_frequency: 'daily'

  notion:
    enabled: true
    test_on_validation: false
    check_frequency: 'weekly'
    rotation_reminder_days: 365

  google_calendar:
    enabled: true
    test_on_validation: true  # Test refresh capability
    check_frequency: 'on_use'
```

---

## Security Considerations

### OAuth Token Storage

**Different from API keys**:
- API keys: macOS Keychain
- OAuth tokens: Database (need refresh capability)
- Client secrets: Environment variables

**Why database for OAuth**:
- Need to store refresh tokens
- Need to track token expiry
- Need to implement refresh flow
- Multiple tokens per integration (access + refresh)

### Validation Frequency

**API Keys**: Validate on change/addition
**OAuth Tokens**:
- Slack: Daily validation (check if revoked)
- Notion: Weekly validation (check if revoked)
- Google: On-use validation (check if refresh works)

---

## Related Issues

- **#252: CORE-KEYS-STRENGTH-VALIDATION** - Base validation system
- **#250: CORE-KEYS-ROTATION-REMINDERS** - Rotation policy framework
- **#255: CORE-UX-STATUS-USER** - Status checker integration point

---

## Future Enhancements

### Phase 2
- Automatic token refresh for Google OAuth
- Slack workspace change detection
- Notion workspace permissions validation

### Phase 3 (MVP)
- Multi-workspace Slack support
- Notion database-level permissions
- Google OAuth scope validation
- Token revocation webhooks

---

## Documentation Requirements

### User Documentation
- How OAuth differs from API keys
- Why some tokens don't need rotation
- What to do if token revoked
- Re-authentication process

### Developer Documentation
- OAuth token storage strategy
- Refresh token implementation
- Live validation patterns
- Provider-specific quirks

---

## Success Metrics

- All OAuth providers validated correctly
- Zero false positives on revocation
- Clear user guidance on token issues
- Smooth re-authentication flow

---

**Sprint**: TBD
**Milestone**: TBD (A8 or later)
**Labels**: enhancement, oauth, security, integrations
**Estimated Effort**: 45-60 minutes
