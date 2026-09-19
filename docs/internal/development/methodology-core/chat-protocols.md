---
type: methodology
title: Chat Protocols and Session Management
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Chat Protocols and Session Management

## Session Management

This document defines the protocols for managing chat sessions and ensuring continuity across development sessions.

## Session End Protocol

Before ending any session:

1. Review any maintenance tasks assigned to human
2. Create reminder list if tasks remain undone
3. Include in next session startup checklist
4. Flag any time-sensitive maintenance items

### Maintenance Task Examples

- Configuration file updates (CLAUDE.md, etc.)
- Environment setup tasks
- Documentation updates assigned to human
- Infrastructure fixes requiring human action

## Session Continuity

### Startup Checklist

- Review previous session logs
- Check for pending maintenance tasks
- Verify infrastructure status
- Confirm test environment readiness

### Handoff Protocol

- Document current state clearly
- Flag any blocking issues
- Provide context for next session
- Include specific next steps

## Claude Code Integration

### Claude Code /agent Usage

For complex tasks requiring specialized execution:

1. **Task Assessment**: Determine if task requires multi-agent coordination
2. **Agent Selection**: Choose appropriate specialized agent based on task type:
   - Architecture/Planning agents for system design
   - Implementation agents for code execution
   - Testing agents for validation workflows
   - Documentation agents for content creation

3. **Handoff Preparation**: Before using `/agent`, prepare:
   - Clear context summary
   - Specific objectives and success criteria
   - Relevant file paths and current state
   - Dependencies and constraints

4. **Agent Instructions**: When invoking `/agent`:
   - Be specific about expected outcomes
   - Reference relevant methodology documents
   - Include verification requirements
   - Specify handoff conditions

5. **Results Integration**: After agent completion:
   - Validate outputs against success criteria
   - Document any new patterns discovered
   - Update project context for future sessions
   - Close loop on original objectives
