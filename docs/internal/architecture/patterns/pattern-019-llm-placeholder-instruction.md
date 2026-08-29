# Pattern-019: LLM Placeholder Instruction Pattern

## Status

**Proven**

## Context

Large Language Models (LLMs) have a tendency to hallucinate or fabricate technical details when information is missing or uncertain, leading to inaccurate documentation, misleading error messages, and false technical claims. Without explicit instructions to handle uncertainty, LLMs may generate plausible-sounding but incorrect technical details, version numbers, error messages, or test results. The LLM Placeholder Instruction Pattern addresses:

- Preventing LLM hallucination in technical content generation
- Maintaining accuracy and trustworthiness in AI-generated documentation
- Providing clear communication about missing or uncertain information
- Establishing professional standards for AI-generated technical content
- Enabling reviewers to identify and fill knowledge gaps systematically
- Preventing misleading stakeholders with fabricated technical details

## Pattern Description

The LLM Placeholder Instruction Pattern prevents LLM hallucination by providing explicit instructions to use structured placeholders when information is missing or uncertain, rather than fabricating technical details. The pattern establishes three types of placeholders for different uncertainty scenarios and provides clear examples of what should not be fabricated.

## Implementation

### Structure

```python
# LLM placeholder instruction framework
class LLMPlaceholderInstructor:
    def __init__(self):
        self.placeholder_types = {
            'specific_example': 'SPECIFIC EXAMPLE NEEDED',
            'fact_check': 'FACT CHECK',
            'clarifying_question': 'QUESTION'
        }

    def generate_placeholder_instructions(self) -> str:
        """Generate comprehensive placeholder instructions for LLM prompts"""
        pass

    def validate_content(self, content: str) -> ContentValidationResult:
        """Validate content for proper placeholder usage"""
        pass

    def extract_placeholders(self, content: str) -> List[PlaceholderItem]:
        """Extract all placeholders for review and completion"""
        pass
```

### Example (Comprehensive Placeholder Instructions)

```python
# LLM prompt instructions for technical content generation
def get_llm_placeholder_instructions() -> str:
    """
    Generate comprehensive placeholder instructions to prevent LLM hallucination
    in technical content generation
    """
    return """
## PLACEHOLDER INSTRUCTIONS (CRITICAL FOR ACCURACY):

**NEVER fabricate specific technical details not provided in the user request.**

When information is missing or uncertain, use these explicit placeholders:

### 1. SPECIFIC EXAMPLE NEEDED
Use when concrete technical details are required but not provided:
- **[SPECIFIC EXAMPLE NEEDED: exact error message displayed]**
- **[SPECIFIC EXAMPLE NEEDED: actual API response format]**
- **[SPECIFIC EXAMPLE NEEDED: precise configuration values]**
- **[SPECIFIC EXAMPLE NEEDED: actual file paths and names]**

### 2. FACT CHECK
Use for unverified claims that need validation:
- **[FACT CHECK: browser versions where issue occurs]**
- **[FACT CHECK: performance metrics and benchmarks]**
- **[FACT CHECK: testing environments and results]**
- **[FACT CHECK: version compatibility matrix]**

### 3. QUESTION
Use when clarification is needed to avoid guessing:
- **[QUESTION: Which specific deployment environment?]**
- **[QUESTION: What authentication method is being used?]**
- **[QUESTION: Are there specific performance requirements?]**
- **[QUESTION: Which user roles need this functionality?]**

### EXAMPLES OF PROPER USAGE:

❌ WRONG (Fabricated):
```

Error message: "Connection timeout: Unable to reach server at localhost:3000"
Tested on Chrome 89, Firefox 86, Safari 14
Performance: Reduces load time by 40%

```

✅ CORRECT (With Placeholders):
```

Error message: [SPECIFIC EXAMPLE NEEDED: exact error message displayed]
Tested on [FACT CHECK: browser versions and environments where issue occurs]
Performance: [FACT CHECK: actual performance impact measurements]

