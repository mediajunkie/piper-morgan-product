# Multi-Agent Coordinator Integration Guide

> 🔴 **HISTORICAL — the whole subsystem this guide teaches is deleted (2026-09-01 banner, supersedes
> the 2026-05-15 one below).** `services/orchestration/` — including `multi_agent_coordinator.py`
> and `chain_of_draft.py`, which the prior banner claimed "survive and remain the concrete
> multi-agent coordination surfaces" — was fully deleted 2026-07-18 (#1436, Tier-3 Family-2
> orchestration-island deletion, commit `addb61c99`; PM-033d thinking preserved as a design
> record). That claim is confirmed false as of this correction: `services/orchestration/` does
> not exist in the live tree. Confirmed via B3 corpus-disposition (CIO, 2026-09-01):
> `docs/internal/architecture/reviews/2026-08-architectural-review/b3-methodology-disposition.md`.
> `doc-sync-sweep`'s own canonical "banner-not-rewrite" example previously cited this file's
> May-15 banner as a success story — that citation described a fix now itself overtaken by
> events; corrected to point at `pattern-024-methodology-patterns.md`'s supersession banner
> instead (a fix that remains current). Guide content preserved below for historical reference
> only — do not write code against it.
>
> <details><summary>Prior (2026-05-15) staleness banner, superseded above</summary>
>
> This guide references `services/orchestration/engine.py` and `OrchestrationEngine`, both
> deleted in #1094 (ENGINE-DELETION, γ-preserve). EXECUTION-intent dispatch now flows through
> `intent_service.process_intent` direct dispatch via the `task_type` registry (Pattern-072,
> promoted to Proven via #1094). The `MultiAgentCoordinator` itself
> (`services/orchestration/multi_agent_coordinator.py`) + `chain_of_draft.py` survive and remain
> the concrete multi-agent coordination surfaces. The code samples below are no longer
> copy-pasteable — extend `intent_service` handler dispatch instead of `OrchestrationEngine` task
> handlers. The high-level concept (decompose-coordinate-execute) remains illustrative; the
> dispatch layer this guide describes is gone.
>
> </details>

**Purpose**: Transform the Multi-Agent Coordinator from aspirational infrastructure to operational development methodology. (historical — subsystem deleted, see banner)

**Status**: 🔴 HISTORICAL — subsystem fully deleted 2026-07-18 (#1436); preserved for reference only
**Target**: Make Multi-Agent coordination a working part of our daily development workflow
**Methodology**: Excellence Flywheel - Systematic Integration

## 🎯 **INTEGRATION OBJECTIVES**

### **Primary Goals**

1. **Operational Deployment**: Make Multi-Agent Coordinator actually usable in development
2. **Workflow Integration**: Connect to existing orchestration engine and session management
3. **Performance Validation**: Ensure coordination meets <1000ms performance targets
4. **User Experience**: Provide clear interfaces for triggering multi-agent coordination

### **Success Criteria**

- [ ] Multi-Agent Coordinator can be triggered from main application
- [ ] Task decomposition works with real development tasks
- [ ] Agent assignment logic functions correctly
- [ ] Performance targets met consistently
- [ ] Integration with existing workflow engine

## 🔧 **CURRENT INTEGRATION STATUS**

### **What's Already Connected**

✅ **Orchestration Engine**: `main.py` imports and uses orchestration engine
✅ **Session Management**: SessionManager handles conversation context
✅ **Database Models**: Intent and Workflow models have context fields
✅ **Workflow Execution**: Engine can execute workflows with context

### **What's Missing**

❌ **Multi-Agent Trigger**: No way to initiate multi-agent coordination
❌ **Task Decomposition Integration**: Decomposition not connected to workflow creation
❌ **Agent Assignment Execution**: Assignment logic not used in real workflows
❌ **Performance Monitoring**: No metrics collection or validation

## 🚀 **INTEGRATION IMPLEMENTATION PLAN**

### **Phase 1: Core Integration (2 hours)**

#### **1.1 Workflow Engine Integration**

```python
# Extend services/orchestration/engine.py
class OrchestrationEngine:
    def __init__(self):
        # Add Multi-Agent Coordinator
        self.multi_agent_coordinator = MultiAgentCoordinator()

    async def create_multi_agent_workflow(self, intent: Intent, context: Dict) -> Workflow:
        """Create workflow using Multi-Agent coordination"""
        # Use coordinator for task decomposition
        coordination_result = await self.multi_agent_coordinator.coordinate_task(intent, context)

        # Convert subtasks to workflow tasks
        workflow = self._create_workflow_from_coordination(intent, coordination_result)

        return workflow
```

#### **1.2 Intent Processing Integration**

```python
# Extend services/intent_service/intent_enricher.py
class IntentEnricher:
    async def enrich_with_multi_agent(self, intent: Intent) -> Intent:
        """Enrich intent with multi-agent coordination data"""
        if self._requires_multi_agent(intent):
            intent.context["multi_agent_coordination"] = True
            intent.context["estimated_complexity"] = "complex"

        return intent
```

#### **1.3 API Endpoint Creation**

```python
# Add to main.py or create new orchestration API
@app.post("/api/orchestration/multi-agent")
async def trigger_multi_agent_coordination(intent_request: IntentRequest):
    """Trigger multi-agent coordination for complex tasks"""

    # Create intent
    intent = Intent(
        id=str(uuid4()),
        category=intent_request.category,
        action=intent_request.action,
        original_message=intent_request.message,
        context={"multi_agent": True}
    )

    # Use orchestration engine with multi-agent
    workflow = await engine.create_multi_agent_workflow(intent, intent_request.context)

    return WorkflowResponse(
        workflow_id=workflow.id,
        status=workflow.status,
        type=workflow.type,
        tasks=workflow.tasks,
        message=f"Multi-agent coordination initiated for: {intent.action}"
    )
```

### **Phase 2: Task Execution Integration (1 hour)**

#### **2.1 Subtask to Workflow Task Conversion**

```python
# In OrchestrationEngine
def _create_workflow_from_coordination(self, intent: Intent, coordination_result: CoordinationResult) -> Workflow:
    """Convert coordination result to executable workflow"""

    workflow = Workflow(
        id=str(uuid4()),
        type=WorkflowType.MULTI_AGENT,
        status=WorkflowStatus.PENDING,
        intent_id=intent.id,
        context={
            "coordination_id": coordination_result.coordination_id,
            "agent_assignments": {
                subtask.id: subtask.assigned_agent.value
                for subtask in coordination_result.subtasks
            }
        }
    )

    # Convert subtasks to workflow tasks
    for subtask in coordination_result.subtasks:
        task = Task(
            id=subtask.id,
            workflow_id=workflow.id,
            name=subtask.title,
            type=self._map_subtask_to_task_type(subtask),
            status=TaskStatus.PENDING,
            input_data={"subtask_data": subtask.__dict__}
        )
        workflow.tasks.append(task)

    return workflow
```

#### **2.2 Agent-Specific Task Execution**

```python
# Extend task handlers in OrchestrationEngine
async def _execute_multi_agent_task(self, task: Task, workflow: Workflow) -> TaskResult:
    """Execute task with agent-specific logic"""

    # Get agent assignment from workflow context
    agent_type = workflow.context["agent_assignments"].get(task.id)

    if agent_type == "code":
        return await self._execute_code_agent_task(task)
    elif agent_type == "cursor":
        return await self._execute_cursor_agent_task(task)
    else:
        return await self._execute_general_task(task)
```

### **Phase 3: Performance & Monitoring (1 hour)**

#### **3.1 Performance Metrics Collection**

```python
# Extend MultiAgentCoordinator
class MultiAgentCoordinator:
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get real-time performance metrics"""
        if not self.coordination_sessions:
            return {"total_coordinations": 0, "average_latency_ms": 0}

        sessions = list(self.coordination_sessions.values())
        total_sessions = len(sessions)
        average_latency = sum(s.total_duration_ms for s in sessions) / total_sessions

        return {
            "total_coordinations": total_sessions,
            "average_latency_ms": int(average_latency),
            "success_rate": sum(1 for s in sessions if s.status != CoordinationStatus.FAILED) / total_sessions,
            "performance_target_met": average_latency < 1000,
            "agent_utilization": self._calculate_agent_utilization(sessions)
        }
```

#### **3.2 Integration Health Monitoring**

```python
# Add to services/health/integration_health_monitor.py
class MultiAgentHealthMonitor:
    async def check_multi_agent_health(self) -> Dict[str, Any]:
        """Monitor Multi-Agent Coordinator health"""

        try:
            # Test coordination performance
            test_intent = Intent(
                id="health_check",
                category=IntentCategory.EXECUTION,
                action="test_coordination",
                original_message="Health check coordination"
            )

            start_time = time.time()
            result = await self.coordinator.coordinate_task(test_intent, {})
            duration_ms = int((time.time() - start_time) * 1000)

            return {
                "status": "healthy" if duration_ms < 1000 else "degraded",
                "response_time_ms": duration_ms,
                "target_met": duration_ms < 1000,
                "coordination_success": result.status == CoordinationStatus.COMPLETED,
                "last_check": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }
```

## 🔄 **WORKFLOW INTEGRATION PATTERNS**

### **Pattern 1: Intent-Based Coordination**

```python
# User sends complex request
intent = Intent(
    category=IntentCategory.EXECUTION,
    action="build_user_preference_api",
    original_message="I need a complete user preference management API with testing"
)

# System automatically detects complexity and triggers multi-agent
if self._requires_multi_agent(intent):
    workflow = await engine.create_multi_agent_workflow(intent, context)
    return f"Multi-agent coordination initiated. Workflow ID: {workflow.id}"
else:
    workflow = await engine.create_single_agent_workflow(intent, context)
    return f"Single agent workflow created. Workflow ID: {workflow.id}"
```

### **Pattern 2: Session-Based Coordination**

```python
# Extend ConversationSession
class ConversationSession:
    async def trigger_multi_agent_coordination(self, intent: Intent) -> str:
        """Trigger multi-agent coordination from conversation"""

        # Check if this session has ongoing coordination
        if "ongoing_coordination" in self.context:
            return "Coordination already in progress. Check workflow status."

        # Create multi-agent workflow
        workflow = await self.orchestration_engine.create_multi_agent_workflow(intent, self.context)

        # Track coordination in session
        self.context["ongoing_coordination"] = {
            "workflow_id": workflow.id,
            "started_at": datetime.utcnow().isoformat(),
            "intent": intent.__dict__
        }

        return f"Multi-agent coordination started. Workflow ID: {workflow.id}"
```

### **Pattern 3: GitHub Integration Coordination**

```python
# Extend GitHub integration for multi-agent workflows
class GitHubMultiAgentIntegration:
    async def create_coordination_issue(self, workflow: Workflow) -> str:
        """Create GitHub issue for multi-agent coordination"""

        issue_body = f"""
# Multi-Agent Coordination: {workflow.intent.action}

## Task Decomposition
{self._format_subtasks(workflow.tasks)}

## Agent Assignments
{self._format_agent_assignments(workflow.context)}

## Coordination Status
- Workflow ID: {workflow.id}
- Status: {workflow.status}
- Created: {workflow.created_at}

## Next Steps
1. Code Agent: Complete assigned tasks
2. Cursor Agent: Complete assigned tasks
3. Integration testing
4. Final validation
        """

        issue = await self.github_client.create_issue(
            title=f"Multi-Agent: {workflow.intent.action}",
            body=issue_body,
            labels=["multi-agent", "coordination", workflow.intent.category.value]
        )

        return issue.html_url
```

## 📊 **PERFORMANCE VALIDATION**

### **Performance Test Suite**

```python
# tests/orchestration/test_multi_agent_integration.py
class TestMultiAgentIntegration:
    async def test_coordination_performance_targets(self):
        """Test that coordination meets <1000ms target"""

        start_time = time.time()
        result = await self.coordinator.coordinate_task(self.test_intent, {})
        duration_ms = int((time.time() - start_time) * 1000)

        assert duration_ms < 1000, f"Coordination took {duration_ms}ms, target is <1000ms"
        assert result.status == CoordinationStatus.COMPLETED

    async def test_workflow_integration_performance(self):
        """Test end-to-end workflow creation performance"""

        start_time = time.time()
        workflow = await self.engine.create_multi_agent_workflow(self.test_intent, {})
        duration_ms = int((time.time() - start_time) * 1000)

        assert duration_ms < 1500, f"Workflow creation took {duration_ms}ms, target is <1500ms"
        assert workflow.type == WorkflowType.MULTI_AGENT
```

### **Load Testing**

```python
# Test concurrent coordination requests
async def test_concurrent_coordination(self):
    """Test multiple simultaneous coordination requests"""

    tasks = []
    for i in range(10):
        intent = Intent(
            id=f"concurrent_{i}",
            category=IntentCategory.EXECUTION,
            action=f"test_action_{i}",
            original_message=f"Concurrent test {i}"
        )
        tasks.append(self.coordinator.coordinate_task(intent, {}))

    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_duration = time.time() - start_time

    # All should complete successfully
    assert all(r.status == CoordinationStatus.COMPLETED for r in results)
    # Total time should be reasonable (not 10x individual time)
    assert total_duration < 5.0, f"Concurrent coordination took {total_duration}s"
```

## 🚀 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment Validation**

- [ ] Multi-Agent Coordinator integration tests pass
- [ ] Performance targets met consistently
- [ ] Workflow engine integration working
- [ ] API endpoints functional
- [ ] Health monitoring operational

### **Deployment Steps**

1. **Deploy Core Integration**: Update orchestration engine with multi-agent support
2. **Enable API Endpoints**: Activate multi-agent coordination API
3. **Update Session Management**: Extend conversation sessions with coordination
4. **Activate Monitoring**: Enable performance and health monitoring
5. **User Training**: Document new multi-agent coordination workflows

### **Post-Deployment Validation**

- [ ] Real user requests trigger multi-agent coordination
- [ ] Performance metrics show <1000ms coordination time
- [ ] Agent assignments are working correctly
- [ ] GitHub integration creates coordination issues
- [ ] Session context maintains coordination state

## 📈 **SUCCESS METRICS & KPIs**

### **Operational Metrics**

- **Coordination Success Rate**: Target >95%
- **Average Response Time**: Target <1000ms
- **Agent Utilization**: Balanced workload distribution
- **Workflow Completion Rate**: Target >90%

### **User Experience Metrics**

- **Coordination Trigger Rate**: How often users trigger multi-agent
- **User Satisfaction**: Feedback on coordination effectiveness
- **Time to Completion**: Faster task completion with coordination
- **Error Reduction**: Fewer failed workflows with coordination

### **Technical Metrics**

- **Integration Health**: All systems operational
- **Performance Consistency**: Stable response times
- **Resource Usage**: Efficient memory and CPU usage
- **Scalability**: Performance maintained under load

---

**Status**: Integration Guide Complete - Ready for Implementation
**Next Steps**: Execute integration plan to make Multi-Agent Coordinator operational
**Timeline**: 4 hours for complete integration and validation
-
