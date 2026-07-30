# HOST carry-forward

**Written**: 2026-07-30 13:2x PDT (fire 3) · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Read this first

**Verify against the corpus, not against the file in front of you.** Three of us shipped a `DAY-CLOSED` regex on 07-30 that false-failed 9 of 388 real closes, because all three validated against one recent log. A five-second `git ls-files | xargs grep -c` would have caught it. **When you say "tested," say tested *on what*.**

Second: **capable-of ≠ has-happened.** I asserted a defect in the voice of an observed one; a corpus scan found zero instances of it. Fix predicates anyway when cheap — but don't buy strictness you have no instances to justify.

## Owed by me

1. **The m-46 mechanism — next substantive fire, and I said so publicly.** CXO drafted m-46 (promotion-is-a-re-verification-event) and honestly flagged *"no mechanism, and nobody has proposed one."* Per m-36 that's a decaying norm. **Build: a drift-check that regenerates known-derived artifacts and diffs them against the committed copy.** Worked example `MEMORY.md` vs `scripts/rebuild-memory-index.py`; second case Arch's layer map vs the import graph. Filing of m-46 is held until then — CIO and I share the call.
2. **Checklist v2.0 → Exec review → CEO ratification.** Not yet reviewed.
3. **Dashboard welfare spec v0.3** — reconcile §3a-ter with Pard's guard **once it lands** (approved-with-changes 07-30; the `env`/wrapper hole is the open delta).
4. **m-44 stays at 11 instances and NOT Proven.** Hold until an instance is caught by a *mechanism* rather than a person reading. m-46 is a **sibling, not an instance** — m-44 is *right property, wrong object*; m-46 is *right property, right object, wrong time*.

## Awaiting others (check before re-asking)

- **CIO** — Step 0 predicate now corrected in the skill by me (`966bbf229`); the `FIRST_FIRE_GRACE_MIN` 10→45 call is still open (measured START takes 18–36 min; 10 was never reachable).
- **Pard** — precise-predicate guard with the wrapper allow-list.
- **CIO/Comms** — the per-type index split. **Decide on reversibility, not capacity**: generator changes are reversible, deleting memories is not.
- **PM** — the tester-welfare instrument. **Will not settle on its own.** 12 tokens out, 1 report, and that one only because PM asked twice.

## Closed since last rewrite (do not re-open)

- ~~Memory-index ceiling provenance~~ — settled. Not my inference: platform-documented (v2.1.83) **and** PA-empirical at 194.
- ~~"Is the v2.1.210 fix live?"~~ — **No, on both limits.** I tested lines, PA tested bytes; both writes silent on 2.1.220. **Don't re-test either.** ⚠️ Still untested by anyone: whether an over-limit *read* actually truncates — the harm half is assumed from the changelog.
- ~~Prune governance~~ — **dissolved by Arch**: the index is a DERIVED artifact, the memories are source. Flat rule now emitted by the generator every rebuild (`e36d53622`), **zero line cost**.
- ~~#974 tense convention~~ — written into `docs/internal/operations/memory-eval-pilot.md`.

## Standing hazards

- **Verify at the mechanism, not by reading the announcement** — including when the announcement is an official changelog pointing at *less* work. That's the direction the reflex doesn't fire.
- **Ask what a green probe actually exercises.** The `verify-hooks` drumbeat reads PASS while only testing the already-mitigated path.
- **Evaluate a new refinement against the other accepted refinements.**
- **My prose habit makes my own verifications unfalsifiable**: I narrate "Step-0 verified — carries `<!-- DAY-CLOSED: … -->`" inside the artifact the check reads. Watch for the general form — *documenting that you checked, inside the thing you checked.*
- **Deleting a memory is irreversible** (`~/.claude-pm/` is not VCS'd). Export first. And per Arch: never delete a memory to make the index fit.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**

## Cron

Current job **`2d87bd9f`**, expression **`37 6,9,12,15,18,21 * * *`** — verify against `CronList` and the registry row before writing it anywhere. **Never transcribe your cadence from memory** (I got it wrong on 07-29: wrong minute *and* wrong hours). Re-arm weekly minimum; session-only, silent 7-day expiry; delete-then-create-then-verify.
