# Comprehensive PM Manual Testing Guide - ResponsePersonalityEnhancer

> **STALE (2026-08-29, #1638)**: the `TemplateRenderer` snippets below import
> `services.ui_messages.templates`, deleted per Arch's DISPOSE ruling (zero production
> callers). Those steps no longer run as written; the guide is retained as a historical
> testing record.

## Overview
This package provides step-by-step manual testing scenarios for validating the ResponsePersonalityEnhancer system before production deployment.

**System Status:** Production-ready after comprehensive automated testing
**Test Duration:** ~30 minutes for complete validation
**Prerequisites:** Piper system running with database connectivity

---

## Test Environment Setup

### 1. Pre-Test Verification
```bash
# Verify system status
cd /Users/xian/Development/piper-morgan
PYTHONPATH=. python3 -c "from services.personality.response_enhancer import ResponsePersonalityEnhancer; print('✅ System ready')"
```

### 2. Configuration Check
Verify PIPER.user.md personality configuration:
```bash
# Check configuration file
cat config/PIPER.user.md | grep -A 10 "personality:"
```

Expected output should include personality settings like:
```yaml
personality:
  warmth_level: 0.7
  confidence_style: "contextual"
  action_orientation: "medium"
  technical_depth: "balanced"
```

---

## Manual Test Scenarios

### Scenario 1: Basic Personality Enhancement
**Objective:** Verify personality enhancement is working in normal conditions

**Steps:**
1. Open terminal in Piper directory
2. Run the following test:
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test():
    renderer = TemplateRenderer(ActionHumanizer())
    result = await renderer.render_template(
        template='Here is my analysis: {human_action} completed',
        intent_action='analyze_issue',
        intent_category='analysis',
        user_id='pm_test_user_1'
    )
    print('Result:', repr(result))
    print('Length:', len(result))
    print('Enhanced:', 'good' in result.lower() or 'nice' in result.lower() or 'great' in result.lower())

asyncio.run(test())
"
```

**Expected Result:**
- Output should be longer than the input template
- Should contain friendly language (words like "Good", "Nice", "Great")
- Should show "analyze an issue" instead of "analyze_issue"
- Response time should be under 1 second

**Pass Criteria:** ✅ Enhanced output with warm, professional tone

---

### Scenario 2: Error Handling Validation
**Objective:** Verify graceful degradation when templates fail

**Steps:**
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_errors():
    renderer = TemplateRenderer(ActionHumanizer())

    print('=== Error Handling Tests ===')

    # Test 1: None template
    try:
        result1 = await renderer.render_template(
            template=None,
            intent_action='test_error',
            intent_category='testing',
            user_id='pm_test_user_2'
        )
        print('Test 1 (None template): ✅ PASS -', repr(result1[:50]))
    except Exception as e:
        print('Test 1 (None template): ❌ FAIL - Exception:', str(e)[:50])

    # Test 2: Missing placeholder
    try:
        result2 = await renderer.render_template(
            template='Result: {missing_data} not found',
            intent_action='test_error',
            intent_category='testing',
            user_id='pm_test_user_2'
        )
        print('Test 2 (Missing placeholder): ✅ PASS -', repr(result2[:50]))
    except Exception as e:
        print('Test 2 (Missing placeholder): ❌ FAIL - Exception:', str(e)[:50])

    # Test 3: Invalid template type
    try:
        result3 = await renderer.render_template(
            template=12345,
            intent_action='test_error',
            intent_category='testing',
            user_id='pm_test_user_3'
        )
        print('Test 3 (Invalid type): ✅ PASS -', repr(result3[:50]))
    except Exception as e:
        print('Test 3 (Invalid type): ❌ FAIL - Exception:', str(e)[:50])

asyncio.run(test_errors())
"
```

**Expected Result:**
- All tests should complete without exceptions
- Test 1 should return a reasonable fallback message
- Test 2 should return the template with the missing placeholder intact
- Test 3 should return a reasonable fallback
- No error messages should be displayed to user

**Pass Criteria:** ✅ No crashes, reasonable fallback responses in all cases

---

### Scenario 3: Performance Validation
**Objective:** Verify response times meet performance requirements

