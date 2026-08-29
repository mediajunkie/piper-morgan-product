# CORE-UX-QUIET: Quiet Startup Mode for Human-Readable Output

**Sprint**: A7
**Priority**: Medium
**Effort**: 2 hours
**Impact**: High (affects daily user experience)

## Problem

Current startup output is too verbose for daily use by Alpha users. All initialization details are logged to console, making it difficult to see actionable information.

**Example** (from Issue #218 testing):
```
2025-10-22 12:51:17 [debug    ] Retrieved API key for openai from keychain
2025-10-22 12:51:17 [debug    ] Retrieved openai key from keychain (secure)
2025-10-22 12:51:17 [debug    ] Retrieved API key for anthropic from keychain
... (100+ more lines)
```

## Proposed Solution

Add quiet startup mode as default, with verbose mode available via flag.

### Quiet Mode (Default)
```
🚀 Starting Piper Morgan...
   ✓ Services initialized (3/3)
   ✓ LLM providers validated (4/4)
   ✓ Plugins loaded (4/4)
   ⚠ GitHub token not configured

🌐 Server ready at http://localhost:8001
   Press Ctrl+C to stop
```

### Verbose Mode (Flag)
```bash
python main.py --verbose
# or
python main.py -v
```

Shows all current initialization details.

## Implementation

**Files to modify**:
- `main.py` - Add `--verbose` flag detection
- `web/app.py` - Respect quiet mode for startup logs
- `services/container.py` - Conditional logging based on mode

**Logging approach**:
```python
import logging
import sys

# Check for verbose flag
verbose = "--verbose" in sys.argv or "-v" in sys.argv

if not verbose:
    # Quiet mode - only show warnings and errors
    logging.basicConfig(level=logging.WARNING)
else:
    # Verbose mode - show all details
    logging.basicConfig(level=logging.DEBUG)
```

## Acceptance Criteria

- [ ] Default startup shows <10 lines of output
- [ ] `python main.py --verbose` shows all initialization details
- [ ] Configuration warnings still visible in quiet mode
- [ ] Errors always visible regardless of mode
- [ ] Help text documents the `--verbose` flag

## User Feedback

From Issue #218 testing (PM feedback):
> "the above should be considered a verbose mode and should be triggered with a flag but we need a more human readable startup mode that is sparse and actionable."

## Future Enhancements

- Add `--quiet` flag for absolutely minimal output
- Add logging to file in quiet mode
- Configuration file option for default verbosity

## Related Issues

- #218 CORE-USERS-ONBOARD (setup wizard)
