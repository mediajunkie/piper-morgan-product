# Gameplan Template v9.5 - Complete Phase Documentation
*Last Updated: June 15, 2026 (deployment-model reframe)*
*Key Addition: Data Flow, Integration Points, Pattern Adaptation, Conversation Design, Post-Completion sections (Issue #490 retrospective)*

---

## Phase Structure Overview

### Complete Phase Sequence
- **Phase -1**: Infrastructure Verification (with PM)
- **Phase 0**: Initial Bookending (GitHub investigation)
- **Phase 0.5**: Frontend-Backend Contract Verification (MANDATORY for UI work)
- **Phase 0.6**: Data Flow & Integration Verification (NEW - for multi-layer features)
- **Phases 1-N**: Development Work (progressive bookending)
- **Phase Z**: Final Bookending & Handoff

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Writing Rest of Gameplan

**Purpose**: Prevent wrong gameplans based on incorrect assumptions

### Part A: Chief Architect's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [ ] Web framework: ____________ (I think: FastAPI/Flask/None/Unknown)
- [ ] CLI structure: ____________ (I think: Click/Argparse/Custom/Unknown)
- [ ] Database: ____________ (I think: PostgreSQL/SQLite/None/Unknown)
- [ ] Testing framework: ____________ (I think: pytest/unittest/None/Unknown)
- [ ] Existing endpoints: ____________ (I think these exist: _______)
- [ ] Missing features: ____________ (I think we need: _______)

**My understanding of the task**:
- I believe we need to: ____________
- I think this involves: ____________
- I assume the current state is: ____________

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?** (Check all that apply)

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [ ] **SKIP WORKTREE** - Overhead criteria dominate
- [ ] **PM DECISION** - Mixed signals, escalate

**If USE WORKTREE:**
```bash
# Agent claims prompt with worktree
./scripts/worktree-setup.sh <prompt-id> <session-id>
cd .trees/<prompt-id>-<session>/
```

**If SKIP WORKTREE:**
Document rationale: ____________
(e.g., "Single agent, 5 files, 15 min estimate - worktree overhead exceeds benefit")

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la web/
   ls -la services/
   ls -la cli/
   find . -name "*[relevant_feature]*"
   ```

2. **Recent work in this area?**
   - Last changes to this feature: ____________
   - Known issues/quirks: ____________
   - Previous attempts: ____________

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [ ] Add to existing application
   - [ ] Fix broken functionality
   - [ ] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Establish context, verify issue exists, understand current state

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view [ISSUE_NUMBER]
   ```

2. **Codebase Investigation**
   ```bash
   # Find existing patterns
   grep -r "[pattern]" . --include="*.py"

   # Check git history
   git log --grep="[feature]" --oneline

   # Verify current state
   python main.py  # or appropriate test
   ```

3. **Update GitHub Issue**
   ```bash
   gh issue edit [ISSUE_NUMBER] --body "
   ## Status: Investigation Started
   - [ ] Current state documented
   - [ ] Root cause identified
   - [ ] Fix approach determined
   "
   ```

### STOP Conditions
- Issue doesn't exist or is wrong number
- Feature already implemented
- Different problem than described

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY for UI work)

### Purpose
Prevent path mismatches between backend routes and frontend API calls. This phase is REQUIRED when the issue involves both backend API routes AND frontend JavaScript/templates.

### When to Apply
- ✅ Creating new API endpoints + UI that calls them
- ✅ Modifying existing API paths
- ✅ Adding JavaScript that makes fetch() calls
- ❌ Backend-only changes (skip this phase)
- ❌ Frontend-only styling changes (skip this phase)

### Required Actions

#### 1. After Backend Routes Created, BEFORE Frontend Work
```bash
# Get all endpoint paths from new route file
grep -n "@router\." web/api/routes/[new_file].py

# Get the mount prefix from app.py or router_initializer.py
grep -n "include_router\|mount_router" web/app.py | grep [module_name]
# OR
grep -n "[module_name]" web/router_initializer.py
```

#### 2. Calculate Full Paths
```markdown
| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| status   | /status    | /setup       | /setup/status |
| create   | /create    | /api/v1/todos | /api/v1/todos/create |
```

#### 3. Verify Paths Work (Server Running)
```bash
# Test each endpoint BEFORE writing frontend
curl -s http://localhost:8001/[full-path]
# Must NOT return {"detail":"Not Found"}
```

#### 4. Static File Verification
```bash
# Verify where static files are served from
grep -n "StaticFiles" web/app.py
# Note the directory path (e.g., web/static vs static)

# If creating JS/CSS files, verify location matches
ls -la web/static/js/  # or wherever app.py points
```

