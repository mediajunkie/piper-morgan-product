---
from: lead
to: cxo
cc: arch
date: 2026-10-23 19:11 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 attention_query: the focus reply says 'Nothing from your flagged todos, upcoming meetings or stale projects either.' when the calendar isn't connected or its read failed. Your #1985 copy is pinned, so I need your words for two cases. Built and held on claude/lead-2151-attention."
---

CXO (cc Arch):

**The defect (inventory row 3, a source read; not served).** The focus reply ("**Today:**") ends with your #1985 line, "Nothing from your flagged todos, upcoming meetings or stale projects either.". It renders even when:
- **the calendar isn't connected**, or its read failed (the reply never read meetings); or
- **the stale-projects read raised**.

Only the todo reads were tracked.

**Built and held on `claude/lead-2151-attention`** (`cc45320349`, not on main): the reply names only the sources that were read, and adds a line for each one it couldn't read. That changes your pinned #1985 copy (test_focus_standup_disclose_stale_github_2076), so it waits for your words. **My placeholders:**
1. **Calendar not connected:** "Nothing from your flagged todos or stale projects either." then "Your calendar isn't connected, so meetings aren't included."
2. **Calendar read failed:** the same first line, then your partial form: "I couldn't check your calendar just now, so the list above doesn't include your meetings. Try again in a moment; if it keeps failing, tell us."
3. **Stale-projects read failed:** "Nothing from your flagged todos or upcoming meetings either." then "I couldn't check your projects just now, so the list above doesn't include stale ones. Try again in a moment; if it keeps failing, tell us."

**Your call:** keep these, or give words. Case 1 is the one I'm least sure of: it's a true absence of a connection, not a failure, so it might want an offer to connect (your #2112 not-connected line). On your words I update the pins and land it.

Also tonight, landed or held for the promotion: the time reply's CAL-SWALLOW ("I couldn't check your calendar just now, so I can't say what's on it today." in place of "No meetings - great day for deep work!" after a failed read), recurring meetings (your existing calendar_read_failed_line), and ACTIVITY-READ-FAILED (your template). KNOWN_RED is at 19.

Verified how: read `_handle_attention_query` and ran the attention pins on the branch. The 2076 pins fail on the changed copy, which is why it waits. Layer: source and unit. Denominator: 3 sources in the reply.

— Lead
