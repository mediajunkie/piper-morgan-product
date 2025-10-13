"""
Issues CLI Command - Issue Intelligence Integration

Provides immediate value through issue management commands:
- piper issues triage: Quick issue triage and prioritization
- piper issues status: Current issue status overview
- piper issues patterns: Discovered issue patterns and insights

Built on: Learning Loop + Cross-Feature Knowledge + GitHub Integration
Performance: Real-time issue intelligence with pattern learning
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.config.github_config import GitHubConfiguration
from services.configuration.piper_config_loader import PiperConfigLoader
from services.domain.github_domain_service import GitHubDomainService
from services.domain.pm_number_manager import PMNumberManager
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.learning import get_cross_feature_service, get_learning_loop


class IssuesCommand:
    """Issues CLI Command with beautiful formatting and learning integration"""

    # Color codes for beautiful output (matching standup command)
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m",
    }

    def __init__(self):
        """Initialize the issues command with required services"""
        self.github_domain_service = GitHubDomainService()
        self.learning_loop = None  # Will be initialized when needed
        self.cross_feature_service = None  # Will be initialized when needed

    async def _initialize_services(self):
        """Initialize learning services when needed"""
        if self.learning_loop is None:
            self.learning_loop = await get_learning_loop()

        # Note: cross_feature_service requires knowledge service instances
        # For now, we'll work with the learning loop directly

    def print_colored(self, text: str, color: str = "reset", bold: bool = False) -> None:
        """Print colored and optionally bold text"""
        color_code = self.COLORS.get(color, self.COLORS["reset"])
        bold_code = self.COLORS["bold"] if bold else ""
        print(f"{bold_code}{color_code}{text}{self.COLORS['reset']}")

    def print_header(self, title: str) -> None:
        """Print a beautiful header"""
        print()
        self.print_colored("=" * 60, "cyan", bold=True)
        self.print_colored(f"  {title}", "cyan", bold=True)
        self.print_colored("=" * 60, "cyan", bold=True)
        print()

    def print_section(self, title: str, color: str = "blue") -> None:
        """Print a section header"""
        print()
        self.print_colored(f"📋 {title}", color, bold=True)
        self.print_colored("-" * 40, color)

    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.print_colored(f"✅ {message}", "green")

    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.print_colored(f"ℹ️  {message}", "blue")

    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.print_colored(f"⚠️  {message}", "yellow")

    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.print_colored(f"❌ {message}", "red")

    async def triage_issues(self, project: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Quick issue triage and prioritization

        Args:
            project: Optional project filter
            limit: Maximum number of issues to analyze

        Returns:
            Dictionary with triage results
        """
        try:
            await self._initialize_services()

            self.print_header("🔍 Issue Triage & Prioritization")

            # Get open issues from GitHub
            issues = await self.github_domain_service.get_open_issues(project, limit)

            if not issues:
                self.print_warning("No open issues found")
                return {"issues_analyzed": 0, "triage_complete": True}

            self.print_section(f"Analyzing {len(issues)} Open Issues", "yellow")

            triage_results = []
            high_priority = []
            medium_priority = []
            low_priority = []

            for issue in issues:
                # Analyze issue for triage
                priority = self._determine_priority(issue)
                triage_note = self._generate_triage_note(issue, priority)

                triage_result = {
                    "issue_number": issue.get("number"),
                    "title": issue.get("title"),
                    "priority": priority,
                    "triage_note": triage_note,
                    "labels": issue.get("labels", []),
                    "assignee": issue.get("assignee"),
                    "created_at": issue.get("created_at"),
                }

                triage_results.append(triage_result)

                # Categorize by priority
                if priority == "high":
                    high_priority.append(triage_result)
                elif priority == "medium":
                    medium_priority.append(triage_result)
                else:
                    low_priority.append(triage_result)

                # Learn from this triage decision
                await self._learn_triage_pattern(issue, priority, triage_note)

            # Display triage results
            self._display_triage_results(high_priority, medium_priority, low_priority)

            # Summary with actionable insights
            self.print_section("Triage Summary & Action Items", "green")
            self.print_success(f"High Priority: {len(high_priority)} issues")
            self.print_info(f"Medium Priority: {len(medium_priority)} issues")
            self.print_info(f"Low Priority: {len(low_priority)} issues")

            # Actionable guidance
            if high_priority:
                self.print_section("🚨 Immediate Actions Required", "red")
                self.print_colored("• Review high-priority issues within 24 hours", "red")
                self.print_colored("• Assign team members to critical issues", "red")
                self.print_colored("• Update stakeholders on blocker status", "red")

            if medium_priority:
                self.print_section("⚡ Sprint Planning", "yellow")
                self.print_colored("• Include medium-priority issues in next sprint", "yellow")
                self.print_colored("• Estimate effort and assign resources", "yellow")
                self.print_colored("• Set clear acceptance criteria", "yellow")

            if low_priority:
                self.print_section("📝 Backlog Management", "blue")
                self.print_colored("• Review low-priority issues quarterly", "blue")
                self.print_colored("• Consider batching similar improvements", "blue")
                self.print_colored("• Archive outdated or superseded issues", "blue")

            # Learning insights
            if self.learning_loop:
                await self._display_triage_learning_insights()

            return {
                "issues_analyzed": len(issues),
                "high_priority": len(high_priority),
                "medium_priority": len(medium_priority),
                "low_priority": len(low_priority),
                "triage_complete": True,
                "triage_results": triage_results,
            }

        except Exception as e:
            self.print_error(f"Issue triage failed: {e}")
            return {"error": str(e), "triage_complete": False}

    def _determine_priority(self, issue: Dict[str, Any]) -> str:
        """Determine issue priority based on labels, title, and content"""
        title = issue.get("title", "").lower()
        labels = [label.get("name", "").lower() for label in issue.get("labels", [])]
        body = issue.get("body", "").lower()

        # High priority indicators
        high_indicators = [
            "urgent",
            "critical",
            "blocker",
            "p0",
            "high",
            "bug",
            "error",
            "fail",
            "broken",
            "crash",
            "security",
            "vulnerability",
            "production",
            "live",
        ]

        # Medium priority indicators
        medium_indicators = [
            "important",
            "p1",
            "medium",
            "enhancement",
            "feature",
            "improvement",
            "performance",
            "optimization",
            "refactor",
        ]

        # Check for high priority
        for indicator in high_indicators:
            if (
                indicator in title
                or any(indicator in label for label in labels)
                or indicator in body
            ):
                return "high"

        # Check for medium priority
        for indicator in medium_indicators:
            if (
                indicator in title
                or any(indicator in label for label in labels)
                or indicator in body
            ):
                return "medium"

        # Default to low priority
        return "low"

    def _generate_triage_note(self, issue: Dict[str, Any], priority: str) -> str:
        """Generate a triage note for the issue"""
        title = issue.get("title", "")
        labels = [label.get("name") for label in issue.get("labels", [])]

        if priority == "high":
            return f"🚨 High priority: {title} - Requires immediate attention"
        elif priority == "medium":
            return f"⚡ Medium priority: {title} - Plan for next sprint"
        else:
            return f"📝 Low priority: {title} - Backlog candidate"

    def _display_triage_results(
        self, high_priority: List[Dict], medium_priority: List[Dict], low_priority: List[Dict]
    ) -> None:
        """Display triage results in organized sections"""

        # High Priority Issues
        if high_priority:
            self.print_section("🚨 High Priority Issues", "red")
            for issue in high_priority:
                self.print_colored(f"#{issue['issue_number']}: {issue['title']}", "red")
                self.print_colored(f"   {issue['triage_note']}", "gray")
                if issue["assignee"]:
                    self.print_colored(
                        f"   Assignee: {issue['assignee'].get('login', 'Unknown')}", "gray"
                    )
                print()

        # Medium Priority Issues
        if medium_priority:
            self.print_section("⚡ Medium Priority Issues", "yellow")
            for issue in medium_priority:
                self.print_colored(f"#{issue['issue_number']}: {issue['title']}", "yellow")
                self.print_colored(f"   {issue['triage_note']}", "gray")
                print()

        # Low Priority Issues
        if low_priority:
            self.print_section("📝 Low Priority Issues", "blue")
            for issue in low_priority:
                self.print_colored(f"#{issue['issue_number']}: {issue['title']}", "blue")
                self.print_colored(f"   {issue['triage_note']}", "gray")
                print()

    async def _learn_triage_pattern(
        self, issue: Dict[str, Any], priority: str, triage_note: str
    ) -> None:
        """Learn from triage decisions to improve future triage"""
        try:
            if self.learning_loop:
                # Create pattern data for triage decision
                pattern_data = {
                    "issue_title_keywords": self._extract_keywords(issue.get("title", "")),
                    "issue_labels": [label.get("name") for label in issue.get("labels", [])],
                    "priority_assigned": priority,
                    "triage_note": triage_note,
                    "pattern_category": "triage_decision",
                }

                # Learn the triage pattern
                await self.learning_loop.learn_pattern(
                    pattern_type="workflow_pattern",
                    source_feature="issue_intelligence",
                    pattern_data=pattern_data,
                    initial_confidence=0.7,
                    metadata={"category": "triage", "priority": priority},
                )

        except Exception as e:
            # Don't fail triage if learning fails
            pass

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Simple keyword extraction - could be enhanced with NLP
        words = text.lower().split()
        # Filter out common words and short words
        keywords = [
            word
            for word in words
            if len(word) > 3
            and word not in ["the", "and", "for", "with", "this", "that", "have", "will", "from"]
        ]
        return keywords[:5]  # Limit to top 5 keywords

    async def _display_triage_learning_insights(self) -> None:
        """Display learning insights specific to triage"""
        try:
            stats = await self.learning_loop.get_learning_stats()

            if stats["total_patterns"] > 0:
                self.print_section("🧠 Triage Learning Insights", "magenta")

                # Get triage-specific patterns
                triage_patterns = await self.learning_loop.get_patterns_for_feature(
                    "issue_intelligence", pattern_type="workflow_pattern", min_confidence=0.5
                )

                if triage_patterns:
                    self.print_info("Recent Triage Patterns Learned:")
                    for pattern in triage_patterns[:3]:  # Show top 3
                        if pattern.metadata.get("category") == "triage":
                            confidence_color = "green" if pattern.confidence > 0.7 else "yellow"
                            self.print_colored(
                                f"  • {pattern.metadata.get('priority', 'Unknown')} priority pattern",
                                confidence_color,
                            )
                            self.print_colored(
                                f"    Confidence: {pattern.confidence:.1f} | Usage: {pattern.usage_count}x",
                                "gray",
                            )

                # Overall learning stats
                self.print_info(f"Total Patterns: {stats['total_patterns']}")
                self.print_info(f"Average Confidence: {stats['average_confidence']:.1f}")

        except Exception as e:
            # Don't fail triage if learning insights fail
            pass

    async def get_issue_status(self, project: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current issue status overview

        Args:
            project: Optional project filter

        Returns:
            Dictionary with issue status information
        """
        try:
            await self._initialize_services()

            self.print_header("📊 Issue Status Overview")

            # Get issue statistics
            open_issues = await self.github_domain_service.get_open_issues(project)
            # Note: closed_issues method may need to be added to domain service if not present
            closed_issues = []  # Temporary placeholder - needs domain service method

            # Calculate statistics
            total_open = len(open_issues)
            total_closed = len(closed_issues)
            total_issues = total_open + total_closed

            # Get recent activity
            recent_issues = await self.github_domain_service.get_recent_issues(
                10
            )  # Limit of 10 recent issues

            # Display status with actionable insights
            self.print_section("Current Status", "blue")
            self.print_info(f"Open Issues: {total_open}")
            self.print_info(f"Closed Issues: {total_closed}")
            self.print_info(f"Total Issues: {total_issues}")

            if total_issues > 0:
                completion_rate = (total_closed / total_issues) * 100
                self.print_info(f"Completion Rate: {completion_rate:.1f}%")

                # Status-based recommendations
                if completion_rate < 30:
                    self.print_warning("Low completion rate - consider issue review and cleanup")
                elif completion_rate > 80:
                    self.print_success("High completion rate - excellent issue management!")
                else:
                    self.print_info("Moderate completion rate - steady progress")

            # Recent activity with insights
            if recent_issues:
                self.print_section("Recent Activity (Last 7 Days)", "green")
                closed_count = sum(1 for issue in recent_issues if issue.get("state") == "closed")
                opened_count = len(recent_issues) - closed_count

                self.print_info(f"New Issues: {opened_count}")
                self.print_info(f"Resolved Issues: {closed_count}")

                # Show top recent issues
                for issue in recent_issues[:5]:  # Show top 5
                    status = "🟢 Closed" if issue.get("state") == "closed" else "🟡 Open"
                    self.print_colored(
                        f"{status} #{issue.get('number')}: {issue.get('title')}", "white"
                    )

                    # Add context for recent issues
                    if issue.get("state") == "closed":
                        closed_at = issue.get("closed_at", "")
                        if closed_at:
                            self.print_colored(f"   Resolved: {closed_at[:10]}", "gray")

            # Learning insights
            if self.learning_loop:
                await self._display_learning_insights()

            # Actionable recommendations
            await self._display_status_recommendations(total_open, total_closed, recent_issues)

            return {
                "open_issues": total_open,
                "closed_issues": total_closed,
                "total_issues": total_issues,
                "completion_rate": (total_closed / total_issues) * 100 if total_issues > 0 else 0,
                "recent_activity": len(recent_issues),
            }

        except Exception as e:
            self.print_error(f"Failed to get issue status: {e}")
            return {"error": str(e)}

    async def _display_learning_insights(self) -> None:
        """Display insights from the learning loop"""
        try:
            stats = await self.learning_loop.get_learning_stats()

            if stats["total_patterns"] > 0:
                self.print_section("🧠 Learning Insights", "magenta")
                self.print_info(f"Total Patterns Learned: {stats['total_patterns']}")
                self.print_info(f"Average Confidence: {stats['average_confidence']:.1f}")

                # Show pattern distribution
                if stats["feature_distribution"]:
                    self.print_info("Pattern Distribution:")
                    for feature, count in stats["feature_distribution"].items():
                        self.print_colored(f"  {feature}: {count} patterns", "gray")

        except Exception as e:
            # Don't fail status if learning insights fail
            pass

    async def _display_status_recommendations(
        self, open_count: int, closed_count: int, recent_issues: List[Dict]
    ) -> None:
        """Display actionable recommendations based on status"""
        self.print_section("💡 Recommendations", "cyan")

        if open_count > 20:
            self.print_warning("High number of open issues - consider triage session")
            self.print_colored("  • Run 'piper issues triage' to prioritize", "gray")
            self.print_colored("  • Review and close outdated issues", "gray")
            self.print_colored("  • Batch similar issues for efficiency", "gray")

        if open_count < 5:
            self.print_success("Low number of open issues - great issue management!")
            self.print_colored("  • Focus on quality over quantity", "gray")
            self.print_colored("  • Consider proactive improvements", "gray")

        if recent_issues:
            recent_closed = sum(1 for issue in recent_issues if issue.get("state") == "closed")
            if recent_closed == 0:
                self.print_warning("No recent issue resolution - check for blockers")
                self.print_colored("  • Review high-priority open issues", "gray")
                self.print_colored("  • Check for resource constraints", "gray")
            elif recent_closed > 5:
                self.print_success("High recent resolution rate - excellent progress!")
                self.print_colored("  • Maintain current momentum", "gray")
                self.print_colored("  • Document successful patterns", "gray")

    async def discover_patterns(self, feature: Optional[str] = None) -> Dict[str, Any]:
        """
        Discover issue patterns and insights

        Args:
            feature: Optional feature filter (issue_intelligence, morning_standup)

        Returns:
            Dictionary with discovered patterns
        """
        try:
            await self._initialize_services()

            self.print_header("🔍 Issue Pattern Discovery")

            if not self.learning_loop:
                self.print_warning("Learning loop not available")
                return {"patterns_discovered": 0}

            # Get patterns for the specified feature or all features
            if feature:
                patterns = await self.learning_loop.get_patterns_for_feature(feature)
                self.print_section(f"Patterns for {feature}", "blue")
            else:
                # Get patterns from all features
                issue_patterns = await self.learning_loop.get_patterns_for_feature(
                    "issue_intelligence"
                )
                standup_patterns = await self.learning_loop.get_patterns_for_feature(
                    "morning_standup"
                )
                patterns = issue_patterns + standup_patterns
                self.print_section("Patterns from All Features", "blue")

            if not patterns:
                self.print_info("No patterns discovered yet")
                self.print_section("🚀 Getting Started", "green")
                self.print_colored("• Run 'piper issues triage' to start learning", "gray")
                self.print_colored(
                    "• Use 'piper standup' to build Morning Standup patterns", "gray"
                )
                self.print_colored("• Patterns will appear here as you use the system", "gray")
                return {"patterns_discovered": 0}

            # Group patterns by type
            pattern_groups = {}
            for pattern in patterns:
                pattern_type = pattern.pattern_type.value
                if pattern_type not in pattern_groups:
                    pattern_groups[pattern_type] = []
                pattern_groups[pattern_type].append(pattern)

            # Display patterns by type with enhanced UX
            total_patterns = 0
            for pattern_type, type_patterns in pattern_groups.items():
                self.print_section(f"{pattern_type.replace('_', ' ').title()} Patterns", "yellow")

                for pattern in type_patterns:
                    confidence_color = (
                        "green"
                        if pattern.confidence > 0.7
                        else "yellow" if pattern.confidence > 0.4 else "red"
                    )
                    self.print_colored(f"📊 {pattern.pattern_id}", confidence_color)
                    self.print_colored(f"   Source: {pattern.source_feature}", "gray")
                    self.print_colored(f"   Confidence: {pattern.confidence:.1f}", confidence_color)
                    self.print_colored(f"   Usage: {pattern.usage_count} times", "gray")

                    if pattern.metadata:
                        metadata_str = ", ".join(
                            [f"{k}: {v}" for k, v in pattern.metadata.items() if k != "category"]
                        )
                        if metadata_str:
                            self.print_colored(f"   Metadata: {metadata_str}", "gray")

                    # Add actionable insights for each pattern
                    if pattern.confidence > 0.8:
                        self.print_colored(
                            f"   💡 High confidence - ready for production use", "green"
                        )
                    elif pattern.confidence > 0.5:
                        self.print_colored(
                            f"   ⚠️  Medium confidence - monitor and validate", "yellow"
                        )
                    else:
                        self.print_colored(
                            f"   🔬 Low confidence - experimental, use with caution", "red"
                        )

                    print()
                    total_patterns += 1

            # Enhanced summary with insights
            self.print_section("Pattern Discovery Summary", "green")
            self.print_success(f"Total Patterns: {total_patterns}")
            self.print_info(f"Pattern Types: {len(pattern_groups)}")

            # Pattern quality insights
            high_confidence = sum(1 for p in patterns if p.confidence > 0.7)
            if high_confidence > 0:
                self.print_success(f"High Confidence Patterns: {high_confidence}")

            # Cross-feature insights
            if not feature:
                issue_count = len([p for p in patterns if p.source_feature == "issue_intelligence"])
                standup_count = len([p for p in patterns if p.source_feature == "morning_standup"])
                self.print_info(f"Issue Intelligence Patterns: {issue_count}")
                self.print_info(f"Morning Standup Patterns: {standup_count}")

            # Actionable recommendations
            await self._display_pattern_recommendations(patterns, pattern_groups)

            return {
                "patterns_discovered": total_patterns,
                "pattern_types": len(pattern_groups),
                "pattern_groups": {k: len(v) for k, v in pattern_groups.items()},
            }

        except Exception as e:
            self.print_error(f"Pattern discovery failed: {e}")
            return {"error": str(e)}

    async def _display_pattern_recommendations(self, patterns: List, pattern_groups: Dict) -> None:
        """Display actionable recommendations based on discovered patterns"""
        self.print_section("💡 Pattern-Based Recommendations", "cyan")

        # High confidence pattern recommendations
        high_confidence = [p for p in patterns if p.confidence > 0.7]
        if high_confidence:
            self.print_success("High-Confidence Patterns Available:")
            self.print_colored("  • These patterns are ready for production use", "gray")
            self.print_colored("  • Consider documenting them as best practices", "gray")
            self.print_colored("  • Share successful patterns with the team", "gray")

        # Low confidence pattern recommendations
        low_confidence = [p for p in patterns if p.confidence < 0.4]
        if low_confidence:
            self.print_warning("Low-Confidence Patterns Need Attention:")
            self.print_colored("  • Review and validate these patterns", "gray")
            self.print_colored("  • Provide feedback to improve confidence", "gray")
            self.print_colored("  • Consider retiring unreliable patterns", "gray")

        # Cross-feature learning opportunities
        if len(pattern_groups) > 1:
            self.print_info("Cross-Feature Learning Opportunities:")
            self.print_colored(
                "  • Look for patterns that could be shared between features", "gray"
            )
            self.print_colored("  • Identify common workflows for standardization", "gray")
            self.print_colored("  • Consider creating shared pattern libraries", "gray")

        # Usage-based recommendations
        high_usage = [p for p in patterns if p.usage_count > 5]
        if high_usage:
            self.print_success("Frequently Used Patterns:")
            self.print_colored("  • These patterns are well-established", "gray")
            self.print_colored("  • Consider optimizing for performance", "gray")
            self.print_colored("  • Document common use cases", "gray")

    async def execute(self, command: str, **kwargs) -> None:
        """Execute the specified issues command"""
        try:
            if command == "triage":
                await self.triage_issues(**kwargs)
            elif command == "status":
                await self.get_issue_status(**kwargs)
            elif command == "patterns":
                await self.discover_patterns(**kwargs)
            else:
                self.print_error(f"Unknown command: {command}")
                self.print_info("Available commands: triage, status, patterns")

        except Exception as e:
            self.print_error(f"Issues command failed: {e}")
            sys.exit(1)


# Click command group for PM number management
@click.group()
def issues():
    """Issue management commands with PM number verification."""
    pass


@issues.command()
@click.option("--title", required=True, help="Issue title")
@click.option("--body", default="", help="Issue description")
@click.option("--labels", help="Comma-separated labels")
@click.option("--dry-run", is_flag=True, help="Show what would be created")
def create(title: str, body: str, labels: str, dry_run: bool):
    """Create new issue with auto-assigned PM number"""
    click.echo(f"🚀 Creating issue: {title}")

    # Validate inputs
    if not title.strip():
        click.echo("❌ Error: Issue title cannot be empty")
        click.echo("💡 Please provide a meaningful title for the issue")
        return

    if len(title) > 200:
        click.echo("❌ Error: Issue title too long (max 200 characters)")
        click.echo(f"💡 Current length: {len(title)} characters")
        return

    # Parse labels
    label_list = []
    if labels:
        label_list = [label.strip() for label in labels.split(",") if label.strip()]
        if len(label_list) > 10:
            click.echo("❌ Error: Too many labels (max 10)")
            click.echo(f"💡 Current count: {len(label_list)} labels")
            return

    if dry_run:
        click.echo("🔍 DRY RUN - Would create:")
        click.echo(f"  Title: {title}")
        click.echo(f"  Body: {body or 'No description provided'}")
        click.echo(f"  Labels: {', '.join(label_list) if label_list else 'None'}")
        click.echo("  PM Number: PM-140 (next available)")
        click.echo("  GitHub Issue: Would be created via GitHubAgent")
        # Load GitHub configuration from user settings
        config_loader = PiperConfigLoader()
        github_config = config_loader.load_github_config()
        click.echo(f"  Repository: {github_config.default_repository}")
        return

    try:
        # Initialize services
        pm_manager = PMNumberManager()
        github_domain_service = GitHubDomainService()

        # Get next PM number
        next_pm_number = asyncio.run(pm_manager.get_next_available_pm_number())
        click.echo(f"📋 Generated PM number: {next_pm_number}")

        # Verify PM number is available
        validation = asyncio.run(pm_manager.validate_pm_number(next_pm_number))
        if not validation.is_valid:
            click.echo(f"❌ Error: PM number {next_pm_number} validation failed")
            for conflict in validation.conflicts:
                click.echo(f"   ⚠️  {conflict}")
            for suggestion in validation.suggestions:
                click.echo(f"   💡 {suggestion}")
            if validation.next_available:
                click.echo(f"   ➡️  Try using: {validation.next_available}")
            return

        # Load GitHub configuration from user settings and create issue
        config_loader = PiperConfigLoader()
        github_config = config_loader.load_github_config()
        repo_name = github_config.default_repository
        issue_body = f"{body}\n\n**PM Number**: {next_pm_number}"

        click.echo("🚀 Creating GitHub issue...")
        issue_data = asyncio.run(
            github_domain_service.create_issue(
                repo_name=repo_name, title=title, body=issue_body, labels=label_list
            )
        )

        # Add PM entry to tracking
        success = asyncio.run(
            pm_manager.reserve_pm_number(
                pm_number=next_pm_number, title=title, issue_number=issue_data["number"]
            )
        )

        if not success:
            click.echo("⚠️  Warning: GitHub issue created but failed to update CSV tracking")
            click.echo("💡 Please run 'issues sync' to synchronize tracking files")

        # Success message
        click.echo("✅ Issue created successfully!")
        click.echo(f"  PM Number: {next_pm_number}")
        click.echo(f"  GitHub Issue: #{issue_data['number']}")
        click.echo(f"  URL: {issue_data['url']}")
        click.echo(f"  Status: {issue_data['state']}")

    except Exception as e:
        click.echo(f"❌ Error creating issue: {e}")
        click.echo("💡 Common solutions:")
        click.echo("  - Check GitHub authentication: gh auth status")
        click.echo("  - Verify network connectivity")
        click.echo("  - Ensure repository access permissions")
        click.echo("  - Try again in a few moments")


@issues.command()
def verify():
    """Verify PM number consistency across all systems"""
    click.echo("🔍 Verifying PM number consistency...")

    try:
        # Check if CSV file exists and is readable
        csv_path = Path("docs/planning/pm-issues-status.csv")
        if not csv_path.exists():
            click.echo("❌ Error: PM issues CSV file not found")
            click.echo(f"💡 Expected location: {csv_path.absolute()}")
            click.echo("💡 Please ensure the file exists and is accessible")
            return

        if not csv_path.is_file():
            click.echo("❌ Error: PM issues CSV path is not a file")
            click.echo(f"💡 Path: {csv_path.absolute()}")
            return

        # Check if we can read the file
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    click.echo("❌ Error: PM issues CSV file is empty")
                    click.echo("💡 Please check if the file has been corrupted")
                    return
        except PermissionError:
            click.echo("❌ Error: Permission denied reading PM issues CSV")
            click.echo("💡 Please check file permissions")
            return
        except UnicodeDecodeError:
            click.echo("❌ Error: PM issues CSV file has invalid encoding")
            click.echo("💡 Please ensure the file is UTF-8 encoded")
            return

        # Initialize PM number manager
        pm_manager = PMNumberManager()

        # Run comprehensive verification
        click.echo("🔍 Checking PM number consistency...")
        verification_result = asyncio.run(pm_manager.verify_consistency())

        if verification_result["consistent"]:
            click.echo("✅ PM number consistency verified!")
            click.echo(f"  Total PM numbers: {verification_result['total_pm_numbers']}")
            click.echo(f"  GitHub issues checked: {verification_result['github_issues_checked']}")
            click.echo(f"  CSV entries verified: {verification_result['csv_entries_verified']}")
        else:
            click.echo("❌ PM number inconsistencies found!")
            click.echo(f"  Issues found: {len(verification_result['issues'])}")

            for issue in verification_result["issues"]:
                click.echo(f"  - {issue}")

            click.echo("\n💡 Suggested actions:")
            click.echo("  - Run 'issues sync' to synchronize systems")
            click.echo("  - Check GitHub issues for missing PM numbers")
            click.echo("  - Verify CSV file format and completeness")

        # Additional statistics
        if verification_result.get("duplicates_found", 0) > 0:
            click.echo(f"\n⚠️  Found {verification_result['duplicates_found']} duplicate PM numbers")

        if verification_result.get("github_only_count", 0) > 0:
            click.echo(
                f"⚠️  Found {verification_result['github_only_count']} PM numbers only in GitHub"
            )

        if verification_result.get("csv_only_count", 0) > 0:
            click.echo(f"⚠️  Found {verification_result['csv_only_count']} PM numbers only in CSV")

        if verification_result.get("missing_issue_numbers", 0) > 0:
            click.echo(
                f"⚠️  Found {verification_result['missing_issue_numbers']} CSV entries missing GitHub issue numbers"
            )

    except Exception as e:
        click.echo(f"❌ Error verifying PM numbers: {e}")
        click.echo("💡 Common solutions:")
        click.echo("  - Check file permissions and accessibility")
        click.echo("  - Verify network connectivity for GitHub access")
        click.echo("  - Ensure all tracking files are properly formatted")
        click.echo("  - Try running with --dry-run first to test")


@issues.command()
@click.option("--dry-run", is_flag=True, help="Show what would be synced")
def sync(dry_run: bool):
    """Synchronize PM numbers across all tracking systems"""
    if dry_run:
        click.echo("🔍 DRY RUN - Would synchronize:")
        click.echo("  GitHub issues ↔ CSV file")
        click.echo("  CSV file ↔ Backlog.md")
        click.echo("  Resolve any numbering conflicts")
        click.echo("  Update missing PM numbers")
        click.echo("  Fix duplicate PM numbers")
        return

    click.echo("🔄 Synchronizing PM numbers across systems...")

    try:
        # Check prerequisites
        csv_path = Path("docs/planning/pm-issues-status.csv")
        backlog_path = Path("docs/planning/backlog.md")

        # Verify CSV file
        if not csv_path.exists():
            click.echo("❌ Error: PM issues CSV file not found")
            click.echo(f"💡 Expected location: {csv_path.absolute()}")
            return

        # Verify backlog file
        if not backlog_path.exists():
            click.echo("❌ Error: Backlog file not found")
            click.echo(f"💡 Expected location: {backlog_path.absolute()}")
            return

        # Check GitHub authentication
        try:
            import subprocess

            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                click.echo("❌ Error: GitHub authentication required")
                click.echo("💡 Please run: gh auth login")
                return
        except (subprocess.TimeoutExpired, FileNotFoundError):
            click.echo("❌ Error: GitHub CLI not available or timeout")
            click.echo("💡 Please install GitHub CLI and authenticate")
            return

        # Initialize PM number manager
        pm_manager = PMNumberManager()

        # Run actual synchronization
        click.echo("🔄 Synchronizing PM numbers across systems...")
        sync_result = asyncio.run(pm_manager.synchronize_systems())

        if sync_result["success"]:
            click.echo("✅ PM number synchronization completed!")
            click.echo(f"  GitHub issues synced: {sync_result['github_issues_synced']}")
            click.echo(f"  CSV entries updated: {sync_result['csv_entries_updated']}")
            click.echo(f"  Conflicts resolved: {sync_result['conflicts_resolved']}")

            if sync_result["csv_only_pm_numbers"]:
                click.echo(f"\n📋 PM numbers only in CSV (may need GitHub issues):")
                for pm_num in sync_result["csv_only_pm_numbers"]:
                    click.echo(f"  - {pm_num}")

        else:
            click.echo("❌ PM number synchronization failed!")
            click.echo(f"  Errors: {len(sync_result['errors'])}")

            for error in sync_result["errors"]:
                click.echo(f"  - {error}")

            click.echo("\n💡 Suggested actions:")
            click.echo("  - Check GitHub authentication: gh auth status")
            click.echo("  - Verify file permissions and accessibility")
            click.echo("  - Try running 'issues verify' to check current state")

    except Exception as e:
        click.echo(f"❌ Error synchronizing PM numbers: {e}")
        click.echo("💡 Common solutions:")
        click.echo("  - Check GitHub authentication: gh auth status")
        click.echo("  - Verify file permissions and accessibility")
        click.echo("  - Ensure network connectivity")
        click.echo("  - Try running with --dry-run first to test")
        click.echo("  - Check if all tracking files are properly formatted")


@issues.command()
@click.option("--project", help="Project filter for issues")
@click.option("--limit", type=int, default=10, help="Limit for triage analysis (default: 10)")
async def triage(project: str, limit: int):
    """Quick issue triage and prioritization"""
    issues_cmd = IssuesCommand()
    kwargs = {}
    if project:
        kwargs["project"] = project
    if limit:
        kwargs["limit"] = limit
    await issues_cmd.execute("triage", **kwargs)


@issues.command()
@click.option("--project", help="Project filter for issues")
async def status(project: str):
    """Current issue status overview"""
    issues_cmd = IssuesCommand()
    kwargs = {}
    if project:
        kwargs["project"] = project
    await issues_cmd.execute("status", **kwargs)


@issues.command()
@click.option("--feature", help="Feature filter for pattern discovery")
async def patterns(feature: str):
    """Discovered issue patterns and insights"""
    issues_cmd = IssuesCommand()
    kwargs = {}
    if feature:
        kwargs["feature"] = feature
    await issues_cmd.execute("patterns", **kwargs)


def main():
    """Main entry point - enable Click command group with async support"""
    # Convert async commands to sync for Click framework compatibility
    for cmd in [create, verify, sync, triage, status, patterns]:
        if asyncio.iscoroutinefunction(cmd.callback):
            original_callback = cmd.callback

            def make_sync_callback(callback):
                def sync_callback(*args, **kwargs):
                    return asyncio.run(callback(*args, **kwargs))

                return sync_callback

            cmd.callback = make_sync_callback(original_callback)

    # Call the Click group directly
    issues()


if __name__ == "__main__":
    main()
