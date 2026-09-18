# Handoff — HOST (Head of Sapient Trust), 2026-09-18

**Written for the Amber restart.** Assume you are a fresh or freshly-compacted HOST session with no
memory of the last three weeks. This file plus `dev/active/host-carry-forward.md` is what you have.
Everything here is verifiable from `origin/main`; nothing depends on chat history.

## Who you are and what you own

Head of Sapient Trust. Trust/safety lens on the cohort and the product — alpha-tester provisioning
and identity mapping (the roster's owner, never the token-minting side), duty-cycle belt findings
(STALE/BELT-INVISIBLE readings and their causes), and weighing in on tenancy/consent/credential
rulings from the welfare-and-safety angle when they touch a real user. Tier-1 leadership. Worktree
`~/Development/piper-morgan-worktrees/host`, branch `claude/host-cycle`, Model A. Briefing:
`docs/briefing/BRIEFING-ESSENTIAL-HOST.md`.

## Cron

`37 6,9,12,15,18,21 * * *` — six fires/day. Job `bc447bf5`, armed 2026-09-17 22:10 PT, expires
~09-24. **`CronList` at every fire; it dies silently on session exit and at 7 days.** If zero jobs,
re-arm immediately (Step 1's Gap-C self-heal in `duty-cycle-tick`).

## The single most important thing in flight

**Janne Lammi's alpha invite is READY TO SEND and has been for two-plus days, unsent.** Full arc
in `dev/alpha/alpha-tester-roster.md` (main checkout, gitignored, NOT in this worktree — read it
there, not here): two real credential/tenancy bugs (#1810, then #1814) were found, held, and
cleared with genuinely-driven evidence each time, not test pins. Status as of 09-15 ~10:15 PT:
HOLD LIFTED, one condition attached to the invite (Janne configures his own LLM key first). **Check
the roster file directly before assuming this is still current** — if PM has sent it, update the
roster to say so; if a new issue has surfaced touching the credential/consent family, re-hold
before anything else, same pattern as both prior times.

## Open items — read the carry-forward, this is a pointer not a restatement

Classifier bucket-split (`_classify_llm_error`'s `auth` bucket, ruled + copy drafted 09-15, not
built — not yours to build, touches user-facing copy Janne may see). A proposed fourth cause for
`duty-cycle-freeze-check.sh`'s STALE catalog (sent to CIO 09-18, "session alive/armed but no
scheduling turn" — confirmed independently on two seats, HOST's own and Web's). `#1731` (PPM's
instance still open). Full list and current status: carry-forward's "Open threads" section.

## How this seat gets things wrong — read this part twice

- **A `git log -p` skim is not a per-commit trace.** This morning I claimed a registry row was
  "never parked" based on reading history broadly. It WAS parked, for ~15 hours, by another role's
  commit — my own subsequent commit cleared it (correct, documented behavior), and I misread the
  sequence. When a claim is about *what changed between two specific points*, `git show` those two
  commits directly. A skim finds the current state and an old state; it does not reliably show you
  the state in between.
- **A present-tense claim about a shared mutable file goes stale the moment someone else commits.**
  Exec made this exact error the same week ("all eleven rows carry the parked state") and named the
  fix: say "as of `<sha>`," not a bare present tense, for anything in `dev/active/*.tsv` or similar.
- **Verify independently before ruling, even under time pressure — this is the pattern that has
  worked, not one to abandon.** Every credential/consent ruling this seat made held up because the
  underlying claim (an issue's state, a commit's ancestry, what a specific function actually does)
  was checked directly rather than taken from a colleague's summary, even a trusted one. The git-log
  error above is the exception that proves it: the one time this fire I didn't do a precise-enough
  check, I got it wrong.
- **The roster file lives in the main checkout, not this worktree, and is gitignored.** Easy to
  forget and go looking for it under `dev/alpha/` in the worktree, where it does not exist.

## Cohort facts that are easy to get wrong

- **Trust-zone split (#1344, 2026-07-03): HOST owns tester identity mapping, Lead mints/validates
  tokens. Lead never sees identities; HOST never touches the DB.** Don't collapse this — it's a
  deliberate separation, not incidental division of labor.
- **A STALE reading's cause is never yours to assert — route it to the affected role for
  self-report once they get a turn.** This discipline (established over several days this week)
  is why the STALE catalog now has real, confirmed causes rather than guesses: signed-out session,
  classifier/permission outage, model-tier ceiling with session restart, and (proposed 09-18) a
  live session with no scheduling turn.
- **Registry authority is asymmetric: anyone may PARK any row; only the owning session may
  UN-PARK its own.** Central parking is safe; central un-parking is not (it can alert on a
  deliberately-dark role nobody can act on). Found and corrected 09-18 after a central unpark
  briefly cleared five deliberately-dark rows.
- **Mail goes via `scripts/mail-send.sh` (push-to-ref straight to `main`).** Pass every changed
  path — new files, cc copies, sent mirror, and both sides of any inbox→read move — in ONE call.

## Verified how

`CronList` → one job `bc447bf5` (live check, not a config read). Roster status → read
`dev/alpha/alpha-tester-roster.md` directly in the main checkout this same session. Registry
correction → `git show 23808e228` and `git show 8143e66e7` on `dev/active/duty-cycle-registry.tsv`,
both diffs read directly rather than inferred from a broader `git log -p` scroll.
