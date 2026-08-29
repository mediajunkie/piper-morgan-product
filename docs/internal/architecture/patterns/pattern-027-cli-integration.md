# Pattern-027: CLI Integration Pattern

## Status

**Proven**

## Context

Command-line interfaces often become disconnected from underlying service architectures, leading to duplicated business logic, inconsistent behavior, and poor user experience. Without proper integration patterns, CLI tools either bypass service layers (creating maintenance nightmares) or provide poor formatting and user interaction. The CLI Integration Pattern addresses:

- Integrating command-line interfaces with underlying service architectures seamlessly
- Providing beautiful, consistent output formatting for enhanced user experience
- Enabling learning system integration for intelligent CLI behavior
- Maintaining separation between presentation logic and business logic
- Supporting both interactive and scripted usage patterns
- Creating progressive disclosure for complex data and operations

## Pattern Description

The CLI Integration Pattern integrates command-line interfaces with underlying service architectures while providing beautiful output formatting, learning system integration, and consistent user experience. The pattern maintains clear separation between CLI presentation logic and business logic while enabling rich, interactive command-line experiences.

## Implementation

### Structure

```python
# CLI integration framework
class CLIIntegrationFramework:
    def __init__(self):
        self.service_locator = ServiceLocator()
        self.formatter = OutputFormatter()
        self.learning_system = LearningSystemIntegrator()
        self.error_handler = CLIErrorHandler()

    def create_command(self, command_name: str, service_dependencies: List[str]) -> CLICommand:
        """Create integrated CLI command with service dependencies"""
        pass

    def register_formatter(self, output_type: str, formatter: Callable):
        """Register custom formatter for specific output types"""
        pass

    async def execute_command(self, command: CLICommand, args: Dict[str, Any]) -> CommandResult:
        """Execute command with full service integration"""
        pass
```

### Example (Beautiful CLI Command with Service Integration)

