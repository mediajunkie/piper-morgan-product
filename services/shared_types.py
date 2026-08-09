"""
Shared Types
Common enums and types used across services
"""

from enum import Enum, IntEnum


class IntentCategory(Enum):
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    STRATEGY = "strategy"
    PLANNING = "planning"  # For planning and design activities
    REVIEW = "review"  # For review and validation activities
    LEARNING = "learning"
    QUERY = "query"  # CQRS-lite: For read-only data retrieval operations
    CONVERSATION = "conversation"  # For greetings, chitchat, social interaction
    IDENTITY = "identity"  # For identity queries - "What's your name and role?"
    DISCOVERY = "discovery"  # For capability queries - "What can you do?" (#488)
    TEMPORAL = "temporal"  # For temporal queries - "What day is it?"
    STATUS = "status"  # For status queries - "What am I working on?"
    PRIORITY = "priority"  # For priority queries - "What's my top priority?"
    GUIDANCE = "guidance"  # For guidance queries - "What should I focus on?"
    TRUST = "trust"  # For trust queries - "Why can't you...?" "How well do you know me?" (#673)
    MEMORY = "memory"  # For memory queries - "What do you remember about me?" (#674)
    PORTFOLIO = "portfolio"  # For portfolio queries - "Archive/delete/restore project X" (#675)
    PROVENANCE = "provenance"  # For "why did you suggest that?" citation queries (#1030 R4)
    UNKNOWN = "unknown"  # For unclear or ambiguous requests


class WorkflowType(Enum):
    CREATE_FEATURE = "create_feature"
    ANALYZE_METRICS = "analyze_metrics"
    CREATE_TICKET = "create_ticket"
    CREATE_TASK = "create_task"
    REVIEW_ITEM = "review_item"
    GENERATE_REPORT = "generate_report"
    PLAN_STRATEGY = "plan_strategy"
    LEARN_PATTERN = "learn_pattern"
    ANALYZE_FEEDBACK = "analyze_feedback"
    # PM-009: Project management workflow types
    CONFIRM_PROJECT = "confirm_project"
    SELECT_PROJECT = "select_project"
    ANALYZE_FILE = "analyze_file"  # Add this line for file analysis workflows
    # PM-021: Project listing workflow type
    LIST_PROJECTS = "list_projects"
    # Multi-Agent coordination workflow type
    MULTI_AGENT = "multi_agent"


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    # Analysis tasks
    ANALYZE_REQUEST = "analyze_request"
    EXTRACT_REQUIREMENTS = "extract_requirements"
    IDENTIFY_DEPENDENCIES = "identify_dependencies"

    # Execution tasks
    CREATE_WORK_ITEM = "create_work_item"
    UPDATE_WORK_ITEM = "update_work_item"
    NOTIFY_STAKEHOLDERS = "notify_stakeholders"

    # Synthesis tasks
    GENERATE_DOCUMENT = "generate_document"
    CREATE_SUMMARY = "create_summary"

    # Integration tasks
    GITHUB_CREATE_ISSUE = "github_create_issue"
    GENERATE_GITHUB_ISSUE_CONTENT = "generate_github_issue_content"
    ANALYZE_GITHUB_ISSUE = "analyze_github_issue"
    ANALYZE_FILE = "analyze_file"
    SUMMARIZE = "summarize"

    # PM-021: Project listing task type
    LIST_PROJECTS = "list_projects"
    EXTRACT_WORK_ITEM = "extract_work_item"
    JIRA_CREATE_TICKET = "jira_create_ticket"
    SLACK_SEND_MESSAGE = "slack_send_message"

    # Feedback tasks
    PROCESS_USER_FEEDBACK = "process_user_feedback"

    # Document processing tasks (Issue #290)
    ANALYZE_DOCUMENT = "analyze_document"
    QUESTION_ANSWER_DOCUMENT = "qa_document"
    COMPARE_DOCUMENTS = "compare_documents"
    SUMMARIZE_DOCUMENT = "summarize_document"
    SEARCH_DOCUMENTS = "search_documents"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# PM-009: Integration type enum for project integrations
