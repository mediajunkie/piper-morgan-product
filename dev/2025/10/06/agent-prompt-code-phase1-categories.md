# Prompt for Code Agent: GREAT-4E Phase 1 - Category Validation

## Context

Phase 0 complete: Test infrastructure ready with 52 stubbed tests and coverage tracking.

**This is Phase 1**: Validate all 13 intent categories work correctly through direct service interface.

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Test each of the 13 intent categories directly through IntentService to verify:
1. Handler exists and executes
2. No placeholder messages returned
3. Proper routing to domain services
4. Error handling works

---

## Phase 1: Category Validation (13 Tests)

### Strategy

Test each category in isolation through the direct service interface before testing through web/slack/cli. This validates the core handlers work before testing entry points.

### Implementation

Update: `tests/intent/test_direct_interface.py`

Each test should:
1. Create Intent with specific category
2. Call intent_service.process()
3. Verify no placeholder messages
4. Verify handler executes (not error)
5. Update coverage tracker

### Test 1/13: TEMPORAL

```python
@pytest.mark.asyncio
async def test_temporal_direct(self, intent_service):
    """DIRECT 1/13: TEMPORAL category."""
    from services.intent_service.classifier import Intent, IntentCategory
    from tests.intent.coverage_tracker import coverage
    import time

    # Create TEMPORAL intent
    intent = Intent(
        text="What's on my calendar today?",
        original_message="What's on my calendar today?",
        category=IntentCategory.TEMPORAL,
        action="calendar_query",
        confidence=0.95,
        context={}
    )

    # Measure performance
    start = time.time()
    result = await intent_service.process(intent, session_id="test_temporal")
    duration_ms = (time.time() - start) * 1000

    # Verify no placeholder
    self.assert_no_placeholder(result.message)

    # Verify handler executed (not error)
    assert result.success is not None
    assert len(result.message) > 0

    # Verify performance
    self.assert_performance(duration_ms)

    # Update coverage
    coverage.categories_tested.add("TEMPORAL")
    coverage.interfaces_tested.add("direct")
    coverage.interface_tests_passed += 1

    print(f"✓ TEMPORAL: {duration_ms:.1f}ms")
```

### Test 2/13: STATUS

```python
@pytest.mark.asyncio
async def test_status_direct(self, intent_service):
    """DIRECT 2/13: STATUS category."""
    from services.intent_service.classifier import Intent, IntentCategory
    from tests.intent.coverage_tracker import coverage
    import time

    intent = Intent(
        text="Show me my current standup status",
        original_message="Show me my current standup status",
        category=IntentCategory.STATUS,
        action="standup_query",
        confidence=0.95,
        context={}
    )

    start = time.time()
    result = await intent_service.process(intent, session_id="test_status")
    duration_ms = (time.time() - start) * 1000

    self.assert_no_placeholder(result.message)
    assert result.success is not None
    self.assert_performance(duration_ms)

    coverage.categories_tested.add("STATUS")
    coverage.interface_tests_passed += 1

    print(f"✓ STATUS: {duration_ms:.1f}ms")
```

### Test 3/13: PRIORITY

```python
@pytest.mark.asyncio
async def test_priority_direct(self, intent_service):
    """DIRECT 3/13: PRIORITY category."""
    from services.intent_service.classifier import Intent, IntentCategory
    from tests.intent.coverage_tracker import coverage
    import time

    intent = Intent(
        text="What's my top priority right now?",
        original_message="What's my top priority right now?",
        category=IntentCategory.PRIORITY,
        action="priority_query",
        confidence=0.95,
        context={}
    )

    start = time.time()
    result = await intent_service.process(intent, session_id="test_priority")
    duration_ms = (time.time() - start) * 1000

    self.assert_no_placeholder(result.message)
    assert result.success is not None
    self.assert_performance(duration_ms)

    coverage.categories_tested.add("PRIORITY")
    coverage.interface_tests_passed += 1

    print(f"✓ PRIORITY: {duration_ms:.1f}ms")
```

### Tests 4-13: Complete Pattern

Continue the same pattern for:
- 4/13: IDENTITY ("Who are you?")
- 5/13: GUIDANCE ("What should I focus on?")
- 6/13: EXECUTION ("Create GitHub issue")
- 7/13: ANALYSIS ("Analyze commits")
- 8/13: SYNTHESIS ("Generate summary")
- 9/13: STRATEGY ("Plan sprint")
- 10/13: LEARNING ("What patterns exist?")
- 11/13: UNKNOWN ("Blarghhh")
- 12/13: QUERY ("What's the weather?")
- 13/13: CONVERSATION ("Hey, how's it going?")

### After All Tests Complete

Add coverage report at end of test file:

```python
@pytest.mark.asyncio
async def test_zzz_coverage_report(self):
    """Generate coverage report after all direct tests."""
    from tests.intent.coverage_tracker import coverage

    print("\n" + "=" * 80)
    print(coverage.report())
    print("=" * 80)

    # Verify we tested all 13 categories through direct interface
    assert len(coverage.categories_tested) == 13, \
        f"Only tested {len(coverage.categories_tested)}/13 categories"

    assert "direct" in coverage.interfaces_tested

    # Should have 13 direct interface tests passing
    assert coverage.interface_tests_passed >= 13
```

---

## Running the Tests

```bash
# Run just the direct interface tests
pytest tests/intent/test_direct_interface.py -v

# Should show:
# test_temporal_direct PASSED
# test_status_direct PASSED
# ... (all 13)
# test_zzz_coverage_report PASSED
#
# 14 tests, 14 passed

# Check coverage
# Should print:
# Categories: 13/13 (100%)
# Interfaces: 1/4 (25%)
# Interface Tests: 13/52 (25%)
```

---

## Success Criteria

- [ ] All 13 category tests implemented
- [ ] All 13 tests passing
- [ ] Coverage report shows 13/13 categories tested
- [ ] No placeholder messages in any response
- [ ] All responses < 100ms
- [ ] Session log updated

---

## Critical Notes

- Use actual IntentCategory enum values (not strings)
- Verify no "Phase 3" or "full orchestration workflow" messages
- Each test must update coverage tracker
- Performance threshold: 100ms per test
- Stop if any test fails - don't proceed to Phase 2

---

**Effort**: Medium (~45-60 minutes for 13 tests)
**Priority**: HIGH (validates core functionality)
**Deliverables**: 13 passing category tests + coverage report
