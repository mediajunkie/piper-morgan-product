# Prompt for Cursor Agent: GREAT-4F Phase 3 - Classification Accuracy Testing

## Context

GREAT-4F mission: Validate 95%+ accuracy for canonical categories after Phase 2 prompt enhancements.

**This is Phase 3**: Create comprehensive accuracy test suite to measure classifier performance on canonical categories.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-0932-prog-cursor-log.md`

## Mission

Create test suite to measure and validate that classifier achieves 95%+ accuracy for canonical categories (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE) after Phase 2 enhancements.

---

## Background from Phase 2

**What changed**:
- Added canonical category definitions to classifier prompt
- Added disambiguation rules (TEMPORAL/STATUS/PRIORITY vs QUERY)
- Added 25 positive/negative examples
- Added confidence scoring guidance

**Expected impact**: 85-95% → 95%+ accuracy

**Now need to**: Measure actual accuracy to validate improvement

---

## Task: Create Accuracy Test Suite

**File**: `tests/intent/test_classification_accuracy.py`

### Test Structure

```python
"""
Classification Accuracy Test Suite

Tests that canonical categories achieve 95%+ accuracy after Phase 2 prompt enhancements.
Each category has 20+ query variants to test classification robustness.
"""

import pytest
from services.intent_service import IntentService
from services.intent_service.classifier import IntentCategory

