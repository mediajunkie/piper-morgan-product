# Conversation Memory and Context Guide

**Feature:** PM-034 10-Turn Conversation Memory
**Implementation:** Production-Ready Context Window System
**Updated:** 2025-08-09

Understand how Piper Morgan remembers your conversations and maintains context across multiple interactions. This guide explains the "magic" behind conversational AI that feels natural and human-like.

---

## How Piper's Memory Works

### The 10-Turn Window

Piper remembers your last 10 interactions in a conversation. Think of it like having a conversation with someone who takes excellent notes - Piper keeps track of everything you've discussed and can reference it naturally.

**Key Benefits:**

- **Natural Flow**: No need to repeat yourself or remember exact details
- **Context Awareness**: Piper understands what you're referring to
- **Seamless Transitions**: Switch between related topics effortlessly
- **Human-like Experience**: Conversations feel natural and intuitive

### What Piper Remembers

Piper automatically tracks and remembers:

- ✅ **Issues, PRs, and tasks** you've mentioned
- ✅ **People and team members** you've referenced
- ✅ **Projects and sprints** in discussion
- ✅ **Documents and files** you've uploaded or searched
- ✅ **Actions you've taken** and their results
- ✅ **Timeline and status information** for all entities

### Memory in Action

Piper's memory works seamlessly across your entire conversation. Here are real examples showing how context is maintained:

#### Example 1: Issue Management Memory

```
You: "Create a high priority bug for the payment processing failure"
Piper: "Created GitHub issue #85 for payment processing failure. Priority: High, Labels: [bug, payments, international]."

You: "What's the current status?"
Piper: "GitHub issue #85 (payment processing failure) is currently in 'To Do' status."

You: "Update it with the error logs from production"
Piper: "Updated GitHub issue #85 with production error logs."

You: "Create a follow-up task for the security review"
Piper: "Created security review task #86 linked to payment processing bug #85."

You: "What's the timeline for fixing that issue?"
Piper: "Based on the payment processing bug (#85) complexity, estimated timeline is 3-5 business days."
```

**Memory Analysis:**

