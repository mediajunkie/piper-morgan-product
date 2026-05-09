# Pattern-024: Methodology Patterns

## Status

**Superseded** — superseded by `methodology-00-EXCELLENCE-FLYWHEEL.md` v2.0 (published 2026-04-26 commit `fa0e71a3`). Implementation file `services/orchestration/excellence_flywheel_integration.py` retired 2026-04-28 commit `adfd453b` per CIO M1 audit recommendation A3 (Lead Dev disposition: zero production importers). Status updated 2026-05-09 by CIO during Pattern Sweep #1025 (catalog-hygiene cleanup; usage index showed 200 references but the underlying canonical content has moved to methodology-00 v2.0). Pattern content preserved here for historical reference; Excellence Flywheel principles operate via methodology-00 v2.0's three-layer canonical formulation (Concept / Practice / Mnemonic).

## Context

Large-scale software development projects require systematic methodologies to maintain quality, consistency, and reliability across teams and over time. Without established methodology patterns, development becomes inconsistent, quality suffers, and teams struggle with coordination and knowledge transfer. The Methodology Patterns represent the systematic application of development methodologies discovered through comprehensive pattern analysis. These patterns address:

- What challenges does this solve? Provides systematic application of development methodologies across the codebase with deep integration of Excellence Flywheel approach
- When should this pattern be considered? When building systematic development practices that need verification-first approaches and evidence-based progress tracking
- What are the typical scenarios where this applies? Development workflow consistency, systematic verification, root cause analysis, testing infrastructure, multi-agent coordination

## Pattern Description

The Methodology Patterns represent the systematic application of development methodologies across the codebase, discovered through pattern sweep analysis. They demonstrate the deep integration of the Excellence Flywheel methodology and architectural consistency with evidence-based development practices, systematic verification, and comprehensive testing approaches.

Core concepts:
- Systematic verification methodology for evidence-based development
- Root cause identification patterns for thorough problem solving
- Comprehensive async testing infrastructure with consistent patterns
- Workflow type standardization for multi-agent coordination
- PM ticket resolution patterns for systematic completion tracking

## Implementation

### 24.1 Systematic Verification Methodology Pattern

