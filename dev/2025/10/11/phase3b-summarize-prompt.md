# Phase 3B: SYNTHESIS Handler - _handle_summarize (Final SYNTHESIS Handler)

**Date**: October 11, 2025, 2:07 PM  
**Agent**: Code Agent  
**Duration**: Estimated 1-2 hours  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 3 (SYNTHESIS Handlers - Final Handler)

---

## Mission

Implement `_handle_summarize` handler with genuine summarization functionality, completing the SYNTHESIS category. This is the **final SYNTHESIS handler** and will establish the pattern for text summarization and condensation.

**Context**: Phase 3 established SYNTHESIS pattern with content generation. Now we apply that pattern to summarization - creating concise versions of larger content.

**PM Priority**: Thoroughness and accuracy over speed.

---

## Success Criteria

- [ ] `_handle_summarize` creates real summaries (not placeholders)
- [ ] Content is actually summarized (not just returning `success=True`)
- [ ] Tests demonstrate actual summarization
- [ ] Pattern follows Phase 3 SYNTHESIS approach
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual summarization with examples
- [ ] Quality maintained - summaries are useful and accurate

---

## Understanding Summarization vs Generation

**Phase 3 (_handle_generate_content)**:
- **Creates** new content from scratch
- **Uses** templates and data
- **Output**: New documents, reports, templates

**Phase 3B (_handle_summarize)**:
- **Condenses** existing content
- **Extracts** key points and main ideas
- **Output**: Shorter versions of input content

**Both are SYNTHESIS** because they create new text, but:
- Generation: Template → Content
- Summarization: Long Content → Short Content

---

## Phase 3B Structure

### Part 1: Study Summarization Requirements (30 min)

#### Step 1.1: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_summarize` (line 822 per original reconciliation, may have shifted after Phase 3)

**Current placeholder** (approximately):
```python
async def _handle_summarize(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SUMMARIZE intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': f'Summarization ready for {target}. Implementation in progress.'
    }
```

**Critical Questions**:
1. What can be summarized?
   - Documents (markdown, text files)?
   - GitHub content (issues, PRs, discussions)?
   - Commit messages (multiple commits)?
   - Meeting notes or conversation logs?
   - Analysis results from Phase 2C?

2. What inputs are needed?
   - Target to summarize (required)
   - Source of content (GitHub, file, text)?
   - Desired length (brief, moderate, detailed)?
   - Format (bullet points, paragraph, executive summary)?

3. How is summarization done?
   - Extractive (pull key sentences)?
   - Abstractive (rewrite in shorter form)?
   - Rule-based (heuristics)?
   - Statistical (frequency analysis)?
   - Combination?

4. What should output contain?
   - The summary itself
   - Original length vs summary length
   - Compression ratio
   - Key points extracted
   - Source information

**STOP if requirements are unclear** - Report to PM for clarification

#### Step 1.2: Review Summarization Approaches

**Check for existing capabilities**:

```bash
# Check for text processing utilities
grep -r "summarize\|extract.*key\|condense" services/ --include="*.py"

# Check for natural language processing
grep -r "nlp\|spacy\|nltk" services/ --include="*.py"

# Check for text analysis utilities
find services -name "*text*" -o -name "*nlp*" -o -name "*analysis*"
```

**Evaluate summarization strategies**:

1. **Extractive (Simple, Reliable)**:
   - Extract first sentences
   - Find sentences with key terms
   - Weight sentences by term frequency
   - Select top N sentences

2. **Rule-Based (Moderate, Structured)**:
   - Identify section headers
   - Extract bullet points
   - Find conclusion paragraphs
   - Pattern matching for key content

3. **Abstractive (Complex, Natural)**:
   - Rewrite content in shorter form
   - Requires LLM or advanced NLP
   - May not be available

**Choose approach that is**:
- Implementable with available tools
- Produces useful results
- Maintainable and testable
- Appropriate for complexity

**Recommendation**: Start with extractive + rule-based (reliable, testable)

---

### Part 2: Define Summarization Types and Strategy (45 min)

#### Step 2.1: Choose Supported Summary Types

**Start with 2-3 summary types that are**:
- Useful for Piper Morgan users
- Implementable with chosen approach
- Good examples of summarization

**Example summary types** (choose 2-3):

1. **Issue Summary**
   - Input: GitHub issue number or content
   - Output: Key points from issue description and comments
   - Method: Extractive + formatting

2. **Commit Summary**
   - Input: List of commits or commit range
   - Output: High-level summary of changes
   - Method: Aggregate commit messages

