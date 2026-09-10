# Getting Started with Conversational AI

**Feature:** PM-034 Conversational AI with Anaphoric Reference Resolution
**Implementation:** Production-Ready ConversationManager
**Updated:** 2025-08-08

Transform your product management workflow from command-based interactions to natural, context-aware conversations. Piper Morgan now understands references like "that issue", "the document", and "show me the first item" automatically.

---

## Quick Start (15 Minutes)

### Before: Command Mode Interaction

**Traditional Approach:**

```
User: "Create GitHub issue for login bug"
Piper: "Created issue #85 for login bug"

User: "Show me GitHub issue #85"  ← Must remember exact issue number
Piper: "Here are the details for GitHub issue #85"
```

**Limitations:**

- Must remember exact identifiers (issue numbers, file names)
- No conversation memory across interactions
- Repetitive, mechanical interactions
- Context lost between sessions

### After: Conversational AI Interaction

**Natural Conversation:**

```
User: "Create GitHub issue for login bug"
Piper: "Created issue #85 for login bug. The issue has been assigned to the development team."

User: "Show me that issue again"  ← Natural reference automatically resolved
Piper: "Here are the details for GitHub issue #85"

User: "What about the testing strategy?"  ← Context-aware follow-up
Piper: "For the login bug (#85), here's the recommended testing approach..."
```

**Benefits:**

- Natural language references automatically resolved
- 10-turn conversation memory maintains context
- Seamless, human-like interactions
- Context preserved across entire conversation

---

## Your First Conversational Session

### Step 1: Start a Conversation (2 minutes)

**Web Interface:**

1. Open Piper Morgan web interface
2. Type your first request naturally: _"Create a high priority bug for the payment processing failure"_
3. Review the generated issue and confirm creation

**API Integration:**

```bash
curl -X POST http://your-piper-instance/api/v1/conversation/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "Create a high priority bug for the payment processing failure",
    "session_id": "my_session_123"
  }'
```

### Step 2: Use Natural References (3 minutes)

**Follow up with natural language:**

```
User: "Show me that issue again"
User: "Update the bug description"
User: "What's the status of that ticket?"
User: "Assign it to the backend team"
```

**Piper automatically resolves:**

- "that issue" → GitHub issue #85
- "the bug" → Payment processing failure
- "that ticket" → Same issue in different context

### Step 3: Multi-turn Context (5 minutes)

**Continue the conversation naturally:**

```
User: "What about the testing strategy?"
Piper: "For the payment processing bug (#85), here's the recommended testing approach..."

User: "How long will the fix take?"
Piper: "Based on the payment processing issue complexity, estimated timeline is..."

User: "Create a follow-up task for the security review"
Piper: "Created security review task #86 linked to payment processing bug #85"
```

**Context maintained throughout:**

- All references to "the bug", "the issue", "it" automatically resolved
- Conversation history preserved for 10 turns
- Seamless context switching between related topics

### Step 4: Advanced References (5 minutes)

**Test different reference types:**

```
User: "Show me the first item from our backlog"
User: "Update the latest document"
User: "What's the status of my current task?"
User: "Close the main issue and create a follow-up"
```

**Automatic resolution:**

- "the first item" → Most recent backlog item
- "the latest document" → Most recently uploaded file
- "my current task" → Your active work item
- "the main issue" → Primary issue in current context

---

## Natural Language Patterns

### Definite References

**Pattern Examples:**

```
"Show me that issue again"
"Update the document"
"Close the bug"
"What's the status of the task?"
```

**How it works:**

- Piper remembers entities mentioned in conversation
- "that", "the", "this" automatically resolved to most relevant item
- 90%+ accuracy on reference resolution
- <150ms response time for resolution

### Demonstrative References

**Pattern Examples:**

```
"Show me this one"
"Update that file"
"Close these items"
"What about those bugs?"
```

**Resolution logic:**

- "this one" → Most recently mentioned item
- "that file" → Previously referenced document
- "these items" → Multiple items in current context
- Context window maintains 10-turn history

### Comparative References

**Pattern Examples:**

```
"Show me the first item"
"Update the latest document"
"What's the main issue?"
"Close the oldest task"
```

**Intelligent resolution:**

- "first" → Chronologically first item
- "latest" → Most recently created/updated
- "main" → Highest priority or most important
- "oldest" → Earliest created item

### Contextual References

**Pattern Examples:**

```
"What's my current task?"
"Show me our project status"
"Update the sprint backlog"
"What about the team's progress?"
```

**Personalized resolution:**

- "my" → Your assigned items
- "our" → Team/project context
- "the team's" → Collective team items
- Context includes user and project information

---

## Before/After Examples

### Example 1: Issue Management

**Before (Command Mode):**

