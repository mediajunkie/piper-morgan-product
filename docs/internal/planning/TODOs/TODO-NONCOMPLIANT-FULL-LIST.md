# Complete List of Non-Compliant TODOs

**Generated**: September 25, 2025, 4:20 PM
**Total Non-Compliant**: 58 TODOs without issue references
**Action Required**: Add issue references or remove obsolete TODOs

## Full List by File

### services/api/task_management.py (14 TODOs)
```
services/api/task_management.py:151:    # TODO: Implement TaskManagementService
services/api/task_management.py:157:    # TODO: Implement UniversalListService
services/api/task_management.py:163:    # TODO: Implement QueryRouter integration
services/api/task_management.py:188:        # TODO: Implement task creation with TaskManagementService
services/api/task_management.py:221:        # TODO: Implement task retrieval with TaskManagementService
services/api/task_management.py:253:        # TODO: Implement task update with TaskManagementService
services/api/task_management.py:290:        # TODO: Implement task deletion with TaskManagementService
services/api/task_management.py:332:        # TODO: Implement advanced search with QueryRouter
services/api/task_management.py:383:        # TODO: Implement task list creation with UniversalListService
services/api/task_management.py:424:        # TODO: Implement task list retrieval with UniversalListService
services/api/task_management.py:457:        # TODO: Implement task list update with UniversalListService
services/api/task_management.py:479:        # TODO: Delete universal List with item_type='task'
services/api/task_management.py:531:        # TODO: Implement member retrieval with UniversalListService
services/api/task_management.py:571:        # TODO: Create universal ListItem with item_type='task'
services/api/task_management.py:604:        # TODO: Remove universal ListItem with item_type='task'
services/api/task_management.py:605:        # TODO: Update PM-040 Knowledge Graph to reflect removal
services/api/task_management.py:645:        # TODO: Implement batch task operations with TaskManagementService
services/api/task_management.py:656:        # TODO: Use QueryRouter to classify search intent
services/api/task_management.py:657:        # TODO: Use PM-034 intent classification for advanced search
```

### services/api/todo_management.py (14 TODOs)
```
services/api/todo_management.py:153:    # TODO: Implement TodoManagementService
services/api/todo_management.py:159:    # TODO: Implement UniversalListService
services/api/todo_management.py:165:    # TODO: Implement KnowledgeGraphService integration
services/api/todo_management.py:171:    # TODO: Implement QueryRouter integration
services/api/todo_management.py:237:        # TODO: Implement todo retrieval with TodoManagementService
services/api/todo_management.py:268:        # TODO: Implement todo update with TodoManagementService
services/api/todo_management.py:298:        # TODO: Implement todo deletion with TodoManagementService
services/api/todo_management.py:340:        # TODO: Implement advanced search with QueryRouter
services/api/todo_management.py:391:        # TODO: Implement todo list creation with UniversalListService
services/api/todo_management.py:432:        # TODO: Implement todo list retrieval with UniversalListService
services/api/todo_management.py:465:        # TODO: Implement todo list update with UniversalListService
services/api/todo_management.py:496:        # TODO: Delete universal List with item_type='todo'
services/api/todo_management.py:539:        # TODO: Implement member retrieval with UniversalListService
services/api/todo_management.py:579:        # TODO: Create universal ListItem with item_type='todo'
services/api/todo_management.py:653:        # TODO: Implement batch todo operations with TodoManagementService
```

### services/intent_service/llm_classifier_factory.py (1 TODO)
```
services/intent_service/llm_classifier_factory.py:55:                        boundary_enforcer=None,  # TODO: Wire BoundaryEnforcer when available
```

### services/knowledge/knowledge_graph_service.py (3 TODOs)
```
services/knowledge/knowledge_graph_service.py:252:                # TODO: Implement proper boundary check
services/knowledge/knowledge_graph_service.py:292:        # TODO: Implement more sophisticated algorithms (Dijkstra, A*, etc.)
services/knowledge/knowledge_graph_service.py:321:                # TODO: Implement proper boundary check
```

### services/orchestration/multi_agent_coordinator.py (1 TODO)
```
services/orchestration/multi_agent_coordinator.py:656:        # TODO: More sophisticated parallel analysis for dependent task chains
```

## Summary by Category

### Service Implementation TODOs (28)
- TodoManagementService: 7 occurrences
- TaskManagementService: 7 occurrences
- UniversalListService: 8 occurrences
- QueryRouter integration: 6 occurrences

### Architecture/Infrastructure TODOs (5)
- BoundaryEnforcer: 3 occurrences
- Algorithm improvements: 1 occurrence
- Parallel processing: 1 occurrence

### Recommendations for Bulk Updates

#### Group 1: Service Implementation
Create a single parent issue for implementing core services:
- **Issue Title**: Implement core service layer (TodoManagementService, TaskManagementService, UniversalListService)
- **Description**: Complete implementation of service layer for todo and task management
- **Files affected**: services/api/todo_management.py, services/api/task_management.py
- **TODO count**: 28 TODOs can reference this single issue

#### Group 2: QueryRouter Integration
Create issue for completing QueryRouter integration:
- **Issue Title**: Complete QueryRouter integration across API endpoints
- **Description**: Wire up QueryRouter for search and intent classification
- **Files affected**: services/api/todo_management.py, services/api/task_management.py
- **TODO count**: 6 TODOs can reference this issue

#### Group 3: Boundary Enforcement
Create issue for boundary checking improvements:
- **Issue Title**: Implement comprehensive boundary checking
- **Description**: Add content-based boundary checking to BoundaryEnforcer
- **Files affected**: services/knowledge/knowledge_graph_service.py, services/intent_service/llm_classifier_factory.py
- **TODO count**: 4 TODOs can reference this issue

## Quick Fix Script

To bulk update similar TODOs with issue references, use:

```bash
# Example: Update all TodoManagementService TODOs
find services/api -name "*.py" -exec sed -i '' 's/# TODO: Implement TodoManagementService/# TODO(#ISSUE-NUMBER): Implement TodoManagementService/g' {} \;

# Example: Update all UniversalListService TODOs
find services/api -name "*.py" -exec sed -i '' 's/# TODO: Implement UniversalListService/# TODO(#ISSUE-NUMBER): Implement UniversalListService/g' {} \;
```

---

**Next Steps**:
1. Create parent GitHub issues for grouped work
2. Run bulk update scripts with actual issue numbers
3. Target 80% compliance (need to fix ~37 more TODOs)