```

### CRITICAL AREAS REQUIRING PLACEHOLDERS:
- Error messages and stack traces
- Version numbers and compatibility details
- Performance metrics and benchmarks
- Test results and coverage statistics
- Configuration values and environment details
- API responses and data formats
- File paths and system-specific details
"""

class TechnicalContentGenerator:
    """Generate technical content with proper placeholder usage"""

    def __init__(self):
        self.placeholder_instructions = get_llm_placeholder_instructions()

    def generate_documentation(self, user_request: str, context: Dict[str, Any]) -> str:
        """Generate documentation with placeholder instructions"""

        prompt = f"""
{self.placeholder_instructions}

## USER REQUEST:
{user_request}

## AVAILABLE CONTEXT:
{json.dumps(context, indent=2)}

## TASK:
Generate comprehensive documentation following the placeholder instructions above.
Use placeholders for any information not explicitly provided in the context.
"""

        # Send to LLM with placeholder instructions
        return self._send_to_llm(prompt)

    def validate_generated_content(self, content: str) -> ContentValidationResult:
        """Validate content for proper placeholder usage"""

        # Check for potential fabrications
        fabrication_indicators = [
            r'Error message: ["\'][^"\']*["\']',  # Quoted error messages
            r'Version \d+\.\d+\.\d+',  # Specific version numbers
            r'\d+% (improvement|reduction|faster)',  # Specific percentages
            r'Tested on [A-Z][a-z]+ \d+',  # Browser versions
        ]

        validation_issues = []
        for pattern in fabrication_indicators:
            matches = re.findall(pattern, content)
            if matches:
                validation_issues.append({
                    'type': 'potential_fabrication',
                    'pattern': pattern,
                    'matches': matches,
                    'recommendation': 'Replace with appropriate placeholder'
                })

        # Check for proper placeholder usage
        placeholder_count = len(re.findall(r'\[(?:SPECIFIC EXAMPLE NEEDED|FACT CHECK|QUESTION):[^\]]+\]', content))

        return ContentValidationResult(
            has_fabrications=len(validation_issues) > 0,
            placeholder_count=placeholder_count,
            validation_issues=validation_issues,
            recommendation=self._generate_validation_recommendation(validation_issues, placeholder_count)
        )
```

### Example (Content Review and Completion)

```python
class PlaceholderReviewManager:
    """Manage placeholder review and completion workflow"""

    def __init__(self):
        self.placeholder_tracker = {}

    def extract_placeholders(self, content: str) -> List[PlaceholderItem]:
        """Extract all placeholders from generated content"""

        placeholder_pattern = r'\[(SPECIFIC EXAMPLE NEEDED|FACT CHECK|QUESTION):\s*([^\]]+)\]'
        matches = re.findall(placeholder_pattern, content)

        placeholders = []
        for i, (placeholder_type, description) in enumerate(matches):
            placeholders.append(PlaceholderItem(
                id=f"placeholder_{i+1}",
                type=placeholder_type.lower().replace(' ', '_'),
                description=description.strip(),
                status='pending',
                priority=self._determine_priority(placeholder_type, description)
            ))

        return placeholders

    def create_review_checklist(self, placeholders: List[PlaceholderItem]) -> ReviewChecklist:
        """Create systematic review checklist for placeholder completion"""

        checklist_items = []

        # Group by type for systematic review
        by_type = {}
        for placeholder in placeholders:
            if placeholder.type not in by_type:
                by_type[placeholder.type] = []
            by_type[placeholder.type].append(placeholder)

        # Create checklist sections
        for placeholder_type, items in by_type.items():
            section_title = {
                'specific_example_needed': 'Technical Details to Provide',
                'fact_check': 'Claims to Verify',
                'question': 'Clarifications Needed'
            }[placeholder_type]

            checklist_items.append(ChecklistSection(
                title=section_title,
                items=[ChecklistItem(
                    id=item.id,
                    description=item.description,
                    priority=item.priority,
                    completed=False
                ) for item in items]
            ))

        return ReviewChecklist(
            title="LLM Placeholder Review",
            sections=checklist_items,
            completion_percentage=0.0
        )

    def complete_placeholder(self, placeholder_id: str, replacement_content: str) -> bool:
        """Mark placeholder as completed with replacement content"""

        if placeholder_id in self.placeholder_tracker:
            self.placeholder_tracker[placeholder_id].update({
                'status': 'completed',
                'replacement': replacement_content,
                'completed_at': datetime.utcnow().isoformat()
            })
            return True
        return False

    def generate_completion_report(self) -> PlaceholderCompletionReport:
        """Generate report on placeholder completion status"""

        total_placeholders = len(self.placeholder_tracker)
        completed_placeholders = sum(1 for p in self.placeholder_tracker.values()
                                   if p.get('status') == 'completed')

        return PlaceholderCompletionReport(
            total_placeholders=total_placeholders,
            completed_placeholders=completed_placeholders,
            completion_percentage=(completed_placeholders / total_placeholders * 100) if total_placeholders > 0 else 0,
            remaining_placeholders=[
                p for p in self.placeholder_tracker.values()
                if p.get('status') != 'completed'
            ]
        )
```

