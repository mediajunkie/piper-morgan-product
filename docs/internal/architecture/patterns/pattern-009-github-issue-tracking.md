# Pattern-009: GitHub Issue Tracking Pattern

## Status

**Proven**

## Context

Software development projects require systematic tracking of work items, bugs, features, and process improvements. Without proper issue tracking, work becomes fragmented, progress is hard to measure, accountability suffers, and context is lost. The GitHub Issue Tracking Pattern addresses:

- Systematic work item documentation and progress tracking
- Evidence-based development with clear audit trails
- Coordination between team members and AI agents
- Integration between planning, execution, and validation phases
- Standardized workflow for issue creation, updates, and closure
- Maintaining project visibility and accountability

## Pattern Description

The GitHub Issue Tracking Pattern provides systematic work item management through structured GitHub issues that serve as single sources of truth for development tasks. The pattern integrates issue tracking with development workflows, ensuring every significant work item has proper documentation, progress tracking, and evidence collection.

## Implementation

### Structure

```python
# GitHub issue workflow integration
class GitHubIssueTracker:
    def __init__(self, github_agent: GitHubAgent):
        self.github_agent = github_agent

    async def create_work_item(self, title: str, description: str, labels: List[str]) -> int:
        """Create new tracked work item"""
        pass

    async def update_progress(self, issue_number: int, progress_update: str) -> None:
        """Update issue with progress evidence"""
        pass

    async def complete_work_item(self, issue_number: int, completion_evidence: str) -> None:
        """Mark work item complete with evidence"""
        pass
```

### Example (GitHub CLI Integration)

```bash
# Before starting work - verify issue exists
gh issue view PM-XXX

# Create new issue with proper numbering
tail -5 docs/planning/pm-issues-status.csv  # Check next number
gh issue create --title "PM-171: Feature Implementation" \
    --body "Detailed description with acceptance criteria"

# During work - update issue description (not comments)
gh issue edit PM-171 --body "Updated description with progress checkboxes"

# Provide evidence links in issue updates
gh issue edit PM-171 --body "Progress update with evidence:
- [x] Phase 1 complete
- [ ] Phase 2 in progress
Evidence: commit abc123, deployment log xyz"
```

### Example (Python Integration)

```python
# Integration with development workflow
from services.integrations.github.github_agent import GitHubAgent

class ProjectWorkflow:
    def __init__(self):
        self.github_agent = GitHubAgent()

    async def start_work_item(self, issue_number: int):
        """Initialize work on tracked issue"""
        issue = await self.github_agent.get_issue_details(issue_number)
        logger.info(f"Starting work on {issue['title']}")
        return issue

    async def log_progress(self, issue_number: int, evidence: Dict[str, Any]):
        """Log progress with evidence to issue"""
        progress_update = self.format_progress_update(evidence)
        await self.github_agent.update_issue_description(
            issue_number,
            progress_update
        )

    def format_progress_update(self, evidence: Dict[str, Any]) -> str:
        """Format evidence for issue updates"""
        return f"""
        Progress Update:
        - Completed: {evidence.get('completed_tasks', [])}
        - Evidence: {evidence.get('evidence_links', [])}
        - Next: {evidence.get('next_steps', [])}
        """
```

### Example (CSV Status Tracking)

```csv
# docs/planning/pm-issues-status.csv
issue_number,issue_title,status,last_updated,assignee
170,Pattern Catalog Consolidation,Open,2025-09-15,cursor-agent
171,Documentation Link Fixes,Closed,2025-09-15,cursor-agent
172,DDD Service Layer Implementation,In Progress,2025-09-15,code-agent
```

## Usage Guidelines

### Issue Creation Best Practices

- **Sequential Numbering**: Check CSV for next available PM-XXX number
- **Descriptive Titles**: Include PM number and clear description
- **Detailed Bodies**: Include context, acceptance criteria, and success metrics
- **Proper Labels**: Use consistent labeling for categorization
- **Evidence Requirements**: Specify what evidence will demonstrate completion

### Progress Tracking Best Practices

- **Update Descriptions**: Modify issue description, not just comments
- **Checkbox Progress**: Use GitHub checkbox syntax for task lists
- **Evidence Links**: Include links to commits, deployments, test results
- **Regular Updates**: Update at major milestones, not just completion
- **Cross-Reference**: Link related issues and pull requests

### Integration Workflow Best Practices

- **Verify Before Work**: Always `gh issue view PM-XXX` before starting
- **Evidence-Based Updates**: Every progress update should include evidence
- **Completion Criteria**: Clear definition of "done" with verification steps
- **Audit Trail**: Maintain complete history of decisions and changes
- **Cross-Agent Coordination**: Use issues for multi-agent work coordination

### Anti-Patterns to Avoid

- Creating issues without proper numbering or description
- Using only comments instead of updating issue descriptions
- Closing issues without evidence of completion
- Working on tasks without corresponding issues
- Inconsistent labeling or categorization
- Missing cross-references between related work items

## Related Patterns

- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Evidence requirements
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Multi-agent coordination
- [Pattern-002: Service Pattern](pattern-002-service.md) - GitHub integration service
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain service integration

## Migration Notes (for consolidation from legacy systems)

- **From `PATTERN-INDEX.md`**: No direct equivalent found - this is an emergent pattern
- **From `pattern-catalog.md`**: No direct equivalent found - this is a process pattern
- **From `github-tracking` rule**: Core requirements and CLI workflow patterns
- **From `GitHubAgent` implementation**: Technical integration patterns and API usage
- **Consolidation Strategy**: Created from observed project practices and tracking requirements

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source practices is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for GitHub API integration and automation
- **Agent B (Cursor)**: Responsible for process documentation and workflow validation
- **Multi-Agent Usage**: Issues serve as coordination points between agents

## References

- GitHub tracking rule: workspace rules `github-tracking`
- GitHub Agent implementation: `services/integrations/github/github_agent.py`
- Issue status tracking: `docs/planning/pm-issues-status.csv`
- GitHub CLI documentation: https://cli.github.com/manual/gh_issue

_Last updated: September 15, 2025_