3. **Document Summary**
   - Input: Markdown or text document
   - Output: Executive summary with key points
   - Method: Extractive with section awareness

4. **Discussion Summary**
   - Input: GitHub discussion or PR comments
   - Output: Main points and decisions
   - Method: Extract key comments

5. **Analysis Summary**
   - Input: Results from Phase 2C analysis
   - Output: Brief overview of findings
   - Method: Reformat analysis data

**Choose 2-3 types** that cover different use cases

#### Step 2.2: Design Summarization Approach

**For each chosen type, define**:

```markdown
## Summary Type: [Name]

### Input Parameters
- target: [what to summarize]
- source_type: [github_issue, commit_range, document, etc.]
- length: [brief, moderate, detailed] (optional)
- format: [bullet_points, paragraph, executive_summary] (optional)

### Summarization Method
- [ ] Extractive (select key sentences)
- [ ] Rule-based (pattern matching)
- [ ] Aggregation (combine similar items)
- [ ] Reformatting (restructure existing data)

### Implementation Approach
```python
async def _summarize_[type](params):
    # 1. Fetch content to summarize
    # 2. Parse/process content
    # 3. Extract key information
    # 4. Format as summary
    # 5. Return structured result
```

### Output Structure
```python
{
    'success': True,
    'summary_type': '[type]',
    'summary': '[the actual summary text]',
    'format': 'bullet_points',  # or paragraph, etc.
    'original_length': 5000,  # characters
    'summary_length': 500,
    'compression_ratio': 0.1,  # 10% of original
    'key_points': [
        'Key point 1',
        'Key point 2',
        # ...
    ]
}
```

### Quality Checks
- [ ] Summary is not empty
- [ ] Summary is shorter than original
- [ ] Summary contains meaningful content
- [ ] Key information preserved
```

#### Step 2.3: Create Helper Methods Plan

**Plan helper methods needed**:

```python
# Text extraction
async def _get_content_to_summarize(target, source_type) -> str:
    """Fetch content based on target and source type"""
    pass

# Extractive summarization
def _extract_key_sentences(text: str, num_sentences: int = 3) -> List[str]:
    """Extract most important sentences from text"""
    pass

def _calculate_sentence_importance(sentence: str, text: str) -> float:
    """Score sentence importance based on term frequency"""
    pass

# Formatting
def _format_summary(key_points: List[str], format_type: str) -> str:
    """Format key points as bullet list, paragraph, etc."""
    pass

def _extract_key_points_from_issue(issue_content: str) -> List[str]:
    """Extract key points from GitHub issue"""
    pass

def _summarize_commits(commits: List) -> str:
    """Create summary from list of commits"""
    pass
```

---

### Part 3: Write Comprehensive Tests (TDD) (45 min)

**File**: `tests/intent/test_synthesis_handlers.py` (add to existing file)

#### Step 3.1: Test Structure

```python
class TestHandleSummarize:
    """Comprehensive tests for _handle_summarize handler
    
    SYNTHESIS handler that condenses content into shorter summaries
    while preserving key information and meaning.
    """
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with required services"""
        service = IntentService()
        return service
```

#### Step 3.2: Write Thorough Unit Tests

**Test 1: Handler exists and is not placeholder**
```python
@pytest.mark.asyncio
async def test_summarize_handler_exists(self, intent_service):
    """Verify handler exists and is not a placeholder"""
    result = await intent_service._handle_summarize(
        query="summarize the latest commits",
        params={'target': 'test', 'source_type': 'commits'}
    )
    
    # Should not have placeholder response
    assert 'requires_clarification' not in result or result.get('requires_clarification') is False
```

**Test 2: Missing target parameter**
```python
@pytest.mark.asyncio
async def test_summarize_missing_target(self, intent_service):
    """Test error when target parameter missing"""
    result = await intent_service._handle_summarize(
        query="summarize something",
        params={}  # Missing target
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'target' in result['error'].lower()
```

**Test 3: Unsupported source type**
```python
@pytest.mark.asyncio
async def test_summarize_unsupported_source_type(self, intent_service):
    """Test handling of unsupported source type"""
    result = await intent_service._handle_summarize(
        query="summarize quantum mechanics paper",
        params={
            'target': 'quantum-paper.pdf',
            'source_type': 'quantum_physics'
        }
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'unsupported' in result['error'].lower() or 'not supported' in result['error'].lower()
```

