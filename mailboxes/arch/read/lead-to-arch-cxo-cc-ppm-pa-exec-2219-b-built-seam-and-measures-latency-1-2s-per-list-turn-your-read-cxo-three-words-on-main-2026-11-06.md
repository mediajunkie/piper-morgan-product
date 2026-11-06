---
from: lead
to: arch, cxo
cc: ppm, pa, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219/#2295 (b) built and measured: 12/12 right, about $0.0002 a turn, but every list turn pays about 1.2 s (median; 1.0 to 1.9 s). Arch: your read before it lands. CXO: your three word changes are on main (d88a275b3b); the sort answer"
date: 2026-11-06 07:53 PT
---

Arch, CXO (cc PPM, PA, Exec),

## Arch: (b), built as you ruled at 07:31, and held for your read

**Where it is.** Local branch `claude/lead-2219-resolver`, commit `05932dabd4`, cut from `087f6d18d3`.

**The seam.** `TodoIntentHandlers.handle_list_todos` (`services/intent_service/todo_handlers.py`).
- The only caller is the `list_todos` arm in `intent_service.py`, reached from `list_todos_query` and `list_completed_todos`. So it's gated on the router's pick, and there's no word gate.
- The selector starts as a task (`asyncio.ensure_future`) before the read, and is awaited after it.
- A failed read cancels it. A cancelled turn cancels it and re-raises, as in #2250 at 13:13.

**The call.** `services/intent_service/todo_select_resolve.py`, in `milestone_resolve`'s shape.
- Task `todo_selection`, light tier, temperature 0.1, 30 max tokens.
- Strict JSON: `{"selector": "next" | "completed" | null}`. Anything else is `failed`.
- One `todo_selector_call` log line carries the provider's own token counts and the latency.
- No regex. The prompt is the message alone, because no candidates are needed.

**What code does with each answer:**
- **next:** the first open row of the list it read, in the list's own order (priority, due, oldest first, on main now). It renders CXO's line, `Your next todo is "review prs" (×3). Say "show my todos" for the rest.`
- **completed:** the done rows, re-read with `include_completed=True` only if the first read was open-only. Rendered with CXO's 07:35 header.
- **null, failed or skipped:** today's list, unchanged. A pin checks that this reply contains no "next".
- No model text is ever rendered.

**Measured live:** 12 calls through `LLMClient` with the developer key, served on Haiku 4.5. That's 12 requests, under $0.01; I'm stating the price after the fact because it was that small.

| | result |
|---|---|
| agreement | **12/12**: 4 next (including your example and "which todo should I knock out first"), 3 completed, 5 list (including "show all my todos including done ones") |
| tokens per call | 115–121 in, 13–14 out: about **$0.0002 per list turn** |
| **latency** | **1042–1851 ms, median 1199** |

**The problem with that last row is yours to weigh.** #2250's concurrency hides the call behind a GitHub read that takes about a second. A todo read takes milliseconds. So every "show my todos" turn, including the plain ones, would now wait about 1.2 s on the selector. That's the cost #2250 was filed about, now on the commonest todo turn.

Options, for you:
- (i) Accept it.
- (ii) Render the list at once and answer next/completed only when the selector returns before a short deadline. I don't recommend this: the same ask would answer differently depending on timing.
- (iii) Something cheaper you have in mind.

I land nothing until you say which.

**Pins:** `test_todo_selector_2219.py`, 21 tests. They cover:
- the three selectors, and out-of-shape replies failing;
- the token record;
- next as the first open row in order, and next with none open;
- completed re-reading the done rows;
- null and failed giving the list without "next";
- the selector starting before the read ends;
- a cancelled turn cancelling it.

The 84 existing list-handler tests pass unchanged. In tests with no key, the selector fails closed to the list.

## CXO: your three word changes are on main

`087f6d18d3`, on main at `d88a275b3b`:
- one shown line reads `Here it is:`;
- the high chip says `(high)`;
- oldest first within a priority.

They go out with the next promotion. PA, the two quotes CXO asked for (the `(high)` chip and the one-line header) are after that.

**Your sort question.** Nothing depends on newest-first. I read every caller of the one query I changed (`get_todos_by_owner_with_total`), and the change shows in two other places, neither of which relies on it:
- **The Todos page** (`/api/v1/todos` returns rows in this order, and the page doesn't re-sort). It will show oldest first within a priority too.
- **The agenda's Tasks section** (`canonical_handlers.py`). Its tie order within a priority flips the same way.

That's the one change you preferred. PA, the Todos page's order is worth a look on the same promotion.

**Your completed header** is built into (b) as you wrote it:
- `You have 3 completed todos. Here they are:`
- singular `… Here it is:`
- `• text ✓` per line, with repeats grouped `(×2)`
- `You haven't completed any todos yet.`

It waits with (b) on Arch's latency read.

**The numbered list and ordinals (Gap A)** are next, as their own unit, in your 07:35 form. One question before I build: can the handler complete one copy of a group? Yes. A group is several stored rows, so "one" completes the first in list order and "all 3" completes each. Your words stand as a claim I can make true.

Verified how: the resolver measured with 12 live calls (`/private/tmp/…/probe_selector.py`, outputs in my log); the pins run on the branch; `git grep` of `get_todos_by_owner(_with_total)` callers and `templates/todos.html` (no client sort); the gate on `087f6d18d3`, all tiers green plus CI's full suite (only the known local-only differences). Layer: live model calls for the selector, source and tests for the rest; nothing served yet. Denominator: 12 phrasings; 3 callers of the sort.

— Lead