## Usage Guidelines

### When to Apply LLM Placeholder Instructions

- **Technical Documentation**: All AI-generated technical documentation and guides
- **Error Reporting**: Bug reports, incident reports, and troubleshooting guides
- **API Documentation**: Endpoint descriptions, response formats, and integration guides
- **Testing Documentation**: Test plans, results reporting, and coverage analysis
- **Configuration Guides**: Setup instructions, environment configuration, and deployment guides

### Placeholder Type Selection

- **SPECIFIC EXAMPLE NEEDED**: For concrete technical details like error messages, API responses, file paths, configuration values
- **FACT CHECK**: For claims about performance, compatibility, testing results, or version-specific behavior
- **QUESTION**: When user clarification is needed to avoid making assumptions about requirements or context

### Content Review Best Practices

- **Systematic Review**: Process placeholders by type for efficient completion
- **Priority Assignment**: Address high-impact placeholders first (error messages, security details)
- **Documentation**: Track placeholder completion for audit and quality assurance
- **Validation**: Verify that replacements are accurate and properly formatted
- **Version Control**: Maintain history of placeholder completion for accountability

### Integration with Workflows

- **Content Generation**: Include placeholder instructions in all LLM prompts for technical content
- **Review Process**: Establish systematic review workflows for placeholder completion
- **Quality Gates**: Require placeholder resolution before content publication
- **Training**: Train reviewers on placeholder types and completion best practices

### Anti-Patterns to Avoid

- **Allowing LLM Fabrication**: Permitting LLMs to guess technical details without placeholders
- **Vague Placeholders**: Creating placeholders without specific guidance on what's needed
- **Ignoring Placeholders**: Publishing content with unresolved placeholders
- **Inconsistent Usage**: Using different placeholder formats across different content
- **Manual Fabrication**: Manually adding fabricated details instead of researching actual information
- **Placeholder Accumulation**: Allowing placeholders to accumulate without systematic resolution

## Benefits

- **Increased Accuracy**: Prevents fabrication of technical details leading to more reliable documentation
- **Clear Communication**: Explicitly identifies areas where information is missing or uncertain
- **Professional Standards**: Maintains high quality standards in AI-generated technical content
- **Stakeholder Trust**: Prevents misleading stakeholders with fabricated technical details
- **Systematic Review**: Enables structured approach to content completion and validation
- **Audit Trail**: Provides clear tracking of what information was missing and how it was resolved

## Trade-offs

- **Additional Review Overhead**: Requires human review and completion of placeholders
- **Content Incompleteness**: Initial generated content may have many gaps requiring resolution
- **Workflow Complexity**: Adds steps to content generation and publication workflows
- **Training Requirements**: Requires training for both LLM prompt engineering and human reviewers
- **Potential Delays**: Content publication may be delayed pending placeholder resolution
- **Maintenance Burden**: Requires ongoing maintenance of placeholder instruction templates

## Related Patterns

- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Verification approach for AI-generated content
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Multi-perspective validation of generated content
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Proper error message documentation
- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md) - Evidence-based issue reporting

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 19 "LLM Placeholder Instruction Pattern" - comprehensive implementation with benefits section
- **From `PATTERN-INDEX.md`**: No direct equivalent - this is an AI/LLM-specific pattern
- **From prompt templates**: Integration with existing prompt engineering practices
- **Consolidation Strategy**: Expanded pattern-catalog.md content with comprehensive workflow integration, review processes, and validation frameworks

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for LLM integration infrastructure and prompt template management
- **Agent B (Cursor)**: Responsible for content validation patterns and review workflow documentation
- **Integration Points**: LLM prompt systems, content generation pipelines, and review management tools

## References

- Original catalog: `docs/architecture/pattern-catalog.md#19-llm-placeholder-instruction-pattern`
- Prompt templates: `docs/development/prompt-templates/`
- Content generation: `services/llm/content_generator.py`
- Review workflows: `docs/development/methodology-core/`

_Last updated: September 15, 2025_
