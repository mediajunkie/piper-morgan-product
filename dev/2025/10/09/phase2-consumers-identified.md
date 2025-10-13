# Phase 2: All LLM Consumers Identified

**Date**: October 9, 2025, 6:53 PM
**Method**: Serena semantic search
**Expected**: 13 consumers
**Found**: 10 production consumers

---

## All 10 Production Consumers

### 1. services/intent_service/classifier.py
- **Line 34**: `from services.llm.clients import llm_client`
- **Usage**: Intent classification with LLM

### 2. services/intent_service/llm_classifier.py
- **Line 22**: `from services.llm.clients import llm_client`
- **Usage**: LLM-based intent classification

### 3. services/knowledge_graph/ingestion.py
- **Line 24**: `from services.llm.clients import llm_client`
- **Usage**: Knowledge graph relationship analysis

### 4. services/integrations/github/issue_analyzer.py
- **Line 15**: `from services.llm.clients import llm_client`
- **Usage**: GitHub issue analysis

### 5. services/integrations/github/content_generator.py
- **Line 11**: `from services.llm.clients import LLMClient`
- **Usage**: GitHub content generation

### 6. services/project_context/project_context.py
- **Line 5**: `from services.llm.clients import LLMClient`
- **Usage**: Project context inference

### 7. services/orchestration/engine.py
- **Line 32**: `from services.llm.clients import LLMClient`
- **Line 73**: `from services.llm.clients import llm_client as global_llm_client`
- **Usage**: Orchestration engine LLM operations

### 8. services/domain/work_item_extractor.py
- **Line 14**: `from services.llm.clients import LLMClient`
- **Usage**: Work item extraction

### 9. web/app.py
- **Line 82**: `from services.llm.clients import llm_client`
- **Usage**: Web app orchestration initialization

### 10. scripts/workflow_reality_check.py
- **Line 28**: `from services.llm.clients import llm_client`
- **Usage**: Workflow validation script

---

## Infrastructure Files (DO NOT UPDATE)

These files are part of the infrastructure layer and should keep their current imports:

1. **services/llm/clients.py** - Infrastructure layer
   - Line 15: `from services.config.llm_config_service import LLMConfigService`
   - Reason: This IS the client implementation

2. **services/llm/provider_selector.py** - Infrastructure layer
   - Line 12: `from services.config.llm_config_service import LLMConfigService`
   - Reason: Infrastructure component

3. **services/domain/llm_domain_service.py** - Already correct
   - Lines 10-11: Uses LLMConfigService and ProviderSelector correctly
   - Line 100: Imports llm_client correctly for initialization
   - Reason: Domain service - already follows correct pattern

---

## Dev/Test Files (SKIP FOR NOW)

These are in dev/ directory for testing purposes:

1. dev/2025/10/06/test_all_intent_handlers.py - line 16
2. dev/2025/10/06/test_execution_handler.py - line 19
3. dev/2025/10/06/trace_canonical_routing.py - line 11

**Recommendation**: Skip these for Phase 2 - they're one-off test scripts

---

## Analysis Files (Dependency Injection Pattern)

These files receive llm_client as a constructor parameter - they don't import it:

1. services/analysis/text_analyzer.py - uses `self.llm_client` (injected)
2. services/analysis/document_analyzer.py - uses `self.llm_client` (injected)
3. services/analysis/file_analyzer.py - uses `self.llm_client` (injected)
4. services/analysis/analyzer_factory.py - passes llm_client to analyzers

**Status**: Already following good DI pattern - no changes needed

---

## Discrepancy from Phase 0

**Phase 0 reported**: 13 active consumers
**Phase 2 found**: 10 production consumers

**Explanation**:
- Phase 0 counted files that import `llm_client`
- Some files use dependency injection instead of direct import
- Some imports are in dev/test files (not production)
- Infrastructure files correctly excluded

**Decision**: Proceed with 10 production consumers
**New target**: 40 checkmarks (10 consumers × 4 checks each)

---

## Migration Checklist (10 Consumers × 4 Checks = 40 Total)

Consumer                                        | Updated | Imports | Tested | Works
----------------------------------------------- | ------- | ------- | ------ | -----
1. services/intent_service/classifier.py        | [ ]     | [ ]     | [ ]    | [ ]
2. services/intent_service/llm_classifier.py    | [ ]     | [ ]     | [ ]    | [ ]
3. services/knowledge_graph/ingestion.py        | [ ]     | [ ]     | [ ]    | [ ]
4. services/integrations/github/issue_analyzer  | [ ]     | [ ]     | [ ]    | [ ]
5. services/integrations/github/content_gen     | [ ]     | [ ]     | [ ]    | [ ]
6. services/project_context/project_context.py  | [ ]     | [ ]     | [ ]    | [ ]
7. services/orchestration/engine.py             | [ ]     | [ ]     | [ ]    | [ ]
8. services/domain/work_item_extractor.py       | [ ]     | [ ]     | [ ]    | [ ]
9. web/app.py                                   | [ ]     | [ ]     | [ ]    | [ ]
10. scripts/workflow_reality_check.py           | [ ]     | [ ]     | [ ]    | [ ]
----------------------------------------------- | ------- | ------- | ------ | -----
TOTAL: 0/40 checkmarks = 0% complete

---

**Next**: Start migration with Consumer #1