**Test 4: Issue summary success**
```python
@pytest.mark.asyncio
async def test_summarize_issue_success(self, intent_service):
    """Test successful issue summarization"""
    result = await intent_service._handle_summarize(
        query="summarize issue 212",
        params={
            'target': '212',
            'source_type': 'github_issue',
            'repository': 'piper-morgan'
        }
    )
    
    assert result['success'] is True
    assert 'summary' in result
    assert len(result['summary']) > 0
    
    # Verify it's actually shorter than typical issue
    assert len(result['summary']) < 5000
    
    # Verify metadata
    if 'summary_length' in result:
        assert result['summary_length'] > 0
```

**Test 5: Commit range summary**
```python
@pytest.mark.asyncio
async def test_summarize_commits_success(self, intent_service):
    """Test summarization of commit range"""
    result = await intent_service._handle_summarize(
        query="summarize commits from last week",
        params={
            'target': 'last_week',
            'source_type': 'commit_range',
            'repository': 'piper-morgan'
        }
    )
    
    assert result['success'] is True
    assert 'summary' in result
    assert len(result['summary']) > 0
    
    # Should mention commits or changes
    summary_lower = result['summary'].lower()
    assert 'commit' in summary_lower or 'change' in summary_lower or 'update' in summary_lower
```

**Test 6: Document summary with text**
```python
@pytest.mark.asyncio
async def test_summarize_document_with_text(self, intent_service):
    """Test document summarization with provided text"""
    long_text = """
    This is a long document with multiple paragraphs. It contains important information
    that needs to be summarized. The first key point is about system architecture.
    
    The second section discusses implementation details. It explains how the system
    processes requests and handles errors. This is crucial for understanding operations.
    
    The final section covers deployment and monitoring. It provides guidelines for
    maintaining the system in production environments. Regular monitoring is essential.
    """
    
    result = await intent_service._handle_summarize(
        query="summarize this document",
        params={
            'target': 'inline_text',
            'source_type': 'text',
            'text': long_text
        }
    )
    
    assert result['success'] is True
    assert 'summary' in result
    
    # Summary should be shorter
    assert len(result['summary']) < len(long_text)
    
    # Should preserve key concepts
    summary_lower = result['summary'].lower()
    # At least some key terms should appear
    key_terms = ['architecture', 'implementation', 'deployment', 'monitoring']
    matches = sum(1 for term in key_terms if term in summary_lower)
    assert matches >= 2  # At least 2 key terms preserved
```

**Test 7: Different summary formats**
```python
@pytest.mark.asyncio
async def test_summarize_different_formats(self, intent_service):
    """Test different summary output formats"""
    text = "Sample text for summarization. Multiple sentences here. More content follows."
    
    # Test bullet point format
    result_bullets = await intent_service._handle_summarize(
        query="summarize as bullet points",
        params={
            'target': 'test',
            'source_type': 'text',
            'text': text,
            'format': 'bullet_points'
        }
    )
    
    if result_bullets['success']:
        assert 'summary' in result_bullets
        # Bullet format might have dashes or asterisks
        assert '-' in result_bullets['summary'] or '*' in result_bullets['summary'] or '•' in result_bullets['summary']
```

**Test 8: Empty content handling**
```python
@pytest.mark.asyncio
async def test_summarize_empty_content(self, intent_service):
    """Test handling of empty content to summarize"""
    result = await intent_service._handle_summarize(
        query="summarize empty document",
        params={
            'target': 'empty',
            'source_type': 'text',
            'text': ''
        }
    )
    
    # Should handle gracefully
    assert 'success' in result
    if result['success']:
        assert 'summary' in result
        # Might be empty or have a message
    else:
        assert 'error' in result
```

#### Step 3.3: Write Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_summarize_real_github_issue(self, intent_service):
    """Test with real GitHub issue summarization"""
    
    # Use a known issue from piper-morgan
    result = await intent_service._handle_summarize(
        query="summarize issue 212",
        params={
            'target': '212',
            'source_type': 'github_issue',
            'repository': 'piper-morgan'
        }
    )
    
    # Verify success
    assert result['success'] is True
    assert 'summary' in result
    
    summary = result['summary']
    assert len(summary) > 0
    
    # Verify summary quality
    # Should be substantially shorter than full issue
    assert len(summary) < 2000  # Reasonable summary length
    
    # Should contain meaningful content (not just "...")
    assert len(summary.strip()) > 50
    
    # Log for manual review
    import json
    logger.info(f"Issue #212 summary:\n{summary}")
    logger.info(f"Summary metadata: {json.dumps(result, indent=2, default=str)}")
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_synthesis_handlers.py::TestHandleSummarize -v
# Should fail - handler is still placeholder
```

---

### Part 4: Implement Handler Thoroughly (60-90 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_summarize` (find current line with Serena or grep)

