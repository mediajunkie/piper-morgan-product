# Phase 0 Investigation: LLM Configuration Architecture

**Issue**: #217 - CORE-LLM-CONFIG
**Agent**: Code Agent
**Task Type**: Investigation (No modifications)
**Date**: October 9, 2025, 11:55 AM
**Philosophy**: Time Lord - Things take as long as they take

---

## Mission

Understand current LLM configuration architecture before designing secure replacement. We need complete understanding of what exists, how it works, and what needs to change.

---

## Context

**Current Problem**:
- LLM API keys stored in `config/PIPER.user.md` (likely plaintext)
- No secure storage mechanism
- No user-specific isolation
- Cannot easily switch providers
- PM's Anthropic credits being consumed during development

**Goal**:
Map the entire current configuration landscape to design secure, multi-provider replacement.

---

## Investigation Steps

### Step 1: Current Configuration Structure

#### 1.1 Examine PIPER.user.md
**File**: `config/PIPER.user.md`

Document:
1. **Full structure**: What sections/format does it use?
2. **Key storage**: How are API keys currently stored?
3. **Plaintext check**: Are keys visible in plaintext? (They probably are)
4. **Provider info**: Which LLM providers are configured?
5. **User specificity**: Is this per-user or system-wide?
6. **Size/complexity**: How large is this file? What else does it contain?

Show relevant excerpts (redact actual key values for security).

#### 1.2 Check Related Config Files
**Directory**: `config/`

