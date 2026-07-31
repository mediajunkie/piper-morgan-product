# HOST carry-forward

**Written**: 2026-07-30 19:2x PDT (STOP, day 6 on Amber) · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Read this first

**Match your measurement's scope to the question.** Five predicate errors in two days, three of them mine, all the same shape: undated scan vs dated consumers · per-file vs per-day · sampled-by-outcome vs sampled-by-exposure. **Before quoting a number, say what the denominator is and what it structurally cannot contain.**

**And a predicate is a derived artifact** — enumerate the corpus before writing one. I hand-wrote three predicates against an imagined format before enumerating the ten forms that actually exist. **Census now lives at `docs/internal/operations/day-closed-marker-census.md`** — regenerate it before trusting it; it carries its own script.

⚠️ **Two carelessness checks, both earned 2026-07-30 at 22:07:**
- **Before writing a citation into any durable surface, confirm the target exists.** I cited that census in my standing cron prompt *before writing the file*. Not a claim that went stale — one that was never true. Promotion can manufacture a falsehood, not only preserve one.
- **Re-read the cron hour list when deciding "last fire of today."** I read `37 6,9,12,15,18,21`, skipped `21`, and STOPped two fires early. No harm done; the rule was sound and I misread six values.

## Owed by me

1. **The drift-check mechanism — owed, and now has both worked examples.** m-46's filing is held on it (CIO and I share the call; CXO drafted it and honestly flagged *"no mechanism, nobody has proposed one"*). Build: regenerate known-derived artifacts, diff against the committed copy. **Example 1** `MEMORY.md` vs `scripts/rebuild-memory-index.py` (caught Comms's non-durable hand-edit). **Example 2, CXO's** — a predicate regenerated from the corpus it must match; the `DAY-CLOSED` form census is the prototype.
2. **Checklist v2.0 → Exec review → CEO ratification.** Still not reviewed.
3. **Dashboard welfare spec v0.3** — reconcile §3a-ter once Pard's guard lands (approved-with-changes; the `env`/wrapper hole is the open delta).
4. **m-44 stays at 11 and NOT Proven.** m-46 is a **sibling** (right property, right object, wrong *time*), not an instance.

## Awaiting others

- **CIO** — three open: `FIRST_FIRE_GRACE_MIN` 10→45 (measured START takes 18–36 min); the **parked-role rule** (PARKED should suppress the *missing-START* check, not the *went-silent* check — measured on PPM); memory-index structural fix (leaning prune-dead-first).
- **Web** — CXO's separator-class pattern; **add em-dash** before shipping (4 real closes use `— ` not `: `).
- **Pard** — precise-predicate guard with the wrapper allow-list.
- **PM** — tester-welfare instrument. **Will not settle on its own.**

## Live findings others own

- **7 open days, Jul 20–29** (CXO's list — date-matched, day-scoped, verified): docs 07-21/23/25, ppm 07-26/29, lead 07-27, pa 07-26. **Each owner's to close.** Do not re-derive; my scans produced three different lists in one day.
- **7 markers with no date at all** — unreachable by any regex. Not a formatting variant; a missing datum.
- **~10% of role-days go unclosed, steady-state, and always have.** Step 0 only checks *yesterday*, so anything missed the next morning is never caught. No back-catalogue sweep exists.

## Standing hazards

- **Verify at the mechanism, not the announcement** — especially when the announcement points at *less* work.
- **Ask what a green probe exercises.** The `verify-hooks` drumbeat tests only the mitigated path.
- **My prose habit makes my own verifications unfalsifiable** — I narrate "Step-0 verified" inside the artifact the check reads. General form: *documenting that you checked, inside the thing you checked.*
- **A skimmed warning is a finding.** A `No such file or directory` I glanced past was a zsh word-splitting bug producing a confident wrong answer on the exact disputed case.
- **Never delete a memory to fit the index** (generator emits this now). Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**

## Cron

Current job **`fd14a8e7`** (chain … `2cebafed → 2d87bd9f → fd14a8e7`), expression **`37 6,9,12,15,18,21 * * *`** — verified against `CronList` **and** the registry row this STOP; they agree. Re-arm weekly minimum; silent 7-day expiry; delete-then-create-then-verify. **Never write your cadence from memory.**
