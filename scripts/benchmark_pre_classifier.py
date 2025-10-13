#!/usr/bin/env python3
"""
Pre-Classifier Hit Rate Benchmark

Measures how many queries hit the pre-classifier vs fall through to LLM.
Target: ≥10% hit rate on representative query set.

Created for #212 Phase 3 (CORE-INTENT-ENHANCE)
"""

from services.intent_service.pre_classifier import PreClassifier


def main():
    pre_classifier = PreClassifier()

    # Representative common queries covering all categories
    # Distribution matches expected real-world usage:
    # - 25% TEMPORAL (very common: time, calendar, schedule)
    # - 20% STATUS (common: standup, progress, work status)
    # - 15% PRIORITY (common: focus, urgent, important)
    # - 10% IDENTITY (occasional: capabilities, features)
    # - 10% GUIDANCE (occasional: how-to, advice)
    # - 20% workflow queries that should NOT match (EXECUTION, ANALYSIS, etc.)

    common_queries = [
        # TEMPORAL (25 queries - 25%)
        "what time is it",
        "what's the date",
        "what day is it",
        "show my calendar",
        "my schedule",
        "what's on my calendar",
        "next meeting",
        "upcoming meetings",
        "when is my meeting",
        "my appointments",
        "events today",
        "meetings this week",
        "when am i free",
        "calendar today",
        "show schedule",
        "my events",
        "what's tomorrow",
        "schedule tomorrow",
        "meetings tomorrow",
        "agenda today",
        "what's on my schedule",
        "upcoming events",
        "available time",
        "free time",
        "open slots",
        # STATUS (20 queries - 20%)
        "standup",
        "what am i working on",
        "my progress",
        "current status",
        "my projects",
        "project status",
        "status update",
        "what's my status",
        "show status",
        "my tasks",
        "current work",
        "active projects",
        "working on now",
        "show projects",
        "current tasks",
        "my standup",
        "progress update",
        "task status",
        "work status",
        "my assignments",
        # PRIORITY (15 queries - 15%)
        "my priorities",
        "what should i focus on",
        "top priority",
        "what's most important",
        "urgent tasks",
        "critical items",
        "what's urgent",
        "focus areas",
        "what should i do first",
        "highest priority",
        "most important",
        "needs attention",
        "what's critical",
        "key priorities",
        "urgent work",
        # IDENTITY (10 queries - 10%)
        "what can you do",
        "who are you",
        "your capabilities",
        "what do you do",
        "tell me about yourself",
        "introduce yourself",
        "what are you capable of",
        "your features",
        "bot capabilities",
        "what's your role",
        # GUIDANCE (10 queries - 10%)
        "how do i create an issue",
        "what's the best way to",
        "guidance",
        "recommendation",
        "advice",
        "next steps",
        "how do i handle this",
        "suggest an approach",
        "what would you recommend",
        "best practices",
        # Workflow queries that should NOT match (20 queries - 20%)
        "create an issue for bug",
        "analyze these commits",
        "generate a report",
        "summarize the document",
        "list all projects",  # Should be QUERY, not STATUS
        "create a ticket",
        "update the issue",
        "delete that task",
        "review this code",
        "analyze performance",
        "synthesize findings",
        "plan the sprint",
        "create a strategy",
        "learn from feedback",
        "query the database",
        "fetch project data",
        "hello there",  # CONVERSATION (greeting) - should match
        "thanks",  # CONVERSATION (thanks) - should match
        "goodbye",  # CONVERSATION (farewell) - should match
        "implement feature X",
    ]

    hits = 0
    total = len(common_queries)
    hit_details = []
    category_hits = {
        "TEMPORAL": 0,
        "STATUS": 0,
        "PRIORITY": 0,
        "IDENTITY": 0,
        "GUIDANCE": 0,
        "CONVERSATION": 0,
        "OTHER": 0,
    }

    for query in common_queries:
        result = pre_classifier.pre_classify(query)
        if result is not None:  # Hit
            hits += 1
            category = result.category.value.upper()
            if category in category_hits:
                category_hits[category] += 1
            else:
                category_hits["OTHER"] += 1
            hit_details.append(f"✓ '{query}' → {category}")
        else:
            hit_details.append(f"✗ '{query}' → (LLM fallback)")

    hit_rate = (hits / total) * 100

    print(f"\n{'='*70}")
    print(f"Pre-Classifier Hit Rate Benchmark - Phase 3")
    print(f"{'='*70}")
    print(f"Total queries: {total}")
    print(f"Pattern hits: {hits}")
    print(f"LLM fallback: {total - hits}")
    print(f"Hit rate: {hit_rate:.1f}%")
    print(f"{'='*70}\n")

    print("Hit distribution by category:")
    for category, count in category_hits.items():
        if count > 0:
            print(f"  {category}: {count} hits")

    print(f"\n{'='*70}")
    print("Sample results (first 30):")
    print(f"{'='*70}")
    for detail in hit_details[:30]:
        print(detail)

    if len(hit_details) > 30:
        print(f"\n... and {len(hit_details) - 30} more results")

    # Target check
    print(f"\n{'='*70}")
    if hit_rate >= 10.0:
        print(f"✅ SUCCESS: Hit rate {hit_rate:.1f}% exceeds 10% target")
    else:
        print(f"⚠️  NEEDS WORK: Hit rate {hit_rate:.1f}% below 10% target")
    print(f"{'='*70}\n")

    return hit_rate >= 10.0


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
