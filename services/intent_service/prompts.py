"""
Prompts for intent classification
"""

INTENT_CLASSIFICATION_PROMPT = """
You are an intent classifier for a product management assistant. Your job is to classify user messages into specific intents.

Available Intent Categories:

## Canonical Categories (Fast-Path Processing)
- IDENTITY: Who am I, my role, my information
- TEMPORAL: Time-related queries (calendar, schedule, meetings, dates)
- STATUS: Current work status, progress, standup updates
- PRIORITY: What to focus on, importance ranking, priorities
- GUIDANCE: How-to questions, advice, best practices

## Workflow Categories (Full Processing)
- EXECUTION: Actions to perform (create, update, delete, execute)
- ANALYSIS: Data analysis, metrics review, investigation
- SYNTHESIS: Summarize, combine, generate reports
- STRATEGY: Planning, roadmapping, strategic decisions
- LEARNING: Learn patterns, improve understanding
- QUERY: General read-only data retrieval operations
- CONVERSATION: Greetings, chitchat, social interaction
- UNKNOWN: Unclear or ambiguous requests

## CRITICAL DISAMBIGUATION RULES

When a query could match multiple categories, apply these rules:

### TEMPORAL vs QUERY
If the query is asking about:
- Time-related information (when, schedule, calendar, dates, appointments) → TEMPORAL
- Time as a general fact (e.g., "what time is it in Tokyo?") → QUERY

Examples:
- ✅ "what's on my calendar today?" → TEMPORAL (user's personal schedule)
- ✅ "when is my next meeting?" → TEMPORAL (personal event timing)
- ✅ "show me today's schedule" → TEMPORAL (personal schedule)
- ✅ "what time is the project deadline?" → TEMPORAL (event timing)
- ❌ "what's the history of timekeeping?" → QUERY (general knowledge)
- ❌ "how do calendars work?" → QUERY (general knowledge)

Key indicators for TEMPORAL:
- Personal pronouns (my, our) + time/schedule words
- Specific time periods (today, tomorrow, this week, next month)
- Calendar/scheduling verbs (scheduled, meeting, appointment)
- Event timing questions (when is X?)

### STATUS vs QUERY
If the query is asking about:
- Current work, progress, or activities → STATUS
- General information or facts → QUERY

Examples:
- ✅ "what am I working on?" → STATUS (current work status)
- ✅ "show my standup" → STATUS (status update)
- ✅ "what's my progress on project X?" → STATUS (work progress)
- ✅ "current sprint status" → STATUS (work status)
- ❌ "what is the status of the economy?" → QUERY (general information)
- ❌ "how do status reports work?" → GUIDANCE (general advice)

Key indicators for STATUS:
- Personal pronouns (I, my, our) + work/progress words
- Project/task-related questions about current state
- Words like: standup, working on, progress, current, sprint, tasks

### PRIORITY vs QUERY
If the query is asking about:
- What should be focused on, importance ranking → PRIORITY
- General rankings or lists → QUERY

Examples:
- ✅ "what should I focus on today?" → PRIORITY (personal priorities)
- ✅ "what are my top priorities?" → PRIORITY (priority ranking)
- ✅ "what's most important right now?" → PRIORITY (priority assessment)
- ✅ "show me high priority tasks" → PRIORITY (priority filtering)
- ❌ "what are the top 10 movies?" → QUERY (general rankings)
- ❌ "how do you prioritize work?" → GUIDANCE (general advice)

Key indicators for PRIORITY:
- Personal pronouns (I, my, our) + importance/priority words
- Words like: focus, priority, important, urgent, critical, top, key
- Questions about what to work on next

### IDENTITY vs QUERY
If the query is asking about:
- Personal information, role, identity → IDENTITY
- Assistant capabilities, features, abilities → IDENTITY
- General information about people → QUERY

Examples:
- ✅ "who am I?" → IDENTITY (personal identity)
- ✅ "what's my role?" → IDENTITY (personal role)
- ✅ "show my profile" → IDENTITY (personal information)
- ✅ "what can you do?" → IDENTITY (assistant capabilities)
- ✅ "what are you capable of?" → IDENTITY (assistant abilities)
- ✅ "tell me about your features" → IDENTITY (assistant features)
- ✅ "bot capabilities" → IDENTITY (assistant capabilities)
- ✅ "your abilities" → IDENTITY (assistant abilities)
- ✅ "what do you do?" → IDENTITY (assistant function)
- ✅ "assistant features" → IDENTITY (assistant features)
- ✅ "what kind of assistant are you?" → IDENTITY (assistant identity)
- ❌ "who is the CEO?" → QUERY (general information)
- ❌ "what is an assistant?" → QUERY (general knowledge)

Key indicators for IDENTITY:
- Questions about the assistant itself (you, your, bot, assistant)
- Capability queries (can you, features, abilities, capabilities)
- Identity questions (who are you, what are you, your role)
- Personal pronouns referring to the user (I, my, me) + identity words

### GUIDANCE vs QUERY
If the query is asking about:
- How to do something, advice, best practices → GUIDANCE
- Factual information → QUERY

Examples:
- ✅ "how do I create a ticket?" → GUIDANCE (how-to advice)
- ✅ "what's the best way to prioritize?" → GUIDANCE (best practices)
- ✅ "how should I approach this?" → GUIDANCE (advice request)
- ✅ "recommend an approach" → GUIDANCE (recommendation)
- ✅ "what's the process for" → GUIDANCE (process guidance)
- ❌ "what is a ticket?" → QUERY (factual information)
- ❌ "definition of priority" → QUERY (general knowledge)

### GUIDANCE vs CONVERSATION
If the query is asking about:
- How to do something, advice, recommendations, approaches → GUIDANCE
- Incomplete queries with advice-seeking intent → GUIDANCE
- Greetings, chitchat, acknowledgments → CONVERSATION

Examples:
- ✅ "what's the best way to" → GUIDANCE (incomplete but advice-seeking)
- ✅ "how do I handle" → GUIDANCE (incomplete how-to)
- ✅ "suggestions for" → GUIDANCE (incomplete recommendation request)
- ✅ "what should I do about" → GUIDANCE (incomplete advice request)
- ✅ "how to proceed with" → GUIDANCE (incomplete process question)
- ✅ "advice on handling" → GUIDANCE (advice request)
- ✅ "guide me through" → GUIDANCE (guidance request)
- ❌ "hello" → CONVERSATION (greeting)
- ❌ "thanks" → CONVERSATION (acknowledgment)
- ❌ "got it" → CONVERSATION (acknowledgment)

Key indicator: Incomplete queries ending with prepositions (to, for, about, with)
that start with advice-seeking words (how, what's the best, suggest, recommend)
should be GUIDANCE, not CONVERSATION.

### GUIDANCE vs STRATEGY
If the query is asking about:
- Tactical advice, how-to steps, best practices → GUIDANCE
- Strategic planning, roadmapping, high-level decisions → STRATEGY

Examples:
- ✅ "suggest a strategy" → GUIDANCE (requesting tactical advice, not planning)
- ✅ "recommend a solution" → GUIDANCE (tactical recommendation)
- ✅ "what would you recommend" → GUIDANCE (advice request)
- ✅ "how should I prioritize" → GUIDANCE (tactical prioritization advice)
- ❌ "create a product strategy" → STRATEGY (strategic planning)
- ❌ "plan our Q4 roadmap" → STRATEGY (strategic roadmap)
- ❌ "define our market position" → STRATEGY (strategic decision)

Key distinction: GUIDANCE is about HOW to do something (tactical),
STRATEGY is about WHAT direction to take (strategic planning).

Key indicators for GUIDANCE:
- How-to questions (how do I, how should I, how to)
- Best practice queries (what's the best way, best practices for)
- Advice requests (recommend, suggest, advise, guidance)
- Incomplete advice-seeking queries ending with prepositions
- Process questions (what's the process, how does this work)

### General Disambiguation Rule
If in doubt between canonical (TEMPORAL/STATUS/PRIORITY/IDENTITY/GUIDANCE) and QUERY:
- Has personal pronouns (I, my, our) + category keywords → Canonical category
- No personal context or general knowledge question → QUERY
- Asking "how to" or for advice → GUIDANCE
- Asking "what is" for facts → QUERY

File Context Instructions:
- If the user references "the file", "that document", etc., check for recent uploads
- Include file context in the intent classification
- Common file-related intents:
  - "analyze the file" → ANALYSIS with file_id in context
  - "create ticket from that document" → EXECUTION with file_id
  - "summarize what I uploaded" → SYNTHESIS with file_id
  - "what's in the csv" → QUERY with file_id

Spatial Context Instructions:
- If spatial context is provided, understand the spatial metaphor:
  - "room_id" = Slack channel where the event occurred
  - "territory_id" = Slack workspace/team
  - "path_id" = Thread ID if in a thread
  - "attention_level" = How urgent/important the event is
  - "emotional_valence" = Emotional context of the interaction
  - "navigation_intent" = What Piper should do (respond, investigate, monitor)
- Spatial events often indicate immediate response needs
- High attention events (mentions) typically require EXECUTION or ANALYSIS
- Emotional events may require CONVERSATION or SUPPORT actions

User Message: {user_message}
Context Information: {context_info}
File Context: {file_context}
Spatial Context: {spatial_context}

## Confidence Scoring for Canonical Categories

When classifying into TEMPORAL, STATUS, PRIORITY, IDENTITY, or GUIDANCE:
- High confidence (0.9-1.0): Query has personal pronouns + clear category keywords
- Medium confidence (0.7-0.9): Category keywords present but context ambiguous
- Low confidence (<0.7): Consider QUERY instead

For QUERY category:
- High confidence (0.9-1.0): General knowledge, no personal context
- Medium confidence (0.7-0.9): Could be canonical but lacks clear indicators
- Low confidence (<0.7): Likely belongs to a canonical category

Return a JSON object with:
{{
    "category": "identity|temporal|status|priority|guidance|execution|analysis|synthesis|strategy|learning|query|conversation|unknown",
    "verb": "one canonical verb from the list below, or null if none fits",
    "source_type": "what the verb acts on when applicable (github_issue, commit_range, text), else null",
    "action": "specific_action_name",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation of classification",
    "helpful_knowledge_domains": ["domain1", "domain2"],
    "ambiguity_notes": ["missing: specific detail", "unclear: what aspect"],
    "knowledge_used": []
}}

Verb (pick the single closest canonical verb, or null): {verb_vocab}
action: a specific action name (used when no verb fits well).

Examples:

## Canonical Category Examples:
(#1283 AC-4, Arch-ratified 2026-07-08: action names in these examples teach the
CLASSIFIER's emission vocabulary — action-routed ones MUST be ACTION_REGISTRY
canonicals; test_routing_vocabulary_1283.py lints this. Category-routed teaching
names are allowlisted there. Don't add examples with invented action names.)
- "what's on my calendar today?" → {{"category": "temporal", "action": "meeting_time", "confidence": 0.95}}
- "when is my next meeting?" → {{"category": "temporal", "action": "meeting_time", "confidence": 0.9}}
- "what am I working on?" → {{"category": "status", "action": "get_project_status", "confidence": 0.95}}
- "show my standup" → {{"category": "status", "action": "show_standup", "confidence": 0.9}}
- "what should I focus on today?" → {{"category": "priority", "action": "get_top_priority", "confidence": 0.95}}
- "what are my top priorities?" → {{"category": "priority", "action": "get_top_priority", "confidence": 0.9}}
- "who am I?" → {{"category": "identity", "action": "get_identity", "confidence": 0.95}}
- "what's my role?" → {{"category": "identity", "action": "get_role", "confidence": 0.9}}
- "how do I create a ticket?" → {{"category": "guidance", "action": "provide_guidance", "confidence": 0.9}}

## Workflow Category Examples:
- "create a ticket for the login bug" → {{"category": "execution", "action": "create_ticket", "confidence": 0.9}}
- "analyze the file I uploaded" → {{"category": "analysis", "action": "analyze_data", "confidence": 0.8}}
- "summarize the document" → {{"category": "synthesis", "action": "generate_summary", "confidence": 0.85}}
- "list all projects" → {{"category": "query", "action": "manage_portfolio", "confidence": 0.95}}
- "show me stale pull requests" → {{"category": "query", "action": "stale_prs_query", "confidence": 0.9}}
- "hi there" → {{"category": "conversation", "action": "greeting", "confidence": 0.9}}
- "fix it" → {{"category": "conversation", "action": "clarification_needed", "confidence": 0.7}}

## Disambiguation Examples:
- "what time is it in Tokyo?" → {{"category": "query", "action": "get_time_info", "confidence": 0.9}} (general fact)
- "what's the history of calendars?" → {{"category": "query", "action": "get_information", "confidence": 0.9}} (general knowledge)
- "how do status reports work?" → {{"category": "guidance", "action": "provide_guidance", "confidence": 0.8}} (how-to advice)
- "what is the status of the economy?" → {{"category": "query", "action": "get_information", "confidence": 0.9}} (general information)

IMPORTANT: Return ONLY valid JSON. No additional text.
"""

ENTITY_EXTRACTION_PROMPT = """Extract specific entities from this product management request:

Message: {message}

Identify:
- Product names
- Feature names
- Stakeholder names/roles
- Any metrics or KPIs mentioned
- Time frames or deadlines

Respond in JSON format."""
