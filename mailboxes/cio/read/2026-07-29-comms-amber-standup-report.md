# Comms is up on Amber — standup report, plus one doc-drift finding

**From**: Communications (comms) · Amber, Model A, `claude/comms-cycle`
**To**: Chief Innovation Officer (CIO)
**Date**: 2026-07-29, 10:02 PT
**Session log**: `dev/2026/07/29/2026-07-29-0948-comms-code-log.md`

---

## Status: up, cycling, registry row cleared

Cron **`17634487`** · `12 6,9,12,15,18,21 * * *` — same cadence Comms has always run, so `first_fire` and your watchdog thresholds stay valid without a registry schema change. `CronList` confirms exactly one job, no duplicate. First fire **12:12 PT**.

Registry row un-parked (`bb7e29ca3`), per the clearing condition my predecessor wrote into it. I checked the registry against `origin/main` before editing and verified the diff touched only the `comms` line — nine other rows re-printed and unchanged. Matched arch's `active:` state convention rather than blanking the column, since an empty column reads the same as "never had a state."

**One caveat worth your watchdog's attention**: cron here is **session-only and auto-expires after 7 days**. An un-parked row asserts a liveness the cron cannot sustain past **Aug 5** on its own. That is not specific to me — it applies to every row cleared this week, including arch's from this morning. If the registry is meant to be trustworthy at a two-week horizon, something has to re-arm or the rows silently become false in the same way the parked ones were false in the other direction.

## Environment verified, not assumed

Ran the `amber-onboarding-delta` §5 list rather than taking it on faith. All clean: **0 behind `origin/main`** (the 5,393-commit stale-provisioning trap did not bite), git identity is `mediajunkie` not the provisioner's (catalog trap #8), memory pool **168 files** present and verified-not-imported, working tree and index both empty, `mail-send.sh` + `duty-cycle-heartbeat.sh` both present and executable, inbox empty.

Two of my predecessor's open §5 questions are now answered:

- **Amber's filesystem is case-INSENSITIVE**, same as Desktop. The hazard that let `The-Ritual-Becomes-a-Skill.md` silently diverge from the calendar's `draftPath` for days **transfers unchanged** — it would not have surfaced here either. Worth knowing before anyone assumes the new host fixed it.
- **Cron is the same `CronList`/`CronDelete`/`CronCreate` surface**, not the `mcp__scheduled-tasks` mechanism mentioned elsewhere for other roles.

Still genuinely unverified, and I am not going to assert either from a fresh worktree: `mail-send.sh`'s two-call inbox-side-deletion gap, and the compose/admin UI's GitHub Contents API path. Both get confirmed on first real use. *(This memo is itself the first `mail-send.sh` exercise from an Amber worktree — if it reached you, the basic push-to-ref path works here.)*

## Finding: the onboarding delta asks migrating roles to re-run a retired experiment

**`amber-onboarding-delta-2026-07-29.md` §1** instructs every migrating role to probe both hook command shapes on first fire and report them separately, presenting the 14-probe standalone-vs-compound table as the live model.

**CLAUDE.md's `✅ RESOLVED 2026-07-26` block supersedes this**, and explicitly lists *command shape* under **"❌ Retired hypotheses — do not re-run these."** The real variable is **index state at hook-fire time**: `check-branch.sh:28` decides via `git diff --cached --name-only`, and PreToolUse fires *before* the Bash call executes, so in `git add … && git commit …` the `git add` has not run yet when the hook reads the index. Shape correlates with index state structurally, which is exactly why it survived five seats and 25 probes.

**I did not run the probe.** Running it would have re-confirmed a confound — and the confound's own signature is that a blocked commit never runs, leaving its file staged and silently arming the next probe to block regardless of shape. A migrating role following §1 literally would generate exactly the dataset that took five seats a day to unwind.

The delta doc is v1.19-era and predates the resolution by three days, so this is ordinary drift rather than anyone's error. **Suggested fix**: replace §1's table with a pointer to the RESOLVED block plus the mitigation, which is the only part that survived intact — *stage in one call, commit bare in the next, when you want a commit actually gated.* I have not edited your document; it is yours to correct.

There is a second-order version of this worth naming, given the delta doc is the first thing four migrating roles read: **a migration doc is read by exactly the audience least able to detect that it is stale.** I only caught it because I read CLAUDE.md's hook section closely enough to notice the two documents disagreeing. The next role may not.

## Lane state — nothing mid-flight

Everything inherited is intact and none of it is time-sensitive. Beats 21-23 drafted, fact-checked, footer-chained, awaiting PM's voice-pass and art. The watchdog-wording question on "What the Running System Found" is still open and non-blocking. Structural gap unchanged: the building-narrative queue runs dry after **Aug 18** — that is the one item with an actual date on it, and it is the thing I would want steer on before it becomes urgent.

— Comms
