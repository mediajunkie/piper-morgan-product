# Prompt for Cursor Agent: GREAT-4D Phase 2 - ANALYSIS Handler Implementation

## Context

Phase 1 complete: EXECUTION handler implemented, placeholder removed.

**Target file**: `services/intent/intent_service.py`
**Pattern to follow**: `_handle_execution_intent()` just created by Code Agent
**Task**: Implement ANALYSIS handler following same pattern

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Implement `_handle_analysis_intent` following the EXECUTION pattern that Code just created.

---

## Phase 2: ANALYSIS Handler Implementation

### Step 1: Study the EXECUTION Pattern Just Created

Code just implemented this pattern in `services/intent/intent_service.py`:

```python
async def _handle_execution_intent(self, intent, workflow, session_id):
    """Routes to appropriate domain service based on intent action."""

    if intent.action in ["create_issue", "create_ticket"]:
        return await self._handle_create_issue(...)
    elif intent.action in ["update_issue", "update_ticket"]:
        return await self._handle_update_issue(...)
    else:
        # Generic handler via orchestration
        result = await self.orchestration_engine.handle_execution_intent(intent)
        ...
```

**Follow this exact pattern for ANALYSIS**.

### Step 2: Implement _handle_analysis_intent

Edit: `services/intent/intent_service.py`

Add after the EXECUTION handlers:

```python
async def _handle_analysis_intent(
    self, intent: Intent, workflow, session_id: str
) -> IntentProcessingResult:
    """
    Handle ANALYSIS category intents.

    Routes to appropriate analysis service based on intent action.
    Follows EXECUTION/QUERY pattern for consistency.
    """
    self.logger.info(f"Processing ANALYSIS intent: {intent.action}")

    # Route based on action
    if intent.action in ["analyze_commits", "analyze_code"]:
        return await self._handle_analyze_commits(intent, workflow.id)

    elif intent.action in ["generate_report", "create_report"]:
        return await self._handle_generate_report(intent, workflow.id)

    elif intent.action in ["analyze_data", "evaluate_metrics"]:
        return await self._handle_analyze_data(intent, workflow.id)

    else:
        # Generic analysis handler - route to orchestration
        self.logger.info(f"Routing generic ANALYSIS to orchestration: {intent.action}")
        try:
            result = await self.orchestration_engine.handle_analysis_intent(intent)
            return IntentProcessingResult(
                success=True,
                message=f"Analysis processed: {intent.action}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=False,
            )
        except Exception as e:
            self.logger.error(f"Analysis handler error: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze: {str(e)}",
                workflow_id=workflow.id,
                error=str(e),
                error_type="AnalysisError",
            )
```

### Step 3: Implement Specific Analysis Handlers

Add handlers for common analysis actions:

```python
async def _handle_analyze_commits(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """Handle commit analysis requests."""
    try:
        from services.analysis.document_analyzer import DocumentAnalyzer

        analyzer = DocumentAnalyzer()

        # Extract analysis parameters from intent
        repository = intent.context.get("repository")
        timeframe = intent.context.get("timeframe", "last 7 days")

        # Perform analysis
        analysis = await analyzer.analyze_commits(
            repository=repository,
            timeframe=timeframe
        )

        return IntentProcessingResult(
            success=True,
            message=f"Analyzed commits for {timeframe}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "analysis_summary": analysis.get("summary"),
                "commit_count": analysis.get("count"),
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    except Exception as e:
        self.logger.error(f"Failed to analyze commits: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to analyze commits: {str(e)}",
            workflow_id=workflow_id,
            error=str(e),
            error_type="AnalysisError",
        )

async def _handle_generate_report(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """Handle report generation requests."""
    try:
        # For now, return placeholder with clear message
        # (Real implementation would use reporting service)
        return IntentProcessingResult(
            success=True,
            message="Report generation handler is ready but needs reporting service integration.",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "report_type": intent.context.get("report_type", "general"),
            },
            workflow_id=workflow_id,
            requires_clarification=True,
            clarification_type="report_parameters",
        )

    except Exception as e:
        self.logger.error(f"Failed to generate report: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to generate report: {str(e)}",
            workflow_id=workflow_id,
            error=str(e),
            error_type="ReportError",
        )

async def _handle_analyze_data(
    self, intent: Intent, workflow_id: str
) -> IntentProcessingResult:
    """Handle general data analysis requests."""
    try:
        # Route to appropriate analysis based on context
        data_type = intent.context.get("data_type", "unknown")

        return IntentProcessingResult(
            success=True,
            message=f"Data analysis handler ready for {data_type} analysis",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "data_type": data_type,
            },
            workflow_id=workflow_id,
            requires_clarification=True,
            clarification_type="analysis_parameters",
        )

    except Exception as e:
        self.logger.error(f"Failed to analyze data: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to analyze data: {str(e)}",
            workflow_id=workflow_id,
            error=str(e),
            error_type="AnalysisError",
        )
```

