> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# File Scoring Algorithm Documentation

**Created:** 2025-07-22 (PM-015 Group 4 Audit)
**Status:** Active Implementation

## Overview

The File Scoring Algorithm determines the relevance of uploaded files to user intents in the Piper Morgan system. The algorithm uses multi-factor scoring with different weight configurations depending on MCP (Model Context Protocol) availability.

## Algorithm Components

### Scoring Factors

#### 1. Recency Score (25-30% weight)
Measures how recently a file was uploaded:

```python
def _calculate_recency_score(upload_time: datetime) -> float:
    age = now - upload_time
    if age <= timedelta(minutes=5): return 1.0      # Perfect score
    if age <= timedelta(hours=1): return max(0.0, 1.0 - (minutes/60))
    return 0.1  # Minimal score for very old files
```

**Weight:** 30% (MCP disabled) | 25% (MCP enabled)

#### 2. File Type Score (25-30% weight)
Measures alignment between file type and intent action:

```python
FILE_TYPE_PREFERENCES = {
    "analyze_report": ["application/pdf", "application/vnd.openxmlformats-...docx"],
    "analyze_data": ["text/csv", "application/vnd.openxmlformats-...xlsx"],
    "create_presentation": ["application/vnd.openxmlformats-...pptx"],
    # ... more mappings
}

def _calculate_type_score(file_type: str, intent_action: str) -> float:
    if file_type in preferred_types: return 1.0     # Perfect match
    if partial_match: return 0.7                    # Partial match
    return 0.2                                      # Poor match
```

**Weight:** 30% (MCP disabled) | 25% (MCP enabled)

#### 3. Name Score (15-20% weight)
Measures keyword overlap between filename and intent:

```python
def _calculate_name_score(filename: str, intent: Intent) -> float:
    keywords = []
    keywords.extend(intent.action.split("_"))

    # Extract from original message (FIXED in PM-015 Group 4)
    original_message = intent.context.get("original_message", "")
    if original_message:
        words = re.findall(r"\b[a-z0-9_-]{3,}\b", original_message.lower())
        keywords.extend(words)

    matches = sum(1 for kw in keywords if kw.lower() in filename.lower())
    return min(matches / len(keywords), 1.0) if keywords else 0.5
```

**Weight:** 20% (MCP disabled) | 15% (MCP enabled)

#### 4. Usage Score (15-20% weight)
Based on file reference history:

```python
def _calculate_usage_score(file: UploadedFile) -> float:
    base_score = min(file.reference_count / 10.0, 0.7)

    # Recent usage bonus
    if file.last_referenced and age <= timedelta(hours=1):
        base_score += 0.3
    elif file.last_referenced and age <= timedelta(hours=24):
        base_score += 0.1

    return min(base_score, 1.0)
```

**Weight:** 20% (MCP disabled) | 15% (MCP enabled)

#### 5. Content Score (20% weight, MCP only)
Uses MCP for content relevance analysis:

```python
def _calculate_content_score(file: UploadedFile, intent: Intent) -> float:
    if not mcp_enabled: return 0.5

    # Extract keywords for content matching
    keywords = extract_content_keywords(intent)

    # Simple implementation: filename-based proxy
    # TODO: Enhance with actual MCP content analysis
    matches = sum(1 for kw in keywords if kw.lower() in filename.lower())
    score = min(matches / len(keywords), 1.0) if keywords else 0.2

    # Boost for exact matches
    if exact_match_detected: score = min(score * 1.5, 1.0)

    return score
```

**Weight:** 20% (MCP enabled only)

## Scoring Modes

### MCP Disabled Mode (Default)
```
Total Score = (Recency × 0.30) + (Type × 0.30) + (Name × 0.20) + (Usage × 0.20)
```

### MCP Enabled Mode
```
Total Score = (Recency × 0.25) + (Type × 0.25) + (Name × 0.15) + (Usage × 0.15) + (Content × 0.20)
```

## Expected Score Ranges

Based on PM-015 Group 4 analysis and test alignment:

### High Relevance (0.6 - 0.9)
- Recent files (< 1 hour)
- Perfect file type match
- Strong filename/intent keyword overlap
- Previous usage history

**Example:** `"exact_match.pdf"` with intent `"analyze exact_match"` → ~0.63

### Medium Relevance (0.3 - 0.6)
- Moderately recent files (1-24 hours)
- Good file type match
- Some keyword overlap
- Limited usage history

### Low Relevance (0.1 - 0.4)
- Old files (> 24 hours)
- Poor file type match
- No keyword overlap
- No usage history

## PM-015 Group 4 Fixes Applied

### Issue 1: Name Score Keyword Extraction Bug
**Problem:** Name scoring extracted keywords from `str(intent.context)` instead of `original_message`
**Fix:** Extract keywords specifically from `intent.context.get("original_message")`
**Impact:** Name scores now correctly include user message keywords

### Issue 2: Test Expectations Misalignment
**Problem:** Tests expected scores based on MCP-disabled algorithm
**Fix:** Updated test expectations for MCP-enabled scoring reality
**Impact:** Tests now validate actual algorithm behavior

### Issue 3: Missing File Type Preferences
**Problem:** `create_presentation` action had no file type preferences
**Fix:** Added PPTX file type preferences for presentation creation
**Impact:** Presentation files now score correctly for presentation intents

## Implementation Notes

### Configuration Detection
```python
# MCP enablement check
if CONFIG_SERVICE_AVAILABLE:
    mcp_enabled = get_config().mcp_enabled
else:
    mcp_enabled = os.getenv("ENABLE_MCP_FILE_SEARCH", "false").lower() == "true"
```

### Domain Model Compliance
- Scoring logic resides in `FileResolver` service layer
- Domain models (`UploadedFile`, `Intent`) remain pure data structures
- Repository pattern used for data access
- Business logic properly separated from persistence

### Testing Strategy
- Component tests validate individual scoring factors
- Integration tests verify end-to-end scoring behavior
- Test expectations align with actual algorithm weights
- Database session management fixed for reliable testing

## Future Enhancements

### Content Scoring Improvements
Current content scoring uses filename as proxy. Future versions should:
- Integrate actual MCP content analysis
- Parse document contents for keyword matching
- Implement semantic similarity scoring
- Cache content analysis results

### Machine Learning Potential
- Learn from user file selection patterns
- Adjust weights based on successful resolutions
- Personalize scoring based on user preferences

## Changelog

**2025-07-22 (PM-015 Group 4):**
- Fixed keyword extraction bug in name scoring
- Updated test expectations for MCP-enabled algorithm
- Added `create_presentation` file type preferences
- Documented complete algorithm specification
- Aligned implementation with test validation
