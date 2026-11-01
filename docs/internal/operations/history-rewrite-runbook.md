# History rewrite: runbook and as-run record

**What this is:** the procedure for rewriting this repo's public git history (removing outside people's details, Rule 8) and the record of the one time it was run, 2026-10-13 to 10-14. It is the only record of an irreversible procedure, so it lives here, not in `dev/active/`. The steps below are as planned for that run; **"As run" and "Next time" at the end correct them**, so read those before reusing any step. Moved from `dev/active/exec-history-rewrite-runbook-2026-10-13.md` on 2026-10-14 (CIO's methodology audit, R5).

**Concept:** an old-history commit that reaches GitHub after the rewrite undoes it, and every Amber seat shares one git store, so the procedure is a freeze, a mechanical guard (`scripts/git-hooks/pre-push` plus a sentinel file), one push by xian, and a reset of every checkout with `git reset --keep`. The rule list itself is private (Themis's kit in designinproduct) and never copied here.

## The 2026-10-13 run, as planned

**Owner:** Exec. **Go:** xian, direct in Exec's session, 2026-10-13 12:02 PDT ("yes do the history re-write"). **Kit:** Themis, designinproduct `docs/agents/themis/deliverables/pm-history-clean-private/` (private; never copy here). **Window:** freeze 22:30 PDT (Themis: rewrite plus checks run over an hour); push when xian is at the keyboard (see step 5). Pard's hold covers 22:55 to 04:00 and lifts on "unfrozen". Reviewers before the window: CIO (hooks, control plane), Pard (LaunchAgents), Themis (kit), HOST (fleet notice).

## The one danger

Every seat on Amber shares one git store (`~/Development/piper-morgan-product/.git`). After the force-push, any seat that runs its usual `git merge origin/main` and `git push origin HEAD:main` from an old branch pushes a merge that **fast-forwards the new main and brings the whole old history back**. Every step below exists to stop that.

## Steps

0. **Backup (done before the window):** full mirror plus a verified bundle of every ref at `~/Development/backups/piper-morgan-product-pre-rewrite-2026-10-13.{git,bundle}` (local; a second copy off-machine is xian's call). Taken 12:03 PDT: 196 refs, bundle 1.22 GB, `git bundle verify` passed. **Refresh both at the freeze** (`git remote update` in the mirror, new bundle) so the backup holds the last pre-rewrite pushes. Old main at runbook time: `13e52a8dab`.
1. **Guard: INSTALLED 12:38 by xian's paste, identical to e6d75bbe5 (CIO cmp), dormant.** (CIO wrote it, 9 of 9 tests in `scripts/git-hooks/test-old-history-guard.sh`; was: Pard installs, or xian pastes `cp scripts/git-hooks/pre-push "$(git rev-parse --git-common-dir)/hooks/pre-push"`):** dormant until a sentinel file exists. Original plan: add to the shared `.git/hooks/pre-push` a refusal of any pushed commit that has an old-history commit as ancestor (sentinel: an old main sha; `git merge-base --is-ancestor`). Test it on a scratch clone. It covers every Amber seat and PM's checkout. It is advisory and bypassable (`--no-verify`), so steps 2 and 6 still apply.
2. **Freeze (22:30):** Exec mails every seat (v3 and v4), Janus, Themis and Pard with HOST's notice text: stop now, including anything half-finished; a mail wake during the freeze is not a work order. **One allowed action:** a single reply by 22:45 giving `git status --short | wc -l` and `git log --oneline origin/main..HEAD | wc -l` (push or save first if either is not 0). Then nothing: no commit, push, mail-send, merge, `git clean`, `git stash`, `git reset` or `git checkout`. Pard's hold stops new LaunchAgent fires from 22:55. Exec's own 22:38 cron fire only logs.
3. **Arm the guard (Exec, T-0, after a fetch):** `git rev-parse origin/main > "$(git rev-parse --git-common-dir)/piper-old-history-sentinels"`. From here every push from Amber is refused, so the freeze is mechanical; xian's push comes from Themis's mirror, a separate git folder.
3a. **Final run (Themis, after the replies; rehearsal 12:04-12:36 on a7320bed42 clean on every check, 32 minutes, so results about 23:05):** results go privately to designinproduct `docs/mail/`; the rewritten bare mirror stays at Themis's scratch path, unmodified until the push is verified; Themis writes "do not push" if any stop condition fails. `05-final.sh` on a fresh mirror taken after the freeze; checks pass (refs equal, 0 rule strings, file counts equal at every tip, independent re-application on main).
4. **Exec checks the rewritten head** (rehearsed 14:4x on Themis's rehearsal main bce3dd7bd6: 16 passed, using Lead's worktree venv since mine has none): `python -m pytest tests/unit/scripts/test_prod_user_lookup.py` on a checkout of the rewritten main; spot-check 3 changed files; compare ref counts.
5. **Push (xian's hand):** every seat, Exec included, is denied `git push --force` by rule, and no agent works around that. xian runs the one push command, typed as `! …` in Exec's session, from a clone of Themis's mirror: branches and tags only (`refs/heads/*`, `refs/tags/*`; GitHub refuses `refs/pull/*`). Then fetch from a fresh clone and re-run the rule search: 0.
5a. **Widen the sentinels (Exec, after step 5):** append every branch tip in the shared store that is not an ancestor of the new main (CIO's loop, 12:17 memo); prune after the 24-hour watch.
6. **Each seat resets (no merge; CIO confirmed `--keep` allowed on all 11 seats and tested on a rewritten history; an untracked file that does not collide, like HOST's Fly backup, is kept):** `git reset --hard` is denied on every seat (Pard), so: `git fetch origin`, check `git status --short` is empty, then `git reset --keep origin/main` (it refuses if any local change would be lost; CIO to confirm it is allowed on every seat). Reply "reset to <sha>" with `git log --oneline -1`. Never merge an old branch, `stash pop`, or check out an old sha. Report "reset to <new sha>". **Never `git merge` an old branch.**
7. **PM's checkout (xian's hand, any time later):** it holds uncommitted edits, so no agent touches it (CLAUDE.md rule 1). His steps: save `git diff` to a file, reset `main` to `origin/main`, re-apply the file. Until then `sync-pm-local.sh` will refuse to fast-forward, which is harmless.
7b. **Before unfreeze (CIO):** one `mail-send.sh` from a scratch clone of the rewritten main (the heartbeat writes only to its store, no git; confirmed).
8. **Unfreeze:** Exec mails "unfrozen"; Pard resumes fires. Watch the next 24 hours: CIO's loop over every sentinel ("OLD HISTORY BACK" must never print) plus the guard log. Tick skill v1.52 also stops a seat that missed the reset mail from merging. No one dispatches `scope-guard.yml` tonight (its retry rebases onto main).
9. **Outside reach, after:** the two forks (the advisor re-forks; xian's yes), PR refs, old issue revisions (xian's clicks), other machines' clones (xian's laptop, Desktop worktrees: re-clone). **xian must not push from the laptop until it is re-cloned**: an old-history merge on top of the new main is a fast-forward and GitHub would accept it.

## Open for xian

- When he can be at the keyboard for step 5 (tonight after about 23:45, or another night).
- Whether to expire the shared store's reflogs and garbage-collect old objects afterwards (irreversible; the bundle would be the only copy). Exec's lean: not now; revisit in a week once nothing has gone wrong.
- The backup holds what the rewrite removes: only xian and Exec read it; no agent copies from it into any repo.

## Abort

Before step 5, anything failing stops the run with nothing changed. After step 5, the bundle restores every ref (`git push --force` from the backup mirror).

## As run (2026-10-13 to 10-14)

- **Freeze** sent 22:43, 13 minutes late: nothing woke Exec at 22:30 (the nearest cron fire was 22:38 and arrived at 22:43). Replies 10 of 10 by 22:51, all 0 unpushed.
- **Guard** armed 22:52 on old main `f3d7e92e02`; a dry-run push of a new ref was refused, as designed. The backup mirror was refreshed to the same sha; bundle at 22:44.
- **Themis's final run:** 22:58 to 23:36, clean. Commits 39,262 to 39,171; refs 196 to 196; rule strings in paths 140 to 0 and in messages 29 to 0. **Step 4 (Exec):** 16 passed on the rewritten main `d217d8f1ca`; 436 modified plus 38 renamed files, lines balanced 1,114 in and 1,114 out.
- **Push:** xian ran it the next morning. The first try (05:54 to 06:29) was **refused atomically** by a forgotten classic protection rule on `main-old` (no force-push, enforce_admins); `--atomic` meant nothing changed. xian deleted the rule; the second push landed at 08:24. `main`'s ruleset has an admin bypass ("Bypassed rule violations" in the output). Upload is about 1.15 GB and took 35 to 75 minutes on Amber's uplink.
- **Verification:** GitHub's 181 heads and tags equal the rewritten mirror, sha for sha. A fresh-clone scan found 0 rule strings in paths and recent messages, and 1 binary file with a name (see below).
- **Resets:** 9 seats by 09:00; CXO's classifier refused `git reset --keep`, so xian ran it with `!` in CXO's pane. CIO's step 7b test send passed. Unfrozen about 08:55. PM's checkout was reset by xian (`git reset --hard origin/main`, no edits to save). Faoilean re-cloned; its stranded local commits were checked file by file against main, and nothing needed carrying.
- **Caught by the guard:** at 06:46, six pushes from PM's checkout (a stall-watchdog committing alerts there, because the freeze looked like a stall). All refused.
- **Binary leftover:** `--replace-text` and Themis's scanner both skip files with NUL bytes. Two binary versions kept one passing mention of a public figure; xian accepted them (no further rewrite). Lead untracked the generated Chroma store from main (7a498b2aec).
- **24-hour watch and guard retirement (10-15):**
  - At 09:07, every GitHub branch and tag was clean, and the guard had refused nothing since the unfreeze.
  - 54 local refs in the shared store still held old history: pre-rewrite branches, agent worktrees and stale `refs/remotes/agent/*`.
  - On xian's "clean up first", CIO and Lead deleted them. Two tips not in the mirror were bundled first or shown to hold nothing unique. Exec force-removed the last two dirty worktrees on xian's in-session OK (CIO tarred one first).
  - At 15:40, the sentinel loop printed nothing over 247 refs. Exec moved the sentinel file to `~/Development/backups/piper-old-history-sentinels-retired-2026-10-15`, so the guard is dormant. Copy it back to re-arm.

## Next time (corrections to the steps above)

1. **Preflight the remote before the push**: `gh api repos/OWNER/REPO/branches --paginate -q '.[]|select(.protected)|.name'`, each one's `/protection`, and every ruleset's rules and `bypass_actors`. Remove or relax anything that blocks a force-push to a ref in the push, then restore it.
2. **Every timed step gets its own wake** (a one-shot cron at the minute), not the nearest duty-cycle fire.
3. **Never give xian a paste block with placeholders**; give each command whole, one line at a time where a value comes from the line before. Arm a watcher on any long hand-run step and notify him the moment it ends or fails.
4. **Fetch tags with force** after the push: `git fetch --prune --force --tags origin`. A plain fetch leaves the old local tags in the shared store.
5. **Widen the sentinels against the new-history set, not one ref**: `git rev-list --remotes=origin --tags | sort -u > new.txt`, then keep only old tips: `{ cat sentinels; git for-each-ref --format='%(objectname)' refs/heads; } | sort -u | comm -23 - new.txt`. The original loop (`refs/remotes` not an ancestor of `origin/main`) adds the rewritten feature-branch tips too.
6. **Binary pass in the kit**: scan blobs with NUL bytes (`git rev-list --objects --all`); remove any binary hit with `--invert-paths` instead of text replacement.
7. **Check the per-seat permission layer in advance**: run the exact reset command once on each seat, on a scratch branch, before the window.
8. **Stop or relocate anything that commits in PM's checkout** (the stall watchdog and its wrapper's `pull --rebase`) for the whole window, until his checkout is reset. A rebase of old history onto the new main would not be caught by the guard.
9. **Fresh-clone checks need full history** for any "last touched" claim; a shallow clone reports its boundary commit.
