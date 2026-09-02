import re
import string
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from services.domain.models import Intent
from services.shared_types import IntentCategory


@dataclass
class MultiIntentResult:
    """
    Result of multi-intent detection (Issue #595).

    Contains all detected intents from a single message, enabling
    "handle all" strategy for messages like "Hi Piper! What's on my agenda?"

    This detection logic is designed to be reusable for #427
    (Unified Conversation Model) where more sophisticated strategy
    selection (handle all, chain, or clarify) will be implemented.
    """

    intents: List[Intent] = field(default_factory=list)
    original_message: str = ""  # stored for logging/debug, not consumed downstream (audit #827)
    is_multi_intent: bool = False
    # Pre-claim shadow probe (2026-09-02): the name of the *PATTERNS list that
    # produced each intent, ALIGNED with ``intents`` (post-subsumption).
    # Measurement-only telemetry — nothing routes on it; default [] keeps every
    # existing constructor call byte-identical.
    pattern_lists: List[str] = field(default_factory=list)

    @property
    def primary_intent(self) -> Optional[Intent]:
        """Get the primary (most important) intent.

        Priority order for determining primary intent:
        1. Non-conversational intents (QUERY, EXECUTION, etc.) take precedence
        2. Among conversational intents, return the first one
        """
        if not self.intents:
            return None

        # Find first non-conversational intent
        for intent in self.intents:
            if intent.category != IntentCategory.CONVERSATION:
                return intent

        # Fall back to first intent if all are conversational
        return self.intents[0]

    @property
    def secondary_intents(self) -> List[Intent]:
        """Get all intents except the primary one."""
        primary = self.primary_intent
        if not primary:
            return []
        return [i for i in self.intents if i.id != primary.id]

    @property
    def has_greeting(self) -> bool:
        """Check if any intent is a greeting."""
        return any(
            i.category == IntentCategory.CONVERSATION and i.action == "greeting"
            for i in self.intents
        )

    @property
    def has_substantive_intent(self) -> bool:
        """Check if there's a non-conversational intent."""
        return any(i.category != IntentCategory.CONVERSATION for i in self.intents)