#### Step 4.1: Implementation Structure

```python
async def _handle_summarize(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SUMMARIZE intent - FULLY IMPLEMENTED
    
    Creates concise summaries of content from various sources. This is a SYNTHESIS
    operation that creates new condensed versions of existing content.
    
    Supported source_types:
        - 'github_issue': Summarize GitHub issue and comments
        - 'commit_range': Summarize commits from a time period
        - 'text': Summarize provided text content
        - [Add other supported types]
    
    Args:
        query: Natural language query describing summarization request
        params: Dictionary containing:
            - target (required): What to summarize (issue #, time range, etc.)
            - source_type (required): Type of source to summarize
            - repository (optional): Repository name for GitHub sources
            - text (optional): Text content to summarize (for source_type='text')
            - length (optional): Desired summary length (brief/moderate/detailed)
            - format (optional): Output format (bullet_points/paragraph/executive_summary)
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if summarization succeeded
            - summary_type: Type of content summarized
            - summary: The actual summary text
            - format: Format of summary
            - original_length: Length of original content (if available)
            - summary_length: Length of summary
            - compression_ratio: Ratio of summary to original
            - key_points: List of extracted key points (if applicable)
            - error: Error message (if success is False)
    """
    try:
        # 1. VALIDATION
        target = params.get('target')
        if not target:
            logger.warning("Target missing for summarization")
            return {
                'success': False,
                'error': 'target parameter is required. Specify what to summarize.'
            }
        
        source_type = params.get('source_type')
        if not source_type:
            logger.warning("Source type missing for summarization")
            return {
                'success': False,
                'error': 'source_type parameter is required. Supported types: github_issue, commit_range, text'
            }
        
        # Normalize source_type
        source_type = source_type.lower().strip()
        
        # Validate source_type is supported
        supported_types = ['github_issue', 'commit_range', 'text']
        if source_type not in supported_types:
            logger.warning(f"Unsupported source type: {source_type}")
            return {
                'success': False,
                'error': f'Source type "{source_type}" is not supported. Supported types: {", ".join(supported_types)}'
            }
        
        # Get optional parameters
        repository = params.get('repository', 'piper-morgan')
        length = params.get('length', 'moderate')
        format_type = params.get('format', 'paragraph')
        
        # 2. FETCH CONTENT TO SUMMARIZE
        if source_type == 'text':
            content = params.get('text', '')
            if not content:
                return {
                    'success': False,
                    'error': 'text parameter required when source_type is "text"'
                }
        else:
            content = await self._get_content_to_summarize(target, source_type, repository)
        
        if not content or len(content.strip()) == 0:
            logger.warning(f"No content found to summarize for target: {target}")
            return {
                'success': True,
                'summary': 'No content available to summarize.',
                'summary_type': source_type,
                'original_length': 0,
                'summary_length': 0
            }
        
        original_length = len(content)
        
        # 3. SUMMARIZE based on source type
        if source_type == 'github_issue':
            summary, key_points = await self._summarize_issue(content, length)
        elif source_type == 'commit_range':
            summary, key_points = await self._summarize_commits(content, length)
        elif source_type == 'text':
            summary, key_points = self._summarize_text(content, length)
        else:
            raise ValueError(f"Unhandled source type: {source_type}")
        
        # 4. FORMAT SUMMARY
        formatted_summary = self._format_summary(summary, key_points, format_type)
        
        summary_length = len(formatted_summary)
        compression_ratio = summary_length / original_length if original_length > 0 else 0
        
        # 5. RETURN SUCCESS
        logger.info(f"Successfully summarized {source_type} ({original_length} → {summary_length} chars, {compression_ratio:.1%})")
        return {
            'success': True,
            'summary_type': source_type,
            'summary': formatted_summary,
            'format': format_type,
            'original_length': original_length,
            'summary_length': summary_length,
            'compression_ratio': compression_ratio,
            'key_points': key_points if key_points else None
        }
        
    except Exception as e:
        # 6. HANDLE ERRORS
        logger.error(f"Failed to summarize: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to summarize: {str(e)}'
        }
```

#### Step 4.2: Implement Helper Methods