```python
from typing import Dict, List, Any, Optional
import subprocess
import logging
from datetime import datetime
from dataclasses import dataclass

@dataclass
class VerificationResult:
    """Result of a systematic verification step"""
    step_name: str
    success: bool
    evidence: Dict[str, Any]
    timestamp: datetime
    command_executed: Optional[str] = None
    output: Optional[str] = None
    error_message: Optional[str] = None

class SystematicVerificationEngine:
    """Deep integration of systematic verification methodology across development work"""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.verification_history: List[VerificationResult] = []
        self.logger = logging.getLogger(__name__)

        # Verification steps registry
        self.verification_steps = {
            "check_existing_patterns": self._check_existing_patterns,
            "verify_domain_models": self._verify_domain_models,
            "validate_implementations": self._validate_implementations,
            "check_dependencies": self._check_dependencies,
            "verify_test_coverage": self._verify_test_coverage,
            "validate_architecture": self._validate_architecture
        }

    async def execute_verification_protocol(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete verification protocol before implementation"""
        verification_results = []

        # Phase 1: Pattern and Model Verification
        pattern_check = await self._execute_verification_step(
            "check_existing_patterns",
            task_context
        )
        verification_results.append(pattern_check)

        domain_check = await self._execute_verification_step(
            "verify_domain_models",
            task_context
        )
        verification_results.append(domain_check)

        # Phase 2: Implementation and Dependency Verification
        impl_check = await self._execute_verification_step(
            "validate_implementations",
            task_context
        )
        verification_results.append(impl_check)

        dep_check = await self._execute_verification_step(
            "check_dependencies",
            task_context
        )
        verification_results.append(dep_check)

        # Phase 3: Quality and Architecture Verification
        test_check = await self._execute_verification_step(
            "verify_test_coverage",
            task_context
        )
        verification_results.append(test_check)

        arch_check = await self._execute_verification_step(
            "validate_architecture",
            task_context
        )
        verification_results.append(arch_check)

        # Compile comprehensive verification report
        return self._compile_verification_report(verification_results, task_context)

    async def _execute_verification_step(self, step_name: str, context: Dict[str, Any]) -> VerificationResult:
        """Execute individual verification step with evidence collection"""
        start_time = datetime.utcnow()

        try:
            step_function = self.verification_steps[step_name]
            result = await step_function(context)

            verification_result = VerificationResult(
                step_name=step_name,
                success=result["success"],
                evidence=result["evidence"],
                timestamp=start_time,
                command_executed=result.get("command"),
                output=result.get("output")
            )

            self.verification_history.append(verification_result)
            self.logger.info(f"Verification step '{step_name}': {'✅ PASSED' if result['success'] else '❌ FAILED'}")

            return verification_result

        except Exception as e:
            error_result = VerificationResult(
                step_name=step_name,
                success=False,
                evidence={"error": str(e)},
                timestamp=start_time,
                error_message=str(e)
            )

            self.verification_history.append(error_result)
            self.logger.error(f"Verification step '{step_name}' failed: {e}")

            return error_result

    async def _check_existing_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify existing patterns before creating new ones"""
        pattern_checks = []

        # Check if pattern already exists
        pattern_name = context.get("pattern_name", "")
        if pattern_name:
            command = f"find {self.project_root} -name '*{pattern_name.lower()}*' -type f"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            pattern_checks.append({
                "check": "existing_pattern_files",
                "command": command,
                "found_files": result.stdout.strip().split('\n') if result.stdout.strip() else [],
                "pattern_exists": bool(result.stdout.strip())
            })

        # Check pattern catalog for existing patterns
        catalog_command = f"grep -r 'Pattern.*{pattern_name}' {self.project_root}/docs/patterns/ || true"
        catalog_result = subprocess.run(catalog_command, shell=True, capture_output=True, text=True)

        pattern_checks.append({
            "check": "pattern_catalog_search",
            "command": catalog_command,
            "matches": catalog_result.stdout.strip().split('\n') if catalog_result.stdout.strip() else [],
            "found_in_catalog": bool(catalog_result.stdout.strip())
        })

        # Check for similar patterns
        if context.get("keywords"):
            for keyword in context["keywords"]:
                keyword_command = f"grep -r '{keyword}' {self.project_root}/docs/patterns/ || true"
                keyword_result = subprocess.run(keyword_command, shell=True, capture_output=True, text=True)

                pattern_checks.append({
                    "check": f"keyword_search_{keyword}",
                    "command": keyword_command,
                    "matches": keyword_result.stdout.strip().split('\n') if keyword_result.stdout.strip() else [],
                    "found_keyword": bool(keyword_result.stdout.strip())
                })

        success = all(not check.get("pattern_exists", False) for check in pattern_checks)

        return {
            "success": success,
            "evidence": {
                "pattern_checks": pattern_checks,
                "verification_type": "existing_patterns",
                "recommendation": "Proceed with pattern creation" if success else "Review existing patterns first"
            }
        }

    async def _verify_domain_models(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check domain models and implementations before starting work"""
        model_checks = []

        # Check main domain models file
        models_command = f"cat {self.project_root}/services/domain/models.py | head -50"
        models_result = subprocess.run(models_command, shell=True, capture_output=True, text=True)

        model_checks.append({
            "check": "domain_models_exists",
            "command": models_command,
            "content_preview": models_result.stdout[:500] if models_result.stdout else "",
            "file_exists": models_result.returncode == 0
        })

        # Check shared types
        types_command = f"cat {self.project_root}/services/shared_types.py | grep 'Enum' || true"
        types_result = subprocess.run(types_command, shell=True, capture_output=True, text=True)

        model_checks.append({
            "check": "shared_types_enums",
            "command": types_command,
            "enums_found": types_result.stdout.strip().split('\n') if types_result.stdout.strip() else [],
            "enum_count": len(types_result.stdout.strip().split('\n')) if types_result.stdout.strip() else 0
        })

        # Check for specific models mentioned in context
        if context.get("required_models"):
            for model_name in context["required_models"]:
                model_command = f"grep -r 'class {model_name}' {self.project_root}/services/ || true"
                model_result = subprocess.run(model_command, shell=True, capture_output=True, text=True)

                model_checks.append({
                    "check": f"model_{model_name}_exists",
                    "command": model_command,
                    "model_found": bool(model_result.stdout.strip()),
                    "locations": model_result.stdout.strip().split('\n') if model_result.stdout.strip() else []
                })

        success = all(check.get("file_exists", True) for check in model_checks)

        return {
            "success": success,
            "evidence": {
                "model_checks": model_checks,
                "verification_type": "domain_models",
                "models_accessible": success
            }
        }

    async def _validate_implementations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate existing implementations before modification"""
        impl_checks = []

        # Check if implementation files exist
        if context.get("target_files"):
            for file_path in context["target_files"]:
                full_path = f"{self.project_root}/{file_path}"
                check_command = f"ls -la '{full_path}' || echo 'File not found'"
                check_result = subprocess.run(check_command, shell=True, capture_output=True, text=True)

                impl_checks.append({
                    "check": f"file_exists_{file_path}",
                    "command": check_command,
                    "file_path": file_path,
                    "exists": "File not found" not in check_result.stdout,
                    "details": check_result.stdout.strip()
                })

        # Check for conflicting implementations
        if context.get("implementation_patterns"):
            for pattern in context["implementation_patterns"]:
                pattern_command = f"grep -r '{pattern}' {self.project_root}/services/ || true"
                pattern_result = subprocess.run(pattern_command, shell=True, capture_output=True, text=True)

                impl_checks.append({
                    "check": f"pattern_{pattern}_usage",
                    "command": pattern_command,
                    "pattern": pattern,
                    "found_usage": bool(pattern_result.stdout.strip()),
                    "usage_locations": pattern_result.stdout.strip().split('\n') if pattern_result.stdout.strip() else []
                })

        success = True  # Implementation validation is informational

        return {
            "success": success,
            "evidence": {
                "implementation_checks": impl_checks,
                "verification_type": "implementations",
                "ready_for_modification": success
            }
        }

    async def _check_dependencies(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check project dependencies and configurations"""
        dep_checks = []

        # Check Python dependencies
        pip_command = "pip list | head -20"
        pip_result = subprocess.run(pip_command, shell=True, capture_output=True, text=True)

        dep_checks.append({
            "check": "python_dependencies",
            "command": pip_command,
            "dependencies_sample": pip_result.stdout.strip().split('\n')[:10] if pip_result.stdout.strip() else [],
            "pip_accessible": pip_result.returncode == 0
        })

        # Check requirements.txt if it exists
        req_command = f"ls {self.project_root}/requirements*.txt || echo 'No requirements files'"
        req_result = subprocess.run(req_command, shell=True, capture_output=True, text=True)

        dep_checks.append({
            "check": "requirements_files",
            "command": req_command,
            "requirements_files": req_result.stdout.strip().split('\n') if "No requirements" not in req_result.stdout else [],
            "has_requirements": "No requirements" not in req_result.stdout
        })

        # Check for specific dependencies mentioned in context
        if context.get("required_dependencies"):
            for dep in context["required_dependencies"]:
                dep_command = f"pip show {dep} || echo 'Package not found'"
                dep_result = subprocess.run(dep_command, shell=True, capture_output=True, text=True)

                dep_checks.append({
                    "check": f"dependency_{dep}",
                    "command": dep_command,
                    "dependency": dep,
                    "installed": "Package not found" not in dep_result.stdout,
                    "version_info": dep_result.stdout.strip() if "Package not found" not in dep_result.stdout else None
                })

        success = True  # Dependency check is informational

        return {
            "success": success,
            "evidence": {
                "dependency_checks": dep_checks,
                "verification_type": "dependencies",
                "environment_ready": success
            }
        }

    async def _verify_test_coverage(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify test coverage and testing infrastructure"""
        test_checks = []

        # Check test directory structure
        test_command = f"find {self.project_root}/tests -type f -name '*.py' | head -10"
        test_result = subprocess.run(test_command, shell=True, capture_output=True, text=True)

        test_checks.append({
            "check": "test_files_exist",
            "command": test_command,
            "test_files": test_result.stdout.strip().split('\n') if test_result.stdout.strip() else [],
            "test_count": len(test_result.stdout.strip().split('\n')) if test_result.stdout.strip() else 0
        })

        # Check for pytest markers
        marker_command = f"grep -r '@pytest.mark.asyncio' {self.project_root}/tests/ | wc -l || echo '0'"
        marker_result = subprocess.run(marker_command, shell=True, capture_output=True, text=True)

        test_checks.append({
            "check": "asyncio_markers",
            "command": marker_command,
            "async_test_count": int(marker_result.stdout.strip()) if marker_result.stdout.strip().isdigit() else 0,
            "has_async_tests": int(marker_result.stdout.strip()) > 0 if marker_result.stdout.strip().isdigit() else False
        })

        # Check for test patterns mentioned in context
        if context.get("test_patterns"):
            for pattern in context["test_patterns"]:
                pattern_command = f"grep -r '{pattern}' {self.project_root}/tests/ || true"
                pattern_result = subprocess.run(pattern_command, shell=True, capture_output=True, text=True)

                test_checks.append({
                    "check": f"test_pattern_{pattern}",
                    "command": pattern_command,
                    "pattern": pattern,
                    "pattern_found": bool(pattern_result.stdout.strip()),
                    "pattern_usage": pattern_result.stdout.strip().split('\n') if pattern_result.stdout.strip() else []
                })

        success = any(check.get("test_count", 0) > 0 for check in test_checks)

        return {
            "success": success,
            "evidence": {
                "test_checks": test_checks,
                "verification_type": "test_coverage",
                "testing_infrastructure_ready": success
            }
        }

    async def _validate_architecture(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate architectural consistency"""
        arch_checks = []

        # Check ADR directory
        adr_command = f"ls {self.project_root}/docs/architecture/decisions/ | wc -l || echo '0'"
        adr_result = subprocess.run(adr_command, shell=True, capture_output=True, text=True)

        arch_checks.append({
            "check": "adr_documents",
            "command": adr_command,
            "adr_count": int(adr_result.stdout.strip()) if adr_result.stdout.strip().isdigit() else 0,
            "has_adrs": int(adr_result.stdout.strip()) > 0 if adr_result.stdout.strip().isdigit() else False
        })

        # Check pattern documentation
        pattern_command = f"ls {self.project_root}/docs/patterns/ | wc -l || echo '0'"
        pattern_result = subprocess.run(pattern_command, shell=True, capture_output=True, text=True)

        arch_checks.append({
            "check": "pattern_documents",
            "command": pattern_command,
            "pattern_count": int(pattern_result.stdout.strip()) if pattern_result.stdout.strip().isdigit() else 0,
            "has_patterns": int(pattern_result.stdout.strip()) > 0 if pattern_result.stdout.strip().isdigit() else False
        })

        # Check architecture documentation
        arch_doc_command = f"ls {self.project_root}/docs/architecture/ | head -5"
        arch_doc_result = subprocess.run(arch_doc_command, shell=True, capture_output=True, text=True)

        arch_checks.append({
            "check": "architecture_docs",
            "command": arch_doc_command,
            "arch_files": arch_doc_result.stdout.strip().split('\n') if arch_doc_result.stdout.strip() else [],
            "has_arch_docs": bool(arch_doc_result.stdout.strip())
        })

        success = all(check.get("has_adrs", False) or check.get("has_patterns", False) or check.get("has_arch_docs", False) for check in arch_checks)

        return {
            "success": success,
            "evidence": {
                "architecture_checks": arch_checks,
                "verification_type": "architecture",
                "architecture_documented": success
            }
        }

    def _compile_verification_report(self, results: List[VerificationResult], context: Dict[str, Any]) -> Dict[str, Any]:
        """Compile comprehensive verification report"""
        total_steps = len(results)
        passed_steps = sum(1 for r in results if r.success)

        report = {
            "verification_complete": True,
            "total_steps": total_steps,
            "passed_steps": passed_steps,
            "success_rate": passed_steps / total_steps if total_steps > 0 else 0,
            "overall_success": passed_steps >= (total_steps * 0.8),  # 80% pass rate required
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
            "step_results": [],
            "recommendations": []
        }

        for result in results:
            report["step_results"].append({
                "step": result.step_name,
                "success": result.success,
                "evidence_summary": self._summarize_evidence(result.evidence),
                "timestamp": result.timestamp.isoformat()
            })

            if not result.success:
                report["recommendations"].append(f"Address issues in {result.step_name}: {result.error_message or 'See evidence details'}")

        if report["overall_success"]:
            report["recommendations"].append("✅ Verification passed - proceed with implementation")
        else:
            report["recommendations"].append("❌ Verification failed - address issues before proceeding")

        return report

    def _summarize_evidence(self, evidence: Dict[str, Any]) -> str:
        """Create human-readable summary of evidence"""
        if evidence.get("error"):
            return f"Error: {evidence['error']}"

        verification_type = evidence.get("verification_type", "unknown")

        if verification_type == "existing_patterns":
            pattern_exists = any(check.get("pattern_exists", False) for check in evidence.get("pattern_checks", []))
            return f"Pattern existence check: {'Found existing' if pattern_exists else 'No conflicts found'}"

        elif verification_type == "domain_models":
            models_accessible = evidence.get("models_accessible", False)
            return f"Domain models: {'Accessible' if models_accessible else 'Issues found'}"

        elif verification_type == "test_coverage":
            has_tests = evidence.get("testing_infrastructure_ready", False)
            return f"Test infrastructure: {'Ready' if has_tests else 'Needs setup'}"

        else:
            return f"{verification_type}: {'Success' if evidence.get('success', False) else 'Issues found'}"
```

