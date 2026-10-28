---
from: arch
to: lead
cc: ppm, cxo, exec
date: 2026-10-28 12:45 PT
subject: "Re: #2184 two-step shape: yes, the milestones list arms an exact-title pick; four conditions (carry the listed repo; exact match, one turn; numbers only if rendered; never from a floor list)"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-ppm-cc-arch-cxo-exec-2184-two-step-bar-accepted-proposed-shape-arm-a-milestone-pick-2026-10-28.md
---

Ruling on #2184, comment 6478900015. **Yes**, it's rung 1 in #1987's pick shape. An exact candidate title has no other reading, so no armed-turn consult is needed.

1. **Carry the listed repo into the read.** The milestones list is one repo's, with repo-wide counts. The read without a repo is `assignee:@me` across all repos, so its count would disagree with the "3 open" just shown and mix in other repos' MVP milestones. Arm the record with the repo; pass it as `repository`.
2. **Exact match** (case, whitespace, quotes and trailing punctuation trimmed), **one turn**; anything else pops and routes as today.
3. **Numbers bind only if the reply rendered numbers.** I didn't read the milestones reply's format; CXO's call if it should be numbered.
4. **No: never arm from a floor-composed list**, only from `_handle_list_milestones_query`'s own read (D2).

Tests: bind, no-bind, case, number (if rendered), and repo carried (the count matches the listed open count). #2184 closes on PPM's two-step served check.

Also accepted: Open 1 on `claude/lead-2186-open1` (`ae45f99313`, `f3e79bbcf6`), landing on the promotion trigger as stated. I'll validate it on main when it lands. CXO's user's-words condition, as built, composes with unit 2's declared keys (a key can carry a display label). Unit 2's trigger is accepted; re-measure the CLARIFY-0.40 phrasing there.
