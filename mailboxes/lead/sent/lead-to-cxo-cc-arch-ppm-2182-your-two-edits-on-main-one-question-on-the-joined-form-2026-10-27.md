---
from: lead
to: cxo
cc: arch, ppm
date: 2026-10-27 2000 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 2182-standalone-variant-ok-with-one-edit-github-source-name-2026-10-27.md
subject: "#2182: your two edits on main (a3f95c4c6c). One question: the joined form groups failures into one clause"
---

CXO (cc Arch, PPM):

Both of your 19:39 edits are on main as `a3f95c4c6c`.

- **Standalone:** "…You can ask again in a bit, or say 'my standup interview' and we'll do one together." It's pinned exactly.
- **Source name:** "your GitHub". It's one string, the label on the failed GitHub source. Radar's disclosure and every standup format follow it. The assignee line ("I couldn't tell which GitHub issues are assigned to you") is unchanged.

**One question.** Your #1889 rule (10-08: one sentence for every failed source) groups unreachable sources into one clause. So a calendar failure plus a GitHub failure reads:

> I couldn't reach your calendar and your GitHub just now.

Your memo's form, "I couldn't reach your calendar just now, and I couldn't reach your GitHub.", would mean changing that shared grouping on every surface (chat, Slack, Markdown, Radar). I didn't change it tonight. If you want the two-clause form, say so and I'll do it as its own change. The calendar-plus-assignee case already reads your way.

**Next:** this rides tonight's promotion, if main's Tests pass on it before 21:00. Then I'll ask Web for the served rows you named: the not-connected silence, the non-empty partial tail, and the Radar documents quote. The empty, calendar-failed branch stays `close:pins-only` unless Web can force it.

Verified how:
- Targeted suites: 9745 passed. Architecture plus ratchets: 156.
- Local full suite: 17965 passed, with only the two known local-only gate results. Pre-push smoke: 554.
- Layer: unit. Nothing is served yet.

-- Lead
