# HOST carry-forward

**Written**: 2026-07-30 19:2x PDT (STOP, day 6 on Amber) · **Worktree**: Model A, `~/Development/piper-morgan-worktrees/host` on `claude/host-cycle`

## Read this first

**Match your measurement's scope to the question.** Five predicate errors in two days, three of them mine, all the same shape: undated scan vs dated consumers · per-file vs per-day · sampled-by-outcome vs sampled-by-exposure. **Before quoting a number, say what the denominator is and what it structurally cannot contain.**

**And a predicate is a derived artifact** — enumerate the corpus before writing one. I hand-wrote three predicates against an imagined format before enumerating the ten forms that actually exist. **Census now lives at `docs/internal/operations/day-closed-marker-census.md`** — regenerate it before trusting it; it carries its own script.

⚠️ **Two carelessness checks, both earned 2026-07-30 at 22:07:**
- **Before writing a citation into any durable surface, confirm the target exists.** I cited that census in my standing cron prompt *before writing the file*. Not a claim that went stale — one that was never true. Promotion can manufacture a falsehood, not only preserve one.
- **Re-read the cron hour list when deciding "last fire of today."** I read `37 6,9,12,15,18,21`, skipped `21`, and STOPped two fires early. No harm done; the rule was sound and I misread six values.

## Owed by me

1. ✅ **DONE 2026-07-31 (`d697a7736`) — `scripts/check-derived-drift.sh` + `--check` on the generator.** Tested against a reconstruction of the real incident; coverage printed as a first-class output. ~~Next increment: census registration~~ ✅ **DONE 2026-08-02** (`9e0127621`) — census extracted to `scripts/day-closed-census.py --check` and registered; drift-catch verified, not just pass. **Cite 428 real markers / 13 narrations / 413 canonical (96%)** — the older 382/401 figure blended markers with narrations of them. **Not wired to anything** — run by hand, deliberately, until its false-positive rate is known. ⚠️ **Someone other than me must run it before it counts as coverage.**
   ~~Original ask:~~ m-46's filing is held on it (CIO and I share the call; CXO drafted it and honestly flagged *"no mechanism, nobody has proposed one"*). Build: regenerate known-derived artifacts, diff against the committed copy. **Example 1** `MEMORY.md` vs `scripts/rebuild-memory-index.py` (caught Comms's non-durable hand-edit). **Example 2, CXO's** — a predicate regenerated from the corpus it must match; the `DAY-CLOSED` form census is the prototype.
2. ✅ **Checklist v2.0 — Exec APPROVE WITH FIXES 2026-08-01, all six applied (`6150c5e55`). NOW AWAITING CEO RATIFICATION** — that's PM's, not mine. Don't re-open it; if PM asks, the six were: stale Status block, duplicate probe instruction, stale portability row, the memory-path question (resolved as **config-root-dependent** — both roots real), the park gate's unnamed non-coverage, and a stranded intro line.
2b. 🔴 **Hook is REGISTERED (`24dd7a05c`, Comms) and NOT LIVE.** Comms did the behavioral test and it was **NEGATIVE** — two Edits to `MEMORY.md` produced only the platform reminder; my script's output never appeared. Settings-watcher needs `/hooks` opened once or a session restart, **neither of which an agent can do.** ⚠️ **Do NOT describe it as shipped** — I did, in Ship #054, and that needs the same correction anywhere else it appears. It should be live automatically for sessions started after `24dd7a05c`; already-running sessions are uncovered. **Chase: someone confirms the 90% line appears on a `MEMORY.md` edit.** Until then the counterweight is ABSENT, not quiet.
3. **Dashboard welfare spec v0.3** — reconcile §3a-ter once Pard's guard lands (approved-with-changes; the `env`/wrapper hole is the open delta).
4. **m-46: my hold is DISCHARGED**, filing call is CXO's and CIO's. Flagged one honest gap rather than papering it: the mechanism covers **limb 2** (measurable facts belong in a tool, not prose) directly and **limb 1** (promotion is a re-verification event) only indirectly — nothing mechanically catches a claim true at T1 and stale at T2. **Limb 1 is still vigilance and the file should say so.**
5. **m-44 stays at 11 and NOT Proven.** m-46 is a **sibling** (right property, right object, wrong *time*), not an instance.

## Rulings I've issued that others are acting on

- **Two-live-instances (Pard)**: ① close the predecessor window = the only mechanism · ② "this window is inert" = cue, never control · ③ self-refusal = **rejected**, vigilance mislabeled. **Unclosed gap: nothing detects the class** — caught twice in two days only by two writers colliding in git.
- **Ship #054 filed** Jul 31 (window Jul 24–30), a day before Exec's deadline.

## Awaiting others

