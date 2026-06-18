"""
Debug and Development Routes

Provides endpoints for debugging and development purposes.

Routes:
- GET /debug-markdown - Markdown renderer debug/test interface

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 350-408)
Now: Extracted to separate router module
"""

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from web.dev_gate import require_dev_environment

logger = structlog.get_logger()

# Router configuration — #1149: dev-only. Every route 404s in production (the
# canonical dev-route gate), so /debug-markdown is invisible in prod, not merely
# forbidden. The global auth middleware already 401s it; this is defense-in-depth
# (don't ship a dev test page to prod at all).
router = APIRouter(
    tags=["debug", "development"],
    dependencies=[Depends(require_dev_environment)],
)


@router.get("/debug-markdown", response_class=HTMLResponse)
async def debug_markdown():
    """Markdown renderer debug/test interface"""
    return HTMLResponse(
        content="""<!DOCTYPE html>
<html>
<head>
    <title>Markdown Debug Test</title>
    <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .test-section { border: 1px solid #ccc; margin: 10px 0; padding: 10px; }
        .raw { background: #f0f0f0; padding: 10px; margin: 5px 0; }
        .rendered { background: #e8f4f8; padding: 10px; margin: 5px 0; }
        h1 { color: #2c3e50; border-bottom: 1px solid #ecf0f1; }
        h2 { color: #34495e; }
        strong { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Markdown Renderer Debug Test</h1>

    <div class="test-section">
        <h3>Test 1: Check if renderMarkdown function exists</h3>
        <div class="rendered" id="test1"></div>
    </div>

    <div class="test-section">
        <h3>Test 2: Simple Header</h3>
        <div class="raw">Input: "# Header 1"</div>
        <div class="rendered" id="test2"></div>
    </div>

    <div class="test-section">
        <h3>Test 3: Your Failing Example</h3>
        <div class="raw">Input: "Here's my summary... # Header ## Subheader"</div>
        <div class="rendered" id="test3"></div>
    </div>

    <script src="/assets/markdown-renderer.js?v=2"></script>
    <script>
        // Test if the function is loaded
        if (typeof renderMarkdown === 'function') {
            document.getElementById('test1').innerHTML = '✅ renderMarkdown function loaded successfully';

            // Test 2: Simple header
            document.getElementById('test2').innerHTML = renderMarkdown('# Header 1');

            // Test 3: Your failing example
            const failingText = `Here's my summary: # Piper Morgan Summary ## File Type This appears to be documentation.`;
            document.getElementById('test3').innerHTML = renderMarkdown(failingText);

        } else {
            document.getElementById('test1').innerHTML = '❌ renderMarkdown function not loaded - check console for errors';
            console.error('renderMarkdown function not found');
        }
    </script>
</body>
</html>"""
    )
