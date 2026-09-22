# Personality Enhancement Configuration

## Overview
The ResponsePersonalityEnhancer system allows customization of Piper's communication style while maintaining accuracy and professionalism. This document covers all configuration options and methods.

## Default Configuration
All personality settings have sensible defaults optimized for professional PM work:
- **Warmth**: 0.7 (warm but professional)
- **Confidence**: "contextual" (transparent but not distracting)
- **Actions**: "medium" (helpful without being pushy)
- **Depth**: "balanced" (appropriate for most users)

## Configuration Sources (Priority Order)
1. **Database** - PersonalityProfile table (persistent, user-specific)
2. **PIPER.user.md** - File-based overrides (development/testing)
3. **System Defaults** - Fallback values (built-in)

## Configuration Structure

### Complete Configuration Schema
```yaml
personality:
  profile:
    warmth_level: 0.7              # 0.0-1.0 (float)
    confidence_style: "contextual"  # enum: numeric|descriptive|contextual|hidden
    action_orientation: "medium"    # enum: high|medium|low
    technical_depth: "balanced"     # enum: detailed|balanced|simplified
  performance:
    max_response_time_ms: 100       # Enhancement timeout (integer)
    cache_ttl_seconds: 300          # Profile cache duration (integer)
    fallback_enabled: true          # Enable graceful degradation (boolean)
```

### Minimal Configuration (PIPER.user.md)
```yaml
personality:
  profile:
    warmth_level: 0.8
    confidence_style: "hidden"
```

## Configuration Options Details

### Warmth Level (0.0 - 1.0)
Controls the enthusiasm and friendliness of responses.

- **0.0 - 0.2**: Very professional, formal, direct
  - Example: "Task completed. 3 issues found."
- **0.3 - 0.5**: Professional with slight warmth
  - Example: "Task completed successfully. Found 3 issues for review."
- **0.6 - 0.8**: Warm and professional (recommended range)
  - Example: "Great! Task completed successfully. I found 3 issues that need attention."
- **0.9 - 1.0**: Very warm and encouraging
  - Example: "Excellent work! Task completed perfectly and I found 3 opportunities for improvement!"

### Confidence Display Style
Controls how uncertainty and confidence levels are communicated.

#### "numeric"
Shows specific percentages and numerical confidence indicators.
- Example: "Analysis complete (87% confident)"
- Example: "Found 5 issues (moderate confidence: 65%)"

#### "descriptive"
Uses descriptive words for confidence levels.
- Example: "Analysis complete (high confidence)"
- Example: "Found 5 issues (preliminary analysis)"

#### "contextual"
Provides context about the confidence assessment.
- Example: "Analysis complete (based on recent patterns)"
- Example: "Found 5 issues (with current information)"

#### "hidden"
No confidence indicators shown - clean, streamlined responses.
- Example: "Analysis complete"
- Example: "Found 5 issues"

### Action Orientation
Controls how much actionable guidance is provided.

#### "high"
Every response includes explicit next steps and recommendations.
- Example: "Task completed successfully—ready for the next step! Here's what I recommend: 1) Review the 3 issues found, 2) Prioritize by impact, 3) Schedule fixes for next sprint."

#### "medium"
Actionable guidance when relevant and helpful.
- Example: "Task completed successfully. Found 3 issues that need attention—shall I help prioritize them?"

#### "low"
Minimal action suggestions - focuses on information delivery.
- Example: "Task completed successfully. Found 3 issues."

### Technical Depth
Controls the level of technical detail in responses.

#### "detailed"
Full technical explanations with implementation specifics.
- Example: "Database query optimization complete. Reduced query execution time from 847ms to 23ms by adding composite index on (user_id, created_at) and implementing connection pooling with 10-connection limit."

#### "balanced"
Right level of detail for most users - technical but accessible.
- Example: "Database optimization complete. Query performance improved by 97% through indexing and connection pooling."

#### "simplified"
High-level summaries focused on outcomes and business impact.
- Example: "Database performance significantly improved. Page load times now under 1 second."

## Environment Variables

### Production Configuration
```bash
# Personality system settings
PERSONALITY_CACHE_TTL=300                    # Profile cache duration (seconds)
PERSONALITY_MAX_LATENCY_MS=100               # Enhancement timeout (milliseconds)
PERSONALITY_FALLBACK_ENABLED=true           # Enable graceful degradation
PERSONALITY_DEFAULT_WARMTH=0.7               # Default warmth level
PERSONALITY_DEFAULT_CONFIDENCE=contextual    # Default confidence style

# Database settings (if using database profiles)
PERSONALITY_DB_CONNECTION_TIMEOUT=5000       # Database timeout (milliseconds)
PERSONALITY_DB_RETRY_ATTEMPTS=3              # Connection retry attempts
```

### Development/Testing Configuration
```bash
# Development overrides
PERSONALITY_CACHE_TTL=10                     # Short cache for testing
PERSONALITY_MAX_LATENCY_MS=200               # Relaxed timeout for debugging
PERSONALITY_FALLBACK_ENABLED=true           # Always enable fallback
PERSONALITY_DEBUG_LOGGING=true               # Enable detailed logging
```

## Configuration Methods

### Method 1: Web Interface (Recommended)
**URL**: http://localhost:8081/personality-preferences

1. Navigate to personality preferences page
2. Adjust sliders and dropdowns for desired settings
3. Click "Save Configuration"
4. Changes take effect immediately

**Advantages**:
- User-friendly interface
- Real-time preview (if available)
- Input validation
- Persistent storage in database

