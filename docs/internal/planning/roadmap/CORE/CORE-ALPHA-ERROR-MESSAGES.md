# CORE-ALPHA-ERROR-MESSAGES - Add Conversational Error Fallbacks

**Priority**: P1 CRITICAL
**Labels**: `ux`, `error-handling`, `mvp-quality`
**Milestone**: Sprint A8 Phase 3
**Estimated Effort**: 4 hours

#### Problem
Current error messages are technical and break the conversational experience:
- "An API error occurred"
- "No handler for action: create_github_issue"
- "Operation timed out after 30 seconds"
- Generic fallthrough for unknown intents

#### Required Conversational Fallbacks

**Empty Input**:
- Current: 30-second timeout
- Required: "I didn't quite catch that. Could you share more about what you'd like to work on?"

**Unknown Actions**:
- Current: "No handler for action: X"
- Required: "I'm still learning how to help with that. What else can I assist with?"

**Timeouts**:
- Current: "Operation timed out"
- Required: "That's a complex request - let me reconsider. Could you break it down?"

**Unknown Intents**:
- Current: Generic error
- Required: "I'm not sure I understood correctly. Could you rephrase?"

**System Errors**:
- Current: "An API error occurred"
- Required: "Something went wrong on my end. Let me try again, or would you like to try something else?"

#### Implementation
1. Create ConversationalErrorMessages class
2. Add input validation before processing
3. Catch specific error types
4. Return friendly messages
5. Log technical details server-side only

#### Acceptance Criteria
- [ ] All error types have conversational fallbacks
- [ ] Empty input caught immediately
- [ ] No technical jargon in user messages
- [ ] Error messages suggest next actions
- [ ] Technical details logged but not shown
- [ ] Maintains Piper's helpful tone
- [ ] All tests pass
