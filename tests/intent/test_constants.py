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
CATEGORY_EXAMPLES = {
    "TEMPORAL": "What's on my calendar today?",
    "STATUS": "Show me my current standup status",
    "PRIORITY": "What's my top priority right now?",
    "IDENTITY": "Who are you and what do you do?",
    "GUIDANCE": "What should I focus on next?",
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
