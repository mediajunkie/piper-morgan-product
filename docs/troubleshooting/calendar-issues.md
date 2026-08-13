# Calendar Integration Troubleshooting

## Common Issues

### Authentication Errors
**Symptom**: "Credentials not found" or "Permission denied"
**Solutions**:
- Verify GOOGLE_CALENDAR_CREDENTIALS_PATH is correct
- Check service account has Calendar API access
- Ensure credentials file is valid JSON

### Spatial Adapter Issues
**Symptom**: "Spatial context extraction failed"
**Solutions**:
- Verify the Model Context Protocol (MCP) service is running
- Check GoogleCalendarAdapter inheritance
- Validate BaseSpatialAdapter integration

### Configuration Validation Failures
**Symptom**: ConfigValidator reports Calendar as invalid
**Solutions**:
- Run detailed validation: `validator.validate_all()`
- Check environment variables are set
- Verify credentials file accessibility

## Diagnostic Commands

### Check Configuration
```bash
python -c "
from services.infrastructure.config.config_validator import ConfigValidator
validator = ConfigValidator()
validator.validate_all()
validator.print_summary()
"
```

### Test Calendar Access
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
router = CalendarIntegrationRouter()
# Test router functionality
```

## Contact
For additional support, refer to integration documentation or configuration guides.