### Method 2: File Configuration (Advanced)
**File**: `../config/PIPER.user.md`

1. Edit the personality section in PIPER.user.md
2. Save the file
3. Restart Piper if needed (depending on configuration)
4. Changes override database settings

**Advantages**:
- Version controllable
- Batch configuration changes
- Development/testing friendly
- Easy backup and restore

### Method 3: API Configuration (Programmatic)
**Endpoint**: `http://localhost:8001/api/v1/personality/profile`

All personality endpoints require authentication (the profile is resolved from the
authenticated session, so there is no user-id path segment). Authenticate once,
then reuse the session cookie:

```bash
# Authenticate first (form-encoded, not JSON)
curl -s -c /tmp/piper-cookies.txt -X POST http://localhost:8001/api/v1/auth/login \
  -d "username=YOUR_USERNAME&password=YOUR_PASSWORD"

# Get current configuration
curl -b /tmp/piper-cookies.txt -X GET "http://localhost:8001/api/v1/personality/profile"

# Update configuration (admin-only — non-admin users get 403)
curl -b /tmp/piper-cookies.txt -X PUT "http://localhost:8001/api/v1/personality/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "warmth_level": 0.8,
    "confidence_style": "contextual",
    "action_orientation": "high",
    "technical_depth": "balanced"
  }'
```

## Configuration Validation

### Valid Value Ranges
- **warmth_level**: 0.0 to 1.0 (inclusive)
- **confidence_style**: "numeric", "descriptive", "contextual", "hidden"
- **action_orientation**: "high", "medium", "low"
- **technical_depth**: "detailed", "balanced", "simplified"

### Invalid Configuration Handling
The system handles invalid configurations gracefully:

1. **Out of range values**: Clamped to valid range
   - warmth_level: 2.0 → 1.0
   - warmth_level: -0.5 → 0.0

2. **Invalid enum values**: Fall back to defaults
   - confidence_style: "invalid" → "contextual"
   - action_orientation: "extreme" → "medium"

3. **Missing configuration**: Use system defaults
4. **Malformed YAML**: Log error and use defaults
5. **Database connection issues**: Fall back to file configuration

## Performance Considerations

### Response Time Impact
- **Target**: <70ms additional latency
- **Actual**: <1ms average enhancement time
- **Timeout**: 100ms maximum (configurable)
- **Fallback**: Original response if timeout exceeded

### Caching Strategy
- **Profile Cache**: 300 seconds TTL (configurable)
- **Enhancement Cache**: In-memory for repeated patterns
- **Database Connections**: Pooled and reused
- **File Watching**: Configuration changes detected automatically

### Resource Usage
- **Memory**: <10MB additional for personality system
- **CPU**: <5% additional load during enhancement
- **Network**: No additional external calls
- **Storage**: Minimal database storage for profiles

## Testing Configuration

### Configuration Testing Checklist
- [ ] Default configuration loads correctly
- [ ] Web interface saves and loads settings
- [ ] File configuration overrides work
- [ ] Invalid values handled gracefully
- [ ] Performance within acceptable limits
- [ ] Fallback behavior works when needed

### Test Configuration Examples

#### High Performance Test
```yaml
personality:
  profile:
    warmth_level: 0.0          # Minimal processing
    confidence_style: "hidden" # No confidence processing
    action_orientation: "low"   # Minimal action processing
  performance:
    max_response_time_ms: 50   # Aggressive timeout
    cache_ttl_seconds: 600     # Long cache
```

#### High Engagement Test
```yaml
personality:
  profile:
    warmth_level: 1.0           # Maximum warmth
    confidence_style: "contextual" # Rich confidence display
    action_orientation: "high"   # Maximum actionability
    technical_depth: "detailed" # Full technical depth
```

## Troubleshooting

### Common Configuration Issues

#### 1. Configuration Not Taking Effect
**Symptoms**: Changes made but responses unchanged
**Causes**:
- Cache not cleared
- Configuration syntax error
- Database connection issues
**Solutions**:
- Restart system to clear caches
- Validate YAML syntax
- Check database connectivity

#### 2. Performance Degradation
**Symptoms**: Slow response times after enabling personality
**Causes**:
- Timeout set too high
- Database connection issues
- Cache not working
**Solutions**:
- Reduce max_response_time_ms
- Check database performance
- Verify cache TTL settings

#### 3. Inconsistent Personality
**Symptoms**: Personality varies between interfaces
**Causes**:
- Different configuration sources
- Cache inconsistency
- Interface-specific overrides
**Solutions**:
- Check configuration priority order
- Clear all caches
- Verify consistent configuration across interfaces

### Debugging Configuration

#### Enable Debug Logging
```bash
export PERSONALITY_DEBUG_LOGGING=true
```

#### Check Configuration Loading
```bash
# View current effective configuration (requires auth — see Method 3 above)
curl -b /tmp/piper-cookies.txt "http://localhost:8001/api/v1/personality/profile" | jq '.'

# Check configuration file syntax
python -c "import yaml; print(yaml.safe_load(open('../config/PIPER.user.md')))"
```

#### Monitor Performance
```bash
# Check response times with personality enabled/disabled
time curl "http://localhost:8001/api/standup?personality=true"
time curl "http://localhost:8001/api/standup?personality=false"
```

---

**Configuration Guide Version**: 1.0
**Last Updated**: September 11, 2025
**Status**: Production Ready
**Next Review**: Post-MVP feedback integration
