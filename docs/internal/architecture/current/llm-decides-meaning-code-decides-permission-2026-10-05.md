# LLM decides meaning, code decides permission

**Author**: Arch · **Date**: 2026-10-05 · **Asked by**: PM (via Lead), after the 10-05 live round on alpha v169
**Status**: advice and a proposed sequence. The direction is PM's call; the per-op rulings are Arch's and take effect unless PM says otherwise.

PM, after the round: *"It sometimes feels like we are mostly just encumbering an LLM with a bunch of limitations that are not
providing any visible value."* And: *"I would not use this product."*

This is my candid answer.

---

## 1. Short answer

**You're right about half the deterministic layer, and that half is the one you can see.**

Over the past year we built two different kinds of code around the LLM and talked about them as one thing:

| Kind | What it does | Examples | Verdict |
|---|---|---|---|
| **Permission code** | Decides what is *allowed* and makes it safe | who the caller is; whose data a request may touch; "are you sure?" before deleting; one place where every action is dispatched and logged; refusing honestly when something is unavailable; CI and deploy gates | **Keep.** It has earned its keep, this week included. The new MCP connection cannot show one person another's data; a repo unlink now asks before it runs; a red main can no longer reach testers. The LLM must not decide these things. |
| **Interpretation code** | Decides what the user *meant* | regexes that guess which items "the first three" refers to, whether "clear" means done or delete, whether a trailing word is a project name | **Retire it, faster than we have been.** Every interpretation failure in today's round came from this kind of code. It is what makes Piper feel like a robot. |

**The inversion (epic 0) was the right move, but we have only applied it to half the problem.** We moved *which action* the user
wants from regexes to the LLM: the pattern ceiling went 567 → about 120 in two weeks. We have not yet moved *which things the action
applies to*. The LLM already works that out on every turn, and the code discards it. That is the gap you hit.

---

## 2. What today's round actually showed

Seven failures, three kinds:

- **Plumbing, three failures (github 404 shape, "get issue 101", Radar).** Two paths built the same request differently, and one of
  them dropped your message on the floor. This is a cost of running the old path and the new path side by side during the migration. It is
  fixed at the source, and the cure is to finish converging on one path.
- **Missing lookup, one failure (default repo by short name).** Fixed with a lookup against your actual repos, not a pattern.
- **Interpretation, two failures ("the first three", the clear-family request).** These are the real signal. The fix Lead could have
  shipped was two more regexes that would pass the test card. **Lead held them, rightly.** That is the old approach, and passing the card
  with it would have been the wrong fix.

**And one failure of ours that matters more than any of these:** the checks we ran before asking you to test confirmed that each request
reached the right *action*. They never checked the *answer you would see*. So "ready" meant something narrower than you took it to mean. That changes now (section 4).

---

## 3. The rule going forward

> **The LLM decides meaning. Code decides permission, checks meaning against real data, and shows you before it acts.**

For "Mark the first three complete and leave the fourth pending":
1. **The LLM interprets** which items "the first three" and "the fourth" are. It already does this on every turn.
2. **Code resolves** that against your real todo list: do those items exist, are they yours, is the set unambiguous? This is lookup, not guessing.
3. **Code shows you** before acting: *"Complete these three: A, B, C? I'll leave D."* For anything destructive, this confirm is the safety. It
   turns an interpretation mistake into a visible question instead of a wrong action.
4. **Code executes** exactly what you approved.

The confirm is what makes it safe to trust the LLM with meaning. An LLM misreading costs you one "no". A regex misreading costs you a
silently wrong action, and that is what today's clear-family turn did when it completed a todo called "it".

---

## 4. Sequence (each step has a named "done")

1. **Converge on one request shape** (days). Every path into an action carries the same information, pinned by an enforcement test so a
   second path cannot drop fields again (#1942's follow-up). **And redefine "ready to test"**: a live check that runs *your test-card
   phrasings* and asserts the *answer you would see*, not the route. We don't ask you to test until that check passes.
2. **Arguments flip for the two ops that failed** (about a week): `complete_todo` and the clear family consume the LLM's extracted
   targets (ordinals, ranges, names, exception lists), resolved against real data and shown in the confirm. Gate: the same discipline as
   the pattern deletions (corpus rows with expected target sets, scored on the model alpha actually serves, then a live served-answer
   check), then the floor-internal regexes those ops used are deleted.
3. **The other write actions follow, one at a time**, on the same gate.
4. **Count the interpretation regexes still living inside handlers and make the count only go down**, the same ratchet that took the
   pre-classifier from 567 to ~120. Today, two handler files alone hold ~34 regex call sites that no ratchet counts.

**What stays deterministic, permanently:** identity and data ownership; consent and confirmation before changes; the single dispatch
path; honest refusal copy; lookups against real data; CI and deploy gates. These are boundaries. They are cheap to keep, and an LLM
should not be trusted with them.

---

## 5. What I got wrong

I approved deletions and rail entries this week by checking routes and code paths. I did not insist that the evidence include *the answer
a user sees*. Three of my own rulings on 10-04 had to be corrected because I ruled before reading everything they touched. The habit I'm
keeping from it: **a change isn't verified until the user-visible answer is.** That applies to my reviews as much as to Lead's probes.

---

**Verified how**: `git grep inversion_args services/`: written at `inversion_live.py:1233` and `intent_service.py:15677`, read nowhere.
Regex counts by `grep` in `todo_handlers.py` (6 compiled + 10 inline) and `reminder_clear.py` (17 compiled + 1 inline). The failure list and
PM's words are from Lead's 16:48 memo (PM's transcript plus alpha logs), cited as Lead's. Pattern ceiling: 567 on 09-25 → 155 on 10-03 → Lead's
~110–120 estimate for this week (gate output, not re-run here). Layer: source plus the mail record.
