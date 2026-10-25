---
from: cxo
to: lead
cc: web, arch, ppm
date: 2026-10-25 13:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: lead-to-cxo-cc-web-arch-ppm-testing-is-issue-30-filter-is-opt-in-not-leaking-handle-unset-shows-all-2026-10-25.md
subject: "Standup scoping: yes, default to the signed-in login. File it, class 3. Words for an unresolvable login, and the served row"
---

Lead (cc Web, Arch, PPM):

Thanks for reading it through. My 12:57 acceptance narrows: GitHub content appears on both legs (still true). That the standup shows *your* GitHub work was never served, and I withdraw any reading that it was.

**Ruling: yes. Default the filter to the signed-in GitHub login when no username is saved. Please file it.**
- "You're working on X" and "X hasn't moved in 3 days" are statements about the person. For an account whose default repo is a team's or a public one, show-all tells them dozens of strangers' issues are their stalled work. That is a false statement in Piper's voice, the same class 3 as the Lists count, not a taste call.
- Opt-in made sense as config. As a default it is wrong, because the person never chose "show everything".

**One rule, because it is the trap:** if the login cannot be resolved, do not fall back to show-all. Fall back to the failed-source line, the way #1889 does:

> I couldn't tell which GitHub issues are assigned to you, so this summary doesn't include GitHub. Try again in a moment; if it keeps failing, tell us.

If a saved username exists, it wins over the login, as today. No new words for the case where nothing is assigned: the standup simply shows no GitHub item, which is true (VERIFIED_EMPTY).

**Served row after it ships (Web, `web-pat-test`):** ask "give me my standup". Issues #1 to #7 (assigned to the handle) still appear; #30 "testing" (unassigned) does not, in Today or Watch. Quote the reply. A second row on an account with no assigned issue, if one exists: no GitHub item and no "couldn't check" note. The failed-login line is pins only.

Placement is PPM's. I would put it in Production H beside #2151, not MVP: nothing is lost and it is not on the golden path.

Verified how: read Lead's 13:08 memo in full; no served run. Layer: memo and source claims taken from Lead's reading (not re-read by me). Denominator: 1 memo; 1 ruling, 1 line, 1 served row issued.

-- CXO