### STOP Conditions
- If ANY endpoint returns 404 → fix backend before frontend
- If static file path is wrong → fix mount before creating files
- If mount prefix unclear → verify in app.py or ask PM

### Evidence Required
```bash
# Document verified paths in gameplan or session log
echo "Verified paths:"
echo "  /setup/status → HTTP 200"
echo "  /setup/check-system → HTTP 200"
echo "  Static files: web/static/ → /static/"
```

---

## Phase 0.6: Data Flow & Integration Verification (NEW)

### Purpose
Prevent data propagation failures in multi-layer features. This phase is REQUIRED when the feature involves data flowing through multiple service layers (e.g., Route → Service → Handler → Repository).

**Added from Issue #490 Retrospective**: The #490 portfolio onboarding gameplan followed the standup pattern but didn't account for the critical difference: standup uses `session_id` for lookup while portfolio needs `user_id`. This caused 4 bugs (beads 9mc, a0h, ejj, 3pv) that required Five Whys debugging.

### When to Apply
- ✅ Multi-turn conversational features
- ✅ Features requiring user context across requests
- ✅ Features that "follow an existing pattern" but with different requirements
- ✅ Any feature touching auth/session/user_id propagation
- ❌ Single-layer changes (skip this phase)
- ❌ Stateless request/response features (skip this phase)

### Part A: Data Flow Requirements

#### User Context Propagation
Document which layers need user_id/session_id and verify each handoff:

| Layer | Needs user_id? | Needs session_id? | Source of value |
|-------|----------------|-------------------|-----------------|
| Route handler | [ ] | [ ] | `get_current_user` dependency |
| Service method | [ ] | [ ] | Parameter from route |
| Domain handler | [ ] | [ ] | Parameter from service |
| Repository | [ ] | [ ] | Parameter from handler |

**Verification Commands**:
```bash
# Check if route has user dependency
grep -n "get_current_user\|current_user" web/api/routes/[file].py

# Check if service method accepts user_id
grep -n "def.*user_id" services/[service].py

# Check if handler receives user_id
grep -n "def.*user_id" services/[handler].py
```

#### State Persistence
- [ ] Where is state stored? (in-memory dict / database / session / redis)
- [ ] Key for lookup: `user_id` / `session_id` / `onboarding_id` / other: ______
- [ ] How is state retrieved on subsequent requests?
- [ ] What happens if state lookup fails? (error / create new / fallback)

### Part B: Integration Points Checklist

For EACH integration point where one layer calls another:

| Caller | Callee | Import Path Verified? | Method Name Verified? | Parameters Available? |
|--------|--------|----------------------|----------------------|----------------------|
| intent_service | conversation_handler | [ ] | [ ] | [ ] |
| conversation_handler | portfolio_handler | [ ] | [ ] | [ ] |
| portfolio_handler | portfolio_manager | [ ] | [ ] | [ ] |
| portfolio_manager | project_repository | [ ] | [ ] | [ ] |

**Verification Commands**:
```bash
# Verify import path exists
python -c "from [module.path] import [Class]"

# Verify method exists
python -c "from [module.path] import [Class]; print(hasattr([Class], '[method_name]'))"
```

### Part C: Pattern Adaptation Notes

**When referencing an existing pattern (e.g., "follow standup pattern"):**

| Aspect | Source Pattern | This Implementation | Why Different? |
|--------|---------------|---------------------|----------------|
| State lookup key | session_id | user_id | Cross-session continuity needed |
| State storage | in-memory | in-memory | Same |
| Auth requirement | optional | required | Need consistent user_id |

**Potential Pitfalls from Differences**:
- [ ] List each difference that could cause bugs
- [ ] Note mitigation for each

### STOP Conditions
- If ANY import path doesn't exist → fix before implementing
- If method name is wrong → verify correct name before calling
- If required parameter not available at call site → trace back to find source
- If pattern difference not documented → document before proceeding

---

## Phase 0.7: Conversation Design (For Conversational Features)

### Purpose
Prevent conversation flow bugs by designing before implementing. This phase is REQUIRED for any feature involving multi-turn conversations.

**Added from Issue #490 Retrospective**: The "Yes, I have another project" bug occurred because the conversation design didn't account for affirmative responses that aren't content. A conversation design table would have caught this.

### When to Apply
- ✅ Onboarding flows
- ✅ Setup wizards via chat
- ✅ Multi-turn data gathering
- ✅ Confirmation dialogs
- ❌ Single-turn Q&A (skip this phase)

### Part A: Happy Path Script

Document the exact expected conversation:

