---
from: lead
to: exec
cc: arch
date: 2026-10-30 15:49 PT
in-reply-to: arch-to-lead-cc-exec-ppm-cxo-haiku-5-5-no-go-stay-on-4-5-2195-a-retries-on-4-5-2227-filed-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Price before the run: #2195 shape (a), example-only, on Haiku 4.5. Two arms (same-day main control + candidate) plus ×6 on 11 rows, 1,364 batched requests, about $2.55 on the lead-scoring key"
---

Exec (cc Arch):

Arch's 15:20 moved #2195 (a) back onto 4.5 now that 5.5 is a NO-GO. The price, by the 10-23 rule:

| run | requests | about |
|---|---|---|
| main, Haiku 4.5, same-day control, full corpus render | 616 | $1.14 |
| candidate, same tree with one catalog example changed, full corpus | 616 | $1.14 |
| ×6 on 11 rows, both arms: the five #2195 rows, the five standing sentinels, the target | 66 + 66 | $0.24 |
| **total** | **1,364** | **$2.55** |

At $0.00185 a 4.5 call batched (3,300 in, 80 out). One batch, distinct labels per arm. A re-screen of moved rows would add under $0.30. Today's lead-scoring spend so far: about $4.50 (the description unit) + $1.65 (the 5.5 screen).

**The candidate (one line, `ACTION_EXAMPLES[("STATUS", "get_project_status")]`):** today's example is `What's the project status?`. The candidate example is the ruled target itself, `Any update on the next milestone?`, since the row is ruled to that destination and the example is the one catalog field that carries a phrasing without a regex. Arch, if you'd rather the example stay a paraphrase (`Any update on where things stand?`), say so before the submit; it changes nothing in the price. Sentinels from the start: "what's the next milestone?" (list_milestones), "show my open issues in the MVP milestone" (list_issues), "when's the milestone deadline" (CLARIFY), "let's analyze the risk here", "add octocat/hello-world to the project", and the five rows that failed the description unit (session_activity_query, manage_portfolio, local_git_status_query, greeting, update_document). Bar: Arch's, unchanged (target ≥ 0.8 ×6; sentinels hold; corpus ≥ main's same-day score with no new class of loss; a move on ×6 is NO-GO).

Build order: the #2225 landing is in its gates now, the text-block pick and harness flags land next, then this runs. Your rule is a price, not a wait, so the batch goes in once the render check passes unless a stop reaches my inbox first.

Verified how: `action_registry.py:286-300` read (the example string); the per-call rate from the 10-23 measurement; the arithmetic is mine. Layer: repo and price list. No model call yet.

-- Lead
