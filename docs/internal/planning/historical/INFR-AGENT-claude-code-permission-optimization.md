# INFR-AGENT: Claude Code Permission Optimization

**Labels**: enhancement, infr-agent, developer-experience, productivity

## Problem Statement

Claude Code's permission system causes significant productivity friction:

- Repeated approval prompts for routine commands
- "Permission amnesia" - forgetting previously granted approvals
- Command parsing bugs with pipes and complex operations
- Flow-state interruptions during intensive coding sessions

Community research reveals this is a known systemic issue with proven workarounds.

## Root Causes (Per Research)

1. **Over-aggressive security model** - Treats `git commit` and `find` as threats
2. **Permission persistence bugs** - System forgets "don't ask again" selections
3. **Command parsing issues** - Pipes and operators trigger unexpected prompts

## Solution Approach

### Immediate Win: Shift+Tab Auto-Accept Mode

- Toggle during focused work sessions (10-40 minute sprints)
- Cycles: normal → auto-accept → plan mode
- No configuration needed, instant productivity boost

### Configuration Optimization

Implement community-validated permission config in `~/.claude.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash(ls:*)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "Bash(echo:*)",
      "Bash(cat:*)",
      "Bash(python:*)",
      "Bash(pytest:*)",
      "Write(*)",
      "Read(*)",
      "Edit(*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Read(./.env*)",
      "Read(./secrets/**)",
      "Read(./config/token*)"
    ]
  }
}
```

### Workaround Documentation

Update Code Agent prompts with:

- Single quotes for git commits: `git commit -m 'message'`
- Break piped commands when hitting permission issues
- Document permission blocks for methodology updates

### Advanced Option: Container Isolation

For unrestricted development work:

- Docker container with `--dangerously-skip-permissions`
- Isolated filesystem and network restrictions
- Safe for aggressive refactoring/generation tasks

## Implementation Steps

- [ ] Test Shift+Tab auto-accept mode immediately
- [ ] Create `~/.claude.json` with recommended config
- [ ] Update `agent-prompt-template.md` with permission workarounds
- [ ] Document permission patterns in methodology
- [ ] Test complex command patterns (pipes, args)
- [ ] Evaluate container isolation for specific tasks
- [ ] Add permission troubleshooting to debugging guide

## Success Criteria

- [ ] 80% reduction in permission prompts
- [ ] Zero interruptions during flow-state work
- [ ] Git operations work without repeated approvals
- [ ] Complex piped commands execute smoothly
- [ ] Clear documentation for edge cases

## Risk Mitigation

**Security Considerations**:

- Allow list focuses on reversible operations
- Explicit deny for destructive commands (`rm`, `curl`)
- Secrets/env files protected
- Container isolation for high-risk work

## Estimated Effort

**2 hours initial setup**, ongoing refinement as patterns emerge

## Priority

**HIGH** - Direct impact on developer productivity and agent effectiveness

## References

- Community research document (comprehensive analysis)
- GitHub issues: #2560, #819, #1614, #2023, #1498
- Shift+Tab feature (GA since May 2025)

## Notes

The Shift+Tab auto-accept mode might be the single biggest productivity improvement available. It allows maintaining flow state during intensive coding sessions while still having the option to review changes afterward.

For PM: Consider creating a "Code Agent Best Practices" document incorporating these permission optimizations and workarounds.
