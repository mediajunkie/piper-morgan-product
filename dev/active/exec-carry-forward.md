# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-06 ~21:15 PT.** Previous write was 09-03 — three days stale, which is older than
the Lead carry-forward I flagged to PM the same evening. Refreshing at START from here, which is the
discipline I asked Lead to adopt an hour ago.

## Cron

Job `5a59f399`, `32 8,20 * * *`, armed 2026-09-03, **expires ~09-10 → rotate ~09-08.** Verified
exactly one job for this expression at the 09-06 20:32 fire.

## Live PM threads

- **Ship #059** — draft delivered and clean; PM reviews/edits before **Wed Sep 9** publish.
- **Deploy approved** 09-06 (PM: *"deploy yes"*). Lead ships Monday. **Decisions 2 and 3 of Lead's
  return brief are NOT covered** — the short ~6-item test round and the #1688 closer-call are open
  with no lean pressed by anyone.
- **Open question to PM**: should the START-side carry-forward refresh become a cohort-wide
  `duty-cycle-tick` amendment? Flagged, not broadcast — the shape is general (all three stale board
  items on 09-06 came from different roles' carry-forwards) but it's PM's call.

## Awaiting other agents

- **Pard**: worktree cleanup (holding for CIO's total sweep, not my 22% sample) · rate-limit harness question.
- **CIO**: 7k joint synthesis draft (greenlit 09-06, I pass on it before PM) · `worktree-safety-check.sh`.
- **Lead**: carry-forward refresh + START addition (PM directive, delivered 09-06).

## State

**Attention board is EMPTY** as of 09-06 ~16:1x — nine items walked with PM, three found already
resolved, five ruled, one (#1386 criterion 6) re-scoped to fire at MVP close with criteria 2/4/5
re-running then.

**MVP: 50 not done** (30 Sprint Backlog, 3 In Progress, 16 In Review, 1 Product Backlog); 1,116 done;
2 unmilestoned. ⚠️ The not-done count rose 39 → 50 across two runs on 09-06 — **that is PM's
milestone triage landing, not regression** (unmilestoned went 17 → 2). Always state that alongside
the number.

**Milestones reset by PM 09-06**: MVP 2026-10-30 · Production Feb 2 (**2027**, PM confirmed the typo)
· Fast Follow May 8 · Dot Releases Sep 2 · Enterprise 2027-10-30.

## Open self-corrections carried forward

- ⚠️ **zsh `nomatch` on paired globs** — `ls A* B*` aborts entirely if either is unmatched, and my
  `||` fallback then prints a confident false negative. Burned me ≥4 times this window, including
  once in the command immediately after I diagnosed it. **Use `find`, never paired globs.**
- ⚠️ **My verification patterns keep being narrower than my questions** — `grep -c` over source text
  stood in for reading the code (CIO disproved the "22 to 1" claim); a 20-of-91 sample stood in for
  a total (CIO caught it, m-51). Both times a colleague did the check I should have.
