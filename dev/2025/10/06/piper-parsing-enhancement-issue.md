# PIPER.md Parsing Enhancement

## Current State
Basic line-by-line parsing of PIPER.md configuration files. Works but doesn't leverage structure.

## Problem
- Current parsing is simple string matching
- Doesn't understand sections or hierarchy
- No validation against expected schema
- Can't extract nested configurations
- Difficult to extend for new fields

## Desired State
Structured parsing that understands PIPER.md format:
- Section recognition (e.g., [Daily Standup], [Projects])
- Key-value extraction with types
- Nested configuration support
- Schema validation
- Better error messages for malformed files

## Example Enhancement
```python
# Current (basic)
for line in piper_content.split('\n'):
    if 'priority' in line.lower():
        priority = line.split(':')[1].strip()

# Desired (structured)
config = PiperConfigParser.parse(piper_content)
priority = config.sections['daily_standup'].get('priority')
projects = config.sections['projects'].items()
```

## Acceptance Criteria
- [ ] Parse PIPER.md into structured object model
- [ ] Recognize standard sections
- [ ] Extract typed key-value pairs
- [ ] Support nested configurations
- [ ] Validate against schema
- [ ] Backward compatible with simple format
- [ ] Clear error messages for invalid format
- [ ] Unit tests for parser

## Technical Notes
- Consider using existing config parser (ConfigParser, YAML, TOML)
- Or create domain-specific parser for PIPER format
- Must handle both PIPER.md and PIPER.user.md
- Should cache parsed results (see GREAT-4C caching work)

## Priority
MEDIUM - Current parsing works, this is an enhancement

## Dependencies
- Review existing PIPER.md files for format patterns
- Define formal schema/specification
- Coordinate with GREAT-4C caching implementation

---
*Issue created as part of GREAT-4C investigation*
*Can be implemented after GREAT-4 completion*
