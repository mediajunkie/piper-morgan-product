# MCP Capability Gap: Local vs Web Claude Code Environments

**Date**: 2026-03-12
**Author**: Lead Developer (Claude Code web session)
**Status**: Research complete, needs issue filing via local `gh` CLI

---

## Summary

During evaluation of [context-hub](https://github.com/andrewyng/context-hub) (Andrew Ng) vs [context7](https://github.com/upstash/context7) for agent documentation access, we discovered that **MCP servers configured for local Claude Code are not available in web-based sessions** — and this degrades silently.

## Current MCP Availability Matrix

| MCP Server | Local (laptop) | Web (cloud) | Claude Projects |
|------------|:-:|:-:|:-:|
| Serena (symbolic code nav) | ✅ | ❌ ghost permissions | N/A |
| Context7 (API docs) | ✅ | ❌ not configured | N/A |
| Chrome DevTools | ✅ | ✅ | N/A |
| `gh` CLI | ✅ | ❌ not installed | N/A |
| Local filesystem | ✅ full | ✅ sandboxed | ❌ |
| MCP support at all | ✅ | ✅ partial | ❌ |

## Evidence

`settings.json` carries local laptop paths (`/Users/xian/Development/`, `/Users/xian/Downloads/`) and pre-approved Serena permissions (`mcp__serena__search_for_pattern`, etc.), but no Serena server process is running. The config is a ghost — permissions without capability.

## Impact on Agent Quality

1. **Code navigation** — Grep/Glob instead of Serena's "find all callers" / "show class hierarchy"
2. **API docs** — Training data instead of verified current docs via context7
3. **Issue management** — Can't file/close GitHub issues without `gh`
4. **Silent degradation** — Agents don't error, they just produce lower-quality work

## Context7 Alternatives Evaluation

| Tool | Differentiator | Readiness |
|------|---------------|-----------|
| [context-hub](https://github.com/andrewyng/context-hub) | Self-improving annotations, local-first, MIT, no rate limits | Early — thin content catalog, no MCP server |
| [Context7](https://github.com/upstash/context7) | 9000+ libraries, native MCP server | Mature but free tier cut to 1K req/mo ($10/mo paid) |
| Deepcon | 90% accuracy vs context7's 65% in benchmarks | Worth evaluating |
| REF MCP | 85% fewer tokens than context7 | Worth evaluating |
| Docfork | Open-source, 9000+ libraries | Worth evaluating |

**Recommendation**: Don't switch from context7 yet. Revisit context-hub when content catalog matures and/or MCP server support is added. Immediate priority is making capability gaps visible.

## Broader Implications: klatch.ing Crossover

This is a specific instance of the **session capability portability** problem that klatch.ing faces:

### The Core Problem

A Claude conversation/agent session has an **implicit capability envelope** that isn't recorded in the chat transcript. When that conversation is:
- Continued in a different environment (local → web)
- Forked and resumed
- Imported into klatch.ing's unified UX
- Replayed or analyzed after the fact

...the capability envelope may not match, and there's no metadata to surface this.

### Key Questions for klatch.ing

1. **Capability metadata** — How to represent "this conversation had access to Serena, context7, local filesystem at /Users/xian/..." in the chat record
2. **Gap detection** — How to detect when replaying/continuing a conversation in an environment that lacks capabilities the original had
3. **Substitution vs surfacing** — Should the system attempt capability substitution (Grep as fallback for Serena) or surface the gap to the user?
4. **Environment taxonomy** — What's the right way to categorize Claude environments? At minimum:
   - Claude Code local (full MCP, full filesystem)
   - Claude Code web (partial MCP, sandboxed filesystem)
   - Claude Projects (no MCP, no filesystem, artifacts only)
   - API direct (no tools at all unless provided)
5. **Fork divergence** — When a conversation forks, the fork inherits context (what was discussed) but not necessarily capability (what tools were available). This is analogous to process forking where file descriptors may or may not be inherited.

### Suggested Capability Manifest Format

```yaml
# Could be embedded in chat export metadata
environment:
  type: claude-code-web  # or claude-code-local, claude-projects, api
  mcps_available:
    - chrome-devtools
  mcps_configured_but_unavailable:
    - serena  # permissions exist, server not running
  tools:
    - bash (sandboxed)
    - read, write, edit, glob, grep
    - web_search, web_fetch
  filesystem:
    type: sandboxed
    root: /home/user/piper-morgan-product
  missing_from_parent:  # if this is a fork
    - gh CLI
    - serena MCP
    - context7 MCP
```

## Action Items

- [ ] File as GitHub issue (needs `gh` CLI — do from local session)
- [ ] Add environment capability check to `.claude/hooks/session-start.sh`
- [ ] Document expected MCPs in CLAUDE.md so agents can self-diagnose
- [ ] Share klatch.ing capability-manifest concept with xian for feedback
- [ ] Evaluate Deepcon and REF MCP more deeply when time permits