class IntegrationType(Enum):
    GITHUB = "github"
    JIRA = "jira"
    LINEAR = "linear"
    SLACK = "slack"


# PM-081: Todo management system enums
class TodoStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TodoPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ListType(Enum):
    PERSONAL = "personal"
    PROJECT = "project"
    TEAM = "team"
    TEMPLATE = "template"
    ARCHIVE = "archive"


class OrderingStrategy(Enum):
    MANUAL = "manual"  # User-defined order
    PRIORITY = "priority"  # Sort by priority
    DUE_DATE = "due_date"  # Sort by due date
    CREATED_DATE = "created_date"  # Sort by creation date
    ALPHABETICAL = "alphabetical"  # Sort alphabetically
    STATUS = "status"  # Group by status


# PM-040: Knowledge graph node types
# Note: Values must be UPPERCASE to match PostgreSQL nodetype enum
class NodeType(Enum):
    CONCEPT = "CONCEPT"
    DOCUMENT = "DOCUMENT"
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    TECHNOLOGY = "TECHNOLOGY"
    PROCESS = "PROCESS"
    METRIC = "METRIC"
    EVENT = "EVENT"
    RELATIONSHIP = "RELATIONSHIP"
    CUSTOM = "CUSTOM"


# PM-040: Knowledge graph edge types (Issue #278: CORE-KNOW-ENHANCE)
# Note: Values must be UPPERCASE to match PostgreSQL edgetype enum
class EdgeType(Enum):
    """Basic relationship types"""

    REFERENCES = "REFERENCES"
    DEPENDS_ON = "DEPENDS_ON"
    IMPLEMENTS = "IMPLEMENTS"
    MEASURES = "MEASURES"
    INVOLVES = "INVOLVES"
    TRIGGERS = "TRIGGERS"
    ENHANCES = "ENHANCES"
    REPLACES = "REPLACES"
    SUPPORTS = "SUPPORTS"

    """Causal relationship types (Issue #278)"""
    BECAUSE = "BECAUSE"  # X happens BECAUSE of Y
    ENABLES = "ENABLES"  # X ENABLES Y capability
    REQUIRES = "REQUIRES"  # X REQUIRES Y to function
    PREVENTS = "PREVENTS"  # X PREVENTS Y from happening
    LEADS_TO = "LEADS_TO"  # X LEADS_TO Y outcome

    """Temporal relationship types (Issue #278)"""
    BEFORE = "BEFORE"  # X occurs BEFORE Y
    DURING = "DURING"  # X occurs DURING Y
    AFTER = "AFTER"  # X occurs AFTER Y

    """Other relationship types"""
    CUSTOM = "CUSTOM"


class PatternType(Enum):
    """
    Types of patterns that can be learned by the auto-learning system.

    Issue #300: CORE-ALPHA-LEARNING-BASIC - Basic Auto-Learning
    """

    USER_WORKFLOW = "user_workflow"  # Recurring user action sequences
    COMMAND_SEQUENCE = "command_sequence"  # Frequently used command patterns
    TIME_BASED = "time_based"  # Temporal patterns (e.g., daily standup)
    CONTEXT_BASED = "context_based"  # Context-triggered patterns
    PREFERENCE = "preference"  # User preference patterns
    INTEGRATION = "integration"  # Integration usage patterns


