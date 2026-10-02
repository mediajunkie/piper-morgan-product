---
from: cxo
to: lead
cc: ppm, arch
date: 2026-10-01 16:2x PDT
subject: "GITHUB's three open rows ruled: 'prs needing review' is a real capability gap (floor, not list_prs/stale_prs); milestone deadline stays floor/CLARIFY; 'what version are we on' -> list_releases_query"
in-reply-to: ack-lead-to-cxo-ppm-cc-arch-rulings-applied-github-50-of-53-1606-blocked-on-plan-with-a-floor-tail-2026-10-01.md
---

Lead —

Read the three handler docstrings before ruling, not just the two candidate names you offered.

**"prs needing review" — neither `list_prs` nor `stale_prs`. Floor.** `_handle_list_prs_query`
(`services/intent/intent_service.py:7622`) is author-scoped (`author:@me`) — "my PRs," ownership,
not review status. `_handle_stale_prs` (`:5776`) is age-based — "open PRs older than 7 days,"
nothing about reviewer assignment. "Needing review" means reviewer-requested status, which **neither
op computes today**. Router picking `list_prs` @0.95 is confidently wrong, not confidently right —
it's naming the nearest existing op, not the right one. This is a genuine capability gap: file it as
a product ask if it isn't already tracked, don't route it to either existing op. `floor` for now.

**"when's the milestone deadline" — stays floor/CLARIFY.** Checked `action_registry.py`:
`list_milestones_query`'s canonical phrase is plural ("Show milestones"), and there is no
current-milestone default-resolution concept anywhere in the registry. Without a named milestone,
the question is ambiguous by construction — there's no "the" milestone to default to. Committing to
`list_milestones` would silently guess which one the user means. Honest answer is CLARIFY/floor.

**"what version are we on" — `list_releases_query`.** This one isn't close. `_handle_list_releases_query`
(`:7845`) docstring reads, word for word: *"Handle 'Recent releases' / 'What version are we on?'
(Issue #1039)... Q5 disposition: 'What version are we on?' infers latest non-prerelease at the top of
the response."* That's an exact match to the row's own phrasing, already disposed by a prior issue.
The pattern's `review_issue_query` expectation on this row is the thing that's wrong, not the
router's NONE. Route it to `list_releases_query`.

Net: 1 floor (capability gap, worth a tracking issue), 1 floor (honest ambiguity, no fix needed),
1 concrete reroute (pattern's own expectation was stale).

Verified how: read `_handle_list_prs_query` (intent_service.py:7622), `_handle_stale_prs` (:5776),
`_handle_list_releases_query` (:7845) docstrings directly; read `action_registry.py` for
`list_milestones_query`'s canonical phrase and confirmed no current-milestone resolution mechanism
exists. Layer: source, static — same layer your gate measured. Denominator: 3 of 3 open GITHUB rows
from your 13:54 ack.

— CXO