- Piper remembers the payment processing issue (#85) throughout the conversation
- "it" and "that issue" automatically resolve to the correct GitHub issue
- Security review task (#86) is linked and remembered
- Timeline estimates consider the full context

#### Example 2: Document Management Memory

```
You: "Upload the new API documentation and user guide"
Piper: "Uploaded API_documentation_v2.1.pdf and User_Guide_v3.0.pdf to the knowledge base."

You: "Search the API documentation for authentication endpoints"
Piper: "Found 5 authentication endpoints in API_documentation_v2.1.pdf..."

You: "Summarize the user guide"
Piper: "Summary of User_Guide_v3.0.pdf: 45 pages covering user onboarding..."

You: "Compare it with the previous version"
Piper: "Comparing User_Guide_v3.0.pdf with User_Guide_v2.5.pdf: 12 new pages added..."
```

**Memory Analysis:**

- Both documents are remembered and can be referenced naturally
- "the API documentation" and "the user guide" resolve correctly
- Version comparison context is maintained
- Search results and summaries are preserved

#### Example 3: Sprint Planning Memory

```
You: "Show me the current sprint backlog"
Piper: "Current sprint backlog contains 12 items: 3 high priority bugs, 5 feature tasks..."

You: "What's the highest priority item?"
Piper: "The highest priority item is bug #89 (user authentication timeout) with 8 story points."

You: "Assign it to the frontend team"
Piper: "Assigned bug #89 (user authentication timeout) to the frontend team."

You: "What about the second priority item?"
Piper: "The second priority item is feature task #92 (dashboard analytics enhancement) with 13 story points."

You: "Update its status to in progress"
Piper: "Updated feature task #92 (dashboard analytics enhancement) status to 'In Progress'."
```

**Memory Analysis:**

- Sprint backlog context is maintained throughout
- Priority ordering is remembered and referenced
- "it" and "its" resolve to the correct items
- Status updates are tracked and preserved

---

## Understanding Context Types

### Conversation Context

Piper maintains complete conversation history including:

- **Turn History**: Every message and response pair
- **Reference Chain**: How entities are referenced over time
- **Topic Evolution**: How conversation topics change and relate
- **Context Switching**: Moving between related topics seamlessly

### Entity Context

Piper tracks specific entities and their states:

- **Issue Tracking**: GitHub issues mentioned and their current status
- **Document References**: Files and documents in conversation
- **Task Management**: Sprint tasks and their progress
- **Project Context**: Current project and team information

### User Context

Piper remembers your preferences and patterns:

- **Personal Preferences**: Your interaction patterns and preferences
- **Team Context**: Your team membership and project access
- **Historical Patterns**: How you typically work and communicate
- **Performance Metrics**: Your interaction efficiency and success rates

---

## Memory Management

### Automatic Context Updates

Piper automatically manages your conversation context:

- **New Turns**: Each interaction is added to the conversation history
- **Entity Tracking**: New entities are identified and stored
- **Reference Resolution**: Anaphoric references are processed in real-time
- **Performance Monitoring**: Response times and accuracy are tracked

### Context Expiration

Piper intelligently manages memory to maintain performance:

- **5-Minute Cache**: Active conversations are cached for quick access
- **10-Turn Limit**: Old turns are automatically removed when exceeded
- **Entity Preservation**: Important entities are maintained beyond the window
- **Graceful Degradation**: System continues working even if cache is unavailable

### Memory Efficiency

Piper optimizes memory usage for the best performance:

- **Compressed Storage**: Conversation data is efficiently stored
- **Lazy Loading**: Context is loaded only when needed
- **Background Processing**: Updates happen without blocking your interaction
- **Memory Monitoring**: System tracks and optimizes memory usage

---

## Best Practices for Effective Memory

### Conversation Design

**Keep Related Topics Together:**

- Group related work in the same conversation
- Start new sessions for completely different topics
- Use clear, specific entity names for better tracking

**Maintain Context Boundaries:**

- Use one conversation per project or sprint
- Separate different types of work (bugs vs features vs documentation)
- Restart conversations when switching major contexts

### Reference Patterns

**Use Consistent References:**

- Use the same reference patterns throughout a conversation
- Be specific when multiple similar entities exist
- Leverage natural language references ("that issue", "the document")

**Optimize for Memory:**

- Mention entities clearly when first introducing them
- Use descriptive names that are easy to reference
- Provide context when switching between related topics

### Performance Optimization

**Session Management:**

- Reuse sessions for related work
- Monitor conversation length and complexity
- Restart sessions when approaching the 10-turn limit

**Context Monitoring:**

- Pay attention to when Piper asks for clarification
- Use specific references when context might be unclear
- Leverage the context window effectively

---

## Troubleshooting Memory Issues

### Common Memory Problems

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

- **Cause**: Complex context processing
- **Solution**: Use simpler references or wait for processing
- **Example**: "Show me the issue" instead of "Show me the first item from the backlog"

### Performance Tips

**Optimal Usage:**

- **Response Time**: <50ms for context retrieval
- **Memory Usage**: <1MB per conversation session
- **Cache Performance**: >95% cache hit ratio for active conversations
- **Context Window**: 10 turns maintained automatically

**When Memory Works Best:**

- ✅ Related topic discussions
- ✅ Multi-step workflows
- ✅ Entity-heavy conversations
- ✅ Context-dependent queries

**When to Start Fresh:**

- ❌ Completely new topics
- ❌ Very long conversations (>10 turns)
- ❌ Complex context switching
- ❌ Performance issues

---

## Advanced Memory Features

### Context Retrieval

You can inspect your current conversation context:

```bash
# Get current conversation context
curl -X GET "http://your-piper-instance/api/v1/conversation/my_session_123/context"
```

**Sample Response:**

```json
{
  "turns": [
    {
      "turn_number": 1,
      "user_message": "Create issue for login bug",
      "assistant_response": "Created issue #85",
      "entities": ["#85", "login bug"],
      "timestamp": "2025-08-09T08:00:00Z"
    }
  ],
  "context_window_size": 10,
  "total_turns": 1
}
```

### Context Settings

Customize your conversation memory:

```json
{
  "context_window": 15, // Increase from default 10
  "cache_ttl": 600, // Cache duration in seconds
  "entity_tracking": true, // Enable entity tracking
  "performance_mode": "balanced" // speed/balanced/high_accuracy
}
```

### Memory Analytics

Track your conversation patterns:

```bash
# Get memory performance metrics
curl -X GET "http://your-piper-instance/api/v1/conversation/my_session_123/analytics"
```

**Metrics Include:**

- Context retrieval performance
- Entity resolution accuracy
- Memory usage patterns
- Cache hit ratios

---

## Integration with Other Features

### Anaphoric Reference Resolution

Memory works seamlessly with reference resolution:

- **Automatic Resolution**: "that issue" resolves using conversation memory
- **Context-Aware**: References consider full conversation history
- **Performance Optimized**: Sub-150ms resolution with memory context
- **Accuracy Enhanced**: 100% accuracy with proper context

### Getting Started Guide

This memory system is the foundation for conversational AI:

- **[Getting Started Guide](./getting-started-conversational-ai.md)** - 15-minute user journey
- **[Understanding Anaphoric References](./understanding-anaphoric-references.md)** - Deep dive into reference resolution

### Performance Validation

Real performance data from PM-034:

- **Context Retrieval**: <50ms for 10-turn window
- **Entity Resolution**: <150ms with memory context
- **Cache Hit Ratio**: >95% for active conversations
- **Memory Usage**: <1MB per conversation session

---

## Success Metrics

### Personal Success Indicators

**You're effectively using conversation memory when:**

- ✅ Context is maintained across 5+ interactions
- ✅ References resolve correctly 90%+ of the time
- ✅ Conversations feel natural and human-like
- ✅ You rarely need to repeat information
- ✅ Context switching works seamlessly

### Team Success Indicators

**Your team is successfully leveraging memory when:**

- ✅ 80%+ of conversations maintain context effectively
- ✅ Reference resolution accuracy >90%
- ✅ Average conversation length 5-8 turns
- ✅ Context loss incidents <10%
- ✅ User satisfaction scores improve

### Performance Benchmarks

**Target Performance:**

- **Context Retrieval**: <50ms average
- **Entity Resolution**: <150ms with memory
- **Cache Hit Ratio**: >95% for active sessions
- **Memory Usage**: <1MB per conversation
- **User Satisfaction**: >4.5/5 rating

**Current Performance (PM-034):**

- **Context Retrieval**: 25ms average ✅
- **Entity Resolution**: 2.33ms with memory ✅
- **Cache Hit Ratio**: >95% achieved ✅
- **Memory Usage**: <1MB per session ✅
- **User Satisfaction**: TBD (new feature)

---

## Next Steps

- [Getting Started with Conversational AI](./getting-started-conversational-ai.md)
- [Understanding Anaphoric References](./understanding-anaphoric-references.md)
- [Upgrading from Command Mode](./upgrading-from-command-mode.md)
- [Conversation Examples](./conversation-scenario-examples.md)
- [Report an Issue](https://github.com/your-repo/issues)

---

**Ready to experience the magic?** Start a conversation and discover how Piper's memory makes your interactions feel natural, efficient, and human-like!