class TestCanonicalAccuracy:
    """Test canonical categories achieve 95% accuracy threshold"""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance for testing"""
        return IntentService()

    # IDENTITY Accuracy (Target: 95%+)

    IDENTITY_VARIANTS = [
        "who are you",
        "what are you",
        "tell me about yourself",
        "what can you do",
        "what are your capabilities",
        "introduce yourself",
        "who am I talking to",
        "what kind of assistant are you",
        "what is your purpose",
        "describe yourself",
        "what are you capable of",
        "tell me about your features",
        "what do you do",
        "explain what you are",
        "your identity please",
        "who is this",
        "what bot is this",
        "assistant info",
        "bot capabilities",
        "your abilities",
        # 20+ variants recommended
    ]

    @pytest.mark.asyncio
    async def test_identity_accuracy(self, intent_service):
        """IDENTITY queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.IDENTITY_VARIANTS:
            intent = await intent_service.classify_intent(query, session_id="test")
            is_correct = intent.category == IntentCategory.IDENTITY
            if is_correct:
                correct += 1
            results.append({
                "query": query,
                "expected": "IDENTITY",
                "actual": intent.category.value,
                "correct": is_correct,
                "confidence": intent.confidence
            })

        accuracy = correct / len(self.IDENTITY_VARIANTS)

        # Log results for analysis
        print(f"\nIDENTITY Accuracy: {accuracy:.1%} ({correct}/{len(self.IDENTITY_VARIANTS)})")
        if accuracy < 0.95:
            print("Failed classifications:")
            for r in results:
                if not r["correct"]:
                    print(f"  '{r['query']}' → {r['actual']} (confidence: {r['confidence']:.2f})")

        assert accuracy >= 0.95, f"IDENTITY accuracy {accuracy:.1%} < 95%"

    # TEMPORAL Accuracy (Target: 95%+)

    TEMPORAL_VARIANTS = [
        "what's on my calendar",
        "show my schedule",
        "when is my next meeting",
        "what do I have today",
        "calendar for tomorrow",
        "my appointments this week",
        "schedule for monday",
        "what time is my meeting",
        "show me today's events",
        "what's coming up",
        "my agenda today",
        "when am I free",
        "available time slots",
        "next available meeting time",
        "schedule overview",
        "what's on my plate today",
        "my meetings this week",
        "today's schedule",
        "upcoming appointments",
        "calendar view",
        "when is the team meeting",
        "what time is standup",
        "schedule for this afternoon",
        "my calendar today",
        "show events",
        # 25+ variants recommended
    ]

    @pytest.mark.asyncio
    async def test_temporal_accuracy(self, intent_service):
        """TEMPORAL queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.TEMPORAL_VARIANTS:
            intent = await intent_service.classify_intent(query, session_id="test")
            is_correct = intent.category == IntentCategory.TEMPORAL
            if is_correct:
                correct += 1
            results.append({
                "query": query,
                "expected": "TEMPORAL",
                "actual": intent.category.value,
                "correct": is_correct,
                "confidence": intent.confidence
            })

        accuracy = correct / len(self.TEMPORAL_VARIANTS)

        print(f"\nTEMPORAL Accuracy: {accuracy:.1%} ({correct}/{len(self.TEMPORAL_VARIANTS)})")
        if accuracy < 0.95:
            print("Failed classifications:")
            for r in results:
                if not r["correct"]:
                    print(f"  '{r['query']}' → {r['actual']} (confidence: {r['confidence']:.2f})")

        assert accuracy >= 0.95, f"TEMPORAL accuracy {accuracy:.1%} < 95%"

    # STATUS Accuracy (Target: 95%+)

    STATUS_VARIANTS = [
        "show my standup",
        "what am I working on",
        "my current status",
        "work progress",
        "what's my status",
        "show status update",
        "current tasks",
        "what am I doing",
        "my work today",
        "progress on projects",
        "what's in progress",
        "current sprint status",
        "my active tasks",
        "show my work",
        "what am I focused on",
        "current workload",
        "status report",
        "my task status",
        "what's on my plate",
        "working on today",
        "current projects",
        "my sprint status",
        "task progress",
        "work status",
        "show my progress",
        # 25+ variants recommended
    ]

    @pytest.mark.asyncio
    async def test_status_accuracy(self, intent_service):
        """STATUS queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.STATUS_VARIANTS:
            intent = await intent_service.classify_intent(query, session_id="test")
            is_correct = intent.category == IntentCategory.STATUS
            if is_correct:
                correct += 1
            results.append({
                "query": query,
                "expected": "STATUS",
                "actual": intent.category.value,
                "correct": is_correct,
                "confidence": intent.confidence
            })

        accuracy = correct / len(self.STATUS_VARIANTS)

        print(f"\nSTATUS Accuracy: {accuracy:.1%} ({correct}/{len(self.STATUS_VARIANTS)})")
        if accuracy < 0.95:
            print("Failed classifications:")
            for r in results:
                if not r["correct"]:
                    print(f"  '{r['query']}' → {r['actual']} (confidence: {r['confidence']:.2f})")

        assert accuracy >= 0.95, f"STATUS accuracy {accuracy:.1%} < 95%"

    # PRIORITY Accuracy (Target: 95%+)

    PRIORITY_VARIANTS = [
        "what should I focus on",
        "my top priorities",
        "what's most important",
        "show priorities",
        "what's urgent",
        "priorities today",
        "what needs attention",
        "critical tasks",
        "top items",
        "what should I prioritize",
        "focus areas",
        "important tasks",
        "what's high priority",
        "urgent items",
        "key priorities",
        "what matters most",
        "priority list",
        "most important work",
        "what's critical",
        "focus priorities",
        "top focus areas",
        "priority tasks",
        "what to work on first",
        "highest priority",
        "key focus areas",
        # 25+ variants recommended
    ]

    @pytest.mark.asyncio
    async def test_priority_accuracy(self, intent_service):
        """PRIORITY queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.PRIORITY_VARIANTS:
            intent = await intent_service.classify_intent(query, session_id="test")
            is_correct = intent.category == IntentCategory.PRIORITY
            if is_correct:
                correct += 1
            results.append({
                "query": query,
                "expected": "PRIORITY",
                "actual": intent.category.value,
                "correct": is_correct,
                "confidence": intent.confidence
            })

        accuracy = correct / len(self.PRIORITY_VARIANTS)

        print(f"\nPRIORITY Accuracy: {accuracy:.1%} ({correct}/{len(self.PRIORITY_VARIANTS)})")
        if accuracy < 0.95:
            print("Failed classifications:")
            for r in results:
                if not r["correct"]:
                    print(f"  '{r['query']}' → {r['actual']} (confidence: {r['confidence']:.2f})")

        assert accuracy >= 0.95, f"PRIORITY accuracy {accuracy:.1%} < 95%"

    # GUIDANCE Accuracy (Target: 95%+)

    GUIDANCE_VARIANTS = [
        "how should I approach this",
        "what's the best way to",
        "give me advice on",
        "recommend an approach",
        "suggest a strategy",
        "how do I handle",
        "what would you recommend",
        "best practices for",
        "guidance on this",
        "advice for dealing with",
        "how to tackle",
        "suggestions for",
        "what's your recommendation",
        "help me decide",
        "guide me through",
        "what should I do about",
        "how would you handle",
        "advise me on",
        "recommend a solution",
        "what's the right approach",
        "how to proceed with",
        "guidance needed",
        "your recommendation",
        "advice on handling",
        "best way forward",
        # 25+ variants recommended
    ]

    @pytest.mark.asyncio
    async def test_guidance_accuracy(self, intent_service):
        """GUIDANCE queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.GUIDANCE_VARIANTS:
            intent = await intent_service.classify_intent(query, session_id="test")
            is_correct = intent.category == IntentCategory.GUIDANCE
            if is_correct:
                correct += 1
            results.append({
                "query": query,
                "expected": "GUIDANCE",
                "actual": intent.category.value,
                "correct": is_correct,
                "confidence": intent.confidence
            })

        accuracy = correct / len(self.GUIDANCE_VARIANTS)

        print(f"\nGUIDANCE Accuracy: {accuracy:.1%} ({correct}/{len(self.GUIDANCE_VARIANTS)})")
        if accuracy < 0.95:
            print("Failed classifications:")
            for r in results:
                if not r["correct"]:
                    print(f"  '{r['query']}' → {r['actual']} (confidence: {r['confidence']:.2f})")

        assert accuracy >= 0.95, f"GUIDANCE accuracy {accuracy:.1%} < 95%"

    # Overall Accuracy Summary

    @pytest.mark.asyncio
    async def test_overall_canonical_accuracy(self, intent_service):
        """Overall canonical category accuracy should be 95%+"""
        all_queries = [
            (q, IntentCategory.IDENTITY) for q in self.IDENTITY_VARIANTS
        ] + [
            (q, IntentCategory.TEMPORAL) for q in self.TEMPORAL_VARIANTS
        ] + [
            (q, IntentCategory.STATUS) for q in self.STATUS_VARIANTS
        ] + [
            (q, IntentCategory.PRIORITY) for q in self.PRIORITY_VARIANTS
        ] + [
            (q, IntentCategory.GUIDANCE) for q in self.GUIDANCE_VARIANTS
        ]

        correct = 0
        for query, expected_category in all_queries:
            intent = await intent_service.classify_intent(query, session_id="test")
            if intent.category == expected_category:
                correct += 1

        accuracy = correct / len(all_queries)

        print(f"\n{'='*60}")
        print(f"OVERALL CANONICAL ACCURACY: {accuracy:.1%} ({correct}/{len(all_queries)})")
        print(f"{'='*60}")

        assert accuracy >= 0.95, f"Overall canonical accuracy {accuracy:.1%} < 95%"
