"""
Shared Types
Common enums and types used across services
"""
from enum import Enum

class IntentCategory(Enum):
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    STRATEGY = "strategy"
    LEARNING = "learning"

class WorkflowType(Enum):
    CREATE_FEATURE = "create_feature"
    ANALYZE_METRICS = "analyze_metrics"
    CREATE_TICKET = "create_ticket"
    CREATE_TASK = "create_task"
    REVIEW_ITEM = "review_item"
    GENERATE_REPORT = "generate_report"
    PLAN_STRATEGY = "plan_strategy"
    LEARN_PATTERN = "learn_pattern"
    
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
    ANALYZE_GITHUB_ISSUE = "analyze_github_issue"
    JIRA_CREATE_TICKET = "jira_create_ticket"
    SLACK_SEND_MESSAGE = "slack_send_message"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"