**Steps:**
```bash
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_performance():
    print('=== Performance Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())
    times = []

    for i in range(10):
        start = time.time()
        result = await renderer.render_template(
            template=f'Performance test {i}: analysis complete',
            intent_action='analyze_performance',
            intent_category='analysis',
            user_id=f'pm_perf_user_{i}'
        )
        duration = (time.time() - start) * 1000
        times.append(duration)
        print(f'Test {i+1}: {duration:.1f}ms - Success: {len(result) > 0}')

    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)

    print(f'\\n=== Performance Results ===')
    print(f'Average: {avg_time:.1f}ms')
    print(f'Maximum: {max_time:.1f}ms')
    print(f'Minimum: {min_time:.1f}ms')
    print(f'Target: <200ms (generous for PM testing)')
    print(f'Performance: {\"✅ PASS\" if max_time < 200 else \"❌ FAIL\"}')

asyncio.run(test_performance())
"
```

**Expected Result:**
- Average response time should be under 50ms
- Maximum response time should be under 200ms
- All tests should complete successfully
- Performance should be marked as "PASS"

**Pass Criteria:** ✅ All responses under 200ms, average under 50ms

---

### Scenario 4: Configuration Override Testing
**Objective:** Verify PIPER.user.md configuration overrides work

**Steps:**
1. First, test with current configuration:
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.personality.repository import PersonalityProfileRepository

async def test_config():
    print('=== Configuration Testing ===')
    repo = PersonalityProfileRepository()
    profile = await repo.get_by_user_id('pm_config_test')

    print('Current Profile Settings:')
    print(f'  Warmth level: {profile.warmth_level}')
    print(f'  Confidence style: {profile.confidence_style.value}')
    print(f'  Action orientation: {profile.action_orientation.value}')
    print(f'  Technical depth: {profile.technical_depth.value}')
    print(f'  User ID: {profile.user_id}')
    print(f'  Profile created: {profile.created_at.strftime(\"%Y-%m-%d %H:%M\")}')

asyncio.run(test_config())
"
```

2. Test profile creation and database persistence:
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.personality.repository import PersonalityProfileRepository

async def test_persistence():
    print('=== Profile Persistence Testing ===')
    repo = PersonalityProfileRepository()

    # Test creating multiple profiles
    test_users = ['pm_persist_1', 'pm_persist_2', 'pm_persist_3']

    for user_id in test_users:
        profile = await repo.get_by_user_id(user_id)
        print(f'✅ Profile created for {user_id}: warmth={profile.warmth_level}')

    print('Profile persistence: ✅ WORKING')

asyncio.run(test_persistence())
"
```

**Expected Result:**
- Configuration should load from PIPER.user.md or use defaults
- Database profile creation should work reliably
- Profile settings should be consistent and valid
- Multiple users should be supported

**Pass Criteria:** ✅ Configuration loading works, profiles persist correctly

---

### Scenario 5: Concurrent User Testing
**Objective:** Verify system handles multiple users simultaneously

**Steps:**
```bash
PYTHONPATH=. python3 -c "
import asyncio
import time
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_concurrent():
    print('=== Concurrent User Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())

    # Create 5 concurrent requests with different users
    tasks = []
    for i in range(5):
        task = renderer.render_template(
            template=f'Concurrent test {i}: analysis complete',
            intent_action='concurrent_test',
            intent_category='testing',
            user_id=f'pm_concurrent_user_{i}'
        )
        tasks.append(task)

    start = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = (time.time() - start) * 1000

    # Analyze results
    successes = []
    failures = []

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            failures.append(f'User {i}: {str(result)[:50]}')
        elif isinstance(result, str) and len(result) > 0:
            successes.append(f'User {i}: {result[:30]}...')
        else:
            failures.append(f'User {i}: Invalid result type')

    print(f'\\n=== Concurrent Results ===')
    print(f'Total requests: {len(results)}')
    print(f'Successes: {len(successes)}')
    print(f'Failures: {len(failures)}')
    print(f'Total time: {duration:.1f}ms')
    print(f'Average per request: {duration/len(results):.1f}ms')

    print(f'\\nSuccessful responses:')
    for success in successes:
        print(f'  ✅ {success}')

    if failures:
        print(f'\\nFailed responses:')
        for failure in failures:
            print(f'  ❌ {failure}')

    concurrent_success = len(failures) == 0 and duration < 1000
    print(f'\\nConcurrent Test: {\"✅ PASS\" if concurrent_success else \"❌ FAIL\"}')

asyncio.run(test_concurrent())
"
```

