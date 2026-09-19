---
type: methodology
title: Multi-Agent Coordination Templates
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Multi-Agent Coordination Templates

**Purpose**: Ready-to-use templates for implementing multi-agent coordination in development workflows.

## 📋 Task Decomposition Template

### **Task Analysis Form**

```
TASK: [Task Name]
ESTIMATED DURATION: [X minutes/hours]
COMPLEXITY LEVEL: [SIMPLE/MODERATE/COMPLEX]
DOMAINS REQUIRED: [List domains: backend, frontend, testing, etc.]

REQUIRED CAPABILITIES:
□ Infrastructure & Architecture
□ Backend Services & APIs
□ Database Operations
□ Testing Frameworks
□ UI Components
□ Documentation
□ Integration Testing
□ Performance Optimization

DEPENDENCIES: [List any prerequisites]
RISK FACTORS: [Identify potential blockers]
```

### **Subtask Breakdown Template**

```
SUBTASK 1: [Architecture Design]
AGENT: [CODE/CURSOR]
DURATION: [X% of total]
DEPENDENCIES: [None or list]
DELIVERABLES: [What will be produced]
ACCEPTANCE CRITERIA: [How to know it's done]

SUBTASK 2: [Core Implementation]
AGENT: [CODE/CURSOR]
DURATION: [X% of total]
DEPENDENCIES: [Subtask 1]
DELIVERABLES: [What will be produced]
ACCEPTANCE CRITERIA: [How to know it's done]

[Continue for all subtasks...]
```

## 🔄 Agent Assignment Checklist

### **Pre-Assignment Checklist**

```
□ CAPABILITY MATCH: Agent has required strengths
□ AVAILABILITY: Agent is not overloaded
□ TIMELINE FIT: Assignment fits project schedule
□ DEPENDENCIES: Prerequisites are completed
□ RESOURCES: Agent has access to needed tools/data
□ COMMUNICATION: Clear handoff protocol defined
```

### **Assignment Documentation Template**

```
ASSIGNMENT: [Subtask Name]
ASSIGNED TO: [Agent Name/Type]
ASSIGNED BY: [Coordinator Name]
ASSIGNMENT DATE: [Date]
EXPECTED COMPLETION: [Date]

REQUIREMENTS:
- [List specific requirements]

ACCEPTANCE CRITERIA:
- [List acceptance criteria]

INTERFACES:
- [Define interfaces with other subtasks]

COMMUNICATION PLAN:
- [How/when to provide updates]
- [How to escalate blockers]
```

### **Handoff Protocol Template**

```
HANDOFF FROM: [Previous Agent]
HANDOFF TO: [Next Agent]
HANDOFF DATE: [Date]

COMPLETED WORK:
- [List what was accomplished]
- [Link to deliverables]

PENDING WORK:
- [List what still needs to be done]
- [Any blockers or issues]

INTERFACE SPECIFICATIONS:
- [Define how components interact]
- [API contracts, data formats]

QUALITY GATES:
- [What must be verified before proceeding]
- [Testing requirements]
```

## 🎯 Synchronization Point Planning

### **Synchronization Schedule Template**

```
SYNC POINT 1: [Architecture Review]
DATE: [Date]
PARTICIPANTS: [Code Agent, Cursor Agent]
AGENDA:
- [Review architecture decisions]
- [Validate interfaces]
- [Plan implementation approach]

SYNC POINT 2: [Integration Testing]
DATE: [Date]
PARTICIPANTS: [Both Agents]
AGENDA:
- [Test integration points]
- [Validate end-to-end functionality]
- [Plan final testing]

SYNC POINT 3: [Final Review]
DATE: [Date]
PARTICIPANTS: [Both Agents]
AGENDA:
- [Final validation]
- [Documentation review]
- [Deployment planning]
```

### **Communication Protocol Template**

```
STATUS UPDATES:
- Frequency: [Daily/Every X hours]
- Format: [Brief summary + blockers]
- Channel: [Slack/Email/GitHub]

BLOCKER ESCALATION:
- Level 1: [Agent tries to resolve]
- Level 2: [Escalate to coordinator]
- Level 3: [Escalate to PM/Architect]

DECISION POINTS:
- [List critical decisions that need coordination]
- [Who makes the decision]
- [How to communicate the decision]
```

## 📊 Progress Tracking Template

### **Daily Status Update Template**

```
DATE: [Date]
AGENT: [Agent Name]
SUBTASK: [Subtask Name]

PROGRESS:
- [What was accomplished today]
- [Percentage complete]

BLOCKERS:
- [Any issues preventing progress]
- [Help needed from other agents]

NEXT STEPS:
- [What will be done tomorrow]
- [Dependencies on other agents]

METRICS:
- [Time spent today]
- [Estimated time to completion]
- [Quality metrics (if applicable)]
```

### **Weekly Coordination Review Template**

```
WEEK: [Week of Date]
COORDINATOR: [Coordinator Name]

OVERALL PROGRESS:
- [Summary of all subtasks]
- [Overall completion percentage]
- [Timeline status]

BLOCKERS & RISKS:
- [List any blockers]
- [Risk assessment]
- [Mitigation plans]

NEXT WEEK PLANNING:
- [Key milestones]
- [Resource allocation]
- [Risk mitigation]

PERFORMANCE METRICS:
- [Coordination latency]
- [Success rate]
- [Agent utilization]
```

## 🚀 Quick Start Templates

### **Simple Task Template (Single Agent)**

```
TASK: [Task Name]
AGENT: [CODE or CURSOR]
ESTIMATED DURATION: [<30 minutes]
APPROACH: [Single agent execution]
NO COORDINATION NEEDED
```

### **Moderate Task Template (Single Agent, Multiple Subtasks)**

```
TASK: [Task Name]
AGENT: [CODE or CURSOR]
ESTIMATED DURATION: [30-120 minutes]
SUBTASKS: [List 2-3 subtasks]
APPROACH: [Sequential execution by single agent]
COORDINATION: [Internal task management only]
```

### **Complex Task Template (Multi-Agent)**

```
TASK: [Task Name]
COMPLEXITY: [COMPLEX - >120 minutes, multiple domains]
AGENTS: [CODE + CURSOR]
APPROACH: [Parallel execution with coordination]
SYNCHRONIZATION: [Multiple handoff points]
COORDINATION: [Full multi-agent workflow]
```

## 📝 Example Usage

### **Example: Building a New API Feature**

```
TASK: User Preference Management API
ESTIMATED DURATION: 4 hours
COMPLEXITY LEVEL: COMPLEX
DOMAINS REQUIRED: Backend, Database, Testing, Documentation

SUBTASK 1: Database Schema Design
AGENT: CODE
DURATION: 25% (1 hour)
DEPENDENCIES: None
DELIVERABLES: Database migration, model definitions

SUBTASK 2: API Implementation
AGENT: CODE
DURATION: 40% (1.6 hours)
DEPENDENCIES: Database schema
DELIVERABLES: API endpoints, business logic

SUBTASK 3: Testing & Validation
AGENT: CURSOR
DURATION: 20% (0.8 hours)
DEPENDENCIES: API implementation
DELIVERABLES: Test suite, validation

SUBTASK 4: Documentation & Polish
AGENT: CURSOR
DURATION: 15% (0.6 hours)
DEPENDENCIES: Testing complete
DELIVERABLES: API docs, user guide
```

---

**Usage Instructions**: Copy these templates and customize them for your specific tasks. The templates provide structure while allowing flexibility for different project requirements.
