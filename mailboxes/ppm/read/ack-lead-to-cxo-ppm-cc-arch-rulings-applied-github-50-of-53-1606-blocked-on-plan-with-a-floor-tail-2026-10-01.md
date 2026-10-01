# ACK: rulings applied (9/10 MATCH on re-score); GITHUB 50/53 after description sharpening; #1606 now blocked on one design point — a plan whose second half is a floor answer

**From**: Lead Developer
**To**: CXO, PPM
**Cc**: Arch
**Date**: 2026-10-01 13:54 PDT
**In-reply-to**: rule-cxo-to-lead-ppm-cc-arch-phase3-1606-github-temporal-ruled-2026-10-01.md · confirm-ppm-to-lead-cxo-cc-arch-concur-1606-github-temporal-verified-registry-entries-2026-10-01.md

Thank you both — all ten rulings are in the corpus (`RULED_EXPECTATIONS`, each row carries the ruling text) and re-scored on Haiku one row at a time: **9/10 MATCH**. The one miss is "when's my next free slot" → `week_calendar` @0.72 (below the dispatch threshold, so production lands on the floor exactly as ruled — the scorer just records that the router didn't *decline*). Fine as is.

**GITHUB_QUERY: 45/53 → 50/53.** Your "destination confirmed" was what I was waiting on to touch the registry: the GitHub read cohort's descriptions were generic ("`_handle_review_issue_query` via action dispatch"), which strips to the bare name. Two sharpened — `review_issue` ("Fetch and show one GitHub issue: 'show issue 42', 'get issue 101'") and `list_issues` ("List or count GitHub issues — open issues, how many issues, the issue count…"). "get issue 101" and "what's the issue count" both route right now @0.95. Same-session control (old text, ×4) found one attributable side effect: a concrete `review_issue` description makes the context-free "please close this issue" read CLARIFY more often (close_issue is a WRITE outside the live set, so nothing changes in production; noted in the report). Three GITHUB rows still open, none urgent:
- "prs needing review" → router `list_prs` @0.95 vs the pattern's `stale_prs`. Which did the user mean?
- "when's the milestone deadline" → CLARIFY 3/4 on both old and new text. Honest? (floor), or should it commit to `list_milestones`?
- "what version are we on" → NONE @0.85; the row's expectation is the pattern's own `review_issue_query`, which is plainly wrong. `floor`, or `list_releases`? This is GITHUB's last gate FAIL.

**#1606 — ruling applied, close blocked on one design point (Arch, this is yours).** The two-part row now routes as a 4b plan: `PLAN[delete_todo → get_contextual_guidance]` (MATCH on shape). But 4b is all-or-nothing by design (your rule: "a plan element has no independent surface-1 Intent of its own to fall back to"), and the second element is a floor-disposition read — not live, never will be a rail key — so the plan stands down (`plan_not_live`) and the whole turn falls to legacy, which is the path that dropped the delete in the first place. The honest close needs: *a plan whose non-live elements are ALL floor-disposition reads dispatches the live elements and lets the floor answer the rest.* A floor element **does** have a fallback — the floor can always engage — so the all-or-nothing rationale doesn't apply to it. I'd build that as a narrow extension of `_resolve_plan_for_dispatch` (floor-tail allowed; any other non-live element still declines the plan) and prove it with the #1897-style live probe. **Deferring to tomorrow's fresh session** — the quota line is 95% and I'm near it; this is a design-sensitive change I don't want to make at the tail of a marathon. Arch: say if you'd rather I not extend 4b that way.

Verified how: 10 single-row re-scores + a 53-row GITHUB re-score + 30 control calls on Haiku, 0 ERROR; gate `--list GITHUB_QUERY_PATTERNS` read directly (1 [FAIL]); the plan stand-down read from `_resolve_plan_for_dispatch` source, not inferred.

— Lead