### 24.2 Root Cause Identification Pattern

```python
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import traceback
import logging

class ProblemCategory(Enum):
    TECHNICAL = "technical"
    PROCESS = "process"
    CONFIGURATION = "configuration"
    INTEGRATION = "integration"
    DATA = "data"
    PERFORMANCE = "performance"

@dataclass
class RootCauseAnalysisResult:
    """Result of root cause analysis investigation"""
    problem_description: str
    category: ProblemCategory
    root_causes: List[str]
    contributing_factors: List[str]
    evidence: Dict[str, Any]
    recommended_solutions: List[str]
    verification_steps: List[str]
    confidence_level: float

class RootCauseIdentificationEngine:
    """Systematic approach to identifying and resolving root causes of issues"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_history: List[RootCauseAnalysisResult] = []

        # Analysis framework mapping
        self.analysis_frameworks = {
            ProblemCategory.TECHNICAL: self._analyze_technical_problem,
            ProblemCategory.PROCESS: self._analyze_process_problem,
            ProblemCategory.CONFIGURATION: self._analyze_configuration_problem,
            ProblemCategory.INTEGRATION: self._analyze_integration_problem,
            ProblemCategory.DATA: self._analyze_data_problem,
            ProblemCategory.PERFORMANCE: self._analyze_performance_problem
        }

    async def analyze_problem(self, problem_description: str, error_context: Dict[str, Any] = None) -> RootCauseAnalysisResult:
        """Perform comprehensive root cause analysis"""
        # Step 1: Categorize the problem
        category = self._categorize_problem(problem_description, error_context)

        # Step 2: Apply category-specific analysis framework
        analysis_framework = self.analysis_frameworks[category]
        analysis_result = await analysis_framework(problem_description, error_context or {})

        # Step 3: Identify root causes using systematic approach
        root_causes = await self._identify_root_causes(analysis_result, category)

        # Step 4: Determine contributing factors
        contributing_factors = await self._identify_contributing_factors(analysis_result, category)

        # Step 5: Generate recommended solutions
        solutions = await self._generate_solutions(root_causes, contributing_factors, category)

        # Step 6: Create verification steps
        verification_steps = await self._create_verification_steps(solutions, category)

        # Step 7: Calculate confidence level
        confidence = self._calculate_confidence_level(analysis_result, root_causes)

        result = RootCauseAnalysisResult(
            problem_description=problem_description,
            category=category,
            root_causes=root_causes,
            contributing_factors=contributing_factors,
            evidence=analysis_result,
            recommended_solutions=solutions,
            verification_steps=verification_steps,
            confidence_level=confidence
        )

        self.analysis_history.append(result)
        return result

    def _categorize_problem(self, description: str, context: Dict[str, Any]) -> ProblemCategory:
        """Categorize problem based on description and context"""
        description_lower = description.lower()

        # Technical issues
        if any(keyword in description_lower for keyword in ["error", "exception", "crash", "bug", "failure"]):
            return ProblemCategory.TECHNICAL

        # Performance issues
        if any(keyword in description_lower for keyword in ["slow", "timeout", "performance", "latency"]):
            return ProblemCategory.PERFORMANCE

        # Configuration issues
        if any(keyword in description_lower for keyword in ["config", "setting", "environment", "missing"]):
            return ProblemCategory.CONFIGURATION

        # Integration issues
        if any(keyword in description_lower for keyword in ["api", "service", "connection", "integration"]):
            return ProblemCategory.INTEGRATION

        # Data issues
        if any(keyword in description_lower for keyword in ["data", "database", "query", "migration"]):
            return ProblemCategory.DATA

        # Process issues
        if any(keyword in description_lower for keyword in ["workflow", "process", "procedure", "method"]):
            return ProblemCategory.PROCESS

        # Default to technical
        return ProblemCategory.TECHNICAL

    async def _analyze_technical_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical problems with systematic debugging"""
        analysis = {
            "stack_trace": context.get("stack_trace"),
            "error_type": context.get("error_type"),
            "error_message": context.get("error_message"),
            "affected_components": [],
            "system_state": {},
            "reproduction_steps": [],
            "environment_factors": {}
        }

        # Analyze stack trace if available
        if analysis["stack_trace"]:
            analysis["affected_components"] = self._extract_components_from_stack_trace(analysis["stack_trace"])

        # Analyze error patterns
        if analysis["error_message"]:
            analysis["error_patterns"] = self._identify_error_patterns(analysis["error_message"])

        # System state analysis
        analysis["system_state"] = await self._gather_system_state()

        return analysis

    async def _analyze_process_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze process and methodology problems"""
        analysis = {
            "process_step": context.get("process_step"),
            "expected_outcome": context.get("expected_outcome"),
            "actual_outcome": context.get("actual_outcome"),
            "process_gaps": [],
            "methodology_adherence": {},
            "communication_issues": [],
            "tooling_problems": []
        }

        # Analyze process adherence
        if context.get("methodology_used"):
            analysis["methodology_adherence"] = self._analyze_methodology_adherence(context["methodology_used"])

        return analysis

    async def _analyze_configuration_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze configuration and environment problems"""
        analysis = {
            "config_files": context.get("config_files", []),
            "environment_variables": context.get("environment_variables", {}),
            "missing_configs": [],
            "conflicting_configs": [],
            "default_overrides": [],
            "validation_results": {}
        }

        # Check for missing configurations
        if analysis["config_files"]:
            analysis["missing_configs"] = await self._check_missing_configs(analysis["config_files"])

        return analysis

    async def _analyze_integration_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze integration and API problems"""
        analysis = {
            "external_services": context.get("external_services", []),
            "api_endpoints": context.get("api_endpoints", []),
            "connectivity_issues": [],
            "authentication_problems": [],
            "data_format_issues": [],
            "version_compatibility": {}
        }

        # Check service connectivity
        for service in analysis["external_services"]:
            connectivity_result = await self._check_service_connectivity(service)
            analysis["connectivity_issues"].append(connectivity_result)

        return analysis

    async def _analyze_data_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and database problems"""
        analysis = {
            "affected_tables": context.get("affected_tables", []),
            "data_integrity_issues": [],
            "schema_problems": [],
            "migration_status": {},
            "query_performance": {},
            "data_consistency": {}
        }

        # Check data integrity
        for table in analysis["affected_tables"]:
            integrity_result = await self._check_data_integrity(table)
            analysis["data_integrity_issues"].append(integrity_result)

        return analysis

    async def _analyze_performance_problem(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance and latency problems"""
        analysis = {
            "performance_metrics": context.get("performance_metrics", {}),
            "bottlenecks": [],
            "resource_usage": {},
            "optimization_opportunities": [],
            "baseline_comparison": {},
            "profiling_results": {}
        }

        # Identify performance bottlenecks
        if analysis["performance_metrics"]:
            analysis["bottlenecks"] = self._identify_performance_bottlenecks(analysis["performance_metrics"])

        return analysis

    async def _identify_root_causes(self, analysis_result: Dict[str, Any], category: ProblemCategory) -> List[str]:
        """Identify root causes using category-specific logic"""
        root_causes = []

        if category == ProblemCategory.TECHNICAL:
            # Technical root cause identification
            if analysis_result.get("error_patterns"):
                for pattern in analysis_result["error_patterns"]:
                    if pattern["type"] == "null_pointer":
                        root_causes.append("Null value not properly handled in code path")
                    elif pattern["type"] == "import_error":
                        root_causes.append("Missing dependency or incorrect module path")
                    elif pattern["type"] == "timeout":
                        root_causes.append("Operation exceeded timeout threshold")

            if analysis_result.get("affected_components"):
                root_causes.append(f"Issue in components: {', '.join(analysis_result['affected_components'])}")

        elif category == ProblemCategory.CONFIGURATION:
            # Configuration root cause identification
            if analysis_result.get("missing_configs"):
                root_causes.append("Required configuration values not set")

            if analysis_result.get("conflicting_configs"):
                root_causes.append("Conflicting configuration values detected")

        elif category == ProblemCategory.PERFORMANCE:
            # Performance root cause identification
            if analysis_result.get("bottlenecks"):
                for bottleneck in analysis_result["bottlenecks"]:
                    root_causes.append(f"Performance bottleneck in {bottleneck['component']}: {bottleneck['description']}")

        # Add generic root cause if none found
        if not root_causes:
            root_causes.append("Root cause requires additional investigation")

        return root_causes

    async def _generate_solutions(self, root_causes: List[str], contributing_factors: List[str], category: ProblemCategory) -> List[str]:
        """Generate recommended solutions based on root causes"""
        solutions = []

        for root_cause in root_causes:
            if "null value" in root_cause.lower():
                solutions.append("Add null checks and defensive programming practices")
            elif "missing dependency" in root_cause.lower():
                solutions.append("Install missing dependencies and verify import paths")
            elif "timeout" in root_cause.lower():
                solutions.append("Increase timeout values or optimize operation performance")
            elif "configuration" in root_cause.lower():
                solutions.append("Review and correct configuration settings")
            elif "bottleneck" in root_cause.lower():
                solutions.append("Optimize performance bottleneck through code improvements")
            else:
                solutions.append(f"Address: {root_cause}")

        # Add category-specific solutions
        if category == ProblemCategory.TECHNICAL:
            solutions.append("Add comprehensive error handling and logging")
            solutions.append("Implement unit tests to prevent regression")

        elif category == ProblemCategory.PERFORMANCE:
            solutions.append("Implement performance monitoring and alerting")
            solutions.append("Add performance benchmarks to CI/CD pipeline")

        return solutions

    async def _create_verification_steps(self, solutions: List[str], category: ProblemCategory) -> List[str]:
        """Create verification steps to validate solutions"""
        verification_steps = []

        for solution in solutions:
            if "error handling" in solution.lower():
                verification_steps.append("Verify error handling covers all edge cases")
            elif "unit tests" in solution.lower():
                verification_steps.append("Run test suite and verify coverage improvement")
            elif "performance" in solution.lower():
                verification_steps.append("Run performance benchmarks and validate improvements")
            elif "configuration" in solution.lower():
                verification_steps.append("Validate configuration changes in test environment")
            else:
                verification_steps.append(f"Verify solution: {solution}")

        # Add final verification step
        verification_steps.append("Reproduce original problem to confirm resolution")

        return verification_steps

    def _calculate_confidence_level(self, analysis_result: Dict[str, Any], root_causes: List[str]) -> float:
        """Calculate confidence level in root cause analysis"""
        confidence_factors = []

        # Evidence quality factor
        if analysis_result.get("stack_trace"):
            confidence_factors.append(0.3)  # Stack trace provides strong evidence

        if analysis_result.get("error_message"):
            confidence_factors.append(0.2)  # Error message provides context

        # Root cause specificity factor
        generic_causes = sum(1 for cause in root_causes if "additional investigation" in cause)
        specific_causes = len(root_causes) - generic_causes
        if specific_causes > 0:
            confidence_factors.append(0.3 * (specific_causes / len(root_causes)))

        # Analysis completeness factor
        if len(analysis_result.keys()) > 3:
            confidence_factors.append(0.2)  # Comprehensive analysis

        return min(sum(confidence_factors), 1.0)

    # Helper methods for analysis frameworks
    def _extract_components_from_stack_trace(self, stack_trace: str) -> List[str]:
        """Extract affected components from stack trace"""
        components = []
        lines = stack_trace.split('\n')
        for line in lines:
            if 'File "' in line and 'services/' in line:
                # Extract service component from file path
                parts = line.split('services/')
                if len(parts) > 1:
                    component = parts[1].split('/')[0]
                    if component not in components:
                        components.append(component)
        return components

    def _identify_error_patterns(self, error_message: str) -> List[Dict[str, str]]:
        """Identify common error patterns"""
        patterns = []

        if "NoneType" in error_message:
            patterns.append({"type": "null_pointer", "description": "Null value access"})

        if "ModuleNotFoundError" in error_message:
            patterns.append({"type": "import_error", "description": "Missing module or dependency"})

        if "timeout" in error_message.lower():
            patterns.append({"type": "timeout", "description": "Operation timeout"})

        return patterns

    async def _gather_system_state(self) -> Dict[str, Any]:
        """Gather current system state for analysis"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "memory_usage": "Available through monitoring",
            "cpu_usage": "Available through monitoring",
            "active_connections": "Available through monitoring"
        }

    async def _check_service_connectivity(self, service: str) -> Dict[str, Any]:
        """Check connectivity to external service"""
        return {
            "service": service,
            "accessible": True,  # Would implement actual connectivity check
            "response_time": "< 100ms",
            "last_check": datetime.utcnow().isoformat()
        }
```

