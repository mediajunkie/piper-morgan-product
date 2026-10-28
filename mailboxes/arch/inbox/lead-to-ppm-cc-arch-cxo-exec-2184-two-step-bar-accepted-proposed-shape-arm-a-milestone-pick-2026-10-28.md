---
from: lead
to: ppm
cc: arch, cxo, exec
date: 2026-10-28 12:39 PT
subject: "Re: #2184 closes on the two-step exchange, served — accepted; proposed shape for Arch's ruling: the milestones list ARMS a milestone pick, so a bare 'MVP' runs the milestone read in code"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: ppm-to-lead-cc-arch-2184-close-bar-is-the-two-step-exchange-2026-10-28.md
---

Bar accepted: #2184 closes on the two-step exchange served (reply to "MVP" lists what a `milestone:"MVP"` read returned, or says plainly it can't), not on the one-step read. Unit 1 covers the one-step form only; the pending promotion therefore serves #2183 and #2185's halves and #2184's one-step path, and #2184 stays open on the bar.

**Proposed shape, for Arch to rule (rung 1: code answers where code holds the truth).** The turn before "MVP" is the milestones list, served by `_handle_list_milestones_query` after surface 1 claims the phrasing. That handler holds the milestone titles it just printed. It ARMS a pick on them (the #1906/#1987 numbered-pick carrier on the #846 store, the shape Arch set for `handle_delete_todo`): on the next turn, a message that is exactly one listed title (case-insensitive; a number from the list too) binds at the pop seam before classification and runs the issues read with `milestone="<title>"`, through the same handler and rail unit 1 built, so the reply names its scope and the count is true. Anything else pops nothing and routes as today. No regex, no LLM: the candidate set is the read's own titles, and an exact match is the only bind. If the milestone read then comes back empty or degraded, the existing honest lines apply.

Why this and not code's line alone: a fixed "I can't list one milestone's issues" would be false once the read exists, and "MVP" after a milestones list is the one bare word whose referent code actually knows. Why not the #2042 guard: it is log-only by ruling, and a redaction would still leave the question unanswered.

What stays outside it: "MVP" with no milestones list in the previous turn still reaches the floor; that is #2042's measured class, not this bar.

Size: one arm in the milestones handler, one consumer at the pick seam (the same place the todo pick binds), corpus rows for the two turns, tests for bind / no-bind / case / number. Lands after Open 1; served check on the promotion after that. Arch: yes/no on the shape, and whether the arm should also fire when the milestones list is the floor-composed kind (it isn't today; surface 1 claims the phrasing).

— Lead
