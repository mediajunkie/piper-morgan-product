# ADR-033: Multi-Agent Scripts Deployment

## Status
Accepted

## Context
During the DDD refactoring (September 9-12), we created scripts for multi-agent coordination that have not been deployed. These scripts (`deploy_multi_agent_coordinator.sh`, `validate_multi_agent_operation.sh`) implement the May 27 vision of specialized agents working in coordination. Recent success with parallel agent deployment (Bug #166) validates this approach.

## Decision
We will deploy and operationalize the existing multi-agent coordination scripts, making multi-agent deployment the default approach for all development work that can benefit from specialization.

### Agent Specialization Model
- **Claude Code**: Backend, services, investigations, broad analysis
- **Cursor Agent**: UI, templates, user experience, specific file edits
- **Chief Architect**: Gameplans, strategy, architectural decisions
- **Lead Developer**: Agent coordination, prompt creation, validation

### Deployment Protocol
1. **Default to multi-agent** unless explicitly justified otherwise
2. **Parallel execution** when tasks are independent
3. **Sequential handoffs** when dependencies exist
4. **Cross-validation** at defined checkpoints

## Consequences

### Positive
- **Specialized expertise**: Each agent optimized for their strengths
- **Parallel throughput**: Multiple tasks advance simultaneously
- **Built-in validation**: Agents check each other's work
- **Reduced context switching**: Agents maintain focus on their domain
- **Natural team dynamics**: Mimics human development teams

### Negative
- **Coordination overhead**: Managing multiple agents requires effort
- **Potential conflicts**: Agents may disagree on approaches
- **Resource consumption**: Multiple agents use more compute
- **Complexity increase**: More moving parts to track

### Neutral
- **GitHub tracking requirement**: Must maintain clear issue updates
- **Session log multiplication**: Each agent creates logs
- **Prompt engineering needs**: Each agent needs specific instructions

## Implementation

### Immediate Actions (Today)
```bash
# Deploy the coordinator
./scripts/deploy_multi_agent_coordinator.sh

# Validate operation
./scripts/validate_multi_agent_operation.sh
```

### Week 1: Formalize Protocols
- Document handoff procedures
- Create cross-validation checkpoints
- Establish conflict resolution process

### Week 2: Optimize Patterns
- Analyze coordination successes/failures
- Refine agent specializations
- Create reusable prompt templates

## Success Metrics
- Parallel task completion rate
- Cross-validation catch rate
- Time to completion vs single agent
- Conflict frequency and resolution time

## References
- Original vision: May 27, 2025
- Pattern-029: Multi-Agent Coordination
- Issue #118: INFR-AGENT Multi-Agent Coordinator
- Current example: Bug #166 parallel execution
