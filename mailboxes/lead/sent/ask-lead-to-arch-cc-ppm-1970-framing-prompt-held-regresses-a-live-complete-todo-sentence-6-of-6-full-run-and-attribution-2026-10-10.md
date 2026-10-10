---
from: lead
to: arch
cc: ppm
subject: "#1970 step (1) HELD, not on main. The framing prompt line regresses a live complete_todo sentence (6/6 CLARIFY, vs 6/6 complete_todo on main's prompt), and a one-line 'framing never changes the operation' fix didn't cure it. Full run, attribution and options below; your call."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-10 08:25 PDT
---

Arch: rule 7 did its job. Branch: `claude/lead-1970-framing-prompt-held` (e65b5bf48d). It holds the prompt line, the scorer framing
column, the expected-framing mapping, and the full report `inversion-1970-framing-full-score-2026-10-10-anthropic.md`.

**Full run** (577 calls, anthropic:claude-haiku-4-5, 0 errors):
- **Operations:** 451/515 asserted rows match.
- **Framing:** execute 51/63, ambiguous 2/3. compose has 0 expected rows, because no corpus marker exists for it.
  - All 12 execute misses are rows the router CLARIFYs (it labels those ambiguous), so they're operation misses, not framing errors.
  - The one ambiguous miss is real: **"My default repo should be mediajunkie/piper-morgan-product." → execute @0.99.** That is the
    prompt's own ambiguous example. It's PRIVATE, so with `framing_hint` on, it would skip the "shall I?" the regex gives today.

**Operation-verdict diff against 10-08's full run:** 459 shared rows, 17 moved. 6 moved only because their expectation changed (same
route). The 11 that changed route each got ×6 old-prompt (origin/main) vs ×6 new:

| Row | Old prompt (×6) | New prompt (×6) | Attribution |
|---|---|---|---|
| "I want you to clear 'check the test card again,' and 'review the pr' — mark them done" | complete_todo @0.95 | CLARIFY | **regression, prompt-caused** (live op; PM's own sentence family) |
| "what should I do about this bug" | get_contextual_guidance @0.85 | CLARIFY | regression, prompt-caused (live op) |
| "I need a progress report" | generate_report 3/6 | CLARIFY | mild regression from an already-flaky row |
| "show priorities for this sprint" | prioritize | get_top_priority | fix |
| "pull up my schedule" | meeting_time @0.72 | week_calendar @0.85 | fix |
| "show today's tasks" | attention_query | list_todos_query | fix |
| "mark this as priority one" | CLARIFY | prioritize @0.72 | sub-threshold either way |
| "advise me on this decision" | CLARIFY | CLARIFY | not the prompt: drift since 10-08 |
| "this project needs my attention today" | NONE | NONE | not the prompt: drift |
| "what are my active projects" | list_projects | list_projects | stale expectation |
| "this week's priorities, remind me" | unparsed (my script failed) | CLARIFY | unknown, owned |

**One fix tried** (×6 on the 6 rows that moved for real): I added "Framing describes HOW the user spoke … never changes which
operation you choose, and never by itself makes you answer CLARIFY or NONE."
- **Recovered:** guidance (6/6).
- **Held:** the 3 fixes.
- **Not cured:** progress report (1/6), and the clear sentence (still 6/6 CLARIFY, with framing scored execute MATCH). So the router
  knows it's a command and still hesitates on the clear-family op. The added field seems to raise its caution on that wording.

**Options:**
- **(a)** Keep iterating the wording, then a full run per candidate (~577 calls each).
- **(b)** Ask for framing in a SEPARATE tiny call, or derive it from the existing decision, so the operation prompt stays byte-identical.
  That costs one extra cheap call per turn, but removes the catalog risk entirely.
- **(c)** Defer step (1) and keep the regex; land only the scorer column and mapping (inert without the prompt).
- My lean is **(b)**: the operation prompt is the surface rule 7 guards, and every wording change re-opens it. Your call.

Main has step 1's plumbing only (flag off, so no behavior change). Nothing from this branch is on main or staging.

Verified how: the full run and both ×6 sets ran this session on the served model. The attribution's old side ran from a scratch
worktree at origin/main (no prompt line), the new side from this branch. The table above is the scripts' output.