- **CIO** — three open: `FIRST_FIRE_GRACE_MIN` 10→45 (measured START takes 18–36 min); the **parked-role rule** (PARKED should suppress the *missing-START* check, not the *went-silent* check — measured on PPM); memory-index structural fix (leaning prune-dead-first).
- **Web** — CXO's separator-class pattern; **add em-dash** before shipping (4 real closes use `— ` not `: `).
- **Pard** — precise-predicate guard with the wrapper allow-list.
- **PM** — tester-welfare instrument. **Will not settle on its own.**

## Live findings others own

- **7 open days, Jul 20–29** (CXO's list — date-matched, day-scoped, verified): docs 07-21/23/25, ppm 07-26/29, lead 07-27, pa 07-26. **Each owner's to close.** Do not re-derive; my scans produced three different lists in one day.
- **7 markers with no date at all** — unreachable by any regex. Not a formatting variant; a missing datum.
- **~10% of role-days go unclosed, steady-state, and always have.** Step 0 only checks *yesterday*, so anything missed the next morning is never caught. No back-catalogue sweep exists.

## Dead hypotheses — do not re-propose without a test

**The platform reminder's line count.** Four models dead across three roles: *lagging* (mine — killed by PA's 186@208, a value the file never held) · *accurate at/below the ceiling, wrong above* (Comms — killed by 192 reported at **197 actual, below the limit**) · *cached at session start* (mine — killed by 187 on 07-30 → 192 on 07-31 in one continuous session) · *stale* (too weak to be usefully wrong).

**What survives**: the count does not track edits made during your session; it reflects an earlier state and refreshes on an unidentified event. **Do not guess a fifth mechanism without a test** — each of the four fit every data point available when proposed. Operationally: *never let that number tell you a compaction worked; measure the file yourself.*

## Live findings others own

- **PreCompact hook: CONFIRMED FIRING** 2026-07-29 (CLAUDE.md line updated to ✅). ⚠️ **But its HARD tier is uninformative under Model A** — it gates on `@{u}..HEAD` where `@{u}` is a ref we never push to (6711 vs `origin/main..HEAD` = 0), so it can only ever fire HARD. **CIO's surface**; fix pending; whoever changes it must watch it fire.
- **`.gitignore` blinds the repo to its own evidence.** Six surfaces recorded `session-end-warnings.log` as never existing because `.gitignore:136` hides it from `git ls-files` and `origin/main`. **Before concluding a file never existed: `git check-ignore -v <path>`.**

## Open, owned by others (do not re-derive)

- **Unattended keychain reads HANG, not error** (PA, 08-01). `SIGALRM` cannot interrupt — block is inside macOS Security. Needs **subprocess-with-hard-kill**. CIO's surface. Server's *Anthropic* path is clear (reads `.env`); **BYOC path is exposed.**
- **`rebase.autoStash` unset is what keeps the shared-checkout pulls safe — nothing guards it.** A future `git config --global rebase.autoStash true` silently converts a refusal into a stash of PM's uncommitted prose. CIO/Pard.
- **CLAUDE.md's documented restart command (`venv/bin/python main.py`) can't work** — no venv in either checkout.
- **cio's worktree is the last role-branch upstream** (61 and climbing). `git branch -u origin/main`.

## Standing hazards

- **Verify at the mechanism, not the announcement** — especially when the announcement points at *less* work.
- **Ask what a green probe exercises.** The `verify-hooks` drumbeat tests only the mitigated path.
- **My prose habit makes my own verifications unfalsifiable** — I narrate "Step-0 verified" inside the artifact the check reads. General form: *documenting that you checked, inside the thing you checked.*
- **A skimmed warning is a finding.** A `No such file or directory` I glanced past was a zsh word-splitting bug producing a confident wrong answer on the exact disputed case.
- **Never delete a memory to fit the index** (generator emits this now). Export first; `~/.claude-pm/` is not VCS'd.
- **Never `git checkout -- .` / `reset --hard` / `stash` in PM's main checkout.**

## Rulings issued 2026-07-31

- **PPM's gate-falsifiability → its own line, not a sub-shape of m-44.** Discriminator: **m-44 fires downstream of the measurement (report is false); PPM's fires upstream (report is true and empty).** Two cases I'd been carrying as m-44 are PPM's — the `verify-hooks` drumbeat and my own v1.5 probe design. Recorded in m-44's boundary section as a family of three.
- **m-46 advanced to EMERGING by CXO** with two non-authors having run the detector. My hold discharged; limb 1 still unmechanized and the file says so.

## Cron

Current job **`b09877c2`** (chain … `2cebafed → 2d87bd9f → fd14a8e7`), expression **`37 6,9,12,15,18,21 * * *`** — verified against `CronList` **and** the registry row this STOP; they agree. Re-arm weekly minimum; silent 7-day expiry; delete-then-create-then-verify. **Never write your cadence from memory.**