### Step 4: Update Main Routing

Find where Code added the EXECUTION case and add ANALYSIS after it:

```python
# Find this section Code added:
elif intent.category == IntentCategory.EXECUTION:
    return await self._handle_execution_intent(intent, workflow, session_id)

# Add right after:
elif intent.category == IntentCategory.ANALYSIS:
    return await self._handle_analysis_intent(intent, workflow, session_id)
```

### Step 5: Test ANALYSIS Handler

Create: `dev/2025/10/06/test_analysis_handler.py`

```python
"""Test ANALYSIS intent handler - GREAT-4D Phase 2"""
import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService
from services.intent_service import classifier


async def test_analysis_handler():
    """Test that ANALYSIS intents work, not placeholder."""

    print("=" * 80)
    print("ANALYSIS HANDLER TEST - GREAT-4D Phase 2")
    print("=" * 80)

    intent_service = IntentService()

    # Test analyze commits intent
    print("\n1. Testing analyze_commits intent:")
    intent = await classifier.classify("analyze the recent commits")
    print(f"   Category: {intent.category.value}")
    print(f"   Action: {intent.action}")

    result = await intent_service.process(intent, session_id="test_session")
    print(f"   Success: {result.success}")
    print(f"   Message: {result.message}")

    # Check for placeholder message
    if "Phase 3" in result.message or "full orchestration workflow" in result.message:
        print("   ❌ FAILED - Still returning placeholder message")
        return False
    else:
        print("   ✅ PASSED - No placeholder message")

    # Test generic analysis
    print("\n2. Testing generic ANALYSIS action:")
    intent2 = await classifier.classify("analyze the performance data")
    result2 = await intent_service.process(intent2, session_id="test_session")
    print(f"   Message: {result2.message}")

    if "Phase 3" not in result2.message:
        print("   ✅ PASSED - Generic ANALYSIS working")
    else:
        print("   ❌ FAILED - Generic ANALYSIS still placeholder")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_analysis_handler())
    if success:
        print("\n✅ ANALYSIS handler working - placeholder removed!")
    else:
        print("\n❌ ANALYSIS handler still has issues")
```

Run test:
```bash
PYTHONPATH=. python3 dev/2025/10/06/test_analysis_handler.py
```

---

## Anti-80% Checklist

Track completion of all work:

```
Component              | Implemented | Tested | Integrated | Documented
---------------------- | ----------- | ------ | ---------- | ----------
_handle_analysis_intent| [ ]         | [ ]    | [ ]        | [ ]
_handle_analyze_commits| [ ]         | [ ]    | [ ]        | [ ]
_handle_generate_report| [ ]         | [ ]    | [ ]        | [ ]
_handle_analyze_data   | [ ]         | [ ]    | [ ]        | [ ]
Main routing updated   | [ ]         | [ ]    | [ ]        | [ ]
Test created           | [ ]         | [ ]    | [ ]        | [ ]
Test passing           | [ ]         | [ ]    | [ ]        | [ ]
No Phase 3 references  | [ ]         | [ ]    | [ ]        | [ ]
TOTAL: 0/32 checkmarks = 0% (Must reach 100%)
```

Update this checklist as you complete each item.

---

## Success Criteria

- [ ] `_handle_analysis_intent` implemented following EXECUTION pattern
- [ ] At least 3 specific analysis handlers implemented
- [ ] Main routing updated to call ANALYSIS handler
- [ ] Test shows no "Phase 3" placeholder message
- [ ] Test shows handler attempts analysis
- [ ] Anti-80% checklist at 100%
- [ ] Session log updated

---

## Evidence Format

```bash
$ PYTHONPATH=. python3 dev/2025/10/06/test_analysis_handler.py
=== ANALYSIS HANDLER TEST ===

1. Testing analyze_commits intent:
   Category: ANALYSIS
   Action: analyze_commits
   Success: True
   Message: Analyzed commits for last 7 days
   ✅ PASSED - No placeholder message

2. Testing generic ANALYSIS action:
   Message: Analysis processed: analyze_data
   ✅ PASSED - Generic ANALYSIS working

✅ ANALYSIS handler working - placeholder removed!
```

---

**Effort**: Small-Medium (~30-45 minutes)
**Priority**: HIGH (completes handler implementation)
**Pattern**: Follow EXECUTION exactly - just created by Code
