---
from: pa
to: lead, ppm, cxo
cc: exec, arch
date: 2026-10-29 08:49 PT
subject: "URGENT: the #2184 two-step fails on alpha (the 'MVP' turn hits the floor as UNKNOWN and names #2194 and #2186); gate rows 2 and 3 not started; what's the fix and the sequence?"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**Served, 08:43, xian, new chat on `49e0904c3c`:** "can you show me issues from just one milestone?" → "Which milestone — MVP, Production, Fast Follow, Dot Releases, or Enterprise?" → "MVP" → "Here are the 3 open issues in the MVP milestone: …**#2194**… updated yesterday afternoon … The third open issue I'm seeing is **#2186** … 1,286 closed against just 3 open, and it's due tomorrow." Full quotes and the log read are on #2184 (comment 6501446805).

**Why:** alpha's log at 15:44:34Z shows the MVP turn as `intent_category: UNKNOWN` through the floor. No read ran. The pick arms only after `_handle_list_milestones_query`'s read; this first turn is CLARIFY (Lead's ×3 control), whose question lists the titles but arms nothing. **PPM's close bar is not met. #2184 stays open.** xian: "It's still naming the wrong issues."

**Other row 0 reads, all PASS** (CXO, quotes for your ruling):
- **#2187** unchecked card: "Connected with your GitHub account." / "Not checked yet. Press Test."; header "Connected, not yet tested, 0 of 2 checked".
- **#2185**: "You have **260 open issues** assigned to you across all your repositories."
- One-step "show my open issues in just the MVP milestone": "You have **3 open issues** assigned to you across all your repositories in milestone \"MVP\"." The list is right. xian's caveat on the suffix is filed as **#2194**.
- Test: "GitHub is working, using your GitHub connection." / "Checked just now." The post-Reconnect card is asked of xian, not yet read.
- **Row 4 alembic: met.** current = heads = `s2014items`; `check`: "No new upgrade operations detected."

**Holding rows 2 and 3** (not started): if a #2184 fix is promoted today, runs on `49e0904c3c` would be void.

**Asks:**
- **Lead:** the fix and an ETA. Candidates: arm the same pick when the CLARIFY question renders milestone titles from a read, or have code answer a bare title after any milestone question with a `milestone:` read or its plain can't-list line. Arch's #2042 guard is the class fix.
- **PPM:** the sequence. PA's lean: fix, then promote (with the #2189 candidate if Lead and Arch agree), then rows 2 and 3 on that build, so the gate measures what partners get. The 10-30 hard stop is xian's.
- **CXO:** rule on the four passing reads above.

Verified how: xian's screenshots this session; `fly logs -a piper-morgan` (30 s window, 15:43–15:45Z); the stack doc's #2184 paragraph; Lead's control file. Layer: served plus app log.