```
Turn 1:
  User: "Hello"
  Piper: "[exact response]"
  State: INITIATED → GATHERING

Turn 2:
  User: "[expected input]"
  Piper: "[exact response]"
  State: GATHERING → GATHERING

Turn 3:
  User: "[completion signal]"
  Piper: "[exact response]"
  State: GATHERING → CONFIRMING
```

### Part B: Edge Cases Table

| User Input | Current State | Expected Behavior | Response Template |
|------------|---------------|-------------------|-------------------|
| "yes" / "sure" / "yeah" | GATHERING | Prompt for content | "Great! What's the name?" |
| "no thanks" | ANY | Exit gracefully | "No problem! What else..." |
| [rambling paragraph] | GATHERING | Extract or clarify? | Decision: ______ |
| "that's all" / "done" | GATHERING | Transition to confirm | "Let me confirm..." |
| [empty/whitespace] | ANY | Re-prompt | "I didn't catch that..." |

### Part C: Pattern Definitions

Define regex patterns BEFORE implementation:

```python
# Affirmation (NOT content)
CONFIRM_PATTERNS = [
    r"\b(yes|yeah|yep|sure|correct|right)\b",
    # ...
]

# Completion signals
DONE_PATTERNS = [
    r"\b(done|that'?s? all|finished)\b",
    # ...
]

# Decline signals
DECLINE_PATTERNS = [
    r"\b(no|nope|not now|skip)\b",
    # ...
]
```

### Part D: State Machine

```
INITIATED
    ├── [accept] → GATHERING
    └── [decline] → DECLINED (terminal)

GATHERING
    ├── [content] → GATHERING (add item, loop)
    ├── [affirm without content] → GATHERING (prompt for content)
    ├── [done signal] → CONFIRMING
    └── [decline] → DECLINED (terminal)

CONFIRMING
    ├── [confirm] → COMPLETE (terminal)
    ├── [add more] → GATHERING
    └── [decline] → DECLINED (terminal)
```

### STOP Conditions
- If edge case behavior unclear → get PM decision before implementing
- If pattern overlap detected → resolve ambiguity before implementing

---

## Phase 0.8: Post-Completion Integration (NEW)

### Purpose
Ensure the feature properly integrates with the rest of the system after completion.

**Added from Issue #490 Retrospective**: Portfolio onboarding created projects but didn't set `setup_complete = true`, leaving users in a broken state. This section ensures completion side-effects are specified.

### When to Apply
- ✅ Features that change user state
- ✅ Features that create/modify database records
- ✅ Features that should affect other feature behavior
- ❌ Read-only features (skip this phase)

### Completion Side-Effects Checklist

When this feature completes successfully:

| Side Effect | Table/Field | Value | Verified? |
|-------------|-------------|-------|-----------|
| User marked as set up | users.setup_complete | true | [ ] |
| Timestamp recorded | users.setup_completed_at | now() | [ ] |
| Projects created | projects table | N rows | [ ] |
| Preference saved | user_preferences | key=value | [ ] |

### Downstream Behavior Changes

After this feature completes, what should behave differently?

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| Greeting | Shows onboarding prompt | Shows normal greeting |
| Orientation modal | Appears | Does not appear |
| Project list | Empty | Shows captured projects |

### Verification Query

```sql
-- Verify completion state after feature runs
SELECT setup_complete, setup_completed_at,
       (SELECT COUNT(*) FROM projects WHERE owner_id = users.id) as project_count
FROM users WHERE id = '[user_id]';
```

---

## Phases 1-N: Development Work with Progressive Bookending

### Multi-Agent Deployment (DEFAULT)

**Current deployment model** — four tiers (Arch-ratified 2026-06-14):

1. **One Claude Code session per agent** — each role runs its own session; no Cursor pairing
2. **Subagents via Task tool** — for parallelizable work (parallel discovery, analysis, test generation)
3. **Duty-cycle cohort over mailboxes** — cross-role coordination; mailboxes are the cross-agent signaling layer
4. **Option B ephemeral worktrees** — substantive sessions use the auto-created worktree; push to `origin/main`

#### Phase [X]: [Specific Work Description]

##### Instructions for this phase
```markdown
[Broad investigation/implementation approach]
- Deploy subagents (Task tool) for parallel discovery; you orchestrate and synthesize
- Check patterns across codebase
- Find all related code
- Focused implementation disciplines (specific files, exact changes, targeted testing) go in the subagent prompt
```

### Progressive Bookending
After each subtask completion:
```bash
gh issue comment [ISSUE_NUMBER] -b "✓ Completed: [subtask]
Evidence: [link or output]"
```

