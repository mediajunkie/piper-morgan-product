"""
Classification Accuracy Test Suite - GREAT-4F Phase 3

Tests that canonical categories achieve 95%+ accuracy after Phase 2 prompt enhancements.
Each category has 20+ query variants to test classification robustness.

This test suite validates the fix for the critical issue where the LLM classifier
didn't know canonical categories existed, causing mis-classification as QUERY.
"""

import pytest

from services.domain.models import IntentCategory
from services.intent.intent_service import IntentService

# #1452 wave 16: this suite drives the LIVE conftest intent_service through
# hundreds of real classifier calls (95%-accuracy sweeps over 20+ variants per
# category) — it belongs in the keyed llm lane, not the keyless CI sweep
# (wave-7 precedent: the canonical-conversation live classes).
pytestmark = pytest.mark.llm


class TestCanonicalAccuracy:
    """Test canonical categories achieve 95% accuracy threshold"""

    # Note: Uses intent_service fixture from conftest.py (removed local override after #217 refactoring)

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
        "what's your role",
        "assistant features",
        "what kind of bot",
        "tell me your purpose",
        "your function",
    ]

    @pytest.mark.asyncio
    async def test_identity_accuracy(self, intent_service):
        """IDENTITY queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.IDENTITY_VARIANTS:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == IntentCategory.IDENTITY
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": "IDENTITY",
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

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
        "when is my deadline",
        "what's scheduled",
        "meeting times today",
        "calendar events",
        "time slots available",
    ]

    @pytest.mark.asyncio
    async def test_temporal_accuracy(self, intent_service):
        """TEMPORAL queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.TEMPORAL_VARIANTS:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == IntentCategory.TEMPORAL
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": "TEMPORAL",
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

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
        "what I'm doing now",
        "current assignments",
        "my work status",
        "active projects",
        "today's work",
    ]

    @pytest.mark.asyncio
    async def test_status_accuracy(self, intent_service):
        """STATUS queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.STATUS_VARIANTS:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == IntentCategory.STATUS
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": "STATUS",
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

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
        "important items",
        "priority work",
        "what's pressing",
        "urgent priorities",
        "critical items",
    ]

    @pytest.mark.asyncio
    async def test_priority_accuracy(self, intent_service):
        """PRIORITY queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.PRIORITY_VARIANTS:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == IntentCategory.PRIORITY
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": "PRIORITY",
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

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
        "how do I create a ticket",
        "what's the process for",
        "how should I prioritize",
        "advice on managing",
        "guidance for handling",
    ]

    @pytest.mark.asyncio
    async def test_guidance_accuracy(self, intent_service):
        """GUIDANCE queries should classify correctly 95%+ of the time"""
        correct = 0
        results = []

        for query in self.GUIDANCE_VARIANTS:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == IntentCategory.GUIDANCE
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": "GUIDANCE",
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

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
        all_queries = (
            [(q, IntentCategory.IDENTITY) for q in self.IDENTITY_VARIANTS]
            + [(q, IntentCategory.TEMPORAL) for q in self.TEMPORAL_VARIANTS]
            + [(q, IntentCategory.STATUS) for q in self.STATUS_VARIANTS]
            + [(q, IntentCategory.PRIORITY) for q in self.PRIORITY_VARIANTS]
            + [(q, IntentCategory.GUIDANCE) for q in self.GUIDANCE_VARIANTS]
        )

        correct = 0
        total_queries = len(all_queries)
        category_results = {
            "IDENTITY": {"correct": 0, "total": len(self.IDENTITY_VARIANTS)},
            "TEMPORAL": {"correct": 0, "total": len(self.TEMPORAL_VARIANTS)},
            "STATUS": {"correct": 0, "total": len(self.STATUS_VARIANTS)},
            "PRIORITY": {"correct": 0, "total": len(self.PRIORITY_VARIANTS)},
            "GUIDANCE": {"correct": 0, "total": len(self.GUIDANCE_VARIANTS)},
        }

        for query, expected_category in all_queries:
            intent = await intent_service.intent_classifier.classify(query)
            if intent.category == expected_category:
                correct += 1
                category_results[expected_category.value.upper()]["correct"] += 1

        accuracy = correct / total_queries

        print(f"\n{'='*60}")
        print(f"OVERALL CANONICAL ACCURACY: {accuracy:.1%} ({correct}/{total_queries})")
        print(f"{'='*60}")

        # Print per-category breakdown
        for category, results in category_results.items():
            cat_accuracy = results["correct"] / results["total"]
            print(f"{category:>10}: {cat_accuracy:.1%} ({results['correct']}/{results['total']})")

        print(f"{'='*60}")
        print(f"Total query variants tested: {total_queries}")
        print(f"Phase 2 enhancement validation: {'✅ PASSED' if accuracy >= 0.95 else '❌ FAILED'}")

        assert accuracy >= 0.95, f"Overall canonical accuracy {accuracy:.1%} < 95%"


class TestDisambiguationEdgeCases:
    """Test edge cases that should NOT be classified as canonical categories"""

    # Note: Uses intent_service fixture from conftest.py (removed local override after #217 refactoring)

    # These should be QUERY, not canonical categories
    QUERY_EDGE_CASES = [
        # General knowledge (should be QUERY, not TEMPORAL)
        ("what time is it in Tokyo", IntentCategory.QUERY),
        ("what's the history of calendars", IntentCategory.QUERY),
        ("how do calendars work", IntentCategory.QUERY),
        # General information (should be QUERY, not STATUS)
        ("what is the status of the economy", IntentCategory.QUERY),
        ("status of climate change", IntentCategory.QUERY),
        # General rankings (should be QUERY, not PRIORITY)
        ("what are the top 10 movies", IntentCategory.QUERY),
        ("best restaurants in the city", IntentCategory.QUERY),
        # General people info (should be QUERY, not IDENTITY)
        ("who is the CEO", IntentCategory.QUERY),
        ("what is Einstein known for", IntentCategory.QUERY),
        # Factual info (should be QUERY, not GUIDANCE)
        ("what is a ticket", IntentCategory.QUERY),
        ("definition of priority", IntentCategory.QUERY),
    ]

    @pytest.mark.asyncio
    async def test_disambiguation_edge_cases(self, intent_service):
        """Edge cases should NOT be mis-classified as canonical categories"""
        correct = 0
        results = []

        for query, expected_category in self.QUERY_EDGE_CASES:
            intent = await intent_service.intent_classifier.classify(query)
            is_correct = intent.category == expected_category
            if is_correct:
                correct += 1
            results.append(
                {
                    "query": query,
                    "expected": expected_category.value,
                    "actual": intent.category.value,
                    "correct": is_correct,
                    "confidence": intent.confidence,
                }
            )

        accuracy = correct / len(self.QUERY_EDGE_CASES)

        print(f"\nDISAMBIGUATION Accuracy: {accuracy:.1%} ({correct}/{len(self.QUERY_EDGE_CASES)})")
        if accuracy < 0.90:  # Slightly lower threshold for edge cases
            print("Failed disambiguations:")
            for r in results:
                if not r["correct"]:
                    print(
                        f"  '{r['query']}' → {r['actual']} (expected: {r['expected']}, confidence: {r['confidence']:.2f})"
                    )

        assert accuracy >= 0.90, f"Disambiguation accuracy {accuracy:.1%} < 90%"