Examine:
- `PIPER.defaults.md` - What are the defaults?
- `PIPER.md` - What's the main config template?
- `PIPER.user.md.example` - What's the example structure?
- `llm.yaml` - Does this exist? (gameplan mentioned it, but we found it doesn't)
- Any other config files related to LLM setup

Document the relationship between these files.

#### 1.3 Configuration Loading
**Search for**: How does Piper currently load configuration?

Find:
1. Where is `PIPER.user.md` parsed/loaded?
2. What module/service handles config loading?
3. Is there a `PiperConfigLoader` or similar?
4. Show the code that reads the config file

Look in:
- `main.py` - Startup configuration
- `services/config/` - Configuration services
- `config/*.py` - Python config modules

---

### Step 2: LLM Client Initialization

#### 2.1 Find LLM Client Code
**Search for**: Where are LLM clients (OpenAI, Anthropic, etc.) initialized?

Find and document:
1. **OpenAI client**: Where is it created? How does it get the API key?
2. **Anthropic client**: Where is it created? How does it get the API key?
3. **Other providers**: Are there Gemini, Perplexity, or other clients?
4. **Initialization timing**: Startup? Lazy? Per-request?

Look in:
- `main.py` - Startup initialization
- `services/llm/` - LLM service modules
- `services/orchestration/` - Orchestration that uses LLMs
- Search for: `openai.OpenAI`, `anthropic.Anthropic`, `ChatOpenAI`, etc.

#### 2.2 Trace Key Loading
For each LLM client found, trace:
1. **Direct code path**: From config file → to client initialization
2. **Key retrieval**: Exact code that gets the key from config
3. **Validation**: Is there any validation of keys?
4. **Error handling**: What happens if key is missing/invalid?

Show code snippets with file paths and line numbers.

---

### Step 3: Current Usage Patterns

#### 3.1 Where LLMs Are Used
**Search for**: All places that make LLM API calls

Find:
1. **Intent classification**: Does this use LLMs?
2. **Query routing**: Does this use LLMs?
3. **Response generation**: Does this use LLMs?
4. **Plugin system**: Do plugins use LLMs?
5. **Any other services**: What else calls LLM APIs?

Document each usage point with:
- File path and function name
- Which LLM provider it uses
- Whether provider is hardcoded or configurable

#### 3.2 Provider Selection Logic
**Question**: Is there any logic for choosing between providers?

Find:
1. Is provider hardcoded? (e.g., always uses OpenAI)
2. Is there provider routing/selection logic?
3. Are there fallbacks if one provider fails?
4. Can different services use different providers?

Show relevant code.

---

### Step 4: Security Analysis

#### 4.1 Current Security Posture
Document current security issues:

1. **Plaintext storage**: Confirm keys are in plaintext
2. **Git exposure**: Is `PIPER.user.md` in `.gitignore`?
3. **Log exposure**: Do keys appear in logs?
4. **Error messages**: Do errors leak key info?
5. **File permissions**: What permissions on config files?

Check:
```bash
# Git ignore status
git check-ignore config/PIPER.user.md

# File permissions
ls -la config/PIPER.user.md

# Search for keys in git history (danger!)
git log -p -- config/ | grep -i "api.*key" | head -20
```

#### 4.2 Identify Security Risks
List all current security risks:
- Where could keys leak?
- What happens if config file is committed?
- Are there backups with plaintext keys?
- Any other exposure vectors?

---

### Step 5: Migration Considerations

#### 5.1 Current Users
**Question**: Who/what depends on current config structure?

Find:
1. **Test suite**: Do tests use config file?
2. **Documentation**: Where is config documented?
3. **Setup scripts**: Any automated setup?
4. **CI/CD**: Does CI use config?

Document all dependencies.

#### 5.2 Breaking Changes
Identify what will break when we change config:
1. **File format change**: Moving from Markdown to what?
2. **Key storage location**: Moving from file to keychain?
3. **Code changes needed**: What code needs updating?
4. **Backward compatibility**: Can old config coexist with new?

---

### Step 6: Architecture Recommendations

Based on findings, recommend:

#### 6.1 Storage Backend Priority
Given what you learned, recommend priority order:
1. Should we start with env vars? (simple)
2. Should we go straight to keychain? (secure)
3. Should encrypted file be Priority 1? (portable + secure)

Justify based on:
- Current complexity
- PM's security requirement (no plaintext)
- Development workflow
- Platform constraints

#### 6.2 Migration Strategy
Recommend approach:
1. **Big bang**: Replace everything at once
2. **Gradual**: Support both old and new config temporarily
3. **Clean slate**: Require fresh setup (simplest)

#### 6.3 Implementation Order
Suggest phase order:
- What to build first?
- What can wait?
- What's the minimum viable secure config?

---

## Deliverable: Comprehensive Investigation Report

Provide report with these sections:

### 1. Current State Summary
- Configuration structure and format
- Where keys are stored
- Security posture (likely: insecure)
- How LLMs are initialized

### 2. Code Analysis
- File paths and line numbers for all config loading
- LLM client initialization code
- Usage patterns throughout codebase
- Current provider selection (or lack thereof)

### 3. Security Assessment
- Current risks (plaintext, git exposure, etc.)
- What needs immediate fixing
- What can be addressed gradually

### 4. Migration Impact
- What will break
- What dependencies exist
- Backward compatibility considerations

### 5. Architecture Recommendations
- Recommended storage backend priority
- Suggested implementation phases
- Minimum viable secure configuration
- Estimated complexity for each phase

### 6. Implementation Roadmap
Based on findings, suggest:
- Phase 1: What to build today
- Phase 2: What to build tomorrow
- Phase 3: What to defer

Include time estimates based on code complexity discovered.

---

## Output Format

For each finding, provide:
1. **What you found**: Clear statement
2. **Where**: File path and line numbers
3. **Code snippet**: Relevant code (redact actual keys!)
4. **Implications**: Why this matters for new implementation

For recommendations, provide:
1. **Option**: What to do
2. **Pros**: Why it's good
3. **Cons**: What's difficult
4. **Recommendation**: Your suggestion with reasoning

---

## STOP Conditions

None - this is pure investigation. Document everything, even surprising findings.

---

## Investigation Philosophy

**Time Lord Approach**:
- Take time to understand deeply
- Don't rush to solutions
- Document thoroughly
- Find hidden complexity before implementing
- Things take as long as they take

**Questions to Keep in Mind**:
- What will surprise us during implementation?
- What assumptions might be wrong?
- What edge cases exist?
- What technical debt will we discover?

---

## Success Criteria

Good investigation will:
- ✅ Give us confidence in architecture choices
- ✅ Reveal hidden complexity before we start coding
- ✅ Identify all code that needs updating
- ✅ Provide clear implementation roadmap
- ✅ Prevent false starts and rework

Take your time. Be thorough. This investigation sets up everything else.

---

**Ready for Code Agent investigation.**

**Estimated Time**: 1-2 hours for thorough investigation
**Worth It**: Absolutely - saves days of rework