class PreClassifier:
    """Rule-based pre-classification for common patterns"""

    # Greeting patterns - using regex with word boundaries for precision
    GREETING_PATTERNS = [
        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",
        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b",
        r"\bgreetings\b",
        r"\bhowdy\b",
        r"\bhi there\b",
    ]

    # Farewell patterns - using regex with word boundaries for precision
    FAREWELL_PATTERNS = [
        r"\bbye\b",
        r"\bgoodbye\b",
        r"\bsee you\b",
        r"\blater\b",
        r"\bfarewell\b",
    ]

    # #1416: filler that may accompany a pure pleasantry without making the
    # message substantive ("hi there!", "hey, how are you?"). Used by
    # _is_pleasantry_only to decide whether the greeting/farewell/thanks
    # short-circuits may claim the message at all.
    _PLEASANTRY_FILLER_PATTERNS = [
        r"\bhow\s+are\s+you(\s+doing)?\b",
        r"\bhow'?s\s+it\s+going\b",
        r"\bwhat'?s\s+up\b",
        r"\bnice\s+to\s+meet\s+you\b",
        r"\bgood\s+(morning|afternoon|evening|night|day)\b",
        r"\bthanks?\s+(so\s+much|a\s+lot|again)\b",
        r"\bthank\s+you(\s+(so\s+much|again))?\b",
        # standalone intensifiers left behind once the pleasantry itself is
        # stripped ("thank you | so much", "thanks | a lot")
        r"\b(so|very)\s+much\b",
        r"\ba\s+lot\b",
        r"\b(there|everyone|all|piper|team|again|folks)\b",
    ]

    @staticmethod
    def _is_pleasantry_only(clean_for_matching: str) -> bool:
        """#1416: True iff the message is ONLY a greeting/farewell/thanks
        pleasantry (plus filler) — the precondition for the canned
        short-circuits below.

        The bug (PM, Scenario A turn 1): "Hi, I just got access to this and am
        excited to try it. How do I address you?" matched ``\\bhi\\b`` and the
        greeting short-circuit swallowed the actual question. Same conservative
        over-resolution discipline as B3-N2/#1417: a deterministic fast-path
        may only claim what it fully understands; anything with substantive
        residue falls through to full classification (where the floor greets
        AND answers).
        """
        residue = clean_for_matching
        for pattern_set in (
            PreClassifier.GREETING_PATTERNS,
            PreClassifier.FAREWELL_PATTERNS,
            PreClassifier.THANKS_PATTERNS,
            PreClassifier._PLEASANTRY_FILLER_PATTERNS,
        ):
            for pattern in pattern_set:
                residue = re.sub(pattern, " ", residue, flags=re.IGNORECASE)
        # Strip punctuation/whitespace; whatever words remain are substance.
        residue_words = re.findall(r"[a-z0-9']+", residue, flags=re.IGNORECASE)
        return len(residue_words) == 0

    # Thanks patterns - using regex with word boundaries for precision
    THANKS_PATTERNS = [
        r"\bthanks\b",
        r"\bthank you\b",
        r"\bthx\b",
        r"\bty\b",
        r"\bmuch appreciated\b",
    ]

    # Issue #488: DISCOVERY patterns for capability queries - "What can you do?"
    # These return dynamic capabilities from PluginRegistry
    # Must be checked BEFORE IDENTITY_PATTERNS to ensure proper routing
    DISCOVERY_PATTERNS = [
        r"\bwhat are your capabilities\b",
        r"\bwhat services\b",
        r"\bwhat do you offer\b",
        r"\bwhat features\b",
        r"\bwhat can you help\b",
        r"\bshow me your capabilities\b",
        r"\bwhat can you do\b",
        r"\bmenu of services\b",
        r"\blist.*capabilities\b",
        r"\byour capabilities\b",
        r"\bcapability menu\b",
        r"\bcapabilities menu\b",
        r"\bshow.*menu\b",
        # Additional discovery patterns
        r"\bwhat.*able to do\b",
        r"\bshow.*features\b",
        r"\bavailable.*features\b",
        # Issue #814: Removed r"\bhelp me get started\b" — routes to GUIDANCE (setup) not DISCOVERY
        # Issue #671: Bare "help" should show capabilities
        r"^help$",  # Exact match for bare "help"
        r"\bhelp\s*menu\b",
        r"\bshow\s*help\b",
        r"\bneed\s*help\b",
    ]

    # Canonical query patterns for identity - "Who are you?"
    # These return static identity information
    IDENTITY_PATTERNS = [
        r"\bwhat'?s your name\b",
        r"\bwho are you\b",
        r"\byour role\b",
        r"\bwhat do you do\b",
        r"\btell me about yourself\b",
        r"\bintroduce yourself\b",
    ]

    TEMPORAL_PATTERNS = [
        # Time queries
        r"\bwhat time is it\b",
        r"\bwhat'?s the time\b",
        r"\bcurrent time\b",
        r"\btime now\b",
        r"\btell me the time\b",
        # Date queries
        r"\bwhat day is it\b",
        r"\bwhat'?s the date\b",
        r"\bcurrent date\b",
        r"\btoday'?s date\b",
        r"\bwhat'?s today\b",
        r"\bdate and time\b",
        r"\bday of the week\b",
        r"\btell me the date\b",
        r"\bwhat date is it\b",
        r"\btoday'?s day\b",
        # Calendar/schedule queries
        r"\bmy calendar\b",
        r"\bshow.{0,10}calendar\b",
        r"\bmy schedule\b",
        r"\bshow.{0,10}schedule\b",
        r"\bcalendar.*today\b",
        r"\bschedule.*today\b",
        r"\bwhat'?s on my calendar\b",
        r"\bwhat'?s on my schedule\b",
        r"\bmy appointments\b",
        r"\bshow.{0,10}appointments\b",
        # Meeting queries
        r"\bmy meetings\b",
        r"\bnext meeting\b",
        r"\bupcoming meetings\b",
        r"\bwhen is my.{0,10}meeting\b",
        r"\bwhen am i.{0,10}meeting\b",
        r"\bmeeting.*today\b",
        r"\bmeeting.*tomorrow\b",
        r"\bmeetings this week\b",
        # Event queries
        r"\bmy events\b",
        r"\bshow.{0,10}events\b",
        r"\bupcoming events\b",
        r"\bevents.*today\b",
        r"\bevents.*tomorrow\b",
        r"\bnext event\b",
        # Relative time
        # Note: "agenda" patterns moved to CALENDAR_QUERY_PATTERNS (Issue #588)
        r"\bwork on today\b",
        r"\bwhat.*yesterday\b",
        r"\bdid.*yesterday\b",
        r"\bhappened yesterday\b",
        r"\blast time.*worked\b",
        r"\bhow long.*working\b",
        r"\bhow long.*been working\b",
        r"\bwhat'?s.{0,10}tomorrow\b",
        r"\btomorrow'?s schedule\b",
        r"\bthis week'?s\b",
        r"\bnext week'?s\b",
        r"\bthis month'?s\b",
        # Availability queries
        r"\bwhen am i free\b",
        r"\bwhen'?s my next.{0,10}free\b",
        r"\bavailable time\b",
        r"\bfree time\b",
        r"\bopen slots\b",
    ]

    # Issue #1117 INTENT-TEMPORAL-OVERGREEDY: completion-history queries
    # ("when did I complete X") are history-lookup intents, NOT current-time
    # intents. Without these patterns they fall through to the LLM classifier,
    # which misroutes 4/5 phrasings to temporal/provide_current_time_with_calendar
    # (returns today's date + a calendar-setup prompt). These patterns catch the
    # history-lookup shape deterministically and route to STATUS, which is
    # floor-routed (since #925) and answers completion-history honestly
    # (the "Did I ever complete X" variant already reaches the floor this way).
    #
    # Phase-4-alignment instance of #1016 LLM-touch-boundary principle
    # (temporal-vs-history classifier surface), implemented as a deterministic
    # pre-classifier dispatch per Architect disposition (Option C, 2026-05-28).
    # Must be checked BEFORE TEMPORAL in the pattern_groups table.
    COMPLETION_HISTORY_PATTERNS = [
        # "when did I/we complete/finish/ship/deliver/launch/close X"
        r"\bwhen did (i|we) (complete|finish|ship|deliver|launch|close|wrap up|finalize)\b",
        # "what date did I/we finish/complete/ship X"
        r"\bwhat date did (i|we) (complete|finish|ship|deliver|launch|close)\b",
        # "show me when I/we shipped/completed/finished X"
        r"\bshow me when (i|we) (completed|finished|shipped|delivered|launched|closed)\b",
        # "when was X completed/finished/shipped/delivered/launched" (passive)
        r"\bwhen was .{1,40}(completed|finished|shipped|delivered|launched)\b",
        # "how long ago did I/we complete/finish/ship X"
        r"\bhow long ago did (i|we) (complete|finish|ship|deliver|launch)\b",
    ]

    STATUS_PATTERNS = [
        # Work status queries
        r"\bwhat am i working on\b",
        r"\bwhat'?s my current project\b",
        r"\bmy projects\b",
        r"\bcurrent work\b",
        # Removed: r"\bwhat'?s on my plate\b" - false positive with temporal ("what's on my plate today")
        r"\bmy portfolio\b",
        r"\bshow.*projects\b",
        r"\bcurrent projects\b",
        r"\bproject overview\b",
        r"\bproject landscape\b",
        r"\blist.*projects\b",
        r"\bprojects.*working on\b",
        r"\bwhat.*working on\b",
        r"\bworking on now\b",
        r"\bmy current work\b",
        r"\bactive projects\b",
        r"\bactive work\b",
        # Status update queries
        r"\bwhat'?s my status\b",
        r"\bproject status\b",
        r"\bstatus update\b",
        r"\bmy status\b",
        r"\bwork status\b",
        r"\bshow.*status\b",
        r"\bcurrent status\b",
        r"\bstatus report\b",
        # Standup queries (with context to avoid false positives)
        # Removed: r"\bstandup\b" - false positive with temporal ("what time is standup")
        r"\bstand-up\b",
        r"\bstand up\b",
        r"\bmy standup\b",
        r"\bstandup update\b",
        r"\bstandup report\b",
        r"\bdaily standup\b",
        r"\bshow.*standup\b",
        # Progress queries
        r"\bmy progress\b",
        r"\bprogress update\b",
        r"\bprogress report\b",
        r"\bprogress on\b",
        r"\bshow.*progress\b",
        r"\bcurrent progress\b",
        r"\bhow'?s.*progress\b",
        r"\bwhat'?s.*progress\b",
        # Task queries
        r"\bmy tasks\b",
        r"\bcurrent tasks\b",
        r"\bactive tasks\b",
        r"\bshow.*tasks\b",
        r"\blist.*tasks\b",
        r"\btasks.*working\b",
        r"\bwhat tasks\b",
        r"\btask status\b",
        # Assignment queries
        r"\bmy assignments\b",
        r"\bcurrent assignments\b",
        r"\bwhat'?s assigned\b",
        r"\bshow.*assignments\b",
        # Issue #898 Q25: Milestone queries are project status, not priority
        r"\bnext milestone\b",
        r"\bwhat'?s the (?:next|upcoming) milestone\b",
        r"\bmilestone status\b",
        r"\bmilestone progress\b",
        r"\bupcoming milestones?\b",
    ]

    # Issue #521: Contextual Intelligence query patterns
    # MUST be checked BEFORE PRIORITY to avoid pattern collision
    # Issue #901: Feature/integration info queries - Query #27
    # "Tell me more about the GitHub integration" should be QUERY, not IDENTITY
    # These MUST be checked before IDENTITY to prevent "about" keyword collision
    FEATURE_INFO_PATTERNS = [
        r"\btell me (?:more )?about the\s+\w+\s+(?:integration|feature|plugin|tool|capability)\b",
        r"\btell me (?:more )?about\s+(?:github|slack|notion|calendar|mcp)\b",
        r"\bhow does the\s+\w+\s+(?:integration|feature|plugin|tool)\s+work\b",
        r"\bwhat is the\s+\w+\s+(?:integration|feature|plugin)\b",
        r"\blearn (?:more )?about the\s+\w+\s+(?:integration|feature)\b",
        r"\binformation about the\s+\w+\s+(?:integration|feature)\b",
    ]

    CONTEXTUAL_QUERY_PATTERNS = [
        # Changes query - Query #29
        r"\bwhat changed since\b",
        r"\bwhat'?s changed since\b",
        r"\bshow.*changes since\b",
        r"\bshow me.*changed\b",
        r"\bchanges since\b",
        r"\bactivity since\b",
        r"\bupdates since\b",
        # Attention query - Query #30
        r"\bwhat needs my attention\b",
        r"\bwhat needs attention\b",
        r"\bneeds my attention\b",
        r"\bshow.*needs.*attention\b",
        r"\bitems.*need.*attention\b",
        r"\battention items\b",
    ]

    # Issue #523: Phase A Canonical Query patterns
    # Issue #589: Added today's calendar/meeting patterns to route to QUERY instead of TEMPORAL
    # Calendar queries - Queries #34, #35, #61
    CALENDAR_QUERY_PATTERNS = [
        # Issue #589: Today's calendar queries - should route to meeting_time (QUERY)
        # These MUST be checked before TEMPORAL_PATTERNS to prevent misrouting
        r"\bwhat'?s on my calendar\b",
        r"\bwhat is on my calendar\b",
        r"\bmy calendar today\b",
        r"\bcalendar today\b",
        r"\bmeetings today\b",
        r"\bdo i have any meetings\b",
        r"\bdo i have meetings\b",
        r"\bwhat meetings do i have\b",
        r"\bwhat meetings\b",
        r"\bmy schedule today\b",
        r"\btoday'?s schedule\b",
        r"\bschedule for today\b",
        # Issue #588: Agenda patterns (calendar queries, not temporal status)
        r"\bagenda.*today\b",
        r"\bagenda.*tomorrow\b",
        r"\bagenda.*this week\b",
        r"\bagenda.*next week\b",
        r"\bmy agenda\b",
        r"\bon my agenda\b",
        # Issue #588: Tomorrow calendar queries
        r"\bcalendar.*tomorrow\b",
        r"\btomorrow'?s calendar\b",
        r"\bmeetings.*tomorrow\b",
        r"\bschedule.*tomorrow\b",
        r"\btomorrow'?s schedule\b",
        r"\bwhat'?s on my calendar.*tomorrow\b",
        r"\bmy calendar tomorrow\b",
        r"\bwhat'?s.*tomorrow\b",
        # Issue #588: This week / next week calendar queries
        r"\bcalendar.*this week\b",
        r"\bcalendar.*next week\b",
        r"\bschedule.*this week\b",
        r"\bschedule.*next week\b",
        r"\bmeetings.*this week\b",
        r"\bmeetings.*next week\b",
        # Meeting time query - Query #34
        r"\bhow much time in meetings\b",
        r"\bhow much time.*meetings\b",
        r"\btime spent in meetings\b",
        r"\bmeeting time\b",
        # Recurring meetings query - Query #35
        r"\breview.*recurring meetings\b",
        r"\bshow.*recurring meetings\b",
        r"\baudit.*standing meetings\b",
        r"\brecurring meetings\b",
        # Week calendar query - Query #61
        r"\bwhat'?s my week look like\b",
        r"\bshow.*my week\b",
        r"\bweek ahead\b",
        r"\bweek calendar\b",
        # Issue #901: Calendar conflict/check queries - Query #62
        # "Check my calendar for conflicts" should be QUERY, not TEMPORAL
        r"\bcheck.{0,10}calendar\b",
        r"\bcalendar.*conflict\b",
        r"\bcalendar.*overlap\b",
        r"\bconflict.*calendar\b",
        # Issue #901: Scheduling/availability queries - Query #33
        # "Find time for a 1:1" should be calendar QUERY, not TEMPORAL
        r"\bfind time for\b",
        r"\bfind.{0,10}time.{0,10}(?:meeting|1:1|1 on 1|sync|chat)\b",
        r"\bschedule.{0,10}(?:1:1|1 on 1|meeting|sync|call)\b",
        r"\bbook.{0,10}(?:meeting|time|1:1|slot)\b",
    ]

    # GitHub queries - Queries #41, #42, #45, #59, #60
    GITHUB_QUERY_PATTERNS = [
        # Shipped query - Query #41
        r"\bwhat did we ship\b",
        r"\bwhat shipped\b",
        r"\bshow.*what.*shipped\b",
        r"\bwhat.*shipped.*week\b",
        # Stale PRs query - Query #42
        r"\bshow.*stale prs\b",
        r"\bstale pull requests\b",
        r"\bold prs\b",
        r"\bprs.*needing review\b",
        # Close issue query - Query #45
        r"\bclose issue\s*#?\d+\b",
        r"\bclose.*completed.*issue\b",
        r"\bclose.*issue\b",
        # Reopen issue query - Issue #902
        r"\breopen\s+issue\s*#?\d+\b",
        r"\bre-open\s+issue\s*#?\d+\b",
        r"\breopen\s+.*issue\b",
        r"\bre-open\s+.*issue\b",
        # Comment issue query - Query #59
        r"\bcomment on issue\s*#?\d+\b",
        r"\badd comment to issue\s*#?\d+\b",
        r"\breply to issue\s*#?\d+\b",
        r"\bcomment\s+on\s+#?\d+\b",
        # Review issue query - Query #60
        r"\breview issue\s*#?\d+\b",
        r"\bshow.*issue\s*#?\d+\b",
        r"\bissue\s*#?\d+\s*details\b",
        r"\bget issue\s*#?\d+\b",
        # Issue #845: Issue listing / count queries
        r"\bhow many.*issues\b",
        r"\bopen issues\b",
        r"\bmy issues\b",
        r"\blist.*issues\b",
        r"\bshow.*issues\b",
        r"\bissue count\b",
        r"\bissues.*assigned\b",
        # Issue #851: PR listing queries
        r"\bshow my prs\b",
        r"\bshow my pull requests\b",
        r"\bmy prs\b",
        r"\bmy pull requests\b",
        r"\blist.*prs\b",
        r"\blist.*pull requests\b",
        r"\bopen pull requests\b",
        r"\bopen prs\b",
        r"\bprs assigned to me\b",
        r"\bpull requests assigned to me\b",
        # Issue #1039: Milestone queries (state-filter UX deferred to #1051)
        r"\bshow.*milestones?\b",
        r"\blist.*milestones?\b",
        r"\bnext milestone\b",
        r"\bwhat milestones?\b",
        r"\bmilestones?\s+(?:status|count|list|due)\b",
        r"\bwhen.*milestone\b",
        # Issue #1039: Release queries (prerelease filter UX deferred to #1051)
        r"\brecent releases?\b",
        r"\bshow.*releases?\b",
        r"\blist.*releases?\b",
        r"\bwhat version (?:are we on|is current)\b",
        r"\bcurrent (?:release|version)\b",
        r"\blatest release\b",
        # Issue #1040: Label queries
        r"\bwhat labels?\b",
        r"\bshow.*labels?\b",
        r"\blist.*labels?\b",
        r"\bissue labels?\b",
        r"\blabels?\s+(?:list|count)\b",
        r"\b(?:available|all)\s+labels?\b",
        # Issue #1040: Branch queries (per Q5 'all non-default'). GitHub-remote
        # branches; local-git "what branch are we on?" lives at #1044 patterns
        # below.
        r"\bactive branches?\b",
        r"\bshow.*branches?\b",
        r"\blist.*branches?\b",
        r"\bfeature branches?\b",
        r"\bcurrent branches?\b",
        r"\bwhat branches?\b",
    ]

    # Issue #1044: Local-git status queries — distinct from GitHub-remote
    # branches above. These patterns target the SERVER'S working-tree state
    # (current branch singular, dirty/clean, ahead/behind from upstream).
    LOCAL_GIT_STATUS_PATTERNS = [
        # Canonical "what branch are we on?" + singular variants
        r"\bwhat branch are we on\b",
        r"\bwhat branch am i on\b",
        r"\bwhich branch are we on\b",
        r"\bcurrent branch\b",  # singular (vs LIST_BRANCHES "current branches")
        # Working-tree state
        r"\bworking tree (?:clean|dirty|status)\b",
        r"\buncommitted changes?\b",
        r"\bdirty (?:working )?tree\b",
        # Upstream / sync state
        r"\bahead of (?:main|origin|upstream|master)\b",
        r"\bbehind (?:main|origin|upstream|master)\b",
        r"\bunpushed commits?\b",
        # Generic local-git status
        r"\blocal git status\b",
        r"\bgit status\b",
    ]

    # Productivity query - Query #51
    PRODUCTIVITY_QUERY_PATTERNS = [
        r"\bwhat'?s my productivity\b",
        r"\bshow.*productivity\b",
        r"\bproductivity metrics\b",
        r"\bmy productivity\b",
    ]

    # Session-activity recall (#1394 / ADR-078 B4) — "what did we create this
    # session". Distinct from GITHUB_QUERY's "what did we ship" (a repo-wide live
    # query); this reads the owner-scoped session_activity ledger for THIS session.
    SESSION_ACTIVITY_QUERY_PATTERNS = [
        r"\bwhat did we create\b",
        r"\bwhat have we created\b",
        r"\bwhat did we make\b",
        r"\bwhat did (?:we|i) create this session\b",
        r"\bwhat did we do this session\b",
        r"\bwhat (?:issues|items) did we (?:create|make|open)\b",
    ]

    # Todo queries - Queries #56, #57
    TODO_QUERY_PATTERNS = [
        # List todos query - Query #56
        # "my" is optional — natural variants: "list todos", "show todos"
        r"\bshow\s+(?:my\s+)?todos\b",
        r"\blist\s+(?:my\s+)?todos\b",
        r"\bwhat are my todos\b",
        r"\bmy todos\b",
        r"\bshow.*completed\s+todos\b",
        r"\bshow\s+all\s+(?:my\s+)?todos\b",
        # Next todo query - Query #57
        r"\bwhat'?s my next todo\b",
        r"\bnext todo\b",
        r"\bwhat should i do next\b",
        r"\bwhat.*next.*do\b",
    ]

    # Issue #904: Todo completion patterns - Query #55
    TODO_COMPLETE_PATTERNS = [
        # "mark/complete/finish todo N" or "mark/complete/finish todo #N"
        r"\b(?:mark|complete|finish)\s+todo\s+#?\d+",
        # "complete the X todo" or "finish the X task"
        r"\b(?:mark|complete|finish)\s+(?:the\s+)?.+?\s+(?:todo|task)\b",
        # "mark X as done/complete"
        r"\b(?:mark|complete|finish)\s+(?:the\s+)?.+?\s+(?:as\s+)?(?:done|complete|finished)\b",
        # "done with the X todo/task"
        r"\bdone\s+with\s+(?:the\s+)?.+?\s*(?:todo|task)?\b",
        # "finish todo about X" (todo immediately after finish)
        r"\bfinish\s+todo\b",
        # "mark done"
        r"\bmark\s+done\b",
        # "complete todo about X" (todo immediately after complete)
        r"\bcomplete\s+todo\b",
    ]

    # #1521: Reminder-QUERY patterns — "what reminders do I have?" is a READ of
    # the stored reminders (todo_items.reminder_date, the #1491 fetch path),
    # NOT a temporal/calendar question and NOT a reminder creation. Before
    # this lane existed no surface claimed the shape: pre_classify returned
    # None and the LLM classifier misrouted it to the temporal lane ("Today is
    # Saturday… No meetings – great day for deep work!" — PM live, 2026-08-08).
    # Deliberately narrow (the OBVIOUS query shapes only): every pattern needs
    # a read verb / question form + the plural-or-possessed "reminders" noun,
    # so creation phrasings ("remind me to…", "set a reminder…") are disjoint
    # by construction — and the blockers below re-assert that disjointness
    # (same belt-and-suspenders discipline as INTEGRATION_CONNECT, #1417/#1471).
    REMINDER_QUERY_PATTERNS = [
        # "what reminders do I have?" / "what reminders are set"
        r"\bwhat reminders\b",
        # "what are my reminders" / "check my reminders" / bare "my reminders"
        r"\bmy reminders\b",
        # "show/list/view/see/check [me] [all] [my] reminders"
        r"\b(?:show|list|view|see|check)\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?reminders\b",
        # "do I have [any] reminders?"
        r"\bdo i have (?:any\s+)?reminders\b",
    ]
    # #1521 blockers (mirror of INTEGRATION_CONNECT_BLOCKERS): a creation verb
    # or a destructive verb means a WRITE ask — never the listing lane. The
    # creation shapes keep their #903 create_reminder routing; the destructive
    # shapes fall through (deletion of reminders is not this lane's claim).
    REMINDER_QUERY_BLOCKERS = [
        r"\bremind\s+me\b",
        r"\bset\s+(?:a\s+)?reminders?\b",
        r"\bcreate\s+(?:a\s+)?reminders?\b",
        r"\bdon'?t\s+let\s+me\s+forget\b",
        r"\bneed\s+to\s+remember\b",
        # "get rid of" joined 1527: with the portfolio delete-claims narrowed,
        # "get rid of my reminders" reached this lane and the destructive-verb
        # blocker missed the phrasal form (reminder_clear's own delete-answer
        # detector already reads "get rid" as delete-family).
        r"\b(?:delete|remove|cancel|clear|dismiss)\b|\bget\s+rid\s+of\b",
    ]

    # Issue #903: Reminder patterns - Query #32
    REMINDER_PATTERNS = [
        # "remind me to X" / "remind me about X"
        r"\bremind\s+me\s+(?:to|about)\b",
        # "set a reminder to X" / "set reminder for X"
        r"\bset\s+(?:a\s+)?reminder\b",
        # "reminder to X" / "create a reminder"
        r"\bcreate\s+(?:a\s+)?reminder\b",
        # "don't let me forget to X"
        r"\bdon'?t\s+let\s+me\s+forget\b",
        # "I need to remember to X"
        r"\bneed\s+to\s+remember\s+to\b",
    ]

    # #1256: stakeholder-update composition — checked BEFORE the document
    # patterns, because "write a short update for the CEO on where we are
    # with X" otherwise matches DOCUMENT_QUERY_PATTERNS' loose
    # `update ... with` shape (the pattern greedily bridges "update for the
    # CEO ... where we are WITH") and routes to update_document_query at
    # confidence 1.0 — the handler then asks "which document?" instead of
    # drafting the memo. Deliberately EXCLUDED here: the bare
    # "update [person] on [topic]" shape from the issue — too collision-prone
    # with document/platform phrasings ("update the readme on GitHub");
    # revisit when the stakeholder-update skill (Wave 2) gives this action a
    # real procedure.
    STAKEHOLDER_UPDATE_PATTERNS = [
        # "write a short update for X" / "write an update for the board"
        r"\bwrite\s+(?:me\s+)?(?:a|an)?\s*(?:\w+\s+){0,3}update\s+for\b",
        # "draft a status update for X" / "draft an update for the team"
        r"\bdraft\s+(?:me\s+)?(?:a|an)?\s*(?:\w+\s+){0,3}update\s+for\b",
        # "write something to send to X"
        r"\bwrite\s+something\s+to\s+send\s+to\b",
        # explicit: "stakeholder update"
        r"\bstakeholder\s+update\b",
    ]

    # Issue #522: Document update query patterns - Query #40
    DOCUMENT_QUERY_PATTERNS = [
        # Update document patterns
        r"\bupdate\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bedit\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bmodify\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bchange\s+(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        # Add to document patterns
        r"\badd\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        r"\bappend\s+(?:to\s+)?(?:the\s+)?[\w\s]+\s+doc(?:ument)?\b",
        # Update with content patterns (e.g., "update X with Y", "edit X with Y")
        r"\bupdate\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bedit\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bmodify\s+(?:the\s+)?[\w\s]+\s+with\b",
        r"\bchange\s+(?:the\s+)?[\w\s]+\s+to\b",
    ]

    # Issue #901: Analysis patterns — blockers, risks, impact assessment
    # "What's blocking the milestone?" should be ANALYSIS, not STATUS
    # Issue #898 Q23: Risk/threat awareness queries should be ANALYSIS, not GUIDANCE
    ANALYSIS_PATTERNS = [
        r"\bwhat'?s blocking\b",
        r"\bwhat is blocking\b",
        r"\bwhat.*block(?:s|ing|ed)\s+(?:the|my|our)\b",
        r"\bblockers?\s+(?:for|on|in)\b",
        r"\bwhat.*obstacle\b",
        r"\bwhat'?s in the way\b",
        r"\banalyze.*(?:risk|impact|blocker|bottleneck)\b",
        r"\brisk assessment\b",
        r"\bimpact analysis\b",
        r"\bbottleneck.*(?:analysis|report)\b",
        # Issue #898 Q23: Risk/threat queries
        r"\bwhat risks\b",
        r"\bwhat.*risk(?:s)?\s+(?:should|do|are)\b",
        r"\bidentify.*risks?\b",
        r"\brisk(?:s)?\s+(?:i|we)\s+should\b",
        r"\bthreats?\s+(?:to|should|i)\b",
        r"\bwhat.*threaten\b",
    ]

    PRIORITY_PATTERNS = [
        # Priority queries
        r"\bmy priorities\b",
        r"\bwhat'?s my top priority\b",
        r"\btop priority\b",
        r"\bhighest priority\b",
        r"\bpriority one\b",
        r"\bshow.*priorities\b",
        r"\blist.*priorities\b",
        r"\bwhat are my priorities\b",
        r"\bcurrent priorities\b",
        r"\btop priorities\b",
        r"\bkey priorities\b",
        # Importance queries
        r"\bmost important\b",
        r"\bmost important task\b",
        r"\bmost important work\b",
        r"\bwhat'?s most important\b",
        r"\bwhat matters most\b",
        r"\bkey tasks\b",
        r"\bkey items\b",
        # Focus queries
        r"\bwhat should i focus on\b",
        r"\bshould i focus\b",
        r"\bwhat.*focus on\b",
        r"\bwhere.*focus\b",
        r"\bfocus areas\b",
        r"\bfocus on today\b",
        r"\bfocus this week\b",
        r"\bwhat to focus\b",
        # Urgency queries
        r"\bwhat'?s urgent\b",
        r"\burgent tasks\b",
        r"\burgent items\b",
        r"\burgent work\b",
        r"\bmost urgent\b",
        r"\bneeds.*focus\b",
        r"\brequires attention\b",
        # Critical queries
        r"\bwhat'?s critical\b",
        r"\bcritical tasks\b",
        r"\bcritical items\b",
        r"\bcritical work\b",
        r"\bmost critical\b",
        # Next action queries
        # Issue #898 Q25: "what.*next" was too greedy — matched "next milestone"
        # Narrowed to avoid matching "next [noun]" (milestone, sprint, release)
        r"\bwhat should i do first\b",
        r"\bwhat should i do next\b",
        r"\bwhat.*(?:do|work on|tackle|handle)\s+next\b",
        r"\bwhat(?:'s| is) next\b",
        r"\bwhat.*first\b",
        r"\bwhich project.*focus\b",
        r"\bwhich task.*focus\b",
        r"\bwhat.*work on next\b",
        r"\bwhat to do\b",
    ]

    GUIDANCE_PATTERNS = [
        # GREAT-4A: Removed focus patterns (moved to PRIORITY)
        r"\bwhere should i focus\b",
        # Issue #898: Moved "\bwhat'?s next\b" to PRIORITY_PATTERNS — it's an action query
        r"\bguidance\b",
        r"\brecommendation\b",
        r"\badvice\b",
        r"\bwhat now\b",
        r"\bnext steps\b",
        # GAP-3 Phase 2: Added October 13, 2025 - Edge case patterns for GUIDANCE disambiguation
        r"\bwhat should (i|we) do (about|with)\b",  # Advice-seeking questions
        r"\badvise (me|us) on\b",  # Direct advice requests
        r"\bwhat('?s| is) the process for\b",  # Process/how-to questions
        # Issue #487: Added setup/configuration patterns for alpha onboarding
        r"\bhelp.*setup\b",
        r"\bhelp.*configure\b",
        r"\bsetup.*projects?\b",  # matches "setup project" or "setup projects"
        r"\bconfigure.*projects?\b",  # matches "configure project" or "configure projects"
        r"\bhow do i.*setup\b",
        r"\bhow do i.*configure\b",
        r"\bget started\b",
        r"\bgetting started\b",
        # Issue #487 follow-up: "set up" with space (common user spelling)
        r"\bhelp.*set up\b",
        r"\bset up.*projects?\b",
        r"\bhow do i.*set up\b",
        r"\bset up.*portfolio\b",
    ]

    # #1417 (Arch-ratified 2026-07-16): integration-connect = connect-verb ×
    # integration-noun, routed deterministically to the EXISTING guidance lane
    # (GUIDANCE/get_contextual_guidance -> _format_integration_setup_guidance).
    # Before this, "can we connect my github?" was mode-4 category-luck: the LLM
    # usually emitted EXECUTION + a free-form action -> the generic unwired-write
    # decline — a false "still on the way" while the OAuth flow, settings page,
    # and a purpose-built chat answer all exist. Noun set is one-line-extensible
    # per integration (Arch ruling).
    INTEGRATION_CONNECT_PATTERNS = [
        r"\b(?:connect|set\s?up|link|hook\s+up|integrate|add|enable)\b.{0,40}?"
        r"\b(?P<integration>github|slack|notion|(?:google\s+)?calendar)\b",
    ]
    # Collision guard (Arch ruling (a), the load-bearing one): an owner/name
    # slug or the word repo(sitory) means the repo-link lane (#862 handles it
    # earlier in the pass) — never integration setup. Same conservative
    # over-resolution discipline as B3's N2 guard.
    INTEGRATION_CONNECT_BLOCKERS = [
        r"[\w.-]+/[\w.-]+",
        r"\brepo(?:sitor(?:y|ies))?s?\b",
        # #1471: an event-write noun means a calendar-WRITE ask ("add a
        # meeting to my calendar"), never integration setup. Without this
        # guard, giving connect-verbs precedence over the temporal calendar
        # patterns (#1471) would also flip event-write phrasings into setup
        # guidance; with it they keep their pre-#1471 routing (temporal).
        # Same conservative over-blocking discipline as the repo guard.
        r"\b(?:meeting|event|appointment|invite|reminder)s?\b",
    ]

    # Issue #673: TRUST patterns for trust explanation queries
    # Routes to ExplanationHandler from services.trust
    # Patterns derived from ExplanationDetector but simplified for pre-classification
    # Issue #1030 R4: PROVENANCE patterns for "why did you suggest that?" queries.
    # MUST be checked BEFORE TRUST_PATTERNS — TRUST has `\bwhy did you (do|just|go ahead)\b`
    # which would otherwise win on "why did you mention..." phrases. The verb-list
    # here is intentionally narrow (mention/bring/suggest/recommend/surface/raise/flag),
    # NOT generic ("do" stays with TRUST = "why did you do that"). See R1 risk in
    # dev/active/r4-suggestion-provenance-design-2026-06-01.md.
    PROVENANCE_PATTERNS = [
        # "why did you mention/bring up/suggest/recommend/surface/raise/flag X?"
        r"\bwhy did you (mention|bring up|suggest|recommend|surface|raise|flag)\b",
        # "where did you get that / where did that come from / where did you find it"
        r"\bwhere did (you get|that come from|you find)\b",
        # "how did you know (about/that)?"
        r"\bhow did you know( about| that)?\b",
        # "what made you (mention|think|suggest|bring) X?"
        r"\bwhat made you (mention|think|suggest|bring)\b",
        # "how do you know (about|that) X?"
        r"\bhow do you know (about|that)\b",
        # "why is X on (my|your|the) list/radar/mind?"
        r"\bwhy.* on (my|your|the) (list|radar|mind)\b",
        # "what's that based on / based on what"
        r"\bbased on what\b",
        r"\bwhat'?s that based on\b",
    ]

    TRUST_PATTERNS = [
        # Capability boundary questions - "Why can't you...?"
        r"\bwhy can'?t you\b",
        r"\bwhy won'?t you\b",
        r"\bwhy don'?t you\b",
        r"\bwhy (are|do) you (so|being so|always) (cautious|careful|conservative)\b",
        r"\bwhat can'?t you do\b",
        r"\bwhat are your limits\b",
        r"\bcapability (boundary|boundaries|limits)\b",
        # Relationship/trust level questions - "How well do you know me?"
        r"\bhow (well )?do you know me\b",
        r"\bdo you trust me\b",
        r"\bhow much do you trust\b",
        r"\bwhat'?s our relationship\b",
        r"\bhow do you see our relationship\b",
        r"\bhow do (we|you and i) work together\b",
        # Why did/didn't you questions about behavior
        r"\bwhy did you (do|just|go ahead)\b",
        r"\bwhy do you (always|keep)\b",
        r"\bi didn'?t (ask|tell) you to\b",
    ]

    # Issue #674: MEMORY patterns for history/memory queries
    # Routes to UserHistoryService from services.memory
    # Issue #1030 INSIGHT-PULL: route "what have you learned about X" queries
    # to MEMORY/pull_insights so context_assembler fetches insights from the
    # InsightRepository and the floor weaves them into its response.
    # Distinct from MEMORY_PATTERNS (conversation-history queries) — these are
    # about Piper's *learned insights*, not conversation transcripts.
    # MUST be checked BEFORE MEMORY_PATTERNS so "what have you learned" wins over
    # "what do you remember" (semantic adjacency).
    INSIGHT_PULL_PATTERNS = [
        # "what have you learned (about X)?"
        r"\bwhat have you learned\b",
        # "what do you know about (me|my X|topic)?"
        r"\bwhat do you know about (me|my |our |the )",
        # "tell me what you've learned / what you have learned"
        r"\btell me what you('ve| have) learned\b",
        # "what insights do you have"
        r"\bwhat insights do you have\b",
        # "show me what you've learned / what you have learned"
        r"\bshow me what you('ve| have) learned\b",
        # "what patterns have you noticed"
        r"\bwhat patterns have you (noticed|observed|found|seen)\b",
        # "what have you noticed about (me|my X|topic)"
        r"\bwhat have you noticed about (me|my |our |the )",
    ]

    MEMORY_PATTERNS = [
        # Direct memory questions - "What do you remember?"
        r"\bwhat do you remember\b",
        r"\bwhat can you remember\b",
        r"\bdo you remember\b",
        r"\bremember (when|that|our|my)\b",
        # History access patterns - "Show my history"
        r"\b(show|view|see) (my |our )?(conversation )?history\b",
        r"\b(my|our) (conversation )?history\b",
        r"\bpast conversations?\b",
        r"\bprevious (conversations?|chats?|messages?)\b",
        r"\bconversation log\b",
        # Search patterns - "Find when I mentioned..."
        r"\bfind (when|where) (i|we)\b",
        r"\bsearch (my |our )?(conversation )?history\b",
        r"\bwhat (did|have) (i|we) (talk|discuss|say)\b",
        r"\bwhat (i|we) (said|talked|discussed)\b",
        # Memory meta questions - "How much do you remember?"
        r"\bhow (much|far back) do you remember\b",
        r"\bhow long (is|do) (your|my) memory\b",
    ]

    # Issue #675: PORTFOLIO patterns for project management operations
    # Routes to PortfolioService from services.onboarding
    # Note: Imports patterns from portfolio_service.py at module level for reuse
    #
    # 1527: the DELETE-family patterns below are guarded by a negative
    # lookahead — when the delete-target noun phrase carries reminder/todo
    # vocabulary ("delete the reminder to hydrate", "delete my hydrate
    # reminder", "delete my reminders", "remove the todo about X"), the
    # portfolio lane must NOT claim the turn. The greedy `(.+)` capture had
    # claimed every such delete into "I couldn't find a project called
    # 'the reminder to hydrate'" (PM live 2026-08-29, three misroutes in one
    # exchange, including a phrase Piper itself taught). The guard makes the
    # pattern DECLINE so the turn falls through this surface to the LLM lane,
    # whose delete_todo emission dispatches the 1666 DESTRUCTIVE rail family
    # (delete_todo/remove_todo/cancel_todo). NARROWING ONLY: no new claim is
    # added anywhere — a guarded miss is a fall-through, never a reroute.
    REMINDER_TODO_NOUN_GUARD = r"(?!.*\b(?:reminders?|to-?dos?|tasks?)\b)"

    PORTFOLIO_PATTERNS = [
        # Archive operations - "Archive my project X"
        r"\barchive\s+(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        r"\bhide\s+(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        r"\bput\s+(.+)\s+(?:away|aside)",
        # Delete operations - "Delete my project X" (reminder/todo-noun
        # deletes decline via the guard, #1527 — see comment above)
        rf"\bdelete\s+{REMINDER_TODO_NOUN_GUARD}(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        rf"\bremove\s+{REMINDER_TODO_NOUN_GUARD}(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        rf"\bget rid of\s+{REMINDER_TODO_NOUN_GUARD}(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        # Restore operations - "Restore project X"
        r"\brestore\s+(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        r"\bunarchive\s+(?:my\s+)?(?:the\s+)?(.+)",
        r"\bbring back\s+(?:my\s+)?(?:the\s+)?(?:project\s+)?(.+)",
        # Search operations - "Search projects for Y"
        r"\bsearch\s+(?:my\s+)?projects?\s+(?:for\s+)?(.+)",
        r"\bfind\s+(?:my\s+)?project\s+(.+)",
        # Add new project - "Add a new project"
        r"\b(?:add|create)\s+(?:a\s+)?(?:new\s+)?project\b",
        r"\bnew project\b",
        # Update project - "Update project X"
        r"\bupdate\s+(?:my\s+)?(?:the\s+)?project\b",
        r"\bedit\s+(?:my\s+)?(?:the\s+)?project\b",
        # List operations - "Show my projects"
        r"\b(?:show|list|view)\s+(?:my\s+)?(?:all\s+)?(?:archived\s+)?projects\b",
    ]

    # Set-default-repo patterns (RECONNECT #1327 gap 1) — conversational counterpart
    # to the GUI default-repo setting. MUST be checked BEFORE REPO_MANAGEMENT_PATTERNS
    # (which captures "add owner/repo to ..." / link/connect) because these phrasings
    # are more specific: they all carry the word "default" alongside repo/repository.
    # The owner/name token is parsed out of original_message by the handler (mirrors
    # the issue-number parse in the close/reopen handlers), so these patterns only
    # need to RECOGNIZE the intent, not capture the repo.
    SET_DEFAULT_REPO_PATTERNS = [
        # "set/change/make my default repo to owner/name" (+ repository, + "my", + "to")
        r"\b(?:set|change|update|make)\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        # "use owner/name as my default repo[sitory]"
        r"\buse\s+[\w.-]+/[\w.-]+\s+as\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        # "make owner/name my default repo[sitory]"
        r"\bmake\s+[\w.-]+/[\w.-]+\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        # "my default repo[sitory] is owner/name" / "... should be owner/name"
        r"\b(?:my\s+)?default\s+repo(?:sitory)?\s+(?:is|should be|=)\s+[\w.-]+/[\w.-]+",
    ]

    # Get-default-repo patterns (RECONNECT #1327 build #2) — the INVERSE of
    # SET_DEFAULT_REPO_PATTERNS: read the per-user default-repo preference so Piper
    # can answer "what is my default repo again?" instead of flooring (PM UAT
    # 2026-06-30). DISJOINT from the set patterns by construction: these require a
    # read verb ("what/which/show") + the literal "default repo[sitory]", whereas
    # the set patterns require a write verb ("set/change/update/make/use"). No
    # owner/name token is involved (it's a read), so these only RECOGNIZE the intent.
    GET_DEFAULT_REPO_PATTERNS = [
        # "what's/what is my default repo[sitory]" (+ "again", "?", "set", etc.)
        r"\bwhat(?:'s|\s+is)?\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        # "what default repo[sitory] do I have / is set / ..."
        r"\bwhat\s+default\s+repo(?:sitory)?\b",
        # "which (repo[sitory]) is my default" / "which is my default repo"
        r"\bwhich\s+(?:repo(?:sitory)?\s+)?is\s+(?:my\s+)?default(?:\s+repo(?:sitory)?)?\b",
        # "show/see/tell me my default repo[sitory]"
        r"\b(?:show|see|tell\s+me|get)\s+(?:my\s+)?default\s+repo(?:sitory)?\b",
        # "(what is) my default repo[sitory]" bare — only when no set verb leads it
        r"^(?:my\s+)?default\s+repo(?:sitory)?\??$",
    ]

    # Repository management patterns (Issue #862)
    REPO_MANAGEMENT_PATTERNS = [
        # Link operations - "link owner/repo to project"
        r"\blink\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)",
        r"\blink\s+[\w.-]+/[\w.-]+",
        r"\bconnect\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)",
        r"\bconnect\s+[\w.-]+/[\w.-]+",
        r"\badd\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+to\s+",
        r"\badd\s+[\w.-]+/[\w.-]+\s+to\s+",
        # Unlink operations - "unlink repo from project"
        r"\bunlink\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)",
        r"\bremove\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+from\s+",
        r"\bdisconnect\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)",
        # List operations - "show my repos", "which repos are linked?"
        r"\b(?:show|list|view|which)\s+(?:(?:my|the)\s+)?(?:linked\s+)?repos\b",
        r"\bwhich\s+repos?\s+(?:are\s+)?(?:linked|connected)\b",
        r"\bshow\s+(?:project\s+)?repositories\b",
    ]

    # File reference patterns (with variations and typo tolerance)
    FILE_REFERENCE_PATTERNS = [
        # Direct references
        r"\b(the file|that file|my file|this file)\b",
        r"\b(the document|that document|my document|this document)\b",
        r"\b(the doc|that doc|my doc|this doc)\b",
        r"\b(what i uploaded|the upload|that upload|this upload)\b",
        # File types
        r"\b(the csv|that csv|my csv|this csv)\b",
        r"\b(the pdf|that pdf|my pdf|this pdf)\b",
        r"\b(the spreadsheet|that spreadsheet|my spreadsheet|this spreadsheet)\b",
        r"\b(the excel file|that excel file|my excel file|this excel file)\b",
        r"\b(the report|that report|my report|this report)\b",
        r"\b(the data file|that data file|my data file|this data file)\b",
        r"\b(the text file|that text file|my text file|this text file)\b",
        r"\b(the markdown file|that markdown file|my markdown file|this markdown file)\b",
        r"\b(the json file|that json file|my json file|this json file)\b",
        # Abbreviated forms
        r"\b(the txt|that txt|my txt|this txt)\b",
        r"\b(the md|that md|my md|this md)\b",
        r"\b(the xlsx|that xlsx|my xlsx|this xlsx)\b",
        r"\b(the docx|that docx|my docx|this docx)\b",
        # Generic patterns with adjectives
        r"\b(that \w+(?:\s+\w+)* file|the \w+(?:\s+\w+)* file|my \w+(?:\s+\w+)* file|this \w+(?:\s+\w+)* file)\b",
        r"\b(that \w+(?:\s+\w+)* document|the \w+(?:\s+\w+)* document|my \w+(?:\s+\w+)* document|this \w+(?:\s+\w+)* document)\b",
        r"\b(that \w+(?:\s+\w+)* doc|the \w+(?:\s+\w+)* doc|my \w+(?:\s+\w+)* doc|this \w+(?:\s+\w+)* doc)\b",
        # Common typos and variations
        r"\b(teh file|taht file|th file)\b",
        r"\b(documnet|docuemnt|docment)\b",
        r"\b(fiel|fils|fille)\b",
        r"\b(uploded|uplaoded|uploadd)\b",
        r"\b(reprot|reoprt|raport)\b",
        r"\b(excell|exel|excel)\b",
        r"\b(spreedsheet|spredsheet|spreadsheat)\b",
        # Integration-related typos (from handoff doc)
        r"\b(intregration|integartion|intergration)\b",
        r"\b(analys[ei]s|analisys|anlyze)\b",
        r"\b(summar[iy]ze|summerize|summarise)\b",
    ]

    @staticmethod
    def pre_classify(message: str) -> Optional[Intent]:
        """Pre-classify message using rule-based patterns.

        Thin delegator over :meth:`pre_classify_with_pattern_list` — the
        claim is byte-identical; the pattern-list identity is dropped here.
        Callers that need to know WHICH ``*PATTERNS`` list claimed the
        message (the pre-claim shadow probe, measurement only) call the
        sibling directly.
        """
        intent, _pattern_list = PreClassifier.pre_classify_with_pattern_list(message)
        return intent

    @staticmethod
    def pre_classify_with_pattern_list(
        message: str,
    ) -> Tuple[Optional[Intent], Optional[str]]:
        """Rule-based pre-classification WITH the claiming list's identity.

        Returns ``(intent, pattern_list_name)`` — the name of the class-level
        ``*PATTERNS`` list whose match produced the claim (e.g.
        ``"DISCOVERY_PATTERNS"``), or ``(None, None)`` when no pattern claims.
        Two synthetic names cover claim sites without a class-level list: the
        #1068 inline milestone-status check reports
        ``MILESTONE_STATUS_INLINE_PATTERNS``, and the helper-guarded lanes
        report their underlying lists (``INTEGRATION_CONNECT_PATTERNS``,
        ``REMINDER_QUERY_PATTERNS``). The identity is telemetry for the
        pre-claim shadow probe (2026-09-02, the measurement backbone for the
        PM-ratified 2026-08-29 narrowing schedule) — nothing routes on it.
        """
        clean_msg = message.strip().lower()
        clean_for_matching = clean_msg.rstrip(string.punctuation + "!?.,;:😊🙂👋")

        # DEBUG: Log the processing
        import structlog

        logger = structlog.get_logger()
        logger.info(f"PRE_CLASSIFIER DEBUG - Original: '{message}'")
        logger.info(f"PRE_CLASSIFIER DEBUG - Clean: '{clean_msg}'")
        logger.info(f"PRE_CLASSIFIER DEBUG - Clean for matching: '{clean_for_matching}'")

        # Check for greetings
        greeting_match = PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.GREETING_PATTERNS
        )
        logger.info(f"PRE_CLASSIFIER DEBUG - Greeting match: {greeting_match}")
        # #1416: the canned pleasantry short-circuits may only claim messages
        # that are ONLY pleasantries. "Hi, … How do I address you?" used to
        # match \bhi\b here and swallow the question; with substantive residue
        # the message now falls through to full classification, where the floor
        # greets AND answers.
        pleasantry_only = PreClassifier._is_pleasantry_only(clean_for_matching)
        if greeting_match and pleasantry_only:
            # Find which pattern matched for debugging
            for pattern in PreClassifier.GREETING_PATTERNS:
                if re.search(pattern, clean_for_matching):
                    logger.info(f"PRE_CLASSIFIER DEBUG - Matched greeting pattern: '{pattern}'")
                    break
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="greeting",
                confidence=1.0,
                context={"original_message": message},
            ), "GREETING_PATTERNS"
        if greeting_match and not pleasantry_only:
            logger.info(
                "PRE_CLASSIFIER DEBUG - Greeting with substantive residue; "
                "falling through to full classification (#1416)"
            )

        # Check for farewells (#1416: same pleasantry-only precondition)
        if pleasantry_only and PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.FAREWELL_PATTERNS
        ):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="farewell",
                confidence=1.0,
                context={"original_message": message},
            ), "FAREWELL_PATTERNS"

        # Check for thanks (#1416: same pleasantry-only precondition)
        if pleasantry_only and PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.THANKS_PATTERNS
        ):
            return Intent(
                category=IntentCategory.CONVERSATION,
                action="thanks",
                confidence=1.0,
                context={"original_message": message},
            ), "THANKS_PATTERNS"

        # Issue #488: Check DISCOVERY before IDENTITY
        # "What can you do?" should return dynamic capabilities, not static identity
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.DISCOVERY_PATTERNS):
            return Intent(
                category=IntentCategory.DISCOVERY,
                action="get_capabilities",
                confidence=1.0,
                context={"original_message": message},
            ), "DISCOVERY_PATTERNS"

        # Issue #1030 R4: Check PROVENANCE BEFORE TRUST
        # "Why did you mention/suggest/recommend X?" routes to ProvenanceHandler
        # which looks up turn_provenance sidecar. TRUST has overlapping
        # `\bwhy did you (do|just|go ahead)\b` so order matters here.
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.PROVENANCE_PATTERNS):
            return Intent(
                category=IntentCategory.PROVENANCE,
                action="explain_suggestion",
                confidence=1.0,
                context={"original_message": message},
            ), "PROVENANCE_PATTERNS"

        # Issue #673: Check TRUST before IDENTITY
        # "Why can't you...?" and "How well do you know me?" route to ExplanationHandler
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.TRUST_PATTERNS):
            return Intent(
                category=IntentCategory.TRUST,
                action="explain_trust",
                confidence=1.0,
                context={"original_message": message},
            ), "TRUST_PATTERNS"

        # Issue #1030 INSIGHT-PULL: Check pull-mode insight queries BEFORE MEMORY
        # so "what have you learned about my work style" wins over "what do you
        # remember about me" (semantic adjacency; different routing).
        # Routes to MEMORY/pull_insights — floor-routed but with InsightRepository
        # context enrichment per context_assembler.
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.INSIGHT_PULL_PATTERNS):
            return Intent(
                category=IntentCategory.MEMORY,
                action="pull_insights",
                confidence=1.0,
                context={"original_message": message},
            ), "INSIGHT_PULL_PATTERNS"

        # Issue #674: Check MEMORY before IDENTITY
        # "What do you remember about me?" routes to UserHistoryService
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.MEMORY_PATTERNS):
            return Intent(
                category=IntentCategory.MEMORY,
                action="get_memory",
                confidence=1.0,
                context={"original_message": message},
            ), "MEMORY_PATTERNS"

        # RECONNECT #1327 build #2: Check GET_DEFAULT_REPO before SET_DEFAULT_REPO
        # and DOCUMENT_QUERY. The read patterns ("what/which/show ... default repo")
        # are disjoint from the set patterns (set/change/update/make/use) by
        # construction, so ordering between the two is safe; GET first lets a read
        # phrasing win deterministically. Must precede DOCUMENT_QUERY because
        # "show my default repo" would otherwise match a document/show pattern.
        # Routes a per-user preference READ (no write, no owner/name token).
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.GET_DEFAULT_REPO_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="get_default_repo",
                confidence=1.0,
                context={"original_message": message},
            ), "GET_DEFAULT_REPO_PATTERNS"

        # RECONNECT #1327: Check SET_DEFAULT_REPO before DOCUMENT_QUERY and
        # REPO_MANAGEMENT. It must precede DOCUMENT_QUERY because a phrasing like
        # "change my default repo to owner/name" otherwise matches the document
        # "change ... to" pattern. These set-default patterns are highly specific
        # (they require the literal "default repo[sitory]"), so they steal no
        # legitimate document or repo-management queries. Routes a per-user
        # preference write, distinct from linking a repo to a project (manage_repos).
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.SET_DEFAULT_REPO_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="set_default_repo",
                confidence=1.0,
                context={"original_message": message},
            ), "SET_DEFAULT_REPO_PATTERNS"

        # #1256: stakeholder-update composition BEFORE document patterns —
        # "write an update FOR [person]" is outbound communication, not
        # document modification (see STAKEHOLDER_UPDATE_PATTERNS comment).
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.STAKEHOLDER_UPDATE_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="write_stakeholder_update",
                confidence=1.0,
                context={"original_message": message},
            ), "STAKEHOLDER_UPDATE_PATTERNS"

        # Issue #522, #681: Check Document query patterns BEFORE PORTFOLIO
        # "update the project plan doc" must route to QUERY, not PORTFOLIO
        # Document patterns are more specific (require "doc/document" suffix)
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.DOCUMENT_QUERY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="update_document_query",
                confidence=1.0,
                context={"original_message": message},
            ), "DOCUMENT_QUERY_PATTERNS"

        # Issue #862: Check REPO_MANAGEMENT before PORTFOLIO (more specific)
        # "link owner/repo to project" routes to repo management handler
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.REPO_MANAGEMENT_PATTERNS
        ):
            return Intent(
                category=IntentCategory.PORTFOLIO,
                action="manage_repos",
                confidence=1.0,
                context={"original_message": message},
            ), "REPO_MANAGEMENT_PATTERNS"

        # Issue #675: Check PORTFOLIO for project management operations
        # "Archive/delete/restore project X" routes to PortfolioService
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.PORTFOLIO_PATTERNS):
            return Intent(
                category=IntentCategory.PORTFOLIO,
                action="manage_portfolio",
                confidence=1.0,
                context={"original_message": message},
            ), "PORTFOLIO_PATTERNS"

        # Issue #901: Check feature/integration info queries BEFORE identity
        # "Tell me more about the GitHub integration" → QUERY, not IDENTITY
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.FEATURE_INFO_PATTERNS):
            return Intent(
                category=IntentCategory.QUERY,
                action="get_feature_info",
                confidence=1.0,
                context={"original_message": message},
            ), "FEATURE_INFO_PATTERNS"

        # Check for identity queries - "Who are you?"
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.IDENTITY_PATTERNS):
            return Intent(
                category=IntentCategory.IDENTITY,
                action="get_identity",
                confidence=1.0,
                context={"original_message": message},
            ), "IDENTITY_PATTERNS"

        # Issue #521: Check CONTEXTUAL_QUERY before TEMPORAL to prevent pattern collision
        # "what changed since yesterday" would match r"\bwhat.*yesterday\b" in TEMPORAL
        # but should route to changes_query instead
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.CONTEXTUAL_QUERY_PATTERNS
        ):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bwhat changed since\b",
                    r"\bwhat'?s changed since\b",
                    r"\bshow.*changes since\b",
                    r"\bshow me.*changed\b",
                    r"\bchanges since\b",
                    r"\bactivity since\b",
                    r"\bupdates since\b",
                ]
            ):
                action = "changes_query"
            else:
                action = "attention_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            ), "CONTEXTUAL_QUERY_PATTERNS"

        # Issue #523: Phase A Canonical Query patterns
        # Issue #589: Check Calendar queries BEFORE temporal to route to QUERY handler
        # Check Calendar queries (Queries #34, #35, #61)
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.CALENDAR_QUERY_PATTERNS
        ):
            # Determine specific action based on which pattern matched
            # Issue #589: Today's calendar patterns route to meeting_time
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bwhat'?s on my calendar\b",
                    r"\bwhat is on my calendar\b",
                    r"\bmy calendar today\b",
                    r"\bcalendar today\b",
                    r"\bmeetings today\b",
                    r"\bdo i have any meetings\b",
                    r"\bdo i have meetings\b",
                    r"\bwhat meetings do i have\b",
                    r"\bwhat meetings\b",
                    r"\bmy schedule today\b",
                    r"\btoday'?s schedule\b",
                    r"\bschedule for today\b",
                    r"\bhow much time in meetings\b",
                    r"\bhow much time.*meetings\b",
                    r"\btime spent in meetings\b",
                    r"\bmeeting time\b",
                    # Issue #588: Tomorrow patterns route to meeting_time (single-day queries)
                    r"\bcalendar.*tomorrow\b",
                    r"\btomorrow'?s calendar\b",
                    r"\bmeetings.*tomorrow\b",
                    r"\bschedule.*tomorrow\b",
                    r"\btomorrow'?s schedule\b",
                    r"\bwhat'?s on my calendar.*tomorrow\b",
                    r"\bmy calendar tomorrow\b",
                    r"\bagenda.*today\b",
                    r"\bagenda.*tomorrow\b",
                    r"\bmy agenda\b",
                    r"\bon my agenda\b",
                ]
            ):
                action = "meeting_time"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\breview.*recurring meetings\b",
                    r"\bshow.*recurring meetings\b",
                    r"\baudit.*standing meetings\b",
                    r"\brecurring meetings\b",
                ]
            ):
                action = "recurring_meetings"
            else:
                action = "week_calendar"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            ), "CALENDAR_QUERY_PATTERNS"

        # Issue #1068: Status-y milestone phrasing must route to STATUS
        # before reaching GITHUB_QUERY (which has broader milestone patterns
        # for list-style queries like "show milestones"). The phrasing here
        # distinguishes "What's the next milestone?" / "milestone status" /
        # "milestone progress" (STATUS — asking about state of the work) from
        # "next milestone" / "show milestones" alone (GITHUB_QUERY listing).
        if PreClassifier._matches_patterns(
            clean_for_matching,
            [
                r"\bwhat'?s the (?:next|upcoming) milestone\b",
                r"\bmilestone status\b",
                r"\bmilestone progress\b",
            ],
        ):
            return Intent(
                category=IntentCategory.STATUS,
                action="get_project_status",
                confidence=1.0,
                context={"original_message": message},
            ), "MILESTONE_STATUS_INLINE_PATTERNS"

        # Issue #1044: Local-git status queries must be checked BEFORE
        # GITHUB_QUERY_PATTERNS — "what branch are we on?" would otherwise
        # match `\bwhat branches?\b` (optional-s plural) in the GitHub
        # remote-branches handler.
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.LOCAL_GIT_STATUS_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="local_git_status_query",
                confidence=1.0,
                context={"original_message": message},
            ), "LOCAL_GIT_STATUS_PATTERNS"

        # Check GitHub queries (Queries #41, #42, #45, #59, #60)
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GITHUB_QUERY_PATTERNS):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bwhat did we ship\b",
                    r"\bwhat shipped\b",
                    r"\bshow.*what.*shipped\b",
                    r"\bwhat.*shipped.*week\b",
                ]
            ):
                action = "shipped_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow.*stale prs\b",
                    r"\bstale pull requests\b",
                    r"\bold prs\b",
                    r"\bprs.*needing review\b",
                ]
            ):
                action = "stale_prs_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bclose issue\s*#?\d+\b",
                    r"\bclose.*completed.*issue\b",
                    r"\bclose.*issue\b",
                    # Issue #902: Confirmation patterns ("yes, close #123")
                    r"\b(yes|confirm|sure),?\s*close\s*#?\d+\b",
                ]
            ):
                action = "close_issue_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\breopen\s+issue\s*#?\d+\b",
                    r"\bre-open\s+issue\s*#?\d+\b",
                    r"\breopen\s+.*issue\b",
                    r"\bre-open\s+.*issue\b",
                    # Issue #902: Confirmation patterns ("yes, reopen #123")
                    r"\b(yes|confirm|sure),?\s*reopen\s*#?\d+\b",
                ]
            ):
                action = "reopen_issue_query"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bcomment on issue\s*#?\d+\b",
                    r"\badd comment to issue\s*#?\d+\b",
                    r"\breply to issue\s*#?\d+\b",
                    r"\bcomment\s+on\s+#?\d+\b",
                ]
            ):
                action = "comment_issue_query"
            # Issue #845: Issue listing / count queries
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bhow many.*issues\b",
                    r"\bopen issues\b",
                    r"\bmy issues\b",
                    r"\blist.*issues\b",
                    r"\bshow.*issues\b",
                    r"\bissue count\b",
                    r"\bissues.*assigned\b",
                ]
            ):
                action = "list_issues_query"
            # Issue #851: PR listing queries
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow my prs\b",
                    r"\bshow my pull requests\b",
                    r"\bmy prs\b",
                    r"\bmy pull requests\b",
                    r"\blist.*prs\b",
                    r"\blist.*pull requests\b",
                    r"\bopen pull requests\b",
                    r"\bopen prs\b",
                    r"\bprs assigned to me\b",
                    r"\bpull requests assigned to me\b",
                ]
            ):
                action = "list_prs_query"
            else:
                # Review issue query - Query #60
                action = "review_issue_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            ), "GITHUB_QUERY_PATTERNS"

        # Check Session-activity recall (#1394 / ADR-078 B4) — "what did we create
        # this session". Before Productivity; distinct from GITHUB's "what did we
        # ship" (a repo-wide live query) — this reads the session_activity ledger.
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.SESSION_ACTIVITY_QUERY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="session_activity_query",
                confidence=1.0,
                context={"original_message": message},
            ), "SESSION_ACTIVITY_QUERY_PATTERNS"

        # Check Productivity query (Query #51)
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.PRODUCTIVITY_QUERY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="productivity_query",
                confidence=1.0,
                context={"original_message": message},
            ), "PRODUCTIVITY_QUERY_PATTERNS"

        # #1521: Check reminder-QUERY before reminder-CREATION and far above
        # TEMPORAL. Read-before-write mirrors GET_DEFAULT_REPO vs
        # SET_DEFAULT_REPO: the two lanes are disjoint by construction (query
        # needs a read verb + plural "reminders"; creation needs "remind
        # me"/"set a reminder"), and _reminder_query_match's blockers keep any
        # residual write phrasing out of this lane. Claiming the shape HERE is
        # what prevents the LLM-classifier temporal misroute (#1521): the LLM
        # never sees the message.
        if PreClassifier._reminder_query_match(clean_for_matching):
            return Intent(
                category=IntentCategory.QUERY,
                action="list_reminders_query",
                confidence=1.0,
                context={"original_message": message},
            ), "REMINDER_QUERY_PATTERNS"

        # Issue #903: Check Reminder patterns (Query #32) before todo patterns
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.REMINDER_PATTERNS):
            return Intent(
                category=IntentCategory.EXECUTION,
                action="create_reminder",
                confidence=1.0,
                context={"original_message": message},
            ), "REMINDER_PATTERNS"

        # Issue #904: Check Todo completion patterns (Query #55) before list patterns
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.TODO_COMPLETE_PATTERNS
        ):
            return Intent(
                category=IntentCategory.EXECUTION,
                action="complete_todo",
                confidence=1.0,
                context={"original_message": message},
            ), "TODO_COMPLETE_PATTERNS"

        # Check Todo queries (Queries #56, #57)
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.TODO_QUERY_PATTERNS):
            # Determine specific action based on which pattern matched
            if any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow.*completed\s+todos\b",
                    r"\bshow\s+all\s+(?:my\s+)?todos\b",
                ]
            ):
                action = "list_completed_todos"
            elif any(
                re.search(pattern, clean_for_matching)
                for pattern in [
                    r"\bshow\s+(?:my\s+)?todos\b",
                    r"\blist\s+(?:my\s+)?todos\b",
                    r"\bwhat are my todos\b",
                    r"\bmy todos\b",
                ]
            ):
                action = "list_todos_query"
            else:
                action = "next_todo_query"

            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                context={"original_message": message},
            ), "TODO_QUERY_PATTERNS"

        # Note: DOCUMENT_QUERY check moved earlier (before PORTFOLIO) per Issue #681

        # Issue #1117 INTENT-TEMPORAL-OVERGREEDY: completion-history queries
        # ("when did I complete X") must be checked BEFORE TEMPORAL so they route
        # to STATUS (floor-routed, honest history answer) rather than falling
        # through to the LLM classifier, which misroutes them to current-time.
        # STATUS is floor-routed (#925); the floor handles completion-history
        # honestly (the "Did I ever complete X" variant already reaches it).
        if PreClassifier._matches_patterns(
            clean_for_matching, PreClassifier.COMPLETION_HISTORY_PATTERNS
        ):
            return Intent(
                category=IntentCategory.STATUS,
                action="check_completion_status",
                confidence=1.0,
                context={"original_message": message},
            ), "COMPLETION_HISTORY_PATTERNS"

        # #1417: integration-connect routes deterministically to the guidance
        # lane (the capability exists — this makes it *reachable*). Checked with
        # explicit collision blockers even though the #862 repo lane already ran
        # above (belt + suspenders; both are unit-tested).
        # #1471: checked BEFORE TEMPORAL — connect/link/set-up verbs out-rank
        # the temporal calendar-noun patterns. "connect my calendar" is a setup
        # ask, not a schedule query; the temporal `\bmy calendar\b` pattern was
        # winning and answering with the current time. The blockers keep the
        # repo lane (#862) and calendar event-writes ("add a meeting to my
        # calendar") out of this lane.
        connect_match = PreClassifier._integration_connect_match(clean_for_matching)
        if connect_match:
            return Intent(
                category=IntentCategory.GUIDANCE,
                action="get_contextual_guidance",
                confidence=1.0,
                context={
                    "original_message": message,
                    "setup_target": connect_match.group("integration").strip(),
                },
            ), "INTEGRATION_CONNECT_PATTERNS"

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.TEMPORAL_PATTERNS):
            return Intent(
                category=IntentCategory.TEMPORAL,
                action="get_current_time",
                confidence=1.0,
                context={"original_message": message},
            ), "TEMPORAL_PATTERNS"

        # Issue #487: Check GUIDANCE before STATUS to catch "help setup my projects"
        # before "my projects" triggers STATUS. More specific patterns should match first.
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.GUIDANCE_PATTERNS):
            return Intent(
                category=IntentCategory.GUIDANCE,
                action="get_contextual_guidance",
                confidence=1.0,
                context={"original_message": message},
            ), "GUIDANCE_PATTERNS"

        # Issue #901: Check ANALYSIS before STATUS to catch blocker/risk queries
        # "What's blocking the milestone?" should be ANALYSIS, not STATUS
        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.ANALYSIS_PATTERNS):
            return Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_blockers",
                confidence=1.0,
                context={"original_message": message},
            ), "ANALYSIS_PATTERNS"

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.STATUS_PATTERNS):
            return Intent(
                category=IntentCategory.STATUS,
                action="get_project_status",
                confidence=1.0,
                context={"original_message": message},
            ), "STATUS_PATTERNS"

        if PreClassifier._matches_patterns(clean_for_matching, PreClassifier.PRIORITY_PATTERNS):
            return Intent(
                category=IntentCategory.PRIORITY,
                action="get_top_priority",
                confidence=1.0,
                context={"original_message": message},
            ), "PRIORITY_PATTERNS"

        return None, None

    @staticmethod
    def detect_file_reference(message: str) -> bool:
        """Check if message references an uploaded file"""
        clean_msg = message.strip().lower()

        # Exclude verb usage of "file" (e.g., "file the report", "file a complaint")
        verb_file_patterns = [
            r"\bfile\s+(?:the|a|an|this|that)\s+\w+",  # "file the report", "file a complaint"
            r"\bfile\s+\w+\s+(?:for|against|with)",  # "file complaint for", "file report against"
        ]

        # If message matches verb usage patterns, it's not a file reference
        if PreClassifier._matches_patterns(clean_msg, verb_file_patterns):
            return False

        return PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS)

    @staticmethod
    def get_file_reference_confidence(message: str) -> float:
        """Calculate confidence score for file reference detection"""
        clean_msg = message.strip().lower()

        # Different patterns have different confidence weights
        high_confidence_patterns = [
            r"\b(the file|that file|my file|this file)\b",
            r"\b(the document|that document|my document|this document)\b",
            r"\b(what i uploaded|the upload|that upload|this upload|my upload)\b",
        ]

        medium_confidence_patterns = [
            r"\b(the csv|that csv|my csv|this csv)\b",
            r"\b(the pdf|that pdf|my pdf|this pdf)\b",
            r"\b(the doc|that doc|my doc|this doc)\b",
            r"\b(the report|that report|my report|this report)\b",
        ]

        low_confidence_patterns = [
            r"\b(teh file|taht file|th file)\b",
            r"\b(documnet|docuemnt|docment)\b",
            r"\b(fiel|fils|fille)\b",
            r"\b(uploded|uplaoded|uploadd)\b",
        ]

        # Check for matches and return highest confidence
        if PreClassifier._matches_patterns(clean_msg, high_confidence_patterns):
            return 0.9
        elif PreClassifier._matches_patterns(clean_msg, medium_confidence_patterns):
            return 0.7
        elif PreClassifier._matches_patterns(clean_msg, low_confidence_patterns):
            return 0.5
        elif PreClassifier._matches_patterns(clean_msg, PreClassifier.FILE_REFERENCE_PATTERNS):
            return 0.6  # Generic patterns
        else:
            return 0.0

    @staticmethod
    def _matches_patterns(message: str, patterns: list) -> bool:
        """Check if message matches any of the given patterns using regex"""
        for pattern in patterns:
            if re.search(pattern, message):
                return True
        return False

    @staticmethod
    def _pattern_list_name(patterns: list) -> str:
        """Resolve a pattern-list OBJECT back to its class-attribute name.

        Identity comparison against the class dict — no parallel name table to
        drift (the whack-a-mole lesson: a hand-maintained mapping is a second
        copy of the precedence order). Used by the pre-claim shadow probe's
        multi-intent threading; ``UNNAMED_PATTERNS`` is the honest fallback
        for a list object that is not a class attribute (none exists today).
        """
        for attr, val in vars(PreClassifier).items():
            if attr.endswith("PATTERNS") and val is patterns:
                return attr
        return "UNNAMED_PATTERNS"

    @staticmethod
    def _reminder_query_match(clean_message: str) -> bool:
        """#1521: True iff the message is a reminder LIST/READ ask.

        Applies REMINDER_QUERY_BLOCKERS (creation + destructive verbs) before
        the query patterns. Shared by pre_classify() and
        detect_multiple_intents() so both entry surfaces resolve the shape with
        identical precedence — the same shared-helper shape as
        _integration_connect_match (#1471).
        """
        if PreClassifier._matches_patterns(clean_message, PreClassifier.REMINDER_QUERY_BLOCKERS):
            return False
        return PreClassifier._matches_patterns(clean_message, PreClassifier.REMINDER_QUERY_PATTERNS)

    @staticmethod
    def _integration_connect_match(clean_message: str):
        """#1417/#1471: the integration-connect regex match for the message,
        or None.

        Applies INTEGRATION_CONNECT_BLOCKERS (repo lane #862, calendar
        event-writes #1471) before the connect-verb x integration-noun
        patterns. Shared by pre_classify() and detect_multiple_intents() so
        both entry surfaces resolve the temporal-calendar collision with
        identical precedence (#1471) — the match carries the named
        ``integration`` group for setup_target.
        """
        if PreClassifier._matches_patterns(
            clean_message, PreClassifier.INTEGRATION_CONNECT_BLOCKERS
        ):
            return None
        for pattern in PreClassifier.INTEGRATION_CONNECT_PATTERNS:
            match = re.search(pattern, clean_message, re.IGNORECASE)
            if match:
                return match
        return None

    @staticmethod
    def detect_multiple_intents(message: str) -> MultiIntentResult:
        """
        Detect ALL intents present in a message (Issue #595).

        Unlike pre_classify() which returns the first match, this method
        finds all matching patterns to support multi-intent messages like
        "Hi Piper! What's on my agenda?"

        This detection logic is designed to be reusable for #427
        (Unified Conversation Model).

        Args:
            message: The user's message to analyze

        Returns:
            MultiIntentResult containing all detected intents
        """
        import structlog

        logger = structlog.get_logger()
        clean_msg = message.strip().lower()
        clean_for_matching = clean_msg.rstrip(string.punctuation + "!?.,;:😊🙂👋")

        intents: List[Intent] = []

        # Define pattern groups with their intent mapping
        # Each tuple: (patterns, category, action_resolver)
        # action_resolver is either a string or a callable that takes the message
        pattern_groups: List[Tuple[List[str], IntentCategory, str]] = [
            # Conversational patterns (lower priority)
            (PreClassifier.GREETING_PATTERNS, IntentCategory.CONVERSATION, "greeting"),
            (PreClassifier.FAREWELL_PATTERNS, IntentCategory.CONVERSATION, "farewell"),
            (PreClassifier.THANKS_PATTERNS, IntentCategory.CONVERSATION, "thanks"),
            # Identity patterns
            (PreClassifier.IDENTITY_PATTERNS, IntentCategory.IDENTITY, "get_identity"),
            # Calendar/agenda patterns (high priority for #595)
            (PreClassifier.CALENDAR_QUERY_PATTERNS, IntentCategory.QUERY, "meeting_time"),
            # Contextual patterns
            (PreClassifier.CONTEXTUAL_QUERY_PATTERNS, IntentCategory.QUERY, "contextual_query"),
            # Issue #1044: Local-git status patterns MUST come before github_query
            # to win specificity — "what branch are we on?" should NOT route to
            # the GitHub list_branches handler (which matches `\bwhat branches?\b`
            # with optional `s`).
            (
                PreClassifier.LOCAL_GIT_STATUS_PATTERNS,
                IntentCategory.QUERY,
                "local_git_status_query",
            ),
            # GitHub patterns
            (PreClassifier.GITHUB_QUERY_PATTERNS, IntentCategory.QUERY, "github_query"),
            # Productivity patterns
            (PreClassifier.PRODUCTIVITY_QUERY_PATTERNS, IntentCategory.QUERY, "productivity_query"),
            # Session-activity recall (#1394 / ADR-078 B4)
            (
                PreClassifier.SESSION_ACTIVITY_QUERY_PATTERNS,
                IntentCategory.QUERY,
                "session_activity_query",
            ),
            # #1521: reminder LIST query — before the todo group (adjacent
            # noun space) and before TEMPORAL (the live misroute lane). The
            # loop body guards this group with _reminder_query_match, so the
            # creation/destructive blockers apply on this path too.
            (
                PreClassifier.REMINDER_QUERY_PATTERNS,
                IntentCategory.QUERY,
                "list_reminders_query",
            ),
            # Todo patterns
            (PreClassifier.TODO_QUERY_PATTERNS, IntentCategory.QUERY, "list_todos_query"),
            # #1256: stakeholder-update BEFORE document (same precedence as the
            # single-intent path — "update for [person]" is not a doc edit)
            (
                PreClassifier.STAKEHOLDER_UPDATE_PATTERNS,
                IntentCategory.QUERY,
                "write_stakeholder_update",
            ),
            # Document patterns
            (PreClassifier.DOCUMENT_QUERY_PATTERNS, IntentCategory.QUERY, "update_document_query"),
            # Issue #1117: completion-history MUST come before TEMPORAL so
            # "when did I complete X" routes to STATUS (floor, honest history
            # answer) not TEMPORAL (current-time).
            (
                PreClassifier.COMPLETION_HISTORY_PATTERNS,
                IntentCategory.STATUS,
                "check_completion_status",
            ),
            # Temporal patterns
            (PreClassifier.TEMPORAL_PATTERNS, IntentCategory.TEMPORAL, "get_current_time"),
            # Issue #671-#675: MUX-WIRE patterns must come BEFORE STATUS to match first
            # Discovery patterns (Issue #671)
            (PreClassifier.DISCOVERY_PATTERNS, IntentCategory.DISCOVERY, "get_capabilities"),
            # Trust patterns (Issue #673)
            # Issue #1030 R4: PROVENANCE must precede TRUST in multi-intent
            # pattern groups too — same precedence reasoning as the explicit
            # check above.
            (PreClassifier.PROVENANCE_PATTERNS, IntentCategory.PROVENANCE, "explain_suggestion"),
            (PreClassifier.TRUST_PATTERNS, IntentCategory.TRUST, "explain_trust"),
            # Issue #1030 INSIGHT-PULL: insight pull MUST come before MEMORY so
            # "what have you learned about X" routes to MEMORY/pull_insights
            # (floor + InsightRepository enrichment) rather than MEMORY/get_memory
            # (floor + conversation history only).
            (PreClassifier.INSIGHT_PULL_PATTERNS, IntentCategory.MEMORY, "pull_insights"),
            # Memory patterns (Issue #674)
            (PreClassifier.MEMORY_PATTERNS, IntentCategory.MEMORY, "get_memory"),
            # Portfolio patterns (Issue #675)
            (PreClassifier.PORTFOLIO_PATTERNS, IntentCategory.PORTFOLIO, "manage_portfolio"),
            # Repo management patterns (Issue #862)
            (PreClassifier.REPO_MANAGEMENT_PATTERNS, IntentCategory.PORTFOLIO, "manage_repos"),
            # Issue #901: Feature info patterns
            (PreClassifier.FEATURE_INFO_PATTERNS, IntentCategory.QUERY, "get_feature_info"),
            # Issue #901: Analysis patterns
            (PreClassifier.ANALYSIS_PATTERNS, IntentCategory.ANALYSIS, "analyze_blockers"),
            # Status patterns
            (PreClassifier.STATUS_PATTERNS, IntentCategory.STATUS, "get_project_status"),
            # Priority patterns
            (PreClassifier.PRIORITY_PATTERNS, IntentCategory.PRIORITY, "get_top_priority"),
            # Guidance patterns
            (PreClassifier.GUIDANCE_PATTERNS, IntentCategory.GUIDANCE, "get_contextual_guidance"),
        ]

        # Check each pattern group
        connect_substituted = False
        # Pre-claim shadow probe: which *PATTERNS list produced each intent,
        # keyed by object identity so the post-loop subsumption filter (which
        # preserves the surviving Intent OBJECTS) realigns for free.
        claimed_list_by_id: dict = {}
        for patterns, category, action in pattern_groups:
            # #1471: same precedence as pre_classify() — an integration-connect
            # ask must not surface as a TEMPORAL calendar/schedule query on the
            # multi-intent path ("connect my calendar" was answered with the
            # current time). Substitute the guidance-lane intent for the
            # temporal one (rather than just skipping) so multi-intent
            # messages keep their other parts ("hi piper, connect my calendar"
            # stays greeting + setup guidance).
            if patterns is PreClassifier.TEMPORAL_PATTERNS and PreClassifier._matches_patterns(
                clean_for_matching, patterns
            ):
                connect_match = PreClassifier._integration_connect_match(clean_for_matching)
                if connect_match:
                    connect_intent = Intent(
                        category=IntentCategory.GUIDANCE,
                        action="get_contextual_guidance",
                        confidence=1.0,
                        original_message=message,
                        context={
                            "original_message": message,
                            "multi_intent_detection": True,
                            "setup_target": connect_match.group("integration").strip(),
                        },
                    )
                    intents.append(connect_intent)
                    claimed_list_by_id[id(connect_intent)] = "INTEGRATION_CONNECT_PATTERNS"
                    connect_substituted = True
                    logger.debug(
                        "multi_intent_connect_substitution",
                        category="guidance",
                        action="get_contextual_guidance",
                    )
                    continue
            # #1471: if the substitution already emitted the guidance-lane
            # intent, don't let GUIDANCE_PATTERNS add a duplicate of the same
            # (category, action) ("help me set up my calendar" matches both).
            if patterns is PreClassifier.GUIDANCE_PATTERNS and connect_substituted:
                continue
            # #1521: the reminder-query group is blocker-guarded — the shared
            # helper (not the raw pattern match) decides, so creation
            # phrasings ("remind me to X") never emit the listing intent on
            # the multi-intent path either.
            if patterns is PreClassifier.REMINDER_QUERY_PATTERNS and not (
                PreClassifier._reminder_query_match(clean_for_matching)
            ):
                continue
            if PreClassifier._matches_patterns(clean_for_matching, patterns):
                # Refine action for specific pattern groups that need it
                final_action = action

                # Special handling for calendar queries to get specific action
                if category == IntentCategory.QUERY and action == "meeting_time":
                    final_action = PreClassifier._get_calendar_action(clean_for_matching)

                # Special handling for contextual queries
                elif category == IntentCategory.QUERY and action == "contextual_query":
                    final_action = PreClassifier._get_contextual_action(clean_for_matching)

                # Special handling for GitHub queries
                elif category == IntentCategory.QUERY and action == "github_query":
                    final_action = PreClassifier._get_github_action(clean_for_matching)

                # Special handling for todo queries
                elif category == IntentCategory.QUERY and action == "list_todos_query":
                    final_action = PreClassifier._get_todo_action(clean_for_matching)

                intent = Intent(
                    category=category,
                    action=final_action,
                    confidence=1.0,
                    # #1460: populate BOTH surfaces at construction. This path
                    # returns before the classify()-entry backfill
                    # (classifier.py), so attribute-only readers (e.g. the
                    # temporal detectors, _detect_setup_request) saw "" and
                    # their gates could never fire — the #1417 mis-route
                    # resurfaced on the dominant chat path.
                    original_message=message,
                    context={"original_message": message, "multi_intent_detection": True},
                )
                intents.append(intent)
                claimed_list_by_id[id(intent)] = PreClassifier._pattern_list_name(patterns)

                logger.debug(
                    "multi_intent_detected",
                    category=category.value,
                    action=final_action,
                )

        # Issue #919: Subsumption filter — remove phantom intents caused
        # by pattern overlap between groups. When a more specific category
        # matches, drop the less specific one it subsumes.
        #
        # This mirrors the priority ordering in pre_classify() (which checks
        # CALENDAR_QUERY before TEMPORAL, etc.) but applies it to multi-intent
        # detection where ALL groups are checked.
        intents = PreClassifier._apply_subsumption_filter(intents, logger)

        result = MultiIntentResult(
            intents=intents,
            original_message=message,
            is_multi_intent=len(intents) > 1,
            # Pre-claim shadow probe: identity realigns post-filter for free —
            # the subsumption filter keeps the surviving Intent OBJECTS.
            pattern_lists=[claimed_list_by_id.get(id(i), "UNNAMED_PATTERNS") for i in intents],
        )

        logger.info(
            "multi_intent_detection_complete",
            message_preview=message[:50],
            intent_count=len(intents),
            is_multi_intent=result.is_multi_intent,
            has_greeting=result.has_greeting,
            has_substantive=result.has_substantive_intent,
        )

        return result

    @staticmethod
    def _apply_subsumption_filter(intents: List[Intent], logger) -> List[Intent]:
        """
        Issue #919: Remove phantom intents from pattern overlap.

        When a message matches both a specific and a general pattern group
        (e.g., CALENDAR_QUERY and TEMPORAL), keep only the more specific one.
        This prevents the orchestrator from trying to handle categories it
        doesn't support (QUERY through canonical handlers).

        Subsumption rules (specific → general):
          QUERY (calendar) subsumes TEMPORAL
          QUERY (contextual) subsumes TEMPORAL
          PRIORITY subsumes GUIDANCE (focus/next queries)
          STATUS subsumes TEMPORAL (work-on-today queries)
          DISCOVERY subsumes GUIDANCE (help queries)
        """
        if len(intents) <= 1:
            return intents

        categories = {i.category.value.upper() for i in intents}

        # Build a set of categories to drop
        drop_categories = set()

        # Calendar queries subsume temporal
        if "QUERY" in categories and "TEMPORAL" in categories:
            # Check if any QUERY intent is calendar-related
            query_actions = {i.action for i in intents if i.category.value.upper() == "QUERY"}
            calendar_actions = {
                "meeting_time",
                "recurring_meetings",
                "week_calendar",
                "changes_query",
                "attention_query",
            }
            if query_actions & calendar_actions:
                drop_categories.add("TEMPORAL")
                logger.debug(
                    "subsumption_filter_applied",
                    kept="QUERY",
                    dropped="TEMPORAL",
                    reason="calendar_query_subsumes_temporal",
                )

        # Priority subsumes guidance
        if "PRIORITY" in categories and "GUIDANCE" in categories:
            drop_categories.add("GUIDANCE")
            logger.debug(
                "subsumption_filter_applied",
                kept="PRIORITY",
                dropped="GUIDANCE",
                reason="priority_subsumes_guidance",
            )

        # Discovery subsumes guidance (help queries)
        if "DISCOVERY" in categories and "GUIDANCE" in categories:
            drop_categories.add("GUIDANCE")
            logger.debug(
                "subsumption_filter_applied",
                kept="DISCOVERY",
                dropped="GUIDANCE",
                reason="discovery_subsumes_guidance",
            )

        # Issue #1067: Document-update queries subsume portfolio (project) intents.
        # "Update the project roadmap document" matches both DOCUMENT_QUERY_PATTERNS
        # (specific) and PORTFOLIO_PATTERNS (general — triggered by "project").
        # The document scope is the user's actual ask; portfolio is a false-positive
        # from the word "project". Without this rule, the orchestrator dispatches
        # both, the doc handler fails (no Notion config), and the portfolio fallback
        # response is what the user sees — completely wrong category.
        if "QUERY" in categories and "PORTFOLIO" in categories:
            query_actions = {i.action for i in intents if i.category.value.upper() == "QUERY"}
            document_actions = {
                "update_document_query",
                "edit_document_query",
                "modify_document_query",
            }
            if query_actions & document_actions:
                drop_categories.add("PORTFOLIO")
                logger.debug(
                    "subsumption_filter_applied",
                    kept="QUERY",
                    dropped="PORTFOLIO",
                    reason="document_query_subsumes_portfolio",
                )

        # Issue #1084: GitHub-specific QUERY actions subsume STATUS.
        # "What's the next milestone?" matches both the milestone-specific
        # GITHUB_QUERY_PATTERNS (→ QUERY/list_milestones_query) AND
        # STATUS_PATTERNS (the milestone-phrasings landed there too, likely
        # via #1068 pre-classifier tuning). The multi-intent orchestrator
        # routes through CanonicalHandlers.handle() which only covers
        # TEMPORAL/GUIDANCE/PORTFOLIO/CONVERSATION — both intents fail with
        # "No handler for category" and the user gets the
        # _aggregate_messages fallback ("I'm having trouble processing...").
        # Single-intent QUERY/list_milestones_query goes through
        # intent_service._handle_query_intent which has the working
        # _handle_list_milestones_query path; STATUS goes to the floor LLM.
        # The specific QUERY action is the user's actual ask; STATUS is the
        # false-positive overlap. Collapsing to single-intent QUERY routes
        # via the working path.
        if "QUERY" in categories and "STATUS" in categories:
            query_actions = {i.action for i in intents if i.category.value.upper() == "QUERY"}
            github_specific_query_actions = {
                "list_milestones_query",
                "list_releases_query",
                "list_labels_query",
                "list_branches_query",
                "list_prs_query",
                "list_issues_query",
            }
            if query_actions & github_specific_query_actions:
                drop_categories.add("STATUS")
                logger.debug(
                    "subsumption_filter_applied",
                    kept="QUERY",
                    dropped="STATUS",
                    reason="github_specific_query_subsumes_status",
                )

        if not drop_categories:
            return intents

        filtered = [i for i in intents if i.category.value.upper() not in drop_categories]
        logger.info(
            "subsumption_filter_result",
            original_count=len(intents),
            filtered_count=len(filtered),
            dropped=list(drop_categories),
        )
        return filtered

    @staticmethod
    def _get_calendar_action(message: str) -> str:
        """Determine specific calendar action based on pattern match."""
        # Check for recurring meetings
        recurring_patterns = [
            r"\breview.*recurring meetings\b",
            r"\bshow.*recurring meetings\b",
            r"\baudit.*standing meetings\b",
            r"\brecurring meetings\b",
        ]
        if PreClassifier._matches_patterns(message, recurring_patterns):
            return "recurring_meetings"

        # Check for week calendar
        week_patterns = [
            r"\bwhat'?s my week look like\b",
            r"\bshow.*my week\b",
            r"\bweek ahead\b",
            r"\bweek calendar\b",
            r"\bcalendar.*this week\b",
            r"\bcalendar.*next week\b",
            r"\bschedule.*this week\b",
            r"\bschedule.*next week\b",
            r"\bmeetings.*this week\b",
            r"\bmeetings.*next week\b",
            r"\bagenda.*this week\b",
            r"\bagenda.*next week\b",
        ]
        if PreClassifier._matches_patterns(message, week_patterns):
            return "week_calendar"

        # Default: meeting_time (single day queries)
        return "meeting_time"

    @staticmethod
    def _get_contextual_action(message: str) -> str:
        """Determine specific contextual action based on pattern match."""
        changes_patterns = [
            r"\bwhat changed since\b",
            r"\bwhat'?s changed since\b",
            r"\bshow.*changes since\b",
            r"\bshow me.*changed\b",
            r"\bchanges since\b",
            r"\bactivity since\b",
            r"\bupdates since\b",
        ]
        if PreClassifier._matches_patterns(message, changes_patterns):
            return "changes_query"
        return "attention_query"

    @staticmethod
    def _get_github_action(message: str) -> str:
        """Determine specific GitHub action based on pattern match."""
        shipped_patterns = [
            r"\bwhat did we ship\b",
            r"\bwhat shipped\b",
            r"\bshow.*what.*shipped\b",
            r"\bwhat.*shipped.*week\b",
        ]
        if PreClassifier._matches_patterns(message, shipped_patterns):
            return "shipped_query"

        stale_patterns = [
            r"\bshow.*stale prs\b",
            r"\bstale pull requests\b",
            r"\bold prs\b",
            r"\bprs.*needing review\b",
        ]
        if PreClassifier._matches_patterns(message, stale_patterns):
            return "stale_prs_query"

        close_patterns = [
            r"\bclose issue\s*#?\d+\b",
            r"\bclose.*completed.*issue\b",
            r"\bclose.*issue\b",
        ]
        if PreClassifier._matches_patterns(message, close_patterns):
            return "close_issue_query"

        reopen_patterns = [
            r"\breopen\s+issue\s*#?\d+\b",
            r"\bre-open\s+issue\s*#?\d+\b",
            r"\breopen\s+.*issue\b",
            r"\bre-open\s+.*issue\b",
        ]
        if PreClassifier._matches_patterns(message, reopen_patterns):
            return "reopen_issue_query"

        comment_patterns = [
            r"\bcomment on issue\s*#?\d+\b",
            r"\badd comment to issue\s*#?\d+\b",
            r"\breply to issue\s*#?\d+\b",
            r"\bcomment\s+on\s+#?\d+\b",
        ]
        if PreClassifier._matches_patterns(message, comment_patterns):
            return "comment_issue_query"

        # Issue #845: Issue listing / count queries
        list_issues_patterns = [
            r"\bhow many.*issues\b",
            r"\bopen issues\b",
            r"\bmy issues\b",
            r"\blist.*issues\b",
            r"\bshow.*issues\b",
            r"\bissue count\b",
            r"\bissues.*assigned\b",
        ]
        if PreClassifier._matches_patterns(message, list_issues_patterns):
            return "list_issues_query"

        # Issue #851: PR listing queries
        list_prs_patterns = [
            r"\bshow my prs\b",
            r"\bshow my pull requests\b",
            r"\bmy prs\b",
            r"\bmy pull requests\b",
            r"\blist.*prs\b",
            r"\blist.*pull requests\b",
            r"\bopen pull requests\b",
            r"\bopen prs\b",
            r"\bprs assigned to me\b",
            r"\bpull requests assigned to me\b",
        ]
        if PreClassifier._matches_patterns(message, list_prs_patterns):
            return "list_prs_query"

        # Issue #1039: Milestone listing queries
        # State-filter UX deferred to #1051; default-state behavior here
        list_milestones_patterns = [
            r"\bshow.*milestones?\b",
            r"\blist.*milestones?\b",
            r"\bnext milestone\b",
            r"\bwhat milestones?\b",
            r"\bmilestones?\s+(?:status|count|list|due)\b",
            r"\bwhen.*milestone\b",
        ]
        if PreClassifier._matches_patterns(message, list_milestones_patterns):
            return "list_milestones_query"

        # Issue #1039: Release listing queries
        # Prerelease filter UX deferred to #1051; handler shows flag inline
        list_releases_patterns = [
            r"\brecent releases?\b",
            r"\bshow.*releases?\b",
            r"\blist.*releases?\b",
            r"\bwhat version (?:are we on|is current)\b",
            r"\bcurrent (?:release|version)\b",
            r"\blatest release\b",
        ]
        if PreClassifier._matches_patterns(message, list_releases_patterns):
            return "list_releases_query"

        # Issue #1040: Label listing queries
        list_labels_patterns = [
            r"\bwhat labels?\b",
            r"\bshow.*labels?\b",
            r"\blist.*labels?\b",
            r"\bissue labels?\b",
            r"\blabels?\s+(?:list|count)\b",
            r"\b(?:available|all)\s+labels?\b",
        ]
        if PreClassifier._matches_patterns(message, list_labels_patterns):
            return "list_labels_query"

        # Issue #1040: Branch listing queries
        # Per Q5 disposition: "all non-default" — handler returns all branches
        # with default-first sort. Filter syntax (claude/* patterns) deferred.
        # Local-git "what branch are we on?" is tracked by #1044.
        list_branches_patterns = [
            r"\bactive branches?\b",
            r"\bshow.*branches?\b",
            r"\blist.*branches?\b",
            r"\bfeature branches?\b",
            r"\bcurrent branches?\b",
            r"\bwhat branches?\b",
        ]
        if PreClassifier._matches_patterns(message, list_branches_patterns):
            return "list_branches_query"

        return "review_issue_query"

    @staticmethod
    def _get_todo_action(message: str) -> str:
        """Determine specific todo action based on pattern match."""
        list_patterns = [
            r"\bshow\s+(?:my\s+)?todos\b",
            r"\blist\s+(?:my\s+)?todos\b",
            r"\bwhat are my todos\b",
            r"\bmy todos\b",
        ]
        if PreClassifier._matches_patterns(message, list_patterns):
            return "list_todos_query"
        return "next_todo_query"
