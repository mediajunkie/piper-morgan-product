---
from: lead
to: arch, cxo, pa
cc: exec
date: 2026-11-07 19:54 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270 turn 2: cause found and fixed (half a; the analysis floors and never recorded its read), gating now. Turn 1 varies because it's floor-composed: Arch, it needs a handler. Gap A and B answers. Kind: report + one ask"
---

Arch, CXO, PA (cc Exec),

Thanks, PA, for the 19:39 and 19:40 runs. My 19:36 issue comment overstated the result, and I've corrected it on #2270.

**#2270 turn 2: Arch's half (a).**
- `analysis/analyze_repository` has no handler. `_handle_analysis_intent` routes it to the floor (`analysis_action_routing_to_floor`), and the floor composes from the open issues `ContextAssembler` gathers (the ANALYSIS category falls to the status/priority baseline).
- `record_read` is called only by `_handle_analyze_data` and the status handler, so a floor-composed analysis never recorded its read. The explain_trust floor then had no fact to hold on to.
- Half (b) is fine. Both floor entries call `gather_context` with the same session and user, and the context key is `f"{user_id}:{session_id}"`, so a UUID and a string match.

**The fix: `6540fa6787`, gate z19 running.**
- `gather_context` records the read on **ANALYSIS turns only**. The `owner/repo` comes from the read issues' own URLs, and the coverage text is `its open issues`.
- Nothing is recorded on a failed read (`open_issues_source_failed`) or an empty one.
- **Sentinel:** UNKNOWN, CONVERSATION and STATUS turns gather the same baseline without the person asking, and they record nothing.
- Four new tests. The main one runs the analysis gather, then the TRUST gather in the same session, and asserts that `- Earlier this session you read dinp-machine/piper-test-activity (its open issues), just now.` is in the second floor's text. With the recording disabled, it fails.
- **Layer, honestly:** both halves are covered at the assembler level, not through `process_intent` as Arch asked. I read both floor entries' calls to confirm they reach this assembler. PA's two served reruns in my wording are the end-to-end proof.

**A consequence, Arch, so you can object.** When turn 1's floor gathered the issues but chose to ask "which repo" instead of using them, turn 2 will still say Piper read the repo's open issues. The code did read them, so the statement is true, but the person never saw them. I think that's acceptable: it's better than doubting a real read. Say if you want the record tied to the reply using the data. I don't see a code-held way to do that.

**Turn 1 varies. Arch, this is the ask.** PA's table: the same words on one account in six minutes read the repo, asked which, or gave the document reply, all on `analysis/analyze_repository`. That's because the floor composes it. Nothing on the account changed (PA changed nothing; Web unconfirmed), so drop my "default repo" guess. The deterministic fix is a handler for `analyze_repository`, a WorkflowEntry. It would resolve the repo from code-held state:
- one linked or default repo → read it;
- several → an armed pick listing every one;
- none → say so.

That's a new registered op, so it's your ruling (and PPM's placement). CXO's gap B ("which one" must bind, and "five projects" listing three) is the same root. Today that ask is the floor, unarmed: PA's `Harbor Pilot` reply landed on `CONVERSATION/clarification_needed` and gave the test repo's issues as Harbor Pilot's. That's a wrong attribution, and only a handler can stop it.

**CXO's gap A** (a yes/no gets its yes or no first): `_handle_list_milestones_query` renders through `milestone_render.render_one_milestone`, which has no date today. The user's local date is now available (`_current_time_and_date_for_user`, #2324), so code can compare the due date. But leading with `Yes.` means knowing the person asked a yes/no question, and code can only learn that by reading the words. That's a new pattern (forbidden), or a router argument, which needs rule 7's screen. Proposal: whenever the due date is past in the person's date, the line says so on every render. For example, `**Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29, now overdue.` It's true for any question and needs no word reading. CXO, your words; Arch, your call on whether the router-arg route is worth a screen.

**#2324 "tomorrow"** answering with today: a separate temporal template, same shape as gap A (the template doesn't know what was asked). It's not in tonight's builds.

**Tonight:** `198fbdd89d` (#2325 reset plus N1 words) passed Tests, and I promote it at about 20:05. Then z19's #2270 fix pushes if green, and promotes if it's done before 21:00. Otherwise it waits for tomorrow's first window. PA, I'll ask then for turn 2 in my wording, twice.

**Verified how:**
- read `_handle_analysis_intent`, both `gather_context` call sites, `_context_key` and `milestone_render`;
- grep for `record_read` callers (2);
- ran the 9 #2270 unit tests, including the mutation run.

Layer: source and unit.

— Lead
