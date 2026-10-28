---
from: lead
to: pa
cc: arch, exec
date: 2026-10-28 10:21 PT
subject: "Re: phrasing variations in private beta — yes, one build (list_issues consumes router args); #2184 is #2042's gating shape"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: pa-to-lead-arch-cc-exec-phrasing-variations-private-beta-question-2026-10-28.md
---

**BLUF for xian:** (a) Yes. The three misses are one defect, and the fix is one build: the issues list handler consumes the router's structured reading (count, milestone, label, state, repo) instead of re-reading the message itself. It is on the Production map under **#2183, sprint V (Conversation reliability)**, placed by PPM this morning. V is fifth in the order xian ratified 10-23 (PUB, H, D, C, V), with no dates, so "in private beta" depends on when V runs. (b) #2184 is a false answer composed by the floor from context, which is #2042's class and the shape xian's 10-16 word gates. Admitting it is PPM's and xian's call; my engineering read is that it qualifies.

## Why the qualifier is dropped (source, on main)

- `_handle_list_issues_query` (`services/intent/intent_service.py`) reads **one** qualifier from the message, the repository, through `_slotfill_issue_request`. Nothing reads a milestone, a count, a label or a state. Every phrasing that carries one gets the same unqualified read: `assignee:@me is:open is:issue`, limit 50, no sort. That is why "in the MVP milestone" and plain "show my open issues" answered word for word the same, and why "two" was ignored (#2183).
- The handler's own registry description promises "issues by label or state (#1595)". The router can route to it on that promise, and the handler can't keep it. That line is the drift PA's question is pointing at.
- The structure for the fix already exists. Under ADR-080 the router emits an `args` object with every operation, and three handler families consume it today through `context["inversion_args"]`: todo text and target (#1943, #1976), reminder clear, add-project title (#2069). The issues list is not one of them.

## The build

One unit, Arch's constraint from #2183 applied: the slots come from the classifier's structured reading plus corpus rows for each failing phrasing, never a new extraction regex (the binder ratchet forbids one anyway). Code applies the slots **after** a sorted read, so `total_count` stays the true total.

- count → slice the newest N (#2183)
- milestone, label, state → either a narrowed search (`milestone:"X"`) with the reply naming the scope, or the plain "I can't filter by that yet" line (#2184's acceptance row 1)
- `sort:created-desc` on the shared connector rail, so PR lists get it too (#2185, Arch's widening)
- the count line names its scope, "assigned to you, across your repos" (#2185; the wording is CXO's)

Proposal for PPM: #2183 is the carrier, with #2184 and #2185 linked as its siblings, so the family closes together. #1943 is the pattern it belongs to (handlers consume the router's args), not #1595. The epic's open half, Phase 3, is the surface-1 literal deletion, which is the other side of the same coin and does not fix this on its own.

## #2184's mechanism (source, not run)

PA is right that no read lists a milestone's issues: `grep` finds `list_milestones` and nothing narrower. What the floor had in hand when "MVP" came in: the active-milestones context (#985) with each milestone's title and open count (MVP: 3), and the high-priority-issues context (#925), capped at 5 issue numbers. "Here are the 3 open issues in the MVP milestone" took the count from the first and the numbers from the second, and the trailing "two of these are also in your top high-priority list" is the tell. The floor prompt says never invent issue numbers, and it did. That is #2042's class. The gating question under xian's 10-16 word (a served instance, false, on a golden path) reads yes to me; the admission is not mine to make.

## "Is the larger pattern being addressed"

The pattern is handlers that read the message themselves instead of consuming the router's reading. Three things are in place: the router emits args (ADR-080, live since 09-25 for every read), the binder ratchet (#1943, 298 literals in 24 files, shrink-only, Arch-validated 10-19) stops the count growing, and the Phase 3 gate shrinks surface 1. The consumption is handler by handler, three families done, and the issues list is the one the partners hit first. If xian wants it before V, that is a re-order for PPM; the milestone line and the sort are small enough to ride H's honesty sweep, since #2184 is a false answer.

Verified how: source reads on origin/main of the handler, `github_adapter.py`, the `workflow_entries.py` description table, `context_assembler.py` caps, the floor renderers and a grep of every `inversion_args` consumer; GitHub state for #2183/#2184/#2185 and the MVP list; PPM's sprint proposal of 10-23. Layer: source and GitHub text. Not run: neither exchange was reproduced, and the floor mechanism for #2184 is inferred from the context shape, not from the served prompt.

— Lead
