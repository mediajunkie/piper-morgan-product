"""Test constants for GREAT-4E validation"""

# All 13 intent categories - ENUMERATE EXPLICITLY
INTENT_CATEGORIES = [
    "TEMPORAL",
    "STATUS",
    "PRIORITY",
    "IDENTITY",
    "GUIDANCE",
    "EXECUTION",
    "ANALYSIS",
    "SYNTHESIS",
    "STRATEGY",
    "LEARNING",
    "UNKNOWN",
    "QUERY",
    "CONVERSATION",
]

# All 4 interfaces - ENUMERATE EXPLICITLY
INTERFACES = [
    "web",
    "slack",
    "cli",
    "direct",
]

# Expected test counts
CATEGORY_COUNT = 13
INTERFACE_COUNT = 4
INTERFACE_TESTS = CATEGORY_COUNT * INTERFACE_COUNT  # 52
CONTRACT_TESTS = CATEGORY_COUNT * 5  # 65 (5 contracts per category)
TOTAL_TESTS = INTERFACE_TESTS + CONTRACT_TESTS  # 117

# Example queries for each category
#
# #1925 (2026-10-03): STATUS and GUIDANCE were swapped from their original
# phrasing ("Show me my current standup status" / "What should I focus on
# next?"), which stopped matching any surface-1 pattern after the #1595
# Phase 3 deletions and fell through to the LLM classifier, which the #1831
# unmarked-tier stub fails deterministically. The new phrasing matches a
# SURVIVING literal in pre_classifier.py (STATUS_PATTERNS' r"\bcurrent
# work\b"; GUIDANCE_PATTERNS' r"\bset up.*projects?\b") so the deterministic
# contract tests in tests/intent/contracts/ keep exercising Stage-1
# classification instead of silently sliding onto the LLM tier.
# TEMPORAL and PRIORITY are intentionally left unchanged: both
# TEMPORAL_PATTERNS and PRIORITY_PATTERNS are now `[]` (fully deleted, see
# pre_classifier.py), so there is no surviving literal for either category —
# any phrase assigned here would be Stage-2-only regardless of wording.
CATEGORY_EXAMPLES = {
    "TEMPORAL": "What's on my calendar today?",
    "STATUS": "Show me my current work status",
    "PRIORITY": "What's my top priority right now?",
    "IDENTITY": "Who are you and what do you do?",
    "GUIDANCE": "Help me set up my projects",
    "EXECUTION": "Create a GitHub issue about testing",
    "ANALYSIS": "Analyze recent commits in the repo",
    "SYNTHESIS": "Generate a summary of this document",
    "STRATEGY": "Help me plan the next sprint",
    "LEARNING": "What patterns do you see in my work?",
    "UNKNOWN": "Blarghhh fuzzbucket",
    "QUERY": "What's the weather in San Francisco?",
    "CONVERSATION": "Hey, how's it going?",
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "max_response_time_ms": 4000,  # 4 seconds for LLM-based classification with modern libraries (anthropic 0.69, openai 2.3) - accounts for network variability
    "min_classification_accuracy": 0.90,
    "min_cache_hit_rate": 0.80,
}
