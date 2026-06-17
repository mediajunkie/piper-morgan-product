# Pattern-029: Multi-Agent Coordination

## Status
**Proven** — multi-agent coordination is live cohort-wide (duty-cycle fleet + mailbox protocol, 2026); refreshed 2026-06-17 (was "Experimental, deployment pending")

## Context
Complex development tasks benefit from multiple specialized AI agents working in coordination, similar to how human development teams have specialized roles. This pattern defines how agents coordinate, hand off work, and validate each other's outputs.

## Pattern

### Agent Specialization Model
```python
class AgentRole(Enum):
    ARCHITECT = "architect"        # Strategic planning, gameplans
    BACKEND = "code"               # Services, domain logic, investigations
    FRONTEND = "cursor"            # UI, templates, user experience
    ANALYST = "analyst"            # Data analysis, pattern detection
    DOCUMENTER = "documenter"      # Documentation, ADRs, patterns
```

### Orchestration Pattern
```python
class MultiAgentOrchestrator:
    """
    Coordinates multiple specialized agents for complex tasks.
    Based on May 27 vision, implemented via scripts.
    """

    def deploy_agents(self, task: Task) -> DeploymentPlan:
        """
        Determine which agents needed and their coordination.
        """
        if task.requires_investigation:
            agents = [AgentRole.BACKEND]  # Code for broad investigation

        if task.requires_ui_changes:
            agents.append(AgentRole.FRONTEND)  # Cursor for UI

        if task.requires_architecture:
            agents.insert(0, AgentRole.ARCHITECT)  # Architect plans first

        return self.create_deployment_plan(agents, task)

    def create_deployment_plan(self, agents: List[AgentRole], task: Task):
        """
        Define coordination points and handoffs.
        """
        plan = DeploymentPlan()

        # Phase 0: Always investigation first
        plan.add_phase("investigation", agents[0],
                      "Verify infrastructure, check existing patterns")

        # Parallel execution where possible
        if len(agents) > 1 and task.allows_parallel:
            plan.add_parallel_phase("implementation", agents,
                                  "Cross-validate every 30 minutes")

        # Sequential handoffs where needed
        else:
            for i, agent in enumerate(agents):
                plan.add_sequential_phase(f"phase_{i}", agent,
                                        "Complete and hand off to next")

        return plan
```

### Existing Scripts (Ready to Deploy)
Located in `scripts/`:
```bash
# Deploy multi-agent coordinator
./scripts/deploy_multi_agent_coordinator.sh

# Validate agent operations
./scripts/validate_multi_agent_operation.sh

# Agent communication protocol
./scripts/setup_agent_communication.sh
```

### Cross-Validation Protocol
```python
# Agents validate each other's work
class CrossValidation:
    """
    Pattern for agents to verify each other's outputs.
    """

    def validate_backend_changes(self, changes: CodeChanges) -> ValidationResult:
        """Cursor validates Code's backend changes don't break UI"""
        pass

    def validate_ui_changes(self, changes: UIChanges) -> ValidationResult:
        """Code validates Cursor's UI changes follow patterns"""
        pass

    def consensus_required(self) -> bool:
        """Both agents must agree on critical changes"""
        return self.change_severity > Severity.MEDIUM
```

## Benefits
- **Specialized expertise**: Each agent optimized for their domain
- **Parallel execution**: Multiple agents work simultaneously
- **Built-in validation**: Cross-checking reduces errors
- **Natural handoffs**: Mimics human team coordination

## Trade-offs
- **Coordination overhead**: Managing multiple agents adds complexity
- **Context synchronization**: Keeping agents aligned requires effort
- **Potential conflicts**: Agents may disagree on approach
- **Resource usage**: Multiple agents consume more resources

## Implementation Strategy

### Phase 1: Deploy Existing Scripts (Immediate)
```bash
# Run deployment script
./scripts/deploy_multi_agent_coordinator.sh

# Verify operations
./scripts/validate_multi_agent_operation.sh
```

### Phase 2: Formalize Coordination (Week 1)
- Document handoff protocols
- Create GitHub issue templates for coordination
- Establish validation checkpoints

### Phase 3: Learn from Patterns (Week 2)
- Analyze coordination successes/failures
- Refine agent specializations
- Optimize parallel execution

## Practical Example: Bug #166 Fix
```markdown
## Multi-Agent Deployment for Bug #166

**Claude Code** (Backend Specialist):
- Fix config nesting issue
- Remove architectural violations
- Centralize port configuration

**Cursor Agent** (UI Specialist):
- Validate UI functionality after each fix
- Verify templates still work
- Cross-check user experience

**Coordination**:
- Check-in every 30 minutes
- Cross-validate after each phase
- Stop if complexity emerges
```

## Related Patterns
- [Pattern-028: Intent Classification](pattern-028-intent-classification.md)
- [Pattern-017: Background Task Error Handling](pattern-017-background-task-error-handling.md)
- [Pattern-030: Plugin Interface](pattern-030-plugin-interface.md)

### Differentiation: Pattern-029 vs Pattern-059

Pattern-029 and [Pattern-059: Leadership Caucus](pattern-059-leadership-caucus.md) both involve multiple agents but operate at different levels:

| Dimension | Pattern-029 (Multi-Agent Coordination) | Pattern-059 (Leadership Caucus) |
|-----------|----------------------------------------|---------------------------------|
| **Domain** | Technical execution | Leadership alignment |
| **Purpose** | Coordinate parallel implementation work | Align on cross-cutting decisions before work begins |
| **Participants** | Coding agents (Backend, Frontend, Analyst) | Advisory agents (CXO, Architect, PPM) + PM |
| **Timing** | During execution | Before execution |
| **Output** | Code, tests, validated changes | Decisions, assignments, implementation direction |
| **Coordination** | Cross-validation, handoffs, parallel phases | Facilitated discussion, real-time decision capture |

**In practice**: A Leadership Caucus (059) might produce the decision and assignment that triggers a Multi-Agent Coordination (029) deployment. They are sequential, not competing — one decides *what* and *how*; the other *executes*.

## References
- Original vision: May 27, 2025 (Multi-agent orchestration)
- Related issue: #118 (INFR-AGENT Multi-Agent Coordinator)
- Scripts location: scripts/deploy_multi_agent_coordinator.sh
- Current usage: Bug #166 parallel execution
