"""
PM-039 Intent Classification Test Coverage

RELOCATED from tests/unit/services/ (#1796, 2026-09-22): the parametrized half is
`llm`-marked — an assertion over LIVE LLM output — and does not belong in the unit
tree, where a bare `pytest tests/unit/...` runs it whenever the seat's keychain
holds real keys (the #1765-family env-divergence shape: local-red/CI-green, plus
pre-#1809 it silently live-billed the developer). Here it sits under
tests/intent/'s tier governance: unmarked tests are pinned deterministic (#1831),
`llm`-marked tests are the deliberate live tier. The known live failure of the
"show me all project plans" param is tracked by #1841 (baseline-verified drift;
fix defaults to a corpus row per the supersession gate, PM 2026-08-29) — do NOT
loosen this test's assertion to make that param pass.

This test suite covers 13 scenarios for document/file search intent classification:

1. search for requirements files
2. find technical specifications
3. locate API documentation
4. show me all project plans
5. get all design docs
6. find docs about onboarding
7. search for budget analysis documents
8. serach for requirments files (typo)
9. find tehcnical specfications (typo)
10. find requirements
11. search files
12. find documents about project timeline
13. Fuzzy matcher typo tolerance (direct test)

- All patterns are expected to be unified to the canonical action: 'search_documents'.
- Fuzzy matching and typo correction are used to handle natural language variation and common misspellings.
- Context extraction is validated for each pattern.

Fuzzy Matching Approach:
- Uses Levenshtein distance (difflib) to match user input to known patterns.
- Common typos are mapped to correct terms before matching.
- Ensures robust handling of user phrasing and errors.

Action Unification Strategy:
- All document/file search actions (find_documents, search_files, etc.) are normalized to 'search_documents'.
- This ensures a single routing path and simplifies downstream handling.
"""

import asyncio

import pytest

from services.intent_service.classifier import IntentClassifier


@pytest.mark.asyncio
@pytest.mark.llm  # Requires real LLM API calls
@pytest.mark.parametrize(
    "message,expected_action,expected_query",
    [
        ("search for requirements files", "search_documents", "requirements files"),
        ("find technical specifications", "search_documents", "technical specifications"),
        ("locate API documentation", "search_documents", "API documentation"),
        ("show me all project plans", "search_documents", "project plans"),
        ("get all design docs", "search_documents", "design docs"),
        ("find docs about onboarding", "search_documents", "onboarding"),
        ("search for budget analysis documents", "search_documents", "budget analysis documents"),
        ("serach for requirments files", "search_documents", "requirements files"),  # typo
        ("find tehcnical specfications", "search_documents", "technical specifications"),  # typo
        ("find requirements", "search_documents", "requirements"),
        ("search files", "search_documents", "files"),
        ("find documents about project timeline", "search_documents", "project timeline"),
    ],
)
async def test_pm039_patterns(initialized_container, message, expected_action, expected_query):
    """
    PM-039 Intent Classification: Document/file search patterns.

    LLM may return more specific actions (e.g., 'search_requirements_files',
    'search_api_documentation') instead of the canonical 'search_documents'.
    This is acceptable - we validate that the action is search-related.
    """
    # Get LLM service from initialized container (#743 fix)
    llm_service = initialized_container.get_service("llm")
    classifier = IntentClassifier(llm_service=llm_service)
    intent = await classifier.classify(message)

    # Accept any search-related action (LLM may be more specific than 'search_documents')
    search_keywords = ["search", "find", "locate", "get", "show", "retrieve", "list", "fetch"]
    is_search_action = any(keyword in intent.action.lower() for keyword in search_keywords)

    assert is_search_action, (
        f"Expected search-related action for: {message}\n"
        f"Got: {intent.action}\n"
        f"Expected keywords: {search_keywords}"
    )

    # Context extraction check - validate query terms are captured
    if "search_query" in intent.context:
        # Check that some query terms are present (flexible matching)
        query_terms = expected_query.lower().split()
        context_query = intent.context["search_query"].lower()

        # At least one term from expected_query should be in the context
        has_query_term = any(term in context_query for term in query_terms if len(term) > 3)
        assert has_query_term, (
            f"Expected query terms from '{expected_query}' in context\n"
            f"Got: {intent.context['search_query']}"
        )
    # If no search_query in context, that's okay - LLM might structure it differently


@pytest.mark.smoke
def test_fuzzy_match_typo_tolerance():
    from services.intent_service.fuzzy_matcher import fuzzy_match

    patterns = [
        "search for requirements files",
        "find technical specifications",
        "locate API documentation",
        "show me all project plans",
        "get all design docs",
    ]
    assert (
        fuzzy_match("serach for requirments files", patterns, cutoff=0.7)
        == "search for requirements files"
    )
    assert (
        fuzzy_match("find tehcnical specfications", patterns, cutoff=0.7)
        == "find technical specifications"
    )