class StandupConversationState(Enum):
    """
    State machine for interactive standup conversations.

    Issue #552: STANDUP-CONV-STATE - Conversation State Management
    Epic #242: CONV-MCP-STANDUP-INTERACTIVE

    Issue #900 Phase 1: Added GATHERING_YESTERDAY / GATHERING_TODAY /
    GATHERING_BLOCKERS for the 3-part structural collection flow.
    Legacy GATHERING_PREFERENCES is preserved for the preference-gathering
    discovery flow (still reachable from INITIATED for callers that want it).
    """

    INITIATED = "initiated"  # User requested standup
    GATHERING_PREFERENCES = (
        "gathering_preferences"  # Asking refinement questions (legacy preference path)
    )
    GATHERING_YESTERDAY = "gathering_yesterday"  # #900: Capturing yesterday's accomplishments
    GATHERING_TODAY = "gathering_today"  # #900: Capturing today's plan
    GATHERING_BLOCKERS = "gathering_blockers"  # #900: Capturing blockers
    GENERATING = "generating"  # Generating standup content
    REFINING = "refining"  # User providing feedback/edits
    FINALIZING = "finalizing"  # Confirming final version
    COMPLETE = "complete"  # Standup delivered
    ABANDONED = "abandoned"  # User cancelled or timed out
    SUSPENDED = "suspended"  # Issue #888: User escaped, state preserved for resumption


class PortfolioOnboardingState(Enum):
    """
    State machine for portfolio onboarding conversations.

    Issue #490: FTUX-PORTFOLIO - Project Portfolio Onboarding
    Epic: FTUX (First Time User Experience)

    Simpler than standup - focused on project capture.
    """

    OFFERED = "offered"  # Issue #888: Piper offered onboarding, awaiting yes/no
    INITIATED = "initiated"  # User accepted offer, onboarding in progress
    GATHERING_PROJECTS = "gathering_projects"  # Collecting project info
    CONFIRMING = "confirming"  # Confirming captured info before save
    GATHERING_REPOS = "gathering_repos"  # Optionally linking repos to projects (#863)
    COMPLETE = "complete"  # Projects saved, onboarding done
    DECLINED = "declined"  # User said no thanks
    SUSPENDED = "suspended"  # Issue #888: User escaped, state preserved for resumption


class InteractionSpace(str, Enum):
    """
    Where the interaction is happening - the Place in MUX grammar.

    Issue #619: GRAMMAR-TRANSFORM: Intent Classification
    Pattern: Pattern-051 (Parallel Place Gathering)

    Different Places call for different communication styles:
    - Slack DM: casual, personal
    - Slack channel: professional, concise (others watching)
    - Web chat: warm, full explanations
    - CLI: terse, no fluff
    """

    SLACK_DM = "slack_dm"
    SLACK_CHANNEL = "slack_channel"
    WEB_CHAT = "web_chat"
    CLI = "cli"
    API = "api"
    UNKNOWN = "unknown"


class PlaceType(str, Enum):
    """
    Type of external source Piper can observe - where Piper looks for FEDERATED data.

    Issue #684: MUX-NAV-PLACES
    ADR-045: Object Model (FEDERATED category - "Piper's Senses")

    Distinct from InteractionSpace which is where user ↔ Piper conversation happens.
    PlaceType is where Piper "looks into" to gather observations about external reality.

    Each type has distinct atmosphere affecting how Piper presents what it sees:
    - IssueTracking: collaborative, status-oriented (GitHub, JIRA)
    - Communication: informal, conversational (Slack messages, email)
    - Temporal: time-bounded, scheduled (Calendar, meetings)
    - Documentation: reference, authoritative (Notion, Confluence)
    """

    ISSUE_TRACKING = "issue_tracking"
    COMMUNICATION = "communication"
    TEMPORAL = "temporal"
    DOCUMENTATION = "documentation"