### 24.3 Async Test Marker Pattern

```python
import pytest
import asyncio
from typing import Any, Dict, List
from functools import wraps

class AsyncTestingFramework:
    """Comprehensive async testing infrastructure with consistent patterns"""

    def __init__(self):
        self.test_session_factory = None
        self.test_metrics = {
            "total_async_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "average_execution_time": 0.0
        }

    @staticmethod
    def async_test(func):
        """Decorator that ensures proper async test marking and setup"""
        @pytest.mark.asyncio
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"Async test {func.__name__} completed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Async test {func.__name__} failed after {execution_time:.3f}s: {e}")
                raise
        return wrapper

    @staticmethod
    def async_db_test(func):
        """Decorator for async tests that require database access"""
        @pytest.mark.asyncio
        @wraps(func)
        async def wrapper(session_factory, *args, **kwargs):
            async with session_factory.session_scope() as session:
                # Inject session into test function
                if 'session' in func.__code__.co_varnames:
                    kwargs['session'] = session
                result = await func(*args, **kwargs)
                # Session is automatically rolled back by session_scope
                return result
        return wrapper

# Usage examples for comprehensive test patterns
class TestSystematicVerification:
    """Test class demonstrating async test marker patterns"""

    @AsyncTestingFramework.async_test
    async def test_verification_protocol_execution(self):
        """Test systematic verification protocol"""
        engine = SystematicVerificationEngine("/test/project")
        context = {
            "pattern_name": "test_pattern",
            "keywords": ["test", "verification"]
        }

        result = await engine.execute_verification_protocol(context)

        assert result["verification_complete"] is True
        assert "step_results" in result
        assert len(result["step_results"]) > 0

    @AsyncTestingFramework.async_db_test
    async def test_domain_model_verification(self, session):
        """Test domain model verification with database access"""
        engine = SystematicVerificationEngine("/test/project")
        context = {
            "required_models": ["Project", "Workflow"]
        }

        result = await engine._verify_domain_models(context)

        assert result["success"] is True
        assert "model_checks" in result["evidence"]

    @AsyncTestingFramework.async_test
    async def test_root_cause_analysis(self):
        """Test root cause identification engine"""
        engine = RootCauseIdentificationEngine()
        error_context = {
            "error_type": "NullPointerException",
            "error_message": "NoneType object has no attribute 'id'",
            "stack_trace": "File services/domain/service.py line 42"
        }

        result = await engine.analyze_problem(
            "Application crashes when processing user request",
            error_context
        )

        assert result.category == ProblemCategory.TECHNICAL
        assert len(result.root_causes) > 0
        assert result.confidence_level > 0.5
```