## GitHub Progress Discipline (MANDATORY)
- Agents UPDATE progress descriptions
- PM VALIDATES by checking boxes
- Include "(PM will validate)" in criteria

## Test Scope Requirements in Acceptance Criteria
- [ ] Unit tests: [what components they test]
- [ ] Integration tests: [what flows they verify]
- [ ] **Wiring tests**: [what import/method/parameter chains they verify] (NEW)
- [ ] Performance tests: [what metrics required]
- [ ] Regression tests: [what they prevent]

### Cross-Validation Points
- Agents share findings via GitHub
- Different approaches validate each other
- Evidence required from both

### Evidence Format
- Terminal output: paste key lines
- Test results: link to full output
- Commits: include hash
- Performance: include metrics

---

## Phase Z: Final Bookending & Handoff

### Purpose
Complete final verification, update all documentation, prepare for PM approval

### Required Actions

#### 1. GitHub Final Update
```bash
gh issue edit [ISSUE_NUMBER] --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [evidence]
- [x] No regressions: [evidence]
- [x] Documentation updated

### Ready for PM Review
"
```

## GitHub Closeout Discipline (MANDATORY)
- Agents provide evidence issue is completed
- PM VALIDATES and closes issue or identifies incomplete work or completed work claims without sufficient evidence

#### 2. Documentation Updates
- [ ] Update relevant ADRs if decisions made
- [ ] Update architecture.md if flow changed
- [ ] Remove/update misleading TODO comments
- [ ] Update CURRENT-STATE.md if significant

#### 3. Evidence Compilation
- [ ] All terminal outputs in session log
- [ ] Key code changes documented
- [ ] Before/after behavior captured
- [ ] Performance metrics if relevant

#### 4. Handoff Preparation (if part of sequence)
- [ ] Document discoveries for next issue
- [ ] Note unexpected complexities
- [ ] Flag architectural concerns
- [ ] Prepare context for next phase

#### 5. Session Completion
- [ ] Run satisfaction assessment
- [ ] Complete session log
- [ ] Note process improvements

#### 6. PM Approval Request
```markdown
@PM - Issue #[NUMBER] complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- Documentation updated ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

### CRITICAL: Agents Do NOT Close Issues
**Only PM closes issues after review and approval**

---

## Multi-Agent Coordination Plan

### Agent Deployment Map
| Phase | Agent Type | Issue | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1 | Code Agent | #XXX | 10 tests, coverage report | Test locations |
| 2 | Subagent (Task tool) | #XXY | File modifications | Diff summary |
| 3 | Lead Dev | #XXZ | Integration verified | User test |

*(Copy and customize for each gameplan)*

### Verification Gates
- [ ] Phase 1: Unit tests passing
- [ ] Phase 2: Integration tests passing
- [ ] Phase 2a: **Routing integration tests** (for intent/handler work)
- [ ] Phase 2b: **Wiring integration tests** (for multi-layer features) (NEW)
- [ ] Phase 3: User verification complete
- [ ] Phase 4: Documentation updated

### CRITICAL: Routing Integration Tests (Issue #521 Learning)

**For any work involving intent handlers, classifiers, or query routing:**

Unit tests that mock routing are NOT sufficient. You MUST include **routing integration tests** that verify the full path:

```python
# BAD: Tests handler in isolation (mocked routing)
async def test_handler_works():
    result = await handler._handle_attention_query(mock_intent, session_id)
    assert "attention" in result  # ✅ Passes but doesn't prove routing works

# GOOD: Tests full routing path (pre-classifier → intent service → handler)
async def test_routing_reaches_handler():
    pre_classifier = PreClassifier()
    intent = pre_classifier.pre_classify("what needs my attention")
    assert intent.category == IntentCategory.QUERY
    assert intent.action == "attention_query"  # ✅ Proves routing works
```

**Why this matters:** Issue #521 had 17 passing unit tests but the queries failed in production because the pre-classifier intercepted them before reaching the handlers. Routing integration tests catch this.

### CRITICAL: Wiring Integration Tests (Issue #490 Learning) (NEW)

**For any work involving data flow through multiple service layers:**

Unit tests that mock internal methods are NOT sufficient. You MUST include **wiring integration tests** that verify:

```python
# BAD: Mocks internal method (hides import/wiring bugs)
@patch('services.conversation.conversation_handler._check_portfolio_onboarding')
async def test_onboarding_works(mock_check):
    mock_check.return_value = {"response": "..."}
    # ✅ Passes but doesn't prove real wiring works