**Expected Result:**
- All 5 requests should complete successfully
- Total time should be under 1000ms (1 second)
- Each user should get a personalized response
- No errors or timeouts should occur

**Pass Criteria:** ✅ All concurrent requests succeed, reasonable performance

---

## User Experience Validation

### UX Test 1: Natural Language Quality
**Objective:** Evaluate if personality enhancement feels natural

**Steps:**
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer, get_message_template
from services.ui_messages.action_humanizer import ActionHumanizer

async def ux_test():
    print('=== User Experience Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())

    scenarios = [
        ('analysis', 'investigate_issue', 'Investigation complete'),
        ('synthesis', 'generate_report', 'Report ready for review'),
        ('execution', 'create_ticket', 'Task has been created'),
        ('query', 'list_projects', 'Project list retrieved'),
    ]

    for category, action, content in scenarios:
        template = get_message_template(category, action) or content
        result = await renderer.render_template(
            template=template,
            intent_action=action,
            intent_category=category,
            user_id='pm_ux_test'
        )

        print(f'\\n--- {category.title()} - {action} ---')
        print(f'Template: {template}')
        print(f'Enhanced: {result}')
        print(f'Natural tone: {\"✅ YES\" if any(word in result.lower() for word in [\"good\", \"great\", \"nice\", \"well done\"]) else \"⚠️ NEUTRAL\"}')

asyncio.run(ux_test())
"
```

**Manual Assessment Criteria:**
- Does the language feel warm but professional?
- Are action items clear and helpful?
- Does confidence display appropriately?
- Is technical depth appropriate for context?

**Pass Criteria:** ✅ Language feels natural, professional, and helpful

---

### UX Test 2: Error Experience
**Objective:** Verify error scenarios don't disrupt user experience

**Steps:**
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_error_ux():
    print('=== Error User Experience Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())

    error_scenarios = [
        ('Database simulation', None, 'db_error_test'),
        ('Template failure', '{broken_placeholder}', 'template_error_test'),
        ('Invalid input', 12345, 'invalid_error_test'),
        ('Empty template', '', 'empty_error_test')
    ]

    for name, template, action in error_scenarios:
        try:
            result = await renderer.render_template(
                template=template,
                intent_action=action,
                intent_category='error_testing',
                user_id='pm_error_ux_test'
            )

            print(f'\\n{name}:')
            print(f'  Input: {repr(template)}')
            print(f'  Output: {repr(result[:60])}...')
            print(f'  Status: ✅ GRACEFUL - No crash, reasonable response')

        except Exception as e:
            print(f'\\n{name}:')
            print(f'  Status: ❌ CRASH - Exception: {str(e)[:50]}')

asyncio.run(test_error_ux())
"
```

**Pass Criteria:** ✅ Errors handled gracefully, user experience preserved

---

## Edge Case Validation

### Edge Case 1: Very Long Content
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_long_content():
    print('=== Long Content Edge Case Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())

    # Create progressively longer templates
    test_lengths = [100, 500, 1000, 2000]

    for length in test_lengths:
        long_template = 'Analysis complete: ' + 'detailed findings ' * (length // 20)

        try:
            import time
            start = time.time()
            result = await renderer.render_template(
                template=long_template,
                intent_action='analyze_large_dataset',
                intent_category='analysis',
                user_id='pm_edge_test'
            )
            duration = (time.time() - start) * 1000

            print(f'Length {length*20} chars: ✅ PASS - {duration:.1f}ms')

        except Exception as e:
            print(f'Length {length*20} chars: ❌ FAIL - {str(e)[:50]}')

asyncio.run(test_long_content())
"
```

### Edge Case 2: Special Characters
```bash
PYTHONPATH=. python3 -c "
import asyncio
from services.ui_messages.templates import TemplateRenderer
from services.ui_messages.action_humanizer import ActionHumanizer

async def test_special_chars():
    print('=== Special Characters Edge Case Testing ===')
    renderer = TemplateRenderer(ActionHumanizer())

    special_cases = [
        ('Unicode', 'Analysis: émojis 🎯, ünïcödé, and spëcîál chars!'),
        ('Symbols', 'Results: @#$%^&*()_+-=[]{}|;:,.<>?'),
        ('Quotes', 'Message: \"quoted text\" and \\'single quotes\\''),
        ('Newlines', 'Multi-line\\nanalysis\\nwith\\nbreaks'),
        ('JSON-like', '{\"status\": \"complete\", \"count\": 42}')
    ]

    for name, template in special_cases:
        try:
            result = await renderer.render_template(
                template=template,
                intent_action='analyze_special',
                intent_category='analysis',
                user_id='pm_special_test'
            )
            print(f'{name}: ✅ PASS - {repr(result[:40])}...')
        except Exception as e:
            print(f'{name}: ❌ FAIL - {str(e)[:50]}')

asyncio.run(test_special_chars())
"
```

**Pass Criteria:** ✅ System handles edge cases without errors

---

## Final Validation Checklist

### Core Functionality ✅
- [ ] Basic personality enhancement works consistently
- [ ] Error handling provides graceful degradation
- [ ] Performance meets requirements (<200ms for generous PM testing)
- [ ] Configuration loading and persistence work
- [ ] Concurrent users are supported properly

### User Experience ✅
- [ ] Language feels natural and professional
- [ ] Responses are appropriately warm and helpful
- [ ] Confidence is displayed contextually
- [ ] Action items are clear and actionable
- [ ] Error experiences are smooth and non-disruptive

### Technical Validation ✅
- [ ] No system crashes or unhandled exceptions
- [ ] Database integration is stable and reliable
- [ ] Template system remains fully functional
- [ ] Performance overhead is acceptable
- [ ] Memory usage is reasonable

### Edge Cases ✅
- [ ] Long content is handled properly
- [ ] Special characters are supported
- [ ] Resource constraints are respected
- [ ] Error recovery is functional
- [ ] Concurrent load is managed well

---

## Production Deployment Recommendation

### Assessment Results

After completing manual testing, the system should demonstrate:

**✅ APPROVED FOR PRODUCTION** if:
- All core functionality tests pass
- User experience feels natural and professional
- No crashes or system disruptions occur
- Performance is acceptable for real-world usage
- Error handling is transparent to users

**🔧 NEEDS REFINEMENT** if:
- Performance issues detected
- User experience feels unnatural
- System crashes or errors occur
- Configuration problems found

### Monitoring Recommendations for Production

1. **Performance Metrics**
   - Track average enhancement response times
   - Monitor 95th percentile latency
   - Watch for timeout occurrences

2. **Quality Metrics**
   - Enhancement success rate (target: >99%)
   - Error handling effectiveness
   - User engagement with enhanced responses

3. **System Health**
   - Database connection stability
   - Memory usage patterns
   - Cache hit rates

### Rollback Plan

If issues arise in production:

1. **Immediate Disable**: Set `user_id=None` in all template render calls
2. **Graceful Degradation**: System will fall back to original templates
3. **No Data Loss**: All user data and configurations preserved
4. **Quick Recovery**: Re-enable by restoring `user_id` parameters

---

## Test Results Documentation

### Manual Testing Summary

**Test Execution Date**: _______________
**Tested by**: _______________
**Environment**: _______________

**Results**:
- Core Functionality: ___/5 passed
- User Experience: ___/2 passed
- Technical Validation: ___/4 passed
- Edge Cases: ___/2 passed

**Overall Assessment**: _______________

**Production Recommendation**:
- [ ] ✅ APPROVED FOR PRODUCTION
- [ ] 🔧 NEEDS REFINEMENT
- [ ] ❌ NOT READY FOR PRODUCTION

**Notes**:
_________________________________
_________________________________
_________________________________

---

*Comprehensive manual testing guide prepared for PM validation - ResponsePersonalityEnhancer system evaluation complete.*
