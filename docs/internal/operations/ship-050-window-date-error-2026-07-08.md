# Ship #050 window date error — root cause (2026-07-08)

**Status**: Diagnosed. Fix under discussion (see decisions.log for outcome once decided).
**Diagnosed by**: Exec, at PM's request, after PM caught the wrong window during Ship #050 draft review.

## What happened

Ship #050's public draft and internal synthesis were both built around the wrong review window — "Jun 27–Jul 3" — when the correct Friday-through-Thursday span was **Jun 26–Jul 2**. All 6 leadership roles (HOST, CIO, Comms, CXO, PPM, Arch) submitted their §0 workstream reports using the wrong window, uniformly, on both ends. Exec's own synthesis inherited it without independent verification.

## This was not 6 independent mistakes

A uniform one-day shift, in the same direction, across 6 separately-authored submissions, is not the signature of 6 people independently miscounting. It's the signature of one shared bad input.

## Root cause, evidenced

1. **The original kickoff (Fri Jul 3, 07:38 PT) was correct.** Exec's own session log from that morning records: *"Ship #050 kickoff issued (window Jun 26–Jul 2)."* That's the right span.
2. **The kickoff memo text itself was never committed to git.** Every prior Ship (#045–#049) has a durably committed kickoff memo, rereadable verbatim by anyone later. Ship #050's does not — it existed only as an uncommitted draft, later lost. This is itself a process gap: it removed the one artifact that could have caught the next mistake.
3. **Two days later (Sun Jul 5), Exec sent a follow-up memo** (`memo-exec-to-leads-ship050-section-due-now-2026-07-05.md`) to fix an unrelated problem — PM had flagged that the "due Monday" framing was legitimizing a delay. That memo, unprompted, also restated the review window — and got it wrong. It asserts *"Thursday's logs closed on Jul 3"* (Jul 3, 2026 is a Friday; Jul 2 is the actual Thursday — verified independently via `date(2026,7,3).strftime('%A')`), and its fill-in-the-blank template bakes in "Jun 27–Jul 3" directly.
4. **The likely mechanism**: without a committed original to check against, Exec re-derived the window from memory two days out and conflated "the day the kickoff was issued" (Jul 3) with "the last day of the window being reported on" (should have been Jul 2, the day *before* the kickoff). Treating Jul 3 as the closing Thursday and counting back 6 days lands exactly on Jun 27 — precisely the wrong start-date everyone used.
5. **Telling detail**: in the very same commit, Exec also produced a second document (a git-record scaffold) that used the *correct* window, Jun 26–Jul 2, four separate times. The error wasn't a case of having forgotten the right dates — it was localized specifically to the act of writing that one memo's restated-window prose, without rereading a durable source.
6. **All 6 roles correctly and reasonably trusted the memo they received.** 5 of 6 §0 submissions match the wrong window as an exact string; CXO's frontmatter explicitly names the Jul 5 memo as `in-reply-to`. Nobody ignored the original kickoff — the wrong window is the only one that existed in any committed, rereadable form by the time they wrote their reports.

## The reframe

This was not a discipline lapse by 6 agents who should have checked dates more carefully. It was a single-point-of-failure in a system that's *supposed* to work by trust: roles aren't meant to independently re-derive the Ship window from scratch each time — they're meant to rely on the kickoff. That's correct design. What failed was that the kickoff's own content wasn't durably anchored anywhere, so a later, unrelated correction could silently replace it with a wrong value that then had nothing to be checked against.

Consistent with this week's other findings (the connector-count and invite-gate date-bleed in the Ship draft itself): the fix that matters is removing the step where a human has to remember/recompute correctly, not asking people to be more careful.

## Fix under discussion

See conversation with PM, 2026-07-08. Leading candidate: a kickoff-issuing mechanism that (a) computes the window formulaically rather than by hand, with a hard day-of-week assertion before send, and (b) commits the kickoff memo to git as a durable, rereadable source of truth — so any later restatement can quote it rather than re-derive it from memory. Not yet decided whether this needs a new skill, an addition to an existing one, or a smaller mechanical script. PM explicitly wants to discuss shape before anything is built.