**Helper 1: Get content to summarize**
```python
async def _get_content_to_summarize(
    self,
    target: str,
    source_type: str,
    repository: str
) -> str:
    """Fetch content to summarize from various sources"""
    
    if source_type == 'github_issue':
        # Get issue content
        github_service = self.service_registry.get('github')
        if not github_service:
            raise ValueError("GitHub service not available")
        
        try:
            issue_number = int(target)
            issue = await github_service.get_issue(issue_number, repository)
            
            # Combine issue body and comments
            content = f"# Issue #{issue_number}: {issue.title}\n\n{issue.body or ''}\n\n"
            
            # Add comments if available
            if hasattr(issue, 'comments') and issue.comments:
                content += "## Comments:\n\n"
                for comment in issue.comments[:10]:  # Limit to first 10 comments
                    content += f"- {comment.body}\n"
            
            return content
            
        except (ValueError, AttributeError) as e:
            logger.error(f"Failed to fetch issue {target}: {e}")
            return ""
    
    elif source_type == 'commit_range':
        # Get commits
        # Reuse get_recent_activity from Phase 2
        analysis_result = await self._handle_analyze_commits(
            query=f"analyze commits in {repository}",
            params={
                'repository': repository,
                'timeframe': target
            }
        )
        
        if analysis_result.get('success'):
            commits = analysis_result.get('commits', [])
            content = '\n'.join([f"- {c.get('message', '')}" for c in commits])
            return content
        
        return ""
    
    return ""
```

**Helper 2: Summarize issue**
```python
async def _summarize_issue(
    self,
    content: str,
    length: str = 'moderate'
) -> Tuple[str, List[str]]:
    """Summarize GitHub issue content"""
    
    # Extract title and body
    lines = content.split('\n')
    title_line = [l for l in lines if l.startswith('# Issue #')]
    title = title_line[0].replace('# Issue #', 'Issue #') if title_line else 'Issue'
    
    # Extract key points using simple heuristics
    key_points = []
    
    # Look for bullet points or numbered lists
    for line in lines:
        line = line.strip()
        if line.startswith(('-', '*', '•')) or (len(line) > 0 and line[0].isdigit() and '.' in line[:3]):
            point = line.lstrip('-*•0123456789. ').strip()
            if len(point) > 10:  # Meaningful point
                key_points.append(point)
    
    # If no explicit points, extract first few non-empty lines
    if not key_points:
        key_points = [l.strip() for l in lines if len(l.strip()) > 20][:3]
    
    # Limit points based on length
    max_points = {'brief': 2, 'moderate': 4, 'detailed': 6}.get(length, 4)
    key_points = key_points[:max_points]
    
    # Create summary
    summary = f"{title}\n\nKey Points:\n"
    summary += '\n'.join(f"- {point}" for point in key_points)
    
    return summary, key_points
```

**Helper 3: Summarize commits**
```python
async def _summarize_commits(
    self,
    content: str,
    length: str = 'moderate'
) -> Tuple[str, List[str]]:
    """Summarize commit messages"""
    
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # Group by common prefixes (conventional commits)
    categories = {}
    for line in lines:
        line = line.lstrip('-*• ')
        
        # Check for conventional commit format
        if ':' in line[:20]:
            prefix = line.split(':', 1)[0].lower()
            categories.setdefault(prefix, []).append(line)
        else:
            categories.setdefault('other', []).append(line)
    
    # Create summary
    summary = f"Changes Summary ({len(lines)} commits):\n\n"
    
    for category, commits in categories.items():
        summary += f"\n**{category.capitalize()}** ({len(commits)} commits):\n"
        # Show first few commits
        max_show = 3 if length == 'brief' else 5 if length == 'moderate' else 10
        for commit in commits[:max_show]:
            summary += f"- {commit}\n"
    
    key_points = [f"{cat}: {len(commits)} changes" for cat, commits in categories.items()]
    
    return summary, key_points
```