```

---

## Verification

After creating tests:

```bash
# Run accuracy tests
pytest tests/intent/test_classification_accuracy.py -v -s

# Expected output:
# IDENTITY Accuracy: 95%+
# TEMPORAL Accuracy: 95%+
# STATUS Accuracy: 95%+
# PRIORITY Accuracy: 95%+
# GUIDANCE Accuracy: 95%+
# OVERALL CANONICAL ACCURACY: 95%+

# Should show 6 passing tests
```

---

## Success Criteria

- [ ] Test suite created with 6 test methods
- [ ] 20+ query variants for each canonical category (100+ total)
- [ ] Tests measure actual classification accuracy
- [ ] Failed classifications are logged for analysis
- [ ] Overall accuracy test included
- [ ] All tests pass (95%+ accuracy achieved)
- [ ] Session log updated

---

## Critical Notes

- If accuracy <95% on first run, that's OK - we need to measure baseline
- Log all failed classifications for analysis
- Consider adding more variants if certain patterns fail
- Tests should be comprehensive but realistic (common user phrasings)

---

## STOP Conditions

- If IntentService.classify_intent method doesn't exist as expected, document and ask PM
- If tests take too long to run (>2 minutes), consider reducing variant count
- If accuracy significantly worse after Phase 2 changes, stop and investigate

---

**Effort**: Medium (~30-45 minutes to write comprehensive tests)
**Priority**: HIGH (validates Phase 2 improvements)
**Deliverable**: Comprehensive accuracy test suite with 95%+ validation