# GOOD: Tests real import chain without mocking internals
async def test_real_wiring():
    # Verify import works
    from services.conversation.conversation_handler import ConversationHandler
    from services.onboarding.portfolio_handler import PortfolioOnboardingHandler

    # Verify method exists
    assert hasattr(ConversationHandler, '_handle_active_onboarding')

    # Verify parameter propagation (with real objects, minimal mocking)
    handler = ConversationHandler(...)
    # Test with real user_id flowing through
```

**Why this matters:** Issue #490 had passing tests but failed in production because tests mocked `_check_portfolio_onboarding`, hiding that `user_id` wasn't being passed through the real code path.

### Evidence Collection Points
1. **After each subagent returns**: Collect evidence immediately
2. **Before phase transition**: Verify accumulated evidence
3. **Before issue closure**: Compile all evidence into issue
4. **At session end**: Update omnibus log and session log

### Handoff Quality Checklist
Before accepting handoff from any agent:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included
- [ ] User verification steps documented
- [ ] Blockers explicitly stated (if any)

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- Infrastructure doesn't match gameplan
- Critical features break
- Performance degrades unacceptably
- Security issues discovered
- Assumptions prove wrong
- **Router/adapter methods missing** (Issue #525 learning)
- **Import path doesn't exist** (Issue #490 learning) (NEW)
- **Method name typo** (Issue #490 learning) (NEW)
- **Required parameter not available at call site** (Issue #490 learning) (NEW)

### Infrastructure Compatibility Check (Issue #525 Learning)

**For any work involving integration handlers (Calendar, GitHub, Slack, Notion):**

Before implementing handlers that call integration adapters:
- [ ] Does the router have all required methods?
- [ ] If not, is "extend router" in scope, or should we STOP?
- [ ] CORE-QUERY-1 pattern compliance verified?

**Why this matters:** Issue #518 Phase A bypassed `CalendarIntegrationRouter` because it lacked `get_events_in_range()` and `get_recurring_events()`. The correct fix was to extend the router, not bypass it. Pre-commit hooks caught the violation but the gameplan should have prevented it.

**Pattern Enforcement:**
- ✅ Handler → Router → Adapter (correct)
- ❌ Handler → Adapter directly (violates CORE-QUERY-1)

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing success
✅ Test results with full output
✅ Performance metrics
✅ Git commits/diffs
✅ Before/after screenshots
✅ SQL query showing state change (NEW)

❌ "Should work"
❌ "Tests pass" without output
❌ "Fixed" without proof

---

## Success Criteria Template

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] **Wiring tests included** (for multi-layer features) (NEW)
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Session Patterns

### Starting a Session
1. Check BRIEFING-CURRENT-STATE
2. Review GitHub issue
3. Verify infrastructure (Phase -1)
4. Begin Phase 0

### During Work
- Progressive bookending
- Evidence collection
- Cross-validation
- GitHub updates

### Ending a Session
- Phase Z completion
- Satisfaction assessment
- Session log finalized
- Clear handoff if incomplete

---

## Remember

- **Inchworm Protocol**: Complete each phase 100% before moving
- **Evidence Required**: No claims without proof
- **75% Pattern**: Complete existing work, don't replace
- **Multi-Agent Default**: Single agent needs justification
- **PM Closes Issues**: Agents request approval only
- **Data Flow Matters**: Trace user_id/session_id through all layers (NEW)
- **Test Real Wiring**: Don't mock internal methods (NEW)

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| v9.5 | 2026-06-15 | #1206 item-3 reframe (Docs, Arch-ratified 2026-06-14): replaced "Both Agents / Multi-Agent Deployment DEFAULT" pairing model with four-tier deployment model (one Code session per agent / subagents via Task tool / duty-cycle cohort over mailboxes / Option B ephemeral worktrees); removed #1058 hygiene flags. |
| v9.4 | 2026-06-12 | #1058 hygiene pass (HOST): removed stale Cursor Agent references (Cursor Instructions sub-block, audit-matrix Cursor row → subagent). Flagged for PM/Lead/Arch ratification (NOT changed): the "Both Agents / Multi-Agent Deployment DEFAULT" pairing model; Phase -1 PM-verification block currency (audit-cascade Phase 1 may cover it). |
| v9.3 | 2026-01-10 | Added Phase 0.6 (Data Flow), Phase 0.7 (Conversation Design), Phase 0.8 (Post-Completion), Wiring Tests requirement. Issue #490 retrospective learnings. |
| v9.2 | 2025-12-04 | Added Worktree Assessment in Phase -1 (Issue #463 learning) |
| v9.0 | 2025-09-22 | Initial complete phase documentation |

---

*This template ensures systematic, complete execution following all methodology learnings*
