# CORE-UX-BROWSER: Auto-Launch Browser on Startup

***Sprint**: A7 (proposed - can defer to A8)
**Priority**: Low
**Effort**: 1 hour
**Impact**: Low (nice-to-have convenience)

## Problem

After running `python main.py`, users must manually open their browser and navigate to `http://localhost:8001`.

**From Issue #218 testing**:
- Server starts successfully
- User sees "Server ready at http://localhost:8001"
- User must manually open browser and type URL

## Proposed Solution

Automatically open browser to Piper Morgan UI after successful startup.

### User Experience

**Current**:
```bash
$ python main.py
... (startup logs)
Server ready at http://localhost:8001
# User copies URL, opens browser, pastes URL
```

**Proposed**:
```bash
$ python main.py
... (startup logs)
Server ready at http://localhost:8001
Opening browser...
# Browser opens automatically to http://localhost:8001
```

### With flag to disable:
```bash
$ python main.py --no-browser
# Starts server but doesn't open browser
```

## Implementation

**Use Python's webbrowser module**:

```python
import webbrowser
import asyncio

async def main():
    # ... existing startup code ...

    logger.info("Starting web server on http://127.0.0.1:8001")

    # Launch browser after short delay (let server start)
    if "--no-browser" not in sys.argv:
        async def open_browser():
            await asyncio.sleep(2)  # Wait for server to be ready
            webbrowser.open("http://127.0.0.1:8001")

        asyncio.create_task(open_browser())

    # Start server
    config = uvicorn.Config(...)
    server = uvicorn.Server(config)
    await server.serve()
```

**Cross-platform support**:
- macOS: Opens default browser
- Linux: Opens default browser
- Windows: Opens default browser
- All handled by `webbrowser` module

## Acceptance Criteria

- [ ] Browser opens automatically after startup
- [ ] Opens to correct URL (http://localhost:8001)
- [ ] `--no-browser` flag disables auto-open
- [ ] Works on macOS, Linux, Windows
- [ ] Only opens browser if server starts successfully
- [ ] Doesn't open browser for `setup` or `status` commands

## User Feedback

From Issue #218 testing:
> "did this launch a browser or do I now manually still need to go do that?"

## Edge Cases

**Multiple startups**:
- If server already running on 8001, don't open browser
- Show error message about port in use

**Headless environments**:
- CI/CD: `--no-browser` should be default if no display detected
- SSH sessions: Detect and skip auto-open

**Implementation**:
```python
import os

def should_open_browser() -> bool:
    """Check if browser should be opened"""
    # Don't open if explicitly disabled
    if "--no-browser" in sys.argv:
        return False

    # Don't open if no display (CI/CD, SSH)
    if not os.environ.get("DISPLAY") and sys.platform != "darwin":
        return False

    # Don't open for non-startup commands
    if len(sys.argv) > 1 and sys.argv[1] in ["setup", "status"]:
        return False

    return True
```

## Testing Plan

1. Run `python main.py` - browser should open
2. Run `python main.py --no-browser` - browser should NOT open
3. Run `python main.py setup` - browser should NOT open
4. Run `python main.py status` - browser should NOT open
5. Test on macOS, Linux, Windows

## Related Issues

- #218 CORE-USERS-ONBOARD (setup wizard)

## Future Enhancements

- Configuration option in PIPER.user.md
- Open to specific page (e.g., /standup)
- Support for custom browser selection
