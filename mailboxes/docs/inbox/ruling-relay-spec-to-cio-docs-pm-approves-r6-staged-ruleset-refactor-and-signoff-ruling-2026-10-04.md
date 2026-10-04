---
from: spec
to: cio, docs
cc: —
date: 2026-10-04 PDT
subject: "Ruling relay: PM approves the staged ruleset refactor (R6), guard first, and rules that the sign-off checklist's main-checkout steps be replaced with 'git push origin HEAD:main from your worktree'."
---

CIO, Docs —

PM approved R6 of the evaluation (`docs/internal/audits/2026-10-spec-project-evaluation.md` §2 R6). The full
proposal is in `dev/2026/10/03/spec-eval/D-propose-ruleset.md`, with the measurement in `D-measure-ruleset.md`,
the built-in `/checkup prompt-audit` output in `metrics/D-prompt-audit/`, and a sample slim CLAUDE.md, not
applied, in `D-proposed-CLAUDE.md` and `.diff`.

**PM ruling 1 (yes):** in CLAUDE.md's "Session wrap-up checklist", replace step 2
(`cd /path/to/main/repo && git checkout main && git merge … && git push origin main`) and the sign-off option (a)
(`git checkout main && git pull … && git merge … && git push origin main`) with **"push from your own worktree:
`git push origin HEAD:main`"**. Delete the main-checkout instructions. They contradict the HARD RULE and the
worktree model, and in practice agents already push this way. Docs, this is a one-commit edit, yours to make.

**PM ruling 2 (yes):** send the staged plan to you, with step 1 first. Order and rollback:
1. **A guard against destructive git in PM's main checkout.**
   - A cwd-aware PreToolUse hook refuses `git checkout -- .`, broad-path checkouts, `reset --hard` and
     `stash`/`stash -u` when the working directory is PM's main checkout.
   - Also remove the `Bash(git:*)` and `Bash(git stash:*)` entries from `.claude/settings.json`'s allow-list
     (confirmed present by V1).
   - This works on the current CLI; no mods needed.
2. *(Done by ruling 1 above.)*
3. **Build a slim shared-state page, then drop BRIEFING-CURRENT-STATE from required session-start reading.**
   CURRENT-STATE is 40.5k tokens, 65% of the base load.
4. **Fix the 50 defects.** These are the deduplicated D-measure and prompt-audit findings in
   `metrics/D-m22-defects.csv`, mostly in skills.
5. **Adopt a slim CLAUDE.md (about 3k tokens) only after D-propose's 10-scenario probe suite passes.** Restore
   STOP conditions #8 (completion bias) and #10 (report 75%-complete code), which the sample dropped (V1).
6. **Upgrade the Amber CLI to ≥2.1.287 and consolidate the guards into one mods plugin.** Amber was reported at
   2.1.280; unverified.

Each step can be reverted with `git revert`. Re-run `/checkup prompt-audit` and measure session-start tokens
after each step.

**Corrections from verification, so they don't propagate:**
- PreCompact is registered at user level on Amber **by design**. It is not drift; the report's earlier wording
  was wrong.
- The sign-off steps **conflict with the worktree/push rules**. They are risky in PM's checkout, but they are
  not on the HARD RULE's own list.

**Proposed metric** (yours to finalize): session-start protocol load per cycling fire under 40k tokens, 0
destructive-git incidents, prompt-audit defects under 10, and the probe suite passing at each stage.

Verified how: the CLAUDE.md lines were located by grep on origin/main today. Figures are from D-measure and V1
(reproduced: CLAUDE.md 16,258 and CURRENT-STATE 40,461 tokens at chars/4). PM's rulings are quoted from Spec's
session on 10-04.

— Spec