## Usage Guidelines

### When to Use Methodology Patterns

- **Development Consistency**: When establishing systematic development practices across teams
- **Quality Assurance**: When implementing verification-first approaches and evidence-based progress tracking
- **Problem Resolution**: When systematic debugging and root cause analysis are required
- **Testing Infrastructure**: When building comprehensive async testing frameworks
- **Multi-Agent Coordination**: When coordinating work across multiple development agents

### Implementation Best Practices

- **Systematic Verification**: Always verify existing patterns before creating new ones
- **Evidence-Based Progress**: Document verification results with concrete evidence
- **Root Cause Analysis**: Use systematic debugging steps to identify and resolve root causes
- **Async Testing**: Mark all async tests with `@pytest.mark.asyncio` and use consistent patterns
- **Workflow Validation**: Validate workflow types before execution in multi-agent scenarios

### Methodology Integration

- **Excellence Flywheel**: Integrate systematic verification methodology across all development work
- **Cross-Validation**: Use cross-validation protocols for quality assurance
- **Documentation**: Maintain comprehensive documentation of verification results and resolution patterns
- **Testing Consistency**: Use AsyncSessionFactory.session_scope() for database tests

## Benefits

- Deep integration of systematic verification methodology across the codebase
- Evidence-based progress tracking with concrete verification results
- Comprehensive root cause analysis for thorough problem resolution
- Consistent async testing infrastructure with proper resource management
- Systematic workflow coordination for multi-agent development scenarios
- Quality assurance through verification-first approaches

