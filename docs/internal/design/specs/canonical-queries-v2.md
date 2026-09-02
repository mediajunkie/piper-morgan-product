# Canonical Queries v2.2

> **Not a duplicate of `docs/internal/architecture/current/canonical-queries.md`** (confirmed
> 2026-09-02, Docs, #1585). **This file** is the versioned implementation-tracking spec (query
> counts, changelog, per-query implementation status). **The other file** is a plain reference
> list of example query phrasings by category. Both are legitimate; neither supersedes the other.

**Version**: 2.2
**Date**: December 27, 2025
**Total Queries**: 62
**Status**: 35/62 implemented (56%)

## Change Log
- v2.4: Implemented Slack Slash Commands (#49, #50) - Issue #520
- v2.3: Implemented Phase B-4 Document Update (#40) - Issue #522
- v2.3: Fixed missing checkmarks for Issue #519 queries (#45, #59, #60)
- v2.2: Implemented Phase B-3 Contextual Intelligence (#29, #30) - Issue #521
- v2.1: Implemented 8 Phase A Quick Wins (#34, #35, #41, #42, #51, #56, #57, #61)
- v2.1: Removed Query #39 (duplicate of #20 - document search)
- v2.0: Removed Query #15 (lifecycle - too abstract)
- v2.0: Added 39 new queries (#26-63) from alpha testing insights
- v2.0: Reclassified Predictive queries as Beta-capable
- v2.0: Added integration-specific categories

---

## Identity Queries (COMPLETE: 5/5)

### 1. What's your name and role? ✅
- What's your name?
- Who are you?
- What do you do?
- Tell me about yourself

### 2. What can you help me with? ✅
- What can you do?
- How can you help me?
- What are your capabilities?
- Show me what you can do

### 3. Are you working properly? ✅
- Are you working?
- Is everything working?
- What's your status?
- Are you online?

### 4. How do I get help? ✅
- I need help
- How do I use you?
- Can you help me?
- What should I ask you?

### 5. What makes you different? ✅
- What's special about you?
- Why should I use you?
- What's your unique value?
- How are you different from other tools?

---

## Temporal Queries (COMPLETE: 5/5)

### 6. What day is it? ✅
- What's today's date?
- What day of the week is it?
- What's the current date?
- Tell me the date

### 7. What did we accomplish yesterday? ✅
- What did we do yesterday?
- What happened yesterday?
- Show me yesterday's work
- What was completed yesterday?

### 8. What's on the agenda for today? ✅
- What should I work on today?
- What's my schedule today?
- What's planned for today?
- Show me today's tasks

### 9. When was the last time we worked on this? ✅
- When did we last work on this?
- How long ago was this updated?
- What's the last activity on this?
- When was this last modified?

### 10. How long have we been working on this project? ✅
- How long has this project been active?
- When did we start this project?
- What's the project timeline?
- How old is this project?

### ~~15. Where are we in the project lifecycle?~~ [REMOVED]
- *Removed: Too abstract, assumes workflow tracking not implemented*

---

## Spatial Queries (80%: 4/5)

### 11. What projects are we working on? ✅
- Show me all projects
- List our projects
- What projects do we have?
- Give me a project overview

### 12. Show me the project landscape ✅
- What's our project portfolio?
- Give me a project overview
- Show me all our work
- What's our project status?

### 13. Which project should I focus on? ✅
- What's the most important project?
- Which project needs attention?
- What should I prioritize?
- Which project is urgent?

### 14. What's the status of project X? ✅
- How is project X doing?
- What's happening with project X?
- Give me an update on project X
- What's the progress on project X?

---

## Capability Queries (COMPLETE: 5/5)

### 16. Create a GitHub issue about X ✅
- Make a GitHub issue for X
- Open a GitHub issue about X
- File a GitHub issue for X
- Create a ticket for X

### 17. Analyze this document ✅
- What's in this document?
- Summarize this document
- Review this document
- Tell me about this document

### 18. List all my projects ✅
- Show me my projects
- What projects do I have?
- Give me a project list
- Show all projects

### 19. Generate a status report ✅
- Create a status report
- Give me a status update
- Show me the current status
- What's our status?

### 20. Search for X in our documents ✅
- Find documents about X
- Search our files for X
- Look for X in our docs
- Find information about X

---

## Predictive Queries [BETA] (20%: 1/5)

### 21. What should I focus on today? ⚠️ PARTIAL
- What's my priority today?
- What should I work on?
- What's most important today?
- What needs my attention?
- **Status**: Time-based only, needs calendar integration

### 22. What patterns do you see? ❌
- What trends are you noticing?
- What patterns have you observed?
- What insights do you have?
- What are you seeing?
- **Beta Target**: Basic pattern reporting from LearnedPattern table

### 23. What risks should I be aware of? ❌
- What should I worry about?
- What risks do you see?
- What could go wrong?
- What should I watch out for?
- **Beta Target**: Stale projects, missed deadlines

### 24. What opportunities should I pursue? ❌
- What should I explore?
- What opportunities do you see?
- What should I look into?
- What's worth pursuing?
- **Beta Target**: Unused integrations, underutilized features

### 25. What's the next milestone? ❌
- What's coming up next?
- What's the next deadline?
- What should I prepare for?
- What's on the horizon?
- **Beta Target**: GitHub + Calendar milestone extraction

---

## Conversational Queries (NEW) (2/5)

### 26. What else can you help with? ❌
- What other capabilities do you have?
- Show me more options
- What else can we do?
- **Purpose**: Contextual capability discovery

### 27. Tell me more about X feature ❌
- Explain how X works
- How does X help me?
- What is X for?
- **Purpose**: Feature deep-dive

### 28. How do I use X? ❌
- Show me how to X
- Guide me through X
- Help me with X
- **Purpose**: Feature guidance

### 29. What changed since X? ✅
- What's new since yesterday?
- Show me recent updates
- What changed this week?
- **Purpose**: Diff view of changes

### 30. What needs my attention? ✅
- What's urgent?
- Show me what's on fire
- Any blockers?
- **Purpose**: Notification aggregation

---

## Scheduling & Reminders (NEW) (0/5)

### 31. Schedule a meeting about X ❌
- Book time to discuss X
- Set up a meeting for X
- Schedule X for tomorrow
- **Integration**: Google Calendar

### 32. Remind me to X ❌
- Set a reminder for X
- Don't let me forget X
- Alert me about X
- **Integration**: Calendar + Notifications

### 33. Find time for X with Y ❌
- When can we meet?
- Find a slot for X
- Schedule time with Y
- **Purpose**: Calendar deconfliction

### 34. How much time in meetings? ✅
- Meeting time this week
- Am I overscheduled?
- Calendar analysis
- **Purpose**: Time audit

### 35. Review my recurring meetings ✅
- Audit my standing meetings
- Which meetings can I drop?
- Meeting efficiency check
- **Purpose**: Calendar optimization

---

## Document Management (NEW) (1/4)

### 36. Create a doc from this conversation ❌
- Save this as a document
- Turn this into notes
- Document this discussion
- **Output**: Notion/Markdown

### 37. Compare these documents ❌
- What's different between X and Y?
- Compare versions
- Show me the changes
- **Purpose**: Document diff

### 38. Synthesize these sources ❌
- Combine these documents
- Merge these notes
- Create summary from sources
- **Purpose**: Multi-doc synthesis

### ~~39. Find docs about X~~ [REMOVED - duplicate of #20]

### 40. Update the X document ✅
- Edit X document
- Add this to X doc
- Update X with new info
- **Integration**: Notion update

---

## GitHub Operations (NEW) (5/8)

### 41. What did we ship this week? ✅
- Show closed PRs
- What got merged?
- Weekly GitHub summary
- **Purpose**: Release tracking

### 42. Show me stale PRs ✅
- Old pull requests
- PRs needing review
- Stuck PRs
- **Purpose**: PR hygiene

### 43. What's blocking the milestone? ❌
- Milestone blockers
- What's holding us up?
- Impediments to release
- **Purpose**: Blocker identification

### 44. Create issues from this meeting ❌
- Turn action items into issues
- File these as GitHub issues
- Create tickets from notes
- **Purpose**: Meeting→Issues

### 45. Close completed issues ✅
- Clean up done issues
- Close finished tickets
- Archive completed work
- **Purpose**: Issue hygiene

### 58. Update issue #X ❌
- Edit issue #X
- Change issue description
- Modify ticket #X
- **Purpose**: Issue mutation

### 59. Comment on issue #X ✅
- Add comment to #X
- Reply to issue #X
- Update issue thread
- **Purpose**: Issue discussion

### 60. Review issue #X ✅
- Show me issue #X
- What's in ticket #X?
- Issue #X details
- **Purpose**: Issue inspection

---

## Slack Communication (NEW) (2/5)

### 46. Any mentions I missed? ❌
- Unread mentions
- Who mentioned me?
- Catch me up on mentions
- **Purpose**: Mention tracking

### 47. Summarize #channel from yesterday ❌
- Channel summary
- What happened in #general?
- Catch up on #channel
- **Purpose**: Channel digests

### 48. Post this update to the team ❌
- Share with team
- Post to Slack
- Send team update
- **Purpose**: Broadcast messages

### 49. /standup ✅
- Slack slash command
- Generate standup in Slack
- **Purpose**: Native Slack command

### 50. /piper help ✅
- Slack help command
- Show Slack commands
- **Purpose**: Slack discovery

---

## Productivity Tracking (NEW) (1/3)

### 51. What's my productivity this week? ✅
- How productive was I?
- Weekly metrics
- My accomplishments
- **Purpose**: Personal metrics

### 52. Are we on track? ❌
- Milestone progress
- Project health check
- On schedule check
- **Purpose**: Goal tracking

### 53. What did the team accomplish? ❌
- Team summary
- Group accomplishments
- Collective progress
- **Purpose**: Team metrics

---

## Todo Management (NEW) (2/4)

### 54. Add a todo ❌
- Create task
- Add to my list
- New todo: X
- **Purpose**: Todo creation

### 55. Complete todo ❌
- Mark X as done
- Complete task X
- Check off X
- **Purpose**: Todo completion

### 56. Show my todos ✅
- List my tasks
- What are my todos?
- Show task list
- **Purpose**: Todo listing

### 57. What's my next todo? ✅
- Next task
- What should I do next?
- Priority task
- **Purpose**: Todo prioritization

---

## Calendar Extended (NEW) (1/2)

### 61. What's my week look like? ✅
- Week ahead view
- Weekly calendar
- This week's schedule
- **Purpose**: Week planning

### 62. Check calendar for conflicts ❌
- Calendar conflicts
- Double-booked?
- Schedule problems
- **Purpose**: Conflict detection

---

## Knowledge Operations (NEW) (0/1)

### 63. Upload a file ❌
- Add to knowledge base
- Import document
- Store this file
- **Purpose**: Knowledge ingestion

---

## Summary by Implementation Status

### Complete Categories
- **Identity**: 5/5 (100%) ✅
- **Temporal**: 5/5 (100%) ✅
- **Capability**: 5/5 (100%) ✅

### In Progress Categories
- **Spatial**: 4/5 (80%)
- **Predictive**: 1/5 (20%) - PARTIAL implementation
- **Scheduling**: 2/5 (40%) - #34, #35 implemented
- **GitHub Ops**: 5/8 (63%) - #41, #42, #45, #59, #60 implemented
- **Productivity**: 1/3 (33%) - #51 implemented
- **Todos**: 2/4 (50%) - #56, #57 implemented
- **Calendar Extended**: 1/2 (50%) - #61 implemented

### In Progress Categories (continued)
- **Conversational**: 2/5 (40%) - #29, #30 implemented
- **Slack**: 2/5 (40%) - #49, #50 implemented

### Not Started Categories (22 queries)
- **Conversational**: 3 remaining (#26, #27, #28)
- **Scheduling**: 3 remaining (#31, #32, #33)
- **Documents**: 3 remaining (#36, #37, #38) - #40 implemented, #39 removed
- **GitHub Ops**: 3 remaining (#43, #44, #58)
- **Slack**: 3 remaining (#46, #47, #48)
- **Productivity**: 2 remaining (#52, #53)
- **Todos**: 2 remaining (#54, #55)
- **Calendar Extended**: 1 remaining (#62)
- **Knowledge**: 0/1

### Overall Progress
- **Implemented**: 35/62 (56%)
- **Partial**: 1/62 (2%)
- **Not Implemented**: 26/62 (42%)

---

## Release Targets

### Alpha (Current)
Focus on core implemented queries (19) for testing and refinement.

### Beta (v0.9)
- Complete Predictive category with heuristic implementations
- Add Todo Management (fundamental CRUD)
- Add core GitHub operations
- Target: 40/62 queries (65%)

### v1.0 (Production)
- All integration queries functional
- Conversational glue implemented
- Document management operational
- Target: 54/62 queries (87%)

### v1.1 (Enhancement)
- ML-enhanced predictive analytics
- Advanced document synthesis
- Team collaboration features
- Target: 62/62 queries (100%)

---

*Note: This list represents the comprehensive jobs-to-be-done identified through alpha testing, design sessions, and user feedback. Not all queries need to be implemented for MVP, but all represent real user needs.*