**Helper 4: Summarize text**
```python
def _summarize_text(
    self,
    content: str,
    length: str = 'moderate'
) -> Tuple[str, List[str]]:
    """Summarize plain text using extractive method"""
    
    # Split into sentences
    sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
    
    if not sentences:
        return "No content to summarize.", []
    
    # Simple importance scoring: prefer first and last sentences, and those with key terms
    def score_sentence(sentence, position, total):
        score = 0.0
        
        # Position bonus (first and last are important)
        if position == 0:
            score += 2.0
        if position == total - 1:
            score += 1.5
        
        # Length bonus (moderate length preferred)
        words = sentence.split()
        if 10 <= len(words) <= 30:
            score += 1.0
        
        # Keyword bonus
        keywords = ['important', 'key', 'essential', 'critical', 'main', 'primary', 'significant']
        for keyword in keywords:
            if keyword in sentence.lower():
                score += 0.5
        
        return score
    
    # Score all sentences
    scored_sentences = [
        (score_sentence(s, i, len(sentences)), s)
        for i, s in enumerate(sentences)
    ]
    
    # Sort by score and select top sentences
    scored_sentences.sort(reverse=True)
    
    max_sentences = {'brief': 2, 'moderate': 4, 'detailed': 6}.get(length, 4)
    top_sentences = [s for _, s in scored_sentences[:max_sentences]]
    
    # Reorder chronologically
    summary_sentences = [s for s in sentences if s in top_sentences]
    
    summary = '. '.join(summary_sentences)
    if not summary.endswith('.'):
        summary += '.'
    
    key_points = summary_sentences[:3]  # First 3 as key points
    
    return summary, key_points
```

**Helper 5: Format summary**
```python
def _format_summary(
    self,
    summary: str,
    key_points: List[str],
    format_type: str
) -> str:
    """Format summary based on requested format"""
    
    if format_type == 'bullet_points':
        # Convert to bullet format
        if key_points:
            return '\n'.join(f"• {point}" for point in key_points)
        else:
            # Split summary into sentences
            sentences = [s.strip() + '.' for s in summary.split('.') if s.strip()]
            return '\n'.join(f"• {s}" for s in sentences)
    
    elif format_type == 'executive_summary':
        # Add executive summary header
        return f"**Executive Summary**\n\n{summary}\n\n**Key Takeaways:**\n" + \
               '\n'.join(f"- {point}" for point in key_points[:3]) if key_points else summary
    
    else:  # paragraph or default
        return summary
```

**Implementation Quality Checklist**:
- [ ] All validation thorough
- [ ] Multiple source types supported
- [ ] Extractive summarization works
- [ ] Summaries are actually shorter
- [ ] Key information preserved
- [ ] Error handling comprehensive
- [ ] Logging appropriate
- [ ] Helper methods focused
- [ ] No placeholder markers

---

### Part 5: Run Tests Thoroughly (30 min)

```bash
# Run all new tests
pytest tests/intent/test_synthesis_handlers.py::TestHandleSummarize -v -s

# Should see all tests passing
# Review summaries in logs
# Verify quality
```

---

### Part 6: Evidence Collection (30 min)

**Create comprehensive documentation**:

1. **Test Results**: `dev/2025/10/11/phase3b-test-results.txt`
2. **Sample Summaries**: `dev/2025/10/11/phase3b-sample-summaries.md`
3. **Pattern Comparison**: `dev/2025/10/11/phase3b-synthesis-completion.md`
4. **SYNTHESIS Category Completion**: `dev/2025/10/11/synthesis-category-complete.md`

**SYNTHESIS Category Completion Report**:
```markdown
# SYNTHESIS Category Completion Report

## Status: 2/2 Handlers Complete (100%) ✅

### Implemented Handlers
1. ✅ _handle_generate_content (Phase 3)
2. ✅ _handle_summarize (Phase 3B)

### Quality Metrics
- Test coverage: [X%]
- Pattern consistency: [100%]
- Documentation: [Complete]
- Evidence: [Complete]

### Category Characteristics
SYNTHESIS handlers CREATE new content:
- Generation: Create from templates/data
- Summarization: Create condensed versions

Both follow same validation → process → format → return pattern

### Lessons Learned
[Key insights from implementing SYNTHESIS handlers]

### Ready for Next Category: STRATEGY
[Verification that pattern can be applied to STRATEGY]
```

---

## Phase 3B Completion Criteria

- [ ] Tests comprehensive (TDD red phase)
- [ ] Multiple source types supported
- [ ] Implementation complete with helpers
- [ ] All tests passing (TDD green phase)
- [ ] Summaries actually shorter than originals
- [ ] Key information preserved
- [ ] No placeholder responses
- [ ] Quality maintained
- [ ] Evidence collected
- [ ] SYNTHESIS category complete

---

## STOP Conditions

- Summarization approach unclear
- No good method available
- Pattern doesn't apply
- Quality concerns
- **Any uncertainty about accuracy**

---

*Phase 3B prompt created: October 11, 2025, 2:07 PM*  
*Agent: Code Agent*  
*Final SYNTHESIS handler - completes category*  
*Priority: Thoroughness and accuracy*