## Trade-offs

- Additional overhead from systematic verification protocols
- Complexity in implementing comprehensive root cause analysis
- Time investment in evidence collection and documentation
- Need for consistent methodology adherence across teams
- Resource requirements for comprehensive testing infrastructure
- Coordination complexity in multi-agent development scenarios

## Anti-patterns to Avoid

- ❌ **Implementing Without Verification**: Skipping systematic verification steps before implementation
- ❌ **Claiming Success Without Evidence**: Making claims without concrete verification results
- ❌ **Symptom-Only Fixes**: Implementing solutions without identifying root causes
- ❌ **Missing Async Markers**: Forgetting `@pytest.mark.asyncio` on async tests
- ❌ **Inconsistent Testing Patterns**: Using different async testing approaches across the codebase
- ❌ **Manual Session Management**: Not using proper async session management in tests

## Related Patterns

- [Pattern-021: Development Session Management Pattern](pattern-021-development-session-management.md) - Session logging for methodology tracking
- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Repository pattern integration with async testing
- [Pattern-005: Transaction Management Pattern](pattern-005-transaction-management.md) - Transaction handling in async tests
- [Pattern-010: Cross-Validation Protocol Pattern](pattern-010-cross-validation-protocol.md) - Cross-validation methodology

## References

- **Detection Evidence**: 1,074 systematic verification occurrences, 1,036 root cause identification patterns, 574 async test markers
- **Implementation**: SystematicVerificationEngine, RootCauseIdentificationEngine, AsyncTestingFramework
- **Usage Evidence**: Excellence Flywheel methodology integration across 1,000+ files
- **Related ADR**: Excellence Flywheel methodology, systematic verification protocols

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#24-methodology-patterns` - Complete methodology pattern analysis with detection metrics
- Pattern sweep analysis results from August 22, 2025 showing deep integration
- Excellence Flywheel methodology implementation across codebase
- Systematic verification and root cause identification frameworks

*Last updated: September 15, 2025*
