# Calendar Configuration Guide

## Prerequisites
- Google Cloud Platform account
- Google Calendar API enabled
- Service account credentials

## Setup Steps

### 1. Google Cloud Configuration
1. Create new Google Cloud Project
2. Enable Google Calendar API
3. Create service account
4. Download credentials JSON file

### 2. Environment Configuration
```bash
export GOOGLE_CALENDAR_CREDENTIALS_PATH="/path/to/credentials.json"
export GOOGLE_CALENDAR_IDS='["primary"]'
```

### 3. Verification
```bash
python -c "
from services.infrastructure.config.config_validator import ConfigValidator
validator = ConfigValidator()
validator.validate_all()
print('Calendar status:', 'Valid' if validator.is_all_valid() else 'Invalid')
"
```

## Security Notes
- Store credentials securely
- Use service account with minimal permissions
- Regularly rotate credentials
- Monitor API usage

## Related Documentation
- [Calendar Integration Guide](../integrations/calendar-integration-guide.md)
- Configuration Validation *(proposed; doc TBD)*