```
User: "Create bug for login failure"
Piper: "Created issue #123 for login failure"

User: "Show me GitHub issue #123"  ← Must remember number
Piper: "Here are the details for GitHub issue #123"

User: "Update GitHub issue #123 with new information"  ← Repetitive
Piper: "Updated GitHub issue #123"

User: "What's the status of GitHub issue #123?"  ← Mechanical
Piper: "GitHub issue #123 is in progress"
```

**After (Conversational AI):**

```
User: "Create bug for login failure"
Piper: "Created issue #123 for login failure"

User: "Show me that issue again"  ← Natural reference
Piper: "Here are the details for GitHub issue #123"

User: "Update it with new information"  ← Simple reference
Piper: "Updated GitHub issue #123"

User: "What's the status?"  ← Context-aware
Piper: "The login failure issue is in progress"
```

### Example 2: Document Management

**Before (Command Mode):**

```
User: "Upload requirements_v2.pdf"
Piper: "Uploaded requirements_v2.pdf to knowledge base"

User: "Search requirements_v2.pdf for API specifications"  ← Exact filename
Piper: "Found 3 API specifications in requirements_v2.pdf"

User: "Summarize requirements_v2.pdf"  ← Repetitive filename
Piper: "Summary of requirements_v2.pdf..."

User: "Compare requirements_v2.pdf with requirements_v1.pdf"  ← Complex
Piper: "Comparison between requirements_v2.pdf and requirements_v1.pdf..."
```

**After (Conversational AI):**

```
User: "Upload the new requirements document"
Piper: "Uploaded requirements_v2.pdf to knowledge base"

User: "Search it for API specifications"  ← Natural reference
Piper: "Found 3 API specifications in the requirements document"

User: "Summarize the document"  ← Simple reference
Piper: "Summary of the requirements document..."

User: "Compare it with the previous version"  ← Context-aware
Piper: "Comparison between requirements_v2.pdf and requirements_v1.pdf..."
```

### Example 3: Project Management

**Before (Command Mode):**

```
User: "Create sprint task for user authentication"
Piper: "Created task #456 for user authentication"

User: "Show me task #456 details"  ← Must remember number
Piper: "Task #456 details..."

User: "Update task #456 status to in progress"  ← Mechanical
Piper: "Updated task #456 status"

User: "What's the priority of task #456?"  ← Repetitive
Piper: "Task #456 has high priority"
```

**After (Conversational AI):**

```
User: "Create sprint task for user authentication"
Piper: "Created task #456 for user authentication"

User: "Show me the task details"  ← Natural reference
Piper: "Task #456 details..."

User: "Mark it as in progress"  ← Simple reference
Piper: "Updated the authentication task status"

User: "What's the priority?"  ← Context-aware
Piper: "The user authentication task has high priority"
```

---

## Troubleshooting Guide

### Common Issues

**Issue: "I can't find that issue"**

- **Cause**: Reference not found in conversation context
- **Solution**: Be more specific or restart conversation
- **Example**: "Show me GitHub issue #85" instead of "Show me that issue"

**Issue: "Wrong item resolved"**

- **Cause**: Multiple similar items in context
- **Solution**: Use more specific references
- **Example**: "Show me the login bug" instead of "Show me the bug"

**Issue: "Context lost"**

- **Cause**: Conversation exceeded 10-turn window
- **Solution**: Start new session or use specific identifiers
- **Example**: "Show me GitHub issue #85" for older references

**Issue: "Slow response"**

- **Cause**: Complex reference resolution
- **Solution**: Use simpler references or wait for resolution
- **Example**: "Show me the issue" instead of "Show me the first item from the backlog"

### Best Practices

**For Best Results:**

1. **Be specific when needed**: "Show me the login bug" vs "Show me the bug"
2. **Use natural language**: "Update it" instead of "Update GitHub issue #123"
3. **Maintain context**: Keep related topics in same conversation
4. **Restart when needed**: New session for completely different topics

**Avoid:**

- Very long conversations (>10 turns) for complex topics
- Vague references when multiple similar items exist
- Mixing unrelated topics in same conversation
- Expecting perfect resolution for ambiguous references

### Performance Tips

**Optimal Usage:**

- **Response Time**: <150ms for most references
- **Accuracy**: 90%+ for clear references
- **Context Window**: 10 turns maintained automatically
- **Cache Duration**: 5 minutes for active conversations

**When to Use:**

- ✅ Natural conversation flows
- ✅ Related topic discussions
- ✅ Multi-step workflows
- ✅ Context-dependent queries

**When to Use Command Mode:**

- ❌ Completely new topics
- ❌ Very specific technical queries
- ❌ Batch operations
- ❌ System administration tasks

---

## Advanced Features

### Conversation Settings

**Customize your experience:**