```python
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import structlog

logger = structlog.get_logger()

class CLICommand(ABC):
    """Base class for CLI commands with service integration"""

    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m",
        "bold": "\033[1m",
        "dim": "\033[2m"
    }

    def __init__(self, service_locator: ServiceLocator):
        self.service_locator = service_locator
        self.services_initialized = False

    async def _initialize_services(self):
        """Initialize required services lazily"""
        if not self.services_initialized:
            await self._setup_services()
            self.services_initialized = True

    @abstractmethod
    async def _setup_services(self):
        """Setup service dependencies - implemented by subclasses"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> CommandResult:
        """Execute the command - implemented by subclasses"""
        pass

    def print_header(self, text: str, color: str = "cyan") -> None:
        """Print formatted section header with consistent styling"""
        separator = "=" * max(60, len(text) + 4)
        color_code = self.COLORS.get(color, self.COLORS["cyan"])
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]

        print(f"\n{bold}{color_code}{separator}{reset}")
        print(f"{bold}{color_code}  {text}{reset}")
        print(f"{bold}{color_code}{separator}{reset}\n")

    def print_subheader(self, text: str, color: str = "blue") -> None:
        """Print formatted subsection header"""
        color_code = self.COLORS.get(color, self.COLORS["blue"])
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]

        print(f"{bold}{color_code}▶ {text}{reset}")

    def print_success(self, message: str) -> None:
        """Print success message with consistent formatting"""
        green = self.COLORS["green"]
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]
        print(f"{bold}{green}✅ {message}{reset}")

    def print_warning(self, message: str) -> None:
        """Print warning message with consistent formatting"""
        yellow = self.COLORS["yellow"]
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]
        print(f"{bold}{yellow}⚠️  {message}{reset}")

    def print_error(self, message: str) -> None:
        """Print error message with consistent formatting"""
        red = self.COLORS["red"]
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]
        print(f"{bold}{red}❌ {message}{reset}")

    def print_info(self, message: str, indent: int = 0) -> None:
        """Print informational message with optional indentation"""
        blue = self.COLORS["blue"]
        reset = self.COLORS["reset"]
        indent_str = "  " * indent
        print(f"{indent_str}{blue}ℹ️  {message}{reset}")

class IssuesCommand(CLICommand):
    """CLI command for GitHub issues with beautiful formatting and learning integration"""

    def __init__(self, service_locator: ServiceLocator):
        super().__init__(service_locator)
        self.github_agent = None
        self.learning_system = None
        self.issue_classifier = None

    async def _setup_services(self):
        """Setup GitHub and learning services"""
        self.github_agent = await self.service_locator.get_service('github_agent')
        self.learning_system = await self.service_locator.get_service('learning_system')
        self.issue_classifier = await self.service_locator.get_service('issue_classifier')

        logger.info("Issues command services initialized")

    async def triage_issues(self, project: Optional[str] = None, limit: int = 10) -> CommandResult:
        """AI-powered issue triage with learning integration and beautiful output"""
        await self._initialize_services()

        try:
            self.print_header(f"🔍 AI-Powered Issue Triage", "cyan")

            if project:
                self.print_info(f"Analyzing issues for project: {project}")
            else:
                self.print_info("Analyzing issues across all accessible repositories")

            # Get and analyze issues through service layer
            self.print_subheader("Fetching Issues", "blue")
            issues = await self.github_agent.get_open_issues(project=project, limit=limit)

            if not issues:
                self.print_warning("No open issues found")
                return CommandResult(success=True, message="No issues to triage")

            self.print_success(f"Retrieved {len(issues)} open issues")

            # Classify and prioritize issues
            self.print_subheader("Analyzing Priority and Classification", "blue")

            high_priority = []
            medium_priority = []
            low_priority = []

            for issue in issues:
                # Use service layer for classification
                classification = await self.issue_classifier.classify_issue(issue)
                priority = self._determine_priority(issue, classification)

                # Learn from triage decisions for future improvement
                await self._learn_triage_pattern(issue, priority, classification)

                # Categorize by priority
                issue_data = {
                    'issue': issue,
                    'classification': classification,
                    'priority': priority
                }

                if priority >= 0.8:
                    high_priority.append(issue_data)
                elif priority >= 0.5:
                    medium_priority.append(issue_data)
                else:
                    low_priority.append(issue_data)

            # Display results with beautiful formatting
            self._display_triage_results(high_priority, medium_priority, low_priority)

            return CommandResult(
                success=True,
                message=f"Triaged {len(issues)} issues",
                data={
                    'high_priority': len(high_priority),
                    'medium_priority': len(medium_priority),
                    'low_priority': len(low_priority)
                }
            )

        except Exception as e:
            error_message = f"Failed to triage issues: {str(e)}"
            self.print_error(error_message)
            logger.error("Issue triage failed", error=str(e), project=project)

            return CommandResult(
                success=False,
                message=error_message,
                error=str(e)
            )

    def _determine_priority(self, issue: Dict[str, Any], classification: Dict[str, Any]) -> float:
        """Determine issue priority based on multiple factors"""
        priority_factors = []

        # Label-based priority
        labels = [label['name'].lower() for label in issue.get('labels', [])]
        if any(label in ['critical', 'urgent', 'blocker'] for label in labels):
            priority_factors.append(0.9)
        elif any(label in ['high', 'important'] for label in labels):
            priority_factors.append(0.7)
        elif any(label in ['medium'] for label in labels):
            priority_factors.append(0.5)
        else:
            priority_factors.append(0.3)

        # Classification-based priority
        if classification.get('category') == 'bug':
            priority_factors.append(0.8)
        elif classification.get('category') == 'feature':
            priority_factors.append(0.5)
        elif classification.get('category') == 'enhancement':
            priority_factors.append(0.4)
        else:
            priority_factors.append(0.3)

        # Age-based priority (older issues get slightly higher priority)
        from datetime import datetime, timezone
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        age_days = (datetime.now(timezone.utc) - created_at).days
        age_factor = min(age_days / 30.0 * 0.2, 0.2)  # Max 0.2 boost for age
        priority_factors.append(age_factor)

        # Comment activity factor
        comment_count = issue.get('comments', 0)
        activity_factor = min(comment_count / 10.0 * 0.1, 0.1)  # Max 0.1 boost for activity
        priority_factors.append(activity_factor)

        return min(sum(priority_factors) / len(priority_factors), 1.0)

    async def _learn_triage_pattern(self, issue: Dict[str, Any], priority: float, classification: Dict[str, Any]):
        """Learn from triage decisions to improve future classifications"""
        try:
            learning_data = {
                'issue_title': issue['title'],
                'issue_body': issue.get('body', ''),
                'labels': [label['name'] for label in issue.get('labels', [])],
                'priority': priority,
                'classification': classification,
                'timestamp': datetime.now().isoformat()
            }

            await self.learning_system.record_triage_decision(learning_data)

        except Exception as e:
            logger.warning("Failed to record triage learning data", error=str(e))

    def _display_triage_results(self, high_priority: List[Dict], medium_priority: List[Dict], low_priority: List[Dict]):
        """Display triage results with beautiful formatting"""

        # High Priority Issues
        if high_priority:
            self.print_header("🚨 HIGH PRIORITY ISSUES", "red")
            for item in high_priority:
                issue = item['issue']
                classification = item['classification']
                self._display_issue_summary(issue, classification, "red")

        # Medium Priority Issues
        if medium_priority:
            self.print_header("⚠️  MEDIUM PRIORITY ISSUES", "yellow")
            for item in medium_priority:
                issue = item['issue']
                classification = item['classification']
                self._display_issue_summary(issue, classification, "yellow")

        # Low Priority Issues
        if low_priority:
            self.print_header("📝 LOW PRIORITY ISSUES", "green")
            for item in low_priority:
                issue = item['issue']
                classification = item['classification']
                self._display_issue_summary(issue, classification, "green")

        # Summary
        total = len(high_priority) + len(medium_priority) + len(low_priority)
        self.print_header("📊 TRIAGE SUMMARY", "cyan")
        self.print_info(f"High Priority: {len(high_priority)} issues", 1)
        self.print_info(f"Medium Priority: {len(medium_priority)} issues", 1)
        self.print_info(f"Low Priority: {len(low_priority)} issues", 1)
        self.print_info(f"Total Analyzed: {total} issues", 1)

    def _display_issue_summary(self, issue: Dict[str, Any], classification: Dict[str, Any], color: str):
        """Display individual issue summary with consistent formatting"""
        color_code = self.COLORS.get(color, self.COLORS["blue"])
        bold = self.COLORS["bold"]
        reset = self.COLORS["reset"]
        gray = self.COLORS["gray"]

        # Issue title and number
        print(f"{bold}{color_code}#{issue['number']}: {issue['title']}{reset}")

        # Classification and labels
        category = classification.get('category', 'unknown')
        confidence = classification.get('confidence', 0.0)
        print(f"  {gray}Category: {category} (confidence: {confidence:.2f}){reset}")

        if issue.get('labels'):
            labels = ', '.join([label['name'] for label in issue['labels']])
            print(f"  {gray}Labels: {labels}{reset}")

        # Issue URL for reference
        print(f"  {gray}URL: {issue['html_url']}{reset}")
        print()

@dataclass
class CommandResult:
    """Result of CLI command execution"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ServiceLocator:
    """Service locator for CLI command dependencies"""

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._initializers: Dict[str, Callable] = {}

    def register_service(self, name: str, initializer: Callable):
        """Register service initializer"""
        self._initializers[name] = initializer

    async def get_service(self, name: str) -> Any:
        """Get service instance, initializing if needed"""
        if name not in self._services:
            if name not in self._initializers:
                raise ValueError(f"Service '{name}' not registered")

            self._services[name] = await self._initializers[name]()

        return self._services[name]
```