class PlaceConfidence(str, Enum):
    """
    How confident Piper is about information from a Place.

    Issue #684: MUX-NAV-PLACES
    Pattern: Confidence-based display modes

    Affects how Place data is presented to users:
    - HIGH: Show summary inline ("I see 3 PRs waiting")
    - MEDIUM: Offer to expand ("I noticed some activity - want details?")
    - LOW: Suggest visiting source ("You might want to check GitHub directly")

    Confidence degrades with:
    - Cache age (stale data)
    - Incomplete API access
    - Rate limiting
    - Connection issues
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PerceptionMode(str, Enum):
    """
    How Piper perceives the intent - temporal framing.

    Issue #619: GRAMMAR-TRANSFORM: Intent Classification
    Pattern: Pattern-052 (Personality Bridge)

    This represents Piper's experiential framing of understanding:
    - NOTICING: Present awareness ("I notice you want...")
    - REMEMBERING: Past pattern ("I remember you often ask...")
    - ANTICIPATING: Future suggestion ("You might also want...")
    """

    NOTICING = "noticing"
    REMEMBERING = "remembering"
    ANTICIPATING = "anticipating"


class EffectClass(IntEnum):
    """
    What a workflow's operation does IN THE WORLD — an ordered effect enum.

    Arch ruling 2026-08-09 (building on PDR-006 condition 2, decisions.log
    2026-08-04): the read/write boundary is DECLARED, not inferred. Effect is
    not computable from an entry point, signature, or description — it's a
    fact about what the operation does in the world (PA's evidence:
    `prioritization` sounds like a bulk-write and writes nothing). Declare
    the non-computable fact once at the source (WorkflowEntry.effect,
    required + defaultless); derive everything else from it.

    ORDERED, and the ordering is contract: READ < WRITE < DESTRUCTIVE, with
    destructive a subset of write (you cannot destroy without writing). Four
    consumers each derive their own predicate from the one declared value —
    a boolean `mutates` would force the destructive consumers to re-derive
    destructiveness, recreating the inference problem one level down:

        readOnlyHint    = (effect == READ)         # MCP annotations, PDR-006 §30
        destructiveHint = (effect == DESTRUCTIVE)  # MCP annotations
        needs_consent   = (effect >= WRITE)        # #1509 consent gate
        needs_confirm   = (effect == DESTRUCTIVE)  # #1190 destructive-mutation gate

    EXTENSION POINT — tier vocabulary is deliberately NOT settled here: Arch
    ruled the properties (ordered enum, required, defaultless, derivable) but
    explicitly did not rule the tier names alone. Exec's reversibility framing
    may later split DESTRUCTIVE by recoverability (e.g. RECOVERABLE vs
    IRREVERSIBLE); settle any new tier vocabulary with the consumers (#1190
    gate, PA's MCP annotation spec) before adding values. New tiers must
    preserve the ordering contract above.
    """

    READ = 1  # Observes the world; changes nothing durable outside the conversation
    WRITE = 2  # Creates or modifies durable state (GitHub, Notion, DB) recoverably
    DESTRUCTIVE = 3  # A write whose effect destroys state (subset of write)


class TrustStage(IntEnum):
    """
    Trust stages governing Piper's proactivity level.

    Issue #647: TRUST-LEVELS-1 - Core Infrastructure
    ADR-053: Trust Computation Architecture
    PDR-002: Conversational Glue

    Users progress through these stages based on interaction history.
    Trust is invisible to users but effects are noticeable through behavior.

    CALIBRATION: Thresholds (10, 50) are starting points for alpha testing.
    """

    NEW = 1  # Respond to queries; no unsolicited help
    BUILDING = 2  # Offer related capabilities after task completion
    ESTABLISHED = 3  # Proactive suggestions based on observed context
    TRUSTED = 4  # Anticipate needs; "I'll do X unless you stop me"


class DelegationType(IntEnum):
    """
    Types of system-initiated delegation.

    Issue #414: MUX-INTERACT-DELEGATION
    UX Research: System-initiated delegation increases perceived self-threat.

    Ordered by proactivity level (least to most proactive).
    Higher values = more autonomous behavior.
    """

    OBSERVE = 1  # "I notice..." - passive observation
    INFORM = 2  # "You should know..." - proactive information
    OFFER = 3  # "Would you like me to...?" - explicit offer
    SUGGEST = 4  # "I think we should..." - recommendation
    CONFIRM = 5  # "I'll do X unless you say no" - opt-out action
    AUTO = 6  # Silent execution with brief confirmation


class RiskLevel(IntEnum):
    """
    Risk classification for actions.

    Issue #414: MUX-INTERACT-DELEGATION
    Used with TrustStage to determine appropriate DelegationType.

    Higher risk = more restrictive delegation allowed.
    """

    LOW = 1  # Read-only queries, notifications, reminders
    MEDIUM = 2  # Draft creation, internal state changes
    HIGH = 3  # Send messages, delete/modify data, external actions


class HardnessLevel(IntEnum):
    """
    Object hardness in the home state experience.

    Issue #419: MUX-NAV-HOME - Home State Design
    ADR-045: Object Model
    ownership-metaphors.md: NATIVE/FEDERATED/SYNTHETIC epistemology

    Hardness represents how persistent and user-controlled an object is.
    Objects can move UP the hardness spectrum through user interaction
    (a soft observation can "harden" into a persistent project).

    Hardness correlates with but is distinct from OwnershipCategory:
    - NATIVE objects tend to be harder (user's core data)
    - FEDERATED objects tend to be softer (observed from places)
    - SYNTHETIC objects can vary (Piper's conclusions can harden)

    Trust stage affects which hardness levels are shown:
    - Stage 1 (NEW): Only hardest objects (user-initiated)
    - Stage 2 (BUILDING): + Soft hints about capabilities
    - Stage 3 (ESTABLISHED): + Soft observations ("I noticed...")
    - Stage 4 (TRUSTED): All levels including anticipatory (softest)
    """

    HARDEST = 5  # Lenses - part of the furniture, always reachable
    HARD = 4  # Persistent user-anchored: Projects, Lists, Products
    MEDIUM = 3  # Objects gaining persistence through interaction
    SOFT = 2  # Piper's contextual offerings: "I noticed 3 PRs waiting"
    SOFTEST = 1  # Ephemeral affordances: this-moment-only offers


class ConversationalLens(str, Enum):
    """
    Tracks what aspect of the user's world the conversation is focused on.

    Issue #763: GLUE-FOLLOWUP — Follow-up recognition with lens inheritance
    ADR-049: Conversational State and Hierarchical Intent Architecture

    Lens persists across follow-up turns until explicitly changed,
    enabling natural follow-ups like "What about Thursday?" to inherit
    the calendar context from a previous turn.
    """

    CALENDAR = "calendar"  # Schedule, meetings, availability
    ISSUES = "issues"  # Tasks, bugs, work items
    PROJECTS = "projects"  # Project status, progress
    PEOPLE = "people"  # Team, contacts, availability
    GENERAL = "general"  # No specific lens / general conversation


class ConversationLifecycleState(str, Enum):
    """
    Lifecycle states for conversation entities.

    Issue #715: MUX-HOME-CONVERSATIONS-LIFECYCLE
    Spec #858: Conversation Lifecycle Specification v1.1

    Maps to entity lifecycle model subset:
      ACTIVE → RATIFIED, ARCHIVED → ARCHIVED, COMPOSTED → COMPOSTED
    User-visible states are simpler (Active, Archived, Gone) —
    internal states inform Piper's behavior, not UI labels.
    """

    ACTIVE = "active"  # Current, accessible — user engaged or recently was
    ARCHIVED = "archived"  # Preserved for reference, searchable, not in active use
    COMPOSTED = "composted"  # Content distilled into learning, not user-visible
    DELETED = "deleted"  # Soft-deleted by user action


class SlotFillingState(str, Enum):
    """
    State machine for slot-filling conversations.

    Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
    ADR-049: Conversational State and Hierarchical Intent Architecture

    Manages multi-turn slot collection with skip-filled logic
    and grouped prompting to avoid interrogation patterns.
    """

    EXTRACTING = "extracting"  # Initial extraction from user message
    PROMPTING = "prompting"  # Asking for missing required slots
    CONFIRMING = "confirming"  # All required slots filled, confirming
    COMPLETE = "complete"  # User confirmed, process done
    CANCELLED = "cancelled"  # User cancelled mid-flow
