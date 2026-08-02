> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# Markdown Formatting Analysis & Recommendations

**Date**: July 9, 2025
**Author**: Claude Code Development Session
**Status**: BLOCKED - Requires Architectural Decision
**Priority**: HIGH - Core feature unusable

## Executive Summary

The Piper Morgan document summarization feature is producing unreadable output due to persistent markdown formatting issues. Despite multiple implementation approaches following best practices, the system continues to generate malformed markdown that renders as an "unreadable jumble" in the web UI.

**Impact**: Core document summarization feature is unusable, affecting PM-011 UI testing and user experience.

## Problem Statement

### Primary Issue
LLM-generated markdown consistently produces non-standard formatting that breaks CommonMark rendering, specifically:
- Mixed bullet syntax: `• -` instead of standard `-`
- Malformed headers: `• ##` patterns
- Inconsistent spacing and nesting

### Secondary Issues
- All bot messages render in italics (CSS/styling layer)
- Workflow timeouts during document processing
- Intent classification brittleness causing clarification loops

## Technical Investigation Summary

### Approaches Attempted

#### 1. Domain-Driven Design Approach ✅ Implemented
- **File**: `services/utils/markdown_formatter.py`
- **Approach**: Domain service with business rules for markdown standardization
- **Result**: Partial improvement but core issues persist

#### 2. Prompt Engineering ✅ Implemented
- **File**: `services/prompts/summarization.py`
- **Approach**: Explicit CommonMark formatting rules, explicit Unicode bullet prohibition
- **Result**: LLM continues generating non-standard format despite clear instructions

#### 3. Pipeline Simplification ✅ Implemented
- **Approach**: Removed multiple formatting layers, trusted marked.js library
- **Result**: Reduced complexity but core formatting issues remain

#### 4. Battle-Tested Library Integration ✅ Implemented
- **Library**: marked.js (frontend), replaced custom regex parser
- **Result**: Proper markdown rendering when given valid input, but input remains malformed

### Current Architecture Flow

```
LLM Generation → Domain Service Cleaning → marked.js Rendering → Web UI
```

**Bottleneck**: LLM consistently generates malformed markdown despite explicit prompts

## Root Cause Analysis

### What We Know
1. **LLM Behavior**: Consistently generates `• -` format across different prompt variations
2. **Domain Service**: Successfully detects and attempts to clean some issues
3. **Rendering Layer**: Works correctly with standard markdown input
4. **CSS Layer**: Separate issue causing all-italics rendering

### What We Don't Know (Research Needed)
1. **Industry Standards**: How do other systems handle LLM markdown generation?
2. **Alternative Approaches**: Should we generate HTML directly instead of markdown?
3. **LLM Training**: Are there prompt engineering techniques we're missing?
4. **Processing Pipeline**: Are there established patterns for LLM output standardization?

## Recommendations for Research

### Immediate Research Areas

#### 1. Industry Best Practices Survey
- **Research**: How do systems like Notion, GitHub Copilot, ChatGPT handle markdown formatting?
- **Focus**: LLM output standardization patterns
- **Timeline**: 2-3 days

#### 2. Alternative Architecture Evaluation
- **Option A**: Backend HTML generation (skip markdown entirely)
- **Option B**: AST-based markdown processing (parse → clean → render)
- **Option C**: LLM fine-tuning for consistent output format
- **Timeline**: 3-5 days

#### 3. Prompt Engineering Research
- **Research**: Advanced prompt techniques for format consistency
- **Focus**: Few-shot examples, output constraints, format validation
- **Timeline**: 1-2 days

### Technical Alternatives to Consider

#### Nuclear Option 1: Backend HTML Generation
```python
# Skip markdown entirely
summary_html = llm_client.complete_with_format(
    prompt=prompt,
    output_format="html",
    constraints={"allowed_tags": ["h1", "h2", "ul", "li", "strong"]}
)
```

#### Nuclear Option 2: AST-Based Processing
```python
# Parse markdown to AST, clean, then render
import markdown_it
md = markdown_it.MarkdownIt()
ast = md.parse(llm_output)
cleaned_ast = clean_ast(ast)  # Fix malformed nodes
html = md.render(cleaned_ast)
```

#### Nuclear Option 3: Template-Based Output
```python
# Use structured templates instead of free-form markdown
summary_template = SummaryTemplate(
    title=title,
    sections=[Section(header=h, bullets=bullets) for h, bullets in content]
)
html = summary_template.render()
```

## Immediate Actions Required

### 1. Architectural Decision (Chief Architect)
- **Decision**: Continue with markdown approach or pivot to HTML generation?
- **Considerations**: Development time, maintainability, user experience
- **Timeline**: 1-2 days

### 2. Research Assignment
- **Assign**: Developer to research industry best practices
- **Deliverable**: Comparative analysis of markdown processing approaches
- **Timeline**: 3-5 days

### 3. CSS Issue Fix (Quick Win)
- **Issue**: All bot messages rendering in italics
- **Fix**: CSS/styling review and correction
- **Timeline**: 1-2 hours

## Risk Assessment

### High Risk
- **User Experience**: Core feature unusable, affects adoption
- **Technical Debt**: Multiple workarounds accumulating
- **Development Velocity**: Blocked on markdown processing

### Medium Risk
- **Architectural Inconsistency**: Ad-hoc solutions not following patterns
- **Testing Complexity**: Difficult to test formatting edge cases

## Success Criteria for Resolution

### Must Have
- [ ] Document summaries render as readable, well-formatted content
- [ ] Consistent formatting across all document types
- [ ] No more "unreadable jumble" output

### Should Have
- [ ] Maintainable, testable formatting solution
- [ ] Follows project's DDD architectural patterns
- [ ] Scalable to future formatting requirements

### Could Have
- [ ] Real-time formatting validation
- [ ] User-customizable formatting preferences
- [ ] Advanced markdown features (tables, code blocks)

## Conclusion

The markdown formatting issue requires architectural guidance and research beyond the current debugging approach. The technical implementation is sound, but the fundamental approach may need reconsideration.

**Recommendation**: Pause current implementation, conduct research on industry best practices, and make an architectural decision on the processing approach before proceeding.

**Next Steps**: Chief architect review and research assignment to identify the most appropriate long-term solution.

---

**Attachments**:
- Session log: `development/session-logs/2025-07-09-log.md`
- Implementation files: `services/utils/markdown_formatter.py`, `services/prompts/summarization.py`
- Test examples: Available in workflow logs
---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