### Example (CLI Error Handling and User Guidance)

```python
class CLIErrorHandler:
    """Centralized error handling for CLI commands"""

    def __init__(self):
        self.colors = CLICommand.COLORS

    def handle_service_error(self, error: Exception, service_name: str) -> str:
        """Handle service-layer errors with user-friendly messages"""

        error_mappings = {
            'GitHubAuthError': f"GitHub authentication failed. Please check your GITHUB_TOKEN environment variable.",
            'GitHubRateLimitError': f"GitHub API rate limit exceeded. Please wait before retrying.",
            'NetworkError': f"Network connection failed. Please check your internet connection.",
            'ConfigurationError': f"Configuration error in {service_name}. Please check your settings."
        }

        error_type = type(error).__name__
        user_message = error_mappings.get(error_type, f"An error occurred in {service_name}: {str(error)}")

        return user_message

    def print_actionable_error(self, error: Exception, service_name: str, suggested_actions: List[str]):
        """Print error with actionable guidance"""
        red = self.colors["red"]
        yellow = self.colors["yellow"]
        bold = self.colors["bold"]
        reset = self.colors["reset"]

        # Error message
        user_message = self.handle_service_error(error, service_name)
        print(f"{bold}{red}❌ {user_message}{reset}")

        # Suggested actions
        if suggested_actions:
            print(f"\n{bold}{yellow}💡 Suggested Actions:{reset}")
            for i, action in enumerate(suggested_actions, 1):
                print(f"  {yellow}{i}.{reset} {action}")

        print()  # Add spacing

class CLIIntegrationManager:
    """Main manager for CLI integration with service architecture"""

    def __init__(self):
        self.service_locator = ServiceLocator()
        self.error_handler = CLIErrorHandler()
        self.commands: Dict[str, CLICommand] = {}
        self._setup_services()

    def _setup_services(self):
        """Setup service initializers"""
        # Register service initializers
        self.service_locator.register_service('github_agent', self._init_github_agent)
        self.service_locator.register_service('learning_system', self._init_learning_system)
        self.service_locator.register_service('issue_classifier', self._init_issue_classifier)

    async def _init_github_agent(self):
        """Initialize GitHub agent service"""
        from services.integrations.github.github_agent import GitHubAgent
        return GitHubAgent()

    async def _init_learning_system(self):
        """Initialize learning system service"""
        from services.learning.learning_system import LearningSystem
        return LearningSystem()

    async def _init_issue_classifier(self):
        """Initialize issue classifier service"""
        from services.classification.issue_classifier import IssueClassifier
        return IssueClassifier()

    def register_command(self, name: str, command_class: type):
        """Register CLI command"""
        self.commands[name] = command_class(self.service_locator)

    async def execute_command(self, command_name: str, **kwargs) -> CommandResult:
        """Execute registered command with error handling"""
        if command_name not in self.commands:
            return CommandResult(
                success=False,
                message=f"Unknown command: {command_name}",
                error=f"Command '{command_name}' not found"
            )

        try:
            command = self.commands[command_name]
            return await command.execute(**kwargs)

        except Exception as e:
            # Handle error with user-friendly messages and guidance
            suggested_actions = self._get_suggested_actions(e, command_name)
            self.error_handler.print_actionable_error(e, command_name, suggested_actions)

            return CommandResult(
                success=False,
                message=f"Command '{command_name}' failed",
                error=str(e)
            )

    def _get_suggested_actions(self, error: Exception, command_name: str) -> List[str]:
        """Get suggested actions based on error type and command"""
        error_type = type(error).__name__

        common_actions = {
            'GitHubAuthError': [
                "Set your GITHUB_TOKEN environment variable",
                "Verify your GitHub token has the required permissions",
                "Check if your token has expired"
            ],
            'NetworkError': [
                "Check your internet connection",
                "Verify GitHub.com is accessible",
                "Try again in a few moments"
            ],
            'ConfigurationError': [
                "Review your configuration settings",
                "Check environment variables are set correctly",
                "Consult the documentation for setup instructions"
            ]
        }

        return common_actions.get(error_type, [
            f"Check the logs for more detailed error information",
            f"Verify the '{command_name}' command is properly configured",
            "Contact support if the issue persists"
        ])

# Usage example
async def main():
    """Example CLI application with service integration"""
    cli_manager = CLIIntegrationManager()

    # Register commands
    cli_manager.register_command('issues', IssuesCommand)

    # Execute command
    result = await cli_manager.execute_command('issues', project='piper-morgan', limit=15)

    if result.success:
        print(f"Command completed successfully: {result.message}")
    else:
        print(f"Command failed: {result.message}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage Guidelines

### CLI Design Best Practices

- **Consistent Color Coding**: Use standardized color schemes for different message types (errors=red, warnings=yellow, success=green, info=blue)
- **Clear Visual Hierarchy**: Implement headers, subheaders, and proper spacing for easy scanning
- **Progressive Disclosure**: Show summary information first, with options to drill down into details
- **Beautiful Formatting**: Use separators, icons, and consistent styling for professional appearance
- **Responsive Design**: Adapt output formatting based on terminal width and capabilities

### Service Integration Best Practices

- **Clean Separation**: Maintain clear boundaries between CLI presentation logic and business logic
- **Service Layer Access**: Always access business functionality through service layers, never directly
- **Lazy Initialization**: Initialize services only when needed to improve startup performance
- **Dependency Injection**: Use service locator or dependency injection patterns for testability
- **Error Translation**: Convert service-layer exceptions to user-friendly CLI messages

### Learning System Integration Best Practices

- **Implicit Learning**: Integrate learning systems transparently without disrupting user workflow
- **Pattern Recognition**: Learn from user interactions and command usage patterns
- **Adaptive Behavior**: Adjust command behavior based on learned preferences and patterns
- **Privacy Awareness**: Only learn from interactions that users consent to tracking
- **Feedback Loops**: Provide mechanisms for users to correct or guide learning behavior

### Output and Interaction Best Practices

- **Machine-Parseable Options**: Support JSON or structured output for scripting scenarios
- **Interactive Features**: Provide interactive prompts and confirmations where appropriate
- **Progress Indicators**: Show progress for long-running operations
- **Comprehensive Help**: Include detailed help text with examples and common usage patterns
- **Accessibility**: Ensure output is accessible to screen readers and different terminal configurations

### Anti-Patterns to Avoid

- **Business Logic in CLI**: Implementing business logic directly in CLI command code instead of delegating to services
- **Inconsistent Formatting**: Using different color schemes, spacing, or formatting across commands
- **Poor Error Messages**: Providing technical error messages without actionable guidance for users
- **Direct Data Access**: Bypassing service layers to access data stores or external APIs directly
- **Missing Learning Integration**: Failing to integrate with learning systems for intelligent behavior adaptation
- **Blocking Operations**: Running long operations without progress indicators or async handling

## Benefits

- **Seamless Service Integration**: Connects CLI interfaces cleanly with underlying service architectures
- **Enhanced User Experience**: Provides beautiful, consistent formatting and interactive features
- **Intelligent Behavior**: Integrates with learning systems for adaptive and intelligent command behavior
- **Maintainable Architecture**: Maintains clear separation between presentation and business logic
- **Comprehensive Error Handling**: Offers user-friendly error messages with actionable guidance
- **Flexible Usage Patterns**: Supports both interactive use and scripted automation scenarios

## Trade-offs

- **Additional Complexity**: Requires sophisticated service integration and formatting infrastructure
- **Development Overhead**: More complex than simple script-based CLI implementations
- **Dependency Management**: Requires careful management of service dependencies and initialization
- **Performance Considerations**: Service layer integration may add latency compared to direct implementations
- **Learning System Complexity**: Integration with learning systems adds architectural complexity
- **Testing Challenges**: Requires comprehensive testing of both CLI formatting and service integration

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Service layer architecture for CLI integration
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain service integration
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Error handling in CLI operations
- [Pattern-019: LLM Placeholder Instruction](pattern-019-llm-placeholder-instruction.md) - Learning system integration
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Service locator and command factory patterns

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 27 "CLI Integration Pattern" - comprehensive implementation with beautiful formatting and service integration
- **From `PATTERN-INDEX.md`**: No direct equivalent - this is a presentation layer pattern
- **From CLI implementations**: Existing command implementations in `cli/commands/` directory
- **Consolidation Strategy**: Expanded pattern-catalog.md content with comprehensive service integration, error handling, learning system integration, and user experience enhancements

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for service layer implementation and CLI command infrastructure
- **Agent B (Cursor)**: Responsible for CLI formatting patterns, user experience design, and integration documentation
- **Integration Points**: CLI command implementations, service locators, error handling systems, and learning system integrations

## References

- Original catalog: `docs/architecture/pattern-catalog.md#27-cli-integration-pattern`
- CLI commands: `cli/commands/`
- Service integration: `services/`
- Error handling: `services/api/errors.py`
- Learning systems: `services/learning/`

_Last updated: September 15, 2025_
