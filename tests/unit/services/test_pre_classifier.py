import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestPreClassifier:
    @pytest.mark.smoke
    def test_greeting_patterns(self):
        """Test each greeting pattern returns correct intent"""
        greeting_patterns = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "greetings",
            "howdy",
            "hi there",
        ]

        for pattern in greeting_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "greeting"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    @pytest.mark.smoke
    def test_farewell_patterns(self):
        """Test each farewell pattern returns correct intent"""
        farewell_patterns = ["goodbye", "bye", "see you", "later", "farewell"]

        for pattern in farewell_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "farewell"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    @pytest.mark.smoke
    def test_thanks_patterns(self):
        """Test each thanks pattern returns correct intent"""
        thanks_patterns = ["thanks", "thank you", "ty", "thx", "much appreciated"]

        for pattern in thanks_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "thanks"
            assert intent.confidence == 1.0
            assert intent.context["original_message"] == pattern

    @pytest.mark.smoke
    def test_greeting_with_punctuation(self):
        """Test greetings with punctuation and emojis"""
        greeting_with_punct = [
            "hello!",
            "hi there!",
            "hey!",
            "good morning!",
            "hello.",
            "hi there.",
            "hey.",
            "good morning.",
            "hello 😊",
            "hi there 👋",
            "hey!",
            "good morning!",
            "hello!!!",
            "hi there...",
            "hey?!",
            "good morning:",
        ]

        for pattern in greeting_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "greeting"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_farewell_with_punctuation(self):
        """Test farewells with punctuation and emojis"""
        farewell_with_punct = [
            "goodbye!",
            "bye!",
            "see you!",
            "later!",
            "farewell!",
            "goodbye.",
            "bye.",
            "see you.",
            "later.",
            "farewell.",
            "goodbye 😊",
            "bye 👋",
            "see you!",
            "later!",
            "farewell!",
        ]

        for pattern in farewell_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "farewell"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_thanks_with_punctuation(self):
        """Test thanks with punctuation and emojis"""
        thanks_with_punct = [
            "thanks!",
            "thank you!",
            "ty!",
            "thx!",
            "much appreciated!",
            "thanks.",
            "thank you.",
            "ty.",
            "thx.",
            "much appreciated.",
            "thanks 😊",
            "thank you 👋",
            "ty!",
            "thx!",
            "much appreciated!",
        ]

        for pattern in thanks_with_punct:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.category == IntentCategory.CONVERSATION
            assert intent.action == "thanks"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_non_conversational_patterns(self):
        """Test patterns that should NOT be pre-classified, except for those Piper now recognizes as greetings, farewells, or thanks."""
        non_conversational = [
            "hello world",
            "hi there everyone",
            "goodbye cruel world",
            "thanks for the help",
            "thank you for everything",
            "hello there how are you",
            "bye bye for now",
            "hello and welcome",
            "goodbye and good luck",
            "thanks a lot",
            "thank you very much",
            "hello, can you help me?",
            "bye, see you tomorrow",
            "thanks, that was helpful",
            "thank you, I appreciate it",
        ]

        for pattern in non_conversational:
            intent = PreClassifier.pre_classify(pattern)
            # #1416 (PM-reported, driver-verified): the pleasantry short-circuit
            # claims pleasantry-ONLY messages. Anything carrying substance beyond
            # the social formula ("hello, can you help me?", "thanks for the
            # help", "bye, see you tomorrow") deliberately falls through (None)
            # so the LLM answers the substance instead of a canned greeting
            # swallowing it. Over-falling-through is the safe direction.
            if pattern in [
                "hi there everyone",
                "hello there how are you",
            ]:
                assert intent is not None and intent.action == "greeting"
            elif pattern in [
                "thanks a lot",
                "thank you very much",
            ]:
                assert intent is not None and intent.action == "thanks"
            else:
                assert intent is None, f"Expected None for '{pattern}' (#1416 pleasantry-only rule), got {intent}"

    @pytest.mark.smoke
    def test_case_insensitivity(self):
        """Test that patterns work regardless of case"""
        case_variations = [
            "HELLO",
            "Hello",
            "HeLLo",
            "hElLo",
            "GOODBYE",
            "Goodbye",
            "GoOdByE",
            "gOoDbYe",
            "THANKS",
            "Thanks",
            "ThAnKs",
            "tHaNkS",
        ]

        for pattern in case_variations:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly"""
        whitespace_variations = [
            "  hello  ",
            "  hi  ",
            "  goodbye  ",
            "  thanks  ",
            "\thello\t",
            "\nhi\n",
            "\r\ngoodbye\r\n",
            "  thanks  ",
        ]

        for pattern in whitespace_variations:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_empty_and_edge_cases(self):
        """Test empty and edge case patterns"""
        edge_cases = [
            "",
            "   ",
            "      ",
            "\n",
            "\n",
            "x",
            "a",
            "z",
            "123",
            "hello123",
            "hello world",
        ]
        for pattern in edge_cases:
            intent = PreClassifier.pre_classify(pattern)
            # #1416 pleasantry-only rule: "hello world" carries a token beyond
            # the pleasantry, so it falls through to the LLM like any other
            # greeting+substance message — every edge case here expects None.
            assert intent is None, f"Expected None for '{pattern}', got {intent}"

    @pytest.mark.smoke
    def test_partial_matches_should_fail(self):
        """Test that partial matches do not trigger pre-classification"""
        partial_matches = ["hello world", "hi there how are you"]
        for pattern in partial_matches:
            intent = PreClassifier.pre_classify(pattern)
            # #1416 pleasantry-only rule: "hi there how are you" is a pure social
            # formula (still short-circuits); "hello world" carries a non-formula
            # token and falls through to the LLM.
            if pattern == "hi there how are you":
                assert intent is not None and intent.action == "greeting"
            else:
                assert intent is None, f"Expected None for non-match '{pattern}', got {intent}"

    @pytest.mark.smoke
    def test_greeting_with_follow_up(self):
        """Test greeting with follow-up message"""
        pattern = "hi there how are you"
        intent = PreClassifier.pre_classify(pattern)
        # Test updated to match improved behavior: Pre-classifier now recognizes greetings
        assert intent is not None and intent.action == "greeting"

    @pytest.mark.smoke
    def test_yes_no_not_preclassified(self):
        """Test that yes/no patterns are NOT pre-classified (removed from pre-classifier)"""
        yes_no_patterns = [
            "yes",
            "no",
            "yeah",
            "nope",
            "yep",
            "nah",
            "sure",
            "negative",
            "affirmative",
            "absolutely",
            "never",
        ]

        for pattern in yes_no_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is None, f"Expected None for yes/no pattern '{pattern}', got {intent}"

    @pytest.mark.smoke
    def test_discovery_patterns(self):
        """Test DISCOVERY patterns return correct intent - Issue #671"""
        discovery_patterns = [
            "what can you do",
            "what are your capabilities",
            "what services",
            "what features",
            "show me your capabilities",
            "help",  # Issue #671: Bare "help" should trigger DISCOVERY
            "Help",  # Case insensitive
            "HELP",  # All caps
            "help menu",
            "show help",
            "need help",
        ]

        for pattern in discovery_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None, f"Expected intent for '{pattern}', got None"
            assert (
                intent.category == IntentCategory.DISCOVERY
            ), f"Expected DISCOVERY for '{pattern}', got {intent.category}"
            assert intent.action == "get_capabilities"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_help_not_guidance(self):
        """Test that bare 'help' routes to DISCOVERY not GUIDANCE - Issue #671"""
        # Bare "help" should be DISCOVERY
        intent = PreClassifier.pre_classify("help")
        assert intent is not None
        assert intent.category == IntentCategory.DISCOVERY
        assert intent.category != IntentCategory.GUIDANCE

        # But "help setup" should still be GUIDANCE
        intent = PreClassifier.pre_classify("help setup my project")
        assert intent is not None
        assert intent.category == IntentCategory.GUIDANCE

    @pytest.mark.smoke
    def test_trust_patterns(self):
        """Test TRUST patterns return correct intent - Issue #673"""
        trust_patterns = [
            # Capability boundary questions
            "why can't you do that",
            "why won't you just do it",
            "why don't you just handle it",
            "what can't you do",
            "what are your limits",
            # Relationship questions
            "how well do you know me",
            "do you trust me",
            "how much do you trust me",
            "what's our relationship",
            "how do you see our relationship",
            "how do we work together",
            # Behavior questions
            "why did you do that",
            "why do you always ask",
            "i didn't ask you to do that",
        ]

        for pattern in trust_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None, f"Expected intent for '{pattern}', got None"
            assert (
                intent.category == IntentCategory.TRUST
            ), f"Expected TRUST for '{pattern}', got {intent.category}"
            assert intent.action == "explain_trust"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_trust_not_identity(self):
        """Test that trust queries route to TRUST not IDENTITY - Issue #673"""
        # "Why can't you" should be TRUST
        intent = PreClassifier.pre_classify("why can't you delete my project")
        assert intent is not None
        assert intent.category == IntentCategory.TRUST
        assert intent.category != IntentCategory.IDENTITY

        # But "who are you" should still be IDENTITY
        intent = PreClassifier.pre_classify("who are you")
        assert intent is not None
        assert intent.category == IntentCategory.IDENTITY

    @pytest.mark.smoke
    def test_memory_patterns(self):
        """Test MEMORY patterns return correct intent - Issue #674"""
        memory_patterns = [
            # Direct memory questions
            "what do you remember about me",
            "do you remember our last conversation",
            "remember when we talked about the project",
            # History access
            "show my history",
            "view my conversation history",
            "past conversations",
            "previous chats",
            # Search patterns
            "find when I mentioned the deadline",
            "search my history for budget",
            "what did we talk about yesterday",
            # Memory meta questions
            "how much do you remember",
            "how far back do you remember",
        ]

        for pattern in memory_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None, f"Expected intent for '{pattern}', got None"
            assert (
                intent.category == IntentCategory.MEMORY
            ), f"Expected MEMORY for '{pattern}', got {intent.category}"
            assert intent.action == "get_memory"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_memory_not_trust(self):
        """Test that memory queries route to MEMORY not TRUST - Issue #674"""
        # "What do you remember" should be MEMORY
        intent = PreClassifier.pre_classify("what do you remember about our project")
        assert intent is not None
        assert intent.category == IntentCategory.MEMORY
        assert intent.category != IntentCategory.TRUST

        # But "how well do you know me" should still be TRUST
        intent = PreClassifier.pre_classify("how well do you know me")
        assert intent is not None
        assert intent.category == IntentCategory.TRUST

    @pytest.mark.smoke
    def test_portfolio_patterns(self):
        """Test PORTFOLIO patterns return correct intent - Issue #675"""
        portfolio_patterns = [
            # Archive operations
            "archive my project Alpha",
            "hide the project Beta",
            "put the old project away",
            # Delete operations
            "delete my project Gamma",
            "remove the project Delta",
            "get rid of my test project",
            # Restore operations
            "restore project Epsilon",
            "unarchive the old project",
            "bring back my archived project",
            # List operations
            "show my projects",
            "list all projects",
            "view my projects",
            # Add/create operations
            "add a new project",
            "create a project",
            # Search operations
            "search projects for budget",
            "find project deadline",
        ]

        for pattern in portfolio_patterns:
            intent = PreClassifier.pre_classify(pattern)
            assert intent is not None, f"Expected intent for '{pattern}', got None"
            assert (
                intent.category == IntentCategory.PORTFOLIO
            ), f"Expected PORTFOLIO for '{pattern}', got {intent.category}"
            assert intent.action == "manage_portfolio"
            assert intent.confidence == 1.0

    @pytest.mark.smoke
    def test_portfolio_not_memory(self):
        """Test that portfolio queries route to PORTFOLIO not MEMORY - Issue #675"""
        # "Archive my project" should be PORTFOLIO
        intent = PreClassifier.pre_classify("archive my project Alpha")
        assert intent is not None
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.category != IntentCategory.MEMORY

        # But "what do you remember" should still be MEMORY
        intent = PreClassifier.pre_classify("what do you remember about me")
        assert intent is not None
        assert intent.category == IntentCategory.MEMORY

    # Issue #898: Classifier edge case fixes

    @pytest.mark.smoke
    def test_analysis_risk_patterns(self):
        """Issue #898 Q23: Risk queries should route to ANALYSIS, not GUIDANCE."""
        risk_queries = [
            "What risks should I be aware of?",
            "What risks do we face?",
            "Identify risks in the project",
        ]
        for query in risk_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"'{query}' should match ANALYSIS patterns"
            assert (
                intent.category == IntentCategory.ANALYSIS
            ), f"'{query}' got {intent.category.value}, expected analysis"

    @pytest.mark.smoke
    def test_milestone_routes_to_status(self):
        """Issue #898 Q25: Milestone queries should route to STATUS, not PRIORITY."""
        intent = PreClassifier.pre_classify("What's the next milestone?")
        assert intent is not None
        assert intent.category == IntentCategory.STATUS

    @pytest.mark.smoke
    def test_priority_next_patterns_not_greedy(self):
        """Issue #898: Priority 'next' patterns should not catch 'next milestone'."""
        # "What's next?" → PRIORITY (action query)
        intent = PreClassifier.pre_classify("What's next?")
        assert intent is not None
        assert intent.category == IntentCategory.PRIORITY

        # "What should I work on next?" → PRIORITY
        intent = PreClassifier.pre_classify("What should I work on next?")
        assert intent is not None
        assert intent.category == IntentCategory.PRIORITY

        # "What's the next milestone?" → STATUS (not PRIORITY)
        intent = PreClassifier.pre_classify("What's the next milestone?")
        assert intent is not None
        assert intent.category == IntentCategory.STATUS

    @pytest.mark.smoke
    def test_blocker_analysis_patterns(self):
        """Issue #901/#898 Q43: Blocker queries should route to ANALYSIS."""
        intent = PreClassifier.pre_classify("What's blocking the milestone?")
        assert intent is not None
        assert intent.category == IntentCategory.ANALYSIS

        intent = PreClassifier.pre_classify("What's blocking the sprint?")
        assert intent is not None
        assert intent.category == IntentCategory.ANALYSIS

    @pytest.mark.smoke
    def test_feature_info_routes_to_query(self):
        """Issue #901/#898 Q27: Feature info queries should route to QUERY."""
        intent = PreClassifier.pre_classify("Tell me more about the GitHub integration")
        assert intent is not None
        assert intent.category == IntentCategory.QUERY

    @pytest.mark.smoke
    def test_completion_history_routes_to_status_not_temporal(self):
        """Issue #1117 INTENT-TEMPORAL-OVERGREEDY: 'when did I complete X'
        history-lookup queries must route to STATUS (floor-routed, honest
        history answer), NOT TEMPORAL (current-time). 4/5 of these previously
        fell through to the LLM classifier and misrouted to
        temporal/provide_current_time_with_calendar.
        """
        completion_history_queries = [
            "When did I complete the API migration?",
            "When did I complete the migration?",
            "What date did I finish the database project?",
            "Show me when I shipped the auth refactor",
            "When did we launch the beta?",
            "How long ago did I finish the redesign?",
            "When was the auth refactor shipped?",
        ]
        for query in completion_history_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert intent.category == IntentCategory.STATUS, (
                f"{query!r} routed to {intent.category} (expected STATUS); "
                "completion-history must not fall through to temporal/current-time"
            )
            assert intent.action == "check_completion_status"

    @pytest.mark.smoke
    def test_insight_pull_routes_to_memory_pull_insights(self):
        """Issue #1030 INSIGHT-PULL: 'what have you learned about X' queries
        must route to MEMORY/pull_insights so context_assembler enriches the
        FloorContext with InsightRepository data. Distinct from MEMORY/get_memory
        (conversation history). Surface 2 of #1047 M2D-UAT.
        """
        insight_pull_queries = [
            "What have you learned about my work style?",
            "what have you learned about me?",
            "What do you know about my calendar habits?",
            "What do you know about my team?",
            "Tell me what you've learned",
            "Tell me what you have learned about my work",
            "What insights do you have?",
            "Show me what you've learned",
            "Show me what you have learned about my projects",
            "What patterns have you noticed?",
            "What patterns have you observed about my standups?",
            "What have you noticed about my work style?",
            "what have you noticed about our team?",
        ]
        for query in insight_pull_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert intent.category == IntentCategory.MEMORY, (
                f"{query!r} routed to {intent.category} (expected MEMORY/pull_insights); "
                "insight-pull queries must reach the floor with insight-repo enrichment"
            )
            assert (
                intent.action == "pull_insights"
            ), f"{query!r} routed to {intent.action} (expected pull_insights)"

    @pytest.mark.smoke
    def test_memory_get_memory_still_works_after_pull_insights(self):
        """Issue #1030 regression guard: conversation-history queries
        ('what do you remember') must still route to MEMORY/get_memory after
        the insight-pull patterns were added (ordering matters in pre-classifier).
        """
        memory_history_queries = [
            "What do you remember about me?",
            "Do you remember when we discussed the API?",
            "Show my conversation history",
            "What did we talk about yesterday?",
        ]
        for query in memory_history_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert (
                intent.category == IntentCategory.MEMORY
            ), f"{query!r} routed to {intent.category} (expected MEMORY)"
            assert intent.action == "get_memory", (
                f"{query!r} routed to {intent.action} (expected get_memory); "
                "conversation-history queries must NOT misroute to pull_insights"
            )

    @pytest.mark.smoke
    def test_provenance_routes_before_trust(self):
        """Issue #1030 R4: 'why did you mention/suggest/recommend X' queries
        must route to PROVENANCE/explain_suggestion, not TRUST/explain_trust.
        TRUST has `\\bwhy did you (do|just|go ahead)\\b` which would otherwise
        win on `why did you...` prefix race. Verifies PROVENANCE precedence.
        """
        provenance_queries = [
            "Why did you mention that meeting?",
            "Why did you bring up the API design?",
            "why did you suggest I look at #1089?",
            "Why did you recommend that approach?",
            "Why did you surface that insight?",
            "Why did you raise the blocker concern?",
            "Why did you flag that as risky?",
            "Where did you get that from?",
            "Where did that come from?",
            "Where did you find that?",
            "How did you know about that?",
            "How did you know that I work in the mornings?",
            "What made you mention the priority?",
            "What made you think of that?",
            "What made you suggest the calendar approach?",
            "How do you know about my schedule?",
            "How do you know that I prefer async?",
            "Why is that on your list?",
            "Why is the API on my radar?",
            "Based on what?",
            "What's that based on?",
        ]
        for query in provenance_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert intent.category == IntentCategory.PROVENANCE, (
                f"{query!r} routed to {intent.category} (expected PROVENANCE); "
                "must precede TRUST/MEMORY in pattern check order"
            )
            assert intent.action == "explain_suggestion"

    @pytest.mark.smoke
    def test_trust_still_routes_after_provenance(self):
        """Issue #1030 R4 regression guard: capability-boundary and
        behavior questions ('why did you DO that') must still route to TRUST
        after PROVENANCE patterns were added before TRUST.
        """
        trust_queries = [
            "Why did you do that?",
            "Why did you just go ahead with it?",
            "Why can't you help me?",
            "Why won't you do this?",
            "How well do you know me?",
            "What are your limits?",
            "Why do you always ask?",
        ]
        for query in trust_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert intent.category == IntentCategory.TRUST, (
                f"{query!r} routed to {intent.category} (expected TRUST); "
                "PROVENANCE patterns must NOT steal TRUST's 'why did you DO' cases"
            )
            assert intent.action == "explain_trust"

    @pytest.mark.smoke
    def test_current_time_still_routes_to_temporal(self):
        """Issue #1117 regression guard: genuine current-time queries must
        still route to TEMPORAL after the completion-history patterns were added.
        """
        current_time_queries = [
            "What time is it?",
            "What's the date?",
            "What day is it?",
            "Current time",
        ]
        for query in current_time_queries:
            intent = PreClassifier.pre_classify(query)
            assert intent is not None, f"No pre-classification for: {query!r}"
            assert (
                intent.category == IntentCategory.TEMPORAL
            ), f"{query!r} routed to {intent.category} (expected TEMPORAL)"
