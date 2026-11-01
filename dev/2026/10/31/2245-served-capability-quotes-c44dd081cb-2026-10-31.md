# #2245 served: the two capability quotes on c44dd081cb (2026-10-31 21:26 PT)

Account web-seed-1386 on alpha, by API (`/api/v1/intent`), a fresh session for each ask. Alpha and beta both served 0.9.0.0 at `c44dd081cb` (`/health` at 21:25). `git merge-base --is-ancestor 5df1db03fa c44dd081cb`: carries the fix. `scripts/check-release-parity.sh c44dd081cb`: PARITY OK.

```
=== #2245 served quotes on c44dd081cb as web-seed-1386 ===

## #2245 capability list, session caec8699

--- C1 [21:26:02, 11.7s, http 200] ---
USER: What can you help me with?
route: DISCOVERY/get_capabilities
PIPER: What I can do today:
- conversational PM guidance
- strategic thinking and prioritization frameworks
- you can ask me: "give me my standup"
- you can ask me: "what have you learned about my work style?"
- you can ask me: "connect my github"
- you can ask me: "what time is it?"
- you can ask me: "link my google calendar"
- you can ask me: "add a repo to my portfolio"
- you can ask me: "show me my todos"
- you can ask me: "list my projects"
- you can ask me: "connect my calendar"
- you can ask me: "what reminders do I have?"

Connected, and what I read from each:
- GitHub: chat reads open issues and their status, one issue by number
- Google Calendar: I can read your calendar for today, tomorrow or this week, including your free time. I can't check for conflicts or find a time that works for other people yet.

## #2245 connect list, session 8a457883

--- C2 [21:26:11, 7.4s, http 200] ---
USER: what can you connect to?
route: DISCOVERY/get_capabilities
PIPER: What I can do today:
- conversational PM guidance
- strategic thinking and prioritization frameworks
- you can ask me: "give me my standup"
- you can ask me: "what have you learned about my work style?"
- you can ask me: "connect my github"
- you can ask me: "what time is it?"
- you can ask me: "link my google calendar"
- you can ask me: "add a repo to my portfolio"
- you can ask me: "show me my todos"
- you can ask me: "list my projects"
- you can ask me: "connect my calendar"
- you can ask me: "what reminders do I have?"

Connected, and what I read from each:
- GitHub: chat reads open issues and their status, one issue by number
- Google Calendar: I can read your calendar for today, tomorrow or this week, including your free time. I can't check for conflicts or find a time that works for other people yet.
```