```json
{
  "context_window": 15, // Increase from default 10
  "reference_resolution": true, // Enable/disable references
  "performance_mode": "balanced", // speed/balanced/high_accuracy
  "cache_ttl": 300 // Cache duration in seconds
}
```

### Session Management

**Track conversation history:**

```bash
# Get current conversation context
curl -X GET "http://your-piper-instance/api/v1/conversation/my_session_123/context"

# Update conversation settings
curl -X PUT "http://your-piper-instance/api/v1/conversation/my_session_123/settings" \
  -H "Content-Type: application/json" \
  -d '{"context_window": 15}'
```

### Reference Resolution History

**Analyze your conversation patterns:**

```bash
# Get reference resolution history
curl -X GET "http://your-piper-instance/api/v1/conversation/my_session_123/references"
```

**Sample output:**

```json
{
  "references": [
    {
      "original_text": "that issue",
      "resolved_entity": "GitHub issue #85",
      "confidence": 0.98,
      "resolution_time_ms": 15.3
    }
  ],
  "average_confidence": 0.95,
  "average_resolution_time_ms": 14.0
}
```

---

## Migration from Command Mode

### Quick Migration Checklist

**For Existing Users:**

- [ ] **Start with simple references**: "Show me that issue" instead of exact numbers
- [ ] **Use natural language**: "Update it" instead of "Update GitHub issue #123"
- [ ] **Maintain conversation context**: Keep related topics together
- [ ] **Restart when needed**: New session for completely different topics
- [ ] **Fall back to specifics**: Use exact identifiers when references fail

### Gradual Adoption Strategy

**Week 1: Experiment**

- Try conversational references for simple queries
- Compare with command mode for same tasks
- Note which references work best

**Week 2: Expand Usage**

- Use conversations for multi-step workflows
- Test different reference types
- Practice natural language patterns

**Week 3: Full Adoption**

- Switch to conversational mode for most interactions
- Use command mode only for specific technical tasks
- Leverage conversation memory for complex workflows

### Command Mode Fallback

**When to use exact identifiers:**

- Very specific technical queries
- System administration tasks
- Batch operations
- When conversation context is unclear

**Example fallback:**

```
User: "Show me that issue"  ← Conversational
Piper: "I can't find a specific issue in our conversation"

User: "Show me GitHub issue #85"  ← Command mode fallback
Piper: "Here are the details for GitHub issue #85"
```

---

## Success Metrics

### Personal Success Indicators

**You're successfully using Conversational AI when:**

- ✅ Natural references work 90%+ of the time
- ✅ Response times feel instant (<150ms)
- ✅ Conversation flows feel natural and human-like
- ✅ Context is maintained across multiple interactions
- ✅ You rarely need to use exact identifiers

### Team Success Indicators

**Your team is successfully adopting when:**

- ✅ 80%+ of interactions use conversational mode
- ✅ Reference resolution accuracy >90%
- ✅ Average response time <150ms
- ✅ User satisfaction scores improve
- ✅ Training time for new users decreases

### Performance Benchmarks

**Target Performance:**

- **Reference Resolution**: 90%+ accuracy
- **Response Time**: <150ms average
- **Context Window**: 10 turns maintained
- **Cache Hit Ratio**: >95% for active sessions
- **User Satisfaction**: >4.5/5 rating

**Current Performance (PM-034 Phase 3):**

- **Reference Resolution**: 100% accuracy ✅
- **Response Time**: 2.33ms average ✅
- **Context Window**: 10 turns operational ✅
- **Cache Hit Ratio**: >95% achieved ✅
- **User Satisfaction**: TBD (new feature)

---

## Next Steps

### Immediate Actions

1. **Try your first conversation**: Start with a simple issue creation
2. **Test reference resolution**: Use "that issue" in follow-up messages
3. **Explore natural patterns**: Try different reference types
4. **Practice multi-turn context**: Keep related topics in same conversation

### Advanced Learning

1. **Read "Understanding Anaphoric References"**: Deep dive into reference resolution
112. **Explore "Conversation Memory and Context"**: Learn about context window management
3. **Review "Upgrading from Command Mode"**: Complete migration guide
4. **Practice with Real Examples**: Test conversation scenarios

### Support Resources

- **API Documentation**: Complete conversation endpoint reference
- **Performance Monitoring**: Real-time conversation metrics
- **Troubleshooting Guide**: Common issues and solutions
- **Community Forum**: Share tips and best practices

---

## Next Steps

- [Understanding Anaphoric References](./understanding-anaphoric-references.md)
- [Conversation Memory and Context](./conversation-memory-guide.md)
- [Upgrading from Command Mode](./upgrading-from-command-mode.md)
- [Conversation Examples](./conversation-scenario-examples.md)
- [Report an Issue](https://github.com/your-repo/issues)

---

**Ready to start?** Begin with a simple conversation and experience the transformation from command mode to natural, context-aware interactions!
