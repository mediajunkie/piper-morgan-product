# Ship #050 window date error — root cause (2026-07-08)

**Status**: Diagnosed. Fix under discussion (see decisions.log for outcome once decided).
**Diagnosed by**: Exec, at PM's request, after PM caught the wrong window during Ship #050 draft review.

## What happened

Ship #050's public draft and internal synthesis were both built around the wrong review window — "Jun 27–Jul 3" — when the correct Friday-through-Thursday span was **Jun 26–Jul 2**. All 6 leadership roles (HOST, CIO, Comms, CXO, PPM, Arch) submitted their §0 workstream reports using the wrong window, uniformly, on both ends. Exec's own synthesis inherited it without independent verification.

## This was not 6 independent mistakes

A uniform one-day shift, in the same direction, across 6 separately-authored submissions, is not the signature of 6 people independently miscounting. It's the signature of one shared bad input.

## Root cause, evidenced

1. **The original kickoff (Fri Jul 3, 07:38 PT) was correct.** Exec's own session log from that morning records: *"Ship #050 kickoff issued (window Jun 26–Jul 2)."* That's the right span.
2. **The kickoff memo was never delivered — it was a casualty of that week's outage, not a discipline lapse.** (Corrected 7/8, second pass, connecting two findings.) All six recipient copies of the kickoff were among the **34 never-committed mailbox drafts** Exec found in its own worktree at the 7/6 START — files from the Jul 1–4 window where session logs narrated "sent" but the `mail-send.sh` push never actually completed. That window was the compound-disruption stretch PM has since named: the Jun 26 machine-sleep outage's aftermath, the July 4th holiday gap, the account-migration discontinuities, and the lean throttle, overlapping. Every prior Ship (#045–#049) has a durably committed, delivered kickoff; #050's delivery silently failed inside the disruption, and the failure wasn't noticed until the residue cleanup on 7/6 — by which point nobody realized one of those 34 dead files had been load-bearing. **Consequence: the roles never received the correct window at all.** All six §0 submissions postdate the Jul 5 follow-up memo; it was not a louder restatement that won out over the original — it was the only statement of the window that ever reached them.
3. **Two days later (Sun Jul 5), Exec sent a follow-up memo** (`memo-exec-to-leads-ship050-section-due-now-2026-07-05.md`) to fix an unrelated problem — PM had flagged that the "due Monday" framing was legitimizing a delay. That memo, unprompted, also restated the review window — and got it wrong. It asserts *"Thursday's logs closed on Jul 3"* (Jul 3, 2026 is a Friday; Jul 2 is the actual Thursday — verified independently via `date(2026,7,3).strftime('%A')`), and its fill-in-the-blank template bakes in "Jun 27–Jul 3" directly.
4. **The likely mechanism**: without a committed original to check against, Exec re-derived the window from memory two days out and conflated "the day the kickoff was issued" (Jul 3) with "the last day of the window being reported on" (should have been Jul 2, the day *before* the kickoff). Treating Jul 3 as the closing Thursday and counting back 6 days lands exactly on Jun 27 — precisely the wrong start-date everyone used.
5. **Telling detail**: in the very same commit, Exec also produced a second document (a git-record scaffold) that used the *correct* window, Jun 26–Jul 2, four separate times. The error wasn't a case of having forgotten the right dates — it was localized specifically to the act of writing that one memo's restated-window prose, without rereading a durable source.
6. **All 6 roles correctly and reasonably trusted the memo they received.** 5 of 6 §0 submissions match the wrong window as an exact string; CXO's frontmatter explicitly names the Jul 5 memo as `in-reply-to`. Nobody ignored the original kickoff — the wrong window is the only one that existed in any committed, rereadable form by the time they wrote their reports.

## The reframe

This was not a discipline lapse by 6 agents who should have checked dates more carefully. It was a single-point-of-failure in a system that's *supposed* to work by trust: roles aren't meant to independently re-derive the Ship window from scratch each time — they're meant to rely on the kickoff. That's correct design. What failed was that the kickoff's own content wasn't durably anchored anywhere, so a later, unrelated correction could silently replace it with a wrong value that then had nothing to be checked against.

Consistent with this week's other findings (the connector-count and invite-gate date-bleed in the Ship draft itself): the fix that matters is removing the step where a human has to remember/recompute correctly, not asking people to be more careful.

## Fix disposition (updated 7/8 after PM discussion)

PM's framing, adopted: this was an **exogenous compound event disrupting a process that has worked reliably** — Ships #045–#049 all ran with correct windows and delivered kickoffs. Don't overlearn; the question is earthquake-proofing vs. repair-readiness, and the answer here is mostly repair-readiness — much of which was already built this week as a side effect of fixing other things:

- **Detection of silent delivery failure**: the verify-at-START discipline Exec adopted 7/6 (fetch + behind-check + untracked-residue check as the first move of every fire) catches the exact failure class that ate the kickoff, within one fire instead of 5 days.
- **Delivery verification at send time**: `mail-send.sh` v3 already prints an explicit `pushed <sha> → origin/main ✓` confirmation; the norm is to treat its absence as failure, not assume success.
- **The one nearly-free hardening**: when issuing a Ship kickoff, compute the window formulaically from the prior Ship (+7 days), assert day-of-week (Friday start, Thursday end) before sending, and confirm the push landed. Folded into Exec's own Friday kickoff procedure — no new skill or script surface needed for this.

The broader "what should be skillified, on what cadence" question was spun out of this incident into its own standing PM+Exec conversation — see `docs/internal/operations/skill-candidates-review.md`.